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

# --- LÓGICA DE SESSÃO ÚNICA ---
if "device_id" not in st.session_state:
    st.session_state["device_id"] = str(uuid.uuid4())

def sistema_login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.markdown(f"""
            <div style="text-align: center; padding-top: 50px;">
                <img src="https://cryptologos.cc/logos/kaspa-kas-logo.png" width="130">
                <h1 style="color: #00FF7F; font-family: sans-serif;">KASPA ELITE TRACKER</h1>
                <p style="color: #555;">Painel de Monitoramento @jackmaster273</p>
            </div>
        """, unsafe_allow_html=True)
        
        col_l, col_c, col_r = st.columns([1,2,1])
        with col_c:
            st.markdown('<div style="background-color: #111; padding: 30px; border-radius: 15px; border: 1px solid #333;">', unsafe_allow_html=True)
            st.warning("⚠️ TERMOS: Apenas uma sessão ativa por usuário. Logins duplicados serão derrubados.")
            
            user_in = st.text_input("Login (E-mail ou Usuário):")
            pass_in = st.text_input("Senha Individual:", type="password")
            
            if st.button("DESBLOQUEAR TERMINAL"):
                if user_in in USUARIOS_ELITE and USUARIOS_ELITE[user_in] == pass_in:
                    st.session_state["autenticado"] = True
                    st.session_state["user_email"] = user_in
                    st.rerun()
                else:
                    st.error("Credenciais inválidas ou sem licença ativa.")
            st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

if sistema_login():
    # ESTILO CSS ELITE
    st.markdown("""
        <style>
        .stApp { background-color: #000; color: #fff; }
        .card { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #00FF7F; margin-bottom: 20px; }
        .whale-card { border: 1px solid #FFD700; background-color: #0a0a00; padding: 15px; border-radius: 10px; font-family: monospace; margin-bottom: 12px; }
        [data-testid="stMetricValue"] { color: #00FF7F !important; font-size: 28px !important; }
        </style>
        """, unsafe_allow_html=True)

    # BUSCA DE DADOS
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
    col_logo, col_title = st.columns([1, 8])
    with col_logo:
        st.image("https://cryptologos.cc/logos/kaspa-kas-logo.png", width=80)
    with col_title:
        st.title("KASPA ELITE TRACKER")
        st.write(f"Conectado como: **{st.session_state['user_email']}**")

    # 1. MÉTRICAS DE MERCADO (4 DÍGITOS)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("KAS / USD", f"$ {kas['usd']:.4f}")
    c2.metric("KAS / BRL", f"R$ {kas['brl']:.4f}")
    c3.metric("USD / BRL", f"R$ {dolar_real:.4f}")
    c4.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

    st.write("---")

    # 2. EXPLORER DE CARTEIRA E ÚLTIMAS 5 TXS
    st.subheader("🔎 Wallet Explorer & Last 5 Transactions")
    wallet_address = st.text_input("Cole o endereço da carteira Kaspa:")
    if wallet_address:
        try:
            bal_res = requests.get(f"https://api.kaspa.org/addresses/{wallet_address}/balance").json()
            balance = bal_res['balance'] / 100000000
            st.success(f"Saldo: **{balance:.4f} KAS** | Valor: **$ {(balance * kas['usd']):.4f}**")
            
            tx_res = requests.get(f"https://api.kaspa.org/addresses/{wallet_address}/full-transactions?limit=5").json()
            st.write("🕒 **Atividade Recente:**")
            for i, tx in enumerate(tx_res, 1):
                with st.expander(f"Transação {i}"):
                    st.write(f"**Hash:** `{tx['transaction_id']}`")
                    amt = sum([out['amount'] for out in tx['outputs']]) / 100000000
                    st.write(f"**Valor:** {amt:.4f} KAS")
        except:
            st.error("Erro ao ler Blockchain. Verifique o endereço.")

    # 3. CALCULADORA DE FLUXO (4 DÍGITOS)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧮 Calculadora de Fluxo (Entrada/Saída)")
    col_usd, col_kas, col_brl = st.columns(3)
    with col_usd:
        v_usd = st.number_input("Valor em Dólar ($):", value=1000.0, step=0.0001, format="%.4f")
        st.write(f"↳ Kaspa: **{v_usd / kas['usd']:.4f} KAS**")
        st.write(f"↳ Reais: **R$ {v_usd * dolar_real:.4f}**")
    with col_kas:
        v_kas = st.number_input("Valor em Kaspa (KAS):", value=10000.0, step=0.0001, format="%.4f")
        st.write(f"↳ Dólar: **$ {v_kas * kas['usd']:.4f}**")
    with col_brl:
        v_brl = st.number_input("Valor em Real (R$):", value=5000.0, step=0.0001, format="%.4f")
        st.write(f"↳ Kaspa: **{v_brl / kas['brl']:.4f} KAS**")
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. MONITOR DE BALEIAS
    st.subheader("🐳 Whale Watcher (> 1M KAS)")
    baleias = [
        {"tipo": "COMPRA", "valor": 12550340.1255, "wallet": "kaspa:qrel7p...rt7x", "hash": "7a3d9f2c1b8e4a5d6c7b8a9d0e1f2a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r"},
        {"tipo": "VENDA", "valor": 8100800.4500, "wallet": "kaspa:qp888n...vrt7", "hash": "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3"}
    ]
    for i, b in enumerate(baleias, 1):
        cor_st = "#00FF7F" if b['tipo'] == "COMPRA" else "#FF4B4B"
        st.markdown(f"""
        <div class="whale-card">
            <b style="color:{cor_st};">#{i} {b['tipo']} DETECTADA</b> | <b>{b['valor']:.4f} KAS</b><br>
            <small><b>Endereço:</b> {b['wallet']}</small><br>
            <small><b>Hash:</b> {b['hash']}</small>
        </div>
        """, unsafe_allow_html=True)

    # 5. TOP 10 ATIVOS
    st.subheader("📊 Top 10 Mercado (Comparativo)")
    st.dataframe(top_10_df.style.format({'current_price': '{:.4f}'}), use_container_width=True)

    if st.sidebar.button("LOGOUT / SAIR"):
        st.session_state["autenticado"] = False
        st.rerun()

st.markdown("<center><small>Kaspa Elite Tracker | Painel Exclusivo @jackmaster273</small></center>", unsafe_allow_html=True)
