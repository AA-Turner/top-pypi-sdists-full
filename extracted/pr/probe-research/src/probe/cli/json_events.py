"""`probe wizard --json`'s events: moved to `probe.core.events` (Probe service, T1).

This name stays for every caller that imports it, and it is the SAME module
object, not a copy: a run started through either name is one run with one set
of globals, and a test that patches one patches both. The wire format did not
change.
"""

import sys

from probe.core import events as _events

sys.modules[__name__] = _events
