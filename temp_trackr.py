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


record = RecordTemp(30)
record.engine()


