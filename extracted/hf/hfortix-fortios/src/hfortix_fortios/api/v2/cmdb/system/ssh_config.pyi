""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/ssh_config
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class SshConfigPayload(TypedDict, total=False):
    """Payload type for SshConfig operations."""
    ssh_kex_algo: str | list[str]
    ssh_enc_algo: str | list[str]
    ssh_mac_algo: str | list[str]
    ssh_hsk_algo: str | list[str]
    ssh_hsk_override: Literal["disable", "enable"]
    ssh_hsk_password: str
    ssh_hsk: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SshConfigResponse(TypedDict, total=False):
    """Response type for SshConfig - use with .dict property for typed dict access."""
    ssh_kex_algo: str
    ssh_enc_algo: str
    ssh_mac_algo: str
    ssh_hsk_algo: str
    ssh_hsk_override: Literal["disable", "enable"]
    ssh_hsk_password: str
    ssh_hsk: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SshConfigObject(FortiObject):
    """Typed FortiObject for SshConfig with field access."""
    ssh_kex_algo: str
    ssh_enc_algo: str
    ssh_mac_algo: str
    ssh_hsk_algo: str
    ssh_hsk_override: Literal["disable", "enable"]
    ssh_hsk_password: str
    ssh_hsk: str


# ================================================================
# Main Endpoint Class
# ================================================================

class SshConfig:
    """
    
    Endpoint: system/ssh_config
    Category: cmdb
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # Singleton endpoint (no mkey)
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
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SshConfigObject: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...


    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SshConfigPayload | None = ...,
        ssh_kex_algo: str | list[str] | None = ...,
        ssh_enc_algo: str | list[str] | None = ...,
        ssh_mac_algo: str | list[str] | None = ...,
        ssh_hsk_algo: str | list[str] | None = ...,
        ssh_hsk_override: Literal["disable", "enable"] | None = ...,
        ssh_hsk_password: str | None = ...,
        ssh_hsk: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SshConfigObject: ...


    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SshConfigPayload | None = ...,
        ssh_kex_algo: Literal["diffie-hellman-group1-sha1", "diffie-hellman-group14-sha1", "diffie-hellman-group14-sha256", "diffie-hellman-group16-sha512", "diffie-hellman-group18-sha512", "diffie-hellman-group-exchange-sha1", "diffie-hellman-group-exchange-sha256", "curve25519-sha256@libssh.org", "ecdh-sha2-nistp256", "ecdh-sha2-nistp384", "ecdh-sha2-nistp521"] | list[str] | None = ...,
        ssh_enc_algo: Literal["chacha20-poly1305@openssh.com", "aes128-ctr", "aes192-ctr", "aes256-ctr", "arcfour256", "arcfour128", "aes128-cbc", "3des-cbc", "blowfish-cbc", "cast128-cbc", "aes192-cbc", "aes256-cbc", "arcfour", "rijndael-cbc@lysator.liu.se", "aes128-gcm@openssh.com", "aes256-gcm@openssh.com"] | list[str] | None = ...,
        ssh_mac_algo: Literal["hmac-md5", "hmac-md5-etm@openssh.com", "hmac-md5-96", "hmac-md5-96-etm@openssh.com", "hmac-sha1", "hmac-sha1-etm@openssh.com", "hmac-sha2-256", "hmac-sha2-256-etm@openssh.com", "hmac-sha2-512", "hmac-sha2-512-etm@openssh.com", "hmac-ripemd160", "hmac-ripemd160@openssh.com", "hmac-ripemd160-etm@openssh.com", "umac-64@openssh.com", "umac-128@openssh.com", "umac-64-etm@openssh.com", "umac-128-etm@openssh.com"] | list[str] | None = ...,
        ssh_hsk_algo: Literal["ssh-rsa", "ecdsa-sha2-nistp521", "ecdsa-sha2-nistp384", "ecdsa-sha2-nistp256", "rsa-sha2-256", "rsa-sha2-512", "ssh-ed25519"] | list[str] | None = ...,
        ssh_hsk_override: Literal["disable", "enable"] | None = ...,
        ssh_hsk_password: str | None = ...,
        ssh_hsk: str | None = ...,
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
    "SshConfig",
    "SshConfigPayload",
    "SshConfigResponse",
    "SshConfigObject",
]