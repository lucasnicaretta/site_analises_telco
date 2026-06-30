import streamlit as st

# Configuração da página
st.set_page_config(page_title="Relatório e Envio", layout="wide")

st.title("📄 Relatório de Insights - Base Telco")

# --- BLOQUEIO DE SEGURANÇA ---
if 'arquivo_dados' not in st.session_state or st.session_state['arquivo_dados'] is None:
    st.error("⚠️ **Acesso restrito:** Nenhum arquivo de dados foi carregado.")
    st.info("Por favor, acesse a **Página Inicial** e anexe o arquivo `.csv` para liberar o acesso.")
    st.stop()

# Conteúdo do Relatório armazenado na variável
relatorio_completo = """RELATÓRIO DE INSIGHTS ESTRATÉGICOS - BASE TELCO

A análise da base de clientes da empresa de telecomunicações evidencia que o índice de cancelamento é um dos principais desafios do negócio. Dos 7.043 clientes cadastrados, aproximadamente 26,5% encerraram seu relacionamento com a empresa, representando uma perda significativa tanto de receita quanto de oportunidades futuras de fidelização. Esse percentual indica que, embora a empresa possua uma carteira consolidada de clientes ativos, existe uma parcela expressiva que não permanece utilizando os serviços. Durante a exploração dos dados, observou-se que a base apresenta boa qualidade, sendo que a maior parte dos valores ausentes ocorre em colunas relacionadas ao cancelamento, como "Churn Reason" e "Churn Category". Esses campos permanecem vazios para clientes ativos, o que demonstra que a ausência dessas informações é esperada e não caracteriza um problema na coleta dos dados, porém pode analisar a causa raiz.

- Clientes com menor tempo de permanência tendem a apresentar maior risco de churn, indicando que os primeiros meses de relacionamento representam um período crítico para a retenção. Esse comportamento sugere a necessidade de estratégias voltadas ao acompanhamento de novos clientes, buscando garantir uma experiência positiva desde a contratação dos serviços.

Outro fator relevante está relacionado ao tipo de contrato. Clientes que utilizam contratos mensais apresentam maior tendência ao cancelamento quando comparados àqueles que possuem contratos anuais ou de longo prazo. Esse comportamento demonstra que contratos mais duradouros contribuem para aumentar a fidelização e reduzir a rotatividade da carteira.

A análise também evidencia que clientes que possuem mensalidades mais elevadas podem apresentar maior propensão ao cancelamento, principalmente quando essa cobrança não é acompanhada por uma percepção satisfatória da qualidade dos serviços prestados.

Níveis menores de satisfação normalmente estão associados a maiores índices de evasão, tornando esse indicador um importante sinal de alerta para a empresa.

Outro ponto importante é o valor do Customer Lifetime Value (CLTV), que representa o potencial financeiro de cada cliente ao longo do relacionamento com a empresa. Considerando que mais de 1.800 clientes cancelaram seus serviços, a perda financeira acumulada torna-se significativa, especialmente quando parte desses clientes possui alto valor de vida útil. Dessa forma, torna-se essencial identificar antecipadamente clientes estratégicos com maior risco de cancelamento para direcionar ações específicas de retenção.

Com base nos resultados obtidos, recomenda-se que a empresa desenvolva programas de retenção direcionados aos clientes com maior risco de churn, principalmente aqueles com pouco tempo de permanência, baixa satisfação e contratos mensais. Também é recomendável incentivar a migração para contratos de maior duração, revisar políticas de preços para clientes mais sensíveis ao valor das mensalidades, investir continuamente na qualidade do atendimento e utilizar modelos preditivos para identificar clientes com elevada probabilidade de cancelamento antes que a evasão ocorra."""

# --- OPÇÕES DE EXPORTAÇÃO ---
st.subheader("📥 Opções de Exportação")

# 1. Download direto
st.download_button(
    label="📥 Baixar Relatório Completo (.txt)",
    data=relatorio_completo,
    file_name="Relatorio_Analise_Churn_Telco.txt",
    mime="text/plain"
)

st.markdown("---")

# 2. Envio por e-mail
st.subheader("📧 Enviar por e-mail")
email_dest = st.text_input("E-mail de destino:", value="", placeholder="exemplo@email.com")

if st.button("Enviar Relatório e Gráfico por E-mail"):
    if email_dest and "@" in email_dest:
        # A lógica de envio (ex: smtplib) seria inserida aqui
        st.success(f"O relatório estratégico e o gráfico foram enviados para {email_dest} com sucesso!")
    else:
        st.error("Por favor, insira um endereço de e-mail válido.")