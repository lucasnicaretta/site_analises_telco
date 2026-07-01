import sys
import os
import streamlit as st

# Garante que o Python enxergue o diretório raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Visualização de Dados - InsightStream", layout="wide")

# ==============================================================================
# 1. SIDEBAR E IDENTIFICAÇÃO
# ==============================================================================
st.sidebar.markdown("### Identificação do Usuário")
if 'username' not in st.session_state:
    st.session_state['username'] = ""
st.session_state['username'] = st.sidebar.text_input("Nome:", value=st.session_state['username'])

if st.session_state['username']:
    st.markdown(f"#### Olá, **{st.session_state['username']}**! Bem-vindo ao módulo de auditoria.")
else:
    st.markdown("#### Bem-vindo ao módulo de auditoria.")

st.title("Visualização de Tabelas")
st.markdown("---")

# ==============================================================================
# 2. LÓGICA DE DADOS
# ==============================================================================
if 'arquivo_dados' not in st.session_state or st.session_state['arquivo_dados'] is None:
    st.warning("**Nenhum dado encontrado!** Por favor, volte na **Página Inicial** e faça o upload do arquivo.")
    st.stop()

df_original = st.session_state['arquivo_dados']
todas_colunas = df_original.columns.tolist()

# Inicializa estado das colunas selecionadas
if 'colunas_selecionadas' not in st.session_state:
    st.session_state['colunas_selecionadas'] = todas_colunas

# Funções de Callback para botões
def acao_marcar_todas():
    st.session_state['colunas_selecionadas'] = todas_colunas

def acao_limpar_todas():
    st.session_state['colunas_selecionadas'] = []

# ==============================================================================
# 3. INTERFACE DE FILTROS
# ==============================================================================
with st.expander("Filtrar Colunas"):
    st.markdown("##### Selecione quais colunas exibir:")
    
    cols_layout = st.columns(4)
    novas_selecoes = []
    
    for idx, col_nome in enumerate(todas_colunas):
        with cols_layout[idx % 4]:
            # Se a coluna estiver na lista, o checkbox nasce marcado
            if st.checkbox(col_nome, value=col_nome in st.session_state['colunas_selecionadas'], key=f"check_{col_nome}"):
                novas_selecoes.append(col_nome)
    
    # Botões de Ação
    col_btn1, col_btn2, col_btn3, _ = st.columns([1.5, 1.5, 1.5, 5.5])
    
    with col_btn1:
        if st.button("Aplicar Filtro", type="primary", use_container_width=True):
            st.session_state['colunas_selecionadas'] = novas_selecoes
            st.rerun()
            
    with col_btn2:
        if st.button("Marcar Todas", on_click=acao_marcar_todas, use_container_width=True):
            st.rerun()

    with col_btn3:
        if st.button("Apagar Seleção", on_click=acao_limpar_todas, use_container_width=True):
            st.rerun()

# ==============================================================================
# 4. BUSCA E EXIBIÇÃO
# ==============================================================================
termo_busca = st.text_input("Buscar na Tabela:", placeholder="Digite para filtrar linhas...")

st.markdown("---")

# Aplica as colunas selecionadas
df_exibicao = df_original[st.session_state['colunas_selecionadas']] if st.session_state['colunas_selecionadas'] else df_original

# Aplica a busca (se houver)
if termo_busca:
    mascara = df_exibicao.astype(str).apply(lambda row: row.str.contains(termo_busca, case=False, na=False)).any(axis=1)
    df_exibicao = df_exibicao[mascara]

st.subheader("Dados Analíticos")
if not st.session_state['colunas_selecionadas']:
    st.info("Nenhuma coluna selecionada. Marque as opções acima e clique em 'Aplicar Filtro'.")
else:
    st.dataframe(df_exibicao, use_container_width=True)
    st.metric(label="Linhas Encontradas", value=df_exibicao.shape[0])