import streamlit as st
import time
import datetime
from connection_manager import MT5Connection
from strategy_engine import StrategyEngine
import MetaTrader5 as mt5
import os
import textwrap
import plotly.graph_objects as go
import pandas as pd

# 1. Configuração da Página
st.set_page_config(
    page_title="InvestFácil Cockpit",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS MASTER (Inspirado no Modelo Premium)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0b111a !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main .block-container {padding: 1.5rem 2rem !important; max-width: 1400px !important;}

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #0d121c !important;
        border-right: 1px solid #1e293b !important;
    }
    .sidebar-category {
        color: #64748b;
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 25px 0 10px 0;
        padding-bottom: 5px;
        border-bottom: 1px solid #1e293b;
    }
    
    /* CARDS & IA */
    .cockpit-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        background: #141b26;
        padding: 1rem 1.5rem;
        border-radius: 16px;
        border: 1px solid #1e293b;
    }
    .ia-card {
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        background: #141b26;
        border: 1px solid #1e293b;
        border-left: 6px solid #3b82f6;
    }
    .ia-success { border-left-color: #00ff41 !important; box-shadow: inset 5px 0 20px rgba(0, 255, 65, 0.05); }
    .ia-warning { border-left-color: #fbbf24 !important; box-shadow: inset 5px 0 20px rgba(251, 191, 36, 0.05); }
    .ia-danger { border-left-color: #ef4444 !important; box-shadow: inset 5px 0 20px rgba(239, 68, 68, 0.05); }
    
    .premium-card {
        background: #141b26;
        border: 1px solid #1e293b;
        border-radius: 20px;
        padding: 1.5rem;
        height: 100%;
    }
    .blue-gradient-card {
        background: linear-gradient(135deg, #1e40af 0%, #111827 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    .card-label { color: #94a3b8; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.5rem; }
    .card-value { font-size: 2.2rem; font-weight: 800; display: block; }
    
    .progress-bar-bg { width: 100%; background: #1e293b; height: 8px; border-radius: 10px; margin-top: 15px; }
    .progress-bar-fill { background: #00ff41 !important; height: 100%; border-radius: 10px; box-shadow: 0 0 15px rgba(0, 255, 65, 0.5); }
    
    .chart-box { background: #141b26; border: 1px solid #1e293b; border-radius: 20px; padding: 1.5rem; margin-top: 2rem; }
    .trade-row { display: flex; justify-content: space-between; padding: 12px 10px; border-bottom: 1px solid #1e293b; font-size: 0.9rem; }
    .trade-row:last-child { border: none; }
    
    .status-pill {
        background: rgba(0, 255, 65, 0.1);
        color: #00ff41;
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 0.7rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .welcome-container { text-align: center; padding: 2rem 1rem; background: radial-gradient(circle at top, rgba(59, 130, 246, 0.05) 0%, transparent 70%); border-radius: 30px; }
    .welcome-title { font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, #3b82f6, #00ff41); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }
    
    .tour-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.5rem;
        margin-top: 3rem;
        text-align: left;
    }
    .tour-card {
        background: rgba(20, 27, 38, 0.6);
        border: 1px solid rgba(30, 41, 59, 0.8);
        padding: 1.5rem;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    .tour-card:hover { transform: translateY(-5px); border-color: #3b82f6; }
    .tour-step { color: #3b82f6; font-weight: 800; font-size: 0.8rem; margin-bottom: 10px; text-transform: uppercase; }
    .tour-icon { font-size: 1.5rem; margin-bottom: 10px; }
    
    /* ACADEMY STYLES */
    .academy-header { text-align: center; margin-bottom: 3rem; }
    .academy-card {
        background: #141b26;
        border: 1px solid #1e293b;
        border-radius: 20px;
        padding: 2rem;
        height: 100%;
        transition: all 0.3s ease;
    }
    .academy-card:hover { border-color: #3b82f6; transform: scale(1.02); }
    .academy-tag { font-size: 0.6rem; font-weight: 800; color: #3b82f6; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    .academy-title { font-size: 1.2rem; font-weight: 700; color: #fff; margin-bottom: 15px; }
    .academy-desc { font-size: 0.85rem; color: #94a3b8; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

def main():
    mt5_mgr = MT5Connection()
    engine = StrategyEngine(mt5_mgr)
    
    if 'connected' not in st.session_state:
        st.session_state.connected = False
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard" # Alterado para carregar o dashboard direto se estiver testando
    if 'algo_on' not in st.session_state:
        st.session_state.algo_on = False
    if 'sidebar_target' not in st.session_state:
        st.session_state.sidebar_target = 500.0
    if 'sidebar_stop' not in st.session_state:
        st.session_state.sidebar_stop = 200.0

    # --- HIDE SIDEBAR IF IN TOUR OR ACADEMY ---
    if st.session_state.page in ["tour", "academy"]:
        st.markdown("""
            <style>
                [data-testid="stSidebar"] { display: none !important; }
                .main .block-container { max-width: 1100px !important; margin: 0 auto; }
            </style>
        """, unsafe_allow_html=True)

    # --- SIDEBAR ---
    if st.session_state.page not in ["tour", "academy"]:
        with st.sidebar:
            st.markdown('<p style="font-size: 1.6rem; font-weight: 800; color: #3b82f6; margin-bottom: 0;">⚡ InvestFácil</p>', unsafe_allow_html=True)
            
            # CATEGORIA: CONEXÃO E BOT
            st.markdown('<div class="sidebar-category">🚀 Controle Principal</div>', unsafe_allow_html=True)
            if not st.session_state.connected:
                if st.button("🔗 CONECTAR MT5", width='stretch', type="primary", key="sidebar_connect"):
                    with st.spinner("Conectando ao MetaTrader 5..."):
                        success, msg = mt5_mgr.connect()
                        st.session_state.connected = success
                        if success: st.toast("MT5 Conectado!", icon="✅")
                        else: st.error(msg)
            else:
                if st.button("🔌 DESCONECTAR MT5", width='stretch', key="sidebar_disconnect"):
                    mt5_mgr.close()
                    st.session_state.connected = False
                    st.session_state.page = "tour"
                    st.rerun()

            # Controle do Robô via Session State para permitir desligamento automático
            algo_on = st.toggle("🤖 ATIVAR ROBÔ", value=st.session_state.algo_on, key="sidebar_algo_toggle", on_change=lambda: st.session_state.update(algo_on=not st.session_state.algo_on))
            # Sincroniza estado manual com variável local
            if st.session_state.algo_on != algo_on: st.session_state.algo_on = algo_on
            
            st.markdown('<div class="sidebar-category">🎯 Configuração</div>', unsafe_allow_html=True)
            symbol = st.text_input("Ativo", value="WDOH26", key="sidebar_symbol").upper()
            lots = st.number_input("Contratos", min_value=1, value=1, key="sidebar_lots")

            
            st.markdown('<div class="sidebar-category">🤖 Estratégia</div>', unsafe_allow_html=True)
            
            # Novo Destaque para o Maestro
            if st.checkbox("🌟 ATIVAR MODO MAESTRO (IA)", value=True, help="O robô decide a melhor estratégia automaticamente baseada no mercado."):
                strategy_name = "MAESTRO (IA)"
                st.info("🎯 Inteligência Artificial no comando da seleção de setups.")
            else:
                profile = st.radio("Perfil", ["Conservador", "Agressivo", "Neutro"], horizontal=True, key="sidebar_profile")
                
                if profile == "Conservador":
                    strategy_name = st.selectbox("Robô", ["Sentinela", "Âncora", "Camaleão", "Sniper"], key="sidebar_strat_cons")
                elif profile == "Agressivo":
                    strategy_name = st.selectbox("Robô", ["Fênix", "Scalper Turbo", "Scalper Pro", "Tubarão", "Relâmpago", "Exaustor", "Velocity Pulse", "Breakout Vol", "HFT Sim"], key="sidebar_strat_aggr")
                else:
                    strategy_name = st.selectbox("Robô", ["Ímã"], key="sidebar_strat_neut")

            # Defaults Inteligentes para Scalper
            def_tp, def_sl = 150, 100
            if strategy_name == "Scalper Turbo":
                def_tp, def_sl = 50, 50 # Scalping agressivo e rápido
                st.caption("⚡ Modo Turbo: TP/SL ajustados para 50pts.")

            # Seleção de Modo de Alvo (Pontos ou Financeiro)
            target_mode = st.radio("Definir Alvos em:", ["Pontos", "Dinheiro (R$)"], horizontal=True, key="sidebar_target_mode")
            
            # Helper para valor do ponto
            point_val = 0.20 if "WIN" in symbol else 10.0 # R$ 10 para WDO, R$ 0.20 para WIN
            
            if target_mode == "Pontos":
                tp_pts = st.number_input("Take Profit (Pts)", value=def_tp, key="sidebar_tp")
                sl_pts = st.number_input("Stop Loss (Pts)", value=def_sl, key="sidebar_sl")
                # Mostra conversão aproximada
                st.caption(f"💰 Aprox. R$ {tp_pts * lots * point_val:.2f} de ganho / R$ {sl_pts * lots * point_val:.2f} de risco")
            else:
                tp_money = st.number_input("Ganho por Trade (R$)", value=float(def_tp * lots * point_val), step=10.0, key="sidebar_tp_money")
                sl_money = st.number_input("Risco por Trade (R$)", value=float(def_sl * lots * point_val), step=10.0, key="sidebar_sl_money")
                
                # Converte de volta para pontos para o robô usar
                if lots > 0:
                    tp_pts = int(tp_money / (lots * point_val))
                    sl_pts = int(sl_money / (lots * point_val))
                else:
                    tp_pts, sl_pts = 150, 100
                    
                st.caption(f"📏 Equivalente a {tp_pts} pts / {sl_pts} pts")

            st.markdown('<div class="sidebar-category">💰 Gestão Diária</div>', unsafe_allow_html=True)
            target = st.number_input("Meta (R$)", key="sidebar_target")
            stop_limit = st.number_input("Stop (R$)", key="sidebar_stop")

            st.markdown('<div class="sidebar-category">🧠 Cérebro IA</div>', unsafe_allow_html=True)
            if st.button("🎓 TREINAR MAESTRO", width='stretch', help="Busca 2000 candles e ensina a IA a prever movimentos."):
                with st.spinner("IA Estudando o histórico... Isso pode levar 10s."):
                    train_df, err_msg = mt5_mgr.get_candles(symbol, mt5.TIMEFRAME_M1, 2000)
                    if train_df is not None:
                        # Calcula indicadores necessários para treino
                        train_df = engine.calculate_indicators(train_df, "MAESTRO (IA)")
                        success, m_log = engine.ml.train(train_df)
                        if success: st.success(m_log)
                        else: st.error(m_log)
                    else:
                        st.error(f"Erro ao buscar dados: {err_msg}")
                        st.info("Dica: Verifique se o ativo está correto ou tente um número menor de candles.")
    else:
        # Defaults for when sidebar is hidden
        algo_on = False
        symbol = "WIN$"
        strategy_name = "Sentinela"
        target = 500.0
        stop_limit = 200.0
        lots = 1
        tp_pts = 150
        sl_pts = 100

    # --- NAVEGAÇÃO DE PÁGINAS ---
    if st.session_state.page == "tour":
        tour_html = textwrap.dedent("""
            <div class="welcome-container">
                <div class="welcome-title">Cockpit InvestFácil</div>
                <p style="color: #94a3b8; font-size: 1.2rem; max-width: 700px; margin: 0 auto;">
                    Sua central de comando para trading automatizado de alta performance. 
                    Escolha um caminho para começar.
                </p>
                <div class="tour-grid">
                    <div class="tour-card" style="border-bottom: 4px solid #3b82f6;">
                        <div class="tour-step">Módulo Educativo</div>
                        <div class="tour-icon">🎓</div>
                        <div style="font-weight: 700; margin-bottom: 5px;">InvestFácil Academy</div>
                        <div style="font-size: 0.85rem; color: #94a3b8;">Aprenda os fundamentos e a psicologia por trás do trading antes de operar.</div>
                    </div>
                    <div class="tour-card" style="border-bottom: 4px solid #00ff41;">
                        <div class="tour-step">Painel de Operações</div>
                        <div class="tour-icon">📊</div>
                        <div style="font-weight: 700; margin-bottom: 5px;">Cockpit em Tempo Real</div>
                        <div style="font-size: 0.85rem; color: #94a3b8;">Acesse o painel para conectar seu MT5 e ativar suas estratégias.</div>
                    </div>
                </div>
            </div>
        """)
        st.markdown(tour_html, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🎓 ENTRAR NO ACADEMY", width='stretch', key="tour_academy_btn"):
                st.session_state.page = "academy"
                st.rerun()
        with c2:
            if st.button("📊 ENTRAR NO COCKPIT", width='stretch', type="primary", key="tour_cockpit_btn"):
                st.session_state.page = "dashboard"
                st.rerun()
        return

    elif st.session_state.page == "academy":
        from academy_content import MODULES
        
        # Initialize academy state
        if 'current_module' not in st.session_state:
            st.session_state.current_module = None
        if 'quiz_answers' not in st.session_state:
            st.session_state.quiz_answers = {}
        if 'quiz_submitted' not in st.session_state:
            st.session_state.quiz_submitted = False
        if 'completed_modules' not in st.session_state:
            st.session_state.completed_modules = set()
        
        # Academy Home
        if st.session_state.current_module is None:
            st.markdown('<div class="academy-header">', unsafe_allow_html=True)
            st.markdown('<h1 style="font-size: 2.5rem; font-weight: 900; color: #fff; margin-bottom: 10px;">🎓 InvestFácil Academy</h1>', unsafe_allow_html=True)
            st.markdown('<p style="color: #94a3b8; font-size: 1.1rem;">Domine o mercado antes de ativar suas estratégias. Complete os módulos e teste seu conhecimento!</p>', unsafe_allow_html=True)
            
            # Progress indicator
            total_modules = len(MODULES)
            completed = len(st.session_state.completed_modules)
            progress_pct = int((completed / total_modules) * 100)
            st.markdown(f'''
                <div style="margin: 20px 0;">
                    <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 5px;">Progresso Geral: {completed}/{total_modules} módulos concluídos</div>
                    <div style="background: #1e293b; border-radius: 10px; height: 8px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #3b82f6, #00ff41); height: 100%; width: {progress_pct}%; transition: width 0.3s;"></div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            if st.button("⬅️ VOLTAR AO INÍCIO", key="academy_back_btn"):
                st.session_state.page = "tour"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            # Module Grid
            a1, a2 = st.columns(2)
            module_keys = list(MODULES.keys())
            
            for idx, (key, module) in enumerate(MODULES.items()):
                col = a1 if idx % 2 == 0 else a2
                with col:
                    completed_badge = "✅ " if key in st.session_state.completed_modules else ""
                    card_html = f'''
                        <div class="academy-card" style="cursor: pointer; transition: all 0.3s; border: 2px solid {'#00ff41' if key in st.session_state.completed_modules else '#1e293b'};">
                            <div class="academy-tag">{module['tag']}</div>
                            <div class="academy-title">{completed_badge}{module['title']}</div>
                            <p class="academy-desc">{module['description']}</p>
                        </div>
                    '''
                    st.markdown(card_html, unsafe_allow_html=True)
                    if st.button(f"📖 ESTUDAR MÓDULO", key=f"study_{key}", use_container_width=True):
                        st.session_state.current_module = key
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_answers = {}
                        st.rerun()
                    st.markdown("<br>", unsafe_allow_html=True)
            return
        
        # Module Content View
        else:
            module_key = st.session_state.current_module
            module = MODULES[module_key]
            
            # Header
            st.markdown(f'''
                <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 30px; border-radius: 15px; margin-bottom: 30px;">
                    <div style="font-size: 0.8rem; color: #3b82f6; font-weight: 800; letter-spacing: 2px; margin-bottom: 10px;">{module['tag']}</div>
                    <h1 style="font-size: 2.5rem; font-weight: 900; color: #fff; margin-bottom: 10px;">{module['title']}</h1>
                    <p style="color: #94a3b8; font-size: 1.1rem;">{module['description']}</p>
                </div>
            ''', unsafe_allow_html=True)
            
            if st.button("⬅️ VOLTAR AOS MÓDULOS", key="back_to_modules"):
                st.session_state.current_module = None
                st.rerun()
            
            # Content Section - Use Streamlit container with CSS
            # Generate unique ID for this content box
            content_id = f"content_{module_key}"
            
            st.markdown(f'''
                <style>
                /* Target the specific container */
                div[data-testid="stVerticalBlock"]:has(div.{content_id}) {{
                    background: rgba(30, 41, 59, 0.4);
                    padding: 30px;
                    border-radius: 15px;
                    border-left: 4px solid #3b82f6;
                    margin-bottom: 30px;
                }}
                
                /* Style the content inside */
                div.{content_id} h2 {{
                    color: #f8fafc !important;
                    font-size: 1.8rem !important;
                    font-weight: 700 !important;
                    margin-top: 30px !important;
                    margin-bottom: 15px !important;
                }}
                div.{content_id} h3 {{
                    color: #3b82f6 !important;
                    font-size: 1.3rem !important;
                    font-weight: 600 !important;
                    margin-top: 20px !important;
                    margin-bottom: 10px !important;
                }}
                div.{content_id} p {{
                    color: #cbd5e1 !important;
                    line-height: 1.8 !important;
                    margin-bottom: 15px !important;
                }}
                div.{content_id} ul, div.{content_id} ol {{
                    color: #cbd5e1 !important;
                    line-height: 1.8 !important;
                    margin-bottom: 15px !important;
                }}
                div.{content_id} li {{
                    margin-bottom: 8px !important;
                }}
                div.{content_id} strong {{
                    color: #00ff41 !important;
                    font-weight: 700 !important;
                }}
                div.{content_id} blockquote {{
                    border-left: 3px solid #3b82f6 !important;
                    padding-left: 20px !important;
                    margin: 20px 0 !important;
                    color: #94a3b8 !important;
                    font-style: italic !important;
                }}
                div.{content_id} table {{
                    width: 100%;
                    border-collapse: collapse !important;
                    margin: 20px 0 !important;
                }}
                div.{content_id} th {{
                    background: rgba(59, 130, 246, 0.2) !important;
                    color: #f8fafc !important;
                    padding: 12px !important;
                    text-align: left;
                    border-bottom: 2px solid #3b82f6 !important;
                }}
                div.{content_id} td {{
                    color: #cbd5e1 !important;
                    padding: 10px 12px !important;
                    border-bottom: 1px solid #1e293b !important;
                }}
                div.{content_id} code {{
                    background: rgba(15, 23, 42, 0.8) !important;
                    color: #00ff41 !important;
                    padding: 2px 6px !important;
                    border-radius: 4px !important;
                    font-size: 0.9em !important;
                }}
                </style>
            ''', unsafe_allow_html=True)
            
            # Render content with marker div
            with st.container():
                st.markdown(f'<div class="{content_id}"></div>', unsafe_allow_html=True)
                st.markdown(module['content'])
            
            # Quiz Section
            st.markdown('''
                <div style="font-size: 1.8rem; font-weight: 800; color: #fff; margin-top: 50px; margin-bottom: 20px; text-align: center;">
                    🎯 Quiz de Avaliação
                </div>
                <p style="text-align: center; color: #94a3b8; margin-bottom: 30px;">Teste seus conhecimentos e complete o módulo!</p>
            ''', unsafe_allow_html=True)
            
            # Quiz Questions
            for q_idx, question in enumerate(module['quiz']):
                st.markdown(f'''
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 3px solid #3b82f6;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #f8fafc; margin-bottom: 15px;">
                            Questão {q_idx + 1}: {question['question']}
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
                
                answer = st.radio(
                    "Escolha sua resposta:",
                    question['options'],
                    key=f"q_{module_key}_{q_idx}",
                    label_visibility="collapsed"
                )
                st.session_state.quiz_answers[q_idx] = question['options'].index(answer)
                
                # Show feedback if submitted
                if st.session_state.quiz_submitted:
                    if st.session_state.quiz_answers[q_idx] == question['correct']:
                        st.success(f"✅ Correto! {question['explanation']}")
                    else:
                        st.error(f"❌ Incorreto. {question['explanation']}")
                
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Submit Button
            if not st.session_state.quiz_submitted:
                if st.button("📝 ENVIAR RESPOSTAS", type="primary", use_container_width=True):
                    st.session_state.quiz_submitted = True
                    
                    # Calculate score
                    correct_count = sum(1 for q_idx, q in enumerate(module['quiz']) 
                                      if st.session_state.quiz_answers.get(q_idx) == q['correct'])
                    total_questions = len(module['quiz'])
                    score_pct = int((correct_count / total_questions) * 100)
                    
                    # Mark as completed if passed
                    if score_pct >= 70:
                        st.session_state.completed_modules.add(module_key)
                    
                    st.rerun()
            else:
                # Show results
                correct_count = sum(1 for q_idx, q in enumerate(module['quiz']) 
                                  if st.session_state.quiz_answers.get(q_idx) == q['correct'])
                total_questions = len(module['quiz'])
                score_pct = int((correct_count / total_questions) * 100)
                
                if score_pct >= 70:
                    st.success(f'''
                        🎉 **Parabéns!** Você acertou {correct_count}/{total_questions} questões ({score_pct}%)
                        
                        Módulo concluído com sucesso! Continue aprendendo.
                    ''')
                else:
                    st.warning(f'''
                        📚 Você acertou {correct_count}/{total_questions} questões ({score_pct}%)
                        
                        Revise o conteúdo e tente novamente. É necessário 70% para concluir o módulo.
                    ''')
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 REFAZER QUIZ", use_container_width=True):
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_answers = {}
                        st.rerun()
                with col2:
                    if st.button("➡️ PRÓXIMO MÓDULO", use_container_width=True):
                        st.session_state.current_module = None
                        st.rerun()
            
            return

    # Se estiver no Dashboard mas não conectado
    if not st.session_state.connected:
        st.info("🔗 Conecte seu MetaTrader 5 na barra lateral para acessar os dados em tempo real.")
        st.warning("Verifique se o Terminal MT5 está aberto e com o 'Algo Trading' ativado.")
        if st.button("⬅️ VOLTAR AO MENU", key="dashboard_back_btn"):
            st.session_state.page = "tour"
            st.rerun()
        return

    # --- DATA FETCHING (UNIFICADO) ---
    account_info, _ = mt5_mgr.get_account_info()
    positions, _ = mt5_mgr.get_open_positions()
    trade_list = mt5_mgr.get_trade_history()
    realized_profit, finished_trades = mt5_mgr.get_daily_history()
    
    # Cálculos Financeiros
    floating_profit = 0.0
    if account_info:
        floating_profit = account_info['equity'] - account_info['balance']
    
    total_result = realized_profit + floating_profit
    ia_status, ia_msg = engine.analyze_market(symbol, strategy_name)
    
    if "event_log" not in st.session_state:
        st.session_state.event_log = []

    if algo_on:
        # Verifica se o símbolo é operável
        s_info = mt5.symbol_info(symbol)
        if s_info and s_info.trade_mode == mt5.SYMBOL_TRADE_MODE_DISABLED:
            status_msg = f"❌ ERRO: {symbol} não permite ordens. Use o contrato atual (ex: WING25)."
            df = None
        else:
            success, status_msg, df = engine.run_tick(symbol, lots, sl_pts, tp_pts, target, stop_limit, strategy_name)
            
            # Detecção de Fim de Trade (Sincronização com Contador)
            if "last_count" not in st.session_state: st.session_state.last_count = finished_trades
            
            if finished_trades > st.session_state.last_count:
                st.session_state.event_log.insert(0, {"time": datetime.datetime.now().strftime("%H:%M:%S"), "msg": f"✅ TRADE FINALIZADO: Resultado registrado no histórico!"})
                st.toast("Operação concluída com sucesso!", icon="💰")
                st.session_state.last_count = finished_trades
            
            # Trava de Meta / Stop Automática (Desliga o Botão)
            if "META BATIDA" in status_msg.upper() or "STOP DIÁRIO" in status_msg.upper():
                st.session_state.algo_on = False # Desliga a variável de controle
                st.session_state.event_log.insert(0, {"time": datetime.datetime.now().strftime("%H:%M:%S"), "msg": f"🎯 {status_msg}"})
                st.rerun()

            # Log de Atividades
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            is_important = any(x in status_msg.upper() for x in ["EXECUTADA", "PROTEÇÃO", "TRAILING", "FINALIZADO"])
            
            if is_important:
                if not st.session_state.event_log or status_msg != st.session_state.event_log[0]["msg"]:
                    st.session_state.event_log.insert(0, {"time": current_time, "msg": status_msg})
                    if "EXECUTADA" in status_msg.upper(): st.toast(status_msg, icon="🚀")
            
            if not st.session_state.event_log:
                st.session_state.event_log.insert(0, {"time": current_time, "msg": "🤖 Robô iniciado e monitorando..."})
    else:
        _, status_msg, df = engine.get_signal(symbol, strategy_name)
        status_msg = f"Scanner {strategy_name}: {status_msg}"
        
    # Aviso de Símbolo Index
    if symbol.endswith("$"):
        st.warning(f"⚠️ O ativo {symbol} é apenas para acompanhamento. Para operar, selecione o contrato do mês (ex: WING25 ou WDOG25).")

    # Header
    st.markdown(f'''
        <div class="cockpit-header">
            <div><div style="font-size: 1.3rem; font-weight: 800;">Cockpit de Operações</div>
                 <div class="status-pill">● CONEXÃO ATIVA: {account_info["login"] if account_info else "---"}</div></div>
            <div style="text-align: right;"><div style="font-size: 0.7rem; color: #94a3b8;">STATUS</div>
                 <div style="color: {"#00ff41" if algo_on else "#94a3b8"}; font-weight: 800;">{"OPERANDO" if algo_on else "EM ESPERA"}</div></div>
        </div>
    ''', unsafe_allow_html=True)

    # IA Card
    icon_map = {"success": "✅", "warning": "⚠️", "danger": "🚫", "neutral": "💎"}
    st.markdown(f'''
        <div class="ia-card ia-{ia_status}">
            <div style="display: flex; justify-content: space-between;">
                <div><div style="font-size: 0.7rem; color: #64748b;">🤖 IA ANALYST</div>
                     <div style="font-size: 1rem; font-weight: 700;">{icon_map.get(ia_status, "💎")} {ia_msg}</div></div>
                <div style="text-align: right; border-left: 1px solid #1e293b; padding-left: 20px;">
                    <div style="font-size: 0.7rem; color: #64748b;">🛰️ MONITOR</div>
                    <div style="font-size: 0.85rem; font-weight: 700; color: #00ff41;">{status_msg.upper()}</div></div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Painel de Monitor de Atividades (Mais visível)
    if st.session_state.event_log:
        st.markdown(f'''
            <div style="background: rgba(15, 23, 42, 0.8); border-left: 4px solid #3b82f6; border-radius: 4px; padding: 15px; margin-bottom: 20px;">
                <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 800; margin-bottom: 10px; letter-spacing: 1px;">🛰️ MONITOR DE ATIVIDADE EM TEMPO REAL</div>
                {"".join([f'<div style="font-size: 0.9rem; color: {"#00ff41" if "EXECUTADA" in l["msg"].upper() else "#f8fafc"}; margin-bottom: 5px; border-bottom: 1px solid #1e293b; padding-bottom: 3px;"><b>[{l["time"]}]</b> {l["msg"]}</div>' for l in st.session_state.event_log[:5]])}
            </div>
        ''', unsafe_allow_html=True)

    # Notificação Toast se houve mudança
    if algo_on and st.session_state.event_log:
        last_event = st.session_state.event_log[0]["msg"]
        if "EXECUTADA" in last_event.upper():
            st.toast(last_event, icon="🚀")

    # Metrics
    m1, m2, m3 = st.columns(3)
    prog = min(100, int((max(0, total_result) / target) * 100)) if target > 0 else 0
    with m1: 
        st.markdown(f'''
            <div class="premium-card">
                <div class="card-label">Resultado do Dia</div>
                <div class="card-value" style="color: {"#00ff41" if total_result >= 0 else "#ef4444"}">R$ {total_result:,.2f}</div>
                <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">{finished_trades} Trades Concluídos</div>
            </div>
        ''', unsafe_allow_html=True)
    with m2: 
        st.markdown(f"""
            <div class="premium-card">
                <div class="card-label">Progresso da Meta</div>
                <div class="card-value" style="color: #3b82f6; font-size: 1.8rem;">{prog}%</div>
                <div style="font-size: 0.75rem; color: #94a3b8;">Alvo: R$ {target:,.2f}</div>
                <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {prog}%"></div></div>
            </div>
        """, unsafe_allow_html=True)
    with m3: 
        wallet_val = account_info["equity"] if account_info else 0.0
        st.markdown(f'''
            <div class="premium-card blue-gradient-card">
                <div class="card-label" style="color:#fff">Carteira Real (Equity)</div>
                <div class="card-value" style="font-size: 1.6rem;">R$ {wallet_val:,.2f}</div>
                <div style="font-size: 0.75rem; color: rgba(255,255,255,0.7); margin-top: 4px;">Atualizado em Tempo Real</div>
            </div>
        ''', unsafe_allow_html=True)

    # Chart
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="card-label">Monitor em Tempo Real: {symbol} ({strategy_name})</div>', unsafe_allow_html=True)
    
    if df is not None and len(df) > 10:
        # Filtra dados válidos
        plot_df = df.copy()
        plot_df = plot_df[plot_df['close'] > 0].tail(60) # Últimos 60 minutos
        
        fig = go.Figure()
        
        # Preço Principal
        fig.add_trace(go.Scatter(x=plot_df['time'], y=plot_df['close'], name='Preço', line=dict(color='#ffffff', width=2)))
        
        # Indicadores Dinâmicos
        if 'bb_up' in plot_df.columns:
            fig.add_trace(go.Scatter(x=plot_df['time'], y=plot_df['bb_up'], name='Bollinger Up', line=dict(color='rgba(59, 130, 246, 0.5)', dash='dot')))
            fig.add_trace(go.Scatter(x=plot_df['time'], y=plot_df['bb_low'], name='Bollinger Low', line=dict(color='rgba(59, 130, 246, 0.5)', dash='dot')))
            fig.add_trace(go.Scatter(x=plot_df['time'], y=plot_df['sma_mid'], name='Média Central', line=dict(color='#fbbf24', width=1)))
        
        if 'sma_fast' in plot_df.columns and 'sma_slow' in plot_df.columns:
            fig.add_trace(go.Scatter(x=plot_df['time'], y=plot_df['sma_fast'], name='Média 9', line=dict(color='#3b82f6', width=1.5)))
            fig.add_trace(go.Scatter(x=plot_df['time'], y=plot_df['sma_slow'], name='Média 21', line=dict(color='#ef4444', width=1.5)))
        
        if 'h_high' in plot_df.columns:
            fig.add_trace(go.Scatter(x=plot_df['time'], y=plot_df['h_high'], name='Topo Recente', line=dict(color='#00ff41', width=1, dash='dash')))
            fig.add_trace(go.Scatter(x=plot_df['time'], y=plot_df['l_low'], name='Fundo Recente', line=dict(color='#ef4444', width=1, dash='dash')))

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=300,
            showlegend=False,
            xaxis=dict(showgrid=False, color='#64748b'),
            yaxis=dict(showgrid=True, gridcolor='#1e293b', zeroline=False, color='#64748b', autorange=True),
        )
        st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
    else:
        st.markdown(f'''
            <div style="height: 300px; display: flex; align-items: center; justify-content: center; background: rgba(15, 23, 42, 0.4); border-radius: 8px; border: 1px dashed #1e293b;">
                <div style="text-align: center; color: #64748b;">
                    <div style="font-size: 2rem; margin-bottom: 10px;">📡</div>
                    Sincronizando dados de {symbol}...<br>
                    Verifique se o ativo está aberto no MetaTrader.
                </div>
            </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- SEÇÃO DE DESEMPENHO (INSPIRADA NO DESIGN SOLICITADO) ---
    st.markdown('<br><div style="font-size: 1.5rem; font-weight: 800; border-bottom: 2px solid #1e293b; padding-bottom: 10px;">📉 Desempenho Histórico</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 0.85rem; color: #64748b; margin-top: 5px; margin-bottom: 20px;">Análise detalhada da lucratividade do seu robô nos últimos 7 dias.</div>', unsafe_allow_html=True)
    
    perf = mt5_mgr.get_performance_stats(days=7)
    if perf:
        # Mini Cards de Performance
        p1, p2, p3, p4 = st.columns(4)
        with p1: 
            st.markdown(f'<div class="premium-card"><div style="font-size:0.7rem; color:#64748b">Total de Trades</div><div style="font-size:1.5rem; font-weight:700;">{perf["total_trades"]}</div></div>', unsafe_allow_html=True)
        with p2: 
            color = "#00ff41" if perf["win_rate"] >= 50 else "#ef4444"
            st.markdown(f'<div class="premium-card"><div style="font-size:0.7rem; color:#64748b">Taxa de Acerto</div><div style="font-size:1.5rem; font-weight:700; color:{color}">{perf["win_rate"]:.1f}%</div></div>', unsafe_allow_html=True)
        with p3: 
            st.markdown(f'<div class="premium-card"><div style="font-size:0.7rem; color:#64748b">Lucro Médio / Trade</div><div style="font-size:1.2rem; font-weight:700;">R$ {perf["avg_profit"]:,.2f}</div></div>', unsafe_allow_html=True)
        with p4: 
            st.markdown(f'<div class="premium-card"><div style="font-size:0.7rem; color:#64748b">Fator de Lucro</div><div style="font-size:1.5rem; font-weight:700; color:#3b82f6;">{perf["profit_factor"]:.2f}</div></div>', unsafe_allow_html=True)

        # Gráfico de Curva de Patrimônio (Linear)
        if perf["equity_curve"]:
            curve_df = pd.DataFrame(perf["equity_curve"])
            fig_curve = go.Figure()
            fig_curve.add_trace(go.Scatter(
                x=curve_df['time'], y=curve_df['cumulative'],
                mode='lines+markers',
                name='Patrimônio Acumulado',
                line=dict(color='#3b82f6', width=3),
                fill='tozeroy',
                fillcolor='rgba(59, 130, 246, 0.1)'
            ))
            fig_curve.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=10, b=0),
                height=300,
                xaxis=dict(showgrid=False, color='#64748b'),
                yaxis=dict(showgrid=True, gridcolor='#1e293b', zeroline=True, zerolinecolor='#334155', color='#64748b')
            )
            st.plotly_chart(fig_curve, width='stretch')

    # --- TABELA DE TRADES RECENTES (ESTILO LISTA) ---
    st.markdown('<div style="font-size: 1.1rem; font-weight: 700; margin-top: 30px; margin-bottom: 15px;">📋 Operações Recentes</div>', unsafe_allow_html=True)
    f1, f2 = st.columns([2, 1])
    with f1:
        if perf and perf["trades"]:
            for t in perf["trades"][:5]:
                p_color = "#00ff41" if t["profit"] >= 0 else "#ef4444"
                arrow = "↑" if t["type"] == "COMPRA" else "↓"
                st.markdown(f'''
                    <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.4); border-radius: 8px; padding: 12px; margin-bottom: 8px; border-left: 4px solid {p_color};">
                        <div style="display: flex; gap: 15px;">
                            <span style="color: {p_color}; font-weight: 900;">{arrow} {t["type"]}</span>
                            <span style="color: #f8fafc; font-weight: 600;">{t["symbol"]}</span>
                            <span style="color: #64748b; font-size: 0.85rem;">{t["time"]}</span>
                        </div>
                        <div style="display: flex; gap: 20px; align-items: center;">
                            <span style="color: {p_color}; font-weight: 700;">R$ {t["profit"]:,.2f}</span>
                            <span style="font-size: 0.7rem; background: #1e293b; color: #94a3b8; padding: 2px 8px; border-radius: 4px;">CONCLUÍDO</span>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
        else:
            st.caption("Sem operações concluídas no período.")
            
    with f2:
        st.markdown('<div class="premium-card"><div class="card-label">Posições Abertas</div>', unsafe_allow_html=True)
        if positions:
            for p in positions:
                st.markdown(f'''
                    <div style="display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #1e293b;">
                        <span style="color: #f8fafc;">{p["symbol"]}</span>
                        <span style="color: {"#00ff41" if p["profit"] >= 0 else "#ef4444"}; font-weight: 700;">R$ {p["profit"]:,.2f}</span>
                    </div>
                ''', unsafe_allow_html=True)
        else:
            st.caption("Nenhuma posição ativa no momento.")
        st.markdown('</div>', unsafe_allow_html=True)

    time.sleep(1)
    st.rerun()

if __name__ == "__main__":
    main()
