"""
    Utility functions for Cosmic Frog
"""

import os
import time
import uuid
from typing import Tuple
from random import randint
from httpx import Client
from .frog_log import get_logger

# Note: Geocoding is via PROD service unless overidden
HYPNOTOAD_URL = (
    os.getenv("HYPNOTOAD_URL") or "https://api.cosmicfrog.optilogic.app/hypnotoad/cosmicfrog/v0.2"
).strip("/")

class FrogUtils:
    """
    Container class for Cosmic Frog utilities
    """

    @staticmethod
    def geocode_table(
        model_name: str,
        table_name: str,
        app_key: str,
        geoprovider: str = "MapBox",
        geoapikey: str = None,
        ignore_low_confidence: bool = True,
        fire_and_forget: bool = True,
        correlation_id: str = None,
    ):
        """
        Wrapper function for geocoding an Cosmic Frog table (in place)
        """
        log = get_logger()
        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        if not app_key:
            log.error("%s Must supply a valid OL app key", correlation_id)
            return {"status": "error", "message": "Must supply a valid OL app key"}

        table_name = table_name.lower().strip()
        if not FrogUtils.___check_if_valid_table_name__(table_name):
            log.error("%s Must supply a valid table name", correlation_id)
            return {"status": "error", "message": "Must supply a valid table name: Customers, Suppliers, Facilities"}


        headers = {"X-App-Key": app_key}

        params = {
            "model_name": model_name,
            "table_name": table_name,
            "geoprovider": geoprovider,
            "ignore_low_confidence": ignore_low_confidence,
        }

        if geoapikey:
            params["geoapikey"] = geoapikey

        log.info("%s Geocoding table %s in model %s", correlation_id, table_name, model_name)

        with Client() as client:
            try:
                response = client.post(
                    f"{HYPNOTOAD_URL}/geocoding/geocode/table",
                    headers=headers,
                    params=params,
                )

                log.info("%s Geocoding response: %s", correlation_id, response.json())

                response.raise_for_status()

                if fire_and_forget:
                    return {
                        "status": "success",
                        "message": "Geocoding will run in the background. To track the status, use the fire_and_forget=False option."
                    }

                return FrogUtils.__await_geocoding_to_finish__(model_name, table_name, app_key, correlation_id)

            except Exception as e:
                if response.status_code == 409:
                    # when 409 is returned, the geocoding operation is already running, so lets just go with the logic for waiting if fire_and_forget is False
                    log.info("%s Geocoding operation already running, if you want to track the status, use the fire_and_forget=False option.", correlation_id)
                    if not fire_and_forget:
                        return FrogUtils.__await_geocoding_to_finish__(model_name, table_name, app_key, correlation_id)

                else:
                    log.error("%s Geocoding failed: %s", correlation_id, e)
                    return {"status": "error", "message": str(e)}


    @staticmethod
    def __await_geocoding_to_finish__(model_name: str, table_name: str, app_key: str, correlation_id: str):
        """
        Wrapper function to wait for geocoding to finish
        """
        try:
            log = get_logger()

            if not correlation_id:
                correlation_id = str(uuid.uuid4())

            if not app_key:
                log.error("%s Must supply a valid OL app key", correlation_id)
                return {"status": "error", "message": "Must supply a valid OL app key"}

            if not model_name:
                log.error("%s Must supply a valid model name", correlation_id)
                return {"status": "error", "message": "Must supply a valid model name"}

            table_name = table_name.lower().strip()
            if not FrogUtils.___check_if_valid_table_name__(table_name):
                log.error("%s Must supply a valid table name", correlation_id)
                return {"status": "error", "message": "Must supply a valid table name: Customers, Suppliers, Facilities"}


            log.info("%s Waiting for geocoding to finish...", correlation_id)
            is_running = True
            start_time: float = time.time()

            while is_running:
                delta: float = time.time() - start_time
                min_time, max_time = FrogUtils.__calulate_geocode_sleep_time__(delta)
                wait: int = randint(min_time, max_time)
                time.sleep(wait)

                log.info("%s Checking geocoding status...", correlation_id)

                response = FrogUtils.check_geocoding_status(model_name, table_name, app_key)
                is_running = response["status"]
                if is_running:
                    log.info("%s Geocoding still running... Will check again...", correlation_id)


            log.info("%s Geocoding finished", correlation_id)
            return {"status": "success", "message": "Geocoding finished"}
        except Exception as e:
            log.error("%s Geocoding failed: %s", correlation_id, e)
            return {"status": "error", "message": str(e)}


    @staticmethod
    def ___check_if_valid_table_name__(table_name: str) -> bool:
        """
        Check if the table name is valid
        """

        return table_name.lower().strip() in ["customers", "facilities", "suppliers"]


    @staticmethod
    def __calulate_geocode_sleep_time__(secs: float) -> Tuple[int, int]:
        if secs < 30:
            return 2, 5
        elif secs < 60:
            return 3, 7
        elif secs < 180:
            return 5, 15
        elif secs < 300:
            return 10, 20
        elif secs < 600:
            return 20, 30
        else:
            return 20, 35


    @staticmethod
    def check_geocoding_status(
        model_name: str,
        table_name: str,
        app_key: str,
    ):
        """
        Wrapper function to check the status of a geocoding operation
        """
        try:
            if not app_key:
                return {"status": "error", "message": "Must supply a valid OL app key"}

            if not model_name:
                return {"status": "error", "message": "Must supply a valid model name"}

            table_name = table_name.lower().strip()
            if not FrogUtils.___check_if_valid_table_name__(table_name):
                return {"status": "error", "message": "Must supply a valid table name: Customers, Suppliers, Facilities"}

            headers = {"X-App-Key": app_key}

            params = {
                "model_name": model_name,
                "table_name": table_name,
            }

            with Client(timeout=30.0) as client:
                response = client.get(
                    f"{HYPNOTOAD_URL}/geocoding/geocode/table/status",
                    headers=headers,
                    params=params,
                )

                response.raise_for_status()

            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
