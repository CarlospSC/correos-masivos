from app.models import session, SentEmail
from datetime import datetime, timezone
from tqdm import tqdm
from app.ses import sesv2_client


with session.begin():
    sent_emails = session.query(SentEmail).all()

    # Revisar si chequear solamente los que tengan estado bounced o sent (esperar unos 10 minutos desde la ejecución de envios_de_email)
    for sent_email in tqdm(sent_emails, desc="Actualizando estado de emails"):
        try:
            response = sesv2_client.get_message_insights(
                MessageId=sent_email.message_id
            )
            insights = response["Insights"]
            for insight in insights:
                events = insight["Events"]
                for event in events:
                    if sent_email.received_at is None and event["Type"] == "DELIVERY":
                        if sent_email.status == "SENT":
                            sent_email.status = "RECEIVED"
                        sent_email.received_at = event["Timestamp"]
                        sent_email.updated_at = datetime.now(timezone.utc)
                    if sent_email.opened_at is None and event["Type"] == "OPEN":
                        sent_email.status = "OPENED"
                        sent_email.opened_at = event["Timestamp"]
                        sent_email.updated_at = datetime.now(timezone.utc)
                    if event["Type"] == "BOUNCE":
                        sent_email.status = "BOUNCED"
                        sent_email.bounce_error = event["Details"]["Bounce"][
                            "DiagnosticCode"
                        ]
                        sent_email.updated_at = datetime.now(timezone.utc)
            sent_email.update_error = None
            sent_email.updated_at = datetime.now(timezone.utc)
        except Exception as e:
            print(f"Error actualizando email {sent_email.rut}: {e}")
            sent_email.update_error = str(e)
            sent_email.updated_at = datetime.now(timezone.utc)

# with session.begin():
#     bounced_emails = session.query(SentEmail).filter(
#         SentEmail.status == "BOUNCED"
#     ).all()

#     # Revisar si chequear solamente los que tengan estado bounced o sent (esperar unos 10 minutos desde la ejecución de envios_de_email)
#     for bounced_email in tqdm(bounced_emails, desc="Actualizando estado de emails"):
#         try:
#             response = sesv2_client.get_message_insights(
#                 MessageId=bounced_email.message_id
#             )
#             insights = response["Insights"]
#             for insight in insights:
#                 events = insight["Events"]
#                 for event in events:
#                     if bounced_email.bounce_error is None and event["Type"] == "BOUNCE":
#                         bounced_email.bounce_error = event["Details"]["Bounce"][
#                             "DiagnosticCode"
#                         ]
#                         bounced_email.updated_at = datetime.now(timezone.utc)
#             bounced_email.update_error = None
#             bounced_email.updated_at = datetime.now(timezone.utc)
#         except Exception as e:
#             print(f"Error actualizando email {bounced_email.rut}: {e}")
#             bounced_email.update_error = str(e)
#             bounced_email.updated_at = datetime.now(timezone.utc)