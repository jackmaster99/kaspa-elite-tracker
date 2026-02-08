import streamlit as st
import requests
import pandas as pd

# 1. CONFIGURAÇÃO DE ELITE
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="wide", page_icon="🟢")

# --- BANCO DE DADOS DE ACESSO ---
USUARIOS_ELITE = {
    "jackmaster273@elite.com": "Kaspa26!@#$%",
    "Kaspa1": "Kas123*#$"
}

# --- IDIOMAS ---
if "lang" not in st.session_state: st.session_state["lang"] = "Português"
with st.sidebar:
    st.image("https://cryptologos.cc/logos/kaspa-kas-logo.png", width=60)
    st.session_state["lang"] = st.radio("🌐 Language", ["Português", "English"])
lang = st.session_state["lang"]

txt = {
    "Português": {
        "titulo": "KASPA ELITE TRACKER",
        "monitor": "📡 Monitor de Atividade em Tempo Real (Blockchain)",
        "calc": "🧮 Calculadora de Fluxo (4 Dígitos)",
        "explorer": "🔎 Tracker de Carteira & Saldo USD",
        "tx_real": "Últimas Transações Detectadas na Rede:"
    },
    "English": {
        "titulo": "KASPA ELITE TRACKER",
        "monitor": "📡 Real-Time Activity Monitor (Blockchain)",
        "calc": "🧮 Flow Calculator (4-Digit)",
        "explorer": "🔎 Wallet Tracker & USD Balance",
        "tx_real": "Latest Transactions Detected on Network:"
    }
}

# --- LOGIN ---
if "autenticado" not in st.session_state: st.session_state["autenticado"] = False
if not st.session_state["autenticado"]:
    st.title(txt[lang]["titulo"])
    u, p = st.text_input("Login:"), st.text_input("Password:", type="password")
    if st.button("ENTER"):
        if u in USUARIOS_ELITE and USUARIOS_ELITE[u] == p:
            st.session_state["autenticado"] = True
            st.rerun()
    st.stop()

# --- BUSCA DE PREÇO REAL ---
@st.cache_data(ttl=30)
def get_kas_data():
    try:
        k = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true").json()['kaspa']
        d = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['BRL']
        return k, d
    except: return {"usd": 0.0320, "brl": 0.1700, "usd_24h_change": 0.0}, 5.25

kas, dolar_real = get_kas_data()

st.title(f"🟢 {txt[lang]['titulo']}")

# MÉTRICAS 4 DÍGITOS
c1, c2, c3, c4 = st.columns(4)
c1.metric("KAS/USD", f"$ {kas['usd']:.4f}")
c2.metric("KAS/BRL", f"R$ {kas['brl']:.4f}")
c3.metric("USD/BRL", f"R$ {dolar_real:.4f}")
c4.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

st.write("---")

# --- MONITOR DE ATIVIDADE REAL (VIA API KASPA) ---
st.subheader(txt[lang]["monitor"])
st.write(txt[lang]["tx_real"])

try:
    # Busca as últimas transações globais da rede
    tx_data = requests.get("https://api.kaspa.org/transactions/recent?limit=8").json()
    for tx in tx_data:
        amount = sum([out['amount'] for out in tx['outputs']]) / 100000000
        val_usd = amount * kas['usd']
        
        # Filtro visual: Verde para grandes volumes, Cinza para pequenos
        cor = "#00FF7F" if amount > 100000 else "#555"
        label = "WHALE MOVEMENT 🐳" if amount > 1000000 else "Transaction"
        
        st.markdown(f'''
        <div style="border-left: 5px solid {cor}; background-color: #111; padding: 12px; border-radius: 5px; margin-bottom: 8px;">
            <b style="color:{cor};">{label}</b> | {amount:,.4f} KAS <b>($ {val_usd:,.2f} USD)</b><br>
            <small style="word-break: break-all;">Hash: {tx['transaction_id']}</small><br>
            <a href="https://kaspa.stream/tx/{tx['transaction_id']}" target="_blank" style="color:#00FF7F; text-decoration:none;"><small>View on Kaspa.stream 🔗</small></a>
        </div>
        ''', unsafe_allow_html=True)
except:
    st.warning("Aguardando novas transações da Blockchain...")

# --- CALCULADORA ELITE ---
st.write("---")
st.subheader(txt[lang]["calc"])
col_u, col_k, col_r = st.columns(3)
v_usd = col_u.number_input("Dollar ($):", value=1000.0, format="%.4f")
col_u.write(f"↳ **{v_usd / kas['usd']:.4f} KAS**")
v_kas = col_k.number_input("Kaspa (KAS):", value=10000.0, format="%.4f")
col_k.write(f"↳ **$ {v_kas * kas['usd']:.4f}**")
v_real = col_r.number_input("Real (R$):", value=5000.0, format="%.4f")
col_r.write(f"↳ **{v_real / kas['brl']:.4f} KAS**")

# --- TRACKER DE CARTEIRA ---
st.write("---")
st.subheader(txt[lang]["explorer"])
target = st.text_input("Wallet (kaspa:q...):")
if target:
    try:
        r = requests.get(f"https://api.kaspa.org/addresses/{target}/balance").json()
        bal = r['balance'] / 100000000
        st.success(f"**Balance: {bal:,.4f} KAS** | **Value: $ {bal * kas['usd']:,.2f} USD**")
        st.markdown(f"[View on Kaspa.stream](https://kaspa.stream/address/{target})")
    except: st.error("Endereço não encontrado.")
