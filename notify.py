from config import *
from log import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def check_matching_tags(postline):
    keywords = get_config('key_words_alert')
    if (keywords is None):
        return None
    
    matching = []
    for keyword in keywords:
        if (keyword.lower() in postline.victim.lower() or 
            keyword.lower() in postline.group.lower()):
            matching.append(keyword)
    
    if matching:
        print(f'Encontrado palavras chaves: {matching}')
        return matching        
    
    return None

def notify(notify_messages):
    if not notify_messages:
        return

    alert = get_config('alert')
    if (alert is None or not alert):
        return
    
    try:
        email_config = get_config('email')

        smtp_server = email_config['smtp_server']
        smtp_port = email_config['smtp_port']
        smtp_username = email_config['smtp_username']
        smtp_password = email_config['smtp_password']

        sender_email = email_config['from']
        receiver_email = email_config['to']
        receiver_bcc_email = email_config['to_bcc'] 

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = ', '.join(receiver_email)
        message["Bcc"] = ', '.join(receiver_bcc_email)
        message["Subject"] = email_config['subject']

        body = email_config['message_head'] + "\n\n"
        for post in notify_messages:
            body += post + " :\n"
        body += "\n" + email_config['message_foot']

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        log_event('-- --Email sent')
            
    except Exception as error:
        error_message = str(error)
        log_event(error_message)