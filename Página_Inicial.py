import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO AMBIENTAL DA HOME
st.set_page_config(
    page_title="InsightStream - Home",
    layout="wide"
)

#INICIALIZAÇÃO DE ESTADO 
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'arquivo_dados' not in st.session_state:
    st.session_state['arquivo_dados'] = None

# SIDEBAR
st.sidebar.markdown("### Identificação do Usuário")
st.session_state['username'] = st.sidebar.text_input("Digite seu nome completo:", value=st.session_state['username'])

# CONTEÚDO PRINCIPAL
st.title("Bem-vindo à InsightStream Analytics")

#SAUDAÇÃO PERSONALIZADA
if st.session_state['username']:
    st.markdown(f"#### Olá, **{st.session_state['username']}**! Bem-vindo(a) à sua central de dados.")
else:
    st.markdown("#### Soluções Avançadas em Business Intelligence & Retenção de Clientes")

st.markdown("---")

st.markdown("""
A **InsightStream** é uma consultoria especializada em engenharia de dados e diagnóstico de rotatividade. 
Esta plataforma foi desenvolvida sob medida para explorar os dados operacionais da sua empresa.
""")

st.markdown("### Ingestão da Base de Dados")
st.markdown("Por favor, faça o upload do arquivo para ativar os módulos.")

#LÓGICA DE UPLOAD PERSISTENTE
def carregar_arquivo():
    if st.session_state['uploader_key'] is not None:
        st.session_state['arquivo_dados'] = pd.read_csv(st.session_state['uploader_key'])

st.file_uploader("Carregue seu arquivo no formato .csv", type=["csv"], key='uploader_key', on_change=carregar_arquivo)

#STATUS DO ARQUIVO
if st.session_state['arquivo_dados'] is not None:
    df = st.session_state['arquivo_dados']
    linhas, colunas = df.shape
    st.success(f"Base de dados integrada e processada com sucesso!")
    st.info(f"**Mapeamento Concluído:** {linhas} registros e {colunas} variáveis.")
else:
    st.warning("Aguardando a importação da base de dados (.csv) para ativar as demais páginas.")