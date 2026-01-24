# This file is auto-generated, do not edit manually
# Generated from XOTP API specification
import json
import logging
from typing import Any, Dict, List, Optional, Union, Callable, Awaitable
from typing_extensions import Annotated, Protocol
from pydantic import StrictStr, StrictBool, StrictInt, StrictFloat, Field
from functools import wraps

from ..api.xotp_api import XotpApi
from ..api_client import ApiClient
from ..configuration import Configuration
from ..exceptions import ApiException
from ..api_response import ApiResponse
from ..rest import RESTResponse
from ..middlewares import ResponseNormalizer, LoggingMiddleware, LoggingConfiguration

# Import all models
from ..models import *

# Set up logger
logger = logging.getLogger(__name__)


# Type for async token provider function
TokenProviderType = Callable[[], Awaitable[str]]


class XotpApiClient:
    """
    XOTP API Client Wrapper
    
    This wrapper provides a simplified interface to the XOTP API,
    similar to the Java SDK structure.
    """

    def __init__(self, base_url: str, tla: str, token_provider: Optional[TokenProviderType] = None, api_client: Optional[ApiClient] = None, logging_config: Optional[LoggingConfiguration] = None):
        """
        Initialize XOTP API Client

        Args:
            base_url: The base URL for the XOTP API
            tla: The TLA (Three Letter Acronym) parameter
            token_provider: Optional async token provider function that returns JWT tokens
            api_client: Optional pre-configured API client
            logging_config: Optional logging configuration
        """
        self.base_url = base_url
        self.tla = tla
        self.token_provider = token_provider
        
        if api_client is None:
            configuration = Configuration()
            configuration.host = base_url
            api_client = ApiClient(configuration)
        
        self.api_client = api_client
        
        # Create response normalizer
        self.response_normalizer = ResponseNormalizer(tla)
        
        # Apply response normalization
        self._apply_response_normalization()
        
        # Apply logging middleware if configured
        if logging_config:
            self.logging_middleware = LoggingMiddleware(logging_config)
            self.logging_middleware.apply_to_client(self.api_client)
        
        # Create the API instance
        self.api = XotpApi(api_client)

    def _apply_response_normalization(self):
        """Apply response normalization by patching API client methods"""
        # Store original methods
        original_param_serialize = self.api_client.param_serialize
        original_deserialize = self.api_client.deserialize
        original_call_api = self.api_client.call_api
        
        # Keep track of request context for response normalization
        request_context = {
            "url": None,
            "method": None,
            "status_code": None        }
        
        # Patch call_api to capture the status code
        @wraps(original_call_api)
        def patched_call_api(resource_path, method, *args, **kwargs):
            response = original_call_api(resource_path, method, *args, **kwargs)
            if hasattr(response, "status") and response.status is not None:
                request_context["status_code"] = response.status
            return response
        
        # Completely replace param_serialize to ensure we get access to the body parameter
        @wraps(original_param_serialize)
        def patched_param_serialize(
            method,
            resource_path,
            path_params=None,
            query_params=None,
            header_params=None,
            body=None,
            post_params=None,
            files=None,
            auth_settings=None,
            collection_formats=None,
            _host=None,
            _request_auth=None
        ):
            # Extract the full URL
            host = _host or self.api_client.configuration.host
            url = host + resource_path
            
            # Store request context for response normalization
            request_context["url"] = url
            request_context["method"] = method
            
            # Apply request transformation - now we have direct access to the body parameter
            modified_url, modified_method, modified_body = self.response_normalizer.pre_process_request(
                url, method, body
            )
            
            # Update parameters if URL changed
            if modified_url != url:
                # Extract resource path from modified URL
                if host in modified_url:
                    resource_path = modified_url[len(host):]
                else:
                    resource_path = modified_url
            
            # Update method and body
            method = modified_method
            if modified_body is not None:
                body = modified_body
            
            # Call original method with potentially modified arguments
            return original_param_serialize(
                method, 
                resource_path, 
                path_params=path_params,
                query_params=query_params,
                header_params=header_params,
                body=body,
                post_params=post_params,
                files=files,
                auth_settings=auth_settings,
                collection_formats=collection_formats,
                _host=_host,
                _request_auth=_request_auth
            )
        
        # Patch deserialize to normalize JSON before deserialization
        @wraps(original_deserialize)
        def patched_deserialize(response_text, response_type):
            try:
                # First, normalize enum values in the raw response text
                response_text = self.response_normalizer._normalize_enums_in_raw_response(response_text, response_type)
                data = json.loads(response_text)
                
                # Get status code from request context
                status_code = request_context.get("status_code")
                
                # Apply response normalization passing the status code
                normalized_data = self.response_normalizer.post_process_response(data, status_code)
                normalized_response_text = json.dumps(normalized_data)
                return original_deserialize(normalized_response_text, response_type)
            except (ValueError, TypeError, json.JSONDecodeError) as e:
                logger.error(f"Error normalizing response: {str(e)}")
                logger.error(f"Response text: {response_text}")
                return None
        
        # Replace the original methods with patched versions
        self.api_client.call_api = patched_call_api
        self.api_client.param_serialize = patched_param_serialize
        self.api_client.deserialize = patched_deserialize

    async def _add_auth_header(self, **kwargs):
        """Add authorization header if token provider is available"""
        if self.token_provider:
            headers = kwargs.get('_headers', {})
            if headers is None:
                headers = {}
            
            # Get fresh token for each request
            token = await self.token_provider()
            headers["Authorization"] = f"Bearer {token}"
            kwargs['_headers'] = headers
        
        return kwargs

    async def account_inquiry(self, account_inquiry_request: Annotated[Optional[AccountInquiryRequest], Field(description = "Create a new profile")] = None) -> AccountInquiryResponse:
        """
        Account Inquiry
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.account_inquiry(self.tla, account_inquiry_request, **kwargs)

    async def cnv_calculation(self, payment_request: Annotated[PaymentRequest, Field(description = "Request body")]) -> PaymentResponse:
        """
        Cnv Calculation
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.cnv_calculation(self.tla, payment_request, **kwargs)

    async def create_autopay(self, autopay_request: Annotated[AutopayRequest, Field(description = "Request body")]) -> AutopayResponse:
        """
        Create Autopay
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.create_autopay(self.tla, autopay_request, **kwargs)

    async def create_profile(self, profile_request: Annotated[ProfileRequest, Field(description = "Create a new profile")]) -> ProfileResponse:
        """
        Create Profile
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.create_profile(self.tla, profile_request, **kwargs)

    async def create_user(self, user_request: Annotated[UserRequest, Field(description = "Request body")]) -> UserResponse:
        """
        Create User
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.create_user(self.tla, user_request, **kwargs)

    async def delete_autopay(self, reference_number: Annotated[StrictStr, Field(description = "String for schedule reference number")]) -> AutopayResponse:
        """
        Delete Autopay
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.delete_autopay(self.tla, reference_number, **kwargs)

    async def delete_profile(self, token: Annotated[StrictStr, Field(description = "profile token that was provided when profile was created")]) -> ProfileResponse:
        """
        Delete Profile
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.delete_profile(self.tla, token, **kwargs)

    async def delete_user(self, user_delete_request: Annotated[UserDeleteRequest, Field(description = "Request body")]) -> UserResponse:
        """
        Delete User
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.delete_user(self.tla, user_delete_request, **kwargs)

    async def fetch_last_payment(self, payment_search_request: Annotated[PaymentSearchRequest, Field(description = "Request body")]) -> PaymentSearchResponse:
        """
        Fetch Last Payment
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.fetch_last_payment(self.tla, payment_search_request, **kwargs)

    async def get_account_info_by_account_number(self, account_number: Annotated[StrictStr, Field(description = "String that points to linked account number")]) -> ListAccountInfoResponse:
        """
        Get Account Info By Account Number
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.get_account_info_by_account_number(self.tla, account_number, **kwargs)

    async def get_account_info_by_email(self, email: Annotated[StrictStr, Field(description = "String that points to linked email")]) -> ListAccountInfoResponse:
        """
        Get Account Info By Email
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.get_account_info_by_email(self.tla, email, **kwargs)

    async def get_autopay(self, reference_number: Annotated[StrictStr, Field(description = "String for schedule reference number")]) -> AutopayFindResponse:
        """
        Get Autopay
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.get_autopay(self.tla, reference_number, **kwargs)

    async def get_bank_info(self, routing_number: Annotated[StrictStr, Field(description = "String that points routing number")]) -> BankInfoResponse:
        """
        Get Bank Info
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.get_bank_info(self.tla, routing_number, **kwargs)

    async def get_payment_history(self, payment_search_request: Annotated[PaymentSearchRequest, Field(description = "Request body")]) -> PaymentHistoryResponse:
        """
        Get Payment History
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.get_payment_history(self.tla, payment_search_request, **kwargs)

    async def get_payment_ref(self, reference_number: Annotated[StrictStr, Field(description = "String that points to reference number")]) -> PaymentRefResponse:
        """
        Get Payment Ref
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.get_payment_ref(self.tla, reference_number, **kwargs)

    async def get_profile(self, token: Annotated[StrictStr, Field(description = "profile token that was provided when profile was created")]) -> ProfileResponse:
        """
        Get Profile
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.get_profile(self.tla, token, **kwargs)

    async def get_profiles(self, login_id: Annotated[str, Field(min_length = 1, strict=True, max_length=256, description="profile email that was provided when profile was created")]) -> ListProfilesResponse:
        """
        Get Profiles
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.get_profiles(self.tla, login_id, **kwargs)

    async def get_user(self, login_id: Annotated[StrictStr, Field(description = "String that points to login id")], include_contact_info: Annotated[Optional[StrictBool], Field(description = "To include contact info in response")] = None) -> UserFindResponse:
        """
        Get User
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.get_user(self.tla, login_id, include_contact_info, **kwargs)

    async def list_auto_pay(self, autopay_search_request: Annotated[AutopaySearchRequest, Field(description = "Request body")]) -> AutopayListResponse:
        """
        List Auto Pay
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.list_auto_pay(self.tla, autopay_search_request, **kwargs)

    async def make_payment(self, make_payment: Annotated[Optional[MakePayment], Field(description = "Request body")] = None) -> PaymentResponse:
        """
        Make Payment
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.make_payment(self.tla, make_payment, **kwargs)

    async def refund_payment(self, payment_request: Annotated[PaymentRequest, Field(description = "Request body")]) -> PaymentResponse:
        """
        Refund Payment
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.refund_payment(self.tla, payment_request, **kwargs)

    async def resend_email_confirmation(self, resend_email_request: Annotated[ResendEmailRequest, Field(description = "Resend an Email confirmation, you can pass account-number,refreence-number,email to fetch receipt")]) -> ResendEmailResponse:
        """
        Resend Email Confirmation
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.resend_email_confirmation(self.tla, resend_email_request, **kwargs)

    async def stage_autopay(self, payment_request: Annotated[PaymentRequest, Field(description = "Request body")]) -> StagePaymentResponse:
        """
        Stage Autopay
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.stage_autopay(self.tla, payment_request, **kwargs)

    async def stage_payment(self, payment_request: Annotated[PaymentRequest, Field(description = "Request body")]) -> StagePaymentResponse:
        """
        Stage Payment
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.stage_payment(self.tla, payment_request, **kwargs)

    async def update_autopay(self, reference_number: Annotated[StrictStr, Field(description = "String for schedule reference number")], autopay_request: Annotated[AutopayRequest, Field(description = "Update an Autopay")]) -> AutopayResponse:
        """
        Update Autopay
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.update_autopay(self.tla, reference_number, autopay_request, **kwargs)

    async def update_profile(self, token: Annotated[StrictStr, Field(description = "profile token that was provided when profile was created")], profile_update_request: Annotated[Optional[ProfileUpdateRequest], Field(description = "Request body")] = None) -> ProfileResponse:
        """
        Update Profile
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.update_profile(self.tla, token, profile_update_request, **kwargs)

    async def update_user(self, user_update_request: Annotated[UserUpdateRequest, Field(description = "Request body")]) -> UserResponse:
        """
        Update User
        """
        kwargs = await self._add_auth_header(_headers={})
        return self.api.update_user(self.tla, user_update_request, **kwargs)
