""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: wireless_controller/hotspot20/hs_profile
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

class HsProfileOsuproviderItem(TypedDict, total=False):
    """Nested item for osu-provider field."""
    name: str


class HsProfilePayload(TypedDict, total=False):
    """Payload type for HsProfile operations."""
    name: str
    release: int
    access_network_type: Literal["private-network", "private-network-with-guest-access", "chargeable-public-network", "free-public-network", "personal-device-network", "emergency-services-only-network", "test-or-experimental", "wildcard"]
    access_network_internet: Literal["enable", "disable"]
    access_network_asra: Literal["enable", "disable"]
    access_network_esr: Literal["enable", "disable"]
    access_network_uesa: Literal["enable", "disable"]
    venue_group: Literal["unspecified", "assembly", "business", "educational", "factory", "institutional", "mercantile", "residential", "storage", "utility", "vehicular", "outdoor"]
    venue_type: Literal["unspecified", "arena", "stadium", "passenger-terminal", "amphitheater", "amusement-park", "place-of-worship", "convention-center", "library", "museum", "restaurant", "theater", "bar", "coffee-shop", "zoo-or-aquarium", "emergency-center", "doctor-office", "bank", "fire-station", "police-station", "post-office", "professional-office", "research-facility", "attorney-office", "primary-school", "secondary-school", "university-or-college", "factory", "hospital", "long-term-care-facility", "rehab-center", "group-home", "prison-or-jail", "retail-store", "grocery-market", "auto-service-station", "shopping-mall", "gas-station", "private", "hotel-or-motel", "dormitory", "boarding-house", "automobile", "airplane", "bus", "ferry", "ship-or-boat", "train", "motor-bike", "muni-mesh-network", "city-park", "rest-area", "traffic-control", "bus-stop", "kiosk"]
    hessid: str
    proxy_arp: Literal["enable", "disable"]
    l2tif: Literal["enable", "disable"]
    pame_bi: Literal["disable", "enable"]
    anqp_domain_id: int
    domain_name: str
    osu_ssid: str
    gas_comeback_delay: int
    gas_fragmentation_limit: int
    dgaf: Literal["enable", "disable"]
    deauth_request_timeout: int
    wnm_sleep_mode: Literal["enable", "disable"]
    bss_transition: Literal["enable", "disable"]
    venue_name: str
    venue_url: str
    roaming_consortium: str
    nai_realm: str
    oper_friendly_name: str
    oper_icon: str
    advice_of_charge: str
    osu_provider_nai: str
    terms_and_conditions: str
    osu_provider: str | list[str] | list[HsProfileOsuproviderItem]
    wan_metrics: str
    network_auth: str
    x3gpp_plmn: str
    conn_cap: str
    qos_map: str
    ip_addr_type: str
    wba_open_roaming: Literal["disable", "enable"]
    wba_financial_clearing_provider: str
    wba_data_clearing_provider: str
    wba_charging_currency: str
    wba_charging_rate: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class HsProfileResponse(TypedDict, total=False):
    """Response type for HsProfile - use with .dict property for typed dict access."""
    name: str
    release: int
    access_network_type: Literal["private-network", "private-network-with-guest-access", "chargeable-public-network", "free-public-network", "personal-device-network", "emergency-services-only-network", "test-or-experimental", "wildcard"]
    access_network_internet: Literal["enable", "disable"]
    access_network_asra: Literal["enable", "disable"]
    access_network_esr: Literal["enable", "disable"]
    access_network_uesa: Literal["enable", "disable"]
    venue_group: Literal["unspecified", "assembly", "business", "educational", "factory", "institutional", "mercantile", "residential", "storage", "utility", "vehicular", "outdoor"]
    venue_type: Literal["unspecified", "arena", "stadium", "passenger-terminal", "amphitheater", "amusement-park", "place-of-worship", "convention-center", "library", "museum", "restaurant", "theater", "bar", "coffee-shop", "zoo-or-aquarium", "emergency-center", "doctor-office", "bank", "fire-station", "police-station", "post-office", "professional-office", "research-facility", "attorney-office", "primary-school", "secondary-school", "university-or-college", "factory", "hospital", "long-term-care-facility", "rehab-center", "group-home", "prison-or-jail", "retail-store", "grocery-market", "auto-service-station", "shopping-mall", "gas-station", "private", "hotel-or-motel", "dormitory", "boarding-house", "automobile", "airplane", "bus", "ferry", "ship-or-boat", "train", "motor-bike", "muni-mesh-network", "city-park", "rest-area", "traffic-control", "bus-stop", "kiosk"]
    hessid: str
    proxy_arp: Literal["enable", "disable"]
    l2tif: Literal["enable", "disable"]
    pame_bi: Literal["disable", "enable"]
    anqp_domain_id: int
    domain_name: str
    osu_ssid: str
    gas_comeback_delay: int
    gas_fragmentation_limit: int
    dgaf: Literal["enable", "disable"]
    deauth_request_timeout: int
    wnm_sleep_mode: Literal["enable", "disable"]
    bss_transition: Literal["enable", "disable"]
    venue_name: str
    venue_url: str
    roaming_consortium: str
    nai_realm: str
    oper_friendly_name: str
    oper_icon: str
    advice_of_charge: str
    osu_provider_nai: str
    terms_and_conditions: str
    osu_provider: list[HsProfileOsuproviderItem]
    wan_metrics: str
    network_auth: str
    x3gpp_plmn: str
    conn_cap: str
    qos_map: str
    ip_addr_type: str
    wba_open_roaming: Literal["disable", "enable"]
    wba_financial_clearing_provider: str
    wba_data_clearing_provider: str
    wba_charging_currency: str
    wba_charging_rate: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class HsProfileOsuproviderItemObject(FortiObject[HsProfileOsuproviderItem]):
    """Typed object for osu-provider table items with attribute access."""
    name: str


