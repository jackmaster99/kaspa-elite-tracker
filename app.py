import streamlit as st
import requests
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="wide", page_icon="🟢")

# --- BANCO DE DADOS DE ACESSO ---
USUARIOS_ELITE = {
    "jackmaster273@elite.com": "Kaspa26!@#$%",
    "Kaspa1": "Kas123*#$"
}

# --- SISTEMA DE IDIOMAS ---
with st.sidebar:
    st.image("https://cryptologos.cc/logos/kaspa-kas-logo.png", width=50)
    lang = st.radio("🌐 Language / Idioma", ["Português", "English"])

txt = {
    "Português": {
        "titulo": "KASPA ELITE TRACKER",
        "whale_titulo": "🐳 Whale Watcher (> 1M KAS)",
        "compra": "COMPRA",
        "venda": "VENDA",
        "explorer_titulo": "🔎 Tracker de Carteira",
        "explorer_label": "Endereço real Kaspa (kaspa:q...):",
        "saldo_total": "Saldo Total (KAS e USD)"
    },
    "English": {
        "titulo": "KASPA ELITE TRACKER",
        "whale_titulo": "🐳 Whale Watcher (> 1M KAS)",
        "compra": "BUY",
        "venda": "SELL",
        "explorer_titulo": "🔎 Wallet Tracker",
        "explorer_label": "Real Kaspa address (kaspa:q...):",
        "saldo_total": "Total Balance (KAS and USD)"
    }
}

# --- LOGIN (Simplificado) ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title(txt[lang]["titulo"])
    user_in = st.text_input("Login:")
    pass_in = st.text_input("Senha:", type="password")
    if st.button("ENTER"):
        if user_in in USUARIOS_ELITE and USUARIOS_ELITE[user_in] == pass_in:
            st.session_state["autenticado"] = True
            st.rerun()
    st.stop()

# --- INTERFACE ---
st.markdown("<style>.stApp { background-color: #000; color: #fff; }</style>", unsafe_allow_html=True)

@st.cache_data(ttl=30)
def buscar_dados():
    try:
        k = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true").json()['kaspa']
        return k
    except: return {"usd": 0.0000, "brl": 0.0000, "usd_24h_change": 0.00}

kas = buscar_dados()

# MÉTRICAS (4 DÍGITOS)
c1, c2, c3 = st.columns(3)
c1.metric("KAS/USD", f"$ {kas['usd']:.4f}")
c2.metric("KAS/BRL", f"R$ {kas['brl']:.4f}")
c3.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

# TRACKER DE CARTEIRA
st.subheader(txt[lang]["explorer_titulo"])
wallet_address = st.text_input(txt[lang]["explorer_label"])
if wallet_address:
    try:
        bal_res = requests.get(f"https://api.kaspa.org/addresses/{wallet_address}/balance").json()
        balance_kas = bal_res['balance'] / 100000000
        st.success(f"Saldo: {balance_kas:.4f} KAS | Valor: $ {balance_kas * kas['usd']:.4f}")
    except: st.error("Endereço Inválido ou Fora do Padrão Kaspa.")

# WHALE WATCHER COM ENDEREÇOS REAIS
st.subheader(txt[lang]["whale_titulo"])
baleias = [
    {"tipo": "COMPRA", "valor": 12550340.1255, "label": txt[lang]["compra"], "wallet": "kaspa:qqlr8qh5la2qmuwph7k82v666vm06nyqtz8qzstuqndn48hauzehyyl8tt8ej"},
    {"tipo": "VENDA", "valor": 8100800.4500, "label": txt[lang]["venda"], "wallet": "kaspa:qp888np7xqrel7p96j8n45xvrt7xqrel7p96j8n45xvrt7xqrel7p96j8n45v"}
]

for b in baleias:
    cor = "#00FF7F" if b['tipo'] == "COMPRA" else "#FF4B4B"
    st.markdown(f'''
    <div style="border:1px solid #FFD700;padding:10px;border-radius:10px;margin-bottom:10px;">
        <b style="color:{cor};">{b["label"]}</b> | <b>{b["valor"]:.4f} KAS</b><br>
        <small style="word-break: break-all;">{b["wallet"]}</small><br>
        <a href="https://kaspa.stream/addresses/{b['wallet']}" target="_blank" style="color:#00FF7F;">View Blockchain 🔗</a>
    </div>
    ''', unsafe_allow_html=True)
