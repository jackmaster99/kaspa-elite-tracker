import streamlit as st
import requests
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="centered", page_icon="🟢")

# --- SISTEMA DE LOGIN SEGURO ---
def verificar_acesso():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.markdown(f"""
            <div style="text-align: center; padding-top: 50px;">
                <img src="https://cryptologos.cc/logos/kaspa-kas-logo.png" width="100">
                <h1 style="color: #00FF7F; font-family: sans-serif;">KASPA ELITE TRACKER</h1>
                <p style="color: #666;">Acesso Restrito: @jackmaster273</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div style="max-width: 400px; margin: 0 auto; background-color: #111; padding: 30px; border-radius: 15px; border: 1px solid #333;">', unsafe_allow_html=True)
            senha = st.text_input("Chave de Acesso:", type="password")
            if st.button("DESBLOQUEAR PAINEL"):
                if senha == "Kaspa26!@#$%":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Chave inválida.")
            st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

# --- CONTEÚDO COMPLETO DO APP ---
if verificar_acesso():
    # ESTILO VISUAL AVANÇADO
    st.markdown("""
        <style>
        .stApp { background-color: #000000; color: #FFFFFF; }
        .card { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #00FF7F; margin-bottom: 20px; }
        .highlight { color: #00FF7F; font-weight: bold; }
        [data-testid="stMetricValue"] { color: #00FF7F !important; font-size: 32px !important; }
        </style>
        """, unsafe_allow_html=True)

    # BUSCA DE DADOS (PREÇO E MERCADO)
    @st.cache_data(ttl=30)
    def fetch_data():
        try:
            kas = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true", timeout=10).json()['kaspa']
            # Busca Top 5 Moedas para Comparação
            m = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=7&page=1", timeout=10).json()
            df = pd.DataFrame([c for c in m if c['symbol'] not in ['usdt', 'usdc']][:5])[['name', 'current_price']]
            df.columns = ['Ativo', 'Preço ($)']
            return kas, df
        except:
            return {"usd": 0.0, "brl": 0.0, "usd_24h_change": 0.0}, pd.DataFrame()

    kas, top_df = fetch_data()

    # CABEÇALHO ATIVO
    st.markdown(f'<p style="color:#00FF7F; margin-bottom:0;">Painel de Elite Ativo: @jackmaster273</p>', unsafe_allow_html=True)
    st.title("📈 Monitoramento Global Kaspa")
    
    # MÉTRICAS PRINCIPAIS
    col1, col2, col3 = st.columns(3)
    col1.metric("Preço USD", f"$ {kas['usd']:.4f}")
    col2.metric("Preço BRL", f"R$ {kas['brl']:.4f}")
    col3.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

    st.write("---")

    # CONVERSOR E CALCULADORA
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔄 Calculadora de Investimento")
    c1, c2 = st.columns(2)
    invest = c1.number_input("Valor para Investir ($):", min_value=0.0, value=1000.0)
    if kas['usd'] > 0:
        c2.markdown(f"<br><p style='font-size:20px;'>Você recebe: <span class='highlight'>{invest / kas['usd']:,.2f} KAS</span></p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # COMPARATIVO DE MERCADO
    st.subheader("🏆 Top Ativos do Mercado")
    st.table(top_df)

    # SEÇÃO DE SEGURANÇA (AFILIADOS)
    st.subheader("🛡️ Proteção de Patrimônio")
    st.markdown("""
    <div class="card" style="text-align: center;">
        <h4>Tangem Wallet</h4>
        <p>A carteira oficial recomendada para armazenar sua Kaspa com segurança máxima.</p>
        <a href="#" target="_blank" style="background-color: #00FF7F; color: black; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold;">ADQUIRIR COM DESCONTO</a>
    </div>
    """, unsafe_allow_html=True)

    # BARRA LATERAL
    with st.sidebar:
        st.image("https://cryptologos.cc/logos/kaspa-kas-logo.png", width=100)
        st.write("---")
        if st.button("ENCERRAR SESSÃO"):
            st.session_state["autenticado"] = False
            st.rerun()

    st.markdown(f'<div style="text-align:center; margin-top:50px; font-size:10px; color:#444;">Desenvolvido por @jackmaster273 | v1.2</div>', unsafe_allow_html=True)
