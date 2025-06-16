import sys
import time
import requests
import sqlite3
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from typing import Dict, Optional, Any
from .utils import get_ngc_response, get_storage_path


def nvcf_submit_helper(
    url: str,
    payload: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
    max_retries: int = 300,
    backoff_factor: float = 0.3,
    request_delay: float = 1.1,
    log_callback: Optional[callable] = None,
) -> Dict[str, Any]:
    def _log_error(start_time: float, status_code: int, poll_count: int):
        if log_callback:
            end_time = time.time()
            try:
                log_callback({}, end_time - start_time, status_code, poll_count)
            except Exception as log_error:
                print(f"Warning: Logging callback failed: {log_error}")

    # use default headers
    if not headers:
        headers = {"accept": "application/json", "content-type": "application/json"}
        print(f"Using Default Headers: {headers}")

    # Configure session with retry strategy
    session = requests.Session()
    status_forcelist = [429, 500, 502, 503, 504, 404]
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=["GET", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Add artificial delay if specified
    time.sleep(request_delay)

    start_time = time.time()
    poll_count = 0
    status_code = 0
    response_data = {}

    try:
        # Make initial request
        response = session.post(url, json=payload, headers=headers, timeout=timeout)
        time.sleep(request_delay)

        # Handle initial response
        response.raise_for_status()
        request_id = response.headers.get("NVCF-REQID")
        polling_url = f"https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/{request_id}"

        print(f"Polling NVCF Request ID: {request_id}")

        # Initial response status
        status_code = response.status_code
        print(f"Initial response status: {status_code}")

        # Create a variable to store the final response
        final_response = response

        # Continue polling while we get 202 (Accepted/Processing)
        while status_code == 202:
            poll_count += 1
            print(f"Polling attempt #{poll_count} to {polling_url}")

            # Wait before next poll
            time.sleep(request_delay)

            # Make a new poll request
            poll_response = session.get(polling_url, headers=headers, timeout=timeout)
            status_code = poll_response.status_code
            print(f"Poll #{poll_count} status: {status_code}")

            # Check for errors
            try:
                poll_response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"Poll request failed: {str(e)}")
                poll_response.close()
                # Log the error before re-raising
                _log_error(start_time, poll_response.status_code, poll_count)
                raise

            # If status is 200, the job is complete
            if status_code == 200:
                print("Polling complete - job finished successfully")
                # Update our final response to be this poll response
                final_response = poll_response
                break

            # Close this poll response if we're going to loop again
            if status_code == 202:
                poll_response.close()

        # If we exited the loop without a 200 status, something went wrong
        if status_code != 200:
            print(f"Polling ended with unexpected status: {status_code}")
            # Log the error before raising
            _log_error(start_time, status_code, poll_count)
            raise Exception(f"Unexpected status code after polling: {status_code}")

        # Get the response data for logging
        response_data = final_response.json()

    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (4xx, 5xx status codes)
        status_code = e.response.status_code if e.response else 0
        print(f"HTTP Error: {str(e)}", file=sys.stderr)
        # Log the error
        _log_error(start_time, status_code, poll_count)
        raise

    except Exception as e:
        # Handle other errors (connection errors, timeouts, etc.)
        print(f"Request Error: {str(e)}", file=sys.stderr)
        # Log the error with status_code 0 to indicate non-HTTP error
        _log_error(start_time, 0, poll_count)
        raise

    # Calculate final duration and log successful requests
    end_time = time.time()
    duration = end_time - start_time

    # Call the logging callback if provided
    if log_callback:
        try:
            log_callback(response_data, duration, status_code, poll_count)
        except Exception as e:
            print(f"Warning: Logging callback failed: {e}")

    # Log metrics
    print(
        f"Request completed: duration={duration:.2f}s, polls={poll_count}, "
        f"status={status_code}, size={len(final_response.content)} bytes"
    )

    return response_data


class NimMetadata(object):
    def __init__(self):
        self._nvcf_chat_completion_models = []
        ngc_response = get_ngc_response()

        self.ngc_api_key = ngc_response["nvcf"]["api_key"]

        for model in ngc_response["nvcf"]["functions"]:
            self._nvcf_chat_completion_models.append(
                {
                    "name": model["model_key"],
                    "function-id": model["id"],
                    "version-id": model["version"],
                }
            )

    def get_nvcf_chat_completion_models(self):
        return self._nvcf_chat_completion_models

    def get_headers_for_nvcf_request(self):
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.ngc_api_key}",
            "NVCF-POLL-SECONDS": "5",
        }


