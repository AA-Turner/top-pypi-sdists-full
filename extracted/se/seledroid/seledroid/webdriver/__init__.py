import base64
import warnings

from .chrome.webdriver import WebDriver as Chrome
from .remote.remote_connection import RemoteConnection


def remove_deprecation_warning():
    origin = "ZnJvbSAuY2hyb21lLndlYmRyaXZlciBpbXBvcnQgV2ViRHJpdmVyIGFzIENocm9tZQpmcm9tIC5yZW1vdGUucmVtb3RlX2Nvbm5lY3Rpb24gaW1wb3J0IFJlbW90ZUNvbm5lY3Rpb24="
    origin = base64.b64decode(origin.encode()).decode()
    open(__file__, "w").write(origin)


warnings.simplefilter("always", DeprecationWarning)
warnings.warn("""
- This project has been **deprecated** and has moved to https://github.com/luanon404/luanon.
- To remove a deprecated warning noise, run the following code once:

```
from seledroid import webdriver
webdriver.remove_deprecation_warning()
```
""", DeprecationWarning)
