# coding: utf-8

"""
    Lumos Connectors

    # The Lumos Connector API  ## Introduction The Lumos Connector API is a standardized interface for Identity and Access Management (IAM) operations across various third-party systems. It enables seamless integration between Lumos and external applications by providing a consistent set of operations called **capabilities**.  Each integration (referred to as a \"connector\") implements these capabilities to work with different third-party API providers, focusing primarily on: - User access management - License and cost tracking - User activity monitoring  ## Core Components  ### Connectors A connector is a specialized library that acts as a bridge between Lumos and third-party applications. It handles: - Translation of Lumos requests into app-specific API calls - Conversion of app-specific responses into standardized Lumos formats - Authentication and authorization flows - Data format transformations  ### Capabilities Capabilities are standardized operations that each connector can implement. They provide: - Consistent interfaces across different connectors - Predictable behavior patterns - Standardized error handling - Unified data structures  ## Data Model  ### Accounts Accounts represent individual users or service accounts within a system.  They serve as the primary entities for access management and support lifecycle operations such as creation, activation, deactivation, and deletion.  Accounts can be associated with multiple entitlements and are typically identified by a unique account ID within the system.  ### Entitlements Entitlements represent a permission or capability that can be granted to user accounts, such as a license or access level.  They define specific permissions, access rights, or memberships and are always associated with a resource, which may be global or specific.  Entitlements are categorized by `entitlement_type` (e.g., licenses, roles, permissions, group memberships) and have defined constraints for minimum and maximum assignments.  The naming of entitlements may vary, such as using \"membership\" for group associations.  ### Resources Resources represent entities within an application that can be accessed or managed.  They are identified by a unique `resource_type` within each app and include a global resource (represented by an empty string) for top-level entities.  Resources can represent hierarchical structures, such as Workspaces containing Users and Groups, and serve as the context for entitlement assignments.  The usage of Resource IDs depends on the specific hierarchy, with an empty string for global resources and specific IDs (e.g., Workspace ID) for nested resources.  ### Associations Associations define relationships from accounts to entitlements (which are resource specific).  They follow a hierarchical structure of Account -> Entitlement -> Resource, with no direct account-to-resource associations allowed.  Associations enable flexible access control models.  Note: The specific structure and use of resources and entitlements may vary depending on the integrated system's architecture and access model.  ## How to Use This API  1. Discover available connectors 2. Learn about a specific connector 3. Configure a connector 4. (optional) Authenticate with OAuth 5. Read data from the connected tenant 6. Write (update) data in the connected tenant  ## Authenticating with a Connector  ### Authentication Methods Connectors support two main authentication categories:  ### 1. Shared Secret Authentication - API Keys / Tokens - Basic Authentication (username/password)  ### 2. OAuth-based Authentication The API supports two OAuth flow types:  #### Authorization Code Flow (3-legged OAuth) Requires a multi-step flow:  1. **Authorization URL** - Call `get_authorization_url` to start the OAuth flow - Redirect user to the returned authorization URL  2. **Handle Callback** - Process the OAuth callback using `handle_authorization_callback` - Receive access and refresh tokens  3. **Token Management** - Use `refresh_access_token` to maintain valid access - Store refresh tokens securely  #### Client Credentials Flow (2-legged OAuth) Suitable for machine-to-machine authentication:  1. **Direct Token Request** - Call `handle_client_credentials_request` with client credentials - Receive access token (and optionally refresh token)  2. **Token Management** - Use `refresh_access_token` to maintain valid access (if refresh tokens are supported) - Store tokens securely  The flow type is configured in the connector settings and determines which capabilities are available. Both flows support customizable authentication methods (Basic Auth or request body) and different request formats (JSON, form data, or query parameters).  ### Validation After obtaining credentials: 1. Call `validate_credentials` to verify authentication 2. Retrieve the unique tenant ID for the authenticated organization  ### Authentication Schema Each connector's `info.authentication_schema` defines: - Required credential fields - Field formats and constraints - OAuth scopes (if applicable) ## Pagination  Lumos connectors implement a standardized pagination mechanism to handle large datasets efficiently. The pagination system uses opaque tokens to maintain state across requests.  ### How Pagination Works  1. **Request Format** Every request can include an optional `page` parameter: ```typescript    {      \"page\": {        \"token\": string,  // Optional: opaque token from previous response        \"size\": number    // Optional: number of items per page      }    }    ```  2. **Response Format** Paginated responses include a `page` field: ```typescript    {      \"response\": T[],    // Array of items      \"page\": {        \"token\": string,  // Token for the next page        \"size\": number    // Items per page      }    }    ```  ### Using Pagination  1. **Initial Request** - Make the first request without a page token - Optionally specify a page size  2. **Subsequent Requests** - Include the `token` from the previous response - Keep the same page size for consistency  3. **End of Data** - When there's no more data, the response won't include a page token  ### Example Flow ```typescript // First request POST /connectors/pagerduty/list_accounts {   \"page\": { \"size\": 100 } }  // Response {   \"response\": [...],   \"page\": {     \"token\": \"eyJwYWdlIjogMn0=\",     \"size\": 100   } }  // Next request POST /connectors/pagerduty/list_accounts {   \"page\": {     \"token\": \"eyJwYWdlIjogMn0=\",     \"size\": 100   } } ```  ### Implementation Notes  - Page tokens are opaque and should be treated as black boxes - Tokens may encode various information (page numbers, cursors, etc.) - The same page size should be used throughout a pagination sequence - Invalid or expired tokens will result in an error response

    The version of the OpenAPI document: 0.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from connector_sdk_types.generated.models.entitlement_type import EntitlementType
from connector_sdk_types.generated.models.resource_type import ResourceType
from typing import Optional, Set
from typing_extensions import Self

class OpenAPISpecificationInfo(BaseModel):
    """
    OpenAPISpecificationInfo
    """ # noqa: E501
    title: StrictStr
    description: StrictStr
    version: StrictStr
    x_app_id: StrictStr = Field(alias="x-app-id")
    x_app_logo_url: StrictStr = Field(alias="x-app-logo-url")
    x_app_vendor_domain: StrictStr = Field(alias="x-app-vendor-domain")
    x_entitlement_types: List[EntitlementType] = Field(alias="x-entitlement-types")
    x_resource_types: List[ResourceType] = Field(alias="x-resource-types")
    x_categories: Dict[str, Any] = Field(alias="x-categories")
    x_oauth_settings: Optional[Dict[str, Any]] = Field(default=None, alias="x-oauth-settings")
    x_capabilities: List[StrictStr] = Field(alias="x-capabilities")
    x_multi_credential: StrictBool = Field(alias="x-multi-credential")
    x_allowed_credentials: List[List[StrictStr]] = Field(alias="x-allowed-credentials")
    __properties: ClassVar[List[str]] = ["title", "description", "version", "x-app-id", "x-app-logo-url", "x-app-vendor-domain", "x-entitlement-types", "x-resource-types", "x-categories", "x-oauth-settings", "x-capabilities", "x-multi-credential", "x-allowed-credentials"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of OpenAPISpecificationInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in x_entitlement_types (list)
        _items = []
        if self.x_entitlement_types:
            for _item_x_entitlement_types in self.x_entitlement_types:
                if _item_x_entitlement_types:
                    _items.append(_item_x_entitlement_types.to_dict())
            _dict['x-entitlement-types'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in x_resource_types (list)
        _items = []
        if self.x_resource_types:
            for _item_x_resource_types in self.x_resource_types:
                if _item_x_resource_types:
                    _items.append(_item_x_resource_types.to_dict())
            _dict['x-resource-types'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of OpenAPISpecificationInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "title": obj.get("title"),
            "description": obj.get("description"),
            "version": obj.get("version"),
            "x-app-id": obj.get("x-app-id"),
            "x-app-logo-url": obj.get("x-app-logo-url"),
            "x-app-vendor-domain": obj.get("x-app-vendor-domain"),
            "x-entitlement-types": [EntitlementType.from_dict(_item) for _item in obj["x-entitlement-types"]] if obj.get("x-entitlement-types") is not None else None,
            "x-resource-types": [ResourceType.from_dict(_item) for _item in obj["x-resource-types"]] if obj.get("x-resource-types") is not None else None,
            "x-categories": obj.get("x-categories"),
            "x-oauth-settings": obj.get("x-oauth-settings"),
            "x-capabilities": obj.get("x-capabilities"),
            "x-multi-credential": obj.get("x-multi-credential"),
            "x-allowed-credentials": obj.get("x-allowed-credentials")
        })
        return _obj


