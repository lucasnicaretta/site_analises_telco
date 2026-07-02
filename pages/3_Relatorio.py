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

#TEXTO PADRÃO DO RELATÓRIO
texto_padrao = """RELATÓRIO DE INSIGHTS ESTRATÉGICOS - BASE TELCO

A análise da base de clientes da empresa de telecomunicações evidencia que o índice de cancelamento é um dos principais desafios do negócio. Dos 7.043 clientes cadastrados, aproximadamente 26,5% encerraram seu relacionamento com a empresa. 

- Clientes com menor tempo de permanência tendem a apresentar maior risco de churn.
- Contratos mensais apresentam maior tendência ao cancelamento.
- Mensalidades elevadas sem percepção de valor aumentam a evasão.

Recomenda-se: programas de retenção direcionados, incentivo à migração para contratos de maior duração e revisão de políticas de preços.
"""

#1. DOWNLOAD 
st.subheader("1. Download")
st.download_button(
    label="📥 Baixar Relatório (Arquivo .txt)",
    data=texto_padrao,
    file_name="Relatorio_Insights_Telco.txt",
    mime="text/plain"
)

st.markdown("---")

# 2. CONFIGURAÇÃO DE E-MAIL 
st.subheader("Configuração do E-mail")
email_destinatario = st.text_input("Destinatário:")
assunto_email = st.text_input("Assunto:")
corpo_email_usuario = st.text_area("Corpo do e-mail:", value="", height=150)

# 3. O QUE DESEJA ENVIAR? ---
st.subheader("O que deseja enviar?")
col1, col2 = st.columns(2)
with col1:
    enviar_relatorio = st.checkbox("Relatório em Anexo (.txt)")
with col2:
    enviar_grafico = st.checkbox("Gráfico em Anexo (.png)")

# Botão de disparo
if st.button("Enviar E-mail", type="primary"):
    if not email_destinatario:
        st.error("Por favor, digite o e-mail do destinatário.")
    else:
        with st.spinner("Enviando e-mail..."):
            try:
                # Corpo padrão caso o usuário não escreva nada
                corpo_final = corpo_email_usuario if corpo_email_usuario else "Segue em anexo o relatório e/ou gráfico solicitado."
                
                txt_para_anexar = texto_padrao if enviar_relatorio else None
                fig = st.session_state.get('fig_churn') if enviar_grafico else None

                # Chamada da função
                enviar_email_seguro(
                    destinatario=email_destinatario, 
                    assunto=assunto_email, 
                    corpo=corpo_final, 
                    fig=fig, 
                    anexo_texto=txt_para_anexar, 
                    nome_anexo_texto="Relatorio_Insights.txt"
                )
                
                st.success(f"E-mail enviado com sucesso para {email_destinatario}!")
                
            except Exception as e:
                st.error(f"Erro ao enviar: {e}")