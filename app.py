import streamlit as st
import requests
import pandas as pd
# Importação para login com Google
from streamlit_google_auth import Authenticate

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="wide", page_icon="🟢")

# --- LISTA DE E-MAILS AUTORIZADOS (SÓ ESTES ENTRAM) ---
# O senhor só precisa colocar o e-mail aqui. Não precisa mais de senha!
EMAILS_AUTORIZADOS = [
    "jackmaster273@gmail.com",
    "cliente01@gmail.com",
    "baleia@vip.com"
]

# --- CONFIGURAÇÃO DO LOGIN GOOGLE ---
# Nota: Para rodar 100%, o senhor precisará criar as chaves no Google Cloud Console.
# Por enquanto, vamos manter a lógica de verificação de e-mail.
def sistema_login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.markdown(f"""
            <div style="text-align: center; padding-top: 50px;">
                <img src="https://cryptologos.cc/logos/kaspa-kas-logo.png" width="130">
                <h1 style="color: #00FF7F;">KASPA ELITE TRACKER</h1>
                <p style="color: #555;">Acesso via Google | @jackmaster273</p>
            </div>
        """, unsafe_allow_html=True)
        
        col_l, col_c, col_r = st.columns([1,2,1])
        with col_c:
            st.info("ℹ️ Utilize seu e-mail autorizado para acessar o terminal.")
            # Simulação do botão Google (Para integração real, o senhor usaria o ClientID do Google)
            email_teste = st.text_input("Digite seu E-mail Google para validar:")
            
            if st.button("ENTRAR COM GOOGLE"):
                if email_teste in EMAILS_AUTORIZADOS:
                    st.session_state["autenticado"] = True
                    st.session_state["user_email"] = email_teste
                    st.success("Sessão única iniciada!")
                    st.rerun()
                else:
                    st.error("Este e-mail não possui licença ativa no Painel Elite.")
        return False
    return True

if sistema_login():
    # --- ESTILO E DASHBOARD (IGUAL AO ANTERIOR COM PRECISÃO DE 4 DÍGITOS) ---
    st.markdown("<style>.stApp { background-color: #000; color: #fff; } .card { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #00FF7F; margin-bottom: 20px; }</style>", unsafe_allow_html=True)

    @st.cache_data(ttl=30)
    def buscar_dados():
        k = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true").json()['kaspa']
        d = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['BRL']
        return k, d

    kas, dolar = buscar_dados()

    st.title("🟢 TERMINAL KASPA ELITE")
    st.write(f"Conectado como: **{st.session_state['user_email']}**")

    # MÉTRICAS
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("KAS/USD", f"$ {kas['usd']:.4f}")
    c2.metric("KAS/BRL", f"R$ {kas['brl']:.4f}")
    c3.metric("USD/BRL", f"R$ {dolar:.4f}")
    c4.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

    # CALCULADORA (DOLAR - KASPA - REAL)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧮 Calculadora de Conversão")
    ca, cb, cc = st.columns(3)
    v_usd = ca.number_input("Valor em Dólar ($):", value=1000.0, format="%.4f")
    cb.write(f"↳ **{v_usd / kas['usd']:.4f} KAS**")
    cc.write(f"↳ **R$ {v_usd * dolar:.4f}**")
    st.markdown('</div>', unsafe_allow_html=True)

    # WHALE WATCHER COLORIDO
    st.subheader("🐳 Whale Watcher (> 1M KAS)")
    baleia = {"tipo": "COMPRA", "valor": 1500450.0000, "wallet": "kaspa:qrel...7xq", "hash": "7a3d...f92c"}
    cor = "#00FF7F" if baleia['tipo'] == "COMPRA" else "#FF4B4B"
    st.markdown(f'<div style="border: 1px solid #FFD700; background-color: #0a0a00; padding: 15px; border-radius: 10px;">'
                f'<b style="color:{cor};">{baleia["tipo"]}</b> | {baleia["valor"]:.4f} KAS<br>'
                f'<small>Wallet: {baleia["wallet"]}</small></div>', unsafe_allow_html=True)

    if st.sidebar.button("LOGOUT"):
        st.session_state["autenticado"] = False
        st.rerun()
