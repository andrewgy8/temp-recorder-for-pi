import json
import unittest

from src.temp_recorded import *


class TestTempRecorder(unittest.TestCase):

    def test_init_trakr(self):
        test_temp = 30
        cntl_temp = RecordTemp(test_temp).get_temp()

        self.assertEqual(cntl_temp, test_temp)


    def test_formatout_put(self):
        test_temp = 30
        controller = RecordTemp(test_temp)
        output_json = controller.format_output()

        output = json.loads(output_json)

        self.assertEqual(output['temp'], str(test_temp))


    def test_format_temp_stdout(self):
        temp_output = b"temp=38.6'C\n"

        temp = RecordTemp(temp_output).format_temp_std_out()
        self.assertEqual(temp, 38.6)

