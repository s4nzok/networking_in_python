import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
# this is where we start the whole process.

with open('password.txt', 'r') as f:
    password = f.read()

server.login('bhaiadhikari1111@gmail.com', password)
# upto here, it is the login process.

msg = MIMEMultipart()
msg['From'] = 'Bhai'
msg['To'] = 'sanjogbhandari3333@gmai.com'
msg['Subject'] = 'Just a Text'

with open('msg.txt', 'r') as f:
    message = f.read().strip()

msg.attach(MIMEText(message, 'plain'))

filename = 'src.png'
attachment = open(filename, 'rb')
# rb: read in byte mode.

p = MIMEBase('application', 'octet-stream')
p.set_payload(attachment.read())
attachment.close()

encoders.encode_base64(p)
p.add_header('Content-Disposition', f'attachment; filename="{filename}"')
msg.attach(p)

text = msg.as_string()

server.sendmail('bhaiadhikari1111@gmail.com', 'sanjogbhandari3333@gmail.com', text)
server.quit()