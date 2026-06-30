import streamlit as st

# ==============================================================================
# 1. CONFIGURAÇÃO AMBIENTAL DA PÁGINA (ESTÁTICA & RESPONSIVA)
# ==============================================================================
st.set_page_config(
    page_title="Visualização de Dados - InsightStream", 
    layout="wide"
)

# ---------------------------------------------------------------------------
# REQUISITO DO PDF: SIDEBAR GLOBAL PARA MANTER O ESTADO DO NOME DO USUÁRIO
# ---------------------------------------------------------------------------
st.sidebar.markdown("### Identificação do Usuário")
if 'username' not in st.session_state:
    st.session_state['username'] = ""

# Sincroniza o input do nome com o session_state para não resetar na navegação
nome_input = st.sidebar.text_input("Digite seu nome completo:", value=st.session_state['username'])
st.session_state['username'] = nome_input

# ---------------------------------------------------------------------------
# REQUISITO DO PDF: SAUDAÇÃO FORMAL COM O NOME DO USUÁRIO NO INÍCIO DA PÁGINA
# ---------------------------------------------------------------------------
if st.session_state['username']:
    st.markdown(f"#### Olá, **{st.session_state['username']}**! Bem-vindo ao módulo de auditoria.")
else:
    st.markdown("#### Bem-vindo ao módulo de auditoria.")

st.title("Visualização de Tabelas")
st.markdown("---")

# ==============================================================================
# 2. VERIFICAÇÃO AUTOMÁTICA: PUXA DIRETO O ARQUIVO EM MEMÓRIA SESSÃO
# ==============================================================================
if 'arquivo_dados' in st.session_state and st.session_state['arquivo_dados'] is not None:
    
    # Recupera o arquivo original do session_state
    df_original = st.session_state['arquivo_dados']
    todas_colunas = df_original.columns.tolist()
    
    # Inicializa o estado das colunas selecionadas com todas se for o primeiro acesso
    if 'colunas_selecionadas' not in st.session_state:
        st.session_state['colunas_selecionadas'] = todas_colunas

    # --- CALLBACKS PARA OS BOTÕES ---
    # Marcar todas as colunas
    def limpar_filtros_callback():
        st.session_state['colunas_selecionadas'] = todas_colunas
        for col in todas_colunas:
            st.session_state[f"col_{col}"] = True

    # Desmarcar todas as colunas (Apagar Seleção)
    def apagar_selecao_callback():
        st.session_state['colunas_selecionadas'] = []
        for col in todas_colunas:
            st.session_state[f"col_{col}"] = False

    # ---------------------------------------------------------------------------
    # 1. PAINEL DE FILTRAR COLUNAS
    # ---------------------------------------------------------------------------
    with st.expander("Filtrar Colunas"):
        st.markdown("##### Selecione quais colunas você quer exibir na tabela abaixo:")
        
        colunas_escolhidas = []
        cols_layout = st.columns(4)
        
        for idx, col_nome in enumerate(todas_colunas):
            with cols_layout[idx % 4]:
                # Define o valor baseado no estado atual da memória do Streamlit
                valor_padrao = col_nome in st.session_state['colunas_selecionadas']
                
                if st.checkbox(col_nome, value=valor_padrao, key=f"col_{col_nome}"):
                    colunas_escolhidas.append(col_nome)
        
        # Alinhamento padronizado dos botões com tamanhos idênticos e proporcionais
        col_btn1, col_btn2, col_btn3, _ = st.columns([1.5, 1.5, 1.5, 5.5])
        
        with col_btn1:
            if st.button("Aplicar Filtro", type="primary", use_container_width=True):
                if colunas_escolhidas:
                    st.session_state['colunas_selecionadas'] = colunas_escolhidas
                    st.rerun()
                else:
                    st.error("Escolha pelo menos 1 coluna para aplicar!")
                    
        with col_btn2:
            if st.button("Marcar Todas", type="secondary", on_click=limpar_filtros_callback, use_container_width=True):
                st.rerun()

        with col_btn3:
            if st.button("Apagar Seleção", type="secondary", on_click=apagar_selecao_callback, use_container_width=True):
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------------
    # 2. ABA DE BUSCA GLOBAL
    # ---------------------------------------------------------------------------
    termo_busca = st.text_input(
        "Buscar na Tabela:", 
        placeholder="Digite qualquer termo para filtrar as linhas (Ex: Casado, Fibra Óptica, Desligado...)"
    )

    st.markdown("---")

    # ---------------------------------------------------------------------------
    # 3. PROCESSAMENTO DOS DADOS (Colunas + Busca)
    # ---------------------------------------------------------------------------
    if st.session_state['colunas_selecionadas']:
        df_exibicao = df_original[st.session_state['colunas_selecionadas']]
    else:
        df_exibicao = df_original.copy() # Mostra o original temporariamente antes de aplicar
    
    if termo_busca:
        mascara = df_exibicao.astype(str).apply(
            lambda row: row.str.contains(termo_busca, case=False, na=False)
        ).any(axis=1)
        df_exibicao = df_exibicao[mascara]

    # ---------------------------------------------------------------------------
    # 4. EXIBIÇÃO DA TABELA FINAL (REQUISITO: MODO ESTÁTICO)
    # ---------------------------------------------------------------------------
    st.subheader("Dados Analíticos")
    
    if not st.session_state['colunas_selecionadas']:
        st.info("Todas as colunas foram desmarcadas. Selecione as colunas desejadas e clique em **'Aplicar Filtro'**.")
    else:
        # Modo estático garantido com st.dataframe
        st.dataframe(df_exibicao, use_container_width=True)
        st.metric(label="Linhas Encontradas", value=df_exibicao.shape[0])

else:
    st.warning("**Nenhum dado encontrado!** Por favor, volte na **Página Inicial** e faça o upload do seu arquivo CSV.")