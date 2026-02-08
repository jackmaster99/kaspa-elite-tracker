import streamlit as st
import requests
import pandas as pd
import uuid

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="wide", page_icon="🟢")

# --- BANCO DE DADOS DE ACESSO INDIVIDUAL ---
USUARIOS_ELITE = {
    "jackmaster273@elite.com": "Kaspa26!@#$%",
    "Kaspa1": "Kas123*#$"
}

# --- SISTEMA DE IDIOMAS (NA SIDEBAR) ---
with st.sidebar:
    st.image("https://cryptologos.cc/logos/kaspa-kas-logo.png", width=50)
    lang = st.radio("🌐 Language / Idioma", ["Português", "English"])

# DICIONÁRIO DE TRADUÇÃO COMPLETO
txt = {
    "Português": {
        "titulo": "KASPA ELITE TRACKER",
        "login_msg": "Painel de Monitoramento @jackmaster273",
        "aviso": "⚠️ TERMOS: Apenas uma sessão ativa por usuário.",
        "calc_titulo": "🧮 Calculadora de Fluxo (Entrada/Saída)",
        "whale_titulo": "🐳 Whale Watcher (> 1M KAS)",
        "compra": "COMPRA DETECTADA",
        "venda": "VENDA DETECTADA",
        "explorer_titulo": "🔎 Explorer de Carteira & Últimas 5 TXs",
        "explorer_label": "Cole o endereço da carteira Kaspa:",
        "top10_titulo": "📊 Top 10 Mercado (Comparativo)",
        "logout": "SAIR",
        "entrada_dolar": "Entrada em Dólar ($):",
        "entrada_kaspa": "Valor em Kaspa (KAS):",
        "entrada_real": "Valor em Real (R$):",
        "saldo": "Saldo",
        "valor": "Valor"
    },
    "English": {
        "titulo": "KASPA ELITE TRACKER",
        "login_msg": "Monitoring Panel @jackmaster273",
        "aviso": "⚠️ TERMS: Only one active session per user.",
        "calc_titulo": "🧮 Flow Calculator (In/Out)",
        "whale_titulo": "🐳 Whale Watcher (> 1M KAS)",
        "compra": "BUY DETECTED",
        "venda": "SELL DETECTED",
        "explorer_titulo": "🔎 Wallet Explorer & Last 5 TXs",
        "explorer_label": "Paste Kaspa wallet address:",
        "top10_titulo": "📊 Market Top 10 (Comparison)",
        "logout": "LOGOUT",
        "entrada_dolar": "Input in Dollar ($):",
        "entrada_kaspa": "Value in Kaspa (KAS):",
        "entrada_real": "Value in Real (R$):",
        "saldo": "Balance",
        "valor": "Value"
    }
}

# --- LÓGICA DE ACESSO ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown(f'<div style="text-align:center;padding-top:50px;"><img src="https://cryptologos.cc/logos/kaspa-kas-logo.png" width="100"><h1>{txt[lang]["titulo"]}</h1><p>{txt[lang]["login_msg"]}</p></div>', unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        st.warning(txt[lang]["aviso"])
        user_in = st.text_input("Login:")
        pass_in = st.text_input("Password / Senha:", type="password")
        if st.button("ENTER / ENTRAR"):
            if user_in in USUARIOS_ELITE and USUARIOS_ELITE[user_in] == pass_in:
                st.session_state["autenticado"] = True
                st.session_state["user_email"] = user_in
                st.rerun()
    st.stop()

# --- INTERFACE TÉCNICA ---
st.markdown("<style>.stApp { background-color: #000; color: #fff; } .card { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #00FF7F; margin-bottom: 20px; } [data-testid='stMetricValue'] { color: #00FF7F !important; }</style>", unsafe_allow_html=True)

