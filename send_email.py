import smtplib, json
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

with open('./send_email/config.json', 'r') as f:
    config = json.load(f)

# Load credentials
sender_email = config['sender_email']
sender_pass = config['sender_pass']
receiver_email = config['receiver_email']

def construct_msg(sender_email : str, receiver_email: list):
    # Construct Email
    msg = MIMEMultipart()
    message_text = "Attached Image: "
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email)
    msg['Subject'] = "Test"
    msg.attach(MIMEText(message_text))

    with open('./send_email/screen_grab.png', 'rb') as f:
        img = f.read()

    msg.attach(MIMEImage(img))
    return msg.as_string()

def send_message(sender_email: str, sender_pass: str, receiver_email: list, message: str):
    # Send Email
    smtp = smtplib.SMTP(host="smtp.gmail.com", port=587) 
    smtp.starttls()
    smtp.login(sender_email, sender_pass)
    smtp.sendmail(sender_email, receiver_email, msg=message)
    smtp.close()


message = construct_msg(sender_email=sender_email, receiver_email=receiver_email)
send_message(sender_email=sender_email, sender_pass=sender_pass, receiver_email=receiver_email, message=message)
print("Message sent!")
