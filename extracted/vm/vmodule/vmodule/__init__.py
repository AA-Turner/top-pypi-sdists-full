try:
    from .version import __version__
except ImportError:
    __version__ = "dev"

import logging
from typing import IO, Optional

LOG = logging.getLogger(__name__)

# My coding religion doesn't allow for import-time side effects that could break
# if imports are reordered.  These constants are _not_ injected into the
# `logging` module because of that.

VLOG_1 = logging.INFO - 1
VLOG_2 = logging.INFO - 2
VLOG_3 = logging.INFO - 3

# However, logging itself needs to know about them in order to reasonably format
# log messages.  This is idempotent, and shouldn't step too badly on other
# people's custom log levels.

logging.addLevelName(VLOG_1, "VLOG_1")
logging.addLevelName(VLOG_2, "VLOG_2")
logging.addLevelName(VLOG_3, "VLOG_3")

DEFAULT_FORMAT = "%(asctime)-15s %(levelname)-8s %(name)s:%(lineno)s %(message)s"
# TODO glog format too, or another compact format that includes thread id


def vmodule_init(
    v: Optional[int],
    vmodule: Optional[str],
    format: Optional[str] = None,
    stream: Optional[IO[str]] = None,
) -> None:
    if v is None:
        level = logging.WARNING
    elif v == 0:
        level = logging.INFO
    else:
        level = logging.INFO - v

    logging.basicConfig(level=level, format=format or DEFAULT_FORMAT, stream=stream)

    if vmodule:
        LOG.log(VLOG_1, "Parse vmodule: %r", vmodule)
        for item in vmodule.split(","):
            LOG.log(VLOG_2, "Item: %r", item)
            k, _, vv = item.partition("=")

            # N.b. getLogger takes no args other than the dotted name, and
            # logging.PlaceHolder is both not public and doesn't keep track of
            # the desired level.  This must work regardless of whether the
            # normal use has actually called getLogger yet, which is a big
            # reason why we don't have a custom Logger class.
            logging.getLogger(k).setLevel(logging.INFO - int(vv))


__all__ = [
    "vmodule_init",
    "VLOG_1",
    "VLOG_2",
    "VLOG_3",
]
