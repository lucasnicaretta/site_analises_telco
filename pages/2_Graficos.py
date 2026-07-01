import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#Imports
from utils_email import enviar_email_seguro
import streamlit as st
import matplotlib.pyplot as plt

# 1. CONFIGURAÇÃO E SEGURANÇA
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="InsightStream - Gráficos", layout="wide")

# Verificação de segurança
if 'arquivo_dados' not in st.session_state or st.session_state['arquivo_dados'] is None:
    st.error("⚠️ Nenhum arquivo carregado. Volte à Página Inicial.")
    st.stop()

df = st.session_state['arquivo_dados']

# 2. TÍTULO E SAUDAÇÃO
st.title("Criação de Gráficos")
if st.session_state['username']:
    st.markdown(f"#### Olá, **{st.session_state['username']}**! Aqui você cria seus gráficos para enxergar seus dados diferentes.")
else:
    st.markdown("#### Aqui você cria seus gráficos para enxergar seus dados diferentes.")

st.markdown("---")

# 3. SELEÇÃO DE DADOS E TIPO DE GRÁFICO
col_a, col_b = st.columns(2)

with col_a:
    coluna_1 = st.selectbox(
        "Selecione a primeira coluna:", 
        options=df.columns, 
        index=None, 
        placeholder="Selecione..."
    )

with col_b:
    lista_graficos = [
        "Pizza", 
        "Barras Verticais", 
        "Barras Horizontais", 
        "Histograma", 
        "Linha", 
        "Área", 
        "Boxplot", 
        "Dispersão"
    ]
    tipo = st.selectbox(
        "Selecione o modelo de gráfico:", 
        options=lista_graficos, 
        index=None, 
        placeholder="Selecione o tipo..."
    )

# Lógica condicional para gráficos que exigem 2 colunas
coluna_2 = None
if tipo == "Dispersão":
    coluna_2 = st.selectbox("Selecione a segunda coluna (Eixo Y):", options=df.columns, index=None)

# 4. GERAÇÃO DO GRÁFICO
# Verifica se as seleções obrigatórias foram feitas
pode_gerar = (coluna_1 and tipo) and (tipo != "Dispersão" or coluna_2)

if pode_gerar:
    fig, ax = plt.subplots(figsize=(5, 3)) 

    try:
        # Lógica para cada tipo de gráfico
        if tipo == "Pizza":
            contagem = df[coluna_1].value_counts()
            ax.pie(contagem, labels=contagem.index, autopct='%1.1f%%', textprops={'fontsize': 8})
            
        elif tipo == "Barras Verticais":
            df[coluna_1].value_counts().plot(kind='bar', ax=ax, color='skyblue')
            
        elif tipo == "Barras Horizontais":
            df[coluna_1].value_counts().plot(kind='barh', ax=ax, color='lightgreen')
            
        elif tipo == "Histograma":
            df[coluna_1].hist(ax=ax, bins=20, color='salmon', edgecolor='black')
            
        elif tipo == "Linha":
            df[coluna_1].value_counts().sort_index().plot(kind='line', ax=ax, marker='o', color='purple')
            
        elif tipo == "Área":
            df[coluna_1].value_counts().sort_index().plot(kind='area', ax=ax, alpha=0.5, color='orange')
            
        elif tipo == "Boxplot":
            df.boxplot(column=[coluna_1], ax=ax, grid=False)
            
        elif tipo == "Dispersão":
            ax.scatter(df[coluna_1], df[coluna_2], color='red', alpha=0.5)
            ax.set_xlabel(coluna_1)
            ax.set_ylabel(coluna_2)

        ax.set_title(f'{tipo}: {coluna_1}', fontsize=10)
        fig.tight_layout()

        # Salva para o e-mail
        st.session_state['fig_churn'] = fig 
        
        # Exibição centralizada
        m_esq, centro, m_dir = st.columns([1, 2, 1]) 
        with centro:
            st.pyplot(fig)
        
        st.success(f"Gráfico de {tipo} gerado com sucesso!")
        
    except Exception as e:
        st.error(f"Não foi possível gerar este gráfico: {e}")
        st.info("Dica: Verifique se os dados da coluna selecionada são compatíveis com o tipo de gráfico (ex: colunas numéricas para Histograma/Boxplot).")
else:
    st.info("Por favor, selecione as opções acima para visualizar o gráfico.")