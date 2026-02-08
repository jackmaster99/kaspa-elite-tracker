import streamlit as st
import requests
import pandas as pd
import uuid

# 1. CONFIGURAÇÃO DE ALTA PERFORMANCE
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="wide", page_icon="🟢")

# --- BANCO DE DADOS DE ACESSO INDIVIDUAL ---
# Mantenha sempre a vírgula ao adicionar novos usuários
USUARIOS_ELITE = {
    "jackmaster273@elite.com": "Kaspa26!@#$%",
    "Kaspa1": "Kas123*#$",
    "Kaspa2": "Kas492!@#"
}

# --- SISTEMA DE IDIOMAS (PORTUGUÊS / ENGLISH) ---
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
        "monitor": "📡 Monitor de Atividade em Tempo Real (Blockchain)",
        "calc": "🧮 Calculadora de Fluxo (Precisão 4 Dígitos)",
        "explorer": "🔎 Tracker de Carteira & Saldo USD",
        "top10": "📊 Top 10 Mercado (Comparativo)",
        "logout": "SAIR / LOGOUT",
        "tx_real": "Últimas Transações Detectadas na Rede:",
        "input_label": "Cole o endereço Kaspa (kaspa:q...):",
        "baleia_label": "MOVIMENTAÇÃO BALEIA 🐳",
        "peixe_label": "GRANDE MOVIMENTAÇÃO 🐠"
    },
    "English": {
        "titulo": "KASPA ELITE TRACKER",
        "login_msg": "Elite Monitoring Panel @jackmaster273",
        "monitor": "📡 Real-Time Activity Monitor (Blockchain)",
        "calc": "🧮 Flow Calculator (4-Digit Precision)",
        "explorer": "🔎 Wallet Tracker & USD Balance",
        "top10": "📊 Market Top 10 (Comparison)",
        "logout": "LOGOUT",
        "tx_real": "Latest Transactions Detected on Network:",
        "input_label": "Paste Kaspa address (kaspa:q...):",
        "baleia_label": "WHALE MOVEMENT 🐳",
        "peixe_label": "BIG FISH MOVEMENT 🐠"
    }
}

