import sys
import os
import streamlit as st

# Ajuste de caminho para importar o utils_email.py que está na raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils_email import enviar_email_seguro

st.set_page_config(page_title="Relatório", layout="centered")

# Verificação de segurança
if 'arquivo_dados' not in st.session_state:
    st.error("⚠️ Volte à Página Inicial e carregue o arquivo.")
    st.stop()

st.title("📄 Central de Relatório Estratégico")

# --- O TEXTO ESTÁ AQUI, MAS NÃO SERÁ EXIBIDO NA TELA ---
texto_relatorio = """
RELATÓRIO DE INSIGHTS ESTRATÉGICOS - BASE TELCO

A análise da base de clientes da empresa de telecomunicações evidencia que o índice de cancelamento é um dos principais desafios do negócio. Dos 7.043 clientes cadastrados, aproximadamente 26,5% encerraram seu relacionamento com a empresa, representando uma perda significativa tanto de receita quanto de oportunidades futuras de fidelização. Esse percentual indica que, embora a empresa possua uma carteira consolidada de clientes ativos, existe uma parcela expressiva que não permanece utilizando os serviços. Durante a exploração dos dados, observou-se que a base apresenta boa qualidade, sendo que a maior parte dos valores ausentes ocorre em colunas relacionadas ao cancelamento, como "Churn Reason" e "Churn Category". Esses campos permanecem vazios para clientes ativos, o que demonstra que a ausência dessas informações é esperada e não caracteriza um problema na coleta dos dados, porém pode analisar a causa raiz.

- Clientes com menor tempo de permanência tendem a apresentar maior risco de churn, indicando que os primeiros meses de relacionamento representam um período crítico para a retenção. Esse comportamento sugere a necessidade de estratégias voltadas ao acompanhamento de novos clientes, buscando garantir uma experiência positiva desde a contratação dos serviços.

Outro fator relevante está relacionado ao tipo de contrato. Clientes que utilizam contratos mensais apresentam maior tendência ao cancelamento quando comparados àqueles que possuem contratos anuais ou de longo prazo. Esse comportamento demonstra que contratos mais duradouros contribuem para aumentar a fidelização e reduzir a rotatividade da carteira.

A análise também evidencia que clientes que possuem mensalidades mais elevadas podem apresentar maior propensão ao cancelamento, principalmente quando essa cobrança não é acompanhada por uma percepção satisfatória da qualidade dos serviços prestados.

Níveis menores de satisfação normalmente estão associados a maiores índices de evasão, tornando esse indicador um importante sinal de alerta para a empresa.

Outro ponto importante é o valor do Customer Lifetime Value (CLTV), que representa o potencial financeiro de cada cliente ao longo do relacionamento com a empresa. Considerando que mais de 1.800 clientes cancelaram seus serviços, a perda financeira acumulada torna-se significativa, especialmente quando parte desses clientes possui alto valor de vida útil. Dessa forma, torna-se essencial identificar antecipadamente clientes estratégicos com maior risco de cancelamento para direcionar ações específicas de retenção.

Com base nos resultados obtidos, recomenda-se que a empresa desenvolva programas de retenção direcionados aos clientes com maior risco de churn, principalmente aqueles com pouco tempo de permanência, baixa satisfação e contratos mensais. Também é recomendável incentivar a migração para contratos de maior duração, revisar políticas de preços para clientes mais sensíveis ao valor das mensalidades, investir continuamente na qualidade do atendimento e utilizar modelos preditivos para identificar clientes com elevada probabilidade de cancelamento antes que a evasão ocorra.
"""

# --- BOTÕES (A ÚNICA INTERFACE DISPONÍVEL) ---

st.subheader("1. Download")
st.download_button(
    label="📥 Baixar Relatório (Arquivo .txt)",
    data=texto_relatorio,
    file_name="Relatorio_Insights_Telco.txt",
    mime="text/plain"
)

st.markdown("---")

st.subheader("2. Envio por E-mail")
email_destinatario = st.text_input("E-mail do Destinatário:")

incluir_grafico = st.checkbox("Incluir gráfico gerado no e-mail?", value=True)

if st.button("Enviar Relatório por E-mail", type="primary"):
    if not email_destinatario:
        st.error("Por favor, digite o e-mail do destinatário.")
    else:
        with st.spinner("Enviando..."):
            try:
                # Busca o gráfico se existir no session_state
                fig = st.session_state.get('fig_churn') if incluir_grafico else None
                
                # Chama a função de envio
                enviar_email_seguro(email_destinatario, "Relatório de Insights Telco", texto_relatorio, fig)
                
                st.success(f"Relatório enviado com sucesso para {email_destinatario}!")
            except Exception as e:
                st.error(f"Erro ao enviar: {e}")