import six
import datetime

def is_string(value):
    return isinstance(value, six.string_types)

def is_datetime(value):
    return type(value) is datetime.datetime