class HsProfileObject(FortiObject):
    """Typed FortiObject for HsProfile with field access."""
    name: str
    release: int
    access_network_type: Literal["private-network", "private-network-with-guest-access", "chargeable-public-network", "free-public-network", "personal-device-network", "emergency-services-only-network", "test-or-experimental", "wildcard"]
    access_network_internet: Literal["enable", "disable"]
    access_network_asra: Literal["enable", "disable"]
    access_network_esr: Literal["enable", "disable"]
    access_network_uesa: Literal["enable", "disable"]
    venue_group: Literal["unspecified", "assembly", "business", "educational", "factory", "institutional", "mercantile", "residential", "storage", "utility", "vehicular", "outdoor"]
    venue_type: Literal["unspecified", "arena", "stadium", "passenger-terminal", "amphitheater", "amusement-park", "place-of-worship", "convention-center", "library", "museum", "restaurant", "theater", "bar", "coffee-shop", "zoo-or-aquarium", "emergency-center", "doctor-office", "bank", "fire-station", "police-station", "post-office", "professional-office", "research-facility", "attorney-office", "primary-school", "secondary-school", "university-or-college", "factory", "hospital", "long-term-care-facility", "rehab-center", "group-home", "prison-or-jail", "retail-store", "grocery-market", "auto-service-station", "shopping-mall", "gas-station", "private", "hotel-or-motel", "dormitory", "boarding-house", "automobile", "airplane", "bus", "ferry", "ship-or-boat", "train", "motor-bike", "muni-mesh-network", "city-park", "rest-area", "traffic-control", "bus-stop", "kiosk"]
    hessid: str
    proxy_arp: Literal["enable", "disable"]
    l2tif: Literal["enable", "disable"]
    pame_bi: Literal["disable", "enable"]
    anqp_domain_id: int
    domain_name: str
    osu_ssid: str
    gas_comeback_delay: int
    gas_fragmentation_limit: int
    dgaf: Literal["enable", "disable"]
    deauth_request_timeout: int
    wnm_sleep_mode: Literal["enable", "disable"]
    bss_transition: Literal["enable", "disable"]
    venue_name: str
    venue_url: str
    roaming_consortium: str
    nai_realm: str
    oper_friendly_name: str
    oper_icon: str
    advice_of_charge: str
    osu_provider_nai: str
    terms_and_conditions: str
    osu_provider: FortiObjectList[HsProfileOsuproviderItemObject]
    wan_metrics: str
    network_auth: str
    x3gpp_plmn: str
    conn_cap: str
    qos_map: str
    ip_addr_type: str
    wba_open_roaming: Literal["disable", "enable"]
    wba_financial_clearing_provider: str
    wba_data_clearing_provider: str
    wba_charging_currency: str
    wba_charging_rate: int


# ================================================================
# Main Endpoint Class
# ================================================================

