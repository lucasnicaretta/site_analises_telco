import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Visualização de Dados - InsightStream", layout="wide")

st.title("Visualização de Tabelas")
if 'username' in st.session_state and st.session_state['username']:
    st.markdown(f"#### Olá, **{st.session_state['username']}**! Aqui você tem a visualização e filtros da sua tabela.")
else:
    st.markdown("#### Aqui você tem a visualização e filtros da sua tabela com uma visão mais dinâmica.")
    
st.markdown("---")

# 3. LÓGICA DE DADOS
if 'arquivo_dados' not in st.session_state or st.session_state['arquivo_dados'] is None:
    st.warning("**Nenhum dado encontrado!** Por favor, volte na **Página Inicial** e faça o upload do arquivo.")
    st.stop()

df_original = st.session_state['arquivo_dados']
todas_colunas = df_original.columns.tolist()

# Variável de CONTROLE (UI dos checkboxes)
if 'colunas_selecionadas' not in st.session_state:
    st.session_state['colunas_selecionadas'] = todas_colunas

# Variável de EXIBIÇÃO (O que a tabela mostra)
if 'colunas_exibidas' not in st.session_state:
    st.session_state['colunas_exibidas'] = todas_colunas

# Funções de Callback
def acao_marcar_todas():
    st.session_state['colunas_selecionadas'] = todas_colunas

def acao_limpar_todas():
    st.session_state['colunas_selecionadas'] = []

# 4. INTERFACE DE FILTROS
with st.expander("Filtrar Colunas", expanded=True):
    st.markdown("##### Selecione quais colunas exibir:")
    
    cols_layout = st.columns(4)
    novas_selecoes = []
    
    # Checkboxes ligados a 'colunas_selecionadas' (UI)
    for idx, col_nome in enumerate(todas_colunas):
        with cols_layout[idx % 4]:
            if st.checkbox(col_nome, value=col_nome in st.session_state['colunas_selecionadas']):
                novas_selecoes.append(col_nome)
    
    # Botões de Ação
    col_btn1, col_btn2, col_btn3, _ = st.columns([1.5, 1.5, 1.5, 5.5])
    
    with col_btn1:
        # BOTÃO APLICAR: Copia o que foi selecionado para as colunas exibidas
        if st.button("Aplicar Filtro", type="primary", use_container_width=True):
            st.session_state['colunas_selecionadas'] = novas_selecoes
            st.session_state['colunas_exibidas'] = novas_selecoes
            st.rerun()
            
    with col_btn2:
        # Apenas atualiza a UI (checkboxes), não a tabela
        if st.button("Marcar Todas", use_container_width=True):
            acao_marcar_todas()
            st.rerun()

    with col_btn3:
        # Apenas atualiza a UI (checkboxes), não a tabela
        if st.button("Apagar Seleção", use_container_width=True):
            acao_limpar_todas()
            st.rerun()

# 5. BUSCA E EXIBIÇÃO
termo_busca = st.text_input("Buscar na Tabela:", placeholder="Digite para filtrar linhas...")

st.markdown("---")

# Aplica as colunas EXIBIDAS (O que foi confirmado pelo botão Aplicar)
if st.session_state['colunas_exibidas']:
    df_exibicao = df_original[st.session_state['colunas_exibidas']]
else:
    df_exibicao = df_original.iloc[:, 0:0] 

# Aplica a busca (na tabela já filtrada pelas colunas escolhidas)
if termo_busca:
    mascara = df_exibicao.astype(str).apply(lambda row: row.str.contains(termo_busca, case=False, na=False)).any(axis=1)
    df_exibicao = df_exibicao[mascara]

st.subheader("Dados Analíticos")
if not st.session_state['colunas_exibidas']:
    st.info("Nenhuma coluna selecionada. Marque as opções acima e clique em 'Aplicar Filtro'.")
else:
    st.dataframe(df_exibicao, use_container_width=True)
    st.metric(label="Linhas Encontradas", value=df_exibicao.shape[0])