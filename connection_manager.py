import MetaTrader5 as mt5
import pandas as pd
import numpy
import sys

# --- COMPATIBILIDADE NUMPY 2.X (HACK) ---
# A biblioteca MetaTrader5 procura por numpy.core, que foi removido no NumPy 2.0.
# Este código cria um alias para manter a compatibilidade no Python 3.13.
if not hasattr(numpy, "core"):
    sys.modules["numpy.core"] = numpy
    numpy.core = numpy
# ----------------------------------------

class MT5Connection:
    def __init__(self):
        self.connected = False
        # Tenta verificar se já está inicializado
        terminal_info = mt5.terminal_info()
        if terminal_info is not None and terminal_info.connected:
            self.connected = True

    def _ensure_connected(self):
        if not self.connected:
            success, _ = self.connect()
            return success
        return True
    
    def connect(self, login=None, password=None, server=None, path=None):
        """
        Inicia a conexão com o MetaTrader 5.
        """
        init_params = {}
        if path:
            import os
            # Se o usuário passou apenas a pasta, adicionamos o executável automaticamente
            if os.path.isdir(path):
                path = os.path.join(path, "terminal64.exe")
            init_params['path'] = path
        if login and password and server:
            init_params['login'] = int(login)
            init_params['password'] = password
            init_params['server'] = server

        # Aumentamos o timeout para 60 segundos (60000ms) para evitar o erro IPC no Windows
        init_params['timeout'] = 60000

        if not mt5.initialize(**init_params):
            last_error = mt5.last_error()
            return False, f"Falha na conexão: {last_error}. Dica: Abra o MetaTrader 5 manualmente como Administrador primeiro."
        
        # Verifica se estamos conectados ao servidor
        terminal_info = mt5.terminal_info()
        if terminal_info is None:
            return False, f"Não foi possível obter informações do terminal. Erro: {mt5.last_error()}"
        
        # Log de diagnóstico no console (ajuda a gente a ver qual MT5 está sendo usado)
        print(f"--- Diagnóstico MT5 ---")
        print(f"Caminho: {terminal_info.path}")
        print(f"Empresa: {terminal_info.company}")
        print(f"Conectado: {terminal_info.connected}")
        print(f"-----------------------")

        if not terminal_info.connected:
            return False, f"Terminal local detectado ({terminal_info.company}), mas não há conexão com o servidor da corretora. Verifique se o login no MT5 está ativo."
        
        self.connected = True
        return True, "Conexão estabelecida com sucesso!"

    def get_account_info(self):
        """
        Retorna informações detalhadas da conta.
        """
        if not self._ensure_connected():
            return None, "Não conectado ao MT5"
        
        account_info = mt5.account_info()
        if account_info is None:
            return None, f"Falha ao obter informações da conta: {mt5.last_error()}"
        
        # Transformando em um dicionário mais amigável
        info_dict = account_info._asdict()
        return info_dict, "Sucesso"

    def get_daily_history(self):
        """
        Busca o lucro realizado e a quantidade de trades fechados hoje com precisão.
        """
        if not self._ensure_connected():
            return 0.0, 0
            
        from datetime import datetime, timedelta
        
        # Para evitar problemas de fuso horário, buscamos um range largo e filtramos no Python
        now = datetime.now()
        start_search = now - timedelta(hours=24) # Busca as últimas 24h
        end_search = now + timedelta(hours=12)
        
        history = mt5.history_deals_get(start_search, end_search)
        
        total_pnl = 0.0
        closed_count = 0
        
        if history is not None and len(history) > 0:
            today_str = now.strftime("%Y-%m-%d")
            
            for deal in history:
                # Converte o tempo do deal (timestamp) para string de data
                deal_dt = datetime.fromtimestamp(deal.time)
                deal_date_str = deal_dt.strftime("%Y-%m-%d")
                
                # Só conta se for do dia de hoje (hora local do PC)
                if deal_date_str == today_str:
                    # No MT5, deals de saída (fechamento) registram o lucro/prejuízo final
                    if deal.entry in [mt5.DEAL_ENTRY_OUT, mt5.DEAL_ENTRY_OUT_BY, mt5.DEAL_ENTRY_INOUT]:
                        pnl = deal.profit + deal.commission + deal.swap
                        total_pnl += pnl
                        closed_count += 1
                
        return total_pnl, closed_count

    def get_open_positions(self):
        """
        Retorna as posições abertas no momento.
        """
        if not self._ensure_connected():
            return [], "Não conectado"
            
        positions = mt5.positions_get()
        if positions is None:
            return [], f"Erro ao buscar posições: {mt5.last_error()}"
            
        # Convertendo para lista de dicionários para facilitar o uso no Streamlit
        pos_list = []
        for p in positions:
            pos_list.append(p._asdict())
            
        return pos_list, "Sucesso"

    def get_candles(self, symbol, timeframe, count=100):
        """
        Busca os últimos candles de um ativo.
        """
        if not self._ensure_connected():
            return None, "Não conectado ao MT5"
            
        # Garante que o ativo está na Observação do Mercado (Importante para XP/BTG)
        if not mt5.symbol_select(symbol, True):
            return None, f"Ativo '{symbol}' não encontrado ou indisponível no seu MT5."

        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None or len(rates) == 0:
            last_err = mt5.last_error()
            return None, f"Sem histórico para {symbol}. Erro MT5: {last_err}"
            
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df, "Sucesso"

    def get_points_for_brl(self, symbol, brl_value):
        """
        Calcula quantos pontos equivalem a um valor em Reais para WIN e WDO.
        """
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return 0
        
        # Lógica B3:
        # Mini Índice: 1 ponto = R$ 0,20 (0.2 * volume)
        # Mini Dólar: 0.5 ponto = R$ 5,00 (1 ponto = R$ 10,00)
        
        if "WIN" in symbol:
            return int(brl_value / 0.20)
        elif "WDO" in symbol:
            return brl_value / 10.0
        
        return 0 # Caso não seja B3 padrão

    def translate_error(self, retcode):
        errors = {
            10013: "Seleção Inválida (Ativo ou Lote incorreto)",
            10014: "Volume de Contratos Inválido",
            10017: "Trade desabilitado pela Corretora",
            10018: "Requotes: O preço mudou rápido demais. Tente novamente.",
            10019: "Ordem Rejeitada pela Corretora (Verifique margem)",
            10027: "Auto-Trading desabilitado no Terminal MT5",
            10044: "Somente fechamento permitido (Close Only)"
        }
        return errors.get(retcode, f"Erro desconhecido ({retcode})")

    def execute_trade(self, symbol, order_type, lots, stop_loss=0, take_profit=0):
        if not self.connected:
            return None, "Não conectado"

        tick = mt5.symbol_info_tick(symbol)
        price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(lots),
            "type": order_type,
            "price": float(price),
            "sl": float(stop_loss) if stop_loss > 0 else 0.0,
            "tp": float(take_profit) if take_profit > 0 else 0.0,
            "magic": 123456,
            "comment": "InvestFácil Pro",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC, # Ajustado para XP/BTG/Brasil
        }

        result = mt5.order_send(request)
        if result is None:
             return None, "Erro crítico: MT5 não respondeu a ordem."

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            # TENTATIVA 2: Se falhar por preenchimento, tenta FOK (comum em algumas contas Demo)
            if result.retcode in [10030, 10013, 10017]: 
                request["type_filling"] = mt5.ORDER_FILLING_FOK
                result = mt5.order_send(request)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    return result, "Ordem executada (Modo FOK)!"
            
            readable_error = self.translate_error(result.retcode)
            return result, f"Falha: {readable_error}"
            
        return result, "Ordem executada com sucesso!"
            
    def modify_position(self, ticket, sl, tp):
        """ Modifica o SL/TP de uma posição aberta. """
        if not self.connected: return False, "Não conectado"
        
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "sl": float(sl),
            "tp": float(tp),
        }
        result = mt5.order_send(request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            return False, f"Falha na modificação: {mt5.last_error()}"
        return True, "Posição protegida (Breakeven)!"

    def close_position(self, ticket):
        """ Fecha uma posição específica. """
        if not self.connected: return False
        
        # Pega detalhes para saber se é Compra ou Venda para fechar invertido
        positions = mt5.positions_get(ticket=ticket)
        if not positions: return False
        pos = positions[0]
        
        # Se é COMPRA, fecha com VENDA (e vice-versa)
        type_close = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(pos.symbol).bid if type_close == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(pos.symbol).ask
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": type_close,
            "position": ticket,
            "price": price,
            "magic": pos.magic,
            "comment": "Fechamento Automático (Meta/Stop)",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        res = mt5.order_send(request)
        if res is None: 
            return False
        return res.retcode == mt5.TRADE_RETCODE_DONE

    def close_all_positions(self):
        """ Zera todas as posições abertas. """
        if not self.connected: return 0
        
        positions = mt5.positions_get()
        count = 0
        if positions:
            for p in positions:
                if self.close_position(p.ticket):
                    count += 1
        return count

    def get_performance_stats(self, days=7):
        """
        Calcula estatísticas de desempenho para o dashboard (Win Rate, Profit Factor, etc).
        """
        if not self.connected:
            return None
            
        from datetime import datetime, timedelta
        
        # Estratégia Robusta de Datas: Pega dos últimos 30 dias
        future_buffer = datetime.now() + timedelta(hours=48)
        past_buffer = datetime.now() - timedelta(days=30) 
        
        history = mt5.history_deals_get(past_buffer, future_buffer)
        
        if history is None or len(history) == 0:
             # Fallback absoluto: tenta buscar os últimos 2000 deals indiscriminadamente
             history = mt5.history_deals_get(0, 2000)
             
        if history is None or len(history) == 0:
             return {
                "total_trades": 0, "win_rate": 0, "avg_profit": 0, 
                "profit_factor": 0, "equity_curve": [], "trades": []
            }
            
        # Filtra MANUALMENTE pelo range desejado (ex: 7 dias)
        # Se for 0, traz tudo o que achou
        if days > 0:
            real_start_date = datetime.now() - timedelta(days=days)
            history = [h for h in history if datetime.fromtimestamp(h.time) >= real_start_date]
        
        # Filtra apenas deals que têm lucro real (saídas) ou ordens executadas
        # No MT5 BR (XP/BTG), deals de entrada têm lucro 0. Só os de saída contam.
            


        total_trades = 0
        wins = 0
        gross_profit = 0.0
        gross_loss = 0.0
        equity_curve = []
        cumulative_pnl = 0.0
        trades_list = []
        
        # Ordena por tempo para a curva de equity
        sorted_history = sorted(history, key=lambda x: x.time)
        
        for deal in sorted_history:
            # Filtrando por saídas (fechamentos) para garantir contagem correta
            if deal.entry in [mt5.DEAL_ENTRY_OUT, mt5.DEAL_ENTRY_OUT_BY]:
                total_trades += 1
                pnl = deal.profit + deal.commission + deal.swap
                cumulative_pnl += pnl
                
                if pnl > 0:
                    wins += 1
                    gross_profit += pnl
                else:
                    gross_loss += abs(pnl)
                
                equity_curve.append({
                    "time": datetime.fromtimestamp(deal.time).strftime("%d/%m %H:%M"),
                    "pnl": pnl,
                    "cumulative": cumulative_pnl
                })
                
                trades_list.append({
                    "type": "COMPRA" if deal.type == mt5.DEAL_TYPE_BUY else "VENDA",
                    "symbol": deal.symbol,
                    "time": datetime.fromtimestamp(deal.time).strftime("%H:%M:%S"),
                    "profit": pnl,
                    "status": "Fechado"
                })
        
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        avg_profit = (cumulative_pnl / total_trades) if total_trades > 0 else 0
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (gross_profit if gross_profit > 0 else 0)
        
        return {
            "total_trades": total_trades,
            "win_rate": win_rate,
            "avg_profit": avg_profit,
            "profit_factor": profit_factor,
            "equity_curve": equity_curve,
            "trades": trades_list[::-1] # Mais recentes primeiro
        }

    def close(self):
        """ Encerra a conexão. """
        mt5.shutdown()
        self.connected = False

    def get_trade_history(self, days=1):
        """
        Busca o histórico de ordens finalizadas.
        """
        if not self.connected:
            return []
            
        from datetime import datetime, timedelta
        from_date = datetime.now() - timedelta(days=days)
        to_date = datetime.now() + timedelta(hours=48)
        
        # Busca ordens do histórico
        history = mt5.history_deals_get(from_date, to_date)
        if history is None or len(history) == 0:
            return []
            
        trades = []
        for deal in history:
            # Mostra COMPRAS e VENDAS (mesmo as de entrada com lucro 0)
            trades.append({
                "ticket": deal.ticket,
                "symbol": deal.symbol,
                "type": "COMPRA" if deal.type == mt5.DEAL_TYPE_BUY else "VENDA",
                "price": deal.price,
                "profit": deal.profit,
                "time": datetime.fromtimestamp(deal.time).strftime("%H:%M:%S"),
                "magic": deal.magic
            })
        
        # Retorna os itens mais recentes (limite 10)
        return trades[::-1][:10]
