import streamlit as st
import requests
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="centered", page_icon="🟢")

# --- SISTEMA DE LOGIN ---
def verificar_acesso():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        # Identidade Visual no Login
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="https://cryptologos.cc/logos/kaspa-kas-logo.png" width="100">
                <h1 style="color: #00FF7F; margin-bottom: 0;">KASPA ELITE TRACKER</h1>
                <p style="color: #555;">@jackmaster273</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        
        # Caixa de Entrada
        with st.container():
            st.markdown('<div style="background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #333;">', unsafe_allow_html=True)
            user = st.text_input("Usuário:", value="@jackmaster273")
            senha = st.text_input("Senha de Acesso:", type="password")
            
            if st.button("ACESSAR SISTEMA"):
                # Validação da senha escolhida
                if senha == "Kaspa26!@#$%":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Acesso negado. Verifique os dados.")
            st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

# Conteúdo Protegido
if verificar_acesso():
    # ESTILO VISUAL DARK MODE
    st.markdown("""
        <style>
        .stApp { background-color: #000000; color: #FFFFFF; }
        .main-card { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #00FF7F; }
        [data-testid="stMetricValue"] { color: #00FF7F !important; }
        </style>
        """, unsafe_allow_html=True)

    # BUSCA DE PREÇOS (API)
    @st.cache_data(ttl=30)
    def get_kas_price():
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl"
            return requests.get(url, timeout=10).json()['kaspa']
        except:
            return {"usd": 0.0000, "brl": 0.0000}

    kas = get_kas_price()

    # DASHBOARD PRINCIPAL
    st.markdown(f'<p style="color:#00FF7F;">Painel Ativo: @jackmaster273</p>', unsafe_allow_html=True)
    st.title("📊 Monitoramento Kaspa")
    
    col1, col2 = st.columns(2)
    col1.metric("Preço USD", f"$ {kas['usd']:.4f}")
    col2.metric("Preço BRL", f"R$ {kas['brl']:.4f}")

    st.write("---")
    
    # FERRAMENTA DE CONVERSÃO
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("🔄 Conversor Elite")
    qtd = st.number_input("Valor para converter (USD):", min_value=0.0, value=100.0)
    if kas['usd'] > 0:
        st.success(f"Equivale a: **{qtd / kas['usd']:,.2f} KAS**")
    st.markdown('</div>', unsafe_allow_html=True)

    # BARRA LATERAL PARA SAÍDA
    if st.sidebar.button("LOGOUT / SAIR"):
        st.session_state["autenticado"] = False
        st.rerun()

    # RODAPÉ
    st.markdown(f'''<div style="text-align:center; margin-top:50px; font-size:10px; color:#444;">
        Desenvolvido por @jackmaster273 <br> Kaspa Elite Tracker v1.0
    </div>''', unsafe_allow_html=True)
