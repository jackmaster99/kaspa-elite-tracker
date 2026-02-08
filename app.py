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
with st.sidebar:
    lang = st.radio("🌐 Language / Idioma", ["Português", "English"])

# Dicionário de tradução
txt = {
    "Português": {
        "titulo": "KASPA ELITE TRACKER",
        "login_msg": "Acesso Restrito @jackmaster273",
        "aviso": "⚠️ TERMOS: Apenas uma sessão ativa por usuário.",
        "calc_titulo": "🧮 Calculadora de Fluxo",
        "whale_titulo": "🐳 Whale Watcher (> 1M KAS)",
        "compra": "COMPRA DETECTADA",
        "venda": "VENDA DETECTADA",
        "logout": "SAIR",
        "entrada": "Entrada em",
    },
    "English": {
        "titulo": "KASPA ELITE TRACKER",
        "login_msg": "Restricted Access @jackmaster273",
        "aviso": "⚠️ TERMS: Only one active session per user.",
        "calc_titulo": "🧮 Flow Calculator",
        "whale_titulo": "🐳 Whale Watcher (> 1M KAS)",
        "compra": "BUY DETECTED",
        "venda": "SELL DETECTED",
        "logout": "LOGOUT",
        "entrada": "Input in",
    }
}

# --- LÓGICA DE LOGIN ---
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
st.markdown("<style>.stApp { background-color: #000; color: #fff; } .card { background-color: #111; padding: 20px; border-radius: 15px; border: 1px solid #00FF7F; margin-bottom: 20px; }</style>", unsafe_allow_html=True)

@st.cache_data(ttl=30)
def get_data():
    k = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true").json()['kaspa']
    d = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['BRL']
    return k, d

kas, dolar = get_data()

st.title(f"🟢 {txt[lang]['titulo']}")

# MÉTRICAS 4 DÍGITOS
c1, c2, c3, c4 = st.columns(4)
c1.metric("KAS / USD", f"$ {kas['usd']:.4f}")
c2.metric("KAS / BRL", f"R$ {kas['brl']:.4f}")
c3.metric("USD / BRL", f"R$ {dolar:.4f}")
c4.metric("24h Var.", f"{kas['usd_24h_change']:.2f}%")

# CALCULADORA
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(txt[lang]["calc_titulo"])
ca, cb, cc = st.columns(3)
v_usd = ca.number_input(f"{txt[lang]['entrada']} Dollar ($):", value=1000.0, format="%.4f")
cb.write(f"↳ **{v_usd / kas['usd']:.4f} KAS**")
cc.write(f"↳ **R$ {v_usd * dolar:.4f}**")
st.markdown('</div>', unsafe_allow_html=True)

# WHALE WATCHER
st.subheader(txt[lang]["whale_titulo"])
baleias = [
    {"tipo": "COMPRA", "valor": 12550340.1255, "label": txt[lang]["compra"]},
    {"tipo": "VENDA", "valor": 8100800.4500, "label": txt[lang]["venda"]}
]
for b in baleias:
    cor = "#00FF7F" if b['tipo'] == "COMPRA" else "#FF4B4B"
    st.markdown(f'<div style="border:1px solid #FFD700;padding:10px;border-radius:10px;margin-bottom:10px;">'
                f'<b style="color:{cor};">{b["label"]}</b> | {b["valor"]:.4f} KAS</div>', unsafe_allow_html=True)

if st.sidebar.button(txt[lang]["logout"]):
    st.session_state["autenticado"] = False
    st.rerun()
