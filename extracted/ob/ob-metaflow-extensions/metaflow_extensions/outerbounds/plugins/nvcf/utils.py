import sys


def warning_message(message, prefix="[@nvidia]"):
    msg = "%s %s" % (prefix, message)
    print(msg, file=sys.stderr)
