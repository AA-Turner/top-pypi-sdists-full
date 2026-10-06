from device_detector.enums import AppType

from . import BaseClientParser


class FeedReader(BaseClientParser):
    __slots__ = ()
    APP_TYPE = AppType.FeedReader

    fixture_files = ('upstream/client/feed_readers.yml',)


__all__ = [
    'FeedReader',
]
