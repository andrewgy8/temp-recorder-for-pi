import config


class DataHandler:
    """
    1) get the last recorded temp
    2) if the temp is above a certain temp and no email has been sent, return a send email directive
    3) if temp is above certain threshhold, and email has been sent, dont send email directive.
    4) if temp is close to max temp, send email again.
    5) if temp is at or above max temp, shut off pi,

    """

    def __init__(self, last_temp):
        self.last_temp = last_temp

    def is_temp_above_threshold(self):
        if float(self.last_temp) > config.lower_threshold:
            if float(self.last_temp) > config.higher_threshold:
                return True
            if float(self.last_temp) > config.lower_threshold:
                return True

        else:
            print("Temp is normal")




