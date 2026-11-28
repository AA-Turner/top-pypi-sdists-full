"""Every standard-library import hugpy-core uses. External packages are in module_imports."""
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, quote, unquote, urlencode, urlsplit

import argparse
import base64
import json
import os
import queue
import re
import secrets
import signal
import socket
import statistics
import sys
import threading
import time
import uuid

__all__ = ['SimpleCookie', 'argparse', 'base64', 'json', 'os', 'parse_qs', 'queue', 'quote', 're', 'secrets', 'signal',
           'socket', 'statistics', 'sys', 'threading', 'time', 'unquote', 'urlencode', 'urlsplit', 'uuid']
