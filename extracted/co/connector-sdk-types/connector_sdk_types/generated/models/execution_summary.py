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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from connector_sdk_types.generated.models.effect import Effect
from connector_sdk_types.generated.models.error import Error
from typing import Optional, Set
from typing_extensions import Self
from connector_sdk_types.generated.models.created_effect import CreatedEffect
from connector_sdk_types.generated.models.deleted_effect import DeletedEffect
from connector_sdk_types.generated.models.noop_effect import NoopEffect
from connector_sdk_types.generated.models.updated_effect import UpdatedEffect


class ExecutionSummary(BaseModel):
    """
    Summary of how a write operation executed from the connector's perspective.  This model provides metadata about the execution of write operations (create, update, delete, etc.), including what effect the operation had, whether it's safe to retry, and any non-fatal errors that occurred during execution.
    """

    effect: CreatedEffect | UpdatedEffect | DeletedEffect | NoopEffect = Field(
        description="The actual effect that occurred in the target system as a result of this operation.  This is a discriminated union that indicates what change (if any) was made: - CreatedEffect: a new record was created - UpdatedEffect: an existing record was updated - DeletedEffect: an existing record was deleted - NoopEffect: no operation was needed (includes required 'reason' field)  The 'kind' field acts as the discriminator to determine which effect type is present."
    )
    request_fingerprint: StrictStr = Field(
        description="A unique fingerprint that identifies this specific execution request.  This value can be used to deduplicate requests, track operation history, and correlate related operations. It should be stable for the same input parameters."
    )
    is_idempotent: StrictBool = Field(
        description="Indicates whether this operation is idempotent and safe to retry with the same request fingerprint.  When true, executing this operation multiple times with the same request fingerprint will produce the same result without causing unintended side effects. This is useful for retry logic and ensuring operation safety."
    )
    description: Optional[StrictStr] = Field(
        default=None,
        description="Optional human-readable description of the execution result.  Provides additional context or details about what happened during execution that may be useful for debugging or user-facing messages. When `effect` is `noop`, this can provide additional details beyond what's captured in `effect_reason`.",
    )
    caught_errors: Optional[List[Error]] = Field(
        default=None,
        description="Optional list of non-fatal errors that occurred during execution.  These are errors that were caught and handled gracefully during the operation. The operation completed successfully despite these errors, but they may contain important information for the end user (e.g., warnings about partial failures, deprecation notices, or validation issues that were automatically corrected).",
    )
    __properties: ClassVar[List[str]] = [
        "effect",
        "request_fingerprint",
        "is_idempotent",
        "description",
        "caught_errors",
    ]
    model_config = ConfigDict(
        populate_by_name=True, validate_assignment=True, protected_namespaces=()
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of ExecutionSummary from a JSON string"""
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
        if self.effect:
            _dict["effect"] = self.effect.to_dict()
        _items = []
        if self.caught_errors:
            for _item_caught_errors in self.caught_errors:
                if _item_caught_errors:
                    _items.append(_item_caught_errors.to_dict())
            _dict["caught_errors"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ExecutionSummary from a dict"""
        if obj is None:
            return None
        if not isinstance(obj, dict):
            return cls.model_validate(obj)
        _obj = cls.model_validate(
            {
                "effect": Effect.from_dict(obj["effect"])
                if obj.get("effect") is not None
                else None,
                "request_fingerprint": obj.get("request_fingerprint"),
                "is_idempotent": obj.get("is_idempotent"),
                "description": obj.get("description"),
                "caught_errors": [Error.from_dict(_item) for _item in obj["caught_errors"]]
                if obj.get("caught_errors") is not None
                else None,
            }
        )
        return _obj
