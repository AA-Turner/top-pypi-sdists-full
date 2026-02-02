""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/lldp/network_policy
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
    overload,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class NetworkPolicyVoiceDict(TypedDict, total=False):
    """Nested object type for voice field."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyVoicesignalingDict(TypedDict, total=False):
    """Nested object type for voice-signaling field."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyGuestDict(TypedDict, total=False):
    """Nested object type for guest field."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyGuestvoicesignalingDict(TypedDict, total=False):
    """Nested object type for guest-voice-signaling field."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicySoftphoneDict(TypedDict, total=False):
    """Nested object type for softphone field."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyVideoconferencingDict(TypedDict, total=False):
    """Nested object type for video-conferencing field."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyStreamingvideoDict(TypedDict, total=False):
    """Nested object type for streaming-video field."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyVideosignalingDict(TypedDict, total=False):
    """Nested object type for video-signaling field."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyPayload(TypedDict, total=False):
    """Payload type for NetworkPolicy operations."""
    name: str
    comment: str
    voice: NetworkPolicyVoiceDict
    voice_signaling: NetworkPolicyVoicesignalingDict
    guest: NetworkPolicyGuestDict
    guest_voice_signaling: NetworkPolicyGuestvoicesignalingDict
    softphone: NetworkPolicySoftphoneDict
    video_conferencing: NetworkPolicyVideoconferencingDict
    streaming_video: NetworkPolicyStreamingvideoDict
    video_signaling: NetworkPolicyVideosignalingDict


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class NetworkPolicyResponse(TypedDict, total=False):
    """Response type for NetworkPolicy - use with .dict property for typed dict access."""
    name: str
    comment: str
    voice: NetworkPolicyVoiceDict
    voice_signaling: NetworkPolicyVoicesignalingDict
    guest: NetworkPolicyGuestDict
    guest_voice_signaling: NetworkPolicyGuestvoicesignalingDict
    softphone: NetworkPolicySoftphoneDict
    video_conferencing: NetworkPolicyVideoconferencingDict
    streaming_video: NetworkPolicyStreamingvideoDict
    video_signaling: NetworkPolicyVideosignalingDict


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class NetworkPolicyVoiceObject(FortiObject):
    """Nested object for voice field with attribute access."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyVoicesignalingObject(FortiObject):
    """Nested object for voice-signaling field with attribute access."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyGuestObject(FortiObject):
    """Nested object for guest field with attribute access."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyGuestvoicesignalingObject(FortiObject):
    """Nested object for guest-voice-signaling field with attribute access."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicySoftphoneObject(FortiObject):
    """Nested object for softphone field with attribute access."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyVideoconferencingObject(FortiObject):
    """Nested object for video-conferencing field with attribute access."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyStreamingvideoObject(FortiObject):
    """Nested object for streaming-video field with attribute access."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyVideosignalingObject(FortiObject):
    """Nested object for video-signaling field with attribute access."""
    status: Literal["disable", "enable"]
    tag: Literal["none", "dot1q", "dot1p"]
    vlan: int
    priority: int
    dscp: int


class NetworkPolicyObject(FortiObject):
    """Typed FortiObject for NetworkPolicy with field access."""
    name: str
    comment: str
    voice: NetworkPolicyVoiceObject
    voice_signaling: NetworkPolicyVoicesignalingObject
    guest: NetworkPolicyGuestObject
    guest_voice_signaling: NetworkPolicyGuestvoicesignalingObject
    softphone: NetworkPolicySoftphoneObject
    video_conferencing: NetworkPolicyVideoconferencingObject
    streaming_video: NetworkPolicyStreamingvideoObject
    video_signaling: NetworkPolicyVideosignalingObject


# ================================================================
# Main Endpoint Class
# ================================================================

class NetworkPolicy:
    """
    
    Endpoint: system/lldp/network_policy
    Category: cmdb
    MKey: name
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    mkey: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # CMDB with mkey - overloads for single vs list returns
    @overload
    def get(
        self,
        name: str,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> NetworkPolicyObject: ...
    
    @overload
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[NetworkPolicyObject]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: NetworkPolicyPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        voice: NetworkPolicyVoiceDict | None = ...,
        voice_signaling: NetworkPolicyVoicesignalingDict | None = ...,
        guest: NetworkPolicyGuestDict | None = ...,
        guest_voice_signaling: NetworkPolicyGuestvoicesignalingDict | None = ...,
        softphone: NetworkPolicySoftphoneDict | None = ...,
        video_conferencing: NetworkPolicyVideoconferencingDict | None = ...,
        streaming_video: NetworkPolicyStreamingvideoDict | None = ...,
        video_signaling: NetworkPolicyVideosignalingDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> NetworkPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: NetworkPolicyPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        voice: NetworkPolicyVoiceDict | None = ...,
        voice_signaling: NetworkPolicyVoicesignalingDict | None = ...,
        guest: NetworkPolicyGuestDict | None = ...,
        guest_voice_signaling: NetworkPolicyGuestvoicesignalingDict | None = ...,
        softphone: NetworkPolicySoftphoneDict | None = ...,
        video_conferencing: NetworkPolicyVideoconferencingDict | None = ...,
        streaming_video: NetworkPolicyStreamingvideoDict | None = ...,
        video_signaling: NetworkPolicyVideosignalingDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> NetworkPolicyObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: NetworkPolicyPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        voice: NetworkPolicyVoiceDict | None = ...,
        voice_signaling: NetworkPolicyVoicesignalingDict | None = ...,
        guest: NetworkPolicyGuestDict | None = ...,
        guest_voice_signaling: NetworkPolicyGuestvoicesignalingDict | None = ...,
        softphone: NetworkPolicySoftphoneDict | None = ...,
        video_conferencing: NetworkPolicyVideoconferencingDict | None = ...,
        streaming_video: NetworkPolicyStreamingvideoDict | None = ...,
        video_signaling: NetworkPolicyVideosignalingDict | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...
    
    # Helper methods
    @staticmethod
    def help(field_name: str | None = ...) -> str: ...
    
    @staticmethod
    def fields(detailed: bool = ...) -> list[str] | list[dict[str, Any]]: ...
    
    @staticmethod
    def field_info(field_name: str) -> FortiObject[Any]: ...
    
    @staticmethod
    def validate_field(name: str, value: Any) -> bool: ...
    
    @staticmethod
    def required_fields() -> list[str]: ...
    
    @staticmethod
    def defaults() -> FortiObject[Any]: ...
    
    @staticmethod
    def schema() -> FortiObject[Any]: ...


__all__ = [
    "NetworkPolicy",
    "NetworkPolicyPayload",
    "NetworkPolicyResponse",
    "NetworkPolicyObject",
]