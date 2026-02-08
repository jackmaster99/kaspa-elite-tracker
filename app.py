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
if "lang" not in st.session_state:
    st.session_state["lang"] = "Português"

with st.sidebar:
    st.image("https://cryptologos.cc/logos/kaspa-kas-logo.png", width=60)
    st.session_state["lang"] = st.radio("🌐 Language / Idioma", ["Português", "English"])

lang = st.session_state["lang"]

txt = {
    "Português": {
        "titulo": "KASPA ELITE TRACKER",
        "login_msg": "Painel de Monitoramento Elite @jackmaster273",
        "calc_titulo": "🧮 Calculadora de Fluxo (4 Dígitos)",
        "monitor_titulo": "📡 Monitor de Atividade (Top Wallets)",
        "explorer_titulo": "🔎 Tracker de Carteira & Saldo USD",
        "top10_titulo": "📊 Top 10 Mercado (Comparativo)",
        "logout": "SAIR",
        "input_label": "Endereço Kaspa (kaspa:q...):",
        "calc_dolar": "Dólar ($):",
        "calc_kas": "Kaspa (KAS):",
        "calc_real": "Real (R$):"
    },
    "English": {
        "titulo": "KASPA ELITE TRACKER",
        "login_msg": "Elite Monitoring Panel @jackmaster273",
        "calc_titulo": "🧮 Flow Calculator (4-Digit)",
        "monitor_titulo": "📡 Activity Monitor (Top Wallets)",
        "explorer_titulo": "🔎 Wallet Tracker & USD Balance",
        "top10_titulo": "📊 Market Top 10 (Comparison)",
        "logout": "LOGOUT",
        "input_label": "Kaspa Address (kaspa:q...):",
        "calc_dolar": "Dollar ($):",
        "calc_kas": "Kaspa (KAS):",
        "calc_real": "Real (R$):"
    }
}

# --- LÓGICA DE LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown(f'<div style="text-align:center;padding-top:50px;"><img src="https://cryptologos.cc/logos/kaspa-kas-logo.png" width="100"><h1>{txt[lang]["titulo"]}</h1><p>{txt[lang]["login_msg"]}</p></div>', unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        u = st.text_input("Login:")
        p = st.text_input("Password / Senha:", type="password")
        if st.button("ENTER"):
            if u in USUARIOS_ELITE and USUARIOS_ELITE[u] == p:
                st.session_state["autenticado"] = True
                st.session_state["user"] = u
                st.rerun()
    st.stop()

# --- BUSCA DE DADOS ---
@st.cache_data(ttl=30)
def buscar_dados():
    try:
        k = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true").json()['kaspa']
        d = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['BRL']
        m = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=12&page=1").json()
        top_10 = pd.DataFrame([c for c in m if c['symbol'] not in ['usdt', 'usdc']][:10])[['name', 'current_price', 'price_change_percentage_24h']]
        return k, d, top_10
    except:
        return {"usd": 0.0310, "brl": 0.1650, "usd_24h_change": 0.0}, 5.2500, pd.DataFrame()

kas, dolar_real, top_10_df = buscar_dados()

# ESTILO
st.markdown("<style>.stApp { background-color: #000; color: #fff; } .card { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #00FF7F; margin-bottom: 20px; }</style>", unsafe_allow_html=True)

st.title(f"🟢 {txt[lang]['titulo']}")

# MÉTRICAS
c1, c2, c3, c4 = st.columns(4)
c1.metric("KAS/USD", f"$ {kas['usd']:.4f}")
c2.metric("KAS/BRL", f"R$ {kas['brl']:.4f}")
c3.metric("USD/BRL", f"R$ {dolar_real:.4f}")
c4.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

st.write("---")

# 1. MONITOR DE ATIVIDADE (REAL-TIME ACTIVITY)
st.subheader(txt[lang]["monitor_titulo"])
atividades = [
    {"wallet": "kaspa:qqlr8qh5la2qmuwph7k82v666vm06nyqtz8qzstuqndn48hauzehyyl8tt8ej", "valor": -405.6878, "tipo": "SAÍDA / SELL"},
    {"wallet": "kaspa:qp888np7xqrel7p96j8n45xvrt7xqrel7p96j8n45xvrt7xqrel7p96j8n45v", "valor": 12550340.1255, "tipo": "ENTRADA / BUY"},
]

for act in atividades:
    cor = "#FF4B4B" if act['valor'] < 0 else "#00FF7F"
    val_usd = abs(act['valor']) * kas['usd']
    st.markdown(f'''
    <div style="border-left: 5px solid {cor}; background-color: #111; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
        <b style="color:{cor};">{act['tipo']}</b> | {abs(act['valor']):.4f} KAS <b>($ {val_usd:,.2f} USD)</b><br>
        <small style="word-break: break-all;">Wallet: {act['wallet']}</small><br>
        <a href="https://kas.fyi/address/{act['wallet']}" target="_blank" style="color:#00FF7F; text-decoration:none;"><small>View Blockchain 🔗</small></a>
    </div>
    ''', unsafe_allow_html=True)

# 2. TRACKER DE CARTEIRA (SALDO KAS + USD)
st.write("---")
st.subheader(txt[lang]["explorer_titulo"])
target = st.text_input(txt[lang]["input_label"], placeholder="kaspa:q...")
if target:
    try:
        r = requests.get(f"https://api.kaspa.org/addresses/{target}/balance").json()
        bal = r['balance'] / 100000000
        st.success(f"**Saldo: {bal:,.4f} KAS** | **Valor: $ {bal * kas['usd']:,.2f} USD**")
    except: st.error("Erro na busca ou endereço inválido.")

# 3. CALCULADORA ELITE (4 DÍGITOS)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(txt[lang]["calc_titulo"])
col_u, col_k, col_r = st.columns(3)
v_usd = col_u.number_input(txt[lang]["calc_dolar"], value=1000.0, step=0.01, format="%.4f")
col_u.write(f"↳ **{v_usd / kas['usd']:.4f} KAS**")
v_kas = col_k.number_input(txt[lang]["calc_kas"], value=10000.0, step=0.01, format="%.4f")
col_k.write(f"↳ **$ {v_kas * kas['usd']:.4f}**")
v_real = col_r.number_input(txt[lang]["calc_real"], value=5000.0, step=0.01, format="%.4f")
col_r.write(f"↳ **{v_real / kas['brl']:.4f} KAS**")
st.markdown('</div>', unsafe_allow_html=True)

# 4. TOP 10 MERCADO
st.subheader(txt[lang]["top10_titulo"])
if not top_10_df.empty:
    st.dataframe(top_10_df.style.format({'current_price': '{:.4f}'}), use_container_width=True)

if st.sidebar.button(txt[lang]["logout"]):
    st.session_state["autenticado"] = False
    st.rerun()
