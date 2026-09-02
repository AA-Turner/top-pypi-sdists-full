"""Module containing common data to be reused accross modules"""

from eumdac.__version__ import __title__, __documentation__, __version__

headers = {
    "referer": "EUMDAC.LIB",
    "User-Agent": str(__title__ + "/" + __version__),
}
