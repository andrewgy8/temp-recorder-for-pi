"""
1) Run `vcgencmd measure_temp`
2) Record output as json {temp: int, time_stamp: number[]}
3) tweet alert to user in config.txt
4) Run in time interaval set by config.txt

"""

import os
import time
import json
import config
import passwords
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class RecordTemp:

    def __init__(self, temp):
        self.temp = temp

    @staticmethod
    def execute_record_cmd():
        os.system("vcgencmd measure_temp")

    def get_temp(self):
        return str(self.temp)

    def format_output(self):
        output = dict()

        output['temp'] = self.get_temp()
        output['time_stamp'] = time.localtime()
        return json.dumps(output)

    def output_temp_into_file(self):
        f = open(config.output_file_name, "a+")
        f.write(self.format_output())
        f.write("\n")
        f.close()

    def engine(self):
        while True:
            self.get_temp()
            self.output_temp_into_file()
            time.sleep(config.time_interval)


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
        body = "Eva is the most beautiful girl in the world"

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

# record = RecordTemp(30)
# record.engine()


if __name__ == '__main__':
    email_alert = EmailAlerter()
    email_alert.engine()
