import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import plotly.io as pio

def enviar_email_seguro(destinatario, assunto, corpo, fig=None, anexo_texto=None, nome_anexo_texto="Relatorio.txt"):
    remetente = st.secrets["email_remetente"]
    senha = st.secrets["senha_app"]
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Criação da mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'plain', 'utf-8'))

    # Adiciona o gráfico
    if fig:
        # Usa pio.to_image para converter o gráfico em bytes
        img_bytes = pio.to_image(fig, format="png")
        parte_img = MIMEImage(img_bytes, name="grafico.png")
        msg.attach(parte_img)

    if anexo_texto:
        parte_txt = MIMEText(anexo_texto, 'plain', 'utf-8')
        parte_txt.add_header('Content-Disposition', f'attachment; filename="{nome_anexo_texto}"')
        msg.attach(parte_txt)

    # Envio via SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(remetente, senha)
    server.send_message(msg)
    server.quit()