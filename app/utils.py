# app/utils.py

from twilio.rest import Client
import os

def enviar_mensagem_whatsapp(numero_destino, mensagem):
    # Credenciais do Twilio (use variáveis de ambiente)
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_whatsapp_number = 'whatsapp:+14155238886'  # Número do Twilio

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=mensagem,
        from_=from_whatsapp_number,
        to=f'whatsapp:{numero_destino}'
    )

    return message.sid
