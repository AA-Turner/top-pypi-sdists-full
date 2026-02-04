"""
FortiOS CMDB - System sdn_connector

Configuration endpoint for managing cmdb system/sdn_connector objects.

API Endpoints:
    GET    /cmdb/system/sdn_connector
    POST   /cmdb/system/sdn_connector
    PUT    /cmdb/system/sdn_connector/{identifier}
    DELETE /cmdb/system/sdn_connector/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_sdn_connector.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_sdn_connector.post(
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

class SdnConnector(CRUDEndpoint, MetadataMixin):
    """SdnConnector Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "sdn_connector"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "server_list": {
            "mkey": "ip",
            "required_fields": ['ip'],
            "example": "[{'ip': '192.168.1.10'}]",
        },
        "external_account_list": {
            "mkey": "role-arn",
            "required_fields": ['role-arn', 'region-list'],
            "example": "[{'role-arn': 'value', 'region-list': 'value'}]",
        },
        "nic": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "route_table": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "compartment_list": {
            "mkey": "compartment-id",
            "required_fields": ['compartment-id'],
            "example": "[{'compartment-id': 'value'}]",
        },
        "oci_region_list": {
            "mkey": "region",
            "required_fields": ['region'],
            "example": "[{'region': 'value'}]",
        },
        "external_ip": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "route": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "gcp_project_list": {
            "mkey": "id",
            "required_fields": ['id'],
            "example": "[{'id': 1}]",
        },
        "forwarding_rule": {
            "mkey": "rule-name",
            "required_fields": ['rule-name', 'target'],
            "example": "[{'rule-name': 'value', 'target': 'value'}]",
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
        """Initialize SdnConnector endpoint."""
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
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve system/sdn_connector configuration.

        Configure connection to SDN Connector.

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
            >>> # Get all system/sdn_connector objects
            >>> result = fgt.api.cmdb.system_sdn_connector.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific system/sdn_connector by name
            >>> result = fgt.api.cmdb.system_sdn_connector.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_sdn_connector.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_sdn_connector.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_sdn_connector.get_schema()

        See Also:
            - post(): Create new system/sdn_connector object
            - put(): Update existing system/sdn_connector object
            - delete(): Remove system/sdn_connector object
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
            endpoint = "/system/sdn-connector/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/system/sdn-connector"
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
            >>> schema = fgt.api.cmdb.system_sdn_connector.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_sdn_connector.get_schema(format="json-schema")
        
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
        status: Literal["disable", "enable"] | None = None,
        type: Literal["aci", "alicloud", "aws", "azure", "gcp", "nsx", "nuage", "oci", "openstack", "kubernetes", "vmware", "sepm", "aci-direct", "ibm", "nutanix", "sap"] | None = None,
        proxy: str | None = None,
        use_metadata_iam: Literal["disable", "enable"] | None = None,
        microsoft_365: Literal["disable", "enable"] | None = None,
        ha_status: Literal["disable", "enable"] | None = None,
        verify_certificate: Literal["disable", "enable"] | None = None,
        server: str | None = None,
        server_list: str | list[str] | list[dict[str, Any]] | None = None,
        server_port: int | None = None,
        message_server_port: int | None = None,
        username: str | None = None,
        password: Any | None = None,
        vcenter_server: str | None = None,
        vcenter_username: str | None = None,
        vcenter_password: Any | None = None,
        access_key: str | None = None,
        secret_key: Any | None = None,
        region: str | None = None,
        vpc_id: str | None = None,
        alt_resource_ip: Literal["disable", "enable"] | None = None,
        external_account_list: str | list[str] | list[dict[str, Any]] | None = None,
        tenant_id: str | None = None,
        client_id: str | None = None,
        client_secret: Any | None = None,
        subscription_id: str | None = None,
        resource_group: str | None = None,
        login_endpoint: str | None = None,
        resource_url: str | None = None,
        azure_region: Literal["global", "china", "germany", "usgov", "local"] | None = None,
        nic: str | list[str] | list[dict[str, Any]] | None = None,
        route_table: str | list[str] | list[dict[str, Any]] | None = None,
        user_id: str | None = None,
        compartment_list: str | list[str] | list[dict[str, Any]] | None = None,
        oci_region_list: str | list[str] | list[dict[str, Any]] | None = None,
        oci_region_type: Literal["commercial", "government"] | None = None,
        oci_cert: str | None = None,
        oci_fingerprint: str | None = None,
        external_ip: str | list[str] | list[dict[str, Any]] | None = None,
        route: str | list[str] | list[dict[str, Any]] | None = None,
        gcp_project_list: str | list[str] | list[dict[str, Any]] | None = None,
        forwarding_rule: str | list[str] | list[dict[str, Any]] | None = None,
        service_account: str | None = None,
        private_key: str | None = None,
        secret_token: str | None = None,
        domain: str | None = None,
        group_name: str | None = None,
        server_cert: str | None = None,
        server_ca_cert: str | None = None,
        api_key: Any | None = None,
        ibm_region: Literal["dallas", "washington-dc", "london", "frankfurt", "sydney", "tokyo", "osaka", "toronto", "sao-paulo", "madrid"] | None = None,
        par_id: str | None = None,
        update_interval: int | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/sdn_connector object.

        Configure connection to SDN Connector.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: SDN connector name.
            status: Enable/disable connection to the remote SDN connector.
            type: Type of SDN connector.
            proxy: SDN proxy.
            use_metadata_iam: Enable/disable use of IAM role from metadata to call API.
            microsoft_365: Enable to use as Microsoft 365 connector.
            ha_status: Enable/disable use for FortiGate HA service.
            verify_certificate: Enable/disable server certificate verification.
            vdom: Virtual domain name of the remote SDN connector.
            server: Server address of the remote SDN connector.
            server_list: Server address list of the remote SDN connector.
                Default format: [{'ip': '192.168.1.10'}]
                Supported formats:
                  - Single string: "value" → [{'ip': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'ip': 'val1'}, ...]
                  - List of dicts: [{'ip': '192.168.1.10'}] (recommended)
            server_port: Port number of the remote SDN connector.
            message_server_port: HTTP port number of the SAP message server.
            username: Username of the remote SDN connector as login credentials.
            password: Password of the remote SDN connector as login credentials.
            vcenter_server: vCenter server address for NSX quarantine.
            vcenter_username: vCenter server username for NSX quarantine.
            vcenter_password: vCenter server password for NSX quarantine.
            access_key: AWS / ACS access key ID.
            secret_key: AWS / ACS secret access key.
            region: AWS / ACS region name.
            vpc_id: AWS VPC ID.
            alt_resource_ip: Enable/disable AWS alternative resource IP.
            external_account_list: Configure AWS external account list.
                Default format: [{'role-arn': 'value', 'region-list': 'value'}]
                Required format: List of dicts with keys: role-arn, region-list
                  (String format not allowed due to multiple required fields)
            tenant_id: Tenant ID (directory ID).
            client_id: Azure client ID (application ID).
            client_secret: Azure client secret (application key).
            subscription_id: Azure subscription ID.
            resource_group: Azure resource group.
            login_endpoint: Azure Stack login endpoint.
            resource_url: Azure Stack resource URL.
            azure_region: Azure server region.
            nic: Configure Azure network interface.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            route_table: Configure Azure route table.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            user_id: User ID.
            compartment_list: Configure OCI compartment list.
                Default format: [{'compartment-id': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'compartment-id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'compartment-id': 'val1'}, ...]
                  - List of dicts: [{'compartment-id': 'value'}] (recommended)
            oci_region_list: Configure OCI region list.
                Default format: [{'region': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'region': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'region': 'val1'}, ...]
                  - List of dicts: [{'region': 'value'}] (recommended)
            oci_region_type: OCI region type.
            oci_cert: OCI certificate.
            oci_fingerprint: OCI pubkey fingerprint.
            external_ip: Configure GCP external IP.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            route: Configure GCP route.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            gcp_project_list: Configure GCP project list.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            forwarding_rule: Configure GCP forwarding rule.
                Default format: [{'rule-name': 'value', 'target': 'value'}]
                Required format: List of dicts with keys: rule-name, target
                  (String format not allowed due to multiple required fields)
            service_account: GCP service account email.
            private_key: Private key of GCP service account.
            secret_token: Secret token of Kubernetes service account.
            domain: Domain name.
            group_name: Full path group name of computers.
            server_cert: Trust servers that contain this certificate only.
            server_ca_cert: Trust only those servers whose certificate is directly/indirectly signed by this certificate.
            api_key: IBM cloud API key or service ID API key.
            ibm_region: IBM cloud region name.
            par_id: Public address range ID.
            update_interval: Dynamic object update interval (30 - 3600 sec, default = 60, 0 = disabled).
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.system_sdn_connector.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_sdn_connector.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if server_list is not None:
            server_list = normalize_table_field(
                server_list,
                mkey="ip",
                required_fields=['ip'],
                field_name="server_list",
                example="[{'ip': '192.168.1.10'}]",
            )
        if external_account_list is not None:
            external_account_list = normalize_table_field(
                external_account_list,
                mkey="role-arn",
                required_fields=['role-arn', 'region-list'],
                field_name="external_account_list",
                example="[{'role-arn': 'value', 'region-list': 'value'}]",
            )
        if nic is not None:
            nic = normalize_table_field(
                nic,
                mkey="name",
                required_fields=['name'],
                field_name="nic",
                example="[{'name': 'value'}]",
            )
        if route_table is not None:
            route_table = normalize_table_field(
                route_table,
                mkey="name",
                required_fields=['name'],
                field_name="route_table",
                example="[{'name': 'value'}]",
            )
        if compartment_list is not None:
            compartment_list = normalize_table_field(
                compartment_list,
                mkey="compartment-id",
                required_fields=['compartment-id'],
                field_name="compartment_list",
                example="[{'compartment-id': 'value'}]",
            )
        if oci_region_list is not None:
            oci_region_list = normalize_table_field(
                oci_region_list,
                mkey="region",
                required_fields=['region'],
                field_name="oci_region_list",
                example="[{'region': 'value'}]",
            )
        if external_ip is not None:
            external_ip = normalize_table_field(
                external_ip,
                mkey="name",
                required_fields=['name'],
                field_name="external_ip",
                example="[{'name': 'value'}]",
            )
        if route is not None:
            route = normalize_table_field(
                route,
                mkey="name",
                required_fields=['name'],
                field_name="route",
                example="[{'name': 'value'}]",
            )
        if gcp_project_list is not None:
            gcp_project_list = normalize_table_field(
                gcp_project_list,
                mkey="id",
                required_fields=['id'],
                field_name="gcp_project_list",
                example="[{'id': 1}]",
            )
        if forwarding_rule is not None:
            forwarding_rule = normalize_table_field(
                forwarding_rule,
                mkey="rule-name",
                required_fields=['rule-name', 'target'],
                field_name="forwarding_rule",
                example="[{'rule-name': 'value', 'target': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            status=status,
            type=type,
            proxy=proxy,
            use_metadata_iam=use_metadata_iam,
            microsoft_365=microsoft_365,
            ha_status=ha_status,
            verify_certificate=verify_certificate,
            server=server,
            server_list=server_list,
            server_port=server_port,
            message_server_port=message_server_port,
            username=username,
            password=password,
            vcenter_server=vcenter_server,
            vcenter_username=vcenter_username,
            vcenter_password=vcenter_password,
            access_key=access_key,
            secret_key=secret_key,
            region=region,
            vpc_id=vpc_id,
            alt_resource_ip=alt_resource_ip,
            external_account_list=external_account_list,
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            subscription_id=subscription_id,
            resource_group=resource_group,
            login_endpoint=login_endpoint,
            resource_url=resource_url,
            azure_region=azure_region,
            nic=nic,
            route_table=route_table,
            user_id=user_id,
            compartment_list=compartment_list,
            oci_region_list=oci_region_list,
            oci_region_type=oci_region_type,
            oci_cert=oci_cert,
            oci_fingerprint=oci_fingerprint,
            external_ip=external_ip,
            route=route,
            gcp_project_list=gcp_project_list,
            forwarding_rule=forwarding_rule,
            service_account=service_account,
            private_key=private_key,
            secret_token=secret_token,
            domain=domain,
            group_name=group_name,
            server_cert=server_cert,
            server_ca_cert=server_ca_cert,
            api_key=api_key,
            ibm_region=ibm_region,
            par_id=par_id,
            update_interval=update_interval,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.sdn_connector import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/sdn_connector",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/system/sdn-connector/" + quote_path_param(name_value)

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
        status: Literal["disable", "enable"] | None = None,
        type: Literal["aci", "alicloud", "aws", "azure", "gcp", "nsx", "nuage", "oci", "openstack", "kubernetes", "vmware", "sepm", "aci-direct", "ibm", "nutanix", "sap"] | None = None,
        proxy: str | None = None,
        use_metadata_iam: Literal["disable", "enable"] | None = None,
        microsoft_365: Literal["disable", "enable"] | None = None,
        ha_status: Literal["disable", "enable"] | None = None,
        verify_certificate: Literal["disable", "enable"] | None = None,
        server: str | None = None,
        server_list: str | list[str] | list[dict[str, Any]] | None = None,
        server_port: int | None = None,
        message_server_port: int | None = None,
        username: str | None = None,
        password: Any | None = None,
        vcenter_server: str | None = None,
        vcenter_username: str | None = None,
        vcenter_password: Any | None = None,
        access_key: str | None = None,
        secret_key: Any | None = None,
        region: str | None = None,
        vpc_id: str | None = None,
        alt_resource_ip: Literal["disable", "enable"] | None = None,
        external_account_list: str | list[str] | list[dict[str, Any]] | None = None,
        tenant_id: str | None = None,
        client_id: str | None = None,
        client_secret: Any | None = None,
        subscription_id: str | None = None,
        resource_group: str | None = None,
        login_endpoint: str | None = None,
        resource_url: str | None = None,
        azure_region: Literal["global", "china", "germany", "usgov", "local"] | None = None,
        nic: str | list[str] | list[dict[str, Any]] | None = None,
        route_table: str | list[str] | list[dict[str, Any]] | None = None,
        user_id: str | None = None,
        compartment_list: str | list[str] | list[dict[str, Any]] | None = None,
        oci_region_list: str | list[str] | list[dict[str, Any]] | None = None,
        oci_region_type: Literal["commercial", "government"] | None = None,
        oci_cert: str | None = None,
        oci_fingerprint: str | None = None,
        external_ip: str | list[str] | list[dict[str, Any]] | None = None,
        route: str | list[str] | list[dict[str, Any]] | None = None,
        gcp_project_list: str | list[str] | list[dict[str, Any]] | None = None,
        forwarding_rule: str | list[str] | list[dict[str, Any]] | None = None,
        service_account: str | None = None,
        private_key: str | None = None,
        secret_token: str | None = None,
        domain: str | None = None,
        group_name: str | None = None,
        server_cert: str | None = None,
        server_ca_cert: str | None = None,
        api_key: Any | None = None,
        ibm_region: Literal["dallas", "washington-dc", "london", "frankfurt", "sydney", "tokyo", "osaka", "toronto", "sao-paulo", "madrid"] | None = None,
        par_id: str | None = None,
        update_interval: int | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new system/sdn_connector object.

        Configure connection to SDN Connector.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: SDN connector name.
            status: Enable/disable connection to the remote SDN connector.
            type: Type of SDN connector.
            proxy: SDN proxy.
            use_metadata_iam: Enable/disable use of IAM role from metadata to call API.
            microsoft_365: Enable to use as Microsoft 365 connector.
            ha_status: Enable/disable use for FortiGate HA service.
            verify_certificate: Enable/disable server certificate verification.
            vdom: Virtual domain name of the remote SDN connector.
            server: Server address of the remote SDN connector.
            server_list: Server address list of the remote SDN connector.
                Default format: [{'ip': '192.168.1.10'}]
                Supported formats:
                  - Single string: "value" → [{'ip': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'ip': 'val1'}, ...]
                  - List of dicts: [{'ip': '192.168.1.10'}] (recommended)
            server_port: Port number of the remote SDN connector.
            message_server_port: HTTP port number of the SAP message server.
            username: Username of the remote SDN connector as login credentials.
            password: Password of the remote SDN connector as login credentials.
            vcenter_server: vCenter server address for NSX quarantine.
            vcenter_username: vCenter server username for NSX quarantine.
            vcenter_password: vCenter server password for NSX quarantine.
            access_key: AWS / ACS access key ID.
            secret_key: AWS / ACS secret access key.
            region: AWS / ACS region name.
            vpc_id: AWS VPC ID.
            alt_resource_ip: Enable/disable AWS alternative resource IP.
            external_account_list: Configure AWS external account list.
                Default format: [{'role-arn': 'value', 'region-list': 'value'}]
                Required format: List of dicts with keys: role-arn, region-list
                  (String format not allowed due to multiple required fields)
            tenant_id: Tenant ID (directory ID).
            client_id: Azure client ID (application ID).
            client_secret: Azure client secret (application key).
            subscription_id: Azure subscription ID.
            resource_group: Azure resource group.
            login_endpoint: Azure Stack login endpoint.
            resource_url: Azure Stack resource URL.
            azure_region: Azure server region.
            nic: Configure Azure network interface.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            route_table: Configure Azure route table.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            user_id: User ID.
            compartment_list: Configure OCI compartment list.
                Default format: [{'compartment-id': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'compartment-id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'compartment-id': 'val1'}, ...]
                  - List of dicts: [{'compartment-id': 'value'}] (recommended)
            oci_region_list: Configure OCI region list.
                Default format: [{'region': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'region': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'region': 'val1'}, ...]
                  - List of dicts: [{'region': 'value'}] (recommended)
            oci_region_type: OCI region type.
            oci_cert: OCI certificate.
            oci_fingerprint: OCI pubkey fingerprint.
            external_ip: Configure GCP external IP.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            route: Configure GCP route.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            gcp_project_list: Configure GCP project list.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            forwarding_rule: Configure GCP forwarding rule.
                Default format: [{'rule-name': 'value', 'target': 'value'}]
                Required format: List of dicts with keys: rule-name, target
                  (String format not allowed due to multiple required fields)
            service_account: GCP service account email.
            private_key: Private key of GCP service account.
            secret_token: Secret token of Kubernetes service account.
            domain: Domain name.
            group_name: Full path group name of computers.
            server_cert: Trust servers that contain this certificate only.
            server_ca_cert: Trust only those servers whose certificate is directly/indirectly signed by this certificate.
            api_key: IBM cloud API key or service ID API key.
            ibm_region: IBM cloud region name.
            par_id: Public address range ID.
            update_interval: Dynamic object update interval (30 - 3600 sec, default = 60, 0 = disabled).
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.system_sdn_connector.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = SdnConnector.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.system_sdn_connector.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(SdnConnector.required_fields()) }}
            
            Use SdnConnector.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if server_list is not None:
            server_list = normalize_table_field(
                server_list,
                mkey="ip",
                required_fields=['ip'],
                field_name="server_list",
                example="[{'ip': '192.168.1.10'}]",
            )
        if external_account_list is not None:
            external_account_list = normalize_table_field(
                external_account_list,
                mkey="role-arn",
                required_fields=['role-arn', 'region-list'],
                field_name="external_account_list",
                example="[{'role-arn': 'value', 'region-list': 'value'}]",
            )
        if nic is not None:
            nic = normalize_table_field(
                nic,
                mkey="name",
                required_fields=['name'],
                field_name="nic",
                example="[{'name': 'value'}]",
            )
        if route_table is not None:
            route_table = normalize_table_field(
                route_table,
                mkey="name",
                required_fields=['name'],
                field_name="route_table",
                example="[{'name': 'value'}]",
            )
        if compartment_list is not None:
            compartment_list = normalize_table_field(
                compartment_list,
                mkey="compartment-id",
                required_fields=['compartment-id'],
                field_name="compartment_list",
                example="[{'compartment-id': 'value'}]",
            )
        if oci_region_list is not None:
            oci_region_list = normalize_table_field(
                oci_region_list,
                mkey="region",
                required_fields=['region'],
                field_name="oci_region_list",
                example="[{'region': 'value'}]",
            )
        if external_ip is not None:
            external_ip = normalize_table_field(
                external_ip,
                mkey="name",
                required_fields=['name'],
                field_name="external_ip",
                example="[{'name': 'value'}]",
            )
        if route is not None:
            route = normalize_table_field(
                route,
                mkey="name",
                required_fields=['name'],
                field_name="route",
                example="[{'name': 'value'}]",
            )
        if gcp_project_list is not None:
            gcp_project_list = normalize_table_field(
                gcp_project_list,
                mkey="id",
                required_fields=['id'],
                field_name="gcp_project_list",
                example="[{'id': 1}]",
            )
        if forwarding_rule is not None:
            forwarding_rule = normalize_table_field(
                forwarding_rule,
                mkey="rule-name",
                required_fields=['rule-name', 'target'],
                field_name="forwarding_rule",
                example="[{'rule-name': 'value', 'target': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            status=status,
            type=type,
            proxy=proxy,
            use_metadata_iam=use_metadata_iam,
            microsoft_365=microsoft_365,
            ha_status=ha_status,
            verify_certificate=verify_certificate,
            server=server,
            server_list=server_list,
            server_port=server_port,
            message_server_port=message_server_port,
            username=username,
            password=password,
            vcenter_server=vcenter_server,
            vcenter_username=vcenter_username,
            vcenter_password=vcenter_password,
            access_key=access_key,
            secret_key=secret_key,
            region=region,
            vpc_id=vpc_id,
            alt_resource_ip=alt_resource_ip,
            external_account_list=external_account_list,
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            subscription_id=subscription_id,
            resource_group=resource_group,
            login_endpoint=login_endpoint,
            resource_url=resource_url,
            azure_region=azure_region,
            nic=nic,
            route_table=route_table,
            user_id=user_id,
            compartment_list=compartment_list,
            oci_region_list=oci_region_list,
            oci_region_type=oci_region_type,
            oci_cert=oci_cert,
            oci_fingerprint=oci_fingerprint,
            external_ip=external_ip,
            route=route,
            gcp_project_list=gcp_project_list,
            forwarding_rule=forwarding_rule,
            service_account=service_account,
            private_key=private_key,
            secret_token=secret_token,
            domain=domain,
            group_name=group_name,
            server_cert=server_cert,
            server_ca_cert=server_ca_cert,
            api_key=api_key,
            ibm_region=ibm_region,
            par_id=par_id,
            update_interval=update_interval,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.sdn_connector import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/sdn_connector",
            )

        endpoint = "/system/sdn-connector"
        
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
        Delete system/sdn_connector object.

        Configure connection to SDN Connector.

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
            >>> result = fgt.api.cmdb.system_sdn_connector.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/system/sdn-connector/" + quote_path_param(name)

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
        Check if system/sdn_connector object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.system_sdn_connector.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.system_sdn_connector.exists(name=1):
            ...     fgt.api.cmdb.system_sdn_connector.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/system/sdn-connector"
        endpoint = f"{endpoint}/{quote_path_param(name)}"
        
        try:
            # Use silent=True to suppress 404 error logging
            result = self._client.get("cmdb", endpoint, vdom=False, silent=True)
            
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
        status: Literal["disable", "enable"] | None = None,
        type: Literal["aci", "alicloud", "aws", "azure", "gcp", "nsx", "nuage", "oci", "openstack", "kubernetes", "vmware", "sepm", "aci-direct", "ibm", "nutanix", "sap"] | None = None,
        proxy: str | None = None,
        use_metadata_iam: Literal["disable", "enable"] | None = None,
        microsoft_365: Literal["disable", "enable"] | None = None,
        ha_status: Literal["disable", "enable"] | None = None,
        verify_certificate: Literal["disable", "enable"] | None = None,
        server: str | None = None,
        server_list: str | list[str] | list[dict[str, Any]] | None = None,
        server_port: int | None = None,
        message_server_port: int | None = None,
        username: str | None = None,
        password: Any | None = None,
        vcenter_server: str | None = None,
        vcenter_username: str | None = None,
        vcenter_password: Any | None = None,
        access_key: str | None = None,
        secret_key: Any | None = None,
        region: str | None = None,
        vpc_id: str | None = None,
        alt_resource_ip: Literal["disable", "enable"] | None = None,
        external_account_list: str | list[str] | list[dict[str, Any]] | None = None,
        tenant_id: str | None = None,
        client_id: str | None = None,
        client_secret: Any | None = None,
        subscription_id: str | None = None,
        resource_group: str | None = None,
        login_endpoint: str | None = None,
        resource_url: str | None = None,
        azure_region: Literal["global", "china", "germany", "usgov", "local"] | None = None,
        nic: str | list[str] | list[dict[str, Any]] | None = None,
        route_table: str | list[str] | list[dict[str, Any]] | None = None,
        user_id: str | None = None,
        compartment_list: str | list[str] | list[dict[str, Any]] | None = None,
        oci_region_list: str | list[str] | list[dict[str, Any]] | None = None,
        oci_region_type: Literal["commercial", "government"] | None = None,
        oci_cert: str | None = None,
        oci_fingerprint: str | None = None,
        external_ip: str | list[str] | list[dict[str, Any]] | None = None,
        route: str | list[str] | list[dict[str, Any]] | None = None,
        gcp_project_list: str | list[str] | list[dict[str, Any]] | None = None,
        forwarding_rule: str | list[str] | list[dict[str, Any]] | None = None,
        service_account: str | None = None,
        private_key: str | None = None,
        secret_token: str | None = None,
        domain: str | None = None,
        group_name: str | None = None,
        server_cert: str | None = None,
        server_ca_cert: str | None = None,
        api_key: Any | None = None,
        ibm_region: Literal["dallas", "washington-dc", "london", "frankfurt", "sydney", "tokyo", "osaka", "toronto", "sao-paulo", "madrid"] | None = None,
        par_id: str | None = None,
        update_interval: int | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update system/sdn_connector object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            status: Field status
            type: Field type
            proxy: Field proxy
            use_metadata_iam: Field use-metadata-iam
            microsoft_365: Field microsoft-365
            ha_status: Field ha-status
            verify_certificate: Field verify-certificate
            server: Field server
            server_list: Field server-list
            server_port: Field server-port
            message_server_port: Field message-server-port
            username: Field username
            password: Field password
            vcenter_server: Field vcenter-server
            vcenter_username: Field vcenter-username
            vcenter_password: Field vcenter-password
            access_key: Field access-key
            secret_key: Field secret-key
            region: Field region
            vpc_id: Field vpc-id
            alt_resource_ip: Field alt-resource-ip
            external_account_list: Field external-account-list
            tenant_id: Field tenant-id
            client_id: Field client-id
            client_secret: Field client-secret
            subscription_id: Field subscription-id
            resource_group: Field resource-group
            login_endpoint: Field login-endpoint
            resource_url: Field resource-url
            azure_region: Field azure-region
            nic: Field nic
            route_table: Field route-table
            user_id: Field user-id
            compartment_list: Field compartment-list
            oci_region_list: Field oci-region-list
            oci_region_type: Field oci-region-type
            oci_cert: Field oci-cert
            oci_fingerprint: Field oci-fingerprint
            external_ip: Field external-ip
            route: Field route
            gcp_project_list: Field gcp-project-list
            forwarding_rule: Field forwarding-rule
            service_account: Field service-account
            private_key: Field private-key
            secret_token: Field secret-token
            domain: Field domain
            group_name: Field group-name
            server_cert: Field server-cert
            server_ca_cert: Field server-ca-cert
            api_key: Field api-key
            ibm_region: Field ibm-region
            par_id: Field par-id
            update_interval: Field update-interval
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.system_sdn_connector.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.system_sdn_connector.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.system_sdn_connector.set(payload_dict=obj_data)
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
        if server_list is not None:
            server_list = normalize_table_field(
                server_list,
                mkey="ip",
                required_fields=['ip'],
                field_name="server_list",
                example="[{'ip': '192.168.1.10'}]",
            )
        if external_account_list is not None:
            external_account_list = normalize_table_field(
                external_account_list,
                mkey="role-arn",
                required_fields=['role-arn', 'region-list'],
                field_name="external_account_list",
                example="[{'role-arn': 'value', 'region-list': 'value'}]",
            )
        if nic is not None:
            nic = normalize_table_field(
                nic,
                mkey="name",
                required_fields=['name'],
                field_name="nic",
                example="[{'name': 'value'}]",
            )
        if route_table is not None:
            route_table = normalize_table_field(
                route_table,
                mkey="name",
                required_fields=['name'],
                field_name="route_table",
                example="[{'name': 'value'}]",
            )
        if compartment_list is not None:
            compartment_list = normalize_table_field(
                compartment_list,
                mkey="compartment-id",
                required_fields=['compartment-id'],
                field_name="compartment_list",
                example="[{'compartment-id': 'value'}]",
            )
        if oci_region_list is not None:
            oci_region_list = normalize_table_field(
                oci_region_list,
                mkey="region",
                required_fields=['region'],
                field_name="oci_region_list",
                example="[{'region': 'value'}]",
            )
        if external_ip is not None:
            external_ip = normalize_table_field(
                external_ip,
                mkey="name",
                required_fields=['name'],
                field_name="external_ip",
                example="[{'name': 'value'}]",
            )
        if route is not None:
            route = normalize_table_field(
                route,
                mkey="name",
                required_fields=['name'],
                field_name="route",
                example="[{'name': 'value'}]",
            )
        if gcp_project_list is not None:
            gcp_project_list = normalize_table_field(
                gcp_project_list,
                mkey="id",
                required_fields=['id'],
                field_name="gcp_project_list",
                example="[{'id': 1}]",
            )
        if forwarding_rule is not None:
            forwarding_rule = normalize_table_field(
                forwarding_rule,
                mkey="rule-name",
                required_fields=['rule-name', 'target'],
                field_name="forwarding_rule",
                example="[{'rule-name': 'value', 'target': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            status=status,
            type=type,
            proxy=proxy,
            use_metadata_iam=use_metadata_iam,
            microsoft_365=microsoft_365,
            ha_status=ha_status,
            verify_certificate=verify_certificate,
            server=server,
            server_list=server_list,
            server_port=server_port,
            message_server_port=message_server_port,
            username=username,
            password=password,
            vcenter_server=vcenter_server,
            vcenter_username=vcenter_username,
            vcenter_password=vcenter_password,
            access_key=access_key,
            secret_key=secret_key,
            region=region,
            vpc_id=vpc_id,
            alt_resource_ip=alt_resource_ip,
            external_account_list=external_account_list,
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            subscription_id=subscription_id,
            resource_group=resource_group,
            login_endpoint=login_endpoint,
            resource_url=resource_url,
            azure_region=azure_region,
            nic=nic,
            route_table=route_table,
            user_id=user_id,
            compartment_list=compartment_list,
            oci_region_list=oci_region_list,
            oci_region_type=oci_region_type,
            oci_cert=oci_cert,
            oci_fingerprint=oci_fingerprint,
            external_ip=external_ip,
            route=route,
            gcp_project_list=gcp_project_list,
            forwarding_rule=forwarding_rule,
            service_account=service_account,
            private_key=private_key,
            secret_token=secret_token,
            domain=domain,
            group_name=group_name,
            server_cert=server_cert,
            server_ca_cert=server_ca_cert,
            api_key=api_key,
            ibm_region=ibm_region,
            par_id=par_id,
            update_interval=update_interval,
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
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move system/sdn_connector object to a new position.
        
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
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Examples:
            >>> # Move to top (first position)
            >>> fgt.api.cmdb.system_sdn_connector.move(
            ...     name=100,
            ...     position="top"
            ... )
            
            >>> # Move to specific position (3rd place)
            >>> fgt.api.cmdb.system_sdn_connector.move(
            ...     name=100,
            ...     position=3
            ... )
            
            >>> # Move before another object
            >>> fgt.api.cmdb.system_sdn_connector.move(
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
            all_objects = self.get()
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
            all_objects = self.get()
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
        endpoint = "/system/sdn-connector/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )





