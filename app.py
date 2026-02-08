import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="KASPA ELITE TRACKER", layout="wide", page_icon="🟢")

# 2. ESTILO CSS ATUALIZADO (MELHOR VISIBILIDADE NA TABELA)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stMetricValue"] { color: #00FF7F !important; font-weight: bold; }

    /* Estilização da Tabela para máxima visibilidade */
    table { color: white !important; background-color: #111111 !important; }
    thead tr th { color: #00FF7F !important; font-size: 16px !important; }
    tbody tr td { color: #FFFFFF !important; font-size: 15px !important; border-bottom: 1px solid #333 !important; }

    .main-card { background-color: #111111; padding: 20px; border-radius: 12px; border: 1px solid #00FF7F; margin-bottom: 20px; }
    .whale-card { background-color: #0a0a0a; border-left: 5px solid #00FF7F; padding: 12px; margin: 10px 0; border: 0.5px solid #333; }
    .halving-box { background: #000; border: 2px solid #00FF7F; padding: 15px; text-align: center; border-radius: 15px; }
    .halving-days { font-size: 45px; color: #00FF7F; font-weight: bold; line-height: 1; }
    .affiliate-card { background: #111; border: 1px solid #00FF7F; padding: 20px; border-radius: 10px; text-align: center; transition: 0.3s; }
    .affiliate-card:hover { border-color: #FFFFFF; transform: translateY(-5px); }
    .buy-button { background-color: #00FF7F; color: black !important; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)


# 3. FUNÇÕES DE DADOS
@st.cache_data(ttl=30)
def get_market_data():
    try:
        kas = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd,brl&include_24hr_change=true",
            timeout=10).json()['kaspa']
        m = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=30&page=1",
            timeout=10).json()
        blacklist = ["whitebit", "figure", "heloc", "staked", "wrapped", "ethena"]
        clean_m = [c for c in m if not any(x in c['name'].lower() for x in blacklist)]
        df = pd.DataFrame(clean_m[:9])[['name', 'current_price', 'price_change_percentage_24h']]
        df.columns = ['Protocolo', 'Preço ($)', '24h (%)']
        df.index = range(1, 10)
        return kas, df
    except:
        return {"usd": 0.1500, "brl": 0.8500, "usd_24h_change": 0}, pd.DataFrame()


def get_whales():
    try:
        r = requests.get("https://api.kaspa.org/transactions/recent?limit=40", timeout=10).json()
        return [{"id": tx['transaction_id'], "val": sum(o['amount'] for o in tx['outputs']) / 1e8} for tx in r if
                sum(o['amount'] for o in tx['outputs']) / 1e8 >= 1000000]
    except:
        return []


# 4. PROCESSAMENTO
hoje = datetime.now()
data_halving = datetime(hoje.year if hoje.month < 12 else hoje.year + 1, (hoje.month % 12) + 1, 1)
dias_restantes = (data_halving - hoje).days
kas, market_df = get_market_data()
whale_list = get_whales()

# --- CABEÇALHO ---
c1, c2, c3 = st.columns([1, 2, 2])
with c1: st.image("https://cryptologos.cc/logos/kaspa-kas-logo.png", width=80)
with c2: st.metric("PREÇO KASPA", f"$ {kas['usd']:.4f}", f"R$ {kas['brl']:.4f}")
with c3: st.markdown(
    f'<div class="halving-box"><small>DIAS PARA PRÓXIMA REDUÇÃO</small><br><span class="halving-days">{dias_restantes}</span><br><small>Dias Estimados</small></div>',
    unsafe_allow_html=True)

st.write("---")

# --- CONTEÚDO PRINCIPAL (COLUNAS) ---
col_l, col_r = st.columns([1.6, 2])

with col_l:
    # CONVERSOR
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("🔄 Conversor Elite")
    modo = st.radio("Escolha:", ["Comprar (Dinheiro ➡️ KAS)", "Vender (KAS ➡️ Dinheiro)"], horizontal=True)
    moeda = st.selectbox("Moeda:", ["Dólar ($)", "Real (R$)"])
    taxa = kas['usd'] if "Dólar" in moeda else kas['brl']

    val = st.number_input("Valor:", min_value=0.0, value=100.0)
    if "Comprar" in modo:
        st.success(f"Você adquire: **{val / taxa:,.2f} KAS**")
    else:
        st.success(f"Valor: **{'$' if 'Dólar' in moeda else 'R$'} {val * taxa:,.4f}**")
    st.markdown('</div>', unsafe_allow_html=True)

    # TRACKER DE CARTEIRA
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("🕵️ Rastreador de Carteira")
    wallet = st.text_input("Cole o endereço Kaspa:", placeholder="kaspa:q...")
    if wallet:
        try:
            res_bal = requests.get(f"https://api.kaspa.org/addresses/{wallet}/balance", timeout=10).json()
            saldo = res_bal.get('balance', 0) / 1e8
            st.markdown(f"### Saldo: {saldo:,.2f} KAS")
            st.write(f"Patrimônio USD: **$ {saldo * kas['usd']:,.4f}**")
            st.write(f"Patrimônio BRL: **R$ {saldo * kas['brl']:,.4f}**")
        except:
            st.error("Erro ao localizar endereço.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    st.subheader("📈 Top 9 Protocolos")
    # Tabela agora com estilo forçado para branco/verde
    st.table(market_df)

    st.write("---")
    st.subheader("🐋 Baleias Detectadas (> 1M KAS)")
    if whale_list:
        for w in whale_list:
            st.markdown(
                f'<div class="whale-card">🟢 <b>{w["val"]:,.0f} KAS</b> em movimento! <a href="https://explorer.kaspa.org/txs/{w["id"]}" target="_blank">Explorer ↗️</a></div>',
                unsafe_allow_html=True)
    else:
        st.write("Monitorando a rede...")

st.write("---")

# --- SEÇÃO DE AFILIADOS ---
st.subheader("🛡️ Segurança Elite: Proteja suas Moedas")
st.write("Não deixe suas Kaspas em corretoras. Use uma Hard Wallet recomendada:")

af_col1, af_col2 = st.columns(2)

with af_col1:
    st.markdown(f"""
    <div class="affiliate-card">
        <h3>Tangem Wallet</h3>
        <p>A favorita da comunidade Kaspa. Sem cabos, formato de cartão.</p>
        <a class="buy-button" href="COLE_SEU_LINK_TANGEM_AQUI" target="_blank">COMPRAR COM DESCONTO</a>
    </div>
    """, unsafe_allow_html=True)

with af_col2:
    st.markdown(f"""
    <div class="affiliate-card">
        <h3>Ledger Nano X</h3>
        <p>A carteira mais segura e conhecida do mundo cripto.</p>
        <a class="buy-button" href="COLE_SEU_LINK_LEDGER_AQUI" target="_blank">VER PREÇO NA LOJA</a>
    </div>
    """, unsafe_allow_html=True)

# --- DOAÇÃO E CRÉDITOS ---
st.markdown(f'''<div style="border:1px dashed #00FF7F; padding:15px; border-radius:10px; text-align:center; margin-top:40px;">
<b>APOIE O DESENVOLVEDOR 🇧🇷</b><br><code>kaspa:qqzsfxvjya7kpcgq74st2fkmv2a8h43erq3k2fynxsju2v2dp5t5z3kz8v2pk</code><br>
<small>Kaspa Elite Tracker v15.0 | jackmaster273</small></div>''', unsafe_allow_html=True)