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
from connector_sdk_types.generated.models.ticket_comment import TicketComment
from connector_sdk_types.generated.models.ticket_event_actor import TicketEventActor
from connector_sdk_types.generated.models.ticket_event_kind import TicketEventKind
from connector_sdk_types.generated.models.ticket_status_change import TicketStatusChange
from typing import Optional, Set
from typing_extensions import Self


class TicketEvent(BaseModel):
    """
    One change to a ticket, reported by the ticketing system. `kind` says which change it is, and the event carries exactly the payload for that kind: `status_change` for `status_changed`, `comment` for `comment_added`.
    """

    kind: TicketEventKind = Field(
        description="What kind of change this is. Decides which payload field is set."
    )
    ticket_id: StrictStr = Field(
        description="The ticket that changed, the same id `create_ticket` returned.",
        json_schema_extra={"x-semantic": "ticket-id"},
    )
    actor: Optional[TicketEventActor] = Field(
        default=None, description="The person who made the change, if known."
    )
    occurred_at: datetime = Field(description="When the change happened.")
    status_change: Optional[TicketStatusChange] = Field(
        default=None,
        description="The status change. Set when `kind` is `status_changed`, and only then.",
    )
    comment: Optional[TicketComment] = Field(
        default=None, description="The comment. Set when `kind` is `comment_added`, and only then."
    )
    __properties: ClassVar[List[str]] = [
        "kind",
        "ticket_id",
        "actor",
        "occurred_at",
        "status_change",
        "comment",
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
        """Create an instance of TicketEvent from a JSON string"""
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
        if self.actor:
            _dict["actor"] = self.actor.to_dict()
        if self.status_change:
            _dict["status_change"] = self.status_change.to_dict()
        if self.comment:
            _dict["comment"] = self.comment.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TicketEvent from a dict"""
        if obj is None:
            return None
        if not isinstance(obj, dict):
            return cls.model_validate(obj)
        _obj = cls.model_validate(
            {
                "kind": obj.get("kind"),
                "ticket_id": obj.get("ticket_id"),
                "actor": TicketEventActor.from_dict(obj["actor"])
                if obj.get("actor") is not None
                else None,
                "occurred_at": obj.get("occurred_at"),
                "status_change": TicketStatusChange.from_dict(obj["status_change"])
                if obj.get("status_change") is not None
                else None,
                "comment": TicketComment.from_dict(obj["comment"])
                if obj.get("comment") is not None
                else None,
            }
        )
        return _obj
