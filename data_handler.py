


class DataHandler:
    """
    1) get the last recorded temp
    2) if the temp is above a certain temp and no email has been sent, return a send email directive
    3) if temp is above certain threshhold, and email has been sent, dont send email directive.
    4) if temp is close to max temp, send email again.
    5) if temp is at or above max temp, shut off pi,

    """
