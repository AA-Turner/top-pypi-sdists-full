"""
FortiOS CMDB - System automation_trigger

Configuration endpoint for managing cmdb system/automation_trigger objects.

API Endpoints:
    GET    /cmdb/system/automation_trigger
    POST   /cmdb/system/automation_trigger
    PUT    /cmdb/system/automation_trigger/{identifier}
    DELETE /cmdb/system/automation_trigger/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_automation_trigger.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_automation_trigger.post(
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

class AutomationTrigger(CRUDEndpoint, MetadataMixin):
    """AutomationTrigger Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "automation_trigger"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "vdom": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "logid": {
            "mkey": "id",
            "required_fields": ['id'],
            "example": "[{'id': 1}]",
        },
        "fields": {
            "mkey": "id",
            "required_fields": ['id'],
            "example": "[{'id': 1}]",
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
    SUPPORTS_CLONE = True
    SUPPORTS_FILTERING = True
    SUPPORTS_PAGINATION = True
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize AutomationTrigger endpoint."""
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
        Retrieve system/automation_trigger configuration.

        Trigger for automation stitches.

        Args:
            name: String identifier to retrieve specific object.
                If None, returns all objects.
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
            >>> # Get all system/automation_trigger objects
            >>> result = fgt.api.cmdb.system_automation_trigger.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific system/automation_trigger by name
            >>> result = fgt.api.cmdb.system_automation_trigger.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_automation_trigger.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_automation_trigger.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_automation_trigger.get_schema()

        See Also:
            - post(): Create new system/automation_trigger object
            - put(): Update existing system/automation_trigger object
            - delete(): Remove system/automation_trigger object
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
            endpoint = "/system/automation-trigger/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/system/automation-trigger"
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
            >>> schema = fgt.api.cmdb.system_automation_trigger.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_automation_trigger.get_schema(format="json-schema")
        
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
        description: str | None = None,
        trigger_type: Literal["event-based", "scheduled"] | None = None,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = None,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = None,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = None,
        stitch_name: str | None = None,
        logid: str | list[str] | list[dict[str, Any]] | None = None,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = None,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = None,
        trigger_day: int | None = None,
        trigger_hour: int | None = None,
        trigger_minute: int | None = None,
        trigger_datetime: Any | None = None,
        fields: str | list[str] | list[dict[str, Any]] | None = None,
        faz_event_name: str | None = None,
        faz_event_severity: str | None = None,
        faz_event_tags: str | None = None,
        serial: str | None = None,
        fabric_event_name: str | None = None,
        fabric_event_severity: str | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/automation_trigger object.

        Trigger for automation stitches.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: Name.
            description: Description.
            trigger_type: Trigger type.
            event_type: Event type.
            vdom: Virtual domain(s) that this trigger is valid for.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            license_type: License type.
            report_type: Security Rating report.
            stitch_name: Triggering stitch name.
            logid: Log IDs to trigger event.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            trigger_frequency: Scheduled trigger frequency (default = daily).
            trigger_weekday: Day of week for trigger.
            trigger_day: Day within a month to trigger.
            trigger_hour: Hour of the day on which to trigger (0 - 23, default = 1).
            trigger_minute: Minute of the hour on which to trigger (0 - 59, default = 0).
            trigger_datetime: Trigger date and time (YYYY-MM-DD HH:MM:SS).
            fields: Customized trigger field settings.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            faz_event_name: FortiAnalyzer event handler name.
            faz_event_severity: FortiAnalyzer event severity.
            faz_event_tags: FortiAnalyzer event tags.
            serial: Fabric connector serial number.
            fabric_event_name: Fabric connector event handler name.
            fabric_event_severity: Fabric connector event severity.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.system_automation_trigger.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_automation_trigger.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if vdom is not None:
            vdom = normalize_table_field(
                vdom,
                mkey="name",
                required_fields=['name'],
                field_name="vdom",
                example="[{'name': 'value'}]",
            )
        if logid is not None:
            logid = normalize_table_field(
                logid,
                mkey="id",
                required_fields=['id'],
                field_name="logid",
                example="[{'id': 1}]",
            )
        if fields is not None:
            fields = normalize_table_field(
                fields,
                mkey="id",
                required_fields=['id'],
                field_name="fields",
                example="[{'id': 1}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            description=description,
            trigger_type=trigger_type,
            event_type=event_type,
            license_type=license_type,
            report_type=report_type,
            stitch_name=stitch_name,
            logid=logid,
            trigger_frequency=trigger_frequency,
            trigger_weekday=trigger_weekday,
            trigger_day=trigger_day,
            trigger_hour=trigger_hour,
            trigger_minute=trigger_minute,
            trigger_datetime=trigger_datetime,
            fields=fields,
            faz_event_name=faz_event_name,
            faz_event_severity=faz_event_severity,
            faz_event_tags=faz_event_tags,
            serial=serial,
            fabric_event_name=fabric_event_name,
            fabric_event_severity=fabric_event_severity,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.automation_trigger import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/automation_trigger",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/system/automation-trigger/" + quote_path_param(name_value)

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
    # POST Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Field-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def post(  # type: ignore[override]
        self,
        payload_dict: dict[str, Any] | None = None,
        name: str | None = None,
        description: str | None = None,
        trigger_type: Literal["event-based", "scheduled"] | None = None,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = None,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = None,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = None,
        stitch_name: str | None = None,
        logid: str | list[str] | list[dict[str, Any]] | None = None,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = None,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = None,
        trigger_day: int | None = None,
        trigger_hour: int | None = None,
        trigger_minute: int | None = None,
        trigger_datetime: Any | None = None,
        fields: str | list[str] | list[dict[str, Any]] | None = None,
        faz_event_name: str | None = None,
        faz_event_severity: str | None = None,
        faz_event_tags: str | None = None,
        serial: str | None = None,
        fabric_event_name: str | None = None,
        fabric_event_severity: str | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new system/automation_trigger object.

        Trigger for automation stitches.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: Name.
            description: Description.
            trigger_type: Trigger type.
            event_type: Event type.
            vdom: Virtual domain(s) that this trigger is valid for.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            license_type: License type.
            report_type: Security Rating report.
            stitch_name: Triggering stitch name.
            logid: Log IDs to trigger event.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            trigger_frequency: Scheduled trigger frequency (default = daily).
            trigger_weekday: Day of week for trigger.
            trigger_day: Day within a month to trigger.
            trigger_hour: Hour of the day on which to trigger (0 - 23, default = 1).
            trigger_minute: Minute of the hour on which to trigger (0 - 59, default = 0).
            trigger_datetime: Trigger date and time (YYYY-MM-DD HH:MM:SS).
            fields: Customized trigger field settings.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            faz_event_name: FortiAnalyzer event handler name.
            faz_event_severity: FortiAnalyzer event severity.
            faz_event_tags: FortiAnalyzer event tags.
            serial: Fabric connector serial number.
            fabric_event_name: Fabric connector event handler name.
            fabric_event_severity: Fabric connector event severity.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.system_automation_trigger.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = AutomationTrigger.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.system_automation_trigger.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(AutomationTrigger.required_fields()) }}
            
            Use AutomationTrigger.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if vdom is not None:
            vdom = normalize_table_field(
                vdom,
                mkey="name",
                required_fields=['name'],
                field_name="vdom",
                example="[{'name': 'value'}]",
            )
        if logid is not None:
            logid = normalize_table_field(
                logid,
                mkey="id",
                required_fields=['id'],
                field_name="logid",
                example="[{'id': 1}]",
            )
        if fields is not None:
            fields = normalize_table_field(
                fields,
                mkey="id",
                required_fields=['id'],
                field_name="fields",
                example="[{'id': 1}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            description=description,
            trigger_type=trigger_type,
            event_type=event_type,
            license_type=license_type,
            report_type=report_type,
            stitch_name=stitch_name,
            logid=logid,
            trigger_frequency=trigger_frequency,
            trigger_weekday=trigger_weekday,
            trigger_day=trigger_day,
            trigger_hour=trigger_hour,
            trigger_minute=trigger_minute,
            trigger_datetime=trigger_datetime,
            fields=fields,
            faz_event_name=faz_event_name,
            faz_event_severity=faz_event_severity,
            faz_event_tags=faz_event_tags,
            serial=serial,
            fabric_event_name=fabric_event_name,
            fabric_event_severity=fabric_event_severity,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.automation_trigger import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/automation_trigger",
            )

        endpoint = "/system/automation-trigger"
        
        # Add explicit query parameters for POST
        params: dict[str, Any] = {}
        if q_action is not None:
            params["action"] = q_action
        if q_nkey is not None:
            params["nkey"] = q_nkey
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data=payload_data, params=params, vdom=False        )

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
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete system/automation_trigger object.

        Trigger for automation stitches.

        Args:
            name: Primary key identifier
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is not provided

        Examples:
            >>> # Delete specific object
            >>> result = fgt.api.cmdb.system_automation_trigger.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/system/automation-trigger/" + quote_path_param(name)

        # Add explicit query parameters for DELETE
        params: dict[str, Any] = {}
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=False        )

    def exists(
        self,
        name: str,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if system/automation_trigger object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.system_automation_trigger.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.system_automation_trigger.exists(name=1):
            ...     fgt.api.cmdb.system_automation_trigger.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/system/automation-trigger"
        endpoint = f"{endpoint}/{quote_path_param(name)}"
        
        try:
            result = self.get(name=name)
            
            # Check if result is a coroutine (async) or direct response (sync)
            # Note: Type checkers can't narrow Union[T, Coroutine[T]] in conditionals
            if hasattr(result, '__await__'):
                # Async response - return coroutine that checks status
                async def _check() -> bool:
                    r = await result  # type: ignore[misc]
                    response = r.raw if hasattr(r, 'raw') else r
                    return is_success(response)
                return _check()
            else:
                # Sync response - check status directly
                response = result.raw if hasattr(result, 'raw') else result  # type: ignore[union-attr]
                return is_success(response)
        except Exception:
            # Any error (404, network, etc.) means we can't confirm existence
            return False


    def set(
        self,
        payload_dict: dict[str, Any] | None = None,
        name: str | None = None,
        description: str | None = None,
        trigger_type: Literal["event-based", "scheduled"] | None = None,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = None,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = None,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = None,
        stitch_name: str | None = None,
        logid: str | list[str] | list[dict[str, Any]] | None = None,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = None,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = None,
        trigger_day: int | None = None,
        trigger_hour: int | None = None,
        trigger_minute: int | None = None,
        trigger_datetime: Any | None = None,
        fields: str | list[str] | list[dict[str, Any]] | None = None,
        faz_event_name: str | None = None,
        faz_event_severity: str | None = None,
        faz_event_tags: str | None = None,
        serial: str | None = None,
        fabric_event_name: str | None = None,
        fabric_event_severity: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update system/automation_trigger object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            description: Field description
            trigger_type: Field trigger-type
            event_type: Field event-type
            license_type: Field license-type
            report_type: Field report-type
            stitch_name: Field stitch-name
            logid: Field logid
            trigger_frequency: Field trigger-frequency
            trigger_weekday: Field trigger-weekday
            trigger_day: Field trigger-day
            trigger_hour: Field trigger-hour
            trigger_minute: Field trigger-minute
            trigger_datetime: Field trigger-datetime
            fields: Field fields
            faz_event_name: Field faz-event-name
            faz_event_severity: Field faz-event-severity
            faz_event_tags: Field faz-event-tags
            serial: Field serial
            fabric_event_name: Field fabric-event-name
            fabric_event_severity: Field fabric-event-severity
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.system_automation_trigger.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.system_automation_trigger.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.system_automation_trigger.set(payload_dict=obj_data)
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
        if vdom is not None:
            vdom = normalize_table_field(
                vdom,
                mkey="name",
                required_fields=['name'],
                field_name="vdom",
                example="[{'name': 'value'}]",
            )
        if logid is not None:
            logid = normalize_table_field(
                logid,
                mkey="id",
                required_fields=['id'],
                field_name="logid",
                example="[{'id': 1}]",
            )
        if fields is not None:
            fields = normalize_table_field(
                fields,
                mkey="id",
                required_fields=['id'],
                field_name="fields",
                example="[{'id': 1}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            description=description,
            trigger_type=trigger_type,
            event_type=event_type,
            license_type=license_type,
            report_type=report_type,
            stitch_name=stitch_name,
            logid=logid,
            trigger_frequency=trigger_frequency,
            trigger_weekday=trigger_weekday,
            trigger_day=trigger_day,
            trigger_hour=trigger_hour,
            trigger_minute=trigger_minute,
            trigger_datetime=trigger_datetime,
            fields=fields,
            faz_event_name=faz_event_name,
            faz_event_severity=faz_event_severity,
            faz_event_tags=faz_event_tags,
            serial=serial,
            fabric_event_name=fabric_event_name,
            fabric_event_severity=fabric_event_severity,
            data=payload_dict,
        )
        
        mkey_value = payload_data.get("name")
        if not mkey_value:
            raise ValueError("name is required for set()")
        
        # Check if resource exists
        if self.exists(name=mkey_value):
            # Update existing resource
            return self.put(payload_dict=payload_data, **kwargs)
        else:
            # Create new resource
            return self.post(payload_dict=payload_data, **kwargs)

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
        Move system/automation_trigger object to a new position.
        
        Reorders objects by moving one before or after another.
        
        Args:
            name: Identifier of object to move
            action: Move "before" or "after" reference object
            reference_name: Identifier of reference object
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Move policy 100 before policy 50
            >>> fgt.api.cmdb.system_automation_trigger.move(
            ...     name=100,
            ...     action="before",
            ...     reference_name=50
            ... )
        """
        # Build params for move operation
        params = {
            "name": name,
            "action": "move",
            action: reference_name,
            **kwargs,
        }
        
        endpoint = "/system/automation-trigger"
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
        Clone system/automation_trigger object.
        
        Creates a copy of an existing object with a new identifier.
        
        Args:
            name: Identifier of object to clone
            new_name: Identifier for the cloned object
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Clone an existing object
            >>> fgt.api.cmdb.system_automation_trigger.clone(
            ...     name=1,
            ...     new_name=100
            ... )
        """
        # Build params for clone operation  
        params = {
            "name": name,
            "new_name": new_name,
            "action": "clone",
            **kwargs,
        }
        
        endpoint = "/system/automation-trigger"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )




