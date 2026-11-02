"""`python -I -m probe.service.keeper`: the OS keeper's run (systemd, launchd, Task Scheduler, lifeboat.sh).
Kept for good (plan A1): those units and older lifeboats persist this module path."""

import sys

from probe.service.keeper.keeper import main

if __name__ == "__main__":
    sys.exit(main())
