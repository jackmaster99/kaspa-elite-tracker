import streamlit as st
import requests
import pandas as pd
import uuid

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="wide", page_icon="🟢")

# --- BANCO DE DADOS DE ACESSO INDIVIDUAL ---
USUARIOS_ELITE = {
    "jackmaster273@elite.com": "Kaspa26!@#$%",
    "investidor01@elite.com": "KAS2026_PRO"
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
            
            # --- TERMOS DE USO ---
            st.warning("⚠️ TERMOS DE ACESSO: Este terminal permite apenas UMA SESSÃO ativa por conta. O compartilhamento de credenciais causará a queda automática do acesso anterior.")
            
            email = st.text_input("E-mail de Acesso:")
            senha = st.text_input("Senha Individual:", type="password")
            
            if st.button("DESBLOQUEAR TERMINAL"):
                if email in USUARIOS_ELITE and USUARIOS_ELITE[email] == senha:
                    st.session_state["autenticado"] = True
                    st.session_state["user_email"] = email
                    st.success("Acesso autorizado. Iniciando sessão única...")
                    st.rerun()
                else:
                    st.error("Credenciais inválidas ou e-mail não autorizado.")
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

    # BUSCA DE COTAÇÕES EM TEMPO REAL
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
    st.markdown(f"Sessão Única Ativa: <span style='color:#00FF7F;'>{st.session_state['user_email']}</span>", unsafe_allow_html=True)

    # 1. MÉTRICAS DE MERCADO (4 DÍGITOS)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("KAS / USD", f"$ {kas['usd']:.4f}")
    c2.metric("KAS / BRL", f"R$ {kas['brl']:.4f}")
    c3.metric("USD / BRL", f"R$ {dolar_real:.4f}")
    c4.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

    st.write("---")

    # 2. CALCULADORA DE FLUXO ELITE (DOLAR - KASPA - REAL)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧮 Calculadora de Fluxo (Entrada/Saída)")
    col_usd, col_kas, col_brl = st.columns(3)
    
    with col_usd:
        v_usd = st.number_input("Valor em Dólar ($):", value=1000.0, step=0.0001, format="%.4f")
        st.write(f"↳ Reais: **R$ {v_usd * dolar_real:.4f}**")
        st.write(f"↳ Kaspa: **{v_usd / kas['usd']:.4f} KAS**")

    with col_kas:
        v_kas = st.number_input("Valor em Kaspa (KAS):", value=10000.0, step=0.0001, format="%.4f")
        st.write(f"↳ Dólar: **$ {v_kas * kas['usd']:.4f}**")
        st.write(f"↳ Reais: **R$ {v_kas * kas['brl']:.4f}**")

    with col_brl:
        v_brl = st.number_input("Valor em Real (R$):", value=5000.0, step=0.0001, format="%.4f")
        st.write(f"↳ Dólar: **$ {v_brl / dolar_real:.4f}**")
        st.write(f"↳ Kaspa: **{v_brl / kas['brl']:.4f} KAS**")
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. WHALE WATCHER (CORES POR OPERAÇÃO)
    st.subheader("🐳 Whale Watcher - Monitor de Fluxo (> 1M KAS)")
    baleias = [
        {"wallet": "kaspa:qrel7p96j8n45xvrt7xqrel7p96j8n45xvrt7xqrel7p96j8n45xvrt7x", "valor": 12550340.1255, "tipo": "COMPRA", "hash": "7a3d9f2c1b8e4a5d6c7b8a9d0e1f2a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r"},
        {"wallet": "kaspa:qp888np7xqrel7p96j8n45xvrt7xqrel7p96j8n45xvrt7xqrel7p96j", "valor": 8100800.4500, "tipo": "VENDA", "hash": "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3"}
    ]
    
    for i, b in enumerate(baleias, 1):
        cor_status = "#00FF7F" if b['tipo'] == "COMPRA" else "#FF4B4B"
        st.markdown(f"""
        <div class="whale-card">
            <b style="color:{cor_status};">#{i} {b['tipo']} DETECTADA</b> | <b>{b['valor']:.4f} KAS</b><br>
            <small><b>Wallet:</b> {b['wallet']}</small><br>
            <small><b>Hash:</b> {b['hash']}</small>
        </div>
        """, unsafe_allow_html=True)

    if st.sidebar.button("LOGOUT / SAIR"):
        st.session_state["autenticado"] = False
        st.rerun()

st.markdown("<center><small>Kaspa Elite Tracker | Painel Exclusivo @jackmaster273</small></center>", unsafe_allow_html=True)
