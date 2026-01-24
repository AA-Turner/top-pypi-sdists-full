"""
Lumos Connectors

# The Lumos Connector API  ## Introduction The Lumos Connector API is a standardized interface for Identity and Access Management (IAM) operations across various third-party systems. It enables seamless integration between Lumos and external applications by providing a consistent set of operations called **capabilities**.  Each integration (referred to as a "connector") implements these capabilities to work with different third-party API providers, focusing primarily on: - User access management - License and cost tracking - User activity monitoring  ## Core Components  ### Connectors A connector is a specialized library that acts as a bridge between Lumos and third-party applications. It handles: - Translation of Lumos requests into app-specific API calls - Conversion of app-specific responses into standardized Lumos formats - Authentication and authorization flows - Data format transformations  ### Capabilities Capabilities are standardized operations that each connector can implement. They provide: - Consistent interfaces across different connectors - Predictable behavior patterns - Standardized error handling - Unified data structures  ## Data Model  ### Accounts Accounts represent individual users or service accounts within a system.  They serve as the primary entities for access management and support lifecycle operations such as creation, activation, deactivation, and deletion.  Accounts can be associated with multiple entitlements and are typically identified by a unique account ID within the system.  ### Entitlements Entitlements represent a permission or capability that can be granted to user accounts, such as a license or access level.  They define specific permissions, access rights, or memberships and are always associated with a resource, which may be global or specific.  Entitlements are categorized by `entitlement_type` (e.g., licenses, roles, permissions, group memberships) and have defined constraints for minimum and maximum assignments.  The naming of entitlements may vary, such as using "membership" for group associations.  ### Resources Resources represent entities within an application that can be accessed or managed.  They are identified by a unique `resource_type` within each app and include a global resource (represented by an empty string) for top-level entities.  Resources can represent hierarchical structures, such as Workspaces containing Users and Groups, and serve as the context for entitlement assignments.  The usage of Resource IDs depends on the specific hierarchy, with an empty string for global resources and specific IDs (e.g., Workspace ID) for nested resources.  ### Associations Associations define relationships from accounts to entitlements (which are resource specific).  They follow a hierarchical structure of Account -> Entitlement -> Resource, with no direct account-to-resource associations allowed.  Associations enable flexible access control models.  Note: The specific structure and use of resources and entitlements may vary depending on the integrated system's architecture and access model.  ## How to Use This API  1. Discover available connectors 2. Learn about a specific connector 3. Configure a connector 4. (optional) Authenticate with OAuth 5. Read data from the connected tenant 6. Write (update) data in the connected tenant  ## Authenticating with a Connector  ### Authentication Methods Connectors support two main authentication categories:  ### 1. Shared Secret Authentication - API Keys / Tokens - Basic Authentication (username/password)  ### 2. OAuth-based Authentication The API supports two OAuth flow types:  #### Authorization Code Flow (3-legged OAuth) Requires a multi-step flow:  1. **Authorization URL** - Call `get_authorization_url` to start the OAuth flow - Redirect user to the returned authorization URL  2. **Handle Callback** - Process the OAuth callback using `handle_authorization_callback` - Receive access and refresh tokens  3. **Token Management** - Use `refresh_access_token` to maintain valid access - Store refresh tokens securely  #### Client Credentials Flow (2-legged OAuth) Suitable for machine-to-machine authentication:  1. **Direct Token Request** - Call `handle_client_credentials_request` with client credentials - Receive access token (and optionally refresh token)  2. **Token Management** - Use `refresh_access_token` to maintain valid access (if refresh tokens are supported) - Store tokens securely  The flow type is configured in the connector settings and determines which capabilities are available. Both flows support customizable authentication methods (Basic Auth or request body) and different request formats (JSON, form data, or query parameters).  ### Validation After obtaining credentials: 1. Call `validate_credentials` to verify authentication 2. Retrieve the unique tenant ID for the authenticated organization  ### Authentication Schema Each connector's `info.authentication_schema` defines: - Required credential fields - Field formats and constraints - OAuth scopes (if applicable) ## Pagination  Lumos connectors implement a standardized pagination mechanism to handle large datasets efficiently. The pagination system uses opaque tokens to maintain state across requests.  ### How Pagination Works  1. **Request Format** Every request can include an optional `page` parameter: ```typescript    {      "page": {        "token": string,  // Optional: opaque token from previous response        "size": number    // Optional: number of items per page      }    }    ```  2. **Response Format** Paginated responses include a `page` field: ```typescript    {      "response": T[],    // Array of items      "page": {        "token": string,  // Token for the next page        "size": number    // Items per page      }    }    ```  ### Using Pagination  1. **Initial Request** - Make the first request without a page token - Optionally specify a page size  2. **Subsequent Requests** - Include the `token` from the previous response - Keep the same page size for consistency  3. **End of Data** - When there's no more data, the response won't include a page token  ### Example Flow ```typescript // First request POST /connectors/pagerduty/list_accounts {   "page": { "size": 100 } }  // Response {   "response": [...],   "page": {     "token": "eyJwYWdlIjogMn0=",     "size": 100   } }  // Next request POST /connectors/pagerduty/list_accounts {   "page": {     "token": "eyJwYWdlIjogMn0=",     "size": 100   } } ```  ### Implementation Notes  - Page tokens are opaque and should be treated as black boxes - Tokens may encode various information (page numbers, cursors, etc.) - The same page size should be used throughout a pagination sequence - Invalid or expired tokens will result in an error response

The version of the OpenAPI document: 0.0.0
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""

from __future__ import annotations
import pprint
import re
import json
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self
from connector_sdk_types.oai.fingerprint import request_fingerprint


class ListUpdatedAccounts(BaseModel):
    """
    Request parameters for listing updated accounts with delta query support.  This model extends the Delta model to provide both traditional date-based filtering and efficient cursor-based incremental synchronization.  ## Parameter Priority  When both `cursor` and `since` are provided: - The `cursor` takes precedence for delta-based synchronization - The `since` is ignored in favor of the cursor's timestamp  ## Best Practices  - Use `cursor` for ongoing synchronization to minimize data transfer - Use `since` for initial syncs or when resuming after a long gap - Include only necessary `custom_attributes` to optimize response size - Store the returned `cursor` persistently for reliable sync state  ## Error Scenarios  - **Invalid Cursor**: May return an error or fall back to full data fetch - **Expired Cursor**: Connector may return all data since the cursor's timestamp - **Unsupported Attributes**: Custom attributes not available in the connector may be ignored or cause errors depending on the connector implementation
    """

    since: Optional[datetime] = Field(
        default=None,
        description='Only include accounts updated since this specific date and time.  This parameter defines the cutoff point for account updates. Only accounts that have been modified since this timestamp will be included in the response.  ## Format Requirements  Must be a valid ISO 8601 datetime string with timezone information: - **UTC**: "2024-01-15T10:30:00Z" - **With Offset**: "2024-01-15T10:30:00+05:00" - **With Timezone**: "2024-01-15T10:30:00-08:00"  ## Connector Limitations  Each connector may have different limitations on how far back in time they can reliably track updates: - Some connectors may limit to 30 days - Others may support up to 1 year - Enterprise connectors might support longer periods  ## Usage Guidelines  - Use for initial synchronization or when resuming after a long gap - Consider the connector\'s data retention policies when setting this value - For ongoing syncs, prefer using `cursor` instead',
    )
    cursor: Optional[StrictStr] = Field(
        default=None,
        description="Cursor token for delta synchronization.  This token represents a point in time and should be included in subsequent requests to receive only the changes that occurred since that point.  - **First request**: Omit this parameter to get all available data - **Subsequent requests**: Include the `cursor` from the previous response  The cursor is typically a base64-encoded string containing timestamp and other metadata needed for the delta synchronization.",
    )
    custom_attributes: Optional[List[StrictStr]] = Field(
        default=None,
        description="Optional array of custom attribute names to include in account data.  This parameter allows you to specify which additional account attributes should be included in the response beyond the standard account information.  ## Attribute Availability  Available attributes vary by connector and may include: - **User Profile**: department, title, manager, location - **Organizational**: cost_center, employee_id, hire_date - **Custom Fields**: custom_1, custom_2, custom_role - **System-Specific**: salesforce_user_type, okta_group_membership  ## Performance Considerations  - Requesting many custom attributes may increase response time - Some attributes may require additional API calls by the connector - Unsupported attributes are typically ignored rather than causing errors  ## Best Practices  - Only request attributes you actually need - Test with small attribute lists first - Consider the connector's rate limits when requesting many attributes - Cache attribute availability information when possible",
    )
    __properties: ClassVar[List[str]] = ["since", "cursor", "custom_attributes"]
    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
        json_schema_extra={"x-capability-level": "read"},
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of ListUpdatedAccounts from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([])
        _dict = self.model_dump(by_alias=True, exclude=excluded_fields, exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ListUpdatedAccounts from a dict"""
        if obj is None:
            return None
        if not isinstance(obj, dict):
            return cls.model_validate(obj)
        _obj = cls.model_validate(
            {
                "since": obj.get("since"),
                "cursor": obj.get("cursor"),
                "custom_attributes": obj.get("custom_attributes"),
            }
        )
        return _obj

    def fingerprint(self) -> str:
        return request_fingerprint(self)
