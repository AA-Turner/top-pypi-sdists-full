import json
import requests
from requests.auth import HTTPBasicAuth
from .user import userManager
from .episode import episodeManager
from .show import showManager
from .exceptions import *

class TVTimeWrapper:
  def __init__(self, username, password, headers=None):
    """
    This is the main instance with which you interact with the APIs. Specify `username` and `password`
    - Optional argument: `headers` , you can set custom HTTP headers
    """
    self.url = "https://api2.tozelabs.com/v2" # Base URL for API requests
    if not headers:
      self.h = {
        "User-Agent": "TVTime Wrapper"
      }
    else:
      self.h = headers
    self.session = requests.Session()
    self.session.headers.update(self.h)
    self.session.auth=HTTPBasicAuth(username,password)
    r = self.session.post(f"{self.url}/signin").json()
    if "result" in r and r['result'] == "KO":
      raise TVTimeLoginError(r['message'])
    else:
      self.userId = r['id']
      self.user = userManager(self)
      self.episode = episodeManager(self)
      self.show = showManager(self)
