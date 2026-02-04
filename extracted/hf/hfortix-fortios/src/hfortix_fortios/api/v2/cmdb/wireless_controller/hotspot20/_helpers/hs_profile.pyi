from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_ACCESS_NETWORK_TYPE: Literal["private-network", "private-network-with-guest-access", "chargeable-public-network", "free-public-network", "personal-device-network", "emergency-services-only-network", "test-or-experimental", "wildcard"]
VALID_BODY_ACCESS_NETWORK_INTERNET: Literal["enable", "disable"]
VALID_BODY_ACCESS_NETWORK_ASRA: Literal["enable", "disable"]
VALID_BODY_ACCESS_NETWORK_ESR: Literal["enable", "disable"]
VALID_BODY_ACCESS_NETWORK_UESA: Literal["enable", "disable"]
VALID_BODY_VENUE_GROUP: Literal["unspecified", "assembly", "business", "educational", "factory", "institutional", "mercantile", "residential", "storage", "utility", "vehicular", "outdoor"]
VALID_BODY_VENUE_TYPE: Literal["unspecified", "arena", "stadium", "passenger-terminal", "amphitheater", "amusement-park", "place-of-worship", "convention-center", "library", "museum", "restaurant", "theater", "bar", "coffee-shop", "zoo-or-aquarium", "emergency-center", "doctor-office", "bank", "fire-station", "police-station", "post-office", "professional-office", "research-facility", "attorney-office", "primary-school", "secondary-school", "university-or-college", "factory", "hospital", "long-term-care-facility", "rehab-center", "group-home", "prison-or-jail", "retail-store", "grocery-market", "auto-service-station", "shopping-mall", "gas-station", "private", "hotel-or-motel", "dormitory", "boarding-house", "automobile", "airplane", "bus", "ferry", "ship-or-boat", "train", "motor-bike", "muni-mesh-network", "city-park", "rest-area", "traffic-control", "bus-stop", "kiosk"]
VALID_BODY_PROXY_ARP: Literal["enable", "disable"]
VALID_BODY_L2TIF: Literal["enable", "disable"]
VALID_BODY_PAME_BI: Literal["disable", "enable"]
VALID_BODY_DGAF: Literal["enable", "disable"]
VALID_BODY_WNM_SLEEP_MODE: Literal["enable", "disable"]
VALID_BODY_BSS_TRANSITION: Literal["enable", "disable"]
VALID_BODY_WBA_OPEN_ROAMING: Literal["disable", "enable"]

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
    "VALID_BODY_ACCESS_NETWORK_TYPE",
    "VALID_BODY_ACCESS_NETWORK_INTERNET",
    "VALID_BODY_ACCESS_NETWORK_ASRA",
    "VALID_BODY_ACCESS_NETWORK_ESR",
    "VALID_BODY_ACCESS_NETWORK_UESA",
    "VALID_BODY_VENUE_GROUP",
    "VALID_BODY_VENUE_TYPE",
    "VALID_BODY_PROXY_ARP",
    "VALID_BODY_L2TIF",
    "VALID_BODY_PAME_BI",
    "VALID_BODY_DGAF",
    "VALID_BODY_WNM_SLEEP_MODE",
    "VALID_BODY_BSS_TRANSITION",
    "VALID_BODY_WBA_OPEN_ROAMING",
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