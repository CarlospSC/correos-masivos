from app.models import session, SentEmail, engine, Base

from datetime import datetime, timezone
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from pathlib import Path

from app.ses import ses_client

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from tqdm import tqdm


Base.metadata.create_all(engine)

# env = Environment(loader=FileSystemLoader("."))
# template = env.get_template("template_email.html")
# output_html = template.render()
# soup = BeautifulSoup(output_html, "html.parser")
# output_text = soup.get_text()

# EMAIL_SUBJECT = "Información pago duplicado de reembolso Corporación de Bienestar"
# EMAIL_FROM = "bewell Corredores de Seguros <info@somosbewell.cl>"
# EMAIL_REPLY_TO = "andrea.pinto@somosbewell.cl"
# ATTACHMENT_DIR = "./cartas"

# # Este DataFrame + unique_ruts soportan los adjuntos y filtros por RUT;
# # si se envía exactamente el mismo correo/adjunto a todos se puede
# # cambiar a una lista directa de correos y omitir el identificador.
# base_df = pd.read_excel("BASE CARTAS REVISADA AL 11 SEP 2025.xlsx")
# unique_ruts = base_df["Rut Asegurado"].drop_duplicates().tolist()


# def build_email(email, attachment_path):
#     msg = MIMEMultipart()
#     msg["Subject"] = EMAIL_SUBJECT
#     msg["From"] = EMAIL_FROM
#     msg["To"] = email
#     msg["Reply-To"] = EMAIL_REPLY_TO

#     alternative = MIMEMultipart("alternative")
#     alternative.attach(MIMEText(output_text, "plain", "utf-8"))
#     alternative.attach(MIMEText(output_html, "html", "utf-8"))
#     msg.attach(alternative)

#     # El adjunto depende del RUT (nombre {rut}_carta.pdf). Si se deja de
#     # personalizar por persona, se puede reemplazar por un archivo fijo
#     # o eliminar por completo este bloque.
#     with open(attachment_path, "rb") as f:
#         part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
#     part["Content-Disposition"] = (
#         f'attachment; filename="{os.path.basename(attachment_path)}"'
#     )
#     msg.attach(part)
#     return msg


# for rut in tqdm(unique_ruts, desc="Enviando email"):
#     try:
#         with session.begin():
#             existing = session.query(SentEmail).filter_by(rut=rut).first()
#             # Aquí se está filtrando netamente por rut

#             if existing is not None and str(existing.status) != "BOUNCED":
#                 print(f"Email ya enviado a rut {rut}, saltando...")
#                 continue
#             # Está la duda de la funcionalidad de este elif, revisar seguramente se agregó porque ya estaban
#             # los rut en la base de datos, debío haber quedado así para enviarle solo a los que rebotaron
#             elif existing is None:
#                 print(f"Email no enviado pero no encontrado en la base de datos el rut {rut}, saltando...")
#                 continue

#         # El adjunto individual se arma con el RUT; si el correo deja de
#         # personalizarse por destinatario, se puede apuntar a un único PDF.
#         filename = os.path.join(ATTACHMENT_DIR, f"{rut}_carta.pdf")

#         # Aquí se cruza la base original por RUT para recuperar el mail.
#         # Para un envío idéntico a todos se podría iterar directo por la
#         # columna MAIL y omitir este filtro por persona.
#         search_email = base_df[base_df["Rut Asegurado"] == rut]["MAIL"]
#         if len(search_email) == 0:
#             raise Exception("email not found")

#         email = search_email.iloc[0]

#         msg = build_email(email, filename)

#         response = ses_client.send_raw_email(
#             Source=msg["From"],
#             Destinations=[msg["To"]],
#             # Destinations=["csalinas@somosbewell.cl"],
#             RawMessage={"Data": msg.as_string()},
#         )
#         response_code = response["ResponseMetadata"]["HTTPStatusCode"]
#         if response_code != 200:
#             raise Exception(f"ResponseMetadata HTTPStatusCode: {response_code}")

#         with session.begin():
#             if existing is not None:
#                 existing.to = msg["To"]
#                 existing.status = "SENT"
#                 existing.message_id = response["MessageId"]
#                 existing.error = None
#                 existing.bounce_error = None
#                 existing.sent_at = datetime.now(timezone.utc)
#                 existing.received_at = None
#                 existing.opened_at = None
#             else:
#                 sent_email = SentEmail(
#                     rut=rut,
#                     to=msg["To"],
#                     status="SENT",
#                     message_id=response["MessageId"],
#                 )
#                 session.add(sent_email)
#     except Exception as e:
#         print(f"Error enviando email a rut {rut}: {e}")
#         with session.begin():
#             existing = session.query(SentEmail).filter_by(rut=rut).first()
#             if existing is not None:
#                 existing.status = "ERROR"
#                 existing.message_id = None
#                 existing.error = str(e)
#                 existing.bounce_error = None
#                 existing.updated_at = datetime.now(timezone.utc)
#             else:
#                 sent_email = SentEmail(rut=rut, to=None, status="ERROR", error=str(e))
#                 session.add(sent_email)


