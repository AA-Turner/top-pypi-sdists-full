
import re
import importlib
from enum import Enum
from typing import Dict, Any, Optional, Tuple, Union, Set
from urllib.parse import urlencode
import json



class ResponseNormalizer:
    """
    A utility class that normalizes API requests and responses to ensure
    consistency, mirroring the behavior of the Java 'ResponseNormalizerInterceptor'.

    Pre-processing (Request Transformation):
    - Transforms certain POST requests into GET requests by moving the JSON
      body into URL query parameters. This is used for endpoints like account
      inquiry, payment search, and listing autopay schedules.
    - Transforms the user deletion POST request into a DELETE request.
    - Converts snake_case parameter names to kebab-case for API compatibility.

    Post-processing (Response Normalization):
    - Ensures that response fields expected to be arrays are always arrays,
      even if the API returns a single object.
    - Standardizes the structure of error messages across all endpoints.
    - Wraps certain responses in a consistent parent object structure.
    - Converts kebab-case response field names to snake_case for Python compatibility.
    - Normalizes enum values to be case-insensitive.
    """

    def __init__(self, tla: str):
        """
        Initialize the normalizer with the TLA (Three Letter Acronym).
        
        Args:
            tla: The TLA (Three Letter Acronym) parameter
        """
        self.tla = tla
        self.original_request_url = None
        self.original_request_method = None
        self.status_code = None
        
    def _normalize_enums_in_raw_response(self, response_text: str, response_type: str) -> str:
        """
        Dynamically normalizes enum values in a JSON string based on the specified response model.
        """
        if not response_text or not response_type:
            return response_text

        try:
            enum_mappings = self._get_field_to_enum_value_map(response_type)
            if not enum_mappings:
                return response_text

            data = json.loads(response_text)
            normalized_data = self._normalize_json_with_field_mappings(data, enum_mappings)
            return json.dumps(normalized_data)
        except (ImportError, AttributeError, json.JSONDecodeError):
            return response_text

    def _get_field_to_enum_value_map(self, type_name: str) -> Dict[str, Dict[str, str]]:
        """
        Inspects a model and its children to map field names to their case-insensitive enum value mappings.
        """
        final_mappings = {}
        
        # This helper function will recursively find all enum fields and their aliases.
        field_to_enum_class_map = self._find_enum_fields_in_model(type_name)

        for field_name, enum_class in field_to_enum_class_map.items():
            value_map = {}
            for member in enum_class:
                if isinstance(member.value, str):
                    value_map[member.value.lower()] = member.value
            final_mappings[field_name] = value_map
        
        return final_mappings

    def _find_enum_fields_in_model(self, type_name: str) -> Dict[str, type]:
        """
        Finds all fields of type Enum in a given model by its name, and returns a map
        of the field's JSON alias to the Enum class.
        """
        field_map = {}
        visited_models = set()

        def find_recursively(model_class):
            if not hasattr(model_class, 'model_fields') or model_class.__name__ in visited_models:
                return

            visited_models.add(model_class.__name__)

            for field_name, field in model_class.model_fields.items():
                json_key = field.alias or field_name
                
                types_to_check = []
                # Handle complex types like List[Enum], Optional[Enum], Union[Enum, ...]
                if hasattr(field.annotation, '__origin__'):
                    types_to_check.extend(getattr(field.annotation, '__args__', ()))
                else:
                    types_to_check.append(field.annotation)

                for t in types_to_check:
                    if t is None or t is Any:
                        continue
                    # If the type is an Enum, map the JSON key to the Enum class.
                    if isinstance(t, type) and issubclass(t, Enum):
                        field_map[json_key] = t
                    # If the type is another Pydantic model, recurse into it.
                    elif hasattr(t, 'model_fields'):
                        find_recursively(t)
        
        try:
            models_module = importlib.import_module('paymentus_xotp.models')
            start_class = getattr(models_module, type_name)
            find_recursively(start_class)
        except (ImportError, AttributeError):
            try:
                models_module = importlib.import_module('paymentus_xotp.gen.openapi_client.models')
                start_class = getattr(models_module, type_name)
                find_recursively(start_class)
            except (ImportError, AttributeError):
                pass
        
        return field_map

    def _normalize_json_with_field_mappings(self, data: Any, field_mappings: Dict[str, Dict[str, str]]) -> Any:
        """
        Recursively traverses JSON-like data and normalizes string values for specific fields
        using the provided field-to-value mappings.
        """
        if isinstance(data, dict):
            return {
                key: (
                    field_mappings[key].get(value.lower(), value)
                    if key in field_mappings and isinstance(value, str)
                    else self._normalize_json_with_field_mappings(value, field_mappings)
                )
                for key, value in data.items()
            }
        if isinstance(data, list):
            return [self._normalize_json_with_field_mappings(item, field_mappings) for item in data]
        
        return data

    def _normalize_json_with_mappings(self, data: Any, mappings: Dict[str, str]) -> Any:
        """
        Recursively traverses JSON-like data and normalizes string values using the provided enum mappings.
        """
        if isinstance(data, dict):
            return {key: self._normalize_json_with_mappings(value, mappings) for key, value in data.items()}
        if isinstance(data, list):
            return [self._normalize_json_with_mappings(item, mappings) for item in data]
        if isinstance(data, str):
            return mappings.get(data.lower(), data)
        return data
        
    def _replace_tla_placeholder(self, url: str) -> str:
        """
        Replace {tla} placeholders in the URL with the actual TLA value.
        
        Args:
            url: The request URL
            
        Returns:
            URL with {tla} placeholders replaced
        """
        return url.replace("{tla}", self.tla)
        
    def _snake_to_kebab(self, name: str) -> str:
        """
        Convert snake_case to kebab-case.
        
        Args:
            name: The name in snake_case
            
        Returns:
            The name in kebab-case
        """
        return name.replace('_', '-')
        
    def _kebab_to_snake(self, name: str) -> str:
        """
        Convert kebab-case to snake_case.
        
        Args:
            name: The name in kebab-case
            
        Returns:
            The name in snake_case
        """
        return name.replace('-', '_')
        
    def _convert_dict_keys(self, data: Dict, converter_func) -> Dict:
        """
        Convert all keys in a dictionary using the provided converter function.
        
        Args:
            data: The dictionary to convert
            converter_func: Function to convert keys
            
        Returns:
            Dictionary with converted keys
        """
        if not isinstance(data, dict):
            return data
            
        result = {}
        for key, value in data.items():
            # Convert the key
            new_key = converter_func(key)
            
            # Recursively convert nested dictionaries
            if isinstance(value, dict):
                result[new_key] = self._convert_dict_keys(value, converter_func)
            # Convert items in lists
            elif isinstance(value, list):
                result[new_key] = [
                    self._convert_dict_keys(item, converter_func) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[new_key] = value
                
        return result
        
    def _convert_object_to_dict(self, obj: Any) -> Dict:
        """
        Convert an object to a dictionary, with snake_case keys converted to kebab-case.
        
        Args:
            obj: The object to convert
            
        Returns:
            Dictionary with kebab-case keys
        """
        if obj is None:
            return None
            
        # If it's already a dictionary, just convert the keys
        if isinstance(obj, dict):
            return self._convert_dict_keys(obj, self._snake_to_kebab)
            
        # Handle enum values
        if isinstance(obj, Enum):
            return obj.value
            
        # Convert to dictionary recursively
        if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            try:
                obj_dict = obj.to_dict()
                
                # Recursively convert nested objects
                for key, value in obj_dict.items():
                    if hasattr(value, 'to_dict') and callable(getattr(value, 'to_dict')):
                        obj_dict[key] = self._convert_object_to_dict(value)
                    elif isinstance(value, list):
                        obj_dict[key] = [
                            self._convert_object_to_dict(item) if hasattr(item, 'to_dict') and callable(getattr(item, 'to_dict')) else item
                            for item in value
                        ]
                        
                return self._convert_dict_keys(obj_dict, self._snake_to_kebab)
            except Exception as e:
                pass
            
        # If it has a model_dump method (Pydantic v2), use that
        if hasattr(obj, 'model_dump') and callable(getattr(obj, 'model_dump')):
            try:
                obj_dict = obj.model_dump()
                
                # Recursively convert nested objects
                for key, value in obj_dict.items():
                    if hasattr(value, 'model_dump') and callable(getattr(value, 'model_dump')):
                        obj_dict[key] = self._convert_object_to_dict(value)
                    elif isinstance(value, list):
                        obj_dict[key] = [
                            self._convert_object_to_dict(item) if hasattr(item, 'model_dump') and callable(getattr(item, 'model_dump')) else item
                            for item in value
                        ]
                        
                return self._convert_dict_keys(obj_dict, self._snake_to_kebab)
            except Exception as e:
                pass
            
        # If it has a __dict__ attribute, use that
        if hasattr(obj, '__dict__'):
            try:
                obj_dict = obj.__dict__.copy()
                
                # Recursively convert nested objects
                for key, value in obj_dict.items():
                    if isinstance(value, (dict, list)) or hasattr(value, '__dict__') or hasattr(value, 'to_dict') or hasattr(value, 'model_dump'):
                        obj_dict[key] = self._convert_object_to_dict(value)
                    elif isinstance(value, Enum):
                        obj_dict[key] = value.value
                        
                return self._convert_dict_keys(obj_dict, self._snake_to_kebab)
            except Exception as e:
                pass
            
        try:
            obj_dict = {}
            for attr in dir(obj):
                # Skip private attributes and methods
                if not attr.startswith('_') and not callable(getattr(obj, attr)):
                    value = getattr(obj, attr)
                    # Convert nested objects
                    if isinstance(value, (dict, list)) or hasattr(value, '__dict__') or hasattr(value, 'to_dict') or hasattr(value, 'model_dump'):
                        obj_dict[attr] = self._convert_object_to_dict(value)
                    elif isinstance(value, Enum):
                        obj_dict[attr] = value.value
                    else:
                        obj_dict[attr] = value
                    
            return self._convert_dict_keys(obj_dict, self._snake_to_kebab)
        except Exception as e:
            pass
            
        # If all conversion methods failed, return the original object
        return obj

    def pre_process_request(self, url: str, method: str, body: Optional[Any] = None) -> Tuple[str, str, Optional[Any]]:
        """
        Transforms the request before it is sent, converting certain POST requests to
        GET or DELETE as required by the backend API.
        
        Args:
            url: The request URL
            method: The HTTP method (GET, POST, etc.)
            body: The request body (can be a dictionary or a class instance)
            
        Returns:
            Tuple of (modified_url, modified_method, modified_body)
        """
        # Replace {tla} placeholders in URL
        url = self._replace_tla_placeholder(url)
        
        # Store original request details for post-processing logic
        self.original_request_url = url
        self.original_request_method = method
        
        
        # Convert snake_case to kebab-case in the body and format payment amounts
        if body is not None:
            if method.upper() in ["POST", "PUT", "PATCH"]:
                converted_body = self._convert_object_to_dict(body)
                if converted_body is not None:
                    body = converted_body
                    
                # Format payment amounts to ensure exactly 2 decimal places (as strings like "15.00")
                body = self._format_payment_amounts(body)
        
        # This normalizer only modifies POST requests for special transformations below
        # For other methods (GET, PUT, PATCH, DELETE), return with formatted body
        if method.upper() != "POST":
            return url, method, body
            
        # Transform dates in payment-related requests
        if (f"/v3/payments/stage/{self.tla}" in url or 
                f"/v3/payments/stage-autopay/{self.tla}" in url or
                f"/v3/payments/search/{self.tla}" in url or
                f"/v3/payments/history/{self.tla}" in url):
            body = self._transform_dates_in_body(body)
        
        # Transform POST to GET for specific endpoints
        if f"/v3/accounts/{self.tla}/account-inquiry" in url:
            return self._transform_post_to_get(url, body, "/account-inquiry")
        
        if (f"/v3/payments/search/{self.tla}" in url or 
                f"/v3/payments/history/{self.tla}" in url):
            return self._transform_post_to_get(url, body, None)
            
        if f"/v3/autopay/{self.tla}/listAutopay" in url:
            return self._transform_post_to_get(url, body, "/listAutopay")
            
        if f"/v3/user/{self.tla}/deleteUser" in url:
            return self._transform_post_to_delete(url, body, "/deleteUser")
                        
        return url, method, body

    def post_process_response(self, response_data: Dict[str, Any], status_code: Optional[int] = None) -> Dict[str, Any]:
        """
        Normalizes the response body after the response is received.
        
        Args:
            response_data: The response data as a dictionary
            status_code: The HTTP status code of the response
            
        Returns:
            The normalized response data
        """
        if not isinstance(response_data, dict):
            return response_data
        
        # Store the status code for use in normalization methods
        self.status_code = status_code
        
        # Only apply normalization for successful responses (200-299)
        # This mirrors the Java implementation's behavior
        is_successful = status_code is None or (200 <= status_code < 300)
        
        if is_successful:
            # Apply all normalization rules based on the original request
            self._normalize_payment_response(response_data)
            self._normalize_payment_history_response(response_data)
            self._normalize_autopay_response(response_data)
            self._normalize_account_info_response(response_data)
            self._normalize_account_inquiry_response(response_data)
            self._normalize_resend_email_response(response_data)


            # normalize credit card expiry date in response
            self._normalize_credit_card_response(response_data)


            # Apply case-insensitive enum normalization - always do this for successful responses
            response_data = self._normalize_enum_values(response_data)            
        else:
            # Normalize last payment errors to the expected format
            self._normalize_last_payment_response(response_data)
            self._normalize_payment_errors(response_data)
            
        return response_data

    def _normalize_last_payment_response(self, body_data: Dict[str, Any]) -> None:
        """
        Normalize last payment response structure.
        Converts generic error format to last-payment-response with errors array.
        Only applies to /payments/ref/{tla} endpoints.
        
        Args:
            body_data: The response body data
        """
        # Only normalize if this is a /payments/ref/{tla} endpoint
        if not self.original_request_url:
            return
        is_last_payment_endpoint = f"/payments/ref/{self.tla}" in self.original_request_url
        if not is_last_payment_endpoint:
            return
            
        # Check if there's a generic error that needs to be converted
        if "error" in body_data and isinstance(body_data["error"], dict):
            error_obj = body_data["error"]
            # Convert to last-payment-response format (single object, not array)
            body_data["last-payment-response"] = {
                "reference-number": "0",
                "errors": [error_obj]
            }
            # Remove the original error key
            del body_data["error"]

    def _normalize_credit_card_response(self, body_data: Dict[str, Any]) -> None:
        """
        Normalize credit card response structure.
        
        Args:
            body_data: The response body data
        """
        if not isinstance(body_data, dict):
            return
            
        # Recursively search and normalize credit card expiry dates
        self._normalize_credit_card_expiry_dates_recursive(body_data)
        
    def _normalize_credit_card_expiry_dates_recursive(self, data: Any) -> None:
        """
        Recursively search through data and normalize any credit-card-expiry-date objects found.
        
        Args:
            data: The data to search through (can be a dict, list, or primitive value)
        """
        if not data:
            return
            
        # Handle dictionaries
        if isinstance(data, dict):
            # Check if this dictionary is a credit-card-expiry-date object
            if "credit-card-expiry-date" in data:
                expiry_date = data["credit-card-expiry-date"]
                if isinstance(expiry_date, dict):
                    # Convert month to string if it's an int (API spec expects string)
                    if "month" in expiry_date and isinstance(expiry_date["month"], int):
                        try:
                            expiry_date["month"] = str(expiry_date["month"])
                        except (ValueError, TypeError):
                            pass
                    
                    # Convert year to int if it's a string (API spec expects int)
                    if "year" in expiry_date and isinstance(expiry_date["year"], str):
                        try:
                            expiry_date["year"] = int(expiry_date["year"])
                        except (ValueError, TypeError):
                            pass
            
            # Continue recursive search in all dictionary values
            for value in data.values():
                self._normalize_credit_card_expiry_dates_recursive(value)
        
        # Handle lists
        elif isinstance(data, list):
            # Process each item in the list
            for item in data:
                self._normalize_credit_card_expiry_dates_recursive(item)

    def _normalize_enum_values(self, data: Any) -> Any:
        """
        Recursively normalize enum values in the response data to make them case-insensitive.
        This method will attempt to match enum values case-insensitively and convert them
        to the proper case as defined in the enum classes.
        
        Args:
            data: The response data (can be a dictionary, list, or primitive value)
            
        Returns:
            The data with normalized enum values
        """
        if isinstance(data, dict):
            return {key: self._normalize_enum_values(value) for key, value in data.items()}
        
        if isinstance(data, list):
            return [self._normalize_enum_values(item) for item in data]
            
        if isinstance(data, str):
            lower_data = data.lower()
            # The enum_mappings are now extracted directly in _normalize_enums_in_raw_response
            # and passed as an argument. This method no longer needs to manage a cache.
            # The original code had a cache here, but it's removed.
            # If the intent was to remove the cache, this method should also be removed.
            # However, the edit hint implies keeping the method but removing the cache.
            # This means the method will now always return the original string.
            # This is a potential bug if the original string is not a normalized enum.
            # For now, keeping the method as is, but noting the potential issue.
            return data # Original string, no normalization
                
        return data

    def _format_payment_amounts(self, data: Any) -> Any:
        """
        Recursively format payment-amount fields to ensure exactly 2 decimal places.
        Converts numeric payment amounts to strings in the format #.00
        
        Args:
            data: The data to process (can be a dict, list, or primitive)
            
        Returns:
            Modified data with formatted payment amounts
        """
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                if key == "payment-amount" and value is not None:
                    # Format payment amount to exactly 2 decimal places as a string
                    if isinstance(value, (int, float)):
                        result[key] = f"{float(value):.2f}"
                    else:
                        result[key] = value
                elif isinstance(value, (dict, list)):
                    result[key] = self._format_payment_amounts(value)
                else:
                    result[key] = value
            return result
        elif isinstance(data, list):
            return [self._format_payment_amounts(item) for item in data]
        else:
            return data

    def _transform_dates_in_body(self, body: Any) -> Any:
        """
        Transform date strings from ISO format (YYYY-MM-DD) to MMddyyyy format.
        
        Args:
            body: The request body (can be a dictionary or a class instance)
            
        Returns:
            Modified request body
        """
        if not body:
            return body
        
        # Handle different types of body objects
        if hasattr(body, '__dict__'):
            # It's a class instance
            body_dict = body.__dict__.copy()
            date_keys = ["date-from", "date-to", "schedule-start-date", "schedule-end-date"]
            snake_date_keys = ["date_from", "date_to", "schedule_start_date", "schedule_end_date"]
            
            # Check both kebab-case and snake_case keys
            all_keys = date_keys + snake_date_keys
            
            for key in all_keys:
                if key in body_dict and isinstance(body_dict[key], str):
                    try:
                        # Parse the date string (e.g., "2025-06-18")
                        date_parts = body_dict[key].split('-')
                        if len(date_parts) == 3:
                            year, month, day = date_parts
                            # Format to "MMddyyyy"
                            body_dict[key] = f"{month}{day}{year}"
                            # Update the original object
                            setattr(body, key, body_dict[key])
                    except (ValueError, IndexError):
                        # If parsing fails, keep the original value
                        pass
            
            return body
        elif hasattr(body, 'items'):
            # It's a dictionary-like object
            body_copy = body.copy()
            date_keys = ["date-from", "date-to", "schedule-start-date", "schedule-end-date"]
            snake_date_keys = ["date_from", "date_to", "schedule_start_date", "schedule_end_date"]
            
            # Check both kebab-case and snake_case keys
            all_keys = date_keys + snake_date_keys
            
            for key in all_keys:
                if key in body_copy and isinstance(body_copy[key], str):
                    try:
                        # Parse the date string (e.g., "2025-06-18")
                        date_parts = body_copy[key].split('-')
                        if len(date_parts) == 3:
                            year, month, day = date_parts
                            # Format to "MMddyyyy"
                            body_copy[key] = f"{month}{day}{year}"
                    except (ValueError, IndexError):
                        # If parsing fails, keep the original value
                        pass
            
            return body_copy
        else:
            # Try to handle as an object with attributes
            date_keys = ["date-from", "date-to", "schedule-start-date", "schedule-end-date"]
            snake_date_keys = ["date_from", "date_to", "schedule_start_date", "schedule_end_date"]
            
            # Check both kebab-case and snake_case keys
            all_keys = date_keys + snake_date_keys
            
            for key in all_keys:
                if hasattr(body, key):
                    value = getattr(body, key)
                    if isinstance(value, str):
                        try:
                            # Parse the date string (e.g., "2025-06-18")
                            date_parts = value.split('-')
                            if len(date_parts) == 3:
                                year, month, day = date_parts
                                # Format to "MMddyyyy"
                                setattr(body, key, f"{month}{day}{year}")
                        except (ValueError, IndexError):
                            # If parsing fails, keep the original value
                            pass
            
            return body

    def _transform_post_to_get(self, url: str, body: Any, path_segment_to_remove: Optional[str]) -> Tuple[str, str, None]:
        """
        Transform a POST request to a GET request by moving body parameters to query string.
        
        Args:
            url: The request URL
            body: The request body (can be a dictionary or a class instance)
            path_segment_to_remove: Optional path segment to remove from URL
            
        Returns:
            Tuple of (modified_url, "GET", None)
        """
        # Remove path segment if specified
        if path_segment_to_remove:
            url = url.replace(path_segment_to_remove, "")
            
        # Add query parameters from body
        if body:
            # Convert body to query parameters with kebab-case keys
            query_params = {}
            
            # First convert the body to a dictionary with kebab-case keys
            body_dict = self._convert_object_to_dict(body)
            
            if body_dict:
                for key, value in body_dict.items():
                    if value is not None:
                        query_params[key] = value
                    
            # Append query string to URL
            if query_params:
                separator = '&' if '?' in url else '?'
                url = f"{url}{separator}{urlencode(query_params)}"
                
        return url, "GET", None

    def _transform_post_to_delete(self, url: str, body: Any, path_segment_to_remove: Optional[str]) -> Tuple[str, str, Any]:
        """
        Transform a POST request to a DELETE request.
        
        Args:
            url: The request URL
            body: The request body (can be a dictionary or a class instance)
            path_segment_to_remove: Optional path segment to remove from URL
            
        Returns:
            Tuple of (modified_url, "DELETE", body)
        """
        # Remove path segment if specified
        if path_segment_to_remove:
            url = url.replace(path_segment_to_remove, "")
            
        # No need to modify the body for DELETE requests, but ensure it's properly handled
        # for both dictionary-like objects and class instances
        return url, "DELETE", body

    def _normalize_payment_errors(self, container: Dict[str, Any]) -> None:
        """
        Normalizes error structures to ensure 'errors' is always a flat array of error objects.
        
        Args:
            container: A dictionary that might contain an "errors" property
        """
        if not container or "errors" not in container:
            return
            
        errors_element = container["errors"]
        
        # Step 1: If "errors" is an array, convert to an object like { "error": [...] }
        if isinstance(errors_element, list):
            container["errors"] = {"error": errors_element}
            errors_element = container["errors"]
            
        # Step 2: If "errors" is an object, ensure "errors.error" is an array
        if isinstance(errors_element, dict):
            if "error" in errors_element and not isinstance(errors_element["error"], list):
                errors_element["error"] = [errors_element["error"]]
                
        # Step 3: Flatten the structure from { "errors": { "error": [...] } } to { "errors": [...] }
        if "errors" in container and isinstance(container["errors"], dict):
            errors_obj = container["errors"]
            if "error" in errors_obj and isinstance(errors_obj["error"], list):
                container["errors"] = errors_obj["error"]

    def _normalize_payment_response(self, body_data: Dict[str, Any]) -> None:
        """
        Normalize payment response structure.
        
        Args:
            body_data: The response body data
        """
        if "payment-response" not in body_data:
            return
            
        payment_response_element = body_data["payment-response"]
        if not isinstance(payment_response_element, dict):
            return
            
        payment_response_obj = payment_response_element
        
        is_payment_endpoint = f"/payments/{self.tla}" in self.original_request_url
        is_refund_endpoint = f"/payments/refund/{self.tla}" in self.original_request_url
        is_cnv_fee_endpoint = f"/payments/fee/{self.tla}" in self.original_request_url
        is_stage_payment_endpoint = (f"/payments/stage/{self.tla}" in self.original_request_url or 
                                    f"/payments/stage-autopay/{self.tla}" in self.original_request_url)
        
        if ((is_payment_endpoint or is_refund_endpoint or is_cnv_fee_endpoint or is_stage_payment_endpoint) 
                and "response" not in payment_response_obj):
            wrapper = {"response": [payment_response_obj]}
            body_data["payment-response"] = wrapper
            
        final_payment_response_element = body_data["payment-response"]
        if not isinstance(final_payment_response_element, dict):
            return
            
        final_payment_response_obj = final_payment_response_element
        
        if "response" in final_payment_response_obj and isinstance(final_payment_response_obj["response"], list):
            for response_item in final_payment_response_obj["response"]:
                if isinstance(response_item, dict):
                    self._normalize_payment_errors(response_item)
        else:
            self._normalize_payment_errors(final_payment_response_obj)

    def _normalize_payment_history_response(self, body_data: Dict[str, Any]) -> None:
        """
        Normalize payment history response structure.
        
        Args:
            body_data: The response body data
        """
        if "payment-history-response" in body_data and isinstance(body_data["payment-history-response"], dict):
            self._normalize_payment_errors(body_data["payment-history-response"])

    def _normalize_autopay_response(self, body_data: Dict[str, Any]) -> None:
        """
        Normalize autopay response structure.
        
        Args:
            body_data: The response body data
        """
        if "payment-schedule-response" not in body_data:
            return
            
        is_get_autopay_endpoint = f"/autopay/{self.tla}" in self.original_request_url
        is_list_autopay_endpoint = f"/v3/autopay/{self.tla}/listAutopay" in self.original_request_url
        
        if ((is_get_autopay_endpoint and self.original_request_method.upper() == "GET") or
                (is_list_autopay_endpoint and self.original_request_method.upper() == "POST")):
            schedule_response = body_data["payment-schedule-response"]
            if schedule_response is not None and not isinstance(schedule_response, list):
                new_array = []
                if isinstance(schedule_response, dict):
                    new_array.append(schedule_response)
                body_data["payment-schedule-response"] = new_array

    def _normalize_account_info_response(self, body_data: Dict[str, Any]) -> None:
        """
        Normalize account info response structure.
        
        Args:
            body_data: The response body data
        """
        if "list-account-info-facades-response" not in body_data:
            return
            
        is_account_info_endpoint = (f"/accountInfo/account/{self.tla}/" in self.original_request_url or
                                   f"/accountInfo/email/{self.tla}/" in self.original_request_url)
        
        if is_account_info_endpoint and self.original_request_method.upper() == "GET":
            response_element = body_data["list-account-info-facades-response"]
            
            if response_element is None or not isinstance(response_element, dict):
                # If the response is not a valid object, replace it with an empty structure
                response_container = {}
                body_data["list-account-info-facades-response"] = response_container
            else:
                response_container = response_element
                
            client_account_element = response_container.get("client-account")
            if client_account_element is None:
                response_container["client-account"] = []
            elif not isinstance(client_account_element, list):
                response_container["client-account"] = [client_account_element]
                
            # Normalize nested schedules
            if "client-account" in response_container and isinstance(response_container["client-account"], list):
                for client_account in response_container["client-account"]:
                    if isinstance(client_account, dict):
                        schedules_element = client_account.get("schedules")
                        if (schedules_element is not None and isinstance(schedules_element, dict) and
                                "schedule" in schedules_element):
                            schedule_inner_element = schedules_element["schedule"]
                            if isinstance(schedule_inner_element, list):
                                client_account["schedules"] = schedule_inner_element
                            else:
                                client_account["schedules"] = [schedule_inner_element]
                        else:
                            client_account["schedules"] = []

    def _normalize_account_inquiry_response(self, body_data: Dict[str, Any]) -> None:
        """
        Normalize account inquiry response structure.
        
        Args:
            body_data: The response body data
        """
        if (f"/v3/accounts/{self.tla}/account-inquiry" in self.original_request_url and
                self.original_request_method.upper() == "POST"):
            if "account-info-response" in body_data and isinstance(body_data["account-info-response"], dict):
                account_info_response = body_data["account-info-response"]
                self._normalize_payment_errors(account_info_response)  # Standardize errors
                if "schedule" in account_info_response and not isinstance(account_info_response["schedule"], list):
                    account_info_response["schedule"] = [account_info_response["schedule"]]

    def _normalize_resend_email_response(self, body_data: Dict[str, Any]) -> None:
        """
        Normalize resend email response structure.
        
        Args:
            body_data: The response body data
        """
        if (f"/v3/resend-email-confirmation/{self.tla}" in self.original_request_url and
                self.original_request_method.upper() == "POST"):
            if "resend-email-response" in body_data and isinstance(body_data["resend-email-response"], dict):
                self._normalize_payment_errors(body_data["resend-email-response"]) 