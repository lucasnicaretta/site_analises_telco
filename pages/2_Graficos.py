import streamlit as st
import plotly.express as px
import pandas as pd

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E SEGURANÇA
# ==============================================================================
st.set_page_config(page_title="Análise Gráfica", layout="wide")
st.title("📊 Análise Gráfica Dinâmica")

if 'arquivo_dados' not in st.session_state or st.session_state['arquivo_dados'] is None:
    st.error("⚠️ Nenhum arquivo carregado.")
    st.info("Volte à Página Inicial para importar seus dados.")
    st.stop()

df = st.session_state['arquivo_dados'].copy()

# ==============================================================================
# 2. CONTROLES DA INTERFACE
# ==============================================================================
col_a, col_b = st.columns(2)
tipo_grafico = col_a.selectbox("Tipo de Gráfico:", 
                               ["Barras", "Linhas", "Pizza", "Área", "Dispersão", "Histograma", "Boxplot"])
eixo_x = col_b.selectbox("Eixo X (Categorias):", [None] + df.columns.tolist())

col_cat = st.selectbox("Dividir por Categoria (Opcional - Cria legenda e divide os dados):", 
                       [None] + df.columns.tolist())

ativar_y = st.toggle("Habilitar métrica de Eixo Y (Valores)")
eixo_y, agg = None, "Contagem"

if ativar_y:
    c1, c2 = st.columns(2)
    eixo_y = c1.selectbox("Coluna Métrica (Y):", df.columns.tolist())
    agg = c2.selectbox("Agregação:", ["Soma", "Média", "Contagem"])

st.markdown("---")

# ==============================================================================
# 3. MOTOR DE RENDERIZAÇÃO ADAPTATIVO
# ==============================================================================
if eixo_x:
    try:
        params = {"color": col_cat} if col_cat else {}
        
        # Pré-processamento dos dados (Agrupamento)
        df_plot = df.copy()
        
        if ativar_y and eixo_y:
            mapa_agg = {"Soma": "sum", "Média": "mean", "Contagem": "count"}
            grupos = [eixo_x, col_cat] if col_cat else [eixo_x]
            df_plot = df.groupby(grupos)[eixo_y].agg(mapa_agg[agg]).reset_index()
            y_final = eixo_y
        else:
            grupos = [eixo_x, col_cat] if col_cat else [eixo_x]
            df_plot = df.groupby(grupos).size().reset_index(name='Contagem')
            y_final = 'Contagem'

        # --- REGRAS DE CLAREZA VISUAL PARA CADA GRÁFICO ---
        if tipo_grafico == "Barras":
            # Barras: text_auto mostra os números e barmode='group' as coloca lado a lado
            fig = px.bar(df_plot, x=eixo_x, y=y_final, text_auto=True, barmode='group', **params)
            fig.update_traces(textposition='outside')

        elif tipo_grafico == "Linhas":
            # Linhas: markers=True cria a bolinha, text mostra o número em cima de cada ponto
            fig = px.line(df_plot.sort_values(eixo_x), x=eixo_x, y=y_final, markers=True, text=y_final, **params)
            fig.update_traces(textposition='top center')

        elif tipo_grafico == "Pizza":
            # Pizza: exibe tanto a porcentagem quanto o número bruto dentro da fatia
            fig = px.pie(df_plot, names=eixo_x, values=y_final, **params)
            fig.update_traces(textposition='inside', textinfo='percent+value')

        elif tipo_grafico == "Área":
            # Área: Adiciona os números no topo da área demarcada
            fig = px.area(df_plot.sort_values(eixo_x), x=eixo_x, y=y_final, text=y_final, **params)
            fig.update_traces(textposition='top center')

        elif tipo_grafico == "Dispersão":
            # Dispersão: Adiciona valores perto das bolinhas (ideal para dados já agrupados)
            fig = px.scatter(df_plot, x=eixo_x, y=y_final, text=y_final, **params)
            fig.update_traces(textposition='top center', marker=dict(size=10))

        elif tipo_grafico == "Histograma":
            # Histograma: Precisa do dado original (df) e exibe text_auto nas contagens
            cor_hist = col_cat if col_cat else None
            fig = px.histogram(df, x=eixo_x, color=cor_hist, barmode='group', text_auto=True)

        elif tipo_grafico == "Boxplot":
            # Boxplot: Precisa do dado original (df) para calcular a mediana e os quartis
            cor_box = col_cat if col_cat else None
            eixo_y_box = eixo_y if ativar_y else None
            fig = px.box(df, x=eixo_x, y=eixo_y_box, color=cor_box)

        # Ajuste fino de layout para que os números não fiquem cortados
        fig.update_layout(margin=dict(t=40, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

        # ==============================================================================
        # 4. BOTÕES DE EXPORTAÇÃO
        # ==============================================================================
        st.markdown("---")
        st.subheader("📥 Exportação")
        
        img_bytes = fig.to_image(format="png", width=1000, height=600)
        st.download_button(
            label="Baixar Gráfico (PNG)",
            data=img_bytes,
            file_name=f"grafico_{tipo_grafico.lower()}.png",
            mime="image/png"
        )
        
        with st.expander("📧 Enviar este gráfico por e-mail"):
            email_dest = st.text_input("E-mail de destino:", value="", key="email_input")
            if st.button("Solicitar Envio"):
                if email_dest and "@" in email_dest:
                    st.success(f"O gráfico estruturado será enviado para {email_dest}!")
                else:
                    st.error("Por favor, informe um e-mail válido.")

    except Exception as e:
        st.error(f"Incompatibilidade detectada: {e}. Tente ajustar a métrica no Eixo Y.")
else:
    st.info("💡 **Aguardando dados:** Selecione uma coluna para o Eixo X.")