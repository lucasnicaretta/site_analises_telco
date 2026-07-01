import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils_email import enviar_email_seguro

st.set_page_config(page_title="Relatório", layout="centered")

# Verificação de segurança
if 'arquivo_dados' not in st.session_state:
    st.error("⚠️ Volte à Página Inicial e carregue o arquivo.")
    st.stop()

st.title("Central de Relatório Estratégico")

#TEXTO PADRÃO DO RELATÓRIO
texto_padrao = """RELATÓRIO DE INSIGHTS ESTRATÉGICOS - BASE TELCO

A análise da base de clientes da empresa de telecomunicações evidencia que o índice de cancelamento é um dos principais desafios do negócio. Dos 7.043 clientes cadastrados, aproximadamente 26,5% encerraram seu relacionamento com a empresa, representando uma perda significativa tanto de receita quanto de oportunidades futuras de fidelização. Esse percentual indica que, embora a empresa possua uma carteira consolidada de clientes ativos, existe uma parcela expressiva que não permanece utilizando os serviços. Durante a exploração dos dados, observou-se que a base apresenta boa qualidade, sendo que a maior parte dos valores ausentes ocorre em colunas relacionadas ao cancelamento, como "Churn Reason" e "Churn Category". Esses campos permanecem vazios para clientes ativos, o que demonstra que a ausência dessas informações é esperada e não caracteriza um problema na coleta dos dados, porém pode analisar a causa raiz.

- Clientes com menor tempo de permanência tendem a apresentar maior risco de churn, indicando que os primeiros meses de relacionamento representam um período crítico para a retenção. Esse comportamento sugere a necessidade de estratégias voltadas ao acompanhamento de novos clientes, buscando garantir uma experiência positiva desde a contratação dos serviços.

Outro fator relevante está relacionado ao tipo de contrato. Clientes que utilizam contratos mensais apresentam maior tendência ao cancelamento quando comparados àqueles que possuem contratos anuais ou de longo prazo. Esse comportamento demonstra que contratos mais duradouros contribuem para aumentar a fidelização e reduzir a rotatividade da carteira.

A análise também evidencia que clientes que possuem mensalidades mais elevadas podem apresentar maior propensão ao cancelamento, principalmente quando essa cobrança não é acompanhada por uma percepção satisfatória da qualidade dos serviços prestados.

Níveis menores de satisfação normalmente estão associados a maiores índices de evasão, tornando esse indicador um importante sinal de alerta para a empresa.

Outro ponto importante é o valor do Customer Lifetime Value (CLTV), que representa o potencial financeiro de cada cliente ao longo do relacionamento com a empresa. Considerando que mais de 1.800 clientes cancelaram seus serviços, a perda financeira acumulada torna-se significativa, especialmente quando parte desses clientes possui alto valor de vida útil. Dessa forma, torna-se essencial identificar antecipadamente clientes estratégicos com maior risco de cancelamento para direcionar ações específicas de retenção.

Com base nos resultados obtidos, recomenda-se que a empresa desenvolva programas de retenção direcionados aos clientes com maior risco de churn, principalmente aqueles com pouco tempo de permanência, baixa satisfação e contratos mensais. Também é recomendável incentivar a migração para contratos de maior duração, revisar políticas de preços para clientes mais sensíveis ao valor das mensalidades, investir continuamente na qualidade do atendimento e utilizar modelos preditivos para identificar clientes com elevada probabilidade de cancelamento antes que a evasão ocorra.
"""

# --- 1. DOWNLOAD ---
st.subheader("Baixar Relatório")
st.download_button(
    label="Baixar Relatório (Arquivo .txt)",
    data=texto_padrao,
    file_name="Relatorio_Insights_Telco.txt",
    mime="text/plain"
)

st.markdown("---")

#2. CONFIGURAÇÃO DE E-MAIL 
st.subheader("Configuração do E-mail")
email_destinatario = st.text_input("Destinatário:")
assunto_email = st.text_input("Assunto:")
corpo_email_usuario = st.text_area("Corpo do e-mail:", value="", height=200)

#3. O QUE DESEJA ENVIAR? ---
st.subheader("O que deseja enviar?")
enviar_relatorio = st.checkbox("Relatório Junto")
enviar_grafico = st.checkbox("Salvar Gráfico")

# Botão de disparo com rótulo "Enviar E-mail"
if st.button("Enviar o E-mail", type="primary"):
    if not email_destinatario:
        st.error("Por favor, digite o e-mail do destinatário.")
    else:
        with st.spinner("Enviando..."):
            try:
                mensagem_usuario = corpo_email_usuario if corpo_email_usuario else ""
                
                if enviar_relatorio:
                    if mensagem_usuario:
                        conteudo_final = f"{mensagem_usuario}\n\n---\n\n{texto_padrao}"
                    else:
                        conteudo_final = texto_padrao
                else:
                    conteudo_final = mensagem_usuario

                if not conteudo_final.strip() and not enviar_grafico:
                    st.warning("O e-mail está vazio! Digite algo ou marque uma das opções de envio.")
                else:
                    fig = st.session_state.get('fig_churn') if enviar_grafico else None
                    
                    enviar_email_seguro(email_destinatario, assunto_email, conteudo_final, fig)
                    
                    st.success(f"E-mail enviado com sucesso para {email_destinatario}!")
            except Exception as e:
                st.error(f"Erro ao enviar: {e}")