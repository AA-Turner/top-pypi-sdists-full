"""
>>> mgr = Manager()
>>> all(map(len, mgr.get_host_ip_addresses()))
True
>>> all(map(len, mgr.get_host_mac_addresses()))
True
"""

import sys
import importlib


Manager = importlib.import_module(f'.{sys.platform}', __package__).Manager
