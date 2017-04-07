import datetime
import json
from email_alerter import *
from data_handler import *

class FileScanner:
    """
    1) scan file for last line
    2) extract data from last line
    3) compare last email sent date
    4) checkout data in data handler
    5) if data handler returns issue with temp and email has not been sent, send an email
    """
    def __init__(self):
        self.previous_entry = None
        self.last_email_time = None
        self.previous_check_time = None
        self.current_time = datetime.datetime.now()
        self.current_temp = None
        self.send_email_bool = None

    def get_last_entry_in_file(self):
        with open(config.path_of_file) as f:
            last_line = [i for i in f.read().split('\n') if i][-1]
            self.previous_entry = json.loads(last_line)
            self.previous_check_time = self.previous_entry["time_stamp"]
            self.last_email_time = self.previous_entry["last_email_sent_time"]
            self.current_temp = self.previous_entry["temp"]
        self.check_if_email_needs_to_be_sent()

    def check_if_email_needs_to_be_sent(self):
        self.send_email_bool = DataHandler(self.current_temp).is_temp_above_threshold()

    def compare_current_and_previous_sent_times(self):
        time_delta = datetime.datetime.now() - datetime.datetime.strptime(self.previous_check_time,
                                                                          "%Y-%m-%d %H:%M:%S.%f"
                                                                          )

        email_alert = EmailAlerter(self.current_temp)
        if time_delta > datetime.timedelta(minutes=10) and self.send_email_bool:
            # check to see
            # email_alert.engine()
            return True
        elif self.send_email_bool and self.last_email_time is None:
            # email_alert.engine()
            return True
        else:
            print('it has been less than 15 min')

    def send_email_directive(self):
        return True