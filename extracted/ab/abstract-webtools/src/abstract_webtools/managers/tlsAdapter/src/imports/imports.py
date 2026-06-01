# tls_adapter.py
from typing import Optional, Sequence, Union, Tuple
import ssl
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager, ProxyManager
# If SSLManager is in the same package:
from ....sslManager import SSLManager  # <-- adjust if needed
