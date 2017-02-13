"""
1) Run `vcgencmd measure_temp`
2) Record output as json {temp: int, time_stamp: number[]}
3) tweet alert to user in config.txt
4) Run in time interaval set by config.txt

Data: {record_time: DateTime, temp: str, email_sent: bool, last_email_sent_time: DateTime}

"""

import time
import datetime
import json
import config
import subprocess


class RecordTemp:

    def __init__(self, temp=None, ):
        self.temp = temp

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

        output['temp'] = str(self.get_temp())
        output['time_stamp'] = str(datetime.datetime.now())
        output['last_email_sent_time'] = None
        return json.dumps(output)

    def output_temp_into_file(self):
        f = open(config.output_file_name, "a+")
        f.write(self.format_output())
        f.write("\n")
        f.close()

    # def engine(self):
    #     if not self.testing:
    #         while True:
    #             self.get_system_temp()
    #             self.format_temp_std_out()
    #             self.output_temp_into_file()
    #             time.sleep(config.time_interval)
    #     else:
    #         self.output_temp_into_file()


class CommandCenter:
    """
    shutdown:
    from subprocess import call
    call("sudo nohup shutdown -h now", shell=True)
    """