@st.cache_data(ttl=30)
def buscar_dados():
    try:
        kas = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true").json()['kaspa']
        usd_brl = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['BRL']
        m = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=12&page=1").json()
        top_10 = pd.DataFrame([c for c in m if c['symbol'] not in ['usdt', 'usdc']][:10])[['name', 'current_price', 'price_change_percentage_24h']]
        return kas, usd_brl, top_10
    except:
        return {"usd": 0.0000, "brl": 0.0000, "usd_24h_change": 0.00}, 5.0000, pd.DataFrame()

kas, dolar_real, top_10_df = buscar_dados()

# HEADER
st.title(f"🟢 {txt[lang]['titulo']}")

# 1. MÉTRICAS (4 DÍGITOS)
c1, c2, c3, c4 = st.columns(4)
c1.metric("KAS / USD", f"$ {kas['usd']:.4f}")
c2.metric("KAS / BRL", f"R$ {kas['brl']:.4f}")
c3.metric("USD / BRL", f"R$ {dolar_real:.4f}")
c4.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

st.write("---")

# 2. EXPLORER DE CARTEIRA
st.subheader(txt[lang]["explorer_titulo"])
wallet_address = st.text_input(txt[lang]["explorer_label"])
if wallet_address:
    try:
        bal_res = requests.get(f"https://api.kaspa.org/addresses/{wallet_address}/balance").json()
        balance = bal_res['balance'] / 100000000
        st.success(f"{txt[lang]['saldo']}: **{balance:.4f} KAS** | {txt[lang]['valor']}: **$ {(balance * kas['usd']):.4f}**")
        tx_res = requests.get(f"https://api.kaspa.org/addresses/{wallet_address}/full-transactions?limit=5").json()
        for i, tx in enumerate(tx_res, 1):
            with st.expander(f"TX {i}"):
                st.code(tx['transaction_id'])
                amt = sum([out['amount'] for out in tx['outputs']]) / 100000000
                st.write(f"Amount: {amt:.4f} KAS")
    except: st.error("Invalid Address / Endereço Inválido")

# 3. CALCULADORA (4 DÍGITOS)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(txt[lang]["calc_titulo"])
col_usd, col_kas, col_brl = st.columns(3)
v_usd = col_usd.number_input(txt[lang]["entrada_dolar"], value=1000.0, format="%.4f")
col_usd.write(f"↳ **{v_usd / kas['usd']:.4f} KAS**")
v_kas = col_kas.number_input(txt[lang]["entrada_kaspa"], value=10000.0, format="%.4f")
col_kas.write(f"↳ **$ {v_kas * kas['usd']:.4f}**")
v_brl = col_brl.number_input(txt[lang]["entrada_real"], value=5000.0, format="%.4f")
col_brl.write(f"↳ **{v_brl / kas['brl']:.4f} KAS**")
st.markdown('</div>', unsafe_allow_html=True)

# 4. MONITOR DE BALEIAS (LINHA 144 CORRIGIDA AQUI)
st.subheader(txt[lang]["whale_titulo"])
baleias = [
    {"tipo": "COMPRA", "valor": 12550340.1255, "label": txt[lang]["compra"]},
    {"tipo": "VENDA", "valor": 8100800.4500, "label": txt[lang]["venda"]}
]
for b in baleias:
    cor = "#00FF7F" if b['tipo'] == "COMPRA" else "#FF4B4B"
    st.markdown(f'<div style="border:1px solid #FFD700;padding:10px;border-radius:10px;margin-bottom:10px;">'
                f'<b style="color:{cor};">{b["label"]}</b> | {b["valor"]:.4f} KAS</div>', unsafe_allow_html=True)

# 5. TOP 10
st.subheader(txt[lang]["top10_titulo"])
if not top_10_df.empty:
    st.dataframe(top_10_df.style.format({'current_price': '{:.4f}'}), use_container_width=True)

if st.sidebar.button(txt[lang]["logout"]):
    st.session_state["autenticado"] = False
    st.rerun()
