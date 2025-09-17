import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
from openai import OpenAI

# 🔹 Diccionarios para traducir día y mes
dias = {
    "Monday": "lunes",
    "Tuesday": "martes",
    "Wednesday": "miércoles",
    "Thursday": "jueves",
    "Friday": "viernes",
    "Saturday": "sábado",
    "Sunday": "domingo"
}

meses = {
    "January": "enero",
    "February": "febrero",
    "March": "marzo",
    "April": "abril",
    "May": "mayo",
    "June": "junio",
    "July": "julio",
    "August": "agosto",
    "September": "septiembre",
    "October": "octubre",
    "November": "noviembre",
    "December": "diciembre"
}

# Fecha actual en español
now = datetime.now()
dia = dias[now.strftime("%A")]
mes = meses[now.strftime("%B")]
fecha_hoy = f"{dia} {now.day} de {mes} de {now.year}"

# Datos
remitente = "selfgeneratedcamilogonzalez@gmail.com"
destinatarios = ["pastoledorubilar@gmail.com"]

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# random phrase ai generated
respuesta = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Eres un generador de frases románticas, tiernas y motivadoras."},
        {"role": "user", "content": f"Escribe una frase bonita y romántica para mi pareja hoy ({fecha_hoy})."}
    ]
)

frase = respuesta.choices[0].message.content.strip()

# message
mensaje = MIMEMultipart("alternative")
mensaje["Subject"] = f"Un mensaje para ti ❤️ ({fecha_hoy})"
mensaje["From"] = remitente
mensaje["To"] = ", ".join(destinatarios)
mensaje["Cc"] = remitente  # copia al remitente

texto = f"Buenos días, regalonchita. Hoy es {fecha_hoy} 💌\n\n{frase}"
mensaje.attach(MIMEText(texto, "plain"))

# send and copy to myself
todos_destinatarios = destinatarios + [remitente]

# Contraseña y envío
password = os.getenv("GMAIL_APP_PASSWORD")
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(remitente, password)
    server.sendmail(remitente, todos_destinatarios, mensaje.as_string())

print("Correo enviado con éxito")


