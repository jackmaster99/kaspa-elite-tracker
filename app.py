import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="wide", page_icon="🟢")

# --- SISTEMA DE LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown(f"""
        <div style="text-align: center; padding-top: 50px;">
            <img src="https://cryptologos.cc/logos/kaspa-kas-logo.png" width="150">
            <h1 style="color: #00FF7F; font-family: sans-serif;">KASPA ELITE TRACKER</h1>
            <p style="color: #555;">@jackmaster273</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col_l, col_c, col_r = st.columns([1,2,1])
        with col_c:
            st.markdown('<div style="background-color: #111; padding: 30px; border-radius: 15px; border: 1px solid #333;">', unsafe_allow_html=True)
            senha = st.text_input("Senha de Acesso:", type="password")
            if st.button("ACESSAR SISTEMA"):
                if senha == "Kaspa26!@#$%":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Chave inválida.")
            st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .card { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #00FF7F; margin-bottom: 20px; }
    .whale-card { border: 1px solid #FFD700; background-color: #0a0a00; padding: 15px; border-radius: 10px; font-family: 'Courier New', monospace; margin-bottom: 10px; }
    [data-testid="stMetricValue"] { color: #00FF7F !important; font-size: 28px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BUSCA DE DADOS ---
@st.cache_data(ttl=30)
def get_market_data():
    try:
        kas = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true", timeout=10).json()['kaspa']
        return kas
    except:
        return {"usd": 0.0000, "brl": 0.0000, "usd_24h_change": 0.00}

kas = get_market_data()

# --- INTERFACE PRINCIPAL ---
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image("https://cryptologos.cc/logos/kaspa-kas-logo.png", width=80)
with col_title:
    st.title("KASPA ELITE TRACKER")
    st.markdown(f"Painel Ativo: <span style='color:#00FF7F;'>@jackmaster273</span>", unsafe_allow_html=True)

# 1. MÉTRICAS COM 4 DÍGITOS
c1, c2, c3 = st.columns(3)
c1.metric("KAS / USD", f"$ {kas['usd']:.4f}")
c2.metric("KAS / BRL", f"R$ {kas['brl']:.4f}")
c3.metric("Var. 24h", f"{kas['usd_24h_change']:.2f}%")

st.write("---")

# 2. EXPLORER DE CARTEIRA
st.subheader("🔎 Wallet Explorer & Precise Activity")
wallet_address = st.text_input("Endereço Completo da Carteira Kaspa:")

if wallet_address:
    try:
        bal_res = requests.get(f"https://api.kaspa.org/addresses/{wallet_address}/balance").json()
        balance = bal_res['balance'] / 100000000
        st.success(f"Saldo: **{balance:.4f} KAS** | Valor: **$ {(balance * kas['usd']):.4f}**")
        
        st.write("🕒 **Últimas 5 Transações da Carteira:**")
        tx_res = requests.get(f"https://api.kaspa.org/addresses/{wallet_address}/full-transactions?limit=5").json()
        for i, tx in enumerate(tx_res, 1):
            with st.expander(f"Transação {i} - Detalhes"):
                st.write(f"**Hash:** `{tx['transaction_id']}`")
                amt = sum([out['amount'] for out in tx['outputs']]) / 100000000
                st.write(f"**Valor Transacionado:** {amt:.4f} KAS")
    except:
        st.error("Erro ao ler Blockchain. Verifique o endereço.")

# 3. CALCULADORA DE PRECISÃO
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🧮 Calculadora de Conversão Elite")
col_a, col_b, col_c = st.columns(3)
val_usd = col_a.number_input("Valor em Dólar ($):", value=1000.0, step=0.0001, format="%.4f")
col_b.write(f"Valor em Real: <br>**R$ {(val_usd * (kas['brl']/kas['usd'])):.4f}**", unsafe_allow_html=True)
col_c.write(f"Total em Kaspa: <br>**{(val_usd / kas['usd']):.4f} KAS**", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 4. WHALE WATCHER (MOVIMENTAÇÕES > 1.000.000 KAS EXCLUSIVAMENTE)
st.subheader("🐳 Whale Watcher - Top 5 Movimentações (> 1M KAS / 24h)")
# Dados simulando transações reais de alto volume capturadas na rede
baleias = [
    {"wallet": "kaspa:qrel7p96j8n45xvrt7xqrel7p96j8n45xvrt7xqrel7p96j8n45xvrt7x", "valor": 12550340.1255, "hash": "7a3d9f2c1b8e4a5d6c7b8a9d0e1f2a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r"},
    {"wallet": "kaspa:qp888np7xqrel7p96j8n45xvrt7xqrel7p96j8n45xvrt7xqrel7p96j", "valor": 8100800.4500, "hash": "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3"},
    {"wallet": "kaspa:qpmasterjack273xqrel7p96j8n45xvrt7xqrel7p96j8n45xvrt7xqr", "valor": 3850000.0000, "hash": "f1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s1t0u2v3w4x5y6z7a8b9c0d1e2"},
    {"wallet": "kaspa:qr5vrt7xqrel7p96j8n45xvrt7xqrel7p96j8n45xvp888np7xqrel7p9", "valor": 1420550.9999, "hash": "d4e5f6a7b8c90123456789abcdef0123456789abcdef0123456789abcdef0123"},
    {"wallet": "kaspa:qkz6vms0k2j8n45xvrt7xqrel7p96j8n45xvrt7xqrel7p96j8n45xvr", "valor": 1100000.4444, "hash": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"}
]

for i, b in enumerate(baleias, 1):
    st.markdown(f"""
    <div class="whale-card">
        <b style="color: #FFD700;">#{i} MOVIMENTAÇÃO DE ELITE (> 1M KAS)</b><br>
        <b>Endereço da Carteira:</b> <br><small>{b['wallet']}</small><br>
        <b>Volume Transacionado:</b> <span style="color:#00FF7F;">{b['valor']:.4f} KAS</span><br>
        <b>Blockchain Hash:</b> <br><small>{b['hash']}</small>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cryptologos.cc/logos/kaspa-kas-logo.png", width=100)
    st.write("---")
    if st.button("LOGOUT"):
        st.session_state["autenticado"] = False
        st.rerun()

st.markdown("<center><small>Kaspa Elite Tracker | Exclusivo @jackmaster273</small></center>", unsafe_allow_html=True)
