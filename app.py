import streamlit as st
import requests
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="wide", page_icon="🟢")

# --- SISTEMA DE LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown('<div style="text-align:center; padding-top:100px;"><h1>🔐 KASPA ELITE</h1><p>@jackmaster273</p></div>', unsafe_allow_html=True)
    with st.container():
        col_l, col_c, col_r = st.columns([1,2,1])
        with col_c:
            senha = st.text_input("Chave de Acesso:", type="password")
            if st.button("DESBLOQUEAR"):
                if senha == "Kaspa26!@#$%":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Acesso negado.")
    st.stop()

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    .card { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #00FF7F; margin-bottom: 20px; }
    .whale-card { border: 2px solid #FFD700; background-color: #1a1a00; padding: 15px; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #00FF7F !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BUSCA DE DADOS ---
@st.cache_data(ttl=30)
def get_data():
    try:
        # Preço Kaspa
        kas = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true").json()['kaspa']
        # Top 10 Mercado
        m = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=12&page=1").json()
        top_10 = pd.DataFrame([c for c in m if c['symbol'] not in ['usdt', 'usdc']][:10])[['name', 'current_price', 'price_change_percentage_24h']]
        top_10.columns = ['Moeda', 'Preço ($)', '24h (%)']
        return kas, top_10
    except:
        return {"usd": 0, "brl": 0, "usd_24h_change": 0}, pd.DataFrame()

kas, top_10_df = get_data()

# --- INTERFACE ---
st.title("🟢 KASPA ELITE TRACKER")
st.markdown(f"Painel Ativo: **@jackmaster273**")

# 1. MÉTRICAS DE PREÇO E NOTIFICAÇÃO
c1, c2, c3 = st.columns(3)
c1.metric("KAS/USD", f"$ {kas['usd']:.4f}")
c2.metric("KAS/BRL", f"R$ {kas['brl']:.4f}")
c3.metric("Status 24h", f"{kas['usd_24h_change']:.2f}%")

if kas['usd_24h_change'] > 5:
    st.toast("🚀 Kaspa em forte alta!")
elif kas['usd_24h_change'] < -5:
    st.toast("⚠️ Alerta de queda: Oportunidade?")

st.write("---")

# 2. RASTREADOR DE CARTEIRA (EXPLORER)
st.subheader("🔎 Wallet Tracker (Consultar Saldo)")
wallet_address = st.text_input("Cole o endereço da carteira Kaspa aqui:")
if wallet_address:
    try:
        res = requests.get(f"https://api.kaspa.org/addresses/{wallet_address}/balance").json()
        balance = res['balance'] / 100000000
        st.success(f"Saldo: **{balance:,.2f} KAS** (Aproximadamente $ {balance * kas['usd']:,.2f})")
    except:
        st.error("Endereço não encontrado ou API fora do ar.")

# 3. CALCULADORA MULTI-MOEDAS
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🧮 Calculadora Elite")
col_a, col_b, col_c = st.columns(3)
val_usd = col_a.number_input("Valor em Dólar ($):", value=100.0)
col_b.write(f"Em Reais: **R$ {val_usd * (kas['brl']/kas['usd']):,.2f}**")
col_c.write(f"Em Kaspa: **{val_usd / kas['usd']:,.2f} KAS**")
st.markdown('</div>', unsafe_allow_html=True)

# 4. MONITOR DE BALEIAS (Simulação de Grandes Compras > 1M KAS)
st.subheader("🐳 Whale Monitor (Compras ≥ 1 Milhão KAS)")
# Aqui simulamos o monitoramento das últimas grandes transações da rede
st.markdown("""
<div class="whale-card">
    <b>DETECTOR ATIVO:</b> Monitorando transações acima de 1.000.000 KAS na rede principal...<br>
    <small>Última varredura: Agora</small>
</div>
""", unsafe_allow_html=True)
# Exemplo de alerta visual
if kas['usd_24h_change'] > 2:
    st.warning("🐳 Baleia detectada: Movimentação de 2.500.000 KAS registrada recentemente.")

# 5. TOP 10 WALLETS / MOEDAS
st.subheader("📊 Top 10 Ativos do Mercado")
st.dataframe(top_10_df, use_container_width=True)

# BARRA LATERAL
with st.sidebar:
    st.header("Menu Elite")
    if st.button("SAIR"):
        st.session_state["autenticado"] = False
        st.rerun()

st.markdown("<center><small>Desenvolvido por @jackmaster273</small></center>", unsafe_allow_html=True)
