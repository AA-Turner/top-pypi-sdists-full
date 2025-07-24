"""
Functions to facilitate interactions with Optilogic platform using 'optilogic' library
"""

import os
import json
import logging
import time
from typing import Tuple
import optilogic


class OptilogicClient:
    """
    Wrapper for optilogic module for consumption in Cosmic Frog services
    """

    def __init__(self, username=None, appkey=None, logger=logging.getLogger()):
        # Detect if being run in Andromeda
        job_app_key = os.environ.get("OPTILOGIC_JOB_APPKEY")

        if appkey and not username:
            # Use supplied key
            self.api = optilogic.pioneer.Api(auth_legacy=False, appkey=appkey)
        elif appkey and username:
            # Use supplied key & name
            self.api = optilogic.pioneer.Api(auth_legacy=False, appkey=appkey, un=username)
        elif job_app_key:
            # Running on Andromeda
            self.api = optilogic.pioneer.Api(auth_legacy=False)
        else:
            raise ValueError("OptilogicClient could not authenticate")

        self.logger = logger

    def model_exists(self, model_name: str) -> bool:
        """
        Returns True if a given model exists, False otherwise
        """
        try:
            return self.api.storagename_database_exists(model_name)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.logger.error(f"Exception in cosmicfrog: {e}")
            return False

    def get_connection_string(self, model_name: str) -> Tuple[bool, str]:

        # TODO: There are two connection string fetch functions, see also frog_dbtools
        max_retries = int(os.getenv("CFLIB_DEFAULT_MAX_RETRIES", "3"))
        max_timeout = int(os.getenv("CFLIB_DEFAULT_RETRY_DELAY", "5"))

        request_attempts = 0

        for number_of_attempts in range(max_retries):

            try:
                self.logger.info('Getting connection string')
                rv = {"message": "error getting connection string"}
                if not self.api.storagename_database_exists(model_name):
                    return False, ""

                connection_info = self.api.sql_connection_info(model_name)

                if connection_info:
                    self.logger.info('connection information retrieved')

                return True, connection_info["connectionStrings"]["url"]

            except Exception as e:
                self.logger.error(f"Exception in cosmicfrog: {e}")
                self.logger.error(f"attempt {number_of_attempts} out of {max_retries}")
                request_attempts = number_of_attempts + 1
                time.sleep(max_timeout)

        if request_attempts >= max_retries:
            self.logger.error('Getting connection failed. Too many attempts')
            return False, ""

    def create_model_synchronous(self, model_name: str, model_template: str):
        try:
            new_model = self.api.database_create(name=model_name, template=model_template)

            status = "success"
            rv = {}
            if "crash" in new_model:
                status = "error"
                rv["message"] = json.loads(new_model["response_body"])["message"]
                rv["httpStatus"] = new_model["resp"].status_code
            else:
                while not self.api.storagename_database_exists(model_name):
                    self.logger.info(f"creating {model_name}")
                    time.sleep(3.0)
                connections = self.api.sql_connection_info(model_name)
                rv["model"] = new_model
                rv["connection"] = connections

            return status, rv

        except Exception as e:
            return "exception", e


    def delete_model_api(self, model_name: str) -> dict:
        """
        Delete a model from the platform

        Args:
            model_name (str): Name of the model to delete
        
        Returns:
            dict: Status of the operation
        """
        if not model_name:
            return {"status": "error", "message": "Model name is required"}

        try:
            response = self.api.storage_delete(name=model_name)
            if response.get('result', 'error') == 'error':
                    return {"status": "error", "message": response.get('message', '')}

            return {"status": "success", "message": f"Model {model_name} deleted successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
