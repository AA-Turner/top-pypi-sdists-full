# Konverter timestamp fra UTC til Oslo tid. Men fjerner timezone info.
from __future__ import annotations
import logging
from datetime import datetime
from dateutil import tz

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

# set py4j logger to ERROR, otherwise logging.info will also print
# unnecessary callback messages from the server, like "Received command c on object id p0"
logging.getLogger("py4j").setLevel(logging.ERROR)
# similarily set pyspark logger to WARNING,
logging.getLogger("pyspark").setLevel(logging.WARNING)


def utc_to_oslo(timestmap):
    from_zone = tz.gettz("UTC")
    to_zone = tz.gettz("Europe/Oslo")

    timestmap = timestmap.replace(tzinfo=from_zone)
    timestmap = timestmap.astimezone(to_zone)

    return timestmap.replace(tzinfo=None)


# Nyttefunksjon som printer med timestamp.
# Kan også kalles med newline=False for å gi mulighet til senere å skrive mer til samme linje.
def logprint(text, newline=True):
    output = f"[{utc_to_oslo(datetime.now()):%Y-%m-%d %H:%M:%S}] {text}"

    if newline:
        print(output)
    else:
        sys.stdout.write(output)


lp = logprint


def bold_lp(msg):
    lp(f"\033[1m{msg}\033[0m")


def success_lp(msg):
    lp(f"\033[92m{msg}\033[0m")


def error_lp(msg):
    lp(f"\033[91m{msg}\033[0m")
