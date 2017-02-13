from email_alerter import *
from temp_recorded import *
from file_scanner import *
import config


if __name__ == '__main__':
    """
    1) record temp, and time
    2) activate file scanner to check the temp
    3) email alert or not
    4) Repeat
    """
    # email_alert = EmailAlerter()
    # email_alert.engine()
    while True:
        if not config.Testing_Mode:
            temp_recorder = RecordTemp(30)
            temp_recorder.get_system_temp()
            temp_recorder.format_temp_std_out()
            temp_recorder.output_temp_into_file()
            scan_file = FileScanner()
            scan_file.get_last_entry_in_file()
            scan_file.compare_current_and_previous_sent_times()
            time.sleep(config.time_interval)

        else:
            temp_recorder = RecordTemp(50)
            temp_recorder.output_temp_into_file()
            scan_file = FileScanner()
            scan_file.get_last_entry_in_file()
            scan_file.compare_current_and_previous_sent_times()
            time.sleep(config.time_interval)