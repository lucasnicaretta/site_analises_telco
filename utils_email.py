import smtplib
import io
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def enviar_email_seguro(destinatario, assunto, corpo, fig=None):
    # Tenta pegar do secrets, se não existir, usa as variáveis abaixo
    try:
        remetente = st.secrets["email_remetente"]
        senha = st.secrets["senha_app"]
    except Exception:
        # COLOCA SEU E-MAIL E SENHA DE APP AQUI PARA TESTAR
        remetente = "SEU_EMAIL@gmail.com" 
        senha = "SUA_SENHA_DE_APP_AQUI"
    
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))
    
    if fig:
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        msg.attach(MIMEImage(buffer.read(), name="grafico.png"))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remetente, senha)
    server.sendmail(remetente, destinatario, msg.as_string())
    server.quit()