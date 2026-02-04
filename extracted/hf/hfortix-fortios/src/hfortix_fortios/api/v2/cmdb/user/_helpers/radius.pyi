from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_ALL_USERGROUP: Literal["disable", "enable"]
VALID_BODY_USE_MANAGEMENT_VDOM: Literal["enable", "disable"]
VALID_BODY_SWITCH_CONTROLLER_NAS_IP_DYNAMIC: Literal["enable", "disable"]
VALID_BODY_NAS_ID_TYPE: Literal["legacy", "custom", "hostname"]
VALID_BODY_CALL_STATION_ID_TYPE: Literal["legacy", "IP", "MAC"]
VALID_BODY_RADIUS_COA: Literal["enable", "disable"]
VALID_BODY_H3C_COMPATIBILITY: Literal["enable", "disable"]
VALID_BODY_AUTH_TYPE: Literal["auto", "ms_chap_v2", "ms_chap", "chap", "pap"]
VALID_BODY_USERNAME_CASE_SENSITIVE: Literal["enable", "disable"]
VALID_BODY_GROUP_OVERRIDE_ATTR_TYPE: Literal["filter-Id", "class"]
VALID_BODY_PASSWORD_RENEWAL: Literal["enable", "disable"]
VALID_BODY_REQUIRE_MESSAGE_AUTHENTICATOR: Literal["enable", "disable"]
VALID_BODY_PASSWORD_ENCODING: Literal["auto", "ISO-8859-1"]
VALID_BODY_MAC_USERNAME_DELIMITER: Literal["hyphen", "single-hyphen", "colon", "none"]
VALID_BODY_MAC_PASSWORD_DELIMITER: Literal["hyphen", "single-hyphen", "colon", "none"]
VALID_BODY_MAC_CASE: Literal["uppercase", "lowercase"]
VALID_BODY_ACCT_ALL_SERVERS: Literal["enable", "disable"]
VALID_BODY_INTERFACE_SELECT_METHOD: Literal["auto", "sdwan", "specify"]
VALID_BODY_SWITCH_CONTROLLER_SERVICE_TYPE: Literal["login", "framed", "callback-login", "callback-framed", "outbound", "administrative", "nas-prompt", "authenticate-only", "callback-nas-prompt", "call-check", "callback-administrative"]
VALID_BODY_TRANSPORT_PROTOCOL: Literal["udp", "tcp", "tls"]
VALID_BODY_TLS_MIN_PROTO_VERSION: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
VALID_BODY_SERVER_IDENTITY_CHECK: Literal["enable", "disable"]
VALID_BODY_ACCOUNT_KEY_PROCESSING: Literal["same", "strip"]
VALID_BODY_ACCOUNT_KEY_CERT_FIELD: Literal["othername", "rfc822name", "dnsname", "cn"]
VALID_BODY_RSSO: Literal["enable", "disable"]
VALID_BODY_RSSO_RADIUS_RESPONSE: Literal["enable", "disable"]
VALID_BODY_RSSO_VALIDATE_REQUEST_SECRET: Literal["enable", "disable"]
VALID_BODY_RSSO_ENDPOINT_ATTRIBUTE: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"]
VALID_BODY_RSSO_ENDPOINT_BLOCK_ATTRIBUTE: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"]
VALID_BODY_SSO_ATTRIBUTE: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"]
VALID_BODY_SSO_ATTRIBUTE_VALUE_OVERRIDE: Literal["enable", "disable"]
VALID_BODY_RSSO_LOG_FLAGS: Literal["protocol-error", "profile-missing", "accounting-stop-missed", "accounting-event", "endpoint-block", "radiusd-other", "none"]
VALID_BODY_RSSO_FLUSH_IP_SESSION: Literal["enable", "disable"]
VALID_BODY_RSSO_EP_ONE_IP_ONLY: Literal["enable", "disable"]
VALID_BODY_DELIMITER: Literal["plus", "comma"]

# Metadata dictionaries
FIELD_TYPES: dict[str, str]
FIELD_DESCRIPTIONS: dict[str, str]
FIELD_CONSTRAINTS: dict[str, dict[str, Any]]
NESTED_SCHEMAS: dict[str, dict[str, Any]]
FIELDS_WITH_DEFAULTS: dict[str, Any]
DEPRECATED_FIELDS: dict[str, dict[str, str]]
REQUIRED_FIELDS: list[str]

# Helper functions
def get_field_type(field_name: str) -> str | None: ...
def get_field_description(field_name: str) -> str | None: ...
def get_field_default(field_name: str) -> Any: ...
def get_field_constraints(field_name: str) -> dict[str, Any]: ...
def get_nested_schema(field_name: str) -> dict[str, Any] | None: ...
def get_field_metadata(field_name: str) -> dict[str, Any]: ...
def validate_field_value(field_name: str, value: Any) -> bool: ...
def get_all_fields() -> list[str]: ...
def get_required_fields() -> list[str]: ...
def get_schema_info() -> dict[str, Any]: ...


__all__ = [
    "VALID_BODY_ALL_USERGROUP",
    "VALID_BODY_USE_MANAGEMENT_VDOM",
    "VALID_BODY_SWITCH_CONTROLLER_NAS_IP_DYNAMIC",
    "VALID_BODY_NAS_ID_TYPE",
    "VALID_BODY_CALL_STATION_ID_TYPE",
    "VALID_BODY_RADIUS_COA",
    "VALID_BODY_H3C_COMPATIBILITY",
    "VALID_BODY_AUTH_TYPE",
    "VALID_BODY_USERNAME_CASE_SENSITIVE",
    "VALID_BODY_GROUP_OVERRIDE_ATTR_TYPE",
    "VALID_BODY_PASSWORD_RENEWAL",
    "VALID_BODY_REQUIRE_MESSAGE_AUTHENTICATOR",
    "VALID_BODY_PASSWORD_ENCODING",
    "VALID_BODY_MAC_USERNAME_DELIMITER",
    "VALID_BODY_MAC_PASSWORD_DELIMITER",
    "VALID_BODY_MAC_CASE",
    "VALID_BODY_ACCT_ALL_SERVERS",
    "VALID_BODY_INTERFACE_SELECT_METHOD",
    "VALID_BODY_SWITCH_CONTROLLER_SERVICE_TYPE",
    "VALID_BODY_TRANSPORT_PROTOCOL",
    "VALID_BODY_TLS_MIN_PROTO_VERSION",
    "VALID_BODY_SERVER_IDENTITY_CHECK",
    "VALID_BODY_ACCOUNT_KEY_PROCESSING",
    "VALID_BODY_ACCOUNT_KEY_CERT_FIELD",
    "VALID_BODY_RSSO",
    "VALID_BODY_RSSO_RADIUS_RESPONSE",
    "VALID_BODY_RSSO_VALIDATE_REQUEST_SECRET",
    "VALID_BODY_RSSO_ENDPOINT_ATTRIBUTE",
    "VALID_BODY_RSSO_ENDPOINT_BLOCK_ATTRIBUTE",
    "VALID_BODY_SSO_ATTRIBUTE",
    "VALID_BODY_SSO_ATTRIBUTE_VALUE_OVERRIDE",
    "VALID_BODY_RSSO_LOG_FLAGS",
    "VALID_BODY_RSSO_FLUSH_IP_SESSION",
    "VALID_BODY_RSSO_EP_ONE_IP_ONLY",
    "VALID_BODY_DELIMITER",
    "FIELD_TYPES",
    "FIELD_DESCRIPTIONS",
    "FIELD_CONSTRAINTS",
    "NESTED_SCHEMAS",
    "FIELDS_WITH_DEFAULTS",
    "DEPRECATED_FIELDS",
    "REQUIRED_FIELDS",
    "get_field_type",
    "get_field_description",
    "get_field_default",
    "get_field_constraints",
    "get_nested_schema",
    "get_field_metadata",
    "validate_field_value",
    "get_all_fields",
    "get_required_fields",
    "get_schema_info",
]