from typing import Optional, List
import requests
from ....sslManager import SSLManager
from ....cipherManager import CipherManager
from ....tlsAdapter import TLSAdapter
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
