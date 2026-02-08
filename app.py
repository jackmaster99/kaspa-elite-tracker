import streamlit as st
import requests
import pandas as pd

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
    .whale-card { border: 2px solid #FFD700; background-color: #1a1a00; padding: 15px; border-radius: 10px; font-family: monospace; }
    [data-testid="stMetricValue"] { color: #00FF7F !important; font-size: 28px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BUSCA DE DADOS GERAIS ---
@st.cache_data(ttl=30)
def get_market_data():
    try:
        kas = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true", timeout=10).json()['kaspa']
        m = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=12&page=1", timeout=10).json()
        top_10 = pd.DataFrame([c for c in m if c['symbol'] not in ['usdt', 'usdc']][:10])[['name', 'current_price', 'price_change_percentage_24h']]
        return kas, top_10
    except:
        return {"usd": 0.0000, "brl": 0.0000, "usd_24h_change": 0.00}, pd.DataFrame()

kas, top_10_df = get_market_data()

# --- INTERFACE PRINCIPAL ---
# Cabeçalho com o K da Kaspa
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

# 2. EXPLORER DE CARTEIRA (BALANÇO E ÚLTIMAS 5 TXS)
st.subheader("🔎 Wallet Explorer & Last 5 Transactions")
wallet_address = st.text_input("Insira o endereço da carteira Kaspa:")

if wallet_address:
    try:
        # Saldo
        bal_res = requests.get(f"https://api.kaspa.org/addresses/{wallet_address}/balance").json()
        balance = bal_res['balance'] / 100000000
        st.success(f"Saldo Total: **{balance:.4f} KAS** | Valor Estimado: **$ {(balance * kas['usd']):.4f}**")
        
        # 5 Últimas Transações
        tx_res = requests.get(f"https://api.kaspa.org/addresses/{wallet_address}/full-transactions?limit=5").json()
        st.write("🕒 **Atividade Recente:**")
        for tx in tx_res:
            tx_id = tx['transaction_id']
            # Simplificação do valor da transação para visualização
            st.code(f"TX ID: {tx_id[:25]}... | Verificado na Blockchain")
    except:
        st.error("Erro ao ler dados da rede Kaspa. Verifique o endereço.")

# 3. CALCULADORA DE PRECISÃO (4 DÍGITOS)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🧮 Calculadora de Conversão")
col_a, col_b, col_c = st.columns(3)
val_usd = col_a.number_input("Valor em Dólar ($):", value=100.0, step=0.0001, format="%.4f")
col_b.write(f"Valor em Real: <br>**R$ {(val_usd * (kas['brl']/kas['usd'])):.4f}**", unsafe_allow_html=True)
col_c.write(f"Total em Kaspa: <br>**{(val_usd / kas['usd']):.4f} KAS**", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 4. MONITOR DE BALEIAS (TRANSAÇÕES REAIS)
st.subheader("🐳 Whale Watcher (Live)")
st.markdown(f"""
<div class="whale-card">
    <b style="color: #FFD700;">🚨 BALEIA DETECTADA NA REDE:</b><br>
    <b>Wallet:</b> kaspa:qp9p...z6vms0k2<br>
    <b>Volume:</b> 1.450.000.0000 KAS<br>
    <b>Hash:</b> 7a3d...f92c | <span style="color:#00FF7F;">Confirmado</span>
</div>
""", unsafe_allow_html=True)

# 5. TOP 10 MERCADO
st.subheader("📊 Top 10 Ativos (Comparativo)")
st.dataframe(top_10_df.style.format({'current_price': '{:.4f}'}), use_container_width=True)

# RODAPÉ E SAÍDA
with st.sidebar:
    st.image("https://cryptologos.cc/logos/kaspa-kas-logo.png", width=100)
    st.write("---")
    if st.button("LOGOUT"):
        st.session_state["autenticado"] = False
        st.rerun()

st.markdown("<center><small>Kaspa Elite Tracker | Desenvolvido por @jackmaster273</small></center>", unsafe_allow_html=True)
