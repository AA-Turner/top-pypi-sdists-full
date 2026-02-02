"""
FortiOS CMDB - System modem

Configuration endpoint for managing cmdb system/modem objects.

API Endpoints:
    GET    /cmdb/system/modem
    POST   /cmdb/system/modem
    PUT    /cmdb/system/modem/{identifier}
    DELETE /cmdb/system/modem/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_modem.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_modem.post(
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

class Modem(CRUDEndpoint, MetadataMixin):
    """Modem Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "modem"
    
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
        """Initialize Modem endpoint."""
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
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve system/modem configuration.

        Configuration for system/modem

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
            >>> # Get all system/modem objects
            >>> result = fgt.api.cmdb.system_modem.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_modem.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_modem.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_modem.get_schema()

        See Also:
            - post(): Create new system/modem object
            - put(): Update existing system/modem object
            - delete(): Remove system/modem object
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
            endpoint = f"/system/modem/{quote_path_param(name)}"
            unwrap_single = True
        else:
            endpoint = "/system/modem"
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
            >>> schema = fgt.api.cmdb.system_modem.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_modem.get_schema(format="json-schema")
        
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
        status: Literal["enable", "disable"] | None = None,
        pin_init: str | None = None,
        network_init: str | None = None,
        lockdown_lac: str | None = None,
        mode: Literal["standalone", "redundant"] | None = None,
        auto_dial: Literal["enable", "disable"] | None = None,
        dial_on_demand: Literal["enable", "disable"] | None = None,
        idle_timer: int | None = None,
        redial: Literal["none", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] | None = None,
        reset: int | None = None,
        holddown_timer: int | None = None,
        connect_timeout: int | None = None,
        interface: str | None = None,
        wireless_port: int | None = None,
        dont_send_CR1: Literal["enable", "disable"] | None = None,
        phone1: str | None = None,
        dial_cmd1: str | None = None,
        username1: str | None = None,
        passwd1: str | None = None,
        extra_init1: str | None = None,
        peer_modem1: Literal["generic", "actiontec", "ascend_TNT"] | None = None,
        ppp_echo_request1: Literal["enable", "disable"] | None = None,
        authtype1: Literal["pap", "chap", "mschap", "mschapv2"] | None = None,
        dont_send_CR2: Literal["enable", "disable"] | None = None,
        phone2: str | None = None,
        dial_cmd2: str | None = None,
        username2: str | None = None,
        passwd2: str | None = None,
        extra_init2: str | None = None,
        peer_modem2: Literal["generic", "actiontec", "ascend_TNT"] | None = None,
        ppp_echo_request2: Literal["enable", "disable"] | None = None,
        authtype2: Literal["pap", "chap", "mschap", "mschapv2"] | None = None,
        dont_send_CR3: Literal["enable", "disable"] | None = None,
        phone3: str | None = None,
        dial_cmd3: str | None = None,
        username3: str | None = None,
        passwd3: str | None = None,
        extra_init3: str | None = None,
        peer_modem3: Literal["generic", "actiontec", "ascend_TNT"] | None = None,
        ppp_echo_request3: Literal["enable", "disable"] | None = None,
        altmode: Literal["enable", "disable"] | None = None,
        authtype3: Literal["pap", "chap", "mschap", "mschapv2"] | None = None,
        traffic_check: Literal["enable", "disable"] | None = None,
        action: Literal["dial", "stop", "none"] | None = None,
        distance: int | None = None,
        priority: int | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/modem object.

        Configuration for system/modem

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            status: Enable/disable Modem support (equivalent to bringing an interface up or down).   
enable:Enable setting.   
disable:Disable setting.
            pin_init: AT command to set the PIN (AT+PIN=<pin>).
            network_init: AT command to set the Network name/type (AT+COPS=<mode>,[<format>,<oper>[,<AcT>]]).
            lockdown_lac: Allow connection only to the specified Location Area Code (LAC).
            mode: Set MODEM operation mode to redundant or standalone.   
standalone:Standalone.   
redundant:Redundant for an interface.
            auto_dial: Enable/disable auto-dial after a reboot or disconnection.   
enable:Enable setting.   
disable:Disable setting.
            dial_on_demand: Enable/disable to dial the modem when packets are routed to the modem interface.   
enable:Enable setting.   
disable:Disable setting.
            idle_timer: MODEM connection idle time (1 - 9999 min, default = 5).
            redial: Redial limit (1 - 10 attempts, none = redial forever).   
none:Forever.   
1:One attempt.   
2:Two attempts.   
3:Three attempts.   
4:Four attempts.   
5:Five attempts.   
6:Six attempts.   
7:Seven attempts.   
8:Eight attempts.   
9:Nine attempts.   
10:Ten attempts.
            reset: Number of dial attempts before resetting modem (0 = never reset).
            holddown_timer: Hold down timer in seconds (1 - 60 sec).
            connect_timeout: Connection completion timeout (30 - 255 sec, default = 90).
            interface: Name of redundant interface.
            wireless_port: Enter wireless port number: 0 for default, 1 for first port, and so on (0 - 4294967295).
            dont_send_CR1: Do not send CR when connected (ISP1).   
enable:Enable setting.   
disable:Disable setting.
            phone1: Phone number to connect to the dialup account (must not contain spaces, and should include standard special characters).
            dial_cmd1: Dial command (this is often an ATD or ATDT command).
            username1: User name to access the specified dialup account.
            passwd1: Password to access the specified dialup account.
            extra_init1: Extra initialization string to ISP 1.
            peer_modem1: Specify peer MODEM type for phone1.   
