import streamlit as st
import requests
import pandas as pd
import uuid

# 1. CONFIGURAÇÃO DE ALTA PERFORMANCE
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="wide", page_icon="🟢")

# --- BANCO DE DADOS DE ACESSO ---
USUARIOS_ELITE = {
    "jackmaster273@elite.com": "Kaspa26!@#$%",
    "Kaspa1": "Kas123*#$",
    "Kaspa2": "Kas492!@#"
}

# --- SISTEMA DE IDIOMAS ---
if "lang" not in st.session_state:
    st.session_state["lang"] = "Português"

with st.sidebar:
    st.image("https://cryptologos.cc/logos/kaspa-kas-logo.png", width=60)
    st.session_state["lang"] = st.radio("🌐 Language / Idioma", ["Português", "English"])

lang = st.session_state["lang"]

txt = {
    "Português": {
        "titulo": "KASPA ELITE TRACKER",
        "login_msg": "Painel Elite @jackmaster273",
        "monitor": "📡 Monitor de Atividade em Tempo Real",
        "calc": "🧮 Calculadora de Fluxo Profissional (4 Dígitos)",
        "explorer": "🔎 Tracker de Carteira & Saldo USD",
        "top10": "📊 Top 10 Mercado",
        "tx_real": "Transações Recentes na Rede (Live):",
        "label_dolar": "Valor em Dólar ($):",
        "label_kas": "Valor em Kaspa (KAS):",
        "label_real": "Valor em Real (R$):",
        "logout": "SAIR"
    },
    "English": {
        "titulo": "KASPA ELITE TRACKER",
        "login_msg": "Elite Monitoring Panel @jackmaster273",
        "monitor": "📡 Real-Time Activity Monitor",
        "calc": "🧮 Professional Flow Calculator (4-Digit)",
        "explorer": "🔎 Wallet Tracker & USD Balance",
        "top10": "📊 Market Top 10",
        "tx_real": "Recent Network Transactions (Live):",
        "label_dolar": "Value in Dollar ($):",
        "label_kas": "Value in Kaspa (KAS):",
        "label_real": "Value in Real (R$):",
        "logout": "LOGOUT"
    }
}

# --- LÓGICA DE LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown(f'<div style="text-align:center;padding-top:50px;"><img src="https://cryptologos.cc/logos/kaspa-kas-logo.png" width="120"><h1>{txt[lang]["titulo"]}</h1></div>', unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        u = st.text_input("Login:")
        p = st.text_input("Password / Senha:", type="password")
        if st.button("UNLOCK TERMINAL"):
            if u in USUARIOS_ELITE and USUARIOS_ELITE[u] == p:
                st.session_state["autenticado"] = True
                st.session_state["user"] = u
                st.rerun()
    st.stop()

# --- ESTILO ---
st.markdown("<style>.stApp { background-color: #000; color: #fff; } .card { background-color: #111; padding: 25px; border-radius: 15px; border: 1px solid #00FF7F; margin-bottom: 25px; }</style>", unsafe_allow_html=True)

# --- BUSCA DE DADOS ---
@st.cache_data(ttl=30)
def get_market_data():
    try:
        k = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true").json()['kaspa']
        d = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['BRL']
        m = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=12&page=1").json()
        top_10 = pd.DataFrame([c for c in m if c['symbol'] not in ['usdt', 'usdc']][:10])[['name', 'current_price', 'price_change_percentage_24h']]
        return k, d, top_10
    except:
        return {"usd": 0.0310, "brl": 0.1650, "usd_24h_change": 0.0}, 5.2500, pd.DataFrame()

kas, dolar_real, top_10_df = get_market_data()

st.title(f"🟢 {txt[lang]['titulo']}")

# MÉTRICAS
c1, c2, c3, c4 = st.columns(4)
c1.metric("KAS / USD", f"$ {kas['usd']:.4f}")
c2.metric("KAS / BRL", f"R$ {kas['brl']:.4f}")
c3.metric("USD / BRL", f"R$ {dolar_real:.4f}")
c4.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

st.write("---")

# 1. MONITOR DE ATIVIDADE REAL (VIA API KASPA)
st.subheader(txt[lang]["monitor"])
try:
    tx_data = requests.get("https://api.kaspa.org/transactions/recent?limit=10", timeout=10).json()
    for tx in tx_data:
        amount = sum([out['amount'] for out in tx['outputs']]) / 100000000
        val_usd = amount * kas['usd']
        cor = "#00FF7F" if amount >= 1000000 else "#555"
        label = "WHALE 🐳" if amount >= 1000000 else "TX"
        st.markdown(f'''
        <div style="border-left: 5px solid {cor}; background-color: #111; padding: 12px; margin-bottom: 8px; border-radius: 5px;">
            <b style="color:{cor};">{label}</b> | {amount:,.4f} KAS <b>($ {val_usd:,.2f} USD)</b><br>
            <a href="https://kaspa.stream/tx/{tx['transaction_id']}" target="_blank" style="color:#00FF7F; text-decoration:none;"><small>Hash: {tx['transaction_id'][:40]}... 🔗</small></a>
        </div>
        ''', unsafe_allow_html=True)
except:
    st.warning("Conectando à Blockchain...")

# 2. CALCULADORA DE 3 VIAS (RESTAURADA)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(txt[lang]["calc"])
col_u, col_k, col_r = st.columns(3)

v_usd = col_u.number_input(txt[lang]["label_dolar"], value=1000.0, format="%.4f")
col_u.write(f"↳ **{v_usd / kas['usd']:.4f} KAS**")

v_kas = col_k.number_input(txt[lang]["label_kas"], value=10000.0, format="%.4f")
col_k.write(f"↳ **$ {v_kas * kas['usd']:.4f}**")

v_real = col_r.number_input(txt[lang]["label_real"], value=5000.0, format="%.4f")
col_r.write(f"↳ **{v_real / kas['brl']:.4f} KAS**")
st.markdown('</div>', unsafe_allow_html=True)

# 3. TRACKER DE CARTEIRA
st.subheader(txt[lang]["explorer"])
target = st.text_input(txt[lang]["input_label"])
if target:
    try:
        r = requests.get(f"https://api.kaspa.org/addresses/{target}/balance").json()
        bal = r['balance'] / 100000000
        st.success(f"Balance: {bal:,.4f} KAS | Value: $ {bal * kas['usd']:,.2f} USD")
        st.markdown(f"[🔗 View on Kaspa.stream](https://kaspa.stream/address/{target})")
    except: st.error("Endereço Inválido.")

# 4. TOP 10 MERCADO
st.subheader(txt[lang]["top10"])
if not top_10_df.empty:
    st.dataframe(top_10_df.style.format({'current_price': '{:.4f}'}), use_container_width=True)

if st.sidebar.button(txt[lang]["logout"]):
    st.session_state["autenticado"] = False
    st.rerun()
