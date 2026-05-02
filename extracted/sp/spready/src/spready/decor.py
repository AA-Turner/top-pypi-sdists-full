from functools import wraps
import functools
from spready.config import getEnvURL

# from spready.config import EnvURLS
from .dto import SPRequest
from typing import List
import requests
import json
from loguru import logger


class sproute(object):
    def __init__(self, path, methods):
        self.path = path
        self.methods: List[str] = methods
        self.logger = logger

    def updateStatus(self, statusURL, res, headers):
        self.logger.info("Updating status")
        try:
            statusUpdate = requests.post(statusURL, headers=headers, json=res)
            if statusUpdate.status_code != 200:
                self.logger.warning(
                    f"Failed to update status: {statusUpdate.status_code}"
                )
            else:
                self.logger.debug(f"Updated status successfully!")
        except Exception as _e:
            self.logger.warning(f"Failed to update status: {_e}")

    def __call__(self, original_func):
        decorator_self = self

        def wrappee(*args, **kwargs):
            res = None
            if type(args[0]) == SPRequest:
                data = args[0]
                statusURL = f"{getEnvURL()}/status/{data.headers['x-spready-job-id']}"
                headers = {"x-auth-token": data.headers["X-Auth-Token"]}
                try:
                    if args[0].requestType not in self.methods:
                        self.logger.error(f"Method not allowed {args[0].requestType}")
                        raise ValueError("Method not allowed")
                    res = original_func(*args, **kwargs)

                    
                    self.logger.debug(f"Updating status")
                    self.updateStatus(statusURL, res, headers)
                except Exception as _e:
                    res = {"error": str(_e)}
                    self.logger.error(f"Error: {_e}")
                    self.logger.info(f"Updating status {statusURL}, {res}, {headers}")
                    self.updateStatus(statusURL, res, headers)
                    self.logger.info("Updated status...")
            return res

        return wrappee
