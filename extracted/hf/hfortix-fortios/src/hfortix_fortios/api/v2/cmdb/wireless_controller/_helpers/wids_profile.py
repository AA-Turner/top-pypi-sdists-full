"""Validation helpers for wireless_controller/wids_profile - Auto-generated"""

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
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "comment": "",
    "sensor-mode": "disable",
    "ap-scan": "disable",
    "ap-bgscan-period": 600,
    "ap-bgscan-intv": 3,
    "ap-bgscan-duration": 30,
    "ap-bgscan-idle": 20,
    "ap-bgscan-report-intv": 30,
    "ap-fgscan-report-intv": 15,
    "ap-scan-passive": "disable",
    "ap-scan-threshold": "-90",
    "ap-auto-suppress": "disable",
    "wireless-bridge": "disable",
    "deauth-broadcast": "disable",
    "null-ssid-probe-resp": "disable",
    "long-duration-attack": "disable",
    "long-duration-thresh": 8200,
    "invalid-mac-oui": "disable",
    "weak-wep-iv": "disable",
    "auth-frame-flood": "disable",
    "auth-flood-time": 10,
    "auth-flood-thresh": 30,
    "assoc-frame-flood": "disable",
    "assoc-flood-time": 10,
    "assoc-flood-thresh": 30,
    "reassoc-flood": "disable",
    "reassoc-flood-time": 10,
    "reassoc-flood-thresh": 30,
    "probe-flood": "disable",
    "probe-flood-time": 1,
    "probe-flood-thresh": 30,
    "bcn-flood": "disable",
    "bcn-flood-time": 1,
    "bcn-flood-thresh": 15,
    "rts-flood": "disable",
    "rts-flood-time": 10,
    "rts-flood-thresh": 30,
    "cts-flood": "disable",
    "cts-flood-time": 10,
    "cts-flood-thresh": 30,
    "client-flood": "disable",
    "client-flood-time": 10,
    "client-flood-thresh": 30,
    "block_ack-flood": "disable",
    "block_ack-flood-time": 1,
    "block_ack-flood-thresh": 50,
    "pspoll-flood": "disable",
    "pspoll-flood-time": 1,
    "pspoll-flood-thresh": 30,
    "netstumbler": "disable",
    "netstumbler-time": 30,
    "netstumbler-thresh": 5,
    "wellenreiter": "disable",
    "wellenreiter-time": 30,
    "wellenreiter-thresh": 5,
    "spoofed-deauth": "disable",
    "asleap-attack": "disable",
    "eapol-start-flood": "disable",
    "eapol-start-thresh": 10,
    "eapol-start-intv": 1,
    "eapol-logoff-flood": "disable",
    "eapol-logoff-thresh": 10,
    "eapol-logoff-intv": 1,
    "eapol-succ-flood": "disable",
    "eapol-succ-thresh": 10,
    "eapol-succ-intv": 1,
    "eapol-fail-flood": "disable",
    "eapol-fail-thresh": 10,
    "eapol-fail-intv": 1,
    "eapol-pre-succ-flood": "disable",
    "eapol-pre-succ-thresh": 10,
    "eapol-pre-succ-intv": 1,
    "eapol-pre-fail-flood": "disable",
    "eapol-pre-fail-thresh": 10,
    "eapol-pre-fail-intv": 1,
    "deauth-unknown-src-thresh": 10,
    "windows-bridge": "disable",
    "disassoc-broadcast": "disable",
    "ap-spoofing": "disable",
    "chan-based-mitm": "disable",
    "adhoc-valid-ssid": "disable",
    "adhoc-network": "disable",
    "eapol-key-overflow": "disable",
    "ap-impersonation": "disable",
    "invalid-addr-combination": "disable",
    "beacon-wrong-channel": "disable",
    "ht-greenfield": "disable",
    "overflow-ie": "disable",
    "malformed-ht-ie": "disable",
    "malformed-auth": "disable",
    "malformed-association": "disable",
    "ht-40mhz-intolerance": "disable",
    "valid-ssid-misuse": "disable",
    "valid-client-misassociation": "disable",
    "hotspotter-attack": "disable",
    "pwsave-dos-attack": "disable",
    "omerta-attack": "disable",
    "disconnect-station": "disable",
    "unencrypted-valid": "disable",
    "fata-jack": "disable",
    "risky-encryption": "disable",
    "fuzzed-beacon": "disable",
    "fuzzed-probe-request": "disable",
    "fuzzed-probe-response": "disable",
    "air-jack": "disable",
    "wpa-ft-attack": "disable",
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
    "name": "string",  # WIDS profile name.
    "comment": "string",  # Comment.
    "sensor-mode": "option",  # Scan nearby WiFi stations (default = disable).
    "ap-scan": "option",  # Enable/disable rogue AP detection.
    "ap-scan-channel-list-2G-5G": "string",  # Selected ap scan channel list for 2.4G and 5G bands.
    "ap-scan-channel-list-6G": "string",  # Selected ap scan channel list for 6G band.
    "ap-bgscan-period": "integer",  # Period between background scans (10 - 3600 sec, default = 600).
    "ap-bgscan-intv": "integer",  # Period between successive channel scans (1 - 600 sec, default = 3).
    "ap-bgscan-duration": "integer",  # Listen time on scanning a channel (10 - 1000 msec, default = 30).
    "ap-bgscan-idle": "integer",  # Wait time for channel inactivity before scanning this channel (0 - 1000 msec, de
    "ap-bgscan-report-intv": "integer",  # Period between background scan reports (15 - 600 sec, default = 30).
    "ap-bgscan-disable-schedules": "string",  # Firewall schedules for turning off FortiAP radio background scan. Background sca
    "ap-fgscan-report-intv": "integer",  # Period between foreground scan reports (15 - 600 sec, default = 15).
    "ap-scan-passive": "option",  # Enable/disable passive scanning. Enable means do not send probe request on any c
    "ap-scan-threshold": "string",  # Minimum signal level/threshold in dBm required for the AP to report detected rog
    "ap-auto-suppress": "option",  # Enable/disable on-wire rogue AP auto-suppression (default = disable).
    "wireless-bridge": "option",  # Enable/disable wireless bridge detection (default = disable).
    "deauth-broadcast": "option",  # Enable/disable broadcasting de-authentication detection (default = disable).
    "null-ssid-probe-resp": "option",  # Enable/disable null SSID probe response detection (default = disable).
    "long-duration-attack": "option",  # Enable/disable long duration attack detection based on user configured threshold
    "long-duration-thresh": "integer",  # Threshold value for long duration attack detection (1000 - 32767 usec, default =
    "invalid-mac-oui": "option",  # Enable/disable invalid MAC OUI detection.
    "weak-wep-iv": "option",  # Enable/disable weak WEP IV (Initialization Vector) detection (default = disable)
    "auth-frame-flood": "option",  # Enable/disable authentication frame flooding detection (default = disable).
    "auth-flood-time": "integer",  # Number of seconds after which a station is considered not connected.
    "auth-flood-thresh": "integer",  # The threshold value for authentication frame flooding.
    "assoc-frame-flood": "option",  # Enable/disable association frame flooding detection (default = disable).
    "assoc-flood-time": "integer",  # Number of seconds after which a station is considered not connected.
    "assoc-flood-thresh": "integer",  # The threshold value for association frame flooding.
    "reassoc-flood": "option",  # Enable/disable reassociation flood detection (default = disable).
    "reassoc-flood-time": "integer",  # Detection Window Period.
    "reassoc-flood-thresh": "integer",  # The threshold value for reassociation flood.
    "probe-flood": "option",  # Enable/disable probe flood detection (default = disable).
    "probe-flood-time": "integer",  # Detection Window Period.
    "probe-flood-thresh": "integer",  # The threshold value for probe flood.
    "bcn-flood": "option",  # Enable/disable bcn flood detection (default = disable).
    "bcn-flood-time": "integer",  # Detection Window Period.
    "bcn-flood-thresh": "integer",  # The threshold value for bcn flood.
    "rts-flood": "option",  # Enable/disable rts flood detection (default = disable).
    "rts-flood-time": "integer",  # Detection Window Period.
    "rts-flood-thresh": "integer",  # The threshold value for rts flood.
    "cts-flood": "option",  # Enable/disable cts flood detection (default = disable).
    "cts-flood-time": "integer",  # Detection Window Period.
    "cts-flood-thresh": "integer",  # The threshold value for cts flood.
    "client-flood": "option",  # Enable/disable client flood detection (default = disable).
    "client-flood-time": "integer",  # Detection Window Period.
    "client-flood-thresh": "integer",  # The threshold value for client flood.
    "block_ack-flood": "option",  # Enable/disable block_ack flood detection (default = disable).
    "block_ack-flood-time": "integer",  # Detection Window Period.
    "block_ack-flood-thresh": "integer",  # The threshold value for block_ack flood.
    "pspoll-flood": "option",  # Enable/disable pspoll flood detection (default = disable).
    "pspoll-flood-time": "integer",  # Detection Window Period.
    "pspoll-flood-thresh": "integer",  # The threshold value for pspoll flood.
    "netstumbler": "option",  # Enable/disable netstumbler detection (default = disable).
    "netstumbler-time": "integer",  # Detection Window Period.
    "netstumbler-thresh": "integer",  # The threshold value for netstumbler.
    "wellenreiter": "option",  # Enable/disable wellenreiter detection (default = disable).
    "wellenreiter-time": "integer",  # Detection Window Period.
    "wellenreiter-thresh": "integer",  # The threshold value for wellenreiter.
    "spoofed-deauth": "option",  # Enable/disable spoofed de-authentication attack detection (default = disable).
    "asleap-attack": "option",  # Enable/disable asleap attack detection (default = disable).
    "eapol-start-flood": "option",  # Enable/disable EAPOL-Start flooding (to AP) detection (default = disable).
    "eapol-start-thresh": "integer",  # The threshold value for EAPOL-Start flooding in specified interval.
    "eapol-start-intv": "integer",  # The detection interval for EAPOL-Start flooding (1 - 3600 sec).
    "eapol-logoff-flood": "option",  # Enable/disable EAPOL-Logoff flooding (to AP) detection (default = disable).
    "eapol-logoff-thresh": "integer",  # The threshold value for EAPOL-Logoff flooding in specified interval.
    "eapol-logoff-intv": "integer",  # The detection interval for EAPOL-Logoff flooding (1 - 3600 sec).
    "eapol-succ-flood": "option",  # Enable/disable EAPOL-Success flooding (to AP) detection (default = disable).
    "eapol-succ-thresh": "integer",  # The threshold value for EAPOL-Success flooding in specified interval.
    "eapol-succ-intv": "integer",  # The detection interval for EAPOL-Success flooding (1 - 3600 sec).
    "eapol-fail-flood": "option",  # Enable/disable EAPOL-Failure flooding (to AP) detection (default = disable).
    "eapol-fail-thresh": "integer",  # The threshold value for EAPOL-Failure flooding in specified interval.
    "eapol-fail-intv": "integer",  # The detection interval for EAPOL-Failure flooding (1 - 3600 sec).
    "eapol-pre-succ-flood": "option",  # Enable/disable premature EAPOL-Success flooding (to STA) detection (default = di
    "eapol-pre-succ-thresh": "integer",  # The threshold value for premature EAPOL-Success flooding in specified interval.
    "eapol-pre-succ-intv": "integer",  # The detection interval for premature EAPOL-Success flooding (1 - 3600 sec).
    "eapol-pre-fail-flood": "option",  # Enable/disable premature EAPOL-Failure flooding (to STA) detection (default = di
    "eapol-pre-fail-thresh": "integer",  # The threshold value for premature EAPOL-Failure flooding in specified interval.
    "eapol-pre-fail-intv": "integer",  # The detection interval for premature EAPOL-Failure flooding (1 - 3600 sec).
    "deauth-unknown-src-thresh": "integer",  # Threshold value per second to deauth unknown src for DoS attack (0: no limit).
    "windows-bridge": "option",  # Enable/disable windows bridge detection (default = disable).
    "disassoc-broadcast": "option",  # Enable/disable broadcast dis-association detection (default = disable).
    "ap-spoofing": "option",  # Enable/disable AP spoofing detection (default = disable).
    "chan-based-mitm": "option",  # Enable/disable channel based mitm detection (default = disable).
    "adhoc-valid-ssid": "option",  # Enable/disable adhoc using valid SSID detection (default = disable).
    "adhoc-network": "option",  # Enable/disable adhoc network detection (default = disable).
    "eapol-key-overflow": "option",  # Enable/disable overflow EAPOL key detection (default = disable).
    "ap-impersonation": "option",  # Enable/disable AP impersonation detection (default = disable).
    "invalid-addr-combination": "option",  # Enable/disable invalid address combination detection (default = disable).
    "beacon-wrong-channel": "option",  # Enable/disable beacon wrong channel detection (default = disable).
    "ht-greenfield": "option",  # Enable/disable HT greenfield detection (default = disable).
    "overflow-ie": "option",  # Enable/disable overflow IE detection (default = disable).
    "malformed-ht-ie": "option",  # Enable/disable malformed HT IE detection (default = disable).
    "malformed-auth": "option",  # Enable/disable malformed auth frame detection (default = disable).
    "malformed-association": "option",  # Enable/disable malformed association request detection (default = disable).
    "ht-40mhz-intolerance": "option",  # Enable/disable HT 40 MHz intolerance detection (default = disable).
    "valid-ssid-misuse": "option",  # Enable/disable valid SSID misuse detection (default = disable).
    "valid-client-misassociation": "option",  # Enable/disable valid client misassociation detection (default = disable).
    "hotspotter-attack": "option",  # Enable/disable hotspotter attack detection (default = disable).
    "pwsave-dos-attack": "option",  # Enable/disable power save DOS attack detection (default = disable).
    "omerta-attack": "option",  # Enable/disable omerta attack detection (default = disable).
    "disconnect-station": "option",  # Enable/disable disconnect station detection (default = disable).
    "unencrypted-valid": "option",  # Enable/disable unencrypted valid detection (default = disable).
    "fata-jack": "option",  # Enable/disable FATA-Jack detection (default = disable).
    "risky-encryption": "option",  # Enable/disable Risky Encryption detection (default = disable).
    "fuzzed-beacon": "option",  # Enable/disable fuzzed beacon detection (default = disable).
    "fuzzed-probe-request": "option",  # Enable/disable fuzzed probe request detection (default = disable).
    "fuzzed-probe-response": "option",  # Enable/disable fuzzed probe response detection (default = disable).
    "air-jack": "option",  # Enable/disable AirJack detection (default = disable).
    "wpa-ft-attack": "option",  # Enable/disable WPA FT attack detection (default = disable).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "WIDS profile name.",
    "comment": "Comment.",
    "sensor-mode": "Scan nearby WiFi stations (default = disable).",
    "ap-scan": "Enable/disable rogue AP detection.",
    "ap-scan-channel-list-2G-5G": "Selected ap scan channel list for 2.4G and 5G bands.",
    "ap-scan-channel-list-6G": "Selected ap scan channel list for 6G band.",
    "ap-bgscan-period": "Period between background scans (10 - 3600 sec, default = 600).",
    "ap-bgscan-intv": "Period between successive channel scans (1 - 600 sec, default = 3).",
    "ap-bgscan-duration": "Listen time on scanning a channel (10 - 1000 msec, default = 30).",
    "ap-bgscan-idle": "Wait time for channel inactivity before scanning this channel (0 - 1000 msec, default = 20).",
    "ap-bgscan-report-intv": "Period between background scan reports (15 - 600 sec, default = 30).",
    "ap-bgscan-disable-schedules": "Firewall schedules for turning off FortiAP radio background scan. Background scan will be disabled when at least one of the schedules is valid. Separate multiple schedule names with a space.",
    "ap-fgscan-report-intv": "Period between foreground scan reports (15 - 600 sec, default = 15).",
    "ap-scan-passive": "Enable/disable passive scanning. Enable means do not send probe request on any channels (default = disable).",
    "ap-scan-threshold": "Minimum signal level/threshold in dBm required for the AP to report detected rogue AP (-95 to -20, default = -90).",
    "ap-auto-suppress": "Enable/disable on-wire rogue AP auto-suppression (default = disable).",
    "wireless-bridge": "Enable/disable wireless bridge detection (default = disable).",
    "deauth-broadcast": "Enable/disable broadcasting de-authentication detection (default = disable).",
    "null-ssid-probe-resp": "Enable/disable null SSID probe response detection (default = disable).",
    "long-duration-attack": "Enable/disable long duration attack detection based on user configured threshold (default = disable).",
    "long-duration-thresh": "Threshold value for long duration attack detection (1000 - 32767 usec, default = 8200).",
    "invalid-mac-oui": "Enable/disable invalid MAC OUI detection.",
    "weak-wep-iv": "Enable/disable weak WEP IV (Initialization Vector) detection (default = disable).",
    "auth-frame-flood": "Enable/disable authentication frame flooding detection (default = disable).",
    "auth-flood-time": "Number of seconds after which a station is considered not connected.",
    "auth-flood-thresh": "The threshold value for authentication frame flooding.",
    "assoc-frame-flood": "Enable/disable association frame flooding detection (default = disable).",
    "assoc-flood-time": "Number of seconds after which a station is considered not connected.",
    "assoc-flood-thresh": "The threshold value for association frame flooding.",
    "reassoc-flood": "Enable/disable reassociation flood detection (default = disable).",
    "reassoc-flood-time": "Detection Window Period.",
    "reassoc-flood-thresh": "The threshold value for reassociation flood.",
    "probe-flood": "Enable/disable probe flood detection (default = disable).",
    "probe-flood-time": "Detection Window Period.",
    "probe-flood-thresh": "The threshold value for probe flood.",
    "bcn-flood": "Enable/disable bcn flood detection (default = disable).",
    "bcn-flood-time": "Detection Window Period.",
    "bcn-flood-thresh": "The threshold value for bcn flood.",
    "rts-flood": "Enable/disable rts flood detection (default = disable).",
    "rts-flood-time": "Detection Window Period.",
    "rts-flood-thresh": "The threshold value for rts flood.",
    "cts-flood": "Enable/disable cts flood detection (default = disable).",
    "cts-flood-time": "Detection Window Period.",
    "cts-flood-thresh": "The threshold value for cts flood.",
    "client-flood": "Enable/disable client flood detection (default = disable).",
    "client-flood-time": "Detection Window Period.",
    "client-flood-thresh": "The threshold value for client flood.",
    "block_ack-flood": "Enable/disable block_ack flood detection (default = disable).",
    "block_ack-flood-time": "Detection Window Period.",
    "block_ack-flood-thresh": "The threshold value for block_ack flood.",
    "pspoll-flood": "Enable/disable pspoll flood detection (default = disable).",
    "pspoll-flood-time": "Detection Window Period.",
    "pspoll-flood-thresh": "The threshold value for pspoll flood.",
    "netstumbler": "Enable/disable netstumbler detection (default = disable).",
    "netstumbler-time": "Detection Window Period.",
    "netstumbler-thresh": "The threshold value for netstumbler.",
    "wellenreiter": "Enable/disable wellenreiter detection (default = disable).",
    "wellenreiter-time": "Detection Window Period.",
    "wellenreiter-thresh": "The threshold value for wellenreiter.",
    "spoofed-deauth": "Enable/disable spoofed de-authentication attack detection (default = disable).",
    "asleap-attack": "Enable/disable asleap attack detection (default = disable).",
    "eapol-start-flood": "Enable/disable EAPOL-Start flooding (to AP) detection (default = disable).",
    "eapol-start-thresh": "The threshold value for EAPOL-Start flooding in specified interval.",
    "eapol-start-intv": "The detection interval for EAPOL-Start flooding (1 - 3600 sec).",
    "eapol-logoff-flood": "Enable/disable EAPOL-Logoff flooding (to AP) detection (default = disable).",
    "eapol-logoff-thresh": "The threshold value for EAPOL-Logoff flooding in specified interval.",
    "eapol-logoff-intv": "The detection interval for EAPOL-Logoff flooding (1 - 3600 sec).",
    "eapol-succ-flood": "Enable/disable EAPOL-Success flooding (to AP) detection (default = disable).",
    "eapol-succ-thresh": "The threshold value for EAPOL-Success flooding in specified interval.",
    "eapol-succ-intv": "The detection interval for EAPOL-Success flooding (1 - 3600 sec).",
    "eapol-fail-flood": "Enable/disable EAPOL-Failure flooding (to AP) detection (default = disable).",
    "eapol-fail-thresh": "The threshold value for EAPOL-Failure flooding in specified interval.",
    "eapol-fail-intv": "The detection interval for EAPOL-Failure flooding (1 - 3600 sec).",
    "eapol-pre-succ-flood": "Enable/disable premature EAPOL-Success flooding (to STA) detection (default = disable).",
    "eapol-pre-succ-thresh": "The threshold value for premature EAPOL-Success flooding in specified interval.",
    "eapol-pre-succ-intv": "The detection interval for premature EAPOL-Success flooding (1 - 3600 sec).",
    "eapol-pre-fail-flood": "Enable/disable premature EAPOL-Failure flooding (to STA) detection (default = disable).",
    "eapol-pre-fail-thresh": "The threshold value for premature EAPOL-Failure flooding in specified interval.",
    "eapol-pre-fail-intv": "The detection interval for premature EAPOL-Failure flooding (1 - 3600 sec).",
    "deauth-unknown-src-thresh": "Threshold value per second to deauth unknown src for DoS attack (0: no limit).",
    "windows-bridge": "Enable/disable windows bridge detection (default = disable).",
    "disassoc-broadcast": "Enable/disable broadcast dis-association detection (default = disable).",
    "ap-spoofing": "Enable/disable AP spoofing detection (default = disable).",
    "chan-based-mitm": "Enable/disable channel based mitm detection (default = disable).",
    "adhoc-valid-ssid": "Enable/disable adhoc using valid SSID detection (default = disable).",
    "adhoc-network": "Enable/disable adhoc network detection (default = disable).",
    "eapol-key-overflow": "Enable/disable overflow EAPOL key detection (default = disable).",
    "ap-impersonation": "Enable/disable AP impersonation detection (default = disable).",
    "invalid-addr-combination": "Enable/disable invalid address combination detection (default = disable).",
    "beacon-wrong-channel": "Enable/disable beacon wrong channel detection (default = disable).",
    "ht-greenfield": "Enable/disable HT greenfield detection (default = disable).",
    "overflow-ie": "Enable/disable overflow IE detection (default = disable).",
    "malformed-ht-ie": "Enable/disable malformed HT IE detection (default = disable).",
    "malformed-auth": "Enable/disable malformed auth frame detection (default = disable).",
    "malformed-association": "Enable/disable malformed association request detection (default = disable).",
    "ht-40mhz-intolerance": "Enable/disable HT 40 MHz intolerance detection (default = disable).",
    "valid-ssid-misuse": "Enable/disable valid SSID misuse detection (default = disable).",
    "valid-client-misassociation": "Enable/disable valid client misassociation detection (default = disable).",
    "hotspotter-attack": "Enable/disable hotspotter attack detection (default = disable).",
    "pwsave-dos-attack": "Enable/disable power save DOS attack detection (default = disable).",
    "omerta-attack": "Enable/disable omerta attack detection (default = disable).",
    "disconnect-station": "Enable/disable disconnect station detection (default = disable).",
    "unencrypted-valid": "Enable/disable unencrypted valid detection (default = disable).",
    "fata-jack": "Enable/disable FATA-Jack detection (default = disable).",
    "risky-encryption": "Enable/disable Risky Encryption detection (default = disable).",
    "fuzzed-beacon": "Enable/disable fuzzed beacon detection (default = disable).",
    "fuzzed-probe-request": "Enable/disable fuzzed probe request detection (default = disable).",
    "fuzzed-probe-response": "Enable/disable fuzzed probe response detection (default = disable).",
    "air-jack": "Enable/disable AirJack detection (default = disable).",
    "wpa-ft-attack": "Enable/disable WPA FT attack detection (default = disable).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "comment": {"type": "string", "max_length": 63},
    "ap-bgscan-period": {"type": "integer", "min": 10, "max": 3600},
    "ap-bgscan-intv": {"type": "integer", "min": 1, "max": 600},
    "ap-bgscan-duration": {"type": "integer", "min": 10, "max": 1000},
    "ap-bgscan-idle": {"type": "integer", "min": 0, "max": 1000},
    "ap-bgscan-report-intv": {"type": "integer", "min": 15, "max": 600},
    "ap-fgscan-report-intv": {"type": "integer", "min": 15, "max": 600},
    "ap-scan-threshold": {"type": "string", "max_length": 7},
    "long-duration-thresh": {"type": "integer", "min": 1000, "max": 32767},
    "auth-flood-time": {"type": "integer", "min": 5, "max": 120},
    "auth-flood-thresh": {"type": "integer", "min": 1, "max": 100},
    "assoc-flood-time": {"type": "integer", "min": 5, "max": 120},
    "assoc-flood-thresh": {"type": "integer", "min": 1, "max": 100},
    "reassoc-flood-time": {"type": "integer", "min": 1, "max": 120},
    "reassoc-flood-thresh": {"type": "integer", "min": 1, "max": 65100},
    "probe-flood-time": {"type": "integer", "min": 1, "max": 120},
    "probe-flood-thresh": {"type": "integer", "min": 1, "max": 65100},
    "bcn-flood-time": {"type": "integer", "min": 1, "max": 120},
    "bcn-flood-thresh": {"type": "integer", "min": 1, "max": 65100},
    "rts-flood-time": {"type": "integer", "min": 1, "max": 120},
    "rts-flood-thresh": {"type": "integer", "min": 1, "max": 65100},
    "cts-flood-time": {"type": "integer", "min": 1, "max": 120},
    "cts-flood-thresh": {"type": "integer", "min": 1, "max": 65100},
    "client-flood-time": {"type": "integer", "min": 1, "max": 120},
    "client-flood-thresh": {"type": "integer", "min": 1, "max": 65100},
    "block_ack-flood-time": {"type": "integer", "min": 1, "max": 120},
    "block_ack-flood-thresh": {"type": "integer", "min": 1, "max": 65100},
    "pspoll-flood-time": {"type": "integer", "min": 1, "max": 120},
    "pspoll-flood-thresh": {"type": "integer", "min": 1, "max": 65100},
    "netstumbler-time": {"type": "integer", "min": 1, "max": 120},
    "netstumbler-thresh": {"type": "integer", "min": 1, "max": 65100},
    "wellenreiter-time": {"type": "integer", "min": 1, "max": 120},
    "wellenreiter-thresh": {"type": "integer", "min": 1, "max": 65100},
    "eapol-start-thresh": {"type": "integer", "min": 2, "max": 100},
    "eapol-start-intv": {"type": "integer", "min": 1, "max": 3600},
    "eapol-logoff-thresh": {"type": "integer", "min": 2, "max": 100},
    "eapol-logoff-intv": {"type": "integer", "min": 1, "max": 3600},
    "eapol-succ-thresh": {"type": "integer", "min": 2, "max": 100},
    "eapol-succ-intv": {"type": "integer", "min": 1, "max": 3600},
    "eapol-fail-thresh": {"type": "integer", "min": 2, "max": 100},
    "eapol-fail-intv": {"type": "integer", "min": 1, "max": 3600},
    "eapol-pre-succ-thresh": {"type": "integer", "min": 2, "max": 100},
    "eapol-pre-succ-intv": {"type": "integer", "min": 1, "max": 3600},
    "eapol-pre-fail-thresh": {"type": "integer", "min": 2, "max": 100},
    "eapol-pre-fail-intv": {"type": "integer", "min": 1, "max": 3600},
    "deauth-unknown-src-thresh": {"type": "integer", "min": 0, "max": 65535},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "ap-scan-channel-list-2G-5G": {
        "chan": {
            "type": "string",
            "help": "Channel number.",
            "required": True,
            "default": "",
            "max_length": 3,
        },
    },
    "ap-scan-channel-list-6G": {
        "chan": {
            "type": "string",
            "help": "Channel 6g number.",
            "required": True,
            "default": "",
            "max_length": 3,
        },
    },
    "ap-bgscan-disable-schedules": {
        "name": {
            "type": "string",
            "help": "Schedule name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_SENSOR_MODE = [
    "disable",
    "foreign",
    "both",
]
VALID_BODY_AP_SCAN = [
    "disable",
    "enable",
]
VALID_BODY_AP_SCAN_PASSIVE = [
    "enable",
    "disable",
]
VALID_BODY_AP_AUTO_SUPPRESS = [
    "enable",
    "disable",
]
VALID_BODY_WIRELESS_BRIDGE = [
    "enable",
    "disable",
]
VALID_BODY_DEAUTH_BROADCAST = [
    "enable",
    "disable",
]
VALID_BODY_NULL_SSID_PROBE_RESP = [
    "enable",
    "disable",
]
VALID_BODY_LONG_DURATION_ATTACK = [
    "enable",
    "disable",
]
VALID_BODY_INVALID_MAC_OUI = [
    "enable",
    "disable",
]
VALID_BODY_WEAK_WEP_IV = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_FRAME_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_ASSOC_FRAME_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_REASSOC_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_PROBE_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_BCN_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_RTS_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_CTS_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_CLIENT_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_BLOCK_ACK_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_PSPOLL_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_NETSTUMBLER = [
    "enable",
    "disable",
]
VALID_BODY_WELLENREITER = [
    "enable",
    "disable",
]
VALID_BODY_SPOOFED_DEAUTH = [
    "enable",
    "disable",
]
VALID_BODY_ASLEAP_ATTACK = [
    "enable",
    "disable",
]
VALID_BODY_EAPOL_START_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_EAPOL_LOGOFF_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_EAPOL_SUCC_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_EAPOL_FAIL_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_EAPOL_PRE_SUCC_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_EAPOL_PRE_FAIL_FLOOD = [
    "enable",
    "disable",
]
VALID_BODY_WINDOWS_BRIDGE = [
    "enable",
    "disable",
]
VALID_BODY_DISASSOC_BROADCAST = [
    "enable",
    "disable",
]
VALID_BODY_AP_SPOOFING = [
    "enable",
    "disable",
]
VALID_BODY_CHAN_BASED_MITM = [
    "enable",
    "disable",
]
VALID_BODY_ADHOC_VALID_SSID = [
    "enable",
    "disable",
]
VALID_BODY_ADHOC_NETWORK = [
    "enable",
    "disable",
]
VALID_BODY_EAPOL_KEY_OVERFLOW = [
    "enable",
    "disable",
]
VALID_BODY_AP_IMPERSONATION = [
    "enable",
    "disable",
]
VALID_BODY_INVALID_ADDR_COMBINATION = [
    "enable",
    "disable",
]
VALID_BODY_BEACON_WRONG_CHANNEL = [
    "enable",
    "disable",
]
VALID_BODY_HT_GREENFIELD = [
    "enable",
    "disable",
]
VALID_BODY_OVERFLOW_IE = [
    "enable",
    "disable",
]
VALID_BODY_MALFORMED_HT_IE = [
    "enable",
    "disable",
]
VALID_BODY_MALFORMED_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_MALFORMED_ASSOCIATION = [
    "enable",
    "disable",
]
VALID_BODY_HT_40MHZ_INTOLERANCE = [
    "enable",
    "disable",
]
VALID_BODY_VALID_SSID_MISUSE = [
    "enable",
    "disable",
]
VALID_BODY_VALID_CLIENT_MISASSOCIATION = [
    "enable",
    "disable",
]
VALID_BODY_HOTSPOTTER_ATTACK = [
    "enable",
    "disable",
]
VALID_BODY_PWSAVE_DOS_ATTACK = [
    "enable",
    "disable",
]
VALID_BODY_OMERTA_ATTACK = [
    "enable",
    "disable",
]
VALID_BODY_DISCONNECT_STATION = [
    "enable",
    "disable",
]
VALID_BODY_UNENCRYPTED_VALID = [
    "enable",
    "disable",
]
VALID_BODY_FATA_JACK = [
    "enable",
    "disable",
]
VALID_BODY_RISKY_ENCRYPTION = [
    "enable",
    "disable",
]
VALID_BODY_FUZZED_BEACON = [
    "enable",
    "disable",
]
VALID_BODY_FUZZED_PROBE_REQUEST = [
    "enable",
    "disable",
]
VALID_BODY_FUZZED_PROBE_RESPONSE = [
    "enable",
    "disable",
]
VALID_BODY_AIR_JACK = [
    "enable",
    "disable",
]
VALID_BODY_WPA_FT_ATTACK = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_wids_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/wids_profile."""
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


def validate_wireless_controller_wids_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/wids_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "sensor-mode" in payload:
        is_valid, error = _validate_enum_field(
            "sensor-mode",
            payload["sensor-mode"],
            VALID_BODY_SENSOR_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-scan" in payload:
        is_valid, error = _validate_enum_field(
            "ap-scan",
            payload["ap-scan"],
            VALID_BODY_AP_SCAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-scan-passive" in payload:
        is_valid, error = _validate_enum_field(
            "ap-scan-passive",
            payload["ap-scan-passive"],
            VALID_BODY_AP_SCAN_PASSIVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-auto-suppress" in payload:
        is_valid, error = _validate_enum_field(
            "ap-auto-suppress",
            payload["ap-auto-suppress"],
            VALID_BODY_AP_AUTO_SUPPRESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wireless-bridge" in payload:
        is_valid, error = _validate_enum_field(
            "wireless-bridge",
            payload["wireless-bridge"],
            VALID_BODY_WIRELESS_BRIDGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "deauth-broadcast" in payload:
        is_valid, error = _validate_enum_field(
            "deauth-broadcast",
            payload["deauth-broadcast"],
            VALID_BODY_DEAUTH_BROADCAST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "null-ssid-probe-resp" in payload:
        is_valid, error = _validate_enum_field(
            "null-ssid-probe-resp",
            payload["null-ssid-probe-resp"],
            VALID_BODY_NULL_SSID_PROBE_RESP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "long-duration-attack" in payload:
        is_valid, error = _validate_enum_field(
            "long-duration-attack",
            payload["long-duration-attack"],
            VALID_BODY_LONG_DURATION_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "invalid-mac-oui" in payload:
        is_valid, error = _validate_enum_field(
            "invalid-mac-oui",
            payload["invalid-mac-oui"],
            VALID_BODY_INVALID_MAC_OUI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "weak-wep-iv" in payload:
        is_valid, error = _validate_enum_field(
            "weak-wep-iv",
            payload["weak-wep-iv"],
            VALID_BODY_WEAK_WEP_IV,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-frame-flood" in payload:
        is_valid, error = _validate_enum_field(
            "auth-frame-flood",
            payload["auth-frame-flood"],
            VALID_BODY_AUTH_FRAME_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "assoc-frame-flood" in payload:
        is_valid, error = _validate_enum_field(
            "assoc-frame-flood",
            payload["assoc-frame-flood"],
            VALID_BODY_ASSOC_FRAME_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reassoc-flood" in payload:
        is_valid, error = _validate_enum_field(
            "reassoc-flood",
            payload["reassoc-flood"],
            VALID_BODY_REASSOC_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "probe-flood" in payload:
        is_valid, error = _validate_enum_field(
            "probe-flood",
            payload["probe-flood"],
            VALID_BODY_PROBE_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bcn-flood" in payload:
        is_valid, error = _validate_enum_field(
            "bcn-flood",
            payload["bcn-flood"],
            VALID_BODY_BCN_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rts-flood" in payload:
        is_valid, error = _validate_enum_field(
            "rts-flood",
            payload["rts-flood"],
            VALID_BODY_RTS_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cts-flood" in payload:
        is_valid, error = _validate_enum_field(
            "cts-flood",
            payload["cts-flood"],
            VALID_BODY_CTS_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-flood" in payload:
        is_valid, error = _validate_enum_field(
            "client-flood",
            payload["client-flood"],
            VALID_BODY_CLIENT_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block_ack-flood" in payload:
        is_valid, error = _validate_enum_field(
            "block_ack-flood",
            payload["block_ack-flood"],
            VALID_BODY_BLOCK_ACK_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pspoll-flood" in payload:
        is_valid, error = _validate_enum_field(
            "pspoll-flood",
            payload["pspoll-flood"],
            VALID_BODY_PSPOLL_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "netstumbler" in payload:
        is_valid, error = _validate_enum_field(
            "netstumbler",
            payload["netstumbler"],
            VALID_BODY_NETSTUMBLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wellenreiter" in payload:
        is_valid, error = _validate_enum_field(
            "wellenreiter",
            payload["wellenreiter"],
            VALID_BODY_WELLENREITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "spoofed-deauth" in payload:
        is_valid, error = _validate_enum_field(
            "spoofed-deauth",
            payload["spoofed-deauth"],
            VALID_BODY_SPOOFED_DEAUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "asleap-attack" in payload:
        is_valid, error = _validate_enum_field(
            "asleap-attack",
            payload["asleap-attack"],
            VALID_BODY_ASLEAP_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-start-flood" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-start-flood",
            payload["eapol-start-flood"],
            VALID_BODY_EAPOL_START_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-logoff-flood" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-logoff-flood",
            payload["eapol-logoff-flood"],
            VALID_BODY_EAPOL_LOGOFF_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-succ-flood" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-succ-flood",
            payload["eapol-succ-flood"],
            VALID_BODY_EAPOL_SUCC_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-fail-flood" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-fail-flood",
            payload["eapol-fail-flood"],
            VALID_BODY_EAPOL_FAIL_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-pre-succ-flood" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-pre-succ-flood",
            payload["eapol-pre-succ-flood"],
            VALID_BODY_EAPOL_PRE_SUCC_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-pre-fail-flood" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-pre-fail-flood",
            payload["eapol-pre-fail-flood"],
            VALID_BODY_EAPOL_PRE_FAIL_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "windows-bridge" in payload:
        is_valid, error = _validate_enum_field(
            "windows-bridge",
            payload["windows-bridge"],
            VALID_BODY_WINDOWS_BRIDGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "disassoc-broadcast" in payload:
        is_valid, error = _validate_enum_field(
            "disassoc-broadcast",
            payload["disassoc-broadcast"],
            VALID_BODY_DISASSOC_BROADCAST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-spoofing" in payload:
        is_valid, error = _validate_enum_field(
            "ap-spoofing",
            payload["ap-spoofing"],
            VALID_BODY_AP_SPOOFING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "chan-based-mitm" in payload:
        is_valid, error = _validate_enum_field(
            "chan-based-mitm",
            payload["chan-based-mitm"],
            VALID_BODY_CHAN_BASED_MITM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adhoc-valid-ssid" in payload:
        is_valid, error = _validate_enum_field(
            "adhoc-valid-ssid",
            payload["adhoc-valid-ssid"],
            VALID_BODY_ADHOC_VALID_SSID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adhoc-network" in payload:
        is_valid, error = _validate_enum_field(
            "adhoc-network",
            payload["adhoc-network"],
            VALID_BODY_ADHOC_NETWORK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-key-overflow" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-key-overflow",
            payload["eapol-key-overflow"],
            VALID_BODY_EAPOL_KEY_OVERFLOW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-impersonation" in payload:
        is_valid, error = _validate_enum_field(
            "ap-impersonation",
            payload["ap-impersonation"],
            VALID_BODY_AP_IMPERSONATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "invalid-addr-combination" in payload:
        is_valid, error = _validate_enum_field(
            "invalid-addr-combination",
            payload["invalid-addr-combination"],
            VALID_BODY_INVALID_ADDR_COMBINATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "beacon-wrong-channel" in payload:
        is_valid, error = _validate_enum_field(
            "beacon-wrong-channel",
            payload["beacon-wrong-channel"],
            VALID_BODY_BEACON_WRONG_CHANNEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ht-greenfield" in payload:
        is_valid, error = _validate_enum_field(
            "ht-greenfield",
            payload["ht-greenfield"],
            VALID_BODY_HT_GREENFIELD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "overflow-ie" in payload:
        is_valid, error = _validate_enum_field(
            "overflow-ie",
            payload["overflow-ie"],
            VALID_BODY_OVERFLOW_IE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "malformed-ht-ie" in payload:
        is_valid, error = _validate_enum_field(
            "malformed-ht-ie",
            payload["malformed-ht-ie"],
            VALID_BODY_MALFORMED_HT_IE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "malformed-auth" in payload:
        is_valid, error = _validate_enum_field(
            "malformed-auth",
            payload["malformed-auth"],
            VALID_BODY_MALFORMED_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "malformed-association" in payload:
        is_valid, error = _validate_enum_field(
            "malformed-association",
            payload["malformed-association"],
            VALID_BODY_MALFORMED_ASSOCIATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ht-40mhz-intolerance" in payload:
        is_valid, error = _validate_enum_field(
            "ht-40mhz-intolerance",
            payload["ht-40mhz-intolerance"],
            VALID_BODY_HT_40MHZ_INTOLERANCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "valid-ssid-misuse" in payload:
        is_valid, error = _validate_enum_field(
            "valid-ssid-misuse",
            payload["valid-ssid-misuse"],
            VALID_BODY_VALID_SSID_MISUSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "valid-client-misassociation" in payload:
        is_valid, error = _validate_enum_field(
            "valid-client-misassociation",
            payload["valid-client-misassociation"],
            VALID_BODY_VALID_CLIENT_MISASSOCIATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "hotspotter-attack" in payload:
        is_valid, error = _validate_enum_field(
            "hotspotter-attack",
            payload["hotspotter-attack"],
            VALID_BODY_HOTSPOTTER_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pwsave-dos-attack" in payload:
        is_valid, error = _validate_enum_field(
            "pwsave-dos-attack",
            payload["pwsave-dos-attack"],
            VALID_BODY_PWSAVE_DOS_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "omerta-attack" in payload:
        is_valid, error = _validate_enum_field(
            "omerta-attack",
            payload["omerta-attack"],
            VALID_BODY_OMERTA_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "disconnect-station" in payload:
        is_valid, error = _validate_enum_field(
            "disconnect-station",
            payload["disconnect-station"],
            VALID_BODY_DISCONNECT_STATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unencrypted-valid" in payload:
        is_valid, error = _validate_enum_field(
            "unencrypted-valid",
            payload["unencrypted-valid"],
            VALID_BODY_UNENCRYPTED_VALID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fata-jack" in payload:
        is_valid, error = _validate_enum_field(
            "fata-jack",
            payload["fata-jack"],
            VALID_BODY_FATA_JACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "risky-encryption" in payload:
        is_valid, error = _validate_enum_field(
            "risky-encryption",
            payload["risky-encryption"],
            VALID_BODY_RISKY_ENCRYPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fuzzed-beacon" in payload:
        is_valid, error = _validate_enum_field(
            "fuzzed-beacon",
            payload["fuzzed-beacon"],
            VALID_BODY_FUZZED_BEACON,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fuzzed-probe-request" in payload:
        is_valid, error = _validate_enum_field(
            "fuzzed-probe-request",
            payload["fuzzed-probe-request"],
            VALID_BODY_FUZZED_PROBE_REQUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fuzzed-probe-response" in payload:
        is_valid, error = _validate_enum_field(
            "fuzzed-probe-response",
            payload["fuzzed-probe-response"],
            VALID_BODY_FUZZED_PROBE_RESPONSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "air-jack" in payload:
        is_valid, error = _validate_enum_field(
            "air-jack",
            payload["air-jack"],
            VALID_BODY_AIR_JACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wpa-ft-attack" in payload:
        is_valid, error = _validate_enum_field(
            "wpa-ft-attack",
            payload["wpa-ft-attack"],
            VALID_BODY_WPA_FT_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_wids_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/wids_profile."""
    # Validate enum values using central function
    if "sensor-mode" in payload:
        is_valid, error = _validate_enum_field(
            "sensor-mode",
            payload["sensor-mode"],
            VALID_BODY_SENSOR_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-scan" in payload:
        is_valid, error = _validate_enum_field(
            "ap-scan",
            payload["ap-scan"],
            VALID_BODY_AP_SCAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-scan-passive" in payload:
        is_valid, error = _validate_enum_field(
            "ap-scan-passive",
            payload["ap-scan-passive"],
            VALID_BODY_AP_SCAN_PASSIVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-auto-suppress" in payload:
        is_valid, error = _validate_enum_field(
            "ap-auto-suppress",
            payload["ap-auto-suppress"],
            VALID_BODY_AP_AUTO_SUPPRESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wireless-bridge" in payload:
        is_valid, error = _validate_enum_field(
            "wireless-bridge",
            payload["wireless-bridge"],
            VALID_BODY_WIRELESS_BRIDGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "deauth-broadcast" in payload:
        is_valid, error = _validate_enum_field(
            "deauth-broadcast",
            payload["deauth-broadcast"],
            VALID_BODY_DEAUTH_BROADCAST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "null-ssid-probe-resp" in payload:
        is_valid, error = _validate_enum_field(
            "null-ssid-probe-resp",
            payload["null-ssid-probe-resp"],
            VALID_BODY_NULL_SSID_PROBE_RESP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "long-duration-attack" in payload:
        is_valid, error = _validate_enum_field(
            "long-duration-attack",
            payload["long-duration-attack"],
            VALID_BODY_LONG_DURATION_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "invalid-mac-oui" in payload:
        is_valid, error = _validate_enum_field(
            "invalid-mac-oui",
            payload["invalid-mac-oui"],
            VALID_BODY_INVALID_MAC_OUI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "weak-wep-iv" in payload:
        is_valid, error = _validate_enum_field(
            "weak-wep-iv",
            payload["weak-wep-iv"],
            VALID_BODY_WEAK_WEP_IV,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-frame-flood" in payload:
        is_valid, error = _validate_enum_field(
            "auth-frame-flood",
            payload["auth-frame-flood"],
            VALID_BODY_AUTH_FRAME_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "assoc-frame-flood" in payload:
        is_valid, error = _validate_enum_field(
            "assoc-frame-flood",
            payload["assoc-frame-flood"],
            VALID_BODY_ASSOC_FRAME_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reassoc-flood" in payload:
        is_valid, error = _validate_enum_field(
            "reassoc-flood",
            payload["reassoc-flood"],
            VALID_BODY_REASSOC_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "probe-flood" in payload:
        is_valid, error = _validate_enum_field(
            "probe-flood",
            payload["probe-flood"],
            VALID_BODY_PROBE_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bcn-flood" in payload:
        is_valid, error = _validate_enum_field(
            "bcn-flood",
            payload["bcn-flood"],
            VALID_BODY_BCN_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rts-flood" in payload:
        is_valid, error = _validate_enum_field(
            "rts-flood",
            payload["rts-flood"],
            VALID_BODY_RTS_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cts-flood" in payload:
        is_valid, error = _validate_enum_field(
            "cts-flood",
            payload["cts-flood"],
            VALID_BODY_CTS_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-flood" in payload:
        is_valid, error = _validate_enum_field(
            "client-flood",
            payload["client-flood"],
            VALID_BODY_CLIENT_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block_ack-flood" in payload:
        is_valid, error = _validate_enum_field(
            "block_ack-flood",
            payload["block_ack-flood"],
            VALID_BODY_BLOCK_ACK_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pspoll-flood" in payload:
        is_valid, error = _validate_enum_field(
            "pspoll-flood",
            payload["pspoll-flood"],
            VALID_BODY_PSPOLL_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "netstumbler" in payload:
        is_valid, error = _validate_enum_field(
            "netstumbler",
            payload["netstumbler"],
            VALID_BODY_NETSTUMBLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wellenreiter" in payload:
        is_valid, error = _validate_enum_field(
            "wellenreiter",
            payload["wellenreiter"],
            VALID_BODY_WELLENREITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "spoofed-deauth" in payload:
        is_valid, error = _validate_enum_field(
            "spoofed-deauth",
            payload["spoofed-deauth"],
            VALID_BODY_SPOOFED_DEAUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "asleap-attack" in payload:
        is_valid, error = _validate_enum_field(
            "asleap-attack",
            payload["asleap-attack"],
            VALID_BODY_ASLEAP_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-start-flood" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-start-flood",
            payload["eapol-start-flood"],
            VALID_BODY_EAPOL_START_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-logoff-flood" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-logoff-flood",
            payload["eapol-logoff-flood"],
            VALID_BODY_EAPOL_LOGOFF_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-succ-flood" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-succ-flood",
            payload["eapol-succ-flood"],
            VALID_BODY_EAPOL_SUCC_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-fail-flood" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-fail-flood",
            payload["eapol-fail-flood"],
            VALID_BODY_EAPOL_FAIL_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-pre-succ-flood" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-pre-succ-flood",
            payload["eapol-pre-succ-flood"],
            VALID_BODY_EAPOL_PRE_SUCC_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-pre-fail-flood" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-pre-fail-flood",
            payload["eapol-pre-fail-flood"],
            VALID_BODY_EAPOL_PRE_FAIL_FLOOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "windows-bridge" in payload:
        is_valid, error = _validate_enum_field(
            "windows-bridge",
            payload["windows-bridge"],
            VALID_BODY_WINDOWS_BRIDGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "disassoc-broadcast" in payload:
        is_valid, error = _validate_enum_field(
            "disassoc-broadcast",
            payload["disassoc-broadcast"],
            VALID_BODY_DISASSOC_BROADCAST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-spoofing" in payload:
        is_valid, error = _validate_enum_field(
            "ap-spoofing",
            payload["ap-spoofing"],
            VALID_BODY_AP_SPOOFING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "chan-based-mitm" in payload:
        is_valid, error = _validate_enum_field(
            "chan-based-mitm",
            payload["chan-based-mitm"],
            VALID_BODY_CHAN_BASED_MITM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adhoc-valid-ssid" in payload:
        is_valid, error = _validate_enum_field(
            "adhoc-valid-ssid",
            payload["adhoc-valid-ssid"],
            VALID_BODY_ADHOC_VALID_SSID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adhoc-network" in payload:
        is_valid, error = _validate_enum_field(
            "adhoc-network",
            payload["adhoc-network"],
            VALID_BODY_ADHOC_NETWORK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-key-overflow" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-key-overflow",
            payload["eapol-key-overflow"],
            VALID_BODY_EAPOL_KEY_OVERFLOW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-impersonation" in payload:
        is_valid, error = _validate_enum_field(
            "ap-impersonation",
            payload["ap-impersonation"],
            VALID_BODY_AP_IMPERSONATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "invalid-addr-combination" in payload:
        is_valid, error = _validate_enum_field(
            "invalid-addr-combination",
            payload["invalid-addr-combination"],
            VALID_BODY_INVALID_ADDR_COMBINATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "beacon-wrong-channel" in payload:
        is_valid, error = _validate_enum_field(
            "beacon-wrong-channel",
            payload["beacon-wrong-channel"],
            VALID_BODY_BEACON_WRONG_CHANNEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ht-greenfield" in payload:
        is_valid, error = _validate_enum_field(
            "ht-greenfield",
            payload["ht-greenfield"],
            VALID_BODY_HT_GREENFIELD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "overflow-ie" in payload:
        is_valid, error = _validate_enum_field(
            "overflow-ie",
            payload["overflow-ie"],
            VALID_BODY_OVERFLOW_IE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "malformed-ht-ie" in payload:
        is_valid, error = _validate_enum_field(
            "malformed-ht-ie",
            payload["malformed-ht-ie"],
            VALID_BODY_MALFORMED_HT_IE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "malformed-auth" in payload:
        is_valid, error = _validate_enum_field(
            "malformed-auth",
            payload["malformed-auth"],
            VALID_BODY_MALFORMED_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "malformed-association" in payload:
        is_valid, error = _validate_enum_field(
            "malformed-association",
            payload["malformed-association"],
            VALID_BODY_MALFORMED_ASSOCIATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ht-40mhz-intolerance" in payload:
        is_valid, error = _validate_enum_field(
            "ht-40mhz-intolerance",
            payload["ht-40mhz-intolerance"],
            VALID_BODY_HT_40MHZ_INTOLERANCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "valid-ssid-misuse" in payload:
        is_valid, error = _validate_enum_field(
            "valid-ssid-misuse",
            payload["valid-ssid-misuse"],
            VALID_BODY_VALID_SSID_MISUSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "valid-client-misassociation" in payload:
        is_valid, error = _validate_enum_field(
            "valid-client-misassociation",
            payload["valid-client-misassociation"],
            VALID_BODY_VALID_CLIENT_MISASSOCIATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "hotspotter-attack" in payload:
        is_valid, error = _validate_enum_field(
            "hotspotter-attack",
            payload["hotspotter-attack"],
            VALID_BODY_HOTSPOTTER_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pwsave-dos-attack" in payload:
        is_valid, error = _validate_enum_field(
            "pwsave-dos-attack",
            payload["pwsave-dos-attack"],
            VALID_BODY_PWSAVE_DOS_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "omerta-attack" in payload:
        is_valid, error = _validate_enum_field(
            "omerta-attack",
            payload["omerta-attack"],
            VALID_BODY_OMERTA_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "disconnect-station" in payload:
        is_valid, error = _validate_enum_field(
            "disconnect-station",
            payload["disconnect-station"],
            VALID_BODY_DISCONNECT_STATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unencrypted-valid" in payload:
        is_valid, error = _validate_enum_field(
            "unencrypted-valid",
            payload["unencrypted-valid"],
            VALID_BODY_UNENCRYPTED_VALID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fata-jack" in payload:
        is_valid, error = _validate_enum_field(
            "fata-jack",
            payload["fata-jack"],
            VALID_BODY_FATA_JACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "risky-encryption" in payload:
        is_valid, error = _validate_enum_field(
            "risky-encryption",
            payload["risky-encryption"],
            VALID_BODY_RISKY_ENCRYPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fuzzed-beacon" in payload:
        is_valid, error = _validate_enum_field(
            "fuzzed-beacon",
            payload["fuzzed-beacon"],
            VALID_BODY_FUZZED_BEACON,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fuzzed-probe-request" in payload:
        is_valid, error = _validate_enum_field(
            "fuzzed-probe-request",
            payload["fuzzed-probe-request"],
            VALID_BODY_FUZZED_PROBE_REQUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fuzzed-probe-response" in payload:
        is_valid, error = _validate_enum_field(
            "fuzzed-probe-response",
            payload["fuzzed-probe-response"],
            VALID_BODY_FUZZED_PROBE_RESPONSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "air-jack" in payload:
        is_valid, error = _validate_enum_field(
            "air-jack",
            payload["air-jack"],
            VALID_BODY_AIR_JACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wpa-ft-attack" in payload:
        is_valid, error = _validate_enum_field(
            "wpa-ft-attack",
            payload["wpa-ft-attack"],
            VALID_BODY_WPA_FT_ATTACK,
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
    "endpoint": "wireless_controller/wids_profile",
    "category": "cmdb",
    "api_path": "wireless-controller/wids-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure wireless intrusion detection system (WIDS) profiles.",
    "total_fields": 110,
    "required_fields_count": 0,
    "fields_with_defaults_count": 107,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
