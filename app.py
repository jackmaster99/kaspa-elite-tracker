import streamlit as st
import requests
import pandas as pd
import uuid

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="wide", page_icon="🟢")

# --- BANCO DE DADOS DE ACESSO INDIVIDUAL ---
# É aqui que você adiciona novos usuários no futuro
USUARIOS_ELITE = {
    "jackmaster273@elite.com": "Kaspa26!@#$%",
    "Kaspa1": "Kas123*#$"  # PRIMEIRO USUÁRIO DE TESTE CADASTRADO
}

# --- LÓGICA DE SESSÃO ÚNICA ---
if "device_id" not in st.session_state:
    st.session_state["device_id"] = str(uuid.uuid4())

def sistema_login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.markdown(f"""
            <div style="text-align: center; padding-top: 50px;">
                <img src="https://cryptologos.cc/logos/kaspa-kas-logo.png" width="130">
                <h1 style="color: #00FF7F; font-family: sans-serif;">KASPA ELITE TRACKER</h1>
                <p style="color: #555;">Painel de Monitoramento @jackmaster273</p>
            </div>
        """, unsafe_allow_html=True)
        
        col_l, col_c, col_r = st.columns([1,2,1])
        with col_c:
            st.markdown('<div style="background-color: #111; padding: 30px; border-radius: 15px; border: 1px solid #333;">', unsafe_allow_html=True)
            st.warning("⚠️ TERMOS: Apenas uma sessão ativa por usuário. Logins duplicados serão derrubados.")
            
            user_in = st.text_input("Login (E-mail ou Usuário):")
            pass_in = st.text_input("Senha Individual:", type="password")
            
            if st.button("DESBLOQUEAR TERMINAL"):
                if user_in in USUARIOS_ELITE and USUARIOS_ELITE[user_in] == pass_in:
                    st.session_state["autenticado"] = True
                    st.session_state["user_email"] = user_in
                    st.rerun()
                else:
                    st.error("Credenciais inválidas ou sem licença ativa.")
            st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

if sistema_login():
    # ESTILO CSS ELITE
    st.markdown("""
        <style>
        .stApp { background-color: #000; color: #fff; }
        .card { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #00FF7F; margin-bottom: 20px; }
        .whale-card { border: 1px solid #FFD700; background-color: #0a0a00; padding: 15px; border-radius: 10px; font-family: monospace; margin-bottom: 12px; }
        [data-testid="stMetricValue"] { color: #00FF7F !important; font-size: 28px !important; }
        </style>
        """, unsafe_allow_html=True)

    # BUSCA DE COTAÇÕES
    @st.cache_data(ttl=30)
    def buscar_cotacoes():
        try:
            kas = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true").json()['kaspa']
            usd_brl = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['BRL']
            return kas, usd_brl
        except:
            return {"usd": 0.0000, "brl": 0.0000, "usd_24h_change": 0.00}, 5.0000

    kas, dolar_real = buscar_cotacoes()

    # HEADER
    st.title("🟢 KASPA ELITE TRACKER")
    st.write(f"Usuário Conectado: **{st.session_state['user_email']}**")

    # 1. MÉTRICAS TÉCNICAS
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("KAS / USD", f"$ {kas['usd']:.4f}")
    c2.metric("KAS / BRL", f"R$ {kas['brl']:.4f}")
    c3.metric("USD / BRL", f"R$ {dolar_real:.4f}")
    c4.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

    st.write("---")

    # 2. CALCULADORA DE FLUXO
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧮 Calculadora de Entrada e Saída")
    col_usd, col_kas, col_brl = st.columns(3)
    
    with col_usd:
        v_usd = st.number_input("Valor em Dólar ($):", value=1000.0, step=0.0001, format="%.4f")
        st.write(f"↳ Kaspa: **{v_usd / kas['usd']:.4f} KAS**")
        st.write(f"↳ Reais: **R$ {v_usd * dolar_real:.4f}**")

    with col_kas:
        v_kas = st.number_input("Valor em Kaspa (KAS):", value=10000.0, step=0.0001, format="%.4f")
        st.write(f"↳ Dólar: **$ {v_kas * kas['usd']:.4f}**")

    with col_brl:
        v_brl = st.number_input("Valor em Real (R$):", value=5000.0, step=0.0001, format="%.4f")
        st.write(f"↳ Kaspa: **{v_brl / kas['brl']:.4f} KAS**")
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. MONITOR DE BALEIAS
    st.subheader("🐳 Whale Watcher (> 1M KAS)")
    baleias = [
        {"tipo": "COMPRA", "valor": 12550340.1255, "wallet": "kaspa:qrel...7xq", "hash": "7a3d...f92c"},
        {"tipo": "VENDA", "valor": 8100800.4500, "wallet": "kaspa:qp88...vrt", "hash": "b2c3...d0e1"}
    ]
    for b in baleias:
        cor_st = "#00FF7F" if b['tipo'] == "COMPRA" else "#FF4B4B"
        st.markdown(f"""
        <div class="whale-card">
            <b style="color:{cor_st};">{b['tipo']} DETECTADA</b> | <b>{b['valor']:.4f} KAS</b><br>
            <small>Hash: {b['hash']}</small>
        </div>
        """, unsafe_allow_html=True)

    if st.sidebar.button("LOGOUT / SAIR"):
        st.session_state["autenticado"] = False
        st.rerun()
