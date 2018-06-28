from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

import datetime,smtplib


def MailMe(subject, from_email, to_emails, body):
    registry = getUtility(IRegistry)
    smtp_host = registry['plone.smtp_host']
    smtp_port = registry['plone.smtp_port']
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = ','.join(from_email)
    msg['To'] = ','.join(to_emails)

    mail = MIMEText(body, 'html')
    msg.attach(mail)

    s = smtplib.SMTP(smtp_host, smtp_port)
    s.sendmail(','.join(from_email), ','.join(to_emails), msg.as_string())
    s.quit()


