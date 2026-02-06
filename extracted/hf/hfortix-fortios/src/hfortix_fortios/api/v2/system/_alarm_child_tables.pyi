"""
Child Table Helper Type Stubs for system/alarm

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class GroupsDict(TypedDict, total=False):
    """Type definition for groups child table entry."""
    id: int | None
    period: int | None
    admin_auth_failure_threshold: int | None
    admin_auth_lockout_threshold: int | None
    user_auth_failure_threshold: int | None
    user_auth_lockout_threshold: int | None
    replay_attempt_threshold: int | None
    self_test_failure_threshold: int | None
    log_full_warning_threshold: int | None
    encryption_failure_threshold: int | None
    decryption_failure_threshold: int | None
    fw_policy_violations: list[Any] | None
    fw_policy_id: int | None
    fw_policy_id_threshold: int | None


class GroupsObject(FortiObject):
    """Typed FortiObject for groups child table entry with attribute access."""
    id: int | None
    period: int | None
    admin_auth_failure_threshold: int | None
    admin_auth_lockout_threshold: int | None
    user_auth_failure_threshold: int | None
    user_auth_lockout_threshold: int | None
    replay_attempt_threshold: int | None
    self_test_failure_threshold: int | None
    log_full_warning_threshold: int | None
    encryption_failure_threshold: int | None
    decryption_failure_threshold: int | None
    fw_policy_violations: list[Any] | None
    fw_policy_id: int | None
    fw_policy_id_threshold: int | None



class GroupsHelper:
    """Helper class for managing groups child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        id: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[GroupsObject] | GroupsObject | None: ...
    
    def set(
        self,
        id: int | None = ...,
        period: int | None = ...,
        admin_auth_failure_threshold: int | None = ...,
        admin_auth_lockout_threshold: int | None = ...,
        user_auth_failure_threshold: int | None = ...,
        user_auth_lockout_threshold: int | None = ...,
        replay_attempt_threshold: int | None = ...,
        self_test_failure_threshold: int | None = ...,
        log_full_warning_threshold: int | None = ...,
        encryption_failure_threshold: int | None = ...,
        decryption_failure_threshold: int | None = ...,
        fw_policy_violations: list[Any] | None = ...,
        fw_policy_id: int | None = ...,
        fw_policy_id_threshold: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

