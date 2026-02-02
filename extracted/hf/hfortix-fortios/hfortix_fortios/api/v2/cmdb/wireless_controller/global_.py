"""
FortiOS CMDB - Wireless_controller global_

Configuration endpoint for managing cmdb wireless_controller/global_ objects.

API Endpoints:
    GET    /cmdb/wireless_controller/global_
    POST   /cmdb/wireless_controller/global_
    PUT    /cmdb/wireless_controller/global_/{identifier}
    DELETE /cmdb/wireless_controller/global_/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.wireless_controller_global.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.wireless_controller_global.post(
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
)
# Import metadata mixin for schema introspection
from hfortix_fortios._helpers.metadata_mixin import MetadataMixin

# Import Protocol-based type hints (eliminates need for local @overload decorators)
from hfortix_fortios._protocols import CRUDEndpoint

class Global(CRUDEndpoint, MetadataMixin):
    """Global Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "global_"
    
    # ========================================================================
    # Capabilities (from schema metadata)
    # ========================================================================
    SUPPORTS_CREATE = False
    SUPPORTS_READ = True
    SUPPORTS_UPDATE = True
    SUPPORTS_DELETE = False
    SUPPORTS_MOVE = True
    SUPPORTS_CLONE = True
    SUPPORTS_FILTERING = True
    SUPPORTS_PAGINATION = True
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize Global endpoint."""
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
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve wireless_controller/global_ configuration.

        Configure wireless controller global settings.

        Args:
            name: Name identifier to retrieve specific object. If None, returns all objects.
            filter: List of filter expressions to limit results.
                Each filter uses format: "field==value" or "field!=value"
                Operators: ==, !=, =@ (contains), !@ (not contains), <=, <, >=, >
                Multiple filters use AND logic. For OR, use comma in single string.
                Example: ["name==test", "status==enable"] or ["name==test,name==prod"]
            count: Maximum number of entries to return (pagination).
            start: Starting entry index for pagination (0-based).
            payload_dict: Additional query parameters for advanced options:
                - datasource (bool): Include datasource information
                - with_meta (bool): Include metadata about each object
                - with_contents_hash (bool): Include checksum of object contents
                - format (list[str]): Property names to include (e.g., ["policyid", "srcintf"])
                - scope (str): Query scope - "global", "vdom", or "both"
                - action (str): Special actions - "schema", "default"
                See FortiOS REST API documentation for complete list.
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
            >>> # Get all wireless_controller/global_ objects
            >>> result = fgt.api.cmdb.wireless_controller_global.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.wireless_controller_global.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.wireless_controller_global.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.wireless_controller_global.get_schema()

        See Also:
            - post(): Create new wireless_controller/global_ object
            - put(): Update existing wireless_controller/global_ object
            - delete(): Remove wireless_controller/global_ object
            - exists(): Check if object exists
            - get_schema(): Get endpoint schema/metadata
        """
        params = payload_dict.copy() if payload_dict else {}
        
        # Add explicit query parameters
        if filter is not None:
            params["filter"] = filter
        if count is not None:
            params["count"] = count
        if start is not None:
            params["start"] = start
        
        if name:
            endpoint = f"/wireless-controller/global/{quote_path_param(name)}"
            unwrap_single = True
        else:
            endpoint = "/wireless-controller/global"
            unwrap_single = False
        
        return self._client.get(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=False, unwrap_single=unwrap_single
        )

    def get_schema(
        self,
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
            format: Schema format - "schema" (FortiOS native) or "json-schema" (JSON Schema standard).
                Defaults to "schema".
                
        Returns:
            Schema definition as dict. Returns Coroutine if using async client.
            
        Example:
            >>> # Get FortiOS native schema
            >>> schema = fgt.api.cmdb.wireless_controller_global.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.wireless_controller_global.get_schema(format="json-schema")
        
        Note:
            Not all endpoints support all schema formats. The "schema" format
            is most widely supported.
        """
        return self.get(payload_dict={"action": format})


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
        location: str | None = None,
        acd_process_count: int | None = None,
        wpad_process_count: int | None = None,
        image_download: Literal["enable", "disable"] | None = None,
        rolling_wtp_upgrade: Literal["enable", "disable"] | None = None,
        rolling_wtp_upgrade_threshold: str | None = None,
        max_retransmit: int | None = None,
        control_message_offload: Literal["ebp-frame", "aeroscout-tag", "ap-list", "sta-list", "sta-cap-list", "stats", "aeroscout-mu", "sta-health", "spectral-analysis"] | list[str] | None = None,
        data_ethernet_II: Literal["enable", "disable"] | None = None,
        link_aggregation: Literal["enable", "disable"] | None = None,
        mesh_eth_type: int | None = None,
        fiapp_eth_type: int | None = None,
        discovery_mc_addr: Any | None = None,
        discovery_mc_addr6: str | None = None,
        max_clients: int | None = None,
        rogue_scan_mac_adjacency: int | None = None,
        ipsec_base_ip: str | None = None,
        wtp_share: Literal["enable", "disable"] | None = None,
        tunnel_mode: Literal["compatible", "strict"] | None = None,
        nac_interval: int | None = None,
        ap_log_server: Literal["enable", "disable"] | None = None,
        ap_log_server_ip: str | None = None,
        ap_log_server_port: int | None = None,
        max_sta_offline: int | None = None,
        max_sta_offline_ip2mac: int | None = None,
        max_sta_cap: int | None = None,
        max_sta_cap_wtp: int | None = None,
        max_rogue_ap: int | None = None,
        max_rogue_ap_wtp: int | None = None,
        max_rogue_sta: int | None = None,
        max_wids_entry: int | None = None,
        max_ble_device: int | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing wireless_controller/global_ object.

        Configure wireless controller global settings.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: Name of the wireless controller.
            location: Description of the location of the wireless controller.
            acd_process_count: Configure the number cw_acd daemons for multi-core CPU support (default = 0).
            wpad_process_count: Wpad daemon process count for multi-core CPU support.
            image_download: Enable/disable WTP image download at join time.
            rolling_wtp_upgrade: Enable/disable rolling WTP upgrade (default = disable).
            rolling_wtp_upgrade_threshold: Minimum signal level/threshold in dBm required for the managed WTP to be included in rolling WTP upgrade (-95 to -20, default = -80).
            max_retransmit: Maximum number of tunnel packet retransmissions (0 - 64, default = 3).
            control_message_offload: Configure CAPWAP control message data channel offload.
            data_ethernet_II: Configure the wireless controller to use Ethernet II or 802.3 frames with 802.3 data tunnel mode (default = enable).
            link_aggregation: Enable/disable calculating the CAPWAP transmit hash to load balance sessions to link aggregation nodes (default = disable).
            mesh_eth_type: Mesh Ethernet identifier included in backhaul packets (0 - 65535, default = 8755).
            fiapp_eth_type: Ethernet type for Fortinet Inter-Access Point Protocol (IAPP), or IEEE 802.11f, packets (0 - 65535, default = 5252).
            discovery_mc_addr: Multicast IP address for AP discovery (default = 244.0.1.140).
            discovery_mc_addr6: Multicast IPv6 address for AP discovery (default = FF02::18C).
            max_clients: Maximum number of clients that can connect simultaneously (default = 0, meaning no limitation).
            rogue_scan_mac_adjacency: Maximum numerical difference between an AP's Ethernet and wireless MAC values to match for rogue detection (0 - 31, default = 7).
            ipsec_base_ip: Base IP address for IPsec VPN tunnels between the access points and the wireless controller (default = 169.254.0.1).
            wtp_share: Enable/disable sharing of WTPs between VDOMs.
            tunnel_mode: Compatible/strict tunnel mode.
            nac_interval: Interval in seconds between two WiFi network access control (NAC) checks (10 - 600, default = 120).
            ap_log_server: Enable/disable configuring FortiGate to redirect wireless event log messages or FortiAPs to send UTM log messages to a syslog server (default = disable).
            ap_log_server_ip: IP address that FortiGate or FortiAPs send log messages to.
            ap_log_server_port: Port that FortiGate or FortiAPs send log messages to.
            max_sta_offline: Maximum number of station offline stored on the controller (default = 0).
            max_sta_offline_ip2mac: Maximum number of station offline ip2mac stored on the controller (default = 0).
            max_sta_cap: Maximum number of station cap stored on the controller (default = 0).
            max_sta_cap_wtp: Maximum number of station cap's wtp info stored on the controller (1 - 16, default = 8).
            max_rogue_ap: Maximum number of rogue APs stored on the controller (default = 0).
            max_rogue_ap_wtp: Maximum number of rogue AP's wtp info stored on the controller (1 - 16, default = 16).
            max_rogue_sta: Maximum number of rogue stations stored on the controller (default = 0).
            max_wids_entry: Maximum number of wids entries stored on the controller (default = 0).
            max_ble_device: Maximum number of BLE devices stored on the controller (default = 0).
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.wireless_controller_global.put(
            ...     name="existing-object",
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": "existing-object",
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.wireless_controller_global.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            location=location,
            acd_process_count=acd_process_count,
            wpad_process_count=wpad_process_count,
            image_download=image_download,
            rolling_wtp_upgrade=rolling_wtp_upgrade,
            rolling_wtp_upgrade_threshold=rolling_wtp_upgrade_threshold,
            max_retransmit=max_retransmit,
            control_message_offload=control_message_offload,
            data_ethernet_II=data_ethernet_II,
            link_aggregation=link_aggregation,
            mesh_eth_type=mesh_eth_type,
            fiapp_eth_type=fiapp_eth_type,
            discovery_mc_addr=discovery_mc_addr,
            discovery_mc_addr6=discovery_mc_addr6,
            max_clients=max_clients,
            rogue_scan_mac_adjacency=rogue_scan_mac_adjacency,
            ipsec_base_ip=ipsec_base_ip,
            wtp_share=wtp_share,
            tunnel_mode=tunnel_mode,
            nac_interval=nac_interval,
            ap_log_server=ap_log_server,
            ap_log_server_ip=ap_log_server_ip,
            ap_log_server_port=ap_log_server_port,
            max_sta_offline=max_sta_offline,
            max_sta_offline_ip2mac=max_sta_offline_ip2mac,
            max_sta_cap=max_sta_cap,
            max_sta_cap_wtp=max_sta_cap_wtp,
            max_rogue_ap=max_rogue_ap,
            max_rogue_ap_wtp=max_rogue_ap_wtp,
            max_rogue_sta=max_rogue_sta,
            max_wids_entry=max_wids_entry,
            max_ble_device=max_ble_device,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.global_ import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/wireless_controller/global_",
            )
        
        # Singleton endpoint - no identifier needed
        endpoint = "/wireless-controller/global"

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
            "cmdb", endpoint, data=payload_data, params=params, vdom=False        )





    # ========================================================================
    # Action: Move
    # ========================================================================
    
    def move(
        self,
        name: str,
        action: Literal["before", "after"],
        reference_name: str,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move wireless_controller/global_ object to a new position.
        
        Reorders objects by moving one before or after another.
        
        Args:
            name: Name of object to move
            action: Move "before" or "after" reference object
            reference_name: Name of reference object
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Move policy 100 before policy 50
            >>> fgt.api.cmdb.wireless_controller_global.move(
            ...     name="object1",
            ...     action="before",
            ...     reference_name="object2"
            ... )
        """
        # Build params for move operation
        params = {
            "name": name,
            "action": "move",
            action: reference_name,
            **kwargs,
        }
        
        endpoint = "/wireless-controller/global"
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )

    # ========================================================================
    # Action: Clone
    # ========================================================================
    
    def clone(
        self,
        name: str,
        new_name: str,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Clone wireless_controller/global_ object.
        
        Creates a copy of an existing object with a new identifier.
        
        Args:
            name: Name of object to clone
            new_name: Name for the cloned object
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Clone an existing object
            >>> fgt.api.cmdb.wireless_controller_global.clone(
            ...     name="template",
            ...     new_name="new-from-template"
            ... )
        """
        # Build params for clone operation  
        params = {
            "name": name,
            "new_name": new_name,
            "action": "clone",
            **kwargs,
        }
        
        endpoint = "/wireless-controller/global"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )




