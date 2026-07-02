import smtplib
import streamlit as st
import io
import matplotlib.pyplot as plt
import plotly.io as pio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

def enviar_email_seguro(destinatario, assunto, corpo, fig=None, anexo_texto=None, nome_anexo_texto="Relatorio.txt"):
    try:
        remetente = st.secrets["email_remetente"]
        senha = st.secrets["senha_app"]
        
        # Criação da mensagem
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto

        # Corpo do e-mail
        msg.attach(MIMEText(corpo, 'plain', 'utf-8'))

        # 1. Processamento do Gráfico
        if fig:
            try:
                if isinstance(fig, plt.Figure):
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', bbox_inches='tight')
                    img_bytes = buf.getvalue()
                    buf.close()
                
                else:
                    img_bytes = pio.to_image(fig, format="png")
                
                parte_img = MIMEImage(img_bytes, name="grafico.png")
                msg.attach(parte_img)
            except Exception as e:
                st.warning(f"Não foi possível anexar o gráfico: {e}")

        #2 Processamento do Anexo 
        if anexo_texto:
            try:
                parte_txt = MIMEApplication(anexo_texto.encode('utf-8'), Name=nome_anexo_texto)
                parte_txt['Content-Disposition'] = f'attachment; filename="{nome_anexo_texto}"'
                msg.attach(parte_txt)
            except Exception as e:
                st.error(f"Erro ao anexar relatório: {e}")

        # 3. Envio via SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)
        server.quit()
        
        return True
        
    except Exception as e:
        st.error(f"Erro crítico no envio: {e}")
        return False