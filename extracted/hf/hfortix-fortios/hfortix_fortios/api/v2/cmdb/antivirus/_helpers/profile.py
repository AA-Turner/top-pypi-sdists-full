"""Validation helpers for antivirus/profile - Auto-generated"""

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
    "replacemsg-group": "",
    "feature-set": "flow",
    "fortisandbox-mode": "analytics-everything",
    "fortisandbox-max-upload": 10,
    "analytics-ignore-filetype": 0,
    "analytics-accept-filetype": 0,
    "analytics-db": "disable",
    "mobile-malware-db": "enable",
    "outbreak-prevention-archive-scan": "enable",
    "external-blocklist-enable-all": "disable",
    "ems-threat-feed": "disable",
    "fortindr-error-action": "log-only",
    "fortindr-timeout-action": "log-only",
    "fortisandbox-scan-timeout": 60,
    "fortisandbox-error-action": "log-only",
    "fortisandbox-timeout-action": "log-only",
    "av-virus-log": "enable",
    "extended-log": "disable",
    "scan-mode": "default",
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
    "comment": "var-string",  # Comment.
    "replacemsg-group": "string",  # Replacement message group customized for this profile.
    "feature-set": "option",  # Flow/proxy feature set.
    "fortisandbox-mode": "option",  # FortiSandbox scan modes.
    "fortisandbox-max-upload": "integer",  # Maximum size of files that can be uploaded to FortiSandbox i
    "analytics-ignore-filetype": "integer",  # Do not submit files matching this DLP file-pattern to FortiS
    "analytics-accept-filetype": "integer",  # Only submit files matching this DLP file-pattern to FortiSan
    "analytics-db": "option",  # Enable/disable using the FortiSandbox signature database to 
    "mobile-malware-db": "option",  # Enable/disable using the mobile malware signature database.
    "http": "string",  # Configure HTTP AntiVirus options.
    "ftp": "string",  # Configure FTP AntiVirus options.
    "imap": "string",  # Configure IMAP AntiVirus options.
    "pop3": "string",  # Configure POP3 AntiVirus options.
    "smtp": "string",  # Configure SMTP AntiVirus options.
    "mapi": "string",  # Configure MAPI AntiVirus options.
    "nntp": "string",  # Configure NNTP AntiVirus options.
    "cifs": "string",  # Configure CIFS AntiVirus options.
    "ssh": "string",  # Configure SFTP and SCP AntiVirus options.
    "nac-quar": "string",  # Configure AntiVirus quarantine settings.
    "content-disarm": "string",  # AV Content Disarm and Reconstruction settings.
    "outbreak-prevention-archive-scan": "option",  # Enable/disable outbreak-prevention archive scanning.
    "external-blocklist-enable-all": "option",  # Enable/disable all external blocklists.
    "external-blocklist": "string",  # One or more external malware block lists.
    "ems-threat-feed": "option",  # Enable/disable use of EMS threat feed when performing AntiVi
    "fortindr-error-action": "option",  # Action to take if FortiNDR encounters an error.
    "fortindr-timeout-action": "option",  # Action to take if FortiNDR encounters a scan timeout.
    "fortisandbox-scan-timeout": "integer",  # FortiSandbox inline scan timeout in seconds (30 - 180, defau
    "fortisandbox-error-action": "option",  # Action to take if FortiSandbox inline scan encounters an err
    "fortisandbox-timeout-action": "option",  # Action to take if FortiSandbox inline scan encounters a scan
    "av-virus-log": "option",  # Enable/disable AntiVirus logging.
    "extended-log": "option",  # Enable/disable extended logging for antivirus.
    "scan-mode": "option",  # Configure scan mode (default or legacy).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Profile name.",
    "comment": "Comment.",
    "replacemsg-group": "Replacement message group customized for this profile.",
    "feature-set": "Flow/proxy feature set.",
    "fortisandbox-mode": "FortiSandbox scan modes.",
    "fortisandbox-max-upload": "Maximum size of files that can be uploaded to FortiSandbox in Mbytes.",
    "analytics-ignore-filetype": "Do not submit files matching this DLP file-pattern to FortiSandbox (post-transfer scan only).",
    "analytics-accept-filetype": "Only submit files matching this DLP file-pattern to FortiSandbox (post-transfer scan only).",
    "analytics-db": "Enable/disable using the FortiSandbox signature database to supplement the AV signature databases.",
    "mobile-malware-db": "Enable/disable using the mobile malware signature database.",
    "http": "Configure HTTP AntiVirus options.",
    "ftp": "Configure FTP AntiVirus options.",
    "imap": "Configure IMAP AntiVirus options.",
    "pop3": "Configure POP3 AntiVirus options.",
    "smtp": "Configure SMTP AntiVirus options.",
    "mapi": "Configure MAPI AntiVirus options.",
    "nntp": "Configure NNTP AntiVirus options.",
    "cifs": "Configure CIFS AntiVirus options.",
    "ssh": "Configure SFTP and SCP AntiVirus options.",
    "nac-quar": "Configure AntiVirus quarantine settings.",
    "content-disarm": "AV Content Disarm and Reconstruction settings.",
    "outbreak-prevention-archive-scan": "Enable/disable outbreak-prevention archive scanning.",
    "external-blocklist-enable-all": "Enable/disable all external blocklists.",
    "external-blocklist": "One or more external malware block lists.",
    "ems-threat-feed": "Enable/disable use of EMS threat feed when performing AntiVirus scan. Analyzes files including the content of archives.",
    "fortindr-error-action": "Action to take if FortiNDR encounters an error.",
    "fortindr-timeout-action": "Action to take if FortiNDR encounters a scan timeout.",
    "fortisandbox-scan-timeout": "FortiSandbox inline scan timeout in seconds (30 - 180, default = 60).",
    "fortisandbox-error-action": "Action to take if FortiSandbox inline scan encounters an error.",
    "fortisandbox-timeout-action": "Action to take if FortiSandbox inline scan encounters a scan timeout.",
    "av-virus-log": "Enable/disable AntiVirus logging.",
    "extended-log": "Enable/disable extended logging for antivirus.",
    "scan-mode": "Configure scan mode (default or legacy).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 47},
    "replacemsg-group": {"type": "string", "max_length": 35},
    "fortisandbox-max-upload": {"type": "integer", "min": 1, "max": 4095},
    "analytics-ignore-filetype": {"type": "integer", "min": 0, "max": 4294967295},
    "analytics-accept-filetype": {"type": "integer", "min": 0, "max": 4294967295},
    "fortisandbox-scan-timeout": {"type": "integer", "min": 30, "max": 180},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "http": {
        "av-scan": {
            "type": "option",
            "help": "Enable AntiVirus scan service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "outbreak-prevention": {
            "type": "option",
            "help": "Enable virus outbreak prevention service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "external-blocklist": {
            "type": "option",
            "help": "Enable external-blocklist. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "malware-stream": {
            "type": "option",
            "help": "Enable 0-day malware-stream scanning. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortindr": {
            "type": "option",
            "help": "Enable scanning of files by FortiNDR.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortisandbox": {
            "type": "option",
            "help": "Enable scanning of files by FortiSandbox.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "quarantine": {
            "type": "option",
            "help": "Enable/disable quarantine for infected files.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "archive-block": {
            "type": "option",
            "help": "Select the archive types to block.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "archive-log": {
            "type": "option",
            "help": "Select the archive types to log.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "emulator": {
            "type": "option",
            "help": "Enable/disable the virus emulator.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "content-disarm": {
            "type": "option",
            "help": "Enable/disable Content Disarm and Reconstruction when performing AntiVirus scan.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
    "ftp": {
        "av-scan": {
            "type": "option",
            "help": "Enable AntiVirus scan service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "outbreak-prevention": {
            "type": "option",
            "help": "Enable virus outbreak prevention service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "external-blocklist": {
            "type": "option",
            "help": "Enable external-blocklist. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "malware-stream": {
            "type": "option",
            "help": "Enable 0-day malware-stream scanning. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortindr": {
            "type": "option",
            "help": "Enable scanning of files by FortiNDR.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortisandbox": {
            "type": "option",
            "help": "Enable scanning of files by FortiSandbox.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "quarantine": {
            "type": "option",
            "help": "Enable/disable quarantine for infected files.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "archive-block": {
            "type": "option",
            "help": "Select the archive types to block.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "archive-log": {
            "type": "option",
            "help": "Select the archive types to log.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "emulator": {
            "type": "option",
            "help": "Enable/disable the virus emulator.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
    "imap": {
        "av-scan": {
            "type": "option",
            "help": "Enable AntiVirus scan service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "outbreak-prevention": {
            "type": "option",
            "help": "Enable virus outbreak prevention service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "external-blocklist": {
            "type": "option",
            "help": "Enable external-blocklist. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "malware-stream": {
            "type": "option",
            "help": "Enable 0-day malware-stream scanning. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortindr": {
            "type": "option",
            "help": "Enable scanning of files by FortiNDR.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortisandbox": {
            "type": "option",
            "help": "Enable scanning of files by FortiSandbox.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "quarantine": {
            "type": "option",
            "help": "Enable/disable quarantine for infected files.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "archive-block": {
            "type": "option",
            "help": "Select the archive types to block.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "archive-log": {
            "type": "option",
            "help": "Select the archive types to log.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "emulator": {
            "type": "option",
            "help": "Enable/disable the virus emulator.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "executables": {
            "type": "option",
            "help": "Treat Windows executable files as viruses for the purpose of blocking or monitoring.",
            "default": "default",
            "options": ["default", "virus"],
        },
        "content-disarm": {
            "type": "option",
            "help": "Enable/disable Content Disarm and Reconstruction when performing AntiVirus scan.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
    "pop3": {
        "av-scan": {
            "type": "option",
            "help": "Enable AntiVirus scan service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "outbreak-prevention": {
            "type": "option",
            "help": "Enable virus outbreak prevention service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "external-blocklist": {
            "type": "option",
            "help": "Enable external-blocklist. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "malware-stream": {
            "type": "option",
            "help": "Enable 0-day malware-stream scanning. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortindr": {
            "type": "option",
            "help": "Enable scanning of files by FortiNDR.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortisandbox": {
            "type": "option",
            "help": "Enable scanning of files by FortiSandbox.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "quarantine": {
            "type": "option",
            "help": "Enable/disable quarantine for infected files.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "archive-block": {
            "type": "option",
            "help": "Select the archive types to block.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "archive-log": {
            "type": "option",
            "help": "Select the archive types to log.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "emulator": {
            "type": "option",
            "help": "Enable/disable the virus emulator.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "executables": {
            "type": "option",
            "help": "Treat Windows executable files as viruses for the purpose of blocking or monitoring.",
            "default": "default",
            "options": ["default", "virus"],
        },
        "content-disarm": {
            "type": "option",
            "help": "Enable/disable Content Disarm and Reconstruction when performing AntiVirus scan.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
    "smtp": {
        "av-scan": {
            "type": "option",
            "help": "Enable AntiVirus scan service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "outbreak-prevention": {
            "type": "option",
            "help": "Enable virus outbreak prevention service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "external-blocklist": {
            "type": "option",
            "help": "Enable external-blocklist. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "malware-stream": {
            "type": "option",
            "help": "Enable 0-day malware-stream scanning. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortindr": {
            "type": "option",
            "help": "Enable scanning of files by FortiNDR.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortisandbox": {
            "type": "option",
            "help": "Enable scanning of files by FortiSandbox.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "quarantine": {
            "type": "option",
            "help": "Enable/disable quarantine for infected files.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "archive-block": {
            "type": "option",
            "help": "Select the archive types to block.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "archive-log": {
            "type": "option",
            "help": "Select the archive types to log.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "emulator": {
            "type": "option",
            "help": "Enable/disable the virus emulator.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "executables": {
            "type": "option",
            "help": "Treat Windows executable files as viruses for the purpose of blocking or monitoring.",
            "default": "default",
            "options": ["default", "virus"],
        },
        "content-disarm": {
            "type": "option",
            "help": "Enable/disable Content Disarm and Reconstruction when performing AntiVirus scan.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
    "mapi": {
        "av-scan": {
            "type": "option",
            "help": "Enable AntiVirus scan service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "outbreak-prevention": {
            "type": "option",
            "help": "Enable virus outbreak prevention service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "external-blocklist": {
            "type": "option",
            "help": "Enable external-blocklist. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "malware-stream": {
            "type": "option",
            "help": "Enable 0-day malware-stream scanning. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortindr": {
            "type": "option",
            "help": "Enable scanning of files by FortiNDR.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortisandbox": {
            "type": "option",
            "help": "Enable scanning of files by FortiSandbox.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "quarantine": {
            "type": "option",
            "help": "Enable/disable quarantine for infected files.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "archive-block": {
            "type": "option",
            "help": "Select the archive types to block.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "archive-log": {
            "type": "option",
            "help": "Select the archive types to log.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "emulator": {
            "type": "option",
            "help": "Enable/disable the virus emulator.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "executables": {
            "type": "option",
            "help": "Treat Windows executable files as viruses for the purpose of blocking or monitoring.",
            "default": "default",
            "options": ["default", "virus"],
        },
    },
    "nntp": {
        "av-scan": {
            "type": "option",
            "help": "Enable AntiVirus scan service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "outbreak-prevention": {
            "type": "option",
            "help": "Enable virus outbreak prevention service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "external-blocklist": {
            "type": "option",
            "help": "Enable external-blocklist. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "malware-stream": {
            "type": "option",
            "help": "Enable 0-day malware-stream scanning. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortindr": {
            "type": "option",
            "help": "Enable scanning of files by FortiNDR.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortisandbox": {
            "type": "option",
            "help": "Enable scanning of files by FortiSandbox.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "quarantine": {
            "type": "option",
            "help": "Enable/disable quarantine for infected files.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "archive-block": {
            "type": "option",
            "help": "Select the archive types to block.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "archive-log": {
            "type": "option",
            "help": "Select the archive types to log.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "emulator": {
            "type": "option",
            "help": "Enable/disable the virus emulator.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
    "cifs": {
        "av-scan": {
            "type": "option",
            "help": "Enable AntiVirus scan service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "outbreak-prevention": {
            "type": "option",
            "help": "Enable virus outbreak prevention service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "external-blocklist": {
            "type": "option",
            "help": "Enable external-blocklist. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "malware-stream": {
            "type": "option",
            "help": "Enable 0-day malware-stream scanning. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortindr": {
            "type": "option",
            "help": "Enable scanning of files by FortiNDR.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortisandbox": {
            "type": "option",
            "help": "Enable scanning of files by FortiSandbox.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "quarantine": {
            "type": "option",
            "help": "Enable/disable quarantine for infected files.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "archive-block": {
            "type": "option",
            "help": "Select the archive types to block.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "archive-log": {
            "type": "option",
            "help": "Select the archive types to log.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "emulator": {
            "type": "option",
            "help": "Enable/disable the virus emulator.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
    "ssh": {
        "av-scan": {
            "type": "option",
            "help": "Enable AntiVirus scan service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "outbreak-prevention": {
            "type": "option",
            "help": "Enable virus outbreak prevention service.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "external-blocklist": {
            "type": "option",
            "help": "Enable external-blocklist. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "malware-stream": {
            "type": "option",
            "help": "Enable 0-day malware-stream scanning. Analyzes files including the content of archives.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortindr": {
            "type": "option",
            "help": "Enable scanning of files by FortiNDR.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "fortisandbox": {
            "type": "option",
            "help": "Enable scanning of files by FortiSandbox.",
            "default": "disable",
            "options": ["disable", "block", "monitor"],
        },
        "quarantine": {
            "type": "option",
            "help": "Enable/disable quarantine for infected files.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "archive-block": {
            "type": "option",
            "help": "Select the archive types to block.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "archive-log": {
            "type": "option",
            "help": "Select the archive types to log.",
            "default": "",
            "options": ["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"],
        },
        "emulator": {
            "type": "option",
            "help": "Enable/disable the virus emulator.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
    "nac-quar": {
        "infected": {
            "type": "option",
            "help": "Enable/Disable quarantining infected hosts to the banned user list.",
            "default": "none",
            "options": ["none", "quar-src-ip"],
        },
        "expiry": {
            "type": "user",
            "help": "Duration of quarantine.",
            "default": "5m",
        },
        "log": {
            "type": "option",
            "help": "Enable/disable AntiVirus quarantine logging.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
    },
    "content-disarm": {
        "analytics-suspicious": {
            "type": "option",
            "help": "Enable/disable using CDR as a secondary method for determining suspicous files for analytics.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "original-file-destination": {
            "type": "option",
            "help": "Destination to send original file if active content is removed.",
            "default": "discard",
            "options": ["fortisandbox", "quarantine", "discard"],
        },
        "error-action": {
            "type": "option",
            "help": "Action to be taken if CDR engine encounters an unrecoverable error.",
            "default": "log-only",
            "options": ["block", "log-only", "ignore"],
        },
        "office-macro": {
            "type": "option",
            "help": "Enable/disable stripping of macros in Microsoft Office documents.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "office-hylink": {
            "type": "option",
            "help": "Enable/disable stripping of hyperlinks in Microsoft Office documents.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "office-linked": {
            "type": "option",
            "help": "Enable/disable stripping of linked objects in Microsoft Office documents.",
            "default": "",
            "options": ["disable", "enable"],
        },
        "office-embed": {
            "type": "option",
            "help": "Enable/disable stripping of embedded objects in Microsoft Office documents.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "office-dde": {
            "type": "option",
            "help": "Enable/disable stripping of Dynamic Data Exchange events in Microsoft Office documents.",
            "default": "",
            "options": ["disable", "enable"],
        },
        "office-action": {
            "type": "option",
            "help": "Enable/disable stripping of PowerPoint action events in Microsoft Office documents.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "pdf-javacode": {
            "type": "option",
            "help": "Enable/disable stripping of JavaScript code in PDF documents.",
            "default": "",
            "options": ["disable", "enable"],
        },
        "pdf-embedfile": {
            "type": "option",
            "help": "Enable/disable stripping of embedded files in PDF documents.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "pdf-hyperlink": {
            "type": "option",
            "help": "Enable/disable stripping of hyperlinks from PDF documents.",
            "default": "",
            "options": ["disable", "enable"],
        },
        "pdf-act-gotor": {
            "type": "option",
            "help": "Enable/disable stripping of PDF document actions that access other PDF documents.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "pdf-act-launch": {
            "type": "option",
            "help": "Enable/disable stripping of PDF document actions that launch other applications.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "pdf-act-sound": {
            "type": "option",
            "help": "Enable/disable stripping of PDF document actions that play a sound.",
            "default": "",
            "options": ["disable", "enable"],
        },
        "pdf-act-movie": {
            "type": "option",
            "help": "Enable/disable stripping of PDF document actions that play a movie.",
            "default": "",
            "options": ["disable", "enable"],
        },
        "pdf-act-java": {
            "type": "option",
            "help": "Enable/disable stripping of PDF document actions that execute JavaScript code.",
            "default": "",
            "options": ["disable", "enable"],
        },
        "pdf-act-form": {
            "type": "option",
            "help": "Enable/disable stripping of PDF document actions that submit data to other targets.",
            "default": "",
            "options": ["disable", "enable"],
        },
        "cover-page": {
            "type": "option",
            "help": "Enable/disable inserting a cover page into the disarmed document.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "detect-only": {
            "type": "option",
            "help": "Enable/disable only detect disarmable files, do not alter content.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
    "external-blocklist": {
        "name": {
            "type": "string",
            "help": "External blocklist.",
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
VALID_BODY_FORTISANDBOX_MODE = [
    "inline",
    "analytics-suspicious",
    "analytics-everything",
]
VALID_BODY_ANALYTICS_DB = [
    "disable",
    "enable",
]
VALID_BODY_MOBILE_MALWARE_DB = [
    "disable",
    "enable",
]
VALID_BODY_OUTBREAK_PREVENTION_ARCHIVE_SCAN = [
    "disable",
    "enable",
]
VALID_BODY_EXTERNAL_BLOCKLIST_ENABLE_ALL = [
    "disable",
    "enable",
]
VALID_BODY_EMS_THREAT_FEED = [
    "disable",
    "enable",
]
VALID_BODY_FORTINDR_ERROR_ACTION = [
    "log-only",
    "block",
    "ignore",
]
VALID_BODY_FORTINDR_TIMEOUT_ACTION = [
    "log-only",
    "block",
    "ignore",
]
VALID_BODY_FORTISANDBOX_ERROR_ACTION = [
    "log-only",
    "block",
    "ignore",
]
VALID_BODY_FORTISANDBOX_TIMEOUT_ACTION = [
    "log-only",
    "block",
    "ignore",
]
VALID_BODY_AV_VIRUS_LOG = [
    "enable",
    "disable",
]
VALID_BODY_EXTENDED_LOG = [
    "enable",
    "disable",
]
VALID_BODY_SCAN_MODE = [
    "default",
    "legacy",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_antivirus_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for antivirus/profile."""
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


def validate_antivirus_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new antivirus/profile object."""
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
    if "fortisandbox-mode" in payload:
        is_valid, error = _validate_enum_field(
            "fortisandbox-mode",
            payload["fortisandbox-mode"],
            VALID_BODY_FORTISANDBOX_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "analytics-db" in payload:
        is_valid, error = _validate_enum_field(
            "analytics-db",
            payload["analytics-db"],
            VALID_BODY_ANALYTICS_DB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mobile-malware-db" in payload:
        is_valid, error = _validate_enum_field(
            "mobile-malware-db",
            payload["mobile-malware-db"],
            VALID_BODY_MOBILE_MALWARE_DB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "outbreak-prevention-archive-scan" in payload:
        is_valid, error = _validate_enum_field(
            "outbreak-prevention-archive-scan",
            payload["outbreak-prevention-archive-scan"],
            VALID_BODY_OUTBREAK_PREVENTION_ARCHIVE_SCAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "external-blocklist-enable-all" in payload:
        is_valid, error = _validate_enum_field(
            "external-blocklist-enable-all",
            payload["external-blocklist-enable-all"],
            VALID_BODY_EXTERNAL_BLOCKLIST_ENABLE_ALL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ems-threat-feed" in payload:
        is_valid, error = _validate_enum_field(
            "ems-threat-feed",
            payload["ems-threat-feed"],
            VALID_BODY_EMS_THREAT_FEED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortindr-error-action" in payload:
        is_valid, error = _validate_enum_field(
            "fortindr-error-action",
            payload["fortindr-error-action"],
            VALID_BODY_FORTINDR_ERROR_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortindr-timeout-action" in payload:
        is_valid, error = _validate_enum_field(
            "fortindr-timeout-action",
            payload["fortindr-timeout-action"],
            VALID_BODY_FORTINDR_TIMEOUT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortisandbox-error-action" in payload:
        is_valid, error = _validate_enum_field(
            "fortisandbox-error-action",
            payload["fortisandbox-error-action"],
            VALID_BODY_FORTISANDBOX_ERROR_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortisandbox-timeout-action" in payload:
        is_valid, error = _validate_enum_field(
            "fortisandbox-timeout-action",
            payload["fortisandbox-timeout-action"],
            VALID_BODY_FORTISANDBOX_TIMEOUT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "av-virus-log" in payload:
        is_valid, error = _validate_enum_field(
            "av-virus-log",
            payload["av-virus-log"],
            VALID_BODY_AV_VIRUS_LOG,
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
    if "scan-mode" in payload:
        is_valid, error = _validate_enum_field(
            "scan-mode",
            payload["scan-mode"],
            VALID_BODY_SCAN_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_antivirus_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update antivirus/profile."""
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
    if "fortisandbox-mode" in payload:
        is_valid, error = _validate_enum_field(
            "fortisandbox-mode",
            payload["fortisandbox-mode"],
            VALID_BODY_FORTISANDBOX_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "analytics-db" in payload:
        is_valid, error = _validate_enum_field(
            "analytics-db",
            payload["analytics-db"],
            VALID_BODY_ANALYTICS_DB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mobile-malware-db" in payload:
        is_valid, error = _validate_enum_field(
            "mobile-malware-db",
            payload["mobile-malware-db"],
            VALID_BODY_MOBILE_MALWARE_DB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "outbreak-prevention-archive-scan" in payload:
        is_valid, error = _validate_enum_field(
            "outbreak-prevention-archive-scan",
            payload["outbreak-prevention-archive-scan"],
            VALID_BODY_OUTBREAK_PREVENTION_ARCHIVE_SCAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "external-blocklist-enable-all" in payload:
        is_valid, error = _validate_enum_field(
            "external-blocklist-enable-all",
            payload["external-blocklist-enable-all"],
            VALID_BODY_EXTERNAL_BLOCKLIST_ENABLE_ALL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ems-threat-feed" in payload:
        is_valid, error = _validate_enum_field(
            "ems-threat-feed",
            payload["ems-threat-feed"],
            VALID_BODY_EMS_THREAT_FEED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortindr-error-action" in payload:
        is_valid, error = _validate_enum_field(
            "fortindr-error-action",
            payload["fortindr-error-action"],
            VALID_BODY_FORTINDR_ERROR_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortindr-timeout-action" in payload:
        is_valid, error = _validate_enum_field(
            "fortindr-timeout-action",
            payload["fortindr-timeout-action"],
            VALID_BODY_FORTINDR_TIMEOUT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortisandbox-error-action" in payload:
        is_valid, error = _validate_enum_field(
            "fortisandbox-error-action",
            payload["fortisandbox-error-action"],
            VALID_BODY_FORTISANDBOX_ERROR_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortisandbox-timeout-action" in payload:
        is_valid, error = _validate_enum_field(
            "fortisandbox-timeout-action",
            payload["fortisandbox-timeout-action"],
            VALID_BODY_FORTISANDBOX_TIMEOUT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "av-virus-log" in payload:
        is_valid, error = _validate_enum_field(
            "av-virus-log",
            payload["av-virus-log"],
            VALID_BODY_AV_VIRUS_LOG,
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
    if "scan-mode" in payload:
        is_valid, error = _validate_enum_field(
            "scan-mode",
            payload["scan-mode"],
            VALID_BODY_SCAN_MODE,
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
    "endpoint": "antivirus/profile",
    "category": "cmdb",
    "api_path": "antivirus/profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure AntiVirus profiles.",
    "total_fields": 33,
    "required_fields_count": 1,
    "fields_with_defaults_count": 20,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
