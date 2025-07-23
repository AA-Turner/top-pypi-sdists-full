# canonmap/services/db_mysql/helpers/datetime_formats.py

import dateutil.parser


DATETIME_TYPES = {"date", "datetime", "timestamp", "time", "year"}

def infer_date_format(samples):
    # Very basic inference, can be expanded
    # Try to use strftime format codes as sample
    formats = set()
    for val in samples:
        try:
            dt = dateutil.parser.parse(str(val))
            # Choose a format based on type
            if len(str(val)) == 4 and str(val).isdigit():
                fmt = "%Y"
            elif "-" in str(val):
                if ":" in str(val):
                    fmt = "%Y-%m-%d %H:%M:%S"
                else:
                    fmt = "%Y-%m-%d"
            else:
                fmt = "unknown"
            formats.add(fmt)
        except Exception:
            continue
    return list(formats) or ["unknown"]