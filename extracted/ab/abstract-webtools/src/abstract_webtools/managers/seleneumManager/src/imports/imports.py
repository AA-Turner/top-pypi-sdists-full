import os, time, re, json, logging, urllib3, requests,tempfile, shutil, socket, atexit, errno
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup          # if you prefer, keep using your parser
# selenium is lazy: importing this manager (and the package) no longer requires
# selenium to be installed; it loads on first webdriver/Options/By/… use.
from abstract_webtools._lazy import LazyModule as _LazyModule, LazyAttr as _LazyAttr
webdriver = _LazyModule("selenium.webdriver")
Options = _LazyAttr("selenium.webdriver.chrome.options", "Options")
By = _LazyAttr("selenium.webdriver.common.by", "By")
WebDriverWait = _LazyAttr("selenium.webdriver.support.ui", "WebDriverWait")
EC = _LazyModule("selenium.webdriver.support.expected_conditions")
from abstract_security import get_env_value
from abstract_utilities import *
from ....urlManager import *      
