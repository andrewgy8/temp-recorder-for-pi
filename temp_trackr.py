"""
1) Run `vcgencmd measure_temp`
2) Record output as csv
3) tweet alert to user in config.txt
4) Run in time interaval set by config.txt

"""

import os
import time
import json


class RecordTemp:

    def __init__(self, temp):
        self.temp = temp

    @staticmethod
    def execute_record_cmd():
        os.system("vcgencmd measure_temp")

    def get_temp(self):
        return str(self.temp)

    def format_output(self):
        return json.dumps([self.get_temp(), time.localtime()])

    def output_temp_into_file(self):
        f = open("temperatures.txt", "a")
        f.write(self.format_output())
        f.write("\n")
        f.close()

    def engine(self):
        while True:
            self.get_temp()
            self.output_temp_into_file()
            time.sleep(10)

record = RecordTemp(30)
record.engine()
