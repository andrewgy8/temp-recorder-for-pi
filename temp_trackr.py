"""
1) Run `vcgencmd measure_temp`
2) Record output as json {temp: int, time_stamp: number[]}
3) tweet alert to user in config.txt
4) Run in time interaval set by config.txt

Data: {time: DateTime, temp: str, email_sent: bool}

"""

import os
import time
import datetime
import json
import config
import passwords
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class RecordTemp:

    def __init__(self, testing, temp=None, ):
        self.temp = temp
        self.testing = testing

    def get_system_temp(self):
        p = subprocess.Popen(["vcgencmd", "measure_temp"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        self.temp, err = p.communicate()

    def format_temp_std_out(self):
        # "b\"temp=38.6'C\\n\""
        self.temp = str(self.temp)
        self.temp = format(self.temp.replace("b\"temp=", "").replace("'C\\n", "").replace('"', ""))
        return float(self.temp)

    def get_temp(self):
        return self.temp



    def format_output(self):
        output = dict()
        date_handler = lambda obj: (
            obj.isoformat()
            if isinstance(obj, datetime.datetime)
               or isinstance(obj, datetime.date)
            else None
        )
        output['temp'] = str(self.get_temp())
        output['time_stamp'] = str(datetime.datetime.now())
        return json.dumps(output)

    def output_temp_into_file(self):
        f = open(config.output_file_name, "a+")
        f.write(self.format_output())
        f.write("\n")
        f.close()

    def engine(self):
        if not self.testing:
            while True:
                self.get_system_temp()
                self.format_temp_std_out()
                self.output_temp_into_file()
                time.sleep(config.time_interval)
        else:
            self.output_temp_into_file()


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


class FileScanner:

    def __init__(self):
        self.previous_entry = None
        self.last_email_time = None
        self.previous_check_time = None
        self.current_time = datetime.datetime.now()

    def get_last_entry_in_file(self):
        with open(config.path_of_file) as f:
            last_line = [i for i in f.read().split('\n') if i][-1]
            self.previous_entry = json.loads(last_line)
            self.previous_check_time = self.previous_entry["time_stamp"]

    def compare_current_and_previous_sent_times(self):
        time_delta = datetime.datetime.now() - datetime.datetime.strptime(self.previous_check_time, "%Y-%m-%d %H:%M:%S.%f")
        print(time_delta)
        # if  != self.current_time:
        #
        # else:

