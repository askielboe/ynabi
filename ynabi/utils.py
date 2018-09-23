import datetime


def string_to_datetime(date_string, date_format):
    return datetime.datetime.strptime(date_string, date_format)
