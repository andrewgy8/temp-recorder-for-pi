from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import passwords
import smtplib

import config


class EmailAlerter:

    def __init__(self):
        self.msg = MIMEMultipart()

    def engine(self):
        self.construct_header()
        self.construct_body()
        self.send()

    def construct_header(self):
        self.msg['From'] = config.from_addr
        self.msg['To'] = config.to_addr
        self.msg['Subject'] = "Damn straight skippy"

    def construct_body(self):
        body = "Your raspberry pi is at a critical temperature"

        self.msg.attach(MIMEText(body, 'plain'))

    def attachment(self):
        attachment = open(config.path_of_file, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % config.filename)
        self.msg.attach(part)

    def send(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(config.from_addr, passwords.your_password)
        text = self.msg.as_string()
        server.sendmail(config.from_addr, config.to_addr, text)
        server.quit()