class HsProfile:
    """
    
    Endpoint: wireless_controller/hotspot20/hs_profile
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
    ) -> HsProfileObject: ...
    
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
    ) -> FortiObjectList[HsProfileObject]: ...
    
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
        payload_dict: HsProfilePayload | None = ...,
        name: str | None = ...,
        release: int | None = ...,
        access_network_type: Literal["private-network", "private-network-with-guest-access", "chargeable-public-network", "free-public-network", "personal-device-network", "emergency-services-only-network", "test-or-experimental", "wildcard"] | None = ...,
        access_network_internet: Literal["enable", "disable"] | None = ...,
        access_network_asra: Literal["enable", "disable"] | None = ...,
        access_network_esr: Literal["enable", "disable"] | None = ...,
        access_network_uesa: Literal["enable", "disable"] | None = ...,
        venue_group: Literal["unspecified", "assembly", "business", "educational", "factory", "institutional", "mercantile", "residential", "storage", "utility", "vehicular", "outdoor"] | None = ...,
        venue_type: Literal["unspecified", "arena", "stadium", "passenger-terminal", "amphitheater", "amusement-park", "place-of-worship", "convention-center", "library", "museum", "restaurant", "theater", "bar", "coffee-shop", "zoo-or-aquarium", "emergency-center", "doctor-office", "bank", "fire-station", "police-station", "post-office", "professional-office", "research-facility", "attorney-office", "primary-school", "secondary-school", "university-or-college", "factory", "hospital", "long-term-care-facility", "rehab-center", "group-home", "prison-or-jail", "retail-store", "grocery-market", "auto-service-station", "shopping-mall", "gas-station", "private", "hotel-or-motel", "dormitory", "boarding-house", "automobile", "airplane", "bus", "ferry", "ship-or-boat", "train", "motor-bike", "muni-mesh-network", "city-park", "rest-area", "traffic-control", "bus-stop", "kiosk"] | None = ...,
        hessid: str | None = ...,
        proxy_arp: Literal["enable", "disable"] | None = ...,
        l2tif: Literal["enable", "disable"] | None = ...,
        pame_bi: Literal["disable", "enable"] | None = ...,
        anqp_domain_id: int | None = ...,
        domain_name: str | None = ...,
        osu_ssid: str | None = ...,
        gas_comeback_delay: int | None = ...,
        gas_fragmentation_limit: int | None = ...,
        dgaf: Literal["enable", "disable"] | None = ...,
        deauth_request_timeout: int | None = ...,
        wnm_sleep_mode: Literal["enable", "disable"] | None = ...,
        bss_transition: Literal["enable", "disable"] | None = ...,
        venue_name: str | None = ...,
        venue_url: str | None = ...,
        roaming_consortium: str | None = ...,
        nai_realm: str | None = ...,
        oper_friendly_name: str | None = ...,
        oper_icon: str | None = ...,
        advice_of_charge: str | None = ...,
        osu_provider_nai: str | None = ...,
        terms_and_conditions: str | None = ...,
        osu_provider: str | list[str] | list[HsProfileOsuproviderItem] | None = ...,
        wan_metrics: str | None = ...,
        network_auth: str | None = ...,
        x3gpp_plmn: str | None = ...,
        conn_cap: str | None = ...,
        qos_map: str | None = ...,
        ip_addr_type: str | None = ...,
        wba_open_roaming: Literal["disable", "enable"] | None = ...,
        wba_financial_clearing_provider: str | None = ...,
        wba_data_clearing_provider: str | None = ...,
        wba_charging_currency: str | None = ...,
        wba_charging_rate: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> HsProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: HsProfilePayload | None = ...,
        name: str | None = ...,
        release: int | None = ...,
        access_network_type: Literal["private-network", "private-network-with-guest-access", "chargeable-public-network", "free-public-network", "personal-device-network", "emergency-services-only-network", "test-or-experimental", "wildcard"] | None = ...,
        access_network_internet: Literal["enable", "disable"] | None = ...,
        access_network_asra: Literal["enable", "disable"] | None = ...,
        access_network_esr: Literal["enable", "disable"] | None = ...,
        access_network_uesa: Literal["enable", "disable"] | None = ...,
        venue_group: Literal["unspecified", "assembly", "business", "educational", "factory", "institutional", "mercantile", "residential", "storage", "utility", "vehicular", "outdoor"] | None = ...,
        venue_type: Literal["unspecified", "arena", "stadium", "passenger-terminal", "amphitheater", "amusement-park", "place-of-worship", "convention-center", "library", "museum", "restaurant", "theater", "bar", "coffee-shop", "zoo-or-aquarium", "emergency-center", "doctor-office", "bank", "fire-station", "police-station", "post-office", "professional-office", "research-facility", "attorney-office", "primary-school", "secondary-school", "university-or-college", "factory", "hospital", "long-term-care-facility", "rehab-center", "group-home", "prison-or-jail", "retail-store", "grocery-market", "auto-service-station", "shopping-mall", "gas-station", "private", "hotel-or-motel", "dormitory", "boarding-house", "automobile", "airplane", "bus", "ferry", "ship-or-boat", "train", "motor-bike", "muni-mesh-network", "city-park", "rest-area", "traffic-control", "bus-stop", "kiosk"] | None = ...,
        hessid: str | None = ...,
        proxy_arp: Literal["enable", "disable"] | None = ...,
        l2tif: Literal["enable", "disable"] | None = ...,
        pame_bi: Literal["disable", "enable"] | None = ...,
        anqp_domain_id: int | None = ...,
        domain_name: str | None = ...,
        osu_ssid: str | None = ...,
        gas_comeback_delay: int | None = ...,
        gas_fragmentation_limit: int | None = ...,
        dgaf: Literal["enable", "disable"] | None = ...,
        deauth_request_timeout: int | None = ...,
        wnm_sleep_mode: Literal["enable", "disable"] | None = ...,
        bss_transition: Literal["enable", "disable"] | None = ...,
        venue_name: str | None = ...,
        venue_url: str | None = ...,
        roaming_consortium: str | None = ...,
        nai_realm: str | None = ...,
        oper_friendly_name: str | None = ...,
        oper_icon: str | None = ...,
        advice_of_charge: str | None = ...,
        osu_provider_nai: str | None = ...,
        terms_and_conditions: str | None = ...,
        osu_provider: str | list[str] | list[HsProfileOsuproviderItem] | None = ...,
        wan_metrics: str | None = ...,
        network_auth: str | None = ...,
        x3gpp_plmn: str | None = ...,
        conn_cap: str | None = ...,
        qos_map: str | None = ...,
        ip_addr_type: str | None = ...,
        wba_open_roaming: Literal["disable", "enable"] | None = ...,
        wba_financial_clearing_provider: str | None = ...,
        wba_data_clearing_provider: str | None = ...,
        wba_charging_currency: str | None = ...,
        wba_charging_rate: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> HsProfileObject: ...

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
        payload_dict: HsProfilePayload | None = ...,
        name: str | None = ...,
        release: int | None = ...,
        access_network_type: Literal["private-network", "private-network-with-guest-access", "chargeable-public-network", "free-public-network", "personal-device-network", "emergency-services-only-network", "test-or-experimental", "wildcard"] | None = ...,
        access_network_internet: Literal["enable", "disable"] | None = ...,
        access_network_asra: Literal["enable", "disable"] | None = ...,
        access_network_esr: Literal["enable", "disable"] | None = ...,
        access_network_uesa: Literal["enable", "disable"] | None = ...,
        venue_group: Literal["unspecified", "assembly", "business", "educational", "factory", "institutional", "mercantile", "residential", "storage", "utility", "vehicular", "outdoor"] | None = ...,
        venue_type: Literal["unspecified", "arena", "stadium", "passenger-terminal", "amphitheater", "amusement-park", "place-of-worship", "convention-center", "library", "museum", "restaurant", "theater", "bar", "coffee-shop", "zoo-or-aquarium", "emergency-center", "doctor-office", "bank", "fire-station", "police-station", "post-office", "professional-office", "research-facility", "attorney-office", "primary-school", "secondary-school", "university-or-college", "factory", "hospital", "long-term-care-facility", "rehab-center", "group-home", "prison-or-jail", "retail-store", "grocery-market", "auto-service-station", "shopping-mall", "gas-station", "private", "hotel-or-motel", "dormitory", "boarding-house", "automobile", "airplane", "bus", "ferry", "ship-or-boat", "train", "motor-bike", "muni-mesh-network", "city-park", "rest-area", "traffic-control", "bus-stop", "kiosk"] | None = ...,
        hessid: str | None = ...,
        proxy_arp: Literal["enable", "disable"] | None = ...,
        l2tif: Literal["enable", "disable"] | None = ...,
        pame_bi: Literal["disable", "enable"] | None = ...,
        anqp_domain_id: int | None = ...,
        domain_name: str | None = ...,
        osu_ssid: str | None = ...,
        gas_comeback_delay: int | None = ...,
        gas_fragmentation_limit: int | None = ...,
        dgaf: Literal["enable", "disable"] | None = ...,
        deauth_request_timeout: int | None = ...,
        wnm_sleep_mode: Literal["enable", "disable"] | None = ...,
        bss_transition: Literal["enable", "disable"] | None = ...,
        venue_name: str | None = ...,
        venue_url: str | None = ...,
        roaming_consortium: str | None = ...,
        nai_realm: str | None = ...,
        oper_friendly_name: str | None = ...,
        oper_icon: str | None = ...,
        advice_of_charge: str | None = ...,
        osu_provider_nai: str | None = ...,
        terms_and_conditions: str | None = ...,
        osu_provider: str | list[str] | list[HsProfileOsuproviderItem] | None = ...,
        wan_metrics: str | None = ...,
        network_auth: str | None = ...,
        x3gpp_plmn: str | None = ...,
        conn_cap: str | None = ...,
        qos_map: str | None = ...,
        ip_addr_type: str | None = ...,
        wba_open_roaming: Literal["disable", "enable"] | None = ...,
        wba_financial_clearing_provider: str | None = ...,
        wba_data_clearing_provider: str | None = ...,
        wba_charging_currency: str | None = ...,
        wba_charging_rate: int | None = ...,
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
    "HsProfile",
    "HsProfilePayload",
    "HsProfileResponse",
    "HsProfileObject",
]