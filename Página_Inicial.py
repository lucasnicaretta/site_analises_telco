import streamlit as st
import pandas as pd

# ==============================================================================
# 1. CONFIGURAÇÃO AMBIENTAL DA HOME
# ==============================================================================
st.set_page_config(
    page_title="InsightStream - Home",
    page_icon="🏠",
    layout="wide"
)

# ---------------------------------------------------------------------------
# REQUISITO DO PDF: SIDEBAR GLOBAL PARA CAPTURA DO NOME (Salvo na Sessão)
# ---------------------------------------------------------------------------
st.sidebar.markdown("### 👤 Identificação do Usuário")
if 'username' not in st.session_state:
    st.session_state['username'] = ""

# Input text que persiste o nome do usuário entre a troca de páginas
nome_input = st.sidebar.text_input("Digite seu nome completo:", value=st.session_state['username'])
st.session_state['username'] = nome_input

# ---------------------------------------------------------------------------
# CONTEÚDO PRINCIPAL: IDENTIDADE DA "EMPRESA" (BÔNUS DO PDF)
# ---------------------------------------------------------------------------
st.title("Bem-vindo à InsightStream Analytics")
st.markdown("#### Soluções Avançadas em Business Intelligence & Retenção de Clientes")
st.markdown("---")

# Apresentação corporativa atendendo ao bônus sugerido no projeto
st.markdown("""
A **InsightStream** é uma consultoria especializada em engenharia de dados e diagnóstico de rotatividade. 
Esta plataforma foi desenvolvida sob medida para explorar os dados operacionais da sua empresa, 
identificar com precisão os gargalos que geram o cancelamento de serviços (**Churn**) e fornecer 
diretrizes estratégicas para o aumento do ciclo de vida dos seus clientes.
""")

st.markdown("### Ingestão da Base de Dados")
st.markdown("Por favor, faça o upload do arquivo contendo os dados demográficos e de consumo dos clientes para liberar os módulos de auditoria tabular e análise gráfica.")

# Componente de Upload do Dataset
arquivo_carregado = st.file_uploader("Carregue seu arquivo no formato .csv", type=["csv"])

if arquivo_carregado is not None:
    try:
        # Armazena o DataFrame na sessão global do Streamlit
        df = pd.read_csv(arquivo_carregado)
        st.session_state['arquivo_dados'] = df
        
        linhas, colunas = df.shape
        st.success(f"Base de dados integrada e processada com sucesso!")
        
        # Informativo de metadados para guiar o analista
        st.info(f"**Mapeamento Concluído:** Foram identificados **{linhas} registros (clientes)** e **{colunas} variáveis** operacionais prontas para análise.")
        
        # Interação amigável com o nome do usuário
        if st.session_state['username']:
            st.markdown(f"**Pronto, {st.session_state['username']}!** Use a barra lateral para navegar entre a visualização de tabelas e a geração de gráficos.")
            
    except Exception as e:
        st.error(f" Erro crítico ao processar o arquivo CSV: {e}")
else:
    st.warning(" Aguardando a importação da base de dados (.csv) para ativar as demais páginas do sistema.")