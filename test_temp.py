"""

"""

from temp_trackr import *
import json


def test_init_trakr():
    test_temp = 30
    cntl_temp = RecordTemp(test_temp).get_temp()

    assert cntl_temp == test_temp


def test_formatout_put():
    test_temp = 30
    controller = RecordTemp(test_temp)
    output_json = controller.format_output()

    output = json.loads(output_json)

    assert output['temp'] == str(test_temp)


def test_format_temp_stdout():
    temp_output = b"temp=38.6'C\n"

    temp = RecordTemp(temp_output).format_temp_std_out()
    assert temp == 38.6

