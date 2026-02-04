"""
FortiOS CMDB - Wireless_controller wtp_profile

Configuration endpoint for managing cmdb wireless_controller/wtp_profile objects.

API Endpoints:
    GET    /cmdb/wireless_controller/wtp_profile
    POST   /cmdb/wireless_controller/wtp_profile
    PUT    /cmdb/wireless_controller/wtp_profile/{identifier}
    DELETE /cmdb/wireless_controller/wtp_profile/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.wireless_controller_wtp_profile.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.wireless_controller_wtp_profile.post(
    ...     name="example",
    ...     srcintf="port1",  # Auto-converted to [{'name': 'port1'}]
    ...     dstintf=["port2", "port3"],  # Auto-converted to list of dicts
    ... )

Important:
    - Use **POST** to create new objects
    - Use **PUT** to update existing objects
    - Use **GET** to retrieve configuration
    - Use **DELETE** to remove objects
    - **Auto-normalization**: List fields accept strings or lists, automatically
      converted to FortiOS format [{'name': '...'}]
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Union

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from hfortix_core.http.interface import IHTTPClient
    from hfortix_fortios.models import FortiObject, FortiObjectList

# Import helper functions from central _helpers module
from hfortix_fortios._helpers import (
    build_api_payload,
    build_cmdb_payload,  # Keep for backward compatibility / manual usage
    is_success,
    quote_path_param,  # URL encoding for path parameters
    normalize_table_field,  # For table field normalization
)
# Import metadata mixin for schema introspection
from hfortix_fortios._helpers.metadata_mixin import MetadataMixin

# Import Protocol-based type hints (eliminates need for local @overload decorators)
from hfortix_fortios._protocols import CRUDEndpoint

class WtpProfile(CRUDEndpoint, MetadataMixin):
    """WtpProfile Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "wtp_profile"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "led_schedules": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "deny_mac_list": {
            "mkey": "id",
            "required_fields": ['id'],
            "example": "[{'id': 1}]",
        },
        "split_tunneling_acl": {
            "mkey": "id",
            "required_fields": ['dest-ip'],
            "example": "[{'dest-ip': 'value'}]",
        },
    }
    
    # ========================================================================
    # Capabilities (from schema metadata)
    # ========================================================================
    SUPPORTS_CREATE = True
    SUPPORTS_READ = True
    SUPPORTS_UPDATE = True
    SUPPORTS_DELETE = True
    SUPPORTS_MOVE = True
    # SUPPORTS_CLONE = True  # Disabled - unreliable across endpoints
    SUPPORTS_FILTERING = True
    SUPPORTS_PAGINATION = True
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize WtpProfile endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: str | None = None,
        format: str | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve wireless_controller/wtp_profile configuration.

        Configure WTP profiles or FortiAP profiles that define radio settings for manageable FortiAP platforms.

        Args:
            name: String identifier to retrieve specific object.
                If None, returns all objects.
            filter: List of filter expressions to limit results.
                Each filter uses format: "field==value" or "field!=value"
                Operators: ==, !=, =@ (contains), !@ (not contains), <=, <, >=, >
                Multiple filters use AND logic. For OR, use comma in single string.
                Example: ["name==test", "status==enable"] or ["name==test,name==prod"]
            sort: Sort results by field. Format: "field" or "field,asc" or "field,dsc"
                Example: "name" (ascending) or "name,dsc" (descending)
                Multiple sorts: Use multiple sort parameters in order of priority
            format: Return only specific fields. Format: "field1|field2|field3"
                Example: "name|type|subnet"
            count: Maximum number of entries to return (pagination).
            start: Starting entry index for pagination (0-based).
            payload_dict: Additional query parameters for advanced options:
                - datasource (bool): Include datasource information
                - with_meta (bool): Include metadata about each object
                - with_contents_hash (bool): Include checksum of object contents
                - scope (str): Query scope - "global", "vdom", or "both"
                - action (str): Special actions - "schema", "default"
                See FortiOS REST API documentation for complete list.
            vdom: Virtual domain name. Use True for global, string for specific VDOM, None for default.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.
            Access results via dictionary keys (e.g., result['results'], result['http_status']).
            
            Response structure:
                - http_method: GET
                - results: Configuration object(s)
                - vdom: Virtual domain
                - path: API path
                - name: Object name (single object queries)
                - status: success/error
                - http_status: HTTP status code
                - build: FortiOS build number

        Examples:
            >>> # Get all wireless_controller/wtp_profile objects
            >>> result = fgt.api.cmdb.wireless_controller_wtp_profile.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific wireless_controller/wtp_profile by name
            >>> result = fgt.api.cmdb.wireless_controller_wtp_profile.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.wireless_controller_wtp_profile.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.wireless_controller_wtp_profile.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.wireless_controller_wtp_profile.get_schema()

        See Also:
            - post(): Create new wireless_controller/wtp_profile object
            - put(): Update existing wireless_controller/wtp_profile object
            - delete(): Remove wireless_controller/wtp_profile object
            - exists(): Check if object exists
            - get_schema(): Get endpoint schema/metadata
        """
        params = payload_dict.copy() if payload_dict else {}
        
        # Add explicit query parameters
        # Handle filter parameter specially to support FortiOS AND syntax with multiple filters
        # FortiOS uses: ?filter=a&filter=b for AND operations
        # Normalize filter syntax to support all common formats:
        #   1. name=@test&name!@web (implicit & separator)
        #   2. name=@test&filter=name!@web (mixed implicit/explicit)
        #   3. filter=name=@test&filter=name!@web (explicit with filter= prefix)
        #   4. filter=name=@test&name!@web (explicit prefix with implicit separator)
        if filter is not None:
            normalized_filter = filter
            
            # Step 1: Remove leading "filter=" if present (normalize input format)
            # "filter=name=@test&..." -> "name=@test&..."
            if normalized_filter.startswith("filter="):
                normalized_filter = normalized_filter[7:]  # Remove "filter=" prefix
            
            # Step 2: Normalize & separators to &filter=
            # This handles all variations: "a&b", "a&filter=b", etc.
            if "&" in normalized_filter:
                # Split on both & and &filter= to get all filter parts
                # Then rejoin with &filter= for consistency
                parts = []
                current = normalized_filter
                
                # Split on &filter= first to preserve already-explicit parts
                while "&filter=" in current:
                    before, after = current.split("&filter=", 1)
                    # Now split 'before' on & if it contains any
                    if "&" in before:
                        parts.extend(before.split("&"))
                    else:
                        parts.append(before)
                    current = after
                
                # Handle remaining part (after last &filter= or the whole string if no &filter=)
                if "&" in current:
                    parts.extend(current.split("&"))
                else:
                    parts.append(current)
                
                # Rejoin with &filter= separator
                if len(parts) > 1:
                    normalized_filter = parts[0] + "".join(f"&filter={part}" for part in parts[1:])
            
            # Step 3: Check if we have multiple filters (AND operation)
            if "&filter=" in normalized_filter:
                # Multiple filters for AND operation: "filter1&filter=filter2&filter=filter3"
                # Split and create list of filter values
                filters = [normalized_filter.split("&filter=")[0]]  # First filter before &filter=
                filters.extend(normalized_filter.split("&filter=")[1:])  # Remaining filters after each &filter=
                params["filter"] = filters
            else:
                params["filter"] = normalized_filter
        if sort is not None:
            params["sort"] = sort
        if format is not None:
            params["format"] = format
        if count is not None:
            params["count"] = count
        if start is not None:
            params["start"] = start
        
        if name:
            endpoint = "/wireless-controller/wtp-profile/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/wireless-controller/wtp-profile"
            unwrap_single = False
        
        return self._client.get(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=vdom, unwrap_single=unwrap_single
        )

    def get_schema(
        self,
        vdom: str | None = None,
        format: str = "schema",
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Get schema/metadata for this endpoint.
        
        Returns the FortiOS schema definition including available fields,
        their types, required vs optional properties, enum values, nested
        structures, and default values.
        
        This queries the live firewall for its current schema, which may
        vary between FortiOS versions.
        
        Args:
            vdom: Virtual domain. None uses default VDOM.
            format: Schema format - "schema" (FortiOS native) or "json-schema" (JSON Schema standard).
                Defaults to "schema".
                
        Returns:
            Schema definition as dict. Returns Coroutine if using async client.
            
        Example:
            >>> # Get FortiOS native schema
            >>> schema = fgt.api.cmdb.wireless_controller_wtp_profile.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.wireless_controller_wtp_profile.get_schema(format="json-schema")
        
        Note:
            Not all endpoints support all schema formats. The "schema" format
            is most widely supported.
        """
        return self.get(payload_dict={"action": format}, vdom=vdom)


    # ========================================================================
    # PUT Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Field-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def put(  # type: ignore[override]
        self,
        payload_dict: dict[str, Any] | None = None,
        name: str | None = None,
        comment: str | None = None,
        platform: str | None = None,
        control_message_offload: Literal["ebp-frame", "aeroscout-tag", "ap-list", "sta-list", "sta-cap-list", "stats", "aeroscout-mu", "sta-health", "spectral-analysis"] | list[str] | None = None,
        bonjour_profile: str | None = None,
        apcfg_profile: str | None = None,
        apcfg_mesh: Literal["enable", "disable"] | None = None,
        apcfg_mesh_ap_type: Literal["ethernet", "mesh", "auto"] | None = None,
        apcfg_mesh_ssid: str | None = None,
        apcfg_mesh_eth_bridge: Literal["enable", "disable"] | None = None,
        ble_profile: str | None = None,
        lw_profile: str | None = None,
        syslog_profile: str | None = None,
        wan_port_mode: Literal["wan-lan", "wan-only"] | None = None,
        lan: str | None = None,
        energy_efficient_ethernet: Literal["enable", "disable"] | None = None,
        led_state: Literal["enable", "disable"] | None = None,
        led_schedules: str | list[str] | list[dict[str, Any]] | None = None,
        dtls_policy: Literal["clear-text", "dtls-enabled", "ipsec-vpn", "ipsec-sn-vpn"] | list[str] | None = None,
        dtls_in_kernel: Literal["enable", "disable"] | None = None,
        max_clients: int | None = None,
        handoff_rssi: int | None = None,
        handoff_sta_thresh: int | None = None,
        handoff_roaming: Literal["enable", "disable"] | None = None,
        deny_mac_list: str | list[str] | list[dict[str, Any]] | None = None,
        ap_country: Literal["--", "AF", "AL", "DZ", "AS", "AO", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "KH", "CM", "KY", "CF", "TD", "CL", "CN", "CX", "CO", "CG", "CD", "CR", "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "ET", "EE", "GF", "PF", "FO", "FJ", "FI", "FR", "GA", "GE", "GM", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "CI", "JM", "JO", "KZ", "KE", "KR", "KW", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "MA", "MZ", "MM", "NA", "NP", "NL", "AN", "AW", "NZ", "NI", "NE", "NG", "NO", "MP", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "KN", "LC", "MF", "PM", "VC", "SA", "SN", "RS", "ME", "SL", "SG", "SK", "SI", "SO", "ZA", "ES", "LK", "SR", "SZ", "SE", "CH", "TW", "TZ", "TH", "TL", "TG", "TT", "TN", "TR", "TM", "AE", "TC", "UG", "UA", "GB", "US", "PS", "UY", "UZ", "VU", "VE", "VN", "VI", "WF", "YE", "ZM", "ZW", "JP", "CA"] | None = None,
        ip_fragment_preventing: Literal["tcp-mss-adjust", "icmp-unreachable"] | list[str] | None = None,
        tun_mtu_uplink: int | None = None,
        tun_mtu_downlink: int | None = None,
        split_tunneling_acl_path: Literal["tunnel", "local"] | None = None,
        split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"] | None = None,
        split_tunneling_acl: str | list[str] | list[dict[str, Any]] | None = None,
        allowaccess: Literal["https", "ssh", "snmp"] | list[str] | None = None,
        login_passwd_change: Literal["yes", "default", "no"] | None = None,
        login_passwd: Any | None = None,
        lldp: Literal["enable", "disable"] | None = None,
        poe_mode: Literal["auto", "8023af", "8023at", "power-adapter", "full", "high", "low"] | None = None,
        usb_port: Literal["enable", "disable"] | None = None,
        frequency_handoff: Literal["enable", "disable"] | None = None,
        ap_handoff: Literal["enable", "disable"] | None = None,
        default_mesh_root: Literal["enable", "disable"] | None = None,
        radio_1: str | None = None,
        radio_2: str | None = None,
        radio_3: str | None = None,
        radio_4: str | None = None,
        lbs: str | None = None,
        ext_info_enable: Literal["enable", "disable"] | None = None,
        indoor_outdoor_deployment: Literal["platform-determined", "outdoor", "indoor"] | None = None,
        esl_ses_dongle: str | None = None,
        console_login: Literal["enable", "disable"] | None = None,
        wan_port_auth: Literal["none", "802.1x"] | None = None,
        wan_port_auth_usrname: str | None = None,
        wan_port_auth_password: Any | None = None,
        wan_port_auth_methods: Literal["all", "EAP-FAST", "EAP-TLS", "EAP-PEAP"] | None = None,
        wan_port_auth_macsec: Literal["enable", "disable"] | None = None,
        apcfg_auto_cert: Literal["enable", "disable"] | None = None,
        apcfg_auto_cert_enroll_protocol: Literal["none", "est", "scep"] | None = None,
        apcfg_auto_cert_crypto_algo: Literal["rsa-1024", "rsa-1536", "rsa-2048", "rsa-4096", "ec-secp256r1", "ec-secp384r1", "ec-secp521r1"] | None = None,
        apcfg_auto_cert_est_server: str | None = None,
        apcfg_auto_cert_est_ca_id: str | None = None,
        apcfg_auto_cert_est_http_username: str | None = None,
        apcfg_auto_cert_est_http_password: Any | None = None,
        apcfg_auto_cert_est_subject: str | None = None,
        apcfg_auto_cert_est_subject_alt_name: str | None = None,
        apcfg_auto_cert_auto_regen_days: int | None = None,
        apcfg_auto_cert_est_https_ca: str | None = None,
        apcfg_auto_cert_scep_keytype: Literal["rsa", "ec"] | None = None,
        apcfg_auto_cert_scep_keysize: Literal["1024", "1536", "2048", "4096"] | None = None,
        apcfg_auto_cert_scep_ec_name: Literal["secp256r1", "secp384r1", "secp521r1"] | None = None,
        apcfg_auto_cert_scep_sub_fully_dn: str | None = None,
        apcfg_auto_cert_scep_url: str | None = None,
        apcfg_auto_cert_scep_password: Any | None = None,
        apcfg_auto_cert_scep_ca_id: str | None = None,
        apcfg_auto_cert_scep_subject_alt_name: str | None = None,
        apcfg_auto_cert_scep_https_ca: str | None = None,
        unii_4_5ghz_band: Literal["enable", "disable"] | None = None,
        admin_auth_tacacs_plus: str | None = None,
        admin_restrict_local: Literal["enable", "disable"] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing wireless_controller/wtp_profile object.

        Configure WTP profiles or FortiAP profiles that define radio settings for manageable FortiAP platforms.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: WTP (or FortiAP or AP) profile name.
            comment: Comment.
            platform: WTP, FortiAP, or AP platform.
            control_message_offload: Enable/disable CAPWAP control message data channel offload.
            bonjour_profile: Bonjour profile name.
            apcfg_profile: AP local configuration profile name.
            apcfg_mesh: Enable/disable AP local mesh configuration (default = disable).
            apcfg_mesh_ap_type: Mesh AP Type (default = ethernet).
            apcfg_mesh_ssid:  Mesh SSID (default = none).
            apcfg_mesh_eth_bridge: Enable/disable mesh ethernet bridge (default = disable).
            ble_profile: Bluetooth Low Energy profile name.
            lw_profile: LoRaWAN profile name.
            syslog_profile: System log server configuration profile name.
            wan_port_mode: Enable/disable using a WAN port as a LAN port.
            lan: WTP LAN port mapping.
            energy_efficient_ethernet: Enable/disable use of energy efficient Ethernet on WTP.
            led_state: Enable/disable use of LEDs on WTP (default = enable).
            led_schedules: Recurring firewall schedules for illuminating LEDs on the FortiAP. If led-state is enabled, LEDs will be visible when at least one of the schedules is valid. Separate multiple schedule names with a space.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            dtls_policy: WTP data channel DTLS policy (default = clear-text).
            dtls_in_kernel: Enable/disable data channel DTLS in kernel.
            max_clients: Maximum number of stations (STAs) supported by the WTP (default = 0, meaning no client limitation).
            handoff_rssi: Minimum received signal strength indicator (RSSI) value for handoff (20 - 30, default = 25).
            handoff_sta_thresh: Threshold value for AP handoff.
            handoff_roaming: Enable/disable client load balancing during roaming to avoid roaming delay (default = enable).
            deny_mac_list: List of MAC addresses that are denied access to this WTP, FortiAP, or AP.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            ap_country: Country in which this WTP, FortiAP, or AP will operate (default = NA, automatically use the country configured for the current VDOM).
            ip_fragment_preventing: Method(s) by which IP fragmentation is prevented for control and data packets through CAPWAP tunnel (default = tcp-mss-adjust).
            tun_mtu_uplink: The maximum transmission unit (MTU) of uplink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU of FortiAP; default = 0).
            tun_mtu_downlink: The MTU of downlink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU of FortiAP; default = 0).
            split_tunneling_acl_path: Split tunneling ACL path is local/tunnel.
            split_tunneling_acl_local_ap_subnet: Enable/disable automatically adding local subnetwork of FortiAP to split-tunneling ACL (default = disable).
            split_tunneling_acl: Split tunneling ACL filter list.
                Default format: [{'dest-ip': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'dest-ip': 'value'}] (recommended)
            allowaccess: Control management access to the managed WTP, FortiAP, or AP. Separate entries with a space.
            login_passwd_change: Change or reset the administrator password of a managed WTP, FortiAP or AP (yes, default, or no, default = no).
            login_passwd: Set the managed WTP, FortiAP, or AP's administrator password.
            lldp: Enable/disable Link Layer Discovery Protocol (LLDP) for the WTP, FortiAP, or AP (default = enable).
            poe_mode: Set the WTP, FortiAP, or AP's PoE mode.
            usb_port: Enable/disable USB port of the WTP (default = enable).
            frequency_handoff: Enable/disable frequency handoff of clients to other channels (default = disable).
            ap_handoff: Enable/disable AP handoff of clients to other APs (default = disable).
            default_mesh_root: Configure default mesh root SSID when it is not included by radio's SSID configuration.
            radio_1: Configuration options for radio 1.
            radio_2: Configuration options for radio 2.
            radio_3: Configuration options for radio 3.
            radio_4: Configuration options for radio 4.
            lbs: Set various location based service (LBS) options.
            ext_info_enable: Enable/disable station/VAP/radio extension information.
            indoor_outdoor_deployment: Set to allow indoor/outdoor-only channels under regulatory rules (default = platform-determined).
            esl_ses_dongle: ESL SES-imagotag dongle configuration.
            console_login: Enable/disable FortiAP console login access (default = enable).
            wan_port_auth: Set WAN port authentication mode (default = none).
            wan_port_auth_usrname: Set WAN port 802.1x supplicant user name.
            wan_port_auth_password: Set WAN port 802.1x supplicant password.
            wan_port_auth_methods: WAN port 802.1x supplicant EAP methods (default = all).
            wan_port_auth_macsec: Enable/disable WAN port 802.1x supplicant MACsec policy (default = disable).
            apcfg_auto_cert: Enable/disable AP local auto cert configuration (default = disable).
            apcfg_auto_cert_enroll_protocol: Certificate enrollment protocol (default = none)
            apcfg_auto_cert_crypto_algo: Cryptography algorithm: rsa-1024, rsa-1536, rsa-2048, rsa-4096, ec-secp256r1, ec-secp384r1, ec-secp521r1 (default = ec-secp256r1)
            apcfg_auto_cert_est_server: Address and port for EST server (e.g. https://example.com:1234).
            apcfg_auto_cert_est_ca_id: CA identifier of the CA server for signing via EST.
            apcfg_auto_cert_est_http_username: HTTP Authentication username for signing via EST.
            apcfg_auto_cert_est_http_password: HTTP Authentication password for signing via EST.
            apcfg_auto_cert_est_subject: Subject e.g. "CN=User,DC=example,DC=COM" (default = CN=FortiAP,DC=local,DC=COM)
            apcfg_auto_cert_est_subject_alt_name: Subject alternative name (optional, e.g. "DNS:dns1.com,IP:192.168.1.99")
            apcfg_auto_cert_auto_regen_days: Number of days to wait before expiry of an updated local certificate is requested (0 = disabled) (default = 30).
            apcfg_auto_cert_est_https_ca: PEM format https CA Certificate.
            apcfg_auto_cert_scep_keytype: Key type (default = rsa)
            apcfg_auto_cert_scep_keysize: Key size: 1024, 1536, 2048, 4096 (default 2048).
            apcfg_auto_cert_scep_ec_name: Elliptic curve name: secp256r1, secp384r1 and secp521r1. (default secp256r1).
            apcfg_auto_cert_scep_sub_fully_dn: Full DN of the subject (e.g C=US,ST=CA,L=Sunnyvale,O=Fortinet,OU=Dep1,emailAddress=test@example.com). There should be no space in between the attributes. Supported DN attributes (case-sensitive) are:C,ST,L,O,OU,emailAddress. The CN defaults to the device’s SN and cannot be changed.
            apcfg_auto_cert_scep_url: SCEP server URL.
            apcfg_auto_cert_scep_password: SCEP server challenge password for auto-regeneration.
            apcfg_auto_cert_scep_ca_id: CA identifier of the CA server for signing via SCEP.
            apcfg_auto_cert_scep_subject_alt_name: Subject alternative name (optional, e.g. "DNS:dns1.com,IP:192.168.1.99")
            apcfg_auto_cert_scep_https_ca: PEM format https CA Certificate.
            unii_4_5ghz_band: Enable/disable UNII-4 5Ghz band channels (default = disable).
            admin_auth_tacacs_plus: Remote authentication server for admin user.
            admin_restrict_local: Enable/disable local admin authentication restriction when remote authenticator is up and running (default = disable).
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.wireless_controller_wtp_profile.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.wireless_controller_wtp_profile.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if led_schedules is not None:
            led_schedules = normalize_table_field(
                led_schedules,
                mkey="name",
                required_fields=['name'],
                field_name="led_schedules",
                example="[{'name': 'value'}]",
            )
        if deny_mac_list is not None:
            deny_mac_list = normalize_table_field(
                deny_mac_list,
                mkey="id",
                required_fields=['id'],
                field_name="deny_mac_list",
                example="[{'id': 1}]",
            )
        if split_tunneling_acl is not None:
            split_tunneling_acl = normalize_table_field(
                split_tunneling_acl,
                mkey="id",
                required_fields=['dest-ip'],
                field_name="split_tunneling_acl",
                example="[{'dest-ip': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            comment=comment,
            platform=platform,
            control_message_offload=control_message_offload,
            bonjour_profile=bonjour_profile,
            apcfg_profile=apcfg_profile,
            apcfg_mesh=apcfg_mesh,
            apcfg_mesh_ap_type=apcfg_mesh_ap_type,
            apcfg_mesh_ssid=apcfg_mesh_ssid,
            apcfg_mesh_eth_bridge=apcfg_mesh_eth_bridge,
            ble_profile=ble_profile,
            lw_profile=lw_profile,
            syslog_profile=syslog_profile,
            wan_port_mode=wan_port_mode,
            lan=lan,
            energy_efficient_ethernet=energy_efficient_ethernet,
            led_state=led_state,
            led_schedules=led_schedules,
            dtls_policy=dtls_policy,
            dtls_in_kernel=dtls_in_kernel,
            max_clients=max_clients,
            handoff_rssi=handoff_rssi,
            handoff_sta_thresh=handoff_sta_thresh,
            handoff_roaming=handoff_roaming,
            deny_mac_list=deny_mac_list,
            ap_country=ap_country,
            ip_fragment_preventing=ip_fragment_preventing,
            tun_mtu_uplink=tun_mtu_uplink,
            tun_mtu_downlink=tun_mtu_downlink,
            split_tunneling_acl_path=split_tunneling_acl_path,
            split_tunneling_acl_local_ap_subnet=split_tunneling_acl_local_ap_subnet,
            split_tunneling_acl=split_tunneling_acl,
            allowaccess=allowaccess,
            login_passwd_change=login_passwd_change,
            login_passwd=login_passwd,
            lldp=lldp,
            poe_mode=poe_mode,
            usb_port=usb_port,
            frequency_handoff=frequency_handoff,
            ap_handoff=ap_handoff,
            default_mesh_root=default_mesh_root,
            radio_1=radio_1,
            radio_2=radio_2,
            radio_3=radio_3,
            radio_4=radio_4,
            lbs=lbs,
            ext_info_enable=ext_info_enable,
            indoor_outdoor_deployment=indoor_outdoor_deployment,
            esl_ses_dongle=esl_ses_dongle,
            console_login=console_login,
            wan_port_auth=wan_port_auth,
            wan_port_auth_usrname=wan_port_auth_usrname,
            wan_port_auth_password=wan_port_auth_password,
            wan_port_auth_methods=wan_port_auth_methods,
            wan_port_auth_macsec=wan_port_auth_macsec,
            apcfg_auto_cert=apcfg_auto_cert,
            apcfg_auto_cert_enroll_protocol=apcfg_auto_cert_enroll_protocol,
            apcfg_auto_cert_crypto_algo=apcfg_auto_cert_crypto_algo,
            apcfg_auto_cert_est_server=apcfg_auto_cert_est_server,
            apcfg_auto_cert_est_ca_id=apcfg_auto_cert_est_ca_id,
            apcfg_auto_cert_est_http_username=apcfg_auto_cert_est_http_username,
            apcfg_auto_cert_est_http_password=apcfg_auto_cert_est_http_password,
            apcfg_auto_cert_est_subject=apcfg_auto_cert_est_subject,
            apcfg_auto_cert_est_subject_alt_name=apcfg_auto_cert_est_subject_alt_name,
            apcfg_auto_cert_auto_regen_days=apcfg_auto_cert_auto_regen_days,
            apcfg_auto_cert_est_https_ca=apcfg_auto_cert_est_https_ca,
            apcfg_auto_cert_scep_keytype=apcfg_auto_cert_scep_keytype,
            apcfg_auto_cert_scep_keysize=apcfg_auto_cert_scep_keysize,
            apcfg_auto_cert_scep_ec_name=apcfg_auto_cert_scep_ec_name,
            apcfg_auto_cert_scep_sub_fully_dn=apcfg_auto_cert_scep_sub_fully_dn,
            apcfg_auto_cert_scep_url=apcfg_auto_cert_scep_url,
            apcfg_auto_cert_scep_password=apcfg_auto_cert_scep_password,
            apcfg_auto_cert_scep_ca_id=apcfg_auto_cert_scep_ca_id,
            apcfg_auto_cert_scep_subject_alt_name=apcfg_auto_cert_scep_subject_alt_name,
            apcfg_auto_cert_scep_https_ca=apcfg_auto_cert_scep_https_ca,
            unii_4_5ghz_band=unii_4_5ghz_band,
            admin_auth_tacacs_plus=admin_auth_tacacs_plus,
            admin_restrict_local=admin_restrict_local,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.wtp_profile import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/wireless_controller/wtp_profile",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/wireless-controller/wtp-profile/" + quote_path_param(name_value)

        # Add explicit query parameters for PUT
        params: dict[str, Any] = {}
        if q_action is not None:
            params["action"] = q_action
        if q_before is not None:
            params["before"] = q_before
        if q_after is not None:
            params["after"] = q_after
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data=payload_data, params=params, vdom=vdom        )

    # ========================================================================
    # POST Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Field-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def post(  # type: ignore[override]
        self,
        payload_dict: dict[str, Any] | None = None,
        name: str | None = None,
        comment: str | None = None,
        platform: str | None = None,
        control_message_offload: Literal["ebp-frame", "aeroscout-tag", "ap-list", "sta-list", "sta-cap-list", "stats", "aeroscout-mu", "sta-health", "spectral-analysis"] | list[str] | None = None,
        bonjour_profile: str | None = None,
        apcfg_profile: str | None = None,
        apcfg_mesh: Literal["enable", "disable"] | None = None,
        apcfg_mesh_ap_type: Literal["ethernet", "mesh", "auto"] | None = None,
        apcfg_mesh_ssid: str | None = None,
        apcfg_mesh_eth_bridge: Literal["enable", "disable"] | None = None,
        ble_profile: str | None = None,
        lw_profile: str | None = None,
        syslog_profile: str | None = None,
        wan_port_mode: Literal["wan-lan", "wan-only"] | None = None,
        lan: str | None = None,
        energy_efficient_ethernet: Literal["enable", "disable"] | None = None,
        led_state: Literal["enable", "disable"] | None = None,
        led_schedules: str | list[str] | list[dict[str, Any]] | None = None,
        dtls_policy: Literal["clear-text", "dtls-enabled", "ipsec-vpn", "ipsec-sn-vpn"] | list[str] | None = None,
        dtls_in_kernel: Literal["enable", "disable"] | None = None,
        max_clients: int | None = None,
        handoff_rssi: int | None = None,
        handoff_sta_thresh: int | None = None,
        handoff_roaming: Literal["enable", "disable"] | None = None,
        deny_mac_list: str | list[str] | list[dict[str, Any]] | None = None,
        ap_country: Literal["--", "AF", "AL", "DZ", "AS", "AO", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "KH", "CM", "KY", "CF", "TD", "CL", "CN", "CX", "CO", "CG", "CD", "CR", "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "ET", "EE", "GF", "PF", "FO", "FJ", "FI", "FR", "GA", "GE", "GM", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "CI", "JM", "JO", "KZ", "KE", "KR", "KW", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "MA", "MZ", "MM", "NA", "NP", "NL", "AN", "AW", "NZ", "NI", "NE", "NG", "NO", "MP", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "KN", "LC", "MF", "PM", "VC", "SA", "SN", "RS", "ME", "SL", "SG", "SK", "SI", "SO", "ZA", "ES", "LK", "SR", "SZ", "SE", "CH", "TW", "TZ", "TH", "TL", "TG", "TT", "TN", "TR", "TM", "AE", "TC", "UG", "UA", "GB", "US", "PS", "UY", "UZ", "VU", "VE", "VN", "VI", "WF", "YE", "ZM", "ZW", "JP", "CA"] | None = None,
        ip_fragment_preventing: Literal["tcp-mss-adjust", "icmp-unreachable"] | list[str] | None = None,
        tun_mtu_uplink: int | None = None,
        tun_mtu_downlink: int | None = None,
        split_tunneling_acl_path: Literal["tunnel", "local"] | None = None,
        split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"] | None = None,
        split_tunneling_acl: str | list[str] | list[dict[str, Any]] | None = None,
        allowaccess: Literal["https", "ssh", "snmp"] | list[str] | None = None,
        login_passwd_change: Literal["yes", "default", "no"] | None = None,
        login_passwd: Any | None = None,
        lldp: Literal["enable", "disable"] | None = None,
        poe_mode: Literal["auto", "8023af", "8023at", "power-adapter", "full", "high", "low"] | None = None,
        usb_port: Literal["enable", "disable"] | None = None,
        frequency_handoff: Literal["enable", "disable"] | None = None,
        ap_handoff: Literal["enable", "disable"] | None = None,
        default_mesh_root: Literal["enable", "disable"] | None = None,
        radio_1: str | None = None,
        radio_2: str | None = None,
        radio_3: str | None = None,
        radio_4: str | None = None,
        lbs: str | None = None,
        ext_info_enable: Literal["enable", "disable"] | None = None,
        indoor_outdoor_deployment: Literal["platform-determined", "outdoor", "indoor"] | None = None,
        esl_ses_dongle: str | None = None,
        console_login: Literal["enable", "disable"] | None = None,
        wan_port_auth: Literal["none", "802.1x"] | None = None,
        wan_port_auth_usrname: str | None = None,
        wan_port_auth_password: Any | None = None,
        wan_port_auth_methods: Literal["all", "EAP-FAST", "EAP-TLS", "EAP-PEAP"] | None = None,
        wan_port_auth_macsec: Literal["enable", "disable"] | None = None,
        apcfg_auto_cert: Literal["enable", "disable"] | None = None,
        apcfg_auto_cert_enroll_protocol: Literal["none", "est", "scep"] | None = None,
        apcfg_auto_cert_crypto_algo: Literal["rsa-1024", "rsa-1536", "rsa-2048", "rsa-4096", "ec-secp256r1", "ec-secp384r1", "ec-secp521r1"] | None = None,
        apcfg_auto_cert_est_server: str | None = None,
        apcfg_auto_cert_est_ca_id: str | None = None,
        apcfg_auto_cert_est_http_username: str | None = None,
        apcfg_auto_cert_est_http_password: Any | None = None,
        apcfg_auto_cert_est_subject: str | None = None,
        apcfg_auto_cert_est_subject_alt_name: str | None = None,
        apcfg_auto_cert_auto_regen_days: int | None = None,
        apcfg_auto_cert_est_https_ca: str | None = None,
        apcfg_auto_cert_scep_keytype: Literal["rsa", "ec"] | None = None,
        apcfg_auto_cert_scep_keysize: Literal["1024", "1536", "2048", "4096"] | None = None,
        apcfg_auto_cert_scep_ec_name: Literal["secp256r1", "secp384r1", "secp521r1"] | None = None,
        apcfg_auto_cert_scep_sub_fully_dn: str | None = None,
        apcfg_auto_cert_scep_url: str | None = None,
        apcfg_auto_cert_scep_password: Any | None = None,
        apcfg_auto_cert_scep_ca_id: str | None = None,
        apcfg_auto_cert_scep_subject_alt_name: str | None = None,
        apcfg_auto_cert_scep_https_ca: str | None = None,
        unii_4_5ghz_band: Literal["enable", "disable"] | None = None,
        admin_auth_tacacs_plus: str | None = None,
        admin_restrict_local: Literal["enable", "disable"] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new wireless_controller/wtp_profile object.

        Configure WTP profiles or FortiAP profiles that define radio settings for manageable FortiAP platforms.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: WTP (or FortiAP or AP) profile name.
            comment: Comment.
            platform: WTP, FortiAP, or AP platform.
            control_message_offload: Enable/disable CAPWAP control message data channel offload.
            bonjour_profile: Bonjour profile name.
            apcfg_profile: AP local configuration profile name.
            apcfg_mesh: Enable/disable AP local mesh configuration (default = disable).
            apcfg_mesh_ap_type: Mesh AP Type (default = ethernet).
            apcfg_mesh_ssid:  Mesh SSID (default = none).
            apcfg_mesh_eth_bridge: Enable/disable mesh ethernet bridge (default = disable).
            ble_profile: Bluetooth Low Energy profile name.
            lw_profile: LoRaWAN profile name.
            syslog_profile: System log server configuration profile name.
            wan_port_mode: Enable/disable using a WAN port as a LAN port.
            lan: WTP LAN port mapping.
            energy_efficient_ethernet: Enable/disable use of energy efficient Ethernet on WTP.
            led_state: Enable/disable use of LEDs on WTP (default = enable).
            led_schedules: Recurring firewall schedules for illuminating LEDs on the FortiAP. If led-state is enabled, LEDs will be visible when at least one of the schedules is valid. Separate multiple schedule names with a space.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            dtls_policy: WTP data channel DTLS policy (default = clear-text).
            dtls_in_kernel: Enable/disable data channel DTLS in kernel.
            max_clients: Maximum number of stations (STAs) supported by the WTP (default = 0, meaning no client limitation).
            handoff_rssi: Minimum received signal strength indicator (RSSI) value for handoff (20 - 30, default = 25).
            handoff_sta_thresh: Threshold value for AP handoff.
            handoff_roaming: Enable/disable client load balancing during roaming to avoid roaming delay (default = enable).
            deny_mac_list: List of MAC addresses that are denied access to this WTP, FortiAP, or AP.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            ap_country: Country in which this WTP, FortiAP, or AP will operate (default = NA, automatically use the country configured for the current VDOM).
            ip_fragment_preventing: Method(s) by which IP fragmentation is prevented for control and data packets through CAPWAP tunnel (default = tcp-mss-adjust).
            tun_mtu_uplink: The maximum transmission unit (MTU) of uplink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU of FortiAP; default = 0).
            tun_mtu_downlink: The MTU of downlink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU of FortiAP; default = 0).
            split_tunneling_acl_path: Split tunneling ACL path is local/tunnel.
            split_tunneling_acl_local_ap_subnet: Enable/disable automatically adding local subnetwork of FortiAP to split-tunneling ACL (default = disable).
            split_tunneling_acl: Split tunneling ACL filter list.
                Default format: [{'dest-ip': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'dest-ip': 'value'}] (recommended)
            allowaccess: Control management access to the managed WTP, FortiAP, or AP. Separate entries with a space.
            login_passwd_change: Change or reset the administrator password of a managed WTP, FortiAP or AP (yes, default, or no, default = no).
            login_passwd: Set the managed WTP, FortiAP, or AP's administrator password.
            lldp: Enable/disable Link Layer Discovery Protocol (LLDP) for the WTP, FortiAP, or AP (default = enable).
            poe_mode: Set the WTP, FortiAP, or AP's PoE mode.
            usb_port: Enable/disable USB port of the WTP (default = enable).
            frequency_handoff: Enable/disable frequency handoff of clients to other channels (default = disable).
            ap_handoff: Enable/disable AP handoff of clients to other APs (default = disable).
            default_mesh_root: Configure default mesh root SSID when it is not included by radio's SSID configuration.
            radio_1: Configuration options for radio 1.
            radio_2: Configuration options for radio 2.
            radio_3: Configuration options for radio 3.
            radio_4: Configuration options for radio 4.
            lbs: Set various location based service (LBS) options.
            ext_info_enable: Enable/disable station/VAP/radio extension information.
            indoor_outdoor_deployment: Set to allow indoor/outdoor-only channels under regulatory rules (default = platform-determined).
            esl_ses_dongle: ESL SES-imagotag dongle configuration.
            console_login: Enable/disable FortiAP console login access (default = enable).
            wan_port_auth: Set WAN port authentication mode (default = none).
            wan_port_auth_usrname: Set WAN port 802.1x supplicant user name.
            wan_port_auth_password: Set WAN port 802.1x supplicant password.
            wan_port_auth_methods: WAN port 802.1x supplicant EAP methods (default = all).
            wan_port_auth_macsec: Enable/disable WAN port 802.1x supplicant MACsec policy (default = disable).
            apcfg_auto_cert: Enable/disable AP local auto cert configuration (default = disable).
            apcfg_auto_cert_enroll_protocol: Certificate enrollment protocol (default = none)
            apcfg_auto_cert_crypto_algo: Cryptography algorithm: rsa-1024, rsa-1536, rsa-2048, rsa-4096, ec-secp256r1, ec-secp384r1, ec-secp521r1 (default = ec-secp256r1)
            apcfg_auto_cert_est_server: Address and port for EST server (e.g. https://example.com:1234).
            apcfg_auto_cert_est_ca_id: CA identifier of the CA server for signing via EST.
            apcfg_auto_cert_est_http_username: HTTP Authentication username for signing via EST.
            apcfg_auto_cert_est_http_password: HTTP Authentication password for signing via EST.
            apcfg_auto_cert_est_subject: Subject e.g. "CN=User,DC=example,DC=COM" (default = CN=FortiAP,DC=local,DC=COM)
            apcfg_auto_cert_est_subject_alt_name: Subject alternative name (optional, e.g. "DNS:dns1.com,IP:192.168.1.99")
            apcfg_auto_cert_auto_regen_days: Number of days to wait before expiry of an updated local certificate is requested (0 = disabled) (default = 30).
            apcfg_auto_cert_est_https_ca: PEM format https CA Certificate.
            apcfg_auto_cert_scep_keytype: Key type (default = rsa)
            apcfg_auto_cert_scep_keysize: Key size: 1024, 1536, 2048, 4096 (default 2048).
            apcfg_auto_cert_scep_ec_name: Elliptic curve name: secp256r1, secp384r1 and secp521r1. (default secp256r1).
            apcfg_auto_cert_scep_sub_fully_dn: Full DN of the subject (e.g C=US,ST=CA,L=Sunnyvale,O=Fortinet,OU=Dep1,emailAddress=test@example.com). There should be no space in between the attributes. Supported DN attributes (case-sensitive) are:C,ST,L,O,OU,emailAddress. The CN defaults to the device’s SN and cannot be changed.
            apcfg_auto_cert_scep_url: SCEP server URL.
            apcfg_auto_cert_scep_password: SCEP server challenge password for auto-regeneration.
            apcfg_auto_cert_scep_ca_id: CA identifier of the CA server for signing via SCEP.
            apcfg_auto_cert_scep_subject_alt_name: Subject alternative name (optional, e.g. "DNS:dns1.com,IP:192.168.1.99")
            apcfg_auto_cert_scep_https_ca: PEM format https CA Certificate.
            unii_4_5ghz_band: Enable/disable UNII-4 5Ghz band channels (default = disable).
            admin_auth_tacacs_plus: Remote authentication server for admin user.
            admin_restrict_local: Enable/disable local admin authentication restriction when remote authenticator is up and running (default = disable).
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.wireless_controller_wtp_profile.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = WtpProfile.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.wireless_controller_wtp_profile.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(WtpProfile.required_fields()) }}
            
            Use WtpProfile.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if led_schedules is not None:
            led_schedules = normalize_table_field(
                led_schedules,
                mkey="name",
                required_fields=['name'],
                field_name="led_schedules",
                example="[{'name': 'value'}]",
            )
        if deny_mac_list is not None:
            deny_mac_list = normalize_table_field(
                deny_mac_list,
                mkey="id",
                required_fields=['id'],
                field_name="deny_mac_list",
                example="[{'id': 1}]",
            )
        if split_tunneling_acl is not None:
            split_tunneling_acl = normalize_table_field(
                split_tunneling_acl,
                mkey="id",
                required_fields=['dest-ip'],
                field_name="split_tunneling_acl",
                example="[{'dest-ip': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            comment=comment,
            platform=platform,
            control_message_offload=control_message_offload,
            bonjour_profile=bonjour_profile,
            apcfg_profile=apcfg_profile,
            apcfg_mesh=apcfg_mesh,
            apcfg_mesh_ap_type=apcfg_mesh_ap_type,
            apcfg_mesh_ssid=apcfg_mesh_ssid,
            apcfg_mesh_eth_bridge=apcfg_mesh_eth_bridge,
            ble_profile=ble_profile,
            lw_profile=lw_profile,
            syslog_profile=syslog_profile,
            wan_port_mode=wan_port_mode,
            lan=lan,
            energy_efficient_ethernet=energy_efficient_ethernet,
            led_state=led_state,
            led_schedules=led_schedules,
            dtls_policy=dtls_policy,
            dtls_in_kernel=dtls_in_kernel,
            max_clients=max_clients,
            handoff_rssi=handoff_rssi,
            handoff_sta_thresh=handoff_sta_thresh,
            handoff_roaming=handoff_roaming,
            deny_mac_list=deny_mac_list,
            ap_country=ap_country,
            ip_fragment_preventing=ip_fragment_preventing,
            tun_mtu_uplink=tun_mtu_uplink,
            tun_mtu_downlink=tun_mtu_downlink,
            split_tunneling_acl_path=split_tunneling_acl_path,
            split_tunneling_acl_local_ap_subnet=split_tunneling_acl_local_ap_subnet,
            split_tunneling_acl=split_tunneling_acl,
            allowaccess=allowaccess,
            login_passwd_change=login_passwd_change,
            login_passwd=login_passwd,
            lldp=lldp,
            poe_mode=poe_mode,
            usb_port=usb_port,
            frequency_handoff=frequency_handoff,
            ap_handoff=ap_handoff,
            default_mesh_root=default_mesh_root,
            radio_1=radio_1,
            radio_2=radio_2,
            radio_3=radio_3,
            radio_4=radio_4,
            lbs=lbs,
            ext_info_enable=ext_info_enable,
            indoor_outdoor_deployment=indoor_outdoor_deployment,
            esl_ses_dongle=esl_ses_dongle,
            console_login=console_login,
            wan_port_auth=wan_port_auth,
            wan_port_auth_usrname=wan_port_auth_usrname,
            wan_port_auth_password=wan_port_auth_password,
            wan_port_auth_methods=wan_port_auth_methods,
            wan_port_auth_macsec=wan_port_auth_macsec,
            apcfg_auto_cert=apcfg_auto_cert,
            apcfg_auto_cert_enroll_protocol=apcfg_auto_cert_enroll_protocol,
            apcfg_auto_cert_crypto_algo=apcfg_auto_cert_crypto_algo,
            apcfg_auto_cert_est_server=apcfg_auto_cert_est_server,
            apcfg_auto_cert_est_ca_id=apcfg_auto_cert_est_ca_id,
            apcfg_auto_cert_est_http_username=apcfg_auto_cert_est_http_username,
            apcfg_auto_cert_est_http_password=apcfg_auto_cert_est_http_password,
            apcfg_auto_cert_est_subject=apcfg_auto_cert_est_subject,
            apcfg_auto_cert_est_subject_alt_name=apcfg_auto_cert_est_subject_alt_name,
            apcfg_auto_cert_auto_regen_days=apcfg_auto_cert_auto_regen_days,
            apcfg_auto_cert_est_https_ca=apcfg_auto_cert_est_https_ca,
            apcfg_auto_cert_scep_keytype=apcfg_auto_cert_scep_keytype,
            apcfg_auto_cert_scep_keysize=apcfg_auto_cert_scep_keysize,
            apcfg_auto_cert_scep_ec_name=apcfg_auto_cert_scep_ec_name,
            apcfg_auto_cert_scep_sub_fully_dn=apcfg_auto_cert_scep_sub_fully_dn,
            apcfg_auto_cert_scep_url=apcfg_auto_cert_scep_url,
            apcfg_auto_cert_scep_password=apcfg_auto_cert_scep_password,
            apcfg_auto_cert_scep_ca_id=apcfg_auto_cert_scep_ca_id,
            apcfg_auto_cert_scep_subject_alt_name=apcfg_auto_cert_scep_subject_alt_name,
            apcfg_auto_cert_scep_https_ca=apcfg_auto_cert_scep_https_ca,
            unii_4_5ghz_band=unii_4_5ghz_band,
            admin_auth_tacacs_plus=admin_auth_tacacs_plus,
            admin_restrict_local=admin_restrict_local,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.wtp_profile import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/wireless_controller/wtp_profile",
            )

        endpoint = "/wireless-controller/wtp-profile"
        
        # Add explicit query parameters for POST
        params: dict[str, Any] = {}
        if q_action is not None:
            params["action"] = q_action
        if q_nkey is not None:
            params["nkey"] = q_nkey
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data=payload_data, params=params, vdom=vdom        )

    # ========================================================================
    # DELETE Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Identifier parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def delete(  # type: ignore[override]
        self,
        name: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete wireless_controller/wtp_profile object.

        Configure WTP profiles or FortiAP profiles that define radio settings for manageable FortiAP platforms.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is not provided

        Examples:
            >>> # Delete specific object
            >>> result = fgt.api.cmdb.wireless_controller_wtp_profile.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/wireless-controller/wtp-profile/" + quote_path_param(name)

        # Add explicit query parameters for DELETE
        params: dict[str, Any] = {}
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=vdom        )

    def exists(
        self,
        name: str,
        vdom: str | bool | None = None,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if wireless_controller/wtp_profile object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.wireless_controller_wtp_profile.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.wireless_controller_wtp_profile.exists(name=1):
            ...     fgt.api.cmdb.wireless_controller_wtp_profile.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/wireless-controller/wtp-profile"
        endpoint = f"{endpoint}/{quote_path_param(name)}"
        
        try:
            # Use silent=True to suppress 404 error logging
            result = self._client.get("cmdb", endpoint, vdom=vdom, silent=True)
            
            # Check if result is a coroutine (async) or direct response (sync)
            # Note: Type checkers can't narrow Union[T, Coroutine[T]] in conditionals
            if hasattr(result, '__await__'):
                # Async response - return coroutine that checks status
                async def _check() -> bool:
                    r = await result  # type: ignore[misc]
                    return r.http_status == "success"  # type: ignore[union-attr]
                return _check()
            else:
                # Sync response - check status directly from FortiObject
                return result.http_status == "success"  # type: ignore[union-attr]
        except Exception:
            # Any error (404, network, etc.) means we can't confirm existence
            return False


    def set(
        self,
        payload_dict: dict[str, Any] | None = None,
        name: str | None = None,
        comment: str | None = None,
        platform: str | None = None,
        control_message_offload: Literal["ebp-frame", "aeroscout-tag", "ap-list", "sta-list", "sta-cap-list", "stats", "aeroscout-mu", "sta-health", "spectral-analysis"] | list[str] | list[dict[str, Any]] | None = None,
        bonjour_profile: str | None = None,
        apcfg_profile: str | None = None,
        apcfg_mesh: Literal["enable", "disable"] | None = None,
        apcfg_mesh_ap_type: Literal["ethernet", "mesh", "auto"] | None = None,
        apcfg_mesh_ssid: str | None = None,
        apcfg_mesh_eth_bridge: Literal["enable", "disable"] | None = None,
        ble_profile: str | None = None,
        lw_profile: str | None = None,
        syslog_profile: str | None = None,
        wan_port_mode: Literal["wan-lan", "wan-only"] | None = None,
        lan: str | None = None,
        energy_efficient_ethernet: Literal["enable", "disable"] | None = None,
        led_state: Literal["enable", "disable"] | None = None,
        led_schedules: str | list[str] | list[dict[str, Any]] | None = None,
        dtls_policy: Literal["clear-text", "dtls-enabled", "ipsec-vpn", "ipsec-sn-vpn"] | list[str] | list[dict[str, Any]] | None = None,
        dtls_in_kernel: Literal["enable", "disable"] | None = None,
        max_clients: int | None = None,
        handoff_rssi: int | None = None,
        handoff_sta_thresh: int | None = None,
        handoff_roaming: Literal["enable", "disable"] | None = None,
        deny_mac_list: str | list[str] | list[dict[str, Any]] | None = None,
        ap_country: Literal["--", "AF", "AL", "DZ", "AS", "AO", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BR", "BN", "BG", "BF", "KH", "CM", "KY", "CF", "TD", "CL", "CN", "CX", "CO", "CG", "CD", "CR", "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "ET", "EE", "GF", "PF", "FO", "FJ", "FI", "FR", "GA", "GE", "GM", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GY", "HT", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "CI", "JM", "JO", "KZ", "KE", "KR", "KW", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "MA", "MZ", "MM", "NA", "NP", "NL", "AN", "AW", "NZ", "NI", "NE", "NG", "NO", "MP", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "KN", "LC", "MF", "PM", "VC", "SA", "SN", "RS", "ME", "SL", "SG", "SK", "SI", "SO", "ZA", "ES", "LK", "SR", "SZ", "SE", "CH", "TW", "TZ", "TH", "TL", "TG", "TT", "TN", "TR", "TM", "AE", "TC", "UG", "UA", "GB", "US", "PS", "UY", "UZ", "VU", "VE", "VN", "VI", "WF", "YE", "ZM", "ZW", "JP", "CA"] | None = None,
        ip_fragment_preventing: Literal["tcp-mss-adjust", "icmp-unreachable"] | list[str] | list[dict[str, Any]] | None = None,
        tun_mtu_uplink: int | None = None,
        tun_mtu_downlink: int | None = None,
        split_tunneling_acl_path: Literal["tunnel", "local"] | None = None,
        split_tunneling_acl_local_ap_subnet: Literal["enable", "disable"] | None = None,
        split_tunneling_acl: str | list[str] | list[dict[str, Any]] | None = None,
        allowaccess: Literal["https", "ssh", "snmp"] | list[str] | list[dict[str, Any]] | None = None,
        login_passwd_change: Literal["yes", "default", "no"] | None = None,
        login_passwd: Any | None = None,
        lldp: Literal["enable", "disable"] | None = None,
        poe_mode: Literal["auto", "8023af", "8023at", "power-adapter", "full", "high", "low"] | None = None,
        usb_port: Literal["enable", "disable"] | None = None,
        frequency_handoff: Literal["enable", "disable"] | None = None,
        ap_handoff: Literal["enable", "disable"] | None = None,
        default_mesh_root: Literal["enable", "disable"] | None = None,
        radio_1: str | None = None,
        radio_2: str | None = None,
        radio_3: str | None = None,
        radio_4: str | None = None,
        lbs: str | None = None,
        ext_info_enable: Literal["enable", "disable"] | None = None,
        indoor_outdoor_deployment: Literal["platform-determined", "outdoor", "indoor"] | None = None,
        esl_ses_dongle: str | None = None,
        console_login: Literal["enable", "disable"] | None = None,
        wan_port_auth: Literal["none", "802.1x"] | None = None,
        wan_port_auth_usrname: str | None = None,
        wan_port_auth_password: Any | None = None,
        wan_port_auth_methods: Literal["all", "EAP-FAST", "EAP-TLS", "EAP-PEAP"] | None = None,
        wan_port_auth_macsec: Literal["enable", "disable"] | None = None,
        apcfg_auto_cert: Literal["enable", "disable"] | None = None,
        apcfg_auto_cert_enroll_protocol: Literal["none", "est", "scep"] | None = None,
        apcfg_auto_cert_crypto_algo: Literal["rsa-1024", "rsa-1536", "rsa-2048", "rsa-4096", "ec-secp256r1", "ec-secp384r1", "ec-secp521r1"] | None = None,
        apcfg_auto_cert_est_server: str | None = None,
        apcfg_auto_cert_est_ca_id: str | None = None,
        apcfg_auto_cert_est_http_username: str | None = None,
        apcfg_auto_cert_est_http_password: Any | None = None,
        apcfg_auto_cert_est_subject: str | None = None,
        apcfg_auto_cert_est_subject_alt_name: str | None = None,
        apcfg_auto_cert_auto_regen_days: int | None = None,
        apcfg_auto_cert_est_https_ca: str | None = None,
        apcfg_auto_cert_scep_keytype: Literal["rsa", "ec"] | None = None,
        apcfg_auto_cert_scep_keysize: Literal["1024", "1536", "2048", "4096"] | None = None,
        apcfg_auto_cert_scep_ec_name: Literal["secp256r1", "secp384r1", "secp521r1"] | None = None,
        apcfg_auto_cert_scep_sub_fully_dn: str | None = None,
        apcfg_auto_cert_scep_url: str | None = None,
        apcfg_auto_cert_scep_password: Any | None = None,
        apcfg_auto_cert_scep_ca_id: str | None = None,
        apcfg_auto_cert_scep_subject_alt_name: str | None = None,
        apcfg_auto_cert_scep_https_ca: str | None = None,
        unii_4_5ghz_band: Literal["enable", "disable"] | None = None,
        admin_auth_tacacs_plus: str | None = None,
        admin_restrict_local: Literal["enable", "disable"] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update wireless_controller/wtp_profile object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            comment: Field comment
            platform: Field platform
            control_message_offload: Field control-message-offload
            bonjour_profile: Field bonjour-profile
            apcfg_profile: Field apcfg-profile
            apcfg_mesh: Field apcfg-mesh
            apcfg_mesh_ap_type: Field apcfg-mesh-ap-type
            apcfg_mesh_ssid: Field apcfg-mesh-ssid
            apcfg_mesh_eth_bridge: Field apcfg-mesh-eth-bridge
            ble_profile: Field ble-profile
            lw_profile: Field lw-profile
            syslog_profile: Field syslog-profile
            wan_port_mode: Field wan-port-mode
            lan: Field lan
            energy_efficient_ethernet: Field energy-efficient-ethernet
            led_state: Field led-state
            led_schedules: Field led-schedules
            dtls_policy: Field dtls-policy
            dtls_in_kernel: Field dtls-in-kernel
            max_clients: Field max-clients
            handoff_rssi: Field handoff-rssi
            handoff_sta_thresh: Field handoff-sta-thresh
            handoff_roaming: Field handoff-roaming
            deny_mac_list: Field deny-mac-list
            ap_country: Field ap-country
            ip_fragment_preventing: Field ip-fragment-preventing
            tun_mtu_uplink: Field tun-mtu-uplink
            tun_mtu_downlink: Field tun-mtu-downlink
            split_tunneling_acl_path: Field split-tunneling-acl-path
            split_tunneling_acl_local_ap_subnet: Field split-tunneling-acl-local-ap-subnet
            split_tunneling_acl: Field split-tunneling-acl
            allowaccess: Field allowaccess
            login_passwd_change: Field login-passwd-change
            login_passwd: Field login-passwd
            lldp: Field lldp
            poe_mode: Field poe-mode
            usb_port: Field usb-port
            frequency_handoff: Field frequency-handoff
            ap_handoff: Field ap-handoff
            default_mesh_root: Field default-mesh-root
            radio_1: Field radio-1
            radio_2: Field radio-2
            radio_3: Field radio-3
            radio_4: Field radio-4
            lbs: Field lbs
            ext_info_enable: Field ext-info-enable
            indoor_outdoor_deployment: Field indoor-outdoor-deployment
            esl_ses_dongle: Field esl-ses-dongle
            console_login: Field console-login
            wan_port_auth: Field wan-port-auth
            wan_port_auth_usrname: Field wan-port-auth-usrname
            wan_port_auth_password: Field wan-port-auth-password
            wan_port_auth_methods: Field wan-port-auth-methods
            wan_port_auth_macsec: Field wan-port-auth-macsec
            apcfg_auto_cert: Field apcfg-auto-cert
            apcfg_auto_cert_enroll_protocol: Field apcfg-auto-cert-enroll-protocol
            apcfg_auto_cert_crypto_algo: Field apcfg-auto-cert-crypto-algo
            apcfg_auto_cert_est_server: Field apcfg-auto-cert-est-server
            apcfg_auto_cert_est_ca_id: Field apcfg-auto-cert-est-ca-id
            apcfg_auto_cert_est_http_username: Field apcfg-auto-cert-est-http-username
            apcfg_auto_cert_est_http_password: Field apcfg-auto-cert-est-http-password
            apcfg_auto_cert_est_subject: Field apcfg-auto-cert-est-subject
            apcfg_auto_cert_est_subject_alt_name: Field apcfg-auto-cert-est-subject-alt-name
            apcfg_auto_cert_auto_regen_days: Field apcfg-auto-cert-auto-regen-days
            apcfg_auto_cert_est_https_ca: Field apcfg-auto-cert-est-https-ca
            apcfg_auto_cert_scep_keytype: Field apcfg-auto-cert-scep-keytype
            apcfg_auto_cert_scep_keysize: Field apcfg-auto-cert-scep-keysize
            apcfg_auto_cert_scep_ec_name: Field apcfg-auto-cert-scep-ec-name
            apcfg_auto_cert_scep_sub_fully_dn: Field apcfg-auto-cert-scep-sub-fully-dn
            apcfg_auto_cert_scep_url: Field apcfg-auto-cert-scep-url
            apcfg_auto_cert_scep_password: Field apcfg-auto-cert-scep-password
            apcfg_auto_cert_scep_ca_id: Field apcfg-auto-cert-scep-ca-id
            apcfg_auto_cert_scep_subject_alt_name: Field apcfg-auto-cert-scep-subject-alt-name
            apcfg_auto_cert_scep_https_ca: Field apcfg-auto-cert-scep-https-ca
            unii_4_5ghz_band: Field unii-4-5ghz-band
            admin_auth_tacacs_plus: Field admin-auth-tacacs+
            admin_restrict_local: Field admin-restrict-local
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.wireless_controller_wtp_profile.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.wireless_controller_wtp_profile.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.wireless_controller_wtp_profile.set(payload_dict=obj_data)
            >>> # Safely applies configuration regardless of current state

        Note:
            This method internally calls exists() then either post() or put().
            For performance-critical code with known state, call post() or put() directly.

        See Also:
            - post(): Create new object
            - put(): Update existing object
            - exists(): Check existence manually
        """
        # Apply normalization for table fields (supports flexible input formats)
        if led_schedules is not None:
            led_schedules = normalize_table_field(
                led_schedules,
                mkey="name",
                required_fields=['name'],
                field_name="led_schedules",
                example="[{'name': 'value'}]",
            )
        if deny_mac_list is not None:
            deny_mac_list = normalize_table_field(
                deny_mac_list,
                mkey="id",
                required_fields=['id'],
                field_name="deny_mac_list",
                example="[{'id': 1}]",
            )
        if split_tunneling_acl is not None:
            split_tunneling_acl = normalize_table_field(
                split_tunneling_acl,
                mkey="id",
                required_fields=['dest-ip'],
                field_name="split_tunneling_acl",
                example="[{'dest-ip': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            comment=comment,
            platform=platform,
            control_message_offload=control_message_offload,
            bonjour_profile=bonjour_profile,
            apcfg_profile=apcfg_profile,
            apcfg_mesh=apcfg_mesh,
            apcfg_mesh_ap_type=apcfg_mesh_ap_type,
            apcfg_mesh_ssid=apcfg_mesh_ssid,
            apcfg_mesh_eth_bridge=apcfg_mesh_eth_bridge,
            ble_profile=ble_profile,
            lw_profile=lw_profile,
            syslog_profile=syslog_profile,
            wan_port_mode=wan_port_mode,
            lan=lan,
            energy_efficient_ethernet=energy_efficient_ethernet,
            led_state=led_state,
            led_schedules=led_schedules,
            dtls_policy=dtls_policy,
            dtls_in_kernel=dtls_in_kernel,
            max_clients=max_clients,
            handoff_rssi=handoff_rssi,
            handoff_sta_thresh=handoff_sta_thresh,
            handoff_roaming=handoff_roaming,
            deny_mac_list=deny_mac_list,
            ap_country=ap_country,
            ip_fragment_preventing=ip_fragment_preventing,
            tun_mtu_uplink=tun_mtu_uplink,
            tun_mtu_downlink=tun_mtu_downlink,
            split_tunneling_acl_path=split_tunneling_acl_path,
            split_tunneling_acl_local_ap_subnet=split_tunneling_acl_local_ap_subnet,
            split_tunneling_acl=split_tunneling_acl,
            allowaccess=allowaccess,
            login_passwd_change=login_passwd_change,
            login_passwd=login_passwd,
            lldp=lldp,
            poe_mode=poe_mode,
            usb_port=usb_port,
            frequency_handoff=frequency_handoff,
            ap_handoff=ap_handoff,
            default_mesh_root=default_mesh_root,
            radio_1=radio_1,
            radio_2=radio_2,
            radio_3=radio_3,
            radio_4=radio_4,
            lbs=lbs,
            ext_info_enable=ext_info_enable,
            indoor_outdoor_deployment=indoor_outdoor_deployment,
            esl_ses_dongle=esl_ses_dongle,
            console_login=console_login,
            wan_port_auth=wan_port_auth,
            wan_port_auth_usrname=wan_port_auth_usrname,
            wan_port_auth_password=wan_port_auth_password,
            wan_port_auth_methods=wan_port_auth_methods,
            wan_port_auth_macsec=wan_port_auth_macsec,
            apcfg_auto_cert=apcfg_auto_cert,
            apcfg_auto_cert_enroll_protocol=apcfg_auto_cert_enroll_protocol,
            apcfg_auto_cert_crypto_algo=apcfg_auto_cert_crypto_algo,
            apcfg_auto_cert_est_server=apcfg_auto_cert_est_server,
            apcfg_auto_cert_est_ca_id=apcfg_auto_cert_est_ca_id,
            apcfg_auto_cert_est_http_username=apcfg_auto_cert_est_http_username,
            apcfg_auto_cert_est_http_password=apcfg_auto_cert_est_http_password,
            apcfg_auto_cert_est_subject=apcfg_auto_cert_est_subject,
            apcfg_auto_cert_est_subject_alt_name=apcfg_auto_cert_est_subject_alt_name,
            apcfg_auto_cert_auto_regen_days=apcfg_auto_cert_auto_regen_days,
            apcfg_auto_cert_est_https_ca=apcfg_auto_cert_est_https_ca,
            apcfg_auto_cert_scep_keytype=apcfg_auto_cert_scep_keytype,
            apcfg_auto_cert_scep_keysize=apcfg_auto_cert_scep_keysize,
            apcfg_auto_cert_scep_ec_name=apcfg_auto_cert_scep_ec_name,
            apcfg_auto_cert_scep_sub_fully_dn=apcfg_auto_cert_scep_sub_fully_dn,
            apcfg_auto_cert_scep_url=apcfg_auto_cert_scep_url,
            apcfg_auto_cert_scep_password=apcfg_auto_cert_scep_password,
            apcfg_auto_cert_scep_ca_id=apcfg_auto_cert_scep_ca_id,
            apcfg_auto_cert_scep_subject_alt_name=apcfg_auto_cert_scep_subject_alt_name,
            apcfg_auto_cert_scep_https_ca=apcfg_auto_cert_scep_https_ca,
            unii_4_5ghz_band=unii_4_5ghz_band,
            admin_auth_tacacs_plus=admin_auth_tacacs_plus,
            admin_restrict_local=admin_restrict_local,
            data=payload_dict,
        )
        
        mkey_value = payload_data.get("name")
        if not mkey_value:
            raise ValueError("name is required for set()")
        
        # Check if resource exists
        if self.exists(name=mkey_value, vdom=vdom):
            # Update existing resource
            return self.put(payload_dict=payload_data, vdom=vdom, **kwargs)
        else:
            # Create new resource
            return self.post(payload_dict=payload_data, vdom=vdom, **kwargs)

    # ========================================================================
    # Action: Move
    # ========================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = None,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move wireless_controller/wtp_profile object to a new position.
        
        Reorders objects by moving one before/after another, to top/bottom, or to a specific position.
        
        Args:
            name: Identifier of object to move
            position: Where to move the object:
                - "before": Move before reference object (requires reference_name)
                - "after": Move after reference object (requires reference_name)
                - "top": Move to first position (reference not needed)
                - "bottom": Move to last position (reference not needed)
                - int (1-based): Move to specific position number (e.g., position=3 for 3rd place)
            reference_name: Identifier of reference object (required for before/after)
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Examples:
            >>> # Move to top (first position)
            >>> fgt.api.cmdb.wireless_controller_wtp_profile.move(
            ...     name=100,
            ...     position="top"
            ... )
            
            >>> # Move to specific position (3rd place)
            >>> fgt.api.cmdb.wireless_controller_wtp_profile.move(
            ...     name=100,
            ...     position=3
            ... )
            
            >>> # Move before another object
            >>> fgt.api.cmdb.wireless_controller_wtp_profile.move(
            ...     name=100,
            ...     position="before",
            ...     reference_name=50
            ... )
        """
        # Handle numeric position (1-based index)
        if isinstance(position, int):
            if position < 1:
                raise ValueError(f"Position must be >= 1, got {position}")
            
            # Get all objects to find the target position
            all_objects = self.get(vdom=vdom)
            if not all_objects:
                raise ValueError("Cannot move to position {position} - no objects found")
            
            # Validate position is within range (can be len+1 to append at end)
            if position > len(all_objects) + 1:
                raise ValueError(
                    f"Position {position} is out of range. Valid range: 1-{len(all_objects) + 1} "
                    f"({len(all_objects)} objects exist)"
                )
            
            # Convert to before/after operation
            if position == 1:
                # Move to first position
                reference_name = all_objects[0].name
                actual_position = "before"
            elif position > len(all_objects):
                # Move to last position (after all existing objects)
                reference_name = all_objects[-1].name
                actual_position = "after"
            else:
                # Move before the object currently at that position
                reference_name = all_objects[position - 1].name
                actual_position = "before"
        
        # Handle top/bottom string positions
        elif position in ("top", "bottom"):
            # Get all objects to find first/last
            all_objects = self.get(vdom=vdom)
            if not all_objects:
                raise ValueError(f"Cannot move to {position} - no objects found")
            
            if position == "top":
                # Move before first object
                reference_name = all_objects[0].name
                actual_position = "before"
            else:  # bottom
                # Move after last object
                reference_name = all_objects[-1].name
                actual_position = "after"
        
        # Handle before/after string positions
        else:
            # Validate reference is provided for before/after
            if reference_name is None:
                raise ValueError(f"reference_name is required when position='{position}'")
            actual_position = position
        
        # Build params for move operation
        params = {
            "action": "move",
            actual_position: reference_name,
            **kwargs,
        }
        
        # Move requires the mkey in the endpoint path
        endpoint = "/wireless-controller/wtp-profile/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





