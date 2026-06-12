import logging
from ..urlManager import (
    urlManager,
    get_url,
    get_url_mgr
    )
from ..requestManager import (
    requestManager,
    get_source,
    get_req_mgr
    )
from ..soupManager import (
    soupManager,
    get_soup,
    get_soup_mgr
    )
from bs4 import BeautifulSoup
logging.basicConfig(level=logging.INFO)
