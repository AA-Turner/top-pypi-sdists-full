"""
Logging middleware for XOTP SDK.
"""
import json
import time
from typing import Dict, Any, Optional, Set, Union
from functools import wraps
from json import JSONDecodeError

from ..logging import Logger, LogLevel, MaskingLevel


class LoggingConfiguration:
    """Configuration for logging middleware."""
    
    def __init__(
        self,
        level: LogLevel = LogLevel.NORMAL,
        masking: MaskingLevel = MaskingLevel.PCI_ONLY,
        logger: Optional[Logger] = None
    ):
        """
        Initialize a new logging configuration.
        
        Args:
            level: Log level.
            masking: Masking level.
            logger: A fully configured logger instance.
        """
        self.level = level
        self.masking = masking
        self.logger = logger or Logger(level)


class LoggingMiddleware:
    """
    Middleware for logging requests and responses.
    
    This middleware is responsible for logging HTTP requests and responses,
    and masking sensitive data based on the configured logging and masking levels.
    """
    
    # Define sensitive fields for PCI masking (e.g., credit card details)
    PCI_FIELDS = {
        "account_number", "account-number", 
        "cvv", "cv2", 
        "card_holder_name", "card-holder-name"
    }

    # Define sensitive fields for general PII masking
    PII_FIELDS = {
        "first_name", "first-name", 
        "last_name", "last-name", 
        "day_phone_nr", "day-phone-nr",
        "email", "phone_number", "phone-number"
    }

    # Define address fields for PII masking
    ADDRESS_FIELDS = {
        "line1", "line2", 
        "state", "zip_code", "zip-code", 
        "city", "country"
    }
    
    def __init__(self, config: LoggingConfiguration):
        """
        Initialize the logging middleware
        
        Args:
            config: Logging configuration
        """
        self.config = config
        self.logger = config.logger
    
    def apply_to_client(self, api_client):
        """
        Apply logging middleware to an API client by patching its methods
        
        Args:
            api_client: The API client to patch
        """
        # Store original methods
        original_call_api = api_client.call_api
        original_param_serialize = api_client.param_serialize
        
        # Request context to track timing and session info
        request_context = {
            "start_time": None,
            "session_id": None,
            "headers": {}
        }
        
        # Patch param_serialize to capture the headers
        @wraps(original_param_serialize)
        def patched_param_serialize(method, resource_path, path_params=None, query_params=None, 
                                  header_params=None, body=None, post_params=None, 
                                  files=None, auth_settings=None, collection_formats=None, 
                                  _host=None, _request_auth=None):
            # Capture headers from both sources
            all_headers = {}
            
            # Add default headers from api_client
            if api_client.default_headers:
                all_headers.update(api_client.default_headers)
                
            # Get headers from header_params parameter
            if header_params and isinstance(header_params, dict):
                all_headers.update(header_params)
                
            # Store all headers in request_context
            request_context["headers"] = all_headers
            
            # Call original method
            return original_param_serialize(method, resource_path, path_params, query_params, 
                                          header_params, body, post_params, files, 
                                          auth_settings, collection_formats, _host, _request_auth)
        
        # Patch call_api to log requests and responses
        @wraps(original_call_api)
        def patched_call_api(resource_path, url, *args, **kwargs):
            # Get session ID from headers if present
            headers = kwargs.get("_headers", {}) or {}
            header_params = kwargs.get("header_params", {}) or {}
            
            # Combine all headers
            all_headers = {}
            all_headers.update(api_client.default_headers)
            all_headers.update(header_params)
            all_headers.update(headers)
            
            if isinstance(all_headers, dict):
                request_context["session_id"] = all_headers.get("X-Ext-Session-Id")
                request_context["headers"] = all_headers
            
            self._log_request(resource_path, url, kwargs.get("body"), all_headers, request_context["session_id"])
            
            # Record start time
            request_context["start_time"] = time.time()
            
            # Make the actual request
            try:
                response = original_call_api(resource_path, url, *args, **kwargs)
                
                # The response body is a one-time read stream. To allow both logging
                # and deserialization, we read it once here and then patch the response
                # object to return the stored data on subsequent reads.
                response_body_bytes = response.read()

                # Patch the response object's read method
                original_read = response.read
                def new_read(*args, **kwargs):
                    return response_body_bytes
                response.read = new_read

                # Also patch the .data property if it's based on read()
                # For safety, we'll just set it directly.
                response.data = response_body_bytes
                
                # Log the response
                elapsed_ms = int((time.time() - request_context["start_time"]) * 1000)
                status_code = getattr(response, "status", None)
                
                # Get response headers if available
                response_headers = {}
                if hasattr(response, "getheaders") and callable(getattr(response, "getheaders")):
                    response_headers = dict(response.getheaders())
                
                self._log_response(url, status_code, response, response_headers, elapsed_ms, request_context["session_id"])
                
                return response
            except Exception as e:
                # Log any exceptions
                self.logger.error("Request failed: %s", str(e))
                raise
        
        # Replace the original methods with patched versions
        api_client.param_serialize = patched_param_serialize
        api_client.call_api = patched_call_api
    
    def _log_request(self, method:str, url: str, body: Any, headers: Optional[Dict[str, str]], session_id: Optional[str]) -> None:
        """
        Log an HTTP request
        
        Args:
            url: Request URL
            method: HTTP method
            body: Request body
            headers: Request headers
            session_id: Session ID if available
        """
        # Skip logging if level is SILENT
        if self.config.level == LogLevel.SILENT:
            return
        
        # Log basic request info
        if session_id:
            self.logger.info("-->[%s] %s %s", session_id, method, url)
        else:
            self.logger.info("--> %s %s", method, url)
        
        # Return if only minimal logging is enabled
        if self.config.level == LogLevel.MINIMAL:
            return
        
        # Log request body for NORMAL and VERBOSE levels
        if body is not None:
            try:
                if isinstance(body, (dict, list)):
                    body_dict = body
                elif hasattr(body, "to_dict") and callable(getattr(body, "to_dict")):
                    body_dict = body.to_dict()
                elif hasattr(body, "model_dump") and callable(getattr(body, "model_dump")):
                    body_dict = body.model_dump()
                else:
                    body_dict = None
                
                if body_dict:
                    masked_body = self._mask_sensitive_data(body_dict)
                    self.logger.debug("Request Body: %s", json.dumps(masked_body))
            except Exception as e:
                self.logger.debug("Request Body: (Failed to parse or mask: %s)", str(e))
        
        # Log headers for VERBOSE level only
        if self.config.level == LogLevel.VERBOSE and headers:
            # Create a safe copy to avoid modifying the original headers
            safe_headers = {}
            for k, v in headers.items():
                # Skip sensitive headers like Authorization
                if k.lower() == 'authorization':
                    safe_headers[k] = 'Bearer [MASKED]'
                else:
                    safe_headers[k] = v
            
            self.logger.debug("Request Headers: %s", json.dumps(safe_headers))
    
    def _log_response(self, url: str, status_code: Optional[int], response: Any, 
                     headers: Optional[Dict[str, str]], elapsed_ms: int, session_id: Optional[str]) -> None:
        """
        Log an HTTP response
        
        Args:
            url: Request URL
            status_code: HTTP status code
            response: Response object
            headers: Response headers
            elapsed_ms: Time elapsed in milliseconds
            session_id: Session ID if available
        """
        # Skip logging if level is SILENT
        if self.config.level == LogLevel.SILENT:
            return
        
        # Log basic response info
        status = status_code if status_code else "???"
        log_method = self.logger.error if status_code and status_code >= 400 else self.logger.info
        
        if session_id:
            log_method("<-- [%s] Response (%dms) - Status: %s for %s", 
                      session_id, elapsed_ms, status, url)
        else:
            log_method("<-- Response (%dms) - Status: %s for %s", 
                      elapsed_ms, status, url)
        
        # Return if only minimal logging is enabled
        if self.config.level == LogLevel.MINIMAL:
            return
        
        # Log response data for NORMAL and VERBOSE levels
        try:
            response_data = getattr(response, "data", None)
            if response_data:
                # Attempt to decode and log as JSON
                try:
                    response_text = response_data.decode('utf-8')
                    response_json = json.loads(response_text)
                    masked_data = self._mask_sensitive_data(response_json)
                    self.logger.debug("Response Body: %s", json.dumps(masked_data))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # If not JSON, log the raw text (truncated)
                    self.logger.debug("Response Body (non-JSON): %s", response_data[:500])
            else:
                self.logger.debug("Response Body: (empty)")
        except Exception as e:
            self.logger.debug("Response Body: (Failed to parse or mask: %s)", str(e))
            
        # Log headers for VERBOSE level only
        if self.config.level == LogLevel.VERBOSE and headers:
            self.logger.debug("Response Headers: %s", json.dumps(headers))
    
    def _mask_sensitive_data(self, data: Any) -> Any:
        """
        Mask sensitive data in the request or response
        
        Args:
            data: Data to mask
            
        Returns:
            Data with sensitive fields masked
        """
        if self.config.masking == MaskingLevel.NONE:
            return data
        
        # Create a deep copy of the data to avoid modifying the original
        if isinstance(data, dict):
            result = data.copy()
            self._mask_dict_fields(result)
            return result
        elif isinstance(data, list):
            return [self._mask_sensitive_data(item) for item in data]
        else:
            return data
    
    def _mask_dict_fields(self, data_dict: Dict[str, Any]) -> None:
        """
        Recursively mask fields in a dictionary
        
        Args:
            data_dict: Dictionary to mask
        """
        if not isinstance(data_dict, dict):
            return
        
        # Process all fields in the dictionary
        for key, value in list(data_dict.items()):
            # Recursively process nested dictionaries
            if isinstance(value, dict):
                self._mask_dict_fields(value)
            # Process items in lists
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._mask_dict_fields(item)
            
            # Check if this field needs masking
            key_lower = key.lower().replace('_', '-')  # Normalize keys for comparison
            
            # Always mask PCI fields
            if key_lower in self.PCI_FIELDS:
                if isinstance(value, str) and value:
                    data_dict[key] = self._mask_value(value)
            
            # Mask PII fields if configured
            elif self.config.masking == MaskingLevel.ALL_PII:
                if key_lower in self.PII_FIELDS or key_lower in self.ADDRESS_FIELDS:
                    if isinstance(value, str) and value:
                        data_dict[key] = self._mask_value(value)
    
    def _mask_value(self, value: str) -> str:
        """
        Mask a sensitive value
        
        Args:
            value: Value to mask
            
        Returns:
            Masked value
        """
        if not value or len(value) <= 4:
            return "****"
        
        # Show first and last character for context, mask the middle
        return value[0] + "*" * (len(value) - 2) + value[-1] 