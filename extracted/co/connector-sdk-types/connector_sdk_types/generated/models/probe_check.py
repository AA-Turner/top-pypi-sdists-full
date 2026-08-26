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
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from connector_sdk_types.generated.models.error import Error
from connector_sdk_types.generated.models.probe_check_name import ProbeCheckName
from connector_sdk_types.generated.models.probe_check_source import ProbeCheckSource
from connector_sdk_types.generated.models.probe_check_status import ProbeCheckStatus
from connector_sdk_types.generated.models.probe_custom_attribute_result import (
    ProbeCustomAttributeResult,
)
from connector_sdk_types.generated.models.probe_entitlement_type_result import (
    ProbeEntitlementTypeResult,
)
from typing import Optional, Set
from typing_extensions import Self
from connector_sdk_types.generated.models.probe_sample_account import ProbeSampleAccount
from connector_sdk_types.generated.models.probe_sample_association import ProbeSampleAssociation
from connector_sdk_types.generated.models.probe_sample_entitlement import ProbeSampleEntitlement


class ProbeCheck(BaseModel):
    """
    The result of a single check within a probe run.
    """

    check: ProbeCheckName = Field(description="Which check this result describes.")
    status: ProbeCheckStatus = Field(description="The outcome of this check.")
    source: ProbeCheckSource = Field(
        description="Whether the connector produced this result itself or the SDK derived it."
    )
    capability: Optional[StrictStr] = Field(
        default=None,
        description="The standard capability that produced this result, e.g. `list_accounts`. Absent when a connector implemented the check natively without mapping it to a single capability.",
    )
    observed_count: StrictInt = Field(
        description="How many records this check observed. At least `samples.length` - a check may count more records than it returns evidence for."
    )
    message: Optional[StrictStr] = Field(
        default=None,
        description='A short, consumer-facing summary of what happened, e.g. "Fetched 1 account (jane',
    )
    error: Optional[Error] = Field(
        default=None,
        description="The error that made this check fail, in the same shape as any other connector error, so callers can reuse their existing error surfaces.",
    )
    samples: List[ProbeSampleAccount | ProbeSampleEntitlement | ProbeSampleAssociation] = Field(
        description="Redacted evidence of what the check fetched, one entry per record. A check that `passed` carries at least one; there is no upper bound, so a consumer can show several accounts, several entitlements per type, or associations across several accounts."
    )
    entitlement_types: Optional[List[ProbeEntitlementTypeResult]] = Field(
        default=None,
        description="Per-entitlement-type breakdown, against the entitlement types the connector declares. Only present on the `entitlements` check.",
    )
    custom_attributes: Optional[List[ProbeCustomAttributeResult]] = Field(
        default=None,
        description="Per-attribute breakdown, against the account attributes the connector's schema declares. Only present on the `accounts` check, and only when the connector implements `list_custom_attributes_schema`.  An attribute no sampled account carries a value for is reported `not_found`, which degrades the run to `partial`: the schema exists but nothing populates it, so custom attributes would sync empty.",
    )
    duration_ms: Optional[StrictInt] = Field(
        default=None, description="Wall-clock duration of this check, in milliseconds."
    )
    __properties: ClassVar[List[str]] = [
        "check",
        "status",
        "source",
        "capability",
        "observed_count",
        "message",
        "error",
        "samples",
        "entitlement_types",
        "custom_attributes",
        "duration_ms",
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
        """Create an instance of ProbeCheck from a JSON string"""
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
        if self.error:
            _dict["error"] = self.error.to_dict()
        _items = []
        if self.samples:
            for _item_samples in self.samples:
                if _item_samples:
                    _items.append(_item_samples.to_dict())
            _dict["samples"] = _items
        _items = []
        if self.entitlement_types:
            for _item_entitlement_types in self.entitlement_types:
                if _item_entitlement_types:
                    _items.append(_item_entitlement_types.to_dict())
            _dict["entitlement_types"] = _items
        _items = []
        if self.custom_attributes:
            for _item_custom_attributes in self.custom_attributes:
                if _item_custom_attributes:
                    _items.append(_item_custom_attributes.to_dict())
            _dict["custom_attributes"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProbeCheck from a dict"""
        if obj is None:
            return None
        if not isinstance(obj, dict):
            return cls.model_validate(obj)
        _obj = cls.model_validate(
            {
                "check": obj.get("check"),
                "status": obj.get("status"),
                "source": obj.get("source"),
                "capability": obj.get("capability"),
                "observed_count": obj.get("observed_count"),
                "message": obj.get("message"),
                "error": Error.from_dict(obj["error"]) if obj.get("error") is not None else None,
                "samples": obj.get("samples"),
                "entitlement_types": [
                    ProbeEntitlementTypeResult.from_dict(_item)
                    for _item in obj["entitlement_types"]
                ]
                if obj.get("entitlement_types") is not None
                else None,
                "custom_attributes": [
                    ProbeCustomAttributeResult.from_dict(_item)
                    for _item in obj["custom_attributes"]
                ]
                if obj.get("custom_attributes") is not None
                else None,
                "duration_ms": obj.get("duration_ms"),
            }
        )
        return _obj
