"""Validate VMODAL_API_KEY against the configured vmodal API."""
from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire
from vmodal import SyncClient


def run():
    client = SyncClient.from_env()
    print(client.auth())


def user_id():
    client = SyncClient.from_env()
    print(client.cfg.user_id)


if __name__ == '__main__':
    fire.Fire({"run": run, "user_id": user_id})