# --- LÓGICA DE LOGIN COM SESSÃO ÚNICA ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown(f'<div style="text-align:center;padding-top:50px;"><img src="https://cryptologos.cc/logos/kaspa-kas-logo.png" width="120"><h1>{txt[lang]["titulo"]}</h1><p>{txt[lang]["login_msg"]}</p></div>', unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        st.markdown('<div style="background-color:#111; padding:20px; border-radius:15px; border:1px solid #333;">', unsafe_allow_html=True)
        u = st.text_input("Login (User/Email):")
        p = st.text_input("Password (Senha):", type="password")
        if st.button("DESBLOQUEAR TERMINAL"):
            if u in USUARIOS_ELITE and USUARIOS_ELITE[u] == p:
                st.session_state["autenticado"] = True
                st.session_state["user_email"] = u
                st.rerun()
            else:
                st.error("Credenciais Inválidas ou Licença Expirada.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- ESTILO CSS ELITE ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .card { background-color: #111; padding: 25px; border-radius: 15px; border: 1px solid #00FF7F; margin-bottom: 25px; }
    [data-testid="stMetricValue"] { color: #00FF7F !important; font-size: 32px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BUSCA DE DADOS (PREÇO E TOP 10) ---
@st.cache_data(ttl=30)
def buscar_dados_mercado():
    try:
        # Preço Kaspa
        k = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true", timeout=10).json()['kaspa']
        # Câmbio Dólar
        d = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10).json()['rates']['BRL']
        # Top 10 Mercado
        m = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=12&page=1", timeout=10).json()
        top_10 = pd.DataFrame([c for c in m if c['symbol'] not in ['usdt', 'usdc']][:10])[['name', 'current_price', 'price_change_percentage_24h']]
        return k, d, top_10
    except:
        return {"usd": 0.0320, "brl": 0.1700, "usd_24h_change": 0.0}, 5.2500, pd.DataFrame()

kas, dolar_real, top_10_df = buscar_dados_mercado()

# HEADER DO TERMINAL
st.title(f"🟢 {txt[lang]['titulo']}")
st.write(f"Conectado: **{st.session_state['user_email']}**")

# MÉTRICAS TÉCNICAS (4 DÍGITOS)
c1, c2, c3, c4 = st.columns(4)
c1.metric("KAS / USD", f"$ {kas['usd']:.4f}")
c2.metric("KAS / BRL", f"R$ {kas['brl']:.4f}")
c3.metric("USD / BRL", f"R$ {dolar_real:.4f}")
c4.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

st.write("---")

# 1. MONITOR DE ATIVIDADE REAL (VIA API BLOCKCHAIN)
st.subheader(txt[lang]["monitor"])
try:
    tx_data = requests.get("https://api.kaspa.org/transactions/recent?limit=10", timeout=10).json()
    for tx in tx_data:
        amount = sum([out['amount'] for out in tx['outputs']]) / 100000000
        val_usd = amount * kas['usd']
        
        if amount >= 1000000:
            cor, label = "#00FF7F", txt[lang]["baleia_label"]
        elif amount >= 100000:
            cor, label = "#FFD700", txt[lang]["peixe_label"]
        else:
            cor, label = "#555", "Retail Transaction"
            
        st.markdown(f'''
        <div style="border-left: 5px solid {cor}; background-color: #111; padding: 15px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #222;">
            <b style="color:{cor};">{label}</b> | {amount:,.4f} KAS <b>($ {val_usd:,.2f} USD)</b><br>
            <small style="word-break: break-all; color: #888;">Hash: {tx['transaction_id']}</small><br>
            <a href="https://kaspa.stream/tx/{tx['transaction_id']}" target="_blank" style="color:#00FF7F; text-decoration:none;"><small>Ver no Kaspa.stream 🔗</small></a>
        </div>
        ''', unsafe_allow_html=True)
except:
    st.warning("Aguardando novas transações da Blockchain (API ocupada)...")

st.write("---")

# 2. TRACKER DE CARTEIRA (SALDO KAS + USD)
st.subheader(txt[lang]["explorer"])
target = st.text_input(txt[lang]["input_label"], placeholder="kaspa:q...")
if target:
    try:
        r = requests.get(f"https://api.kaspa.org/addresses/{target}/balance", timeout=10).json()
        bal = r['balance'] / 100000000
        st.success(f"**Saldo: {bal:,.4f} KAS** | **Valor: $ {bal * kas['usd']:,.2f} USD**")
        st.markdown(f"[🔗 Verificar no Kaspa.stream](https://kaspa.stream/address/{target})")
    except:
        st.error("Endereço não encontrado ou inválido.")

# 3. CALCULADORA ELITE (4 DÍGITOS)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(txt[lang]["calc"])
col_u, col_k, col_r = st.columns(3)

v_usd = col_u.number_input(f"{txt[lang]['titulo']} ($):", value=1000.0, step=0.01, format="%.4f")
if kas['usd'] > 0:
    col_u.write(f"↳ **{v_usd / kas['usd']:.4f} KAS**")
    col_u.write(f"↳ **R$ {v_usd * dolar_real:.4f}**")

v_kas = col_k.number_input("Kaspa (KAS):", value=10000.0, step=0.01, format="%.4f")
col_k.write(f"↳ **$ {v_kas * kas['usd']:.4f}**")
col_k.write(f"↳ **R$ {v_kas * kas['brl']:.4f}**")

v_real = col_r.number_input("Real (R$):", value=5000.0, step=0.01, format="%.4f")
if kas['brl'] > 0:
    col_r.write(f"↳ **{v_real / kas['brl']:.4f} KAS**")
    col_r.write(f"↳ **$ {v_real / dolar_real:.4f}**")
st.markdown('</div>', unsafe_allow_html=True)

# 4. TOP 10 MERCADO
st.subheader(txt[lang]["top10"])
if not top_10_df.empty:
    st.dataframe(top_10_df.style.format({'current_price': '{:.4f}'}), use_container_width=True)

# RODAPÉ E LOGOUT
st.sidebar.write("---")
if st.sidebar.button(txt[lang]["logout"]):
    st.session_state["autenticado"] = False
    st.rerun()

st.markdown("<br><center><small>Kaspa Elite Tracker | © 2026 @jackmaster273</small></center>", unsafe_allow_html=True)
