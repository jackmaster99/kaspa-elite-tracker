import streamlit as st
import requests
import pandas as pd
import uuid

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
        "login_msg": "Acesso Elite @jackmaster273",
        "calc_titulo": "🧮 Calculadora de Fluxo",
        "whale_titulo": "🐳 Whale Watcher (> 1M KAS)",
        "compra": "COMPRA",
        "venda": "VENDA",
        "explorer_titulo": "🔎 Tracker de Carteira",
        "explorer_label": "Endereço da carteira Kaspa:",
        "logout": "SAIR",
        "saldo_total": "Saldo Total"
    },
    "English": {
        "titulo": "KASPA ELITE TRACKER",
        "login_msg": "Elite Access @jackmaster273",
        "calc_titulo": "🧮 Flow Calculator",
        "whale_titulo": "🐳 Whale Watcher (> 1M KAS)",
        "compra": "BUY",
        "venda": "SELL",
        "explorer_titulo": "🔎 Wallet Tracker",
        "explorer_label": "Kaspa wallet address:",
        "logout": "LOGOUT",
        "saldo_total": "Total Balance"
    }
}

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown(f'<div style="text-align:center;padding-top:50px;"><img src="https://cryptologos.cc/logos/kaspa-kas-logo.png" width="100"><h1>{txt[lang]["titulo"]}</h1></div>', unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        user_in = st.text_input("Login:")
        pass_in = st.text_input("Password / Senha:", type="password")
        if st.button("ENTER"):
            if user_in in USUARIOS_ELITE and USUARIOS_ELITE[user_in] == pass_in:
                st.session_state["autenticado"] = True
                st.rerun()
    st.stop()

# --- INTERFACE ---
st.markdown("<style>.stApp { background-color: #000; color: #fff; } .card { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #00FF7F; }</style>", unsafe_allow_html=True)

@st.cache_data(ttl=30)
def buscar_dados():
    try:
        k = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true").json()['kaspa']
        d = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['BRL']
        return k, d
    except: return {"usd": 0.0000, "brl": 0.0000, "usd_24h_change": 0.00}, 5.0000

kas, dolar_real = buscar_dados()

st.title(f"🟢 {txt[lang]['titulo']}")

# MÉTRICAS
c1, c2, c3, c4 = st.columns(4)
c1.metric("KAS/USD", f"$ {kas['usd']:.4f}")
c2.metric("KAS/BRL", f"R$ {kas['brl']:.4f}")
c3.metric("USD/BRL", f"R$ {dolar_real:.4f}")
c4.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

st.write("---")

# 2. TRACKER DE CARTEIRA (SALDO KAS E USD)
st.subheader(txt[lang]["explorer_titulo"])
wallet_address = st.text_input(txt[lang]["explorer_label"])
if wallet_address:
    try:
        bal_res = requests.get(f"https://api.kaspa.org/addresses/{wallet_address}/balance").json()
        balance_kas = bal_res['balance'] / 100000000
        balance_usd = balance_kas * kas['usd']
        
        st.success(f"**{txt[lang]['saldo_total']}**")
        col_a, col_b = st.columns(2)
        col_a.metric("Saldo (KAS)", f"{balance_kas:.4f} KAS")
        col_b.metric("Saldo (USD)", f"$ {balance_usd:.4f}")
        st.markdown(f"[🔗 Ver na Blockchain](https://kas.fyi/address/{wallet_address})")
    except: st.error("Endereço não encontrado.")

# 3. CALCULADORA
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(txt[lang]["calc_titulo"])
ca, cb, cc = st.columns(3)
v_usd = ca.number_input("Dólar ($):", value=1000.0, format="%.4f")
cb.write(f"↳ **{v_usd / kas['usd']:.4f} KAS**")
cc.write(f"↳ **R$ {v_usd * dolar_real:.4f}**")
st.markdown('</div>', unsafe_allow_html=True)

# 4. WHALE WATCHER (> 1M KAS) - ENDEREÇO E VALOR
st.subheader(txt[lang]["whale_titulo"])
baleias = [
    {"tipo": "COMPRA", "valor": 12550340.1255, "label": txt[lang]["compra"], "wallet": "kaspa:qrel7p96j8n45xvrt7xqrel7p96j8n45xvrt7xqrel7p96j8n45xvrt7x"},
    {"tipo": "VENDA", "valor": 8100800.4500, "label": txt[lang]["venda"], "wallet": "kaspa:qp888np7xqrel7p96j8n45xvrt7xqrel7p96j8n45xvrt7xqrel7p96j"}
]
for b in baleias:
    cor = "#00FF7F" if b['tipo'] == "COMPRA" else "#FF4B4B"
    st.markdown(f'''
    <div style="border:1px solid #FFD700;padding:15px;border-radius:10px;margin-bottom:10px;background-color:#0a0a00;">
        <b style="color:{cor};">{b["label"]}</b> | <b>{b["valor"]:.4f} KAS</b><br>
        <small style="word-break: break-all;"><b>Wallet:</b> {b["wallet"]}</small><br>
        <a href="https://kas.fyi/address/{b['wallet']}" target="_blank" style="color:#00FF7F;text-decoration:none;"><small>Explorer 🔗</small></a>
    </div>
    ''', unsafe_allow_html=True)

if st.sidebar.button(txt[lang]["logout"]):
    st.session_state["autenticado"] = False
    st.rerun()
