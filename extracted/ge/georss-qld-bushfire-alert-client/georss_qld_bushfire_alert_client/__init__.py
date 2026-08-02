"""Queensland Bushfire Alert Feed. Fetches GeoRSS feed from Queensland Bushfire Alert Feed."""

from .feed import QldBushfireAlertFeed  # noqa: F401
from .feed_entry import QldBushfireAlertFeedEntry  # noqa: F401
from .feed_manager import QldBushfireAlertFeedManager  # noqa: F401

VALID_CATEGORIES = [
    "Emergency Warning",
    "Watch and Act",
    "Advice",
    "Notification",
    "Information",
]