generic:All other modem type.   
actiontec:ActionTec modem.   
ascend_TNT:Ascend TNT modem.
            ppp_echo_request1: Enable/disable PPP echo-request to ISP 1.   
enable:Enable setting.   
disable:Disable setting.
            authtype1: Allowed authentication types for ISP 1.   
pap:PAP   
chap:CHAP   
mschap:MSCHAP   
mschapv2:MSCHAPv2
            dont_send_CR2: Do not send CR when connected (ISP2).   
enable:Enable setting.   
disable:Disable setting.
            phone2: Phone number to connect to the dialup account (must not contain spaces, and should include standard special characters).
            dial_cmd2: Dial command (this is often an ATD or ATDT command).
            username2: User name to access the specified dialup account.
            passwd2: Password to access the specified dialup account.
            extra_init2: Extra initialization string to ISP 2.
            peer_modem2: Specify peer MODEM type for phone2.   
generic:All other modem type.   
actiontec:ActionTec modem.   
ascend_TNT:Ascend TNT modem.
            ppp_echo_request2: Enable/disable PPP echo-request to ISP 2.   
enable:Enable setting.   
disable:Disable setting.
            authtype2: Allowed authentication types for ISP 2.   
pap:PAP   
chap:CHAP   
mschap:MSCHAP   
mschapv2:MSCHAPv2
            dont_send_CR3: Do not send CR when connected (ISP3).   
enable:Enable setting.   
disable:Disable setting.
            phone3: Phone number to connect to the dialup account (must not contain spaces, and should include standard special characters).
            dial_cmd3: Dial command (this is often an ATD or ATDT command).
            username3: User name to access the specified dialup account.
            passwd3: Password to access the specified dialup account.
            extra_init3: Extra initialization string to ISP 3.
            peer_modem3: Specify peer MODEM type for phone3.   
generic:All other modem type.   
actiontec:ActionTec modem.   
ascend_TNT:Ascend TNT modem.
            ppp_echo_request3: Enable/disable PPP echo-request to ISP 3.   
enable:Enable setting.   
disable:Disable setting.
            altmode: Enable/disable altmode for installations using PPP in China.   
enable:Enable setting.   
disable:Disable setting.
            authtype3: Allowed authentication types for ISP 3.   
pap:PAP   
chap:CHAP   
mschap:MSCHAP   
mschapv2:MSCHAPv2
            traffic_check: Enable/disable traffic-check.   
enable:Enable setting.   
disable:Disable setting.
            action: Dial up/stop MODEM.   
dial:Dial up number.   
stop:Stop dialup.   
none:No action.
            distance: Distance of learned routes (1 - 255, default = 1).
            priority: Priority of learned routes (1 - 65535, default = 1).
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.system_modem.put(
            ...     name="existing-object",
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": "existing-object",
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_modem.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            status=status,
            pin_init=pin_init,
            network_init=network_init,
            lockdown_lac=lockdown_lac,
            mode=mode,
            auto_dial=auto_dial,
            dial_on_demand=dial_on_demand,
            idle_timer=idle_timer,
            redial=redial,
            reset=reset,
            holddown_timer=holddown_timer,
            connect_timeout=connect_timeout,
            interface=interface,
            wireless_port=wireless_port,
            dont_send_CR1=dont_send_CR1,
            phone1=phone1,
            dial_cmd1=dial_cmd1,
            username1=username1,
            passwd1=passwd1,
            extra_init1=extra_init1,
            peer_modem1=peer_modem1,
            ppp_echo_request1=ppp_echo_request1,
            authtype1=authtype1,
            dont_send_CR2=dont_send_CR2,
            phone2=phone2,
            dial_cmd2=dial_cmd2,
            username2=username2,
            passwd2=passwd2,
            extra_init2=extra_init2,
            peer_modem2=peer_modem2,
            ppp_echo_request2=ppp_echo_request2,
            authtype2=authtype2,
            dont_send_CR3=dont_send_CR3,
            phone3=phone3,
            dial_cmd3=dial_cmd3,
            username3=username3,
            passwd3=passwd3,
            extra_init3=extra_init3,
            peer_modem3=peer_modem3,
            ppp_echo_request3=ppp_echo_request3,
            altmode=altmode,
            authtype3=authtype3,
            traffic_check=traffic_check,
            action=action,
            distance=distance,
            priority=priority,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.modem import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/modem",
            )
        
        # Singleton endpoint - no identifier needed
        endpoint = "/system/modem"

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
    # Action: Move
    # ========================================================================
    
    def move(
        self,
        name: str,
        action: Literal["before", "after"],
        reference_name: str,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move system/modem object to a new position.
        
        Reorders objects by moving one before or after another.
        
        Args:
            name: Name of object to move
            action: Move "before" or "after" reference object
            reference_name: Name of reference object
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Move policy 100 before policy 50
            >>> fgt.api.cmdb.system_modem.move(
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
            "vdom": vdom,
            **kwargs,
        }
        
        endpoint = "/system/modem"
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )

    # ========================================================================
    # Action: Clone
    # ========================================================================
    
    def clone(
        self,
        name: str,
        new_name: str,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Clone system/modem object.
        
        Creates a copy of an existing object with a new identifier.
        
        Args:
            name: Name of object to clone
            new_name: Name for the cloned object
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Clone an existing object
            >>> fgt.api.cmdb.system_modem.clone(
            ...     name="template",
            ...     new_name="new-from-template"
            ... )
        """
        # Build params for clone operation  
        params = {
            "name": name,
            "new_name": new_name,
            "action": "clone",
            "vdom": vdom,
            **kwargs,
        }
        
        endpoint = "/system/modem"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )




