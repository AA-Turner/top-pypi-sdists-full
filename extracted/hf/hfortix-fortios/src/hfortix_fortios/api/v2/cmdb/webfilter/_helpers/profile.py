"""Validation helpers for webfilter/profile - Auto-generated"""

from typing import Any, TypedDict, Literal
from typing_extensions import NotRequired

# Import common validators from central _helpers module
from hfortix_fortios._helpers import (
    validate_enable_disable,
    validate_integer_range,
    validate_string_length,
    validate_port_number,
    validate_ip_address,
    validate_ipv6_address,
    validate_mac_address,
)

# Import central validation functions (avoid duplication across 1,062 files)
from hfortix_fortios._helpers.validation import (
    validate_required_fields as _validate_required_fields,
    validate_enum_field as _validate_enum_field,
    validate_query_parameter as _validate_query_parameter,
)

# ============================================================================
# Required Fields Validation
# Auto-generated from schema
# ============================================================================

# ⚠️  IMPORTANT: FortiOS schemas have known issues with required field marking:

# Do NOT use this list for strict validation - test with the actual FortiOS API!

# Fields marked as required (after filtering false positives)
REQUIRED_FIELDS = [
    "name",  # Profile name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "feature-set": "flow",
    "replacemsg-group": "",
    "options": "",
    "https-replacemsg": "enable",
    "web-flow-log-encoding": "utf-8",
    "ovrd-perm": "",
    "post-action": "normal",
    "wisp": "disable",
    "wisp-algorithm": "auto-learning",
    "log-all-url": "disable",
    "web-content-log": "enable",
    "web-filter-activex-log": "enable",
    "web-filter-command-block-log": "enable",
    "web-filter-cookie-log": "enable",
    "web-filter-applet-log": "enable",
    "web-filter-jscript-log": "enable",
    "web-filter-js-log": "enable",
    "web-filter-vbs-log": "enable",
    "web-filter-unknown-log": "enable",
    "web-filter-referer-log": "enable",
    "web-filter-cookie-removal-log": "enable",
    "web-url-log": "enable",
    "web-invalid-domain-log": "enable",
    "web-ftgd-err-log": "enable",
    "web-ftgd-quota-usage": "enable",
    "extended-log": "disable",
    "web-extended-all-action-log": "disable",
    "web-antiphishing-log": "enable",
}

# ============================================================================
# Deprecated Fields
# Auto-generated from schema - warns users about deprecated fields
# ============================================================================

# Deprecated fields with migration guidance
DEPRECATED_FIELDS = {
}

# ============================================================================
# Field Metadata (Type Information & Descriptions)
# Auto-generated from schema - use for IDE autocomplete and documentation
# ============================================================================

# Field types mapping
FIELD_TYPES = {
    "name": "string",  # Profile name.
    "comment": "var-string",  # Optional comments.
    "feature-set": "option",  # Flow/proxy feature set.
    "replacemsg-group": "string",  # Replacement message group.
    "options": "option",  # Options.
    "https-replacemsg": "option",  # Enable replacement messages for HTTPS.
    "web-flow-log-encoding": "option",  # Log encoding in flow mode.
    "ovrd-perm": "option",  # Permitted override types.
    "post-action": "option",  # Action taken for HTTP POST traffic.
    "override": "string",  # Web Filter override settings.
    "web": "string",  # Web content filtering settings.
    "ftgd-wf": "string",  # FortiGuard Web Filter settings.
    "antiphish": "string",  # AntiPhishing profile.
    "wisp": "option",  # Enable/disable web proxy WISP.
    "wisp-servers": "string",  # WISP servers.
    "wisp-algorithm": "option",  # WISP server selection algorithm.
    "log-all-url": "option",  # Enable/disable logging all URLs visited.
    "web-content-log": "option",  # Enable/disable logging logging blocked web content.
    "web-filter-activex-log": "option",  # Enable/disable logging ActiveX.
    "web-filter-command-block-log": "option",  # Enable/disable logging blocked commands.
    "web-filter-cookie-log": "option",  # Enable/disable logging cookie filtering.
    "web-filter-applet-log": "option",  # Enable/disable logging Java applets.
    "web-filter-jscript-log": "option",  # Enable/disable logging JScripts.
    "web-filter-js-log": "option",  # Enable/disable logging Java scripts.
    "web-filter-vbs-log": "option",  # Enable/disable logging VBS scripts.
    "web-filter-unknown-log": "option",  # Enable/disable logging unknown scripts.
    "web-filter-referer-log": "option",  # Enable/disable logging referrers.
    "web-filter-cookie-removal-log": "option",  # Enable/disable logging blocked cookies.
    "web-url-log": "option",  # Enable/disable logging URL filtering.
    "web-invalid-domain-log": "option",  # Enable/disable logging invalid domain names.
    "web-ftgd-err-log": "option",  # Enable/disable logging rating errors.
    "web-ftgd-quota-usage": "option",  # Enable/disable logging daily quota usage.
    "extended-log": "option",  # Enable/disable extended logging for web filtering.
    "web-extended-all-action-log": "option",  # Enable/disable extended any filter action logging for web filtering.
    "web-antiphishing-log": "option",  # Enable/disable logging of AntiPhishing checks.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Profile name.",
    "comment": "Optional comments.",
    "feature-set": "Flow/proxy feature set.",
    "replacemsg-group": "Replacement message group.",
    "options": "Options.",
    "https-replacemsg": "Enable replacement messages for HTTPS.",
    "web-flow-log-encoding": "Log encoding in flow mode.",
    "ovrd-perm": "Permitted override types.",
    "post-action": "Action taken for HTTP POST traffic.",
    "override": "Web Filter override settings.",
    "web": "Web content filtering settings.",
    "ftgd-wf": "FortiGuard Web Filter settings.",
    "antiphish": "AntiPhishing profile.",
    "wisp": "Enable/disable web proxy WISP.",
    "wisp-servers": "WISP servers.",
    "wisp-algorithm": "WISP server selection algorithm.",
    "log-all-url": "Enable/disable logging all URLs visited.",
    "web-content-log": "Enable/disable logging logging blocked web content.",
    "web-filter-activex-log": "Enable/disable logging ActiveX.",
    "web-filter-command-block-log": "Enable/disable logging blocked commands.",
    "web-filter-cookie-log": "Enable/disable logging cookie filtering.",
    "web-filter-applet-log": "Enable/disable logging Java applets.",
    "web-filter-jscript-log": "Enable/disable logging JScripts.",
    "web-filter-js-log": "Enable/disable logging Java scripts.",
    "web-filter-vbs-log": "Enable/disable logging VBS scripts.",
    "web-filter-unknown-log": "Enable/disable logging unknown scripts.",
    "web-filter-referer-log": "Enable/disable logging referrers.",
    "web-filter-cookie-removal-log": "Enable/disable logging blocked cookies.",
    "web-url-log": "Enable/disable logging URL filtering.",
    "web-invalid-domain-log": "Enable/disable logging invalid domain names.",
    "web-ftgd-err-log": "Enable/disable logging rating errors.",
    "web-ftgd-quota-usage": "Enable/disable logging daily quota usage.",
    "extended-log": "Enable/disable extended logging for web filtering.",
    "web-extended-all-action-log": "Enable/disable extended any filter action logging for web filtering.",
    "web-antiphishing-log": "Enable/disable logging of AntiPhishing checks.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
    "replacemsg-group": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "override": {
        "ovrd-cookie": {
            "type": "option",
            "help": "Allow/deny browser-based (cookie) overrides.",
            "default": "deny",
            "options": ["allow", "deny"],
        },
        "ovrd-scope": {
            "type": "option",
            "help": "Override scope.",
            "default": "user",
            "options": ["user", "user-group", "ip", "browser", "ask"],
        },
        "profile-type": {
            "type": "option",
            "help": "Override profile type.",
            "default": "list",
            "options": ["list", "radius"],
        },
        "ovrd-dur-mode": {
            "type": "option",
            "help": "Override duration mode.",
            "default": "constant",
            "options": ["constant", "ask"],
        },
        "ovrd-dur": {
            "type": "user",
            "help": "Override duration.",
            "default": "15m",
        },
        "profile-attribute": {
            "type": "option",
            "help": "Profile attribute to retrieve from the RADIUS server.",
            "default": "Login-LAT-Service",
            "options": ["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"],
        },
        "ovrd-user-group": {
            "type": "string",
            "help": "User groups with permission to use the override.",
        },
        "profile": {
            "type": "string",
            "help": "Web filter profile with permission to create overrides.",
        },
    },
    "web": {
        "bword-threshold": {
            "type": "integer",
            "help": "Banned word score threshold.",
            "default": 10,
            "min_value": 0,
            "max_value": 2147483647,
        },
        "bword-table": {
            "type": "integer",
            "help": "Banned word table ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "urlfilter-table": {
            "type": "integer",
            "help": "URL filter table ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "content-header-list": {
            "type": "integer",
            "help": "Content header list.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "blocklist": {
            "type": "option",
            "help": "Enable/disable automatic addition of URLs detected by FortiSandbox to blocklist.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "allowlist": {
            "type": "option",
            "help": "FortiGuard allowlist settings.",
            "default": "",
            "options": ["exempt-av", "exempt-webcontent", "exempt-activex-java-cookie", "exempt-dlp", "exempt-rangeblock", "extended-log-others"],
        },
        "safe-search": {
            "type": "option",
            "help": "Safe search type.",
            "default": "",
            "options": ["url", "header"],
        },
        "youtube-restrict": {
            "type": "option",
            "help": "YouTube EDU filter level.",
            "default": "none",
            "options": ["none", "strict", "moderate"],
        },
        "vimeo-restrict": {
            "type": "string",
            "help": "Set Vimeo-restrict (\"7\" = don't show mature content, \"134\" = don't show unrated and mature content). A value of cookie \"content_rating\".",
            "default": "",
            "max_length": 63,
        },
        "log-search": {
            "type": "option",
            "help": "Enable/disable logging all search phrases.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "keyword-match": {
            "type": "string",
            "help": "Search keywords to log when match is found.",
        },
    },
    "ftgd-wf": {
        "options": {
            "type": "option",
            "help": "Options for FortiGuard Web Filter.",
            "default": "ftgd-disable",
            "options": ["error-allow", "rate-server-ip", "connect-request-bypass", "ftgd-disable"],
        },
        "exempt-quota": {
            "type": "user",
            "help": "Do not stop quota for these categories.",
            "default": "17",
        },
        "ovrd": {
            "type": "user",
            "help": "Allow web filter profile overrides.",
            "default": "",
        },
        "filters": {
            "type": "string",
            "help": "FortiGuard filters.",
        },
        "risk": {
            "type": "string",
            "help": "FortiGuard risk level settings.",
        },
        "quota": {
            "type": "string",
            "help": "FortiGuard traffic quota settings.",
        },
        "max-quota-timeout": {
            "type": "integer",
            "help": "Maximum FortiGuard quota used by single page view in seconds (excludes streams).",
            "default": 300,
            "min_value": 1,
            "max_value": 86400,
        },
        "rate-javascript-urls": {
            "type": "option",
            "help": "Enable/disable rating JavaScript by URL.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "rate-css-urls": {
            "type": "option",
            "help": "Enable/disable rating CSS by URL.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "rate-crl-urls": {
            "type": "option",
            "help": "Enable/disable rating CRL by URL.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
    },
    "antiphish": {
        "status": {
            "type": "option",
            "help": "Toggle AntiPhishing functionality.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "default-action": {
            "type": "option",
            "help": "Action to be taken when there is no matching rule.",
            "default": "exempt",
            "options": ["exempt", "log", "block"],
        },
        "check-uri": {
            "type": "option",
            "help": "Enable/disable checking of GET URI parameters for known credentials.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "check-basic-auth": {
            "type": "option",
            "help": "Enable/disable checking of HTTP Basic Auth field for known credentials.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "check-username-only": {
            "type": "option",
            "help": "Enable/disable username only matching of credentials. Action will be taken for valid usernames regardless of password validity.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "max-body-len": {
            "type": "integer",
            "help": "Maximum size of a POST body to check for credentials.",
            "default": 1024,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "inspection-entries": {
            "type": "string",
            "help": "AntiPhishing entries.",
        },
        "custom-patterns": {
            "type": "string",
            "help": "Custom username and password regex patterns.",
        },
        "authentication": {
            "type": "option",
            "help": "Authentication methods.",
            "required": True,
            "default": "domain-controller",
            "options": ["domain-controller", "ldap"],
        },
        "domain-controller": {
            "type": "string",
            "help": "Domain for which to verify received credentials against.",
            "default": "",
            "max_length": 63,
        },
        "ldap": {
            "type": "string",
            "help": "LDAP server for which to verify received credentials against.",
            "default": "",
            "max_length": 63,
        },
    },
    "wisp-servers": {
        "name": {
            "type": "string",
            "help": "Server name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_FEATURE_SET = [
    "flow",
    "proxy",
]
VALID_BODY_OPTIONS = [
    "activexfilter",
    "cookiefilter",
    "javafilter",
    "block-invalid-url",
    "jscript",
    "js",
    "vbs",
    "unknown",
    "intrinsic",
    "wf-referer",
    "wf-cookie",
    "per-user-bal",
]
VALID_BODY_HTTPS_REPLACEMSG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FLOW_LOG_ENCODING = [
    "utf-8",
    "punycode",
]
VALID_BODY_OVRD_PERM = [
    "bannedword-override",
    "urlfilter-override",
    "fortiguard-wf-override",
    "contenttype-check-override",
]
VALID_BODY_POST_ACTION = [
    "normal",
    "block",
]
VALID_BODY_WISP = [
    "enable",
    "disable",
]
VALID_BODY_WISP_ALGORITHM = [
    "primary-secondary",
    "round-robin",
    "auto-learning",
]
VALID_BODY_LOG_ALL_URL = [
    "enable",
    "disable",
]
VALID_BODY_WEB_CONTENT_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FILTER_ACTIVEX_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FILTER_COMMAND_BLOCK_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FILTER_COOKIE_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FILTER_APPLET_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FILTER_JSCRIPT_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FILTER_JS_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FILTER_VBS_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FILTER_UNKNOWN_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FILTER_REFERER_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FILTER_COOKIE_REMOVAL_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_URL_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_INVALID_DOMAIN_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FTGD_ERR_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_FTGD_QUOTA_USAGE = [
    "enable",
    "disable",
]
VALID_BODY_EXTENDED_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_EXTENDED_ALL_ACTION_LOG = [
    "enable",
    "disable",
]
VALID_BODY_WEB_ANTIPHISHING_LOG = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_webfilter_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for webfilter/profile."""
    # Validate query parameters using central function
    if "action" in params:
        is_valid, error = _validate_query_parameter(
            "action",
            params.get("action"),
            VALID_QUERY_ACTION
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# POST Validation
# ============================================================================


def validate_webfilter_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new webfilter/profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "feature-set" in payload:
        is_valid, error = _validate_enum_field(
            "feature-set",
            payload["feature-set"],
            VALID_BODY_FEATURE_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "options" in payload:
        is_valid, error = _validate_enum_field(
            "options",
            payload["options"],
            VALID_BODY_OPTIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "https-replacemsg" in payload:
        is_valid, error = _validate_enum_field(
            "https-replacemsg",
            payload["https-replacemsg"],
            VALID_BODY_HTTPS_REPLACEMSG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-flow-log-encoding" in payload:
        is_valid, error = _validate_enum_field(
            "web-flow-log-encoding",
            payload["web-flow-log-encoding"],
            VALID_BODY_WEB_FLOW_LOG_ENCODING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ovrd-perm" in payload:
        is_valid, error = _validate_enum_field(
            "ovrd-perm",
            payload["ovrd-perm"],
            VALID_BODY_OVRD_PERM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "post-action" in payload:
        is_valid, error = _validate_enum_field(
            "post-action",
            payload["post-action"],
            VALID_BODY_POST_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wisp" in payload:
        is_valid, error = _validate_enum_field(
            "wisp",
            payload["wisp"],
            VALID_BODY_WISP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wisp-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "wisp-algorithm",
            payload["wisp-algorithm"],
            VALID_BODY_WISP_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-all-url" in payload:
        is_valid, error = _validate_enum_field(
            "log-all-url",
            payload["log-all-url"],
            VALID_BODY_LOG_ALL_URL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-content-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-content-log",
            payload["web-content-log"],
            VALID_BODY_WEB_CONTENT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-activex-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-activex-log",
            payload["web-filter-activex-log"],
            VALID_BODY_WEB_FILTER_ACTIVEX_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-command-block-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-command-block-log",
            payload["web-filter-command-block-log"],
            VALID_BODY_WEB_FILTER_COMMAND_BLOCK_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-cookie-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-cookie-log",
            payload["web-filter-cookie-log"],
            VALID_BODY_WEB_FILTER_COOKIE_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-applet-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-applet-log",
            payload["web-filter-applet-log"],
            VALID_BODY_WEB_FILTER_APPLET_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-jscript-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-jscript-log",
            payload["web-filter-jscript-log"],
            VALID_BODY_WEB_FILTER_JSCRIPT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-js-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-js-log",
            payload["web-filter-js-log"],
            VALID_BODY_WEB_FILTER_JS_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-vbs-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-vbs-log",
            payload["web-filter-vbs-log"],
            VALID_BODY_WEB_FILTER_VBS_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-unknown-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-unknown-log",
            payload["web-filter-unknown-log"],
            VALID_BODY_WEB_FILTER_UNKNOWN_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-referer-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-referer-log",
            payload["web-filter-referer-log"],
            VALID_BODY_WEB_FILTER_REFERER_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-cookie-removal-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-cookie-removal-log",
            payload["web-filter-cookie-removal-log"],
            VALID_BODY_WEB_FILTER_COOKIE_REMOVAL_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-url-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-url-log",
            payload["web-url-log"],
            VALID_BODY_WEB_URL_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-invalid-domain-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-invalid-domain-log",
            payload["web-invalid-domain-log"],
            VALID_BODY_WEB_INVALID_DOMAIN_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-ftgd-err-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-ftgd-err-log",
            payload["web-ftgd-err-log"],
            VALID_BODY_WEB_FTGD_ERR_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-ftgd-quota-usage" in payload:
        is_valid, error = _validate_enum_field(
            "web-ftgd-quota-usage",
            payload["web-ftgd-quota-usage"],
            VALID_BODY_WEB_FTGD_QUOTA_USAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extended-log" in payload:
        is_valid, error = _validate_enum_field(
            "extended-log",
            payload["extended-log"],
            VALID_BODY_EXTENDED_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-extended-all-action-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-extended-all-action-log",
            payload["web-extended-all-action-log"],
            VALID_BODY_WEB_EXTENDED_ALL_ACTION_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-antiphishing-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-antiphishing-log",
            payload["web-antiphishing-log"],
            VALID_BODY_WEB_ANTIPHISHING_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_webfilter_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update webfilter/profile."""
    # Validate enum values using central function
    if "feature-set" in payload:
        is_valid, error = _validate_enum_field(
            "feature-set",
            payload["feature-set"],
            VALID_BODY_FEATURE_SET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "options" in payload:
        is_valid, error = _validate_enum_field(
            "options",
            payload["options"],
            VALID_BODY_OPTIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "https-replacemsg" in payload:
        is_valid, error = _validate_enum_field(
            "https-replacemsg",
            payload["https-replacemsg"],
            VALID_BODY_HTTPS_REPLACEMSG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-flow-log-encoding" in payload:
        is_valid, error = _validate_enum_field(
            "web-flow-log-encoding",
            payload["web-flow-log-encoding"],
            VALID_BODY_WEB_FLOW_LOG_ENCODING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ovrd-perm" in payload:
        is_valid, error = _validate_enum_field(
            "ovrd-perm",
            payload["ovrd-perm"],
            VALID_BODY_OVRD_PERM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "post-action" in payload:
        is_valid, error = _validate_enum_field(
            "post-action",
            payload["post-action"],
            VALID_BODY_POST_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wisp" in payload:
        is_valid, error = _validate_enum_field(
            "wisp",
            payload["wisp"],
            VALID_BODY_WISP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wisp-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "wisp-algorithm",
            payload["wisp-algorithm"],
            VALID_BODY_WISP_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-all-url" in payload:
        is_valid, error = _validate_enum_field(
            "log-all-url",
            payload["log-all-url"],
            VALID_BODY_LOG_ALL_URL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-content-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-content-log",
            payload["web-content-log"],
            VALID_BODY_WEB_CONTENT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-activex-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-activex-log",
            payload["web-filter-activex-log"],
            VALID_BODY_WEB_FILTER_ACTIVEX_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-command-block-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-command-block-log",
            payload["web-filter-command-block-log"],
            VALID_BODY_WEB_FILTER_COMMAND_BLOCK_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-cookie-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-cookie-log",
            payload["web-filter-cookie-log"],
            VALID_BODY_WEB_FILTER_COOKIE_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-applet-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-applet-log",
            payload["web-filter-applet-log"],
            VALID_BODY_WEB_FILTER_APPLET_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-jscript-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-jscript-log",
            payload["web-filter-jscript-log"],
            VALID_BODY_WEB_FILTER_JSCRIPT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-js-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-js-log",
            payload["web-filter-js-log"],
            VALID_BODY_WEB_FILTER_JS_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-vbs-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-vbs-log",
            payload["web-filter-vbs-log"],
            VALID_BODY_WEB_FILTER_VBS_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-unknown-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-unknown-log",
            payload["web-filter-unknown-log"],
            VALID_BODY_WEB_FILTER_UNKNOWN_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-referer-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-referer-log",
            payload["web-filter-referer-log"],
            VALID_BODY_WEB_FILTER_REFERER_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-filter-cookie-removal-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-filter-cookie-removal-log",
            payload["web-filter-cookie-removal-log"],
            VALID_BODY_WEB_FILTER_COOKIE_REMOVAL_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-url-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-url-log",
            payload["web-url-log"],
            VALID_BODY_WEB_URL_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-invalid-domain-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-invalid-domain-log",
            payload["web-invalid-domain-log"],
            VALID_BODY_WEB_INVALID_DOMAIN_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-ftgd-err-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-ftgd-err-log",
            payload["web-ftgd-err-log"],
            VALID_BODY_WEB_FTGD_ERR_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-ftgd-quota-usage" in payload:
        is_valid, error = _validate_enum_field(
            "web-ftgd-quota-usage",
            payload["web-ftgd-quota-usage"],
            VALID_BODY_WEB_FTGD_QUOTA_USAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extended-log" in payload:
        is_valid, error = _validate_enum_field(
            "extended-log",
            payload["extended-log"],
            VALID_BODY_EXTENDED_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-extended-all-action-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-extended-all-action-log",
            payload["web-extended-all-action-log"],
            VALID_BODY_WEB_EXTENDED_ALL_ACTION_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "web-antiphishing-log" in payload:
        is_valid, error = _validate_enum_field(
            "web-antiphishing-log",
            payload["web-antiphishing-log"],
            VALID_BODY_WEB_ANTIPHISHING_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# Metadata Access Functions
# Imported from central module to avoid duplication across 1,062 files
# Bound to this endpoint's data using functools.partial (saves ~7KB per file)
# ============================================================================

from functools import partial
from hfortix_fortios._helpers.metadata import (
    get_field_description,
    get_field_type,
    get_field_constraints,
    get_field_default,
    get_field_options,
    get_nested_schema,
    get_all_fields,
    get_field_metadata,
    validate_field_value,
)

# Bind module-specific data to central functions using partial application
get_field_description = partial(get_field_description, FIELD_DESCRIPTIONS)
get_field_type = partial(get_field_type, FIELD_TYPES)
get_field_constraints = partial(get_field_constraints, FIELD_CONSTRAINTS)
get_field_default = partial(get_field_default, FIELDS_WITH_DEFAULTS)
get_field_options = partial(get_field_options, globals())
get_nested_schema = partial(get_nested_schema, NESTED_SCHEMAS)
get_all_fields = partial(get_all_fields, FIELD_TYPES)
get_field_metadata = partial(get_field_metadata, FIELD_TYPES, FIELD_DESCRIPTIONS, 
                             FIELD_CONSTRAINTS, FIELDS_WITH_DEFAULTS, REQUIRED_FIELDS,
                             NESTED_SCHEMAS, globals())
validate_field_value = partial(validate_field_value, FIELD_TYPES, FIELD_DESCRIPTIONS,
                               FIELD_CONSTRAINTS, globals())


# ============================================================================
# Schema Information
# Metadata about this endpoint schema
# ============================================================================

SCHEMA_INFO = {
    "endpoint": "webfilter/profile",
    "category": "cmdb",
    "api_path": "webfilter/profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Web filter profiles.",
    "total_fields": 35,
    "required_fields_count": 1,
    "fields_with_defaults_count": 29,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
