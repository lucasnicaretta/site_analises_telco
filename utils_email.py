import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def enviar_email_seguro(destinatario, assunto, corpo, fig=None, anexo_texto=None, nome_anexo_texto="Relatorio.txt"):
    # --- CONFIGURAÇÕES (Certifique-se de manter as suas aqui) ---
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remetente = "SEU_EMAIL@gmail.com" # Coloque seu e-mail
    senha = "SUA_SENHA_DE_APP"        # Coloque sua senha de app
    
    # Criação da mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto

    # Adiciona o corpo do e-mail
    msg.attach(MIMEText(corpo, 'plain', 'utf-8'))

    # Adiciona o gráfico (se existir)
    if fig:
        # Supondo que 'fig' seja uma figura do Plotly, converte para imagem
        img_bytes = fig.to_image(format="png")
        parte_img = MIMEImage(img_bytes, name="grafico.png")
        msg.attach(parte_img)

    # --- NOVO: Adiciona o relatório como anexo .txt (se existir) ---
    if anexo_texto:
        parte_txt = MIMEText(anexo_texto, 'plain', 'utf-8')
        parte_txt.add_header('Content-Disposition', f'attachment; filename="{nome_anexo_texto}"')
        msg.attach(parte_txt)

    # Envio
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(remetente, senha)
    server.send_message(msg)
    server.quit()