# ==========================
#  Flujo específico RRHH
# ==========================

# Ajusta estos valores para cada campaña RRHH antes de ejecutar send_rrhh_emails.
# RRHH_EMAIL_SUBJECT = "Asunto RRHH"
# RRHH_EMAIL_FROM = "Nombre Remitente <correo@example.com>"
# RRHH_EMAIL_REPLY_TO = "replyto@example.com"
RRHH_EMAIL_SUBJECT = "Comunicado Alex-IA"
RRHH_EMAIL_FROM = "bewell Corredores de Seguros <info@somosbewell.cl>"
RRHH_EMAIL_REPLY_TO = "info@somosbewell.cl"

RRHH_LIST_PATH = Path("rrhh_listado_correos_prueba.xlsx")
RRHH_IMAGE_PATH = Path("rrhh_email_image.jpg")


def load_rrhh_recipients(excel_path: Path) -> list[dict]:
    """Lee el Excel con columnas Nombre y Correo y devuelve una lista limpia."""
    if not excel_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo RRHH: {excel_path}")

    df = pd.read_excel(excel_path)
    expected = {"Nombre", "Correo"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"El Excel debe contener las columnas: {', '.join(expected)} (faltan {missing})")

    recipients = (
        df[["Nombre", "Correo"]]
        .dropna(subset=["Correo"])
        .drop_duplicates(subset=["Correo"])
        .to_dict("records")
    )
    return recipients


def build_rrhh_email_body(image_cid: str) -> str:
    """Genera el HTML del cuerpo, referenciando imágenes inline vía CID."""
    html_parts = [
        "<html>",
        "<body style='margin:0;padding:0;font-family:Arial, sans-serif;background-color:#ffffff;'>",
        "<div style='max-width:800px;margin:0 auto;background:#ffffff;padding:16px;'>",
    ]

    html_parts.append(
        "<div style='margin-bottom:16px;'>"
        f"<img src='cid:{image_cid}' alt='Comunicado RRHH' "
        "style='width:100%;height:auto;display:block;' />"
        "</div>"
    )

    html_parts.append("</div></body></html>")
    return "".join(html_parts)


def build_rrhh_plain_text() -> str:
    """Fallback mínimo cuando el cliente no soporta HTML/PDF embebido."""
    return (
        "Este correo contiene información importante para RRHH en formato gráfico. "
        "Por favor abre el correo en un cliente compatible para visualizarlo correctamente."
    )


def send_rrhh_emails(
    excel_path: Path = RRHH_LIST_PATH,
    image_path: Path = RRHH_IMAGE_PATH,
):
    """Envía el comunicado de RRHH usando la lista de nombre/correo indicada."""
    recipients = load_rrhh_recipients(excel_path)
    if not recipients:
        print("No se encontraron destinatarios RRHH.")
        return

    if not image_path.exists():
        raise FileNotFoundError(f"No se encontró la imagen RRHH: {image_path}")

    image_bytes = image_path.read_bytes()
    body_cid = "rrhh-body-image"

    html_body = build_rrhh_email_body(body_cid)
    plain_body = build_rrhh_plain_text()

    for recipient in tqdm(recipients, desc="Enviando RRHH"):
        email = recipient["Correo"]
        name = recipient.get("Nombre", "").strip()
        try:
            msg = MIMEMultipart("related")
            msg["Subject"] = RRHH_EMAIL_SUBJECT
            msg["From"] = RRHH_EMAIL_FROM
            msg["To"] = email
            msg["Reply-To"] = RRHH_EMAIL_REPLY_TO

            alternative = MIMEMultipart("alternative")
            personalized_html = html_body.replace("{{nombre}}", name or "Equipo RRHH")
            alternative.attach(MIMEText(plain_body, "plain", "utf-8"))
            alternative.attach(MIMEText(personalized_html, "html", "utf-8"))
            msg.attach(alternative)

            img_part = MIMEImage(image_bytes)
            img_part.add_header("Content-ID", f"<{body_cid}>")
            img_part.add_header("Content-Disposition", "inline", filename=image_path.name)
            msg.attach(img_part)

            response = ses_client.send_raw_email(
                Source=msg["From"],
                Destinations=[msg["To"]],
                RawMessage={"Data": msg.as_string()},
            )
            response_code = response["ResponseMetadata"]["HTTPStatusCode"]
            if response_code != 200:
                raise Exception(f"ResponseMetadata HTTPStatusCode: {response_code}")
        except Exception as exc:
            print(f"Error enviando email RRHH a {email}: {exc}")


# Para realizar una prueba manual descomenta la llamada siguiente.
if __name__ == "__main__":
    send_rrhh_emails()
