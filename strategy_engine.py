import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from ml_engine import MLEngine

class StrategyEngine:
    def __init__(self, mt5_connection):
        self.mt5_conn = mt5_connection
        self.magic_number = 123456
        self.ml = MLEngine()
        # Definições baseadas na Documentação 3.0 + Novas Estratégias Scalper
        self.strategies = {
            "Sentinela": {"type": "SMA", "fast": 20, "slow": 50, "profile": "Conservador"},
            "Âncora": {"type": "BREAKOUT", "period": 20, "profile": "Conservador"},
            "Camaleão": {"type": "ADAPTIVE", "base_f": 10, "base_s": 30, "profile": "Conservador"},
            "Sniper": {"type": "PULLBACK", "period": 20, "profile": "Conservador"},
            "Fênix": {"type": "SMA", "fast": 9, "slow": 21, "profile": "Agressivo"},
            "Scalper Pro": {"type": "BOLLINGER", "period": 20, "dev": 2.0, "profile": "Agressivo"},
            "Scalper Turbo": {"type": "SCALPER_RSI", "period": 14, "rsi_low": 30, "rsi_high": 70, "profile": "Agressivo"},
            "Exaustor": {"type": "REVERSION_ULTRA", "rsi_p": 2, "overbought": 95, "oversold": 5, "profile": "Agressivo"},
            "Velocity Pulse": {"type": "VOLUME_SPIKE", "mult": 2.5, "profile": "Agressivo"},
            "Breakout Vol": {"type": "BREAKOUT_VOLUME", "period": 10, "vol_mult": 1.5, "profile": "Agressivo"},
            "HFT Sim": {"type": "MICRO_SCALPER", "period": 3, "profile": "Agressivo"},
            "Tubarão": {"type": "BREAKOUT", "period": 5, "profile": "Agressivo"},
            "Relâmpago": {"type": "BREAKOUT", "period": 2, "profile": "Agressivo"},
            "Ímã": {"type": "REVERSION", "period": 200, "threshold": 0.002, "profile": "Neutro"},
            "MAESTRO (IA)": {"type": "AUTO", "profile": "Inteligente"}
        }

    def calculate_indicators(self, df, strat_name="Sentinela"):
        """Calcula indicadores específicos com blindagem contra erros de troca de estratégia."""
        strat = self.strategies.get(strat_name, self.strategies["Sentinela"])
        is_maestro = strat_name == "MAESTRO (IA)"
        
        # 1. Indicadores Base (Sempre calculados)
        high_low = df['high'] - df['low']
        high_cp = np.abs(df['high'] - df['close'].shift())
        low_cp = np.abs(df['low'] - df['close'].shift())
        df['tr'] = np.max([high_low, high_cp, low_cp], axis=0)
        df['atr'] = df['tr'].rolling(window=14).mean()
        df['vol_sma'] = df['tick_volume'].rolling(window=20).mean()

        # Médias Fixas para Análise e Filtros
        df['sma_fast_9'] = df['close'].rolling(window=9).mean()
        df['sma_slow_21'] = df['close'].rolling(window=21).mean()
        df['sma_200'] = df['close'].rolling(window=200).mean()

        # 2. Lógica Dinâmica / Condicional (Com proteção para o Maestro)
        # Se for Maestro ou estratégia de Bandas/RSI rápido
        if is_maestro or strat["type"] in ["BOLLINGER", "REVERSION_ULTRA"]:
            period = strat.get("period", 20) if not is_maestro else 20
            df['sma_mid'] = df['close'].rolling(window=period).mean()
            std = df['close'].rolling(window=period).std()
            dev = strat.get("dev", 2.0)
            df['bb_up'] = df['sma_mid'] + (std * dev)
            df['bb_low'] = df['sma_mid'] - (std * dev)

        # Se for Maestro ou Breakout
        if is_maestro or strat["type"] in ["BREAKOUT", "BREAKOUT_VOLUME"]:
            period = strat.get("period", 2) if not is_maestro else 2
            df['h_high'] = df['high'].rolling(window=period).max().shift(1)
            df['l_low'] = df['low'].rolling(window=period).min().shift(1)

        # Se for SMA manual ou Adaptativo
        if strat["type"] == "SMA":
            df['sma_fast'] = df['close'].rolling(window=strat.get("fast", 9)).mean()
            df['sma_slow'] = df['close'].rolling(window=strat.get("slow", 21)).mean()
        
        elif strat["type"] == "ADAPTIVE":
            avg_atr = df['atr'].rolling(window=50).mean()
            vol_mult = (df['atr'] / avg_atr).fillna(1.0).iloc[-1]
            df['sma_fast'] = df['close'].rolling(window=max(5, int(strat["base_f"] * vol_mult))).mean()
            df['sma_slow'] = df['close'].rolling(window=max(15, int(strat["base_s"] * vol_mult))).mean()

        # 3. RSI (Sempre útil para filtros)
        def get_rsi(p):
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=p).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=p).mean()
            rs = gain / (loss + 1e-9)
            return 100 - (100 / (1 + rs))

        df['rsi'] = get_rsi(strat.get("period", 14))
        df['rsi_fast'] = get_rsi(2)

        return df

    def select_maestro_strategy(self, df):
        """Inteligência que decide qual robô usar no momento atual."""
        last_atr = df['atr'].iloc[-1]
        avg_atr = df['atr'].tail(50).mean()
        
        # 1. Se volatilidade explodiu -> Exaustor
        if last_atr > avg_atr * 2.0:
            return "Exaustor"
        
        # 2. Se tendência forte detectada -> Relâmpago
        dist_ma = abs(df['sma_fast_9'].iloc[-1] - df['sma_slow_21'].iloc[-1])
        if dist_ma > (df['close'].iloc[-1] * 0.0005):
            return "Relâmpago"
        
        # 3. Se mercado calmo -> Scalper Pro
        return "Scalper Pro"

    def analyze_market(self, symbol, strategy_name):
        df, _ = self.mt5_conn.get_candles(symbol, mt5.TIMEFRAME_M1, 250)
        if df is None or len(df) < 20:
            return "neutral", f"IA Sincronizando: {len(df) if df is not None else 0}/20 candles..."
        
        df = self.calculate_indicators(df, strategy_name)
        last_atr = df['atr'].iloc[-1]
        avg_atr = df['atr'].tail(50).mean()
        
        if strategy_name == "MAESTRO (IA)":
            best = self.select_maestro_strategy(df)
            ml_pred = self.ml.predict(df)
            ia_tip = ""
            if ml_pred:
                ia_tip = f" | Previsão IA: {ml_pred['prediction']} ({ml_pred['confidence']:.0f}%)"
            return "success", f"💎 MAESTRO: Usando {best}{ia_tip}"

        return "success", f"💎 IA CONFIRMA: Condições ideais para {strategy_name} no perfil {self.strategies[strategy_name]['profile']}."

    def get_signal(self, symbol, strategy_name="Sentinela"):
        # Lógica para o Maestro decidir a estratégia
        is_maestro = strategy_name == "MAESTRO (IA)"
        
        df, msg = self.mt5_conn.get_candles(symbol, mt5.TIMEFRAME_M1, 250)
        if df is None or len(df) < 10: return 'NONE', "Sincronizando...", df
        
        df = self.calculate_indicators(df, strategy_name)
        
        # Filtro de Confiança IA para o Maestro
        ml_prediction = None
        if is_maestro:
            strategy_name = self.select_maestro_strategy(df)
            ml_prediction = self.ml.predict(df)
            
            # Se a IA estiver muito incerta (< 55%), melhor não operar no modo Maestro
            if ml_prediction and ml_prediction['confidence'] < 55:
                return 'NONE', f"IA Indecisa ({ml_prediction['confidence']:.0f}%): Aguardando sinal claro.", df
        
        strat = self.strategies.get(strategy_name, self.strategies["Sentinela"])
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Filtro de Volume Global
        vol_confirm = (last['tick_volume'] > last['vol_sma'] * 0.4)

        # Lógica por Tipo de Estratégia
        signal = 'NONE'
        reason = f"{strategy_name}: Monitorando..."

        if strat["type"] in ["SMA", "ADAPTIVE"]:
            if prev['sma_fast'] <= prev['sma_slow'] and last['sma_fast'] > last['sma_slow'] and vol_confirm: 
                signal, reason = 'BUY', f"Cruzamento Alta ({strategy_name})"
            elif prev['sma_fast'] >= prev['sma_slow'] and last['sma_fast'] < last['sma_slow'] and vol_confirm: 
                signal, reason = 'SELL', f"Cruzamento Baixa ({strategy_name})"

        elif strat["type"] == "BOLLINGER":
            if last['close'] < last['bb_low']: signal, reason = 'BUY', "Scalp: Retorno à média"
            elif last['close'] > last['bb_up']: signal, reason = 'SELL', "Scalp: Retorno à média"

        elif strat["type"] == "REVERSION_ULTRA":
            if last['rsi_fast'] < strat["oversold"]: signal, reason = 'BUY', f"Exaustão Baixa (RSI2: {last['rsi_fast']:.1f})"
            elif last['rsi_fast'] > strat["overbought"]: signal, reason = 'SELL', f"Exaustão Alta (RSI2: {last['rsi_fast']:.1f})"

        elif strat["type"] == "VOLUME_SPIKE":
            is_huge_vol = last['tick_volume'] > (last['vol_sma'] * strat["mult"])
            if is_huge_vol and last['close'] > last['open']: signal, reason = 'BUY', "Velocity: Surto de Compra"
            elif is_huge_vol and last['close'] < last['open']: signal, reason = 'SELL', "Velocity: Surto de Venda"

        elif strat["type"] == "REVERSION":
            dist = (last['close'] - last['sma_200']) / last['sma_200']
            if dist < -strat["threshold"]: signal, reason = 'BUY', "Ímã: Preço muito abaixo da média"
            elif dist > strat["threshold"]: signal, reason = 'SELL', "Ímã: Preço muito acima da média"

        elif strat["type"] == "BREAKOUT":
            if last['close'] > last['h_high']: signal, reason = 'BUY', f"Explosão Alta ({strat['period']}p)"
            elif last['close'] < last['l_low']: signal, reason = 'SELL', f"Explosão Baixa ({strat['period']}p)"

        elif strat["type"] == "PULLBACK":
            period = strat.get("period", 20)
            ma_val = df['close'].rolling(window=period).mean().iloc[-1]
            if prev['low'] <= ma_val and last['close'] > ma_val and last['close'] > last['open']:
                signal, reason = 'BUY', "Sniper: Pullback na Média"
            elif prev['high'] >= ma_val and last['close'] < ma_val and last['close'] < last['open']:
                signal, reason = 'SELL', "Sniper: Pullback na Média"

        elif strat["type"] == "BREAKOUT_VOLUME":
            h_high = df['high'].rolling(window=strat["period"]).max().shift(1).iloc[-1]
            l_low = df['low'].rolling(window=strat["period"]).min().shift(1).iloc[-1]
            is_vol_ok = last['tick_volume'] > (last['vol_sma'] * strat["vol_mult"])
            if last['close'] > h_high and is_vol_ok: signal, reason = 'BUY', "Breakout + Vol"
            elif last['close'] < l_low and is_vol_ok: signal, reason = 'SELL', "Breakout + Vol"

        elif strat["type"] == "MICRO_SCALPER":
            if all(df['close'].tail(3) > df['open'].tail(3)) and vol_confirm:
                signal, reason = 'BUY', "HFT Sim: Micro-Tendência Alta"
            elif all(df['close'].tail(3) < df['open'].tail(3)) and vol_confirm:
                signal, reason = 'SELL', "HFT Sim: Micro-Tendência Baixa"

        elif strat["type"] == "SCALPER_RSI":
            if last['rsi'] < strat["rsi_low"]: signal, reason = 'BUY', f"Turbo RSI: {last['rsi']:.1f}"
            elif last['rsi'] > strat["rsi_high"]: signal, reason = 'SELL', f"Turbo RSI: {last['rsi']:.1f}"

        # FILTRO FINAL: A IA precisa concordar com a direção ou estar Neutra
        if is_maestro and signal != 'NONE' and ml_prediction:
            if signal == 'BUY' and ml_prediction['prediction'] == 'BAIXA':
                return 'NONE', f"🚫 IA Filter: Operação de COMPRA vetada pela previsão de BAIXA.", df
            if signal == 'SELL' and ml_prediction['prediction'] == 'ALTA':
                return 'NONE', f"🚫 IA Filter: Operação de VENDA vetada pela previsão de ALTA.", df

        return signal, reason, df

    def run_tick(self, symbol, lots, sl_points, tp_points, daily_target, daily_stop, strategy_name="Sentinela"):
        # 0. Filtro de Horário (Proteção Opening/Closing)
        from datetime import datetime
        now = datetime.now().time()
        if now < datetime.strptime("09:05", "%H:%M").time():
            return False, "💤 AGUARDANDO: Abertura de mercado muito volátil...", None
        if now > datetime.strptime("17:50", "%H:%M").time():
            self.mt5_conn.close_all_positions()
            return False, "🛑 ENCERRADO: Fim do horário operacional.", None

        # 1. Filtro de Spread (Segurança Anti-Ruído)
        tick = mt5.symbol_info_tick(symbol)
        if tick:
            spread = tick.ask - tick.bid
            # Se spread for maior que 25% do lucro pretendido, não vale o risco no Scalping
            if spread > (tp_points * 0.25):
                return False, f"🚫 SPREAD ALTO ({spread:.1f}): Aguardando melhora...", None

        # 2. Busca sinal
        signal, reason, df = self.get_signal(symbol, strategy_name)
        
        # 3. Trava Financeira
        realized_pnl, trade_count = self.mt5_conn.get_daily_history()
        acc, _ = self.mt5_conn.get_account_info()
        
        floating_pnl = 0.0
        if acc: floating_pnl = acc['equity'] - acc['balance']
        total_pnl = realized_pnl + floating_pnl
        
        if total_pnl >= daily_target: 
            self.mt5_conn.close_all_positions()
            return False, f"🏆 META BATIDA: R$ {total_pnl:.2f}.", df
        if total_pnl <= -daily_stop: 
            self.mt5_conn.close_all_positions()
            return False, f"🛑 STOP DIÁRIO: R$ {total_pnl:.2f}.", df

        # 3. Gestão de Posição (Breakeven / Trailing Stop)
        positions, _ = self.mt5_conn.get_open_positions()
        current_pos = [p for p in positions if p['symbol'] == symbol]
        
        if current_pos:
            pos = current_pos[0]
            is_buy = pos['type'] == mt5.POSITION_TYPE_BUY
            entry = pos['price_open']
            current = pos['price_current']
            sl_current = pos['sl']
            
            p_pts = (current - entry) if is_buy else (entry - current)
            if "WIN" in symbol: p_pts = p_pts 
            if "WDO" in symbol: p_pts = p_pts * 2 
            
            # BREAKEVEN (60% do alvo)
            if p_pts >= tp_points * 0.6 and sl_current != entry:
                new_sl = entry + (10 if is_buy else -10)
                self.mt5_conn.modify_position(pos['ticket'], new_sl, pos['tp'])
                return False, f"🛡️ PROTEÇÃO: Breakeven Ativo (+10 pts)", df
            
            # TRAILING STOP (85% do alvo)
            if p_pts >= tp_points * 0.85:
                trail_sl = entry + (p_pts * 0.4 if is_buy else -p_pts * 0.4)
                if (is_buy and trail_sl > sl_current) or (not is_buy and trail_sl < sl_current):
                    self.mt5_conn.modify_position(pos['ticket'], trail_sl, pos['tp'])
                    return False, f"🔥 TRAILING: Perseguindo Lucro...", df
                
            return False, f"Monitorando {symbol} (Aberto: R$ {pos['profit']:.2f} | Total Hoje: R$ {total_pnl:.2f})", df

        # 4. Execução de Novo Sinal
        if signal == 'NONE': return False, reason, df

        tick = mt5.symbol_info_tick(symbol)
        sl = tick.ask - sl_points if signal == 'BUY' else tick.bid + sl_points
        tp = tick.ask + tp_points if signal == 'BUY' else tick.bid - tp_points
        
        success, msg = self.mt5_conn.execute_trade(symbol, mt5.ORDER_TYPE_BUY if signal == 'BUY' else mt5.ORDER_TYPE_SELL, lots, sl, tp)
        return success, msg, df
