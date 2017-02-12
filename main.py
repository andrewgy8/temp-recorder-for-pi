from temp_trackr import *

if __name__ == '__main__':
    # email_alert = EmailAlerter()
    # email_alert.engine()
    RecordTemp(True, 30).engine()
    scan_file = FileScanner()
    scan_file.get_last_entry_in_file()
    scan_file.compare_current_and_previous_sent_times()
