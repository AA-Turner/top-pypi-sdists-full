import sys

from seshat import app

rc = 1
try:
    app()
    rc = 0
except Exception as e:
    print("Error: %s" % e, file=sys.stderr)

sys.exit(rc)
