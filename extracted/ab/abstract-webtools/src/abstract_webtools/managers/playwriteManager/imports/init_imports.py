# playwright (and its browser binaries) is heavy and Android-hostile; keep it lazy
# so importing this manager doesn't require playwright. Loads on first call.
from abstract_webtools._lazy import LazyAttr as _LazyAttr
sync_playwright = _LazyAttr("playwright.sync_api", "sync_playwright")