class NimManager(object):
    def __init__(self, models, flow, step_name, monitor):
        nim_metadata = NimMetadata()
        nvcf_models = [
            m["name"] for m in nim_metadata.get_nvcf_chat_completion_models()
        ]
        self.models = {}

        # Convert models to a standard format
        standardized_models = []
        # If models is a single string, convert it to a list with a dict
        if isinstance(models, str):
            standardized_models = [{"name": models}]
        # If models is a list, process each item
        elif isinstance(models, list):
            for model_item in models:
                # If the item is a string, convert it to a dict
                if isinstance(model_item, str):
                    standardized_models.append({"name": model_item})
                # If it's already a dict, use it as is
                elif isinstance(model_item, dict):
                    standardized_models.append(model_item)
                else:
                    raise ValueError(
                        f"Model specification must be a string or dictionary, got {type(model_item)}"
                    )
        else:
            raise ValueError(
                f"Models must be a string or a list of strings/dictionaries, got {type(models)}"
            )

        # Process each standardized model
        for each_model_dict in standardized_models:
            model_name = each_model_dict.get("name", "")
            nvcf_id = each_model_dict.get("nvcf_id", "")
            nvcf_version = each_model_dict.get("nvcf_version", "")

            if model_name and not (nvcf_id and nvcf_version):
                if model_name in nvcf_models:
                    self.models[model_name] = NimChatCompletion(
                        model=model_name,
                        nvcf_id=nvcf_id,
                        nvcf_version=nvcf_version,
                        nim_metadata=nim_metadata,
                        monitor=monitor,
                    )
                else:
                    raise ValueError(
                        f"Model {model_name} not supported by the Outerbounds @nim offering."
                        f"\nYou can choose from these options: {nvcf_models}\n\n"
                        "Reach out to Outerbounds if there are other models you'd like supported."
                    )
            elif nvcf_id and nvcf_version:
                self.models[model_name] = NimChatCompletion(
                    model=model_name,
                    nvcf_id=nvcf_id,
                    nvcf_version=nvcf_version,
                    nim_metadata=nim_metadata,
                    monitor=monitor,
                )
            else:
                raise ValueError(
                    "You must provide either a valid 'name' or a custom 'name' along with both 'nvcf_id' and 'nvcf_version'."
                )


class NimChatCompletion(object):
    def __init__(
        self,
        model: str = "meta/llama3-8b-instruct",
        nvcf_id: str = "",
        nvcf_version: str = "",
        nim_metadata: NimMetadata = None,
        monitor: bool = False,
        **kwargs,
    ):
        if nim_metadata is None:
            raise ValueError(
                "NimMetadata object is required to initialize NimChatCompletion object."
            )

        self.model_name = model
        self.nim_metadata = nim_metadata
        self.monitor = monitor
        all_nvcf_models = self.nim_metadata.get_nvcf_chat_completion_models()

        if nvcf_id and nvcf_version:
            matching_models = [
                m
                for m in all_nvcf_models
                if m["function-id"] == nvcf_id and m["version-id"] == nvcf_version
            ]
            if matching_models:
                self.model = matching_models[0]
                self.function_id = self.model["function-id"]
                self.version_id = self.model["version-id"]
                self.model_name = self.model["name"]
            else:
                raise ValueError(
                    f"Function {self.function_id} with version {self.version_id} not found on NVCF"
                )
        else:
            all_nvcf_model_names = [m["name"] for m in all_nvcf_models]

            if self.model_name not in all_nvcf_model_names:
                raise ValueError(
                    f"Model {self.model_name} not found in available NVCF models"
                )

            self.model = all_nvcf_models[all_nvcf_model_names.index(self.model_name)]
            self.function_id = self.model["function-id"]
            self.version_id = self.model["version-id"]

        self.first_request = True

    def log_stats(self, response_data, duration, status_code, poll_count):
        if not self.monitor:
            return

        stats = {
            "status_code": status_code,
            "success": 1 if status_code == 200 else 0,
            "error": 0 if status_code == 200 else 1,
            "e2e_time": duration,
            "model": self.model_name,
            "poll_count": poll_count,
        }

        if status_code == 200 and response_data:
            try:
                stats["prompt_tokens"] = response_data["usage"]["prompt_tokens"]
            except (KeyError, TypeError):
                stats["prompt_tokens"] = None

            try:
                stats["completion_tokens"] = response_data["usage"]["completion_tokens"]
            except (KeyError, TypeError):
                stats["completion_tokens"] = None
        else:
            stats["prompt_tokens"] = None
            stats["completion_tokens"] = None

        conn = sqlite3.connect(self.file_name)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO metrics (error, success, status_code, prompt_tokens, completion_tokens, e2e_time, model)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    stats["error"],
                    stats["success"],
                    stats["status_code"],
                    stats["prompt_tokens"],
                    stats["completion_tokens"],
                    stats["e2e_time"],
                    stats["model"],
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def __call__(self, **kwargs):
        if self.first_request:
            from metaflow import current

            self.file_name = get_storage_path(current.task_id)
            self.first_request = False

        # Create log callback if monitoring is enabled
        log_callback = self.log_stats if self.monitor else None

        request_data = {"model": self.model_name, **kwargs}
        request_url = (
            f"https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/{self.function_id}"
        )

        try:
            response_data = nvcf_submit_helper(
                url=request_url,
                payload=request_data,
                headers=self.nim_metadata.get_headers_for_nvcf_request(),
                log_callback=log_callback,
            )

            return response_data

        except requests.exceptions.HTTPError as e:
            error_msg = f"[@nim ERROR] NVCF API request failed: {str(e)}"
            print(error_msg, file=sys.stderr)
            raise

        except Exception as e:
            error_msg = f"[@nim ERROR] Unexpected error: {str(e)}"
            print(error_msg, file=sys.stderr)
            raise
