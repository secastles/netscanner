import smtplib
import logging
from email.mime.text import MIMEText

import settings as s

logger = logging.getLogger(__name__)

def send_notifications(subject, payload):
    """" Email notifications currently only work with gmail """
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        logger.info("Emailing notfication: starting TLS session.")
        smtpObj.starttls()  # expect 220
    except (smtplib.SMTPHeloError, smtplib.SMTPNotSupportedError, RuntimeError) as err:
        logger.error("Error creating TLS mode for SMTP. Returned error: {}".format(err))
    try:
        logger.info("Logging into email account.")
        smtpObj.login(s.EMAIL_ADDR, s.EMAIL_PASS)  # expect 235
    except (smtplib.SMTPHeloError, smtplib.SMTPAuthenticationError, smtplib.SMTPNotSupportedError, smtplib.SMTPException) as err:
        logger.error("SMTP login error. Returned error: {}".format(err))
    try:
        logger.info("Sending mail.")
        msg = MIMEText(payload)
        msg['Subject'] = subject
        msg['From'] = s.EMAIL_ADDR
        msg['To'] = s.NOTIFY_EMAIL
        smtpObj.sendmail(s.EMAIL_ADDR, s.NOTIFY_EMAIL, msg.as_string())  # expect empty dictionary
    except (smtplib.SMTPHeloError, smtplib.SMTPRecipientsRefused, smtplib.SMTPNotSupportedError, smtplib.SMTPSenderRefused, smtplib.SMTPDataError) as err:
        logger.error("SMTP send error. Returned error: {}".format(err))
    smtpObj.quit()
