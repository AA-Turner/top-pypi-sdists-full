"""
Pydantic Models for CMDB - system/sdn_connector

Runtime validation models for system/sdn_connector configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class SdnConnectorServerList(BaseModel):
    """
    Child table model for server-list.
    
    Server address list of the remote SDN connector.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    ip: str = Field(max_length=15, description="IPv4 address.")
class SdnConnectorRouteTableRoute(BaseModel):
    """
    Child table model for route-table.route.
    
    Configure Azure route.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=63, description="Route name.")    
    next_hop: str = Field(max_length=127, description="Next hop address.")
class SdnConnectorRouteTable(BaseModel):
    """
    Child table model for route-table.
    
    Configure Azure route table.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=63, description="Route table name.")    
    subscription_id: str | None = Field(max_length=63, default=None, description="Subscription ID of Azure route table.")    
    resource_group: str | None = Field(max_length=63, default=None, description="Resource group of Azure route table.")    
    route: list[SdnConnectorRouteTableRoute] = Field(default_factory=list, description="Configure Azure route.")
class SdnConnectorRoute(BaseModel):
    """
    Child table model for route.
    
    Configure GCP route.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=63, description="Route name.")
class SdnConnectorOciRegionList(BaseModel):
    """
    Child table model for oci-region-list.
    
    Configure OCI region list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    region: str = Field(max_length=31, description="OCI region.")
class SdnConnectorNicIp(BaseModel):
    """
    Child table model for nic.ip.
    
    Configure IP configuration.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=63, description="IP configuration name.")    
    private_ip: str | None = Field(max_length=39, default=None, description="Private IP address.")    
    public_ip: str | None = Field(max_length=63, default=None, description="Public IP name.")    
    resource_group: str | None = Field(max_length=63, default=None, description="Resource group of Azure public IP.")
class SdnConnectorNic(BaseModel):
    """
    Child table model for nic.
    
    Configure Azure network interface.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=63, description="Network interface name.")    
    peer_nic: str | None = Field(max_length=63, default=None, description="Peer network interface name.")    
    ip: list[SdnConnectorNicIp] = Field(default_factory=list, description="Configure IP configuration.")
class SdnConnectorGcpProjectListGcpZoneList(BaseModel):
    """
    Child table model for gcp-project-list.gcp-zone-list.
    
    Configure GCP zone list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=127, description="GCP zone name.")
class SdnConnectorGcpProjectList(BaseModel):
    """
    Child table model for gcp-project-list.
    
    Configure GCP project list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: str = Field(max_length=127, serialization_alias="id", description="GCP project ID.")    
    gcp_zone_list: list[SdnConnectorGcpProjectListGcpZoneList] = Field(default_factory=list, description="Configure GCP zone list.")
class SdnConnectorForwardingRule(BaseModel):
    """
    Child table model for forwarding-rule.
    
    Configure GCP forwarding rule.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    rule_name: str = Field(max_length=63, description="Forwarding rule name.")    
    target: str = Field(max_length=63, description="Target instance name.")
class SdnConnectorExternalIp(BaseModel):
    """
    Child table model for external-ip.
    
    Configure GCP external IP.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    name: str = Field(max_length=63, description="External IP name.")
class SdnConnectorExternalAccountListRegionList(BaseModel):
    """
    Child table model for external-account-list.region-list.
    
    AWS region name list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    region: str = Field(max_length=31, description="AWS region name.")
class SdnConnectorExternalAccountList(BaseModel):
    """
    Child table model for external-account-list.
    
    Configure AWS external account list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    role_arn: str = Field(max_length=2047, description="AWS role ARN to assume.")    
    external_id: str | None = Field(max_length=1399, default=None, description="AWS external ID.")    
    region_list: list[SdnConnectorExternalAccountListRegionList] = Field(description="AWS region name list.")
class SdnConnectorCompartmentList(BaseModel):
    """
    Child table model for compartment-list.
    
    Configure OCI compartment list.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    compartment_id: str = Field(max_length=127, description="OCI compartment ID.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class SdnConnectorTypeEnum(str, Enum):
    """Allowed values for type_ field."""
    ACI = "aci"
    ALICLOUD = "alicloud"
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    NSX = "nsx"
    NUAGE = "nuage"
    OCI = "oci"
    OPENSTACK = "openstack"
    KUBERNETES = "kubernetes"
    VMWARE = "vmware"
    SEPM = "sepm"
    ACI_DIRECT = "aci-direct"
    IBM = "ibm"
    NUTANIX = "nutanix"
    SAP = "sap"

class SdnConnectorAzureRegionEnum(str, Enum):
    """Allowed values for azure_region field."""
    GLOBAL = "global"
    CHINA = "china"
    GERMANY = "germany"
    USGOV = "usgov"
    LOCAL = "local"

class SdnConnectorIbmRegionEnum(str, Enum):
    """Allowed values for ibm_region field."""
    DALLAS = "dallas"
    WASHINGTON_DC = "washington-dc"
    LONDON = "london"
    FRANKFURT = "frankfurt"
    SYDNEY = "sydney"
    TOKYO = "tokyo"
    OSAKA = "osaka"
    TORONTO = "toronto"
    SAO_PAULO = "sao-paulo"
    MADRID = "madrid"


# ============================================================================
# Main Model
# ============================================================================

class SdnConnectorModel(BaseModel):
    """
    Pydantic model for system/sdn_connector configuration.
    
    Configure connection to SDN Connector.
    
    Validation Rules:        - name: max_length=35 pattern=        - status: pattern=        - type_: pattern=        - proxy: max_length=35 pattern=        - use_metadata_iam: pattern=        - microsoft_365: pattern=        - ha_status: pattern=        - verify_certificate: pattern=        - vdom: max_length=31 pattern=        - server: max_length=127 pattern=        - server_list: pattern=        - server_port: min=0 max=65535 pattern=        - message_server_port: min=0 max=65535 pattern=        - username: max_length=64 pattern=        - password: pattern=        - vcenter_server: max_length=127 pattern=        - vcenter_username: max_length=64 pattern=        - vcenter_password: pattern=        - access_key: max_length=31 pattern=        - secret_key: max_length=59 pattern=        - region: max_length=31 pattern=        - vpc_id: max_length=31 pattern=        - alt_resource_ip: pattern=        - external_account_list: pattern=        - tenant_id: max_length=127 pattern=        - client_id: max_length=63 pattern=        - client_secret: max_length=59 pattern=        - subscription_id: max_length=63 pattern=        - resource_group: max_length=63 pattern=        - login_endpoint: max_length=127 pattern=        - resource_url: max_length=127 pattern=        - azure_region: pattern=        - nic: pattern=        - route_table: pattern=        - user_id: max_length=127 pattern=        - compartment_list: pattern=        - oci_region_list: pattern=        - oci_region_type: pattern=        - oci_cert: max_length=63 pattern=        - oci_fingerprint: max_length=63 pattern=        - external_ip: pattern=        - route: pattern=        - gcp_project_list: pattern=        - forwarding_rule: pattern=        - service_account: max_length=127 pattern=        - private_key: pattern=        - secret_token: pattern=        - domain: max_length=127 pattern=        - group_name: max_length=127 pattern=        - server_cert: max_length=127 pattern=        - server_ca_cert: max_length=127 pattern=        - api_key: max_length=59 pattern=        - ibm_region: pattern=        - par_id: max_length=63 pattern=        - update_interval: min=0 max=3600 pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=35, default=None, description="SDN connector name.")    
    status: Literal["disable", "enable"] = Field(default="enable", description="Enable/disable connection to the remote SDN connector.")    
    type_: SdnConnectorTypeEnum = Field(default=SdnConnectorTypeEnum.AWS, serialization_alias="type", description="Type of SDN connector.")    
    proxy: str | None = Field(max_length=35, default=None, description="SDN proxy.")  # datasource: ['system.sdn-proxy.name']    
    use_metadata_iam: Literal["disable", "enable"] = Field(default="disable", description="Enable/disable use of IAM role from metadata to call API.")    
    microsoft_365: Literal["disable", "enable"] = Field(default="disable", description="Enable to use as Microsoft 365 connector.")    
    ha_status: Literal["disable", "enable"] = Field(default="disable", description="Enable/disable use for FortiGate HA service.")    
    verify_certificate: Literal["disable", "enable"] = Field(default="enable", description="Enable/disable server certificate verification.")    
    vdom: str | None = Field(max_length=31, default=None, description="Virtual domain name of the remote SDN connector.")  # datasource: ['system.vdom.name']    
    server: str = Field(max_length=127, description="Server address of the remote SDN connector.")    
    server_list: list[SdnConnectorServerList] = Field(description="Server address list of the remote SDN connector.")    
    server_port: int | None = Field(ge=0, le=65535, default=0, description="Port number of the remote SDN connector.")    
    message_server_port: int | None = Field(ge=0, le=65535, default=0, description="HTTP port number of the SAP message server.")    
    username: str = Field(max_length=64, description="Username of the remote SDN connector as login credentials.")    
    password: Any = Field(description="Password of the remote SDN connector as login credentials.")    
    vcenter_server: str | None = Field(max_length=127, default=None, description="vCenter server address for NSX quarantine.")    
    vcenter_username: str | None = Field(max_length=64, default=None, description="vCenter server username for NSX quarantine.")    
    vcenter_password: Any = Field(default=None, description="vCenter server password for NSX quarantine.")    
    access_key: str = Field(max_length=31, description="AWS / ACS access key ID.")    
    secret_key: Any = Field(max_length=59, description="AWS / ACS secret access key.")    
    region: str = Field(max_length=31, description="AWS / ACS region name.")    
    vpc_id: str | None = Field(max_length=31, default=None, description="AWS VPC ID.")    
    alt_resource_ip: Literal["disable", "enable"] | None = Field(default="disable", description="Enable/disable AWS alternative resource IP.")    
    external_account_list: list[SdnConnectorExternalAccountList] = Field(default_factory=list, description="Configure AWS external account list.")    
    tenant_id: str | None = Field(max_length=127, default=None, description="Tenant ID (directory ID).")    
    client_id: str | None = Field(max_length=63, default=None, description="Azure client ID (application ID).")    
    client_secret: Any = Field(max_length=59, default=None, description="Azure client secret (application key).")    
    subscription_id: str | None = Field(max_length=63, default=None, description="Azure subscription ID.")    
    resource_group: str | None = Field(max_length=63, default=None, description="Azure resource group.")    
    login_endpoint: str | None = Field(max_length=127, default=None, description="Azure Stack login endpoint.")    
    resource_url: str | None = Field(max_length=127, default=None, description="Azure Stack resource URL.")    
    azure_region: SdnConnectorAzureRegionEnum | None = Field(default=SdnConnectorAzureRegionEnum.GLOBAL, description="Azure server region.")    
    nic: list[SdnConnectorNic] = Field(default_factory=list, description="Configure Azure network interface.")    
    route_table: list[SdnConnectorRouteTable] = Field(default_factory=list, description="Configure Azure route table.")    
    user_id: str | None = Field(max_length=127, default=None, description="User ID.")    
    compartment_list: list[SdnConnectorCompartmentList] = Field(default_factory=list, description="Configure OCI compartment list.")    
    oci_region_list: list[SdnConnectorOciRegionList] = Field(default_factory=list, description="Configure OCI region list.")    
    oci_region_type: Literal["commercial", "government"] = Field(default="commercial", description="OCI region type.")    
    oci_cert: str | None = Field(max_length=63, default=None, description="OCI certificate.")  # datasource: ['certificate.local.name']    
    oci_fingerprint: str | None = Field(max_length=63, default=None, description="OCI pubkey fingerprint.")    
    external_ip: list[SdnConnectorExternalIp] = Field(default_factory=list, description="Configure GCP external IP.")    
    route: list[SdnConnectorRoute] = Field(default_factory=list, description="Configure GCP route.")    
    gcp_project_list: list[SdnConnectorGcpProjectList] = Field(default_factory=list, description="Configure GCP project list.")    
    forwarding_rule: list[SdnConnectorForwardingRule] = Field(default_factory=list, description="Configure GCP forwarding rule.")    
    service_account: str = Field(max_length=127, description="GCP service account email.")    
    private_key: str = Field(description="Private key of GCP service account.")    
    secret_token: str = Field(description="Secret token of Kubernetes service account.")    
    domain: str | None = Field(max_length=127, default=None, description="Domain name.")    
    group_name: str | None = Field(max_length=127, default=None, description="Full path group name of computers.")    
    server_cert: str | None = Field(max_length=127, default=None, description="Trust servers that contain this certificate only.")  # datasource: ['certificate.remote.name']    
    server_ca_cert: str | None = Field(max_length=127, default=None, description="Trust only those servers whose certificate is directly/indirectly signed by this certificate.")  # datasource: ['certificate.remote.name', 'certificate.ca.name']    
    api_key: Any = Field(max_length=59, description="IBM cloud API key or service ID API key.")    
    ibm_region: SdnConnectorIbmRegionEnum = Field(default=SdnConnectorIbmRegionEnum.DALLAS, description="IBM cloud region name.")    
    par_id: str | None = Field(max_length=63, default=None, description="Public address range ID.")    
    update_interval: int | None = Field(ge=0, le=3600, default=60, description="Dynamic object update interval (30 - 3600 sec, default = 60, 0 = disabled).")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
    @field_validator('proxy')
    @classmethod
    def validate_proxy(cls, v: Any) -> Any:
        """
        Validate proxy field.
        
        Datasource: ['system.sdn-proxy.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('vdom')
    @classmethod
    def validate_vdom(cls, v: Any) -> Any:
        """
        Validate vdom field.
        
        Datasource: ['system.vdom.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('oci_cert')
    @classmethod
    def validate_oci_cert(cls, v: Any) -> Any:
        """
        Validate oci_cert field.
        
        Datasource: ['certificate.local.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('server_cert')
    @classmethod
    def validate_server_cert(cls, v: Any) -> Any:
        """
        Validate server_cert field.
        
        Datasource: ['certificate.remote.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    @field_validator('server_ca_cert')
    @classmethod
    def validate_server_ca_cert(cls, v: Any) -> Any:
        """
        Validate server_ca_cert field.
        
        Datasource: ['certificate.remote.name', 'certificate.ca.name']
        
        Note:
            This validator only checks basic constraints.
            To validate that referenced object exists, query the API.
        """
        # Basic validation passed via Field() constraints
        # Additional datasource validation could be added here
        return v    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def to_fortios_dict(self) -> dict[str, Any]:
        """
        Convert model to FortiOS API payload format.
        
        Returns:
            Dict suitable for POST/PUT operations
        """
        # Export with exclude_none to avoid sending null values
        return self.model_dump(exclude_none=True, by_alias=True)
    
    @classmethod
    def from_fortios_response(cls, data: dict[str, Any]) -> "SdnConnectorModel":
        """
        Create model instance from FortiOS API response.
        
        Args:
            data: Response data from API
            
        Returns:
            Validated model instance
        """
        return cls(**data)
    # ========================================================================
    # Datasource Validation Methods
    # ========================================================================    
    async def validate_proxy_references(self, client: Any) -> list[str]:
        """
        Validate proxy references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - system/sdn-proxy        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = SdnConnectorModel(
            ...     proxy="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_proxy_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.system.sdn_connector.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "proxy", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.system.sdn_proxy.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Proxy '{value}' not found in "
                "system/sdn-proxy"
            )        
        return errors    
    async def validate_vdom_references(self, client: Any) -> list[str]:
        """
        Validate vdom references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - system/vdom        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = SdnConnectorModel(
            ...     vdom="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_vdom_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.system.sdn_connector.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "vdom", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.system.vdom.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Vdom '{value}' not found in "
                "system/vdom"
            )        
        return errors    
    async def validate_oci_cert_references(self, client: Any) -> list[str]:
        """
        Validate oci_cert references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - certificate/local        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = SdnConnectorModel(
            ...     oci_cert="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_oci_cert_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.system.sdn_connector.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "oci_cert", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.certificate.local.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Oci-Cert '{value}' not found in "
                "certificate/local"
            )        
        return errors    
    async def validate_server_cert_references(self, client: Any) -> list[str]:
        """
        Validate server_cert references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - certificate/remote        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = SdnConnectorModel(
            ...     server_cert="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_server_cert_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.system.sdn_connector.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "server_cert", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.certificate.remote.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Server-Cert '{value}' not found in "
                "certificate/remote"
            )        
        return errors    
    async def validate_server_ca_cert_references(self, client: Any) -> list[str]:
        """
        Validate server_ca_cert references exist in FortiGate.
        
        This method checks if referenced objects exist by calling exists() on
        the appropriate API endpoints. This is an OPTIONAL validation step that
        can be called before posting to the API to catch reference errors early.
        
        Datasource endpoints checked:
        - certificate/remote        - certificate/ca        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of validation error messages (empty if all valid)
            
        Example:
            >>> from hfortix_fortios import FortiOS
            >>> 
            >>> fgt = FortiOS(host="192.168.1.1", token="your-token")
            >>> policy = SdnConnectorModel(
            ...     server_ca_cert="invalid-name",
            ... )
            >>> 
            >>> # Validate before posting
            >>> errors = await policy.validate_server_ca_cert_references(fgt._client)
            >>> if errors:
            ...     print("Validation failed:", errors)
            ... else:
            ...     result = await fgt.api.cmdb.system.sdn_connector.post(policy.to_fortios_dict())
        """
        errors: list[str] = []
        
        # Validate scalar field
        value = getattr(self, "server_ca_cert", None)
        if not value:
            return errors
        
        # Check all datasource endpoints
        found = False
        if await client.api.cmdb.certificate.remote.exists(value):
            found = True
        elif await client.api.cmdb.certificate.ca.exists(value):
            found = True
        
        if not found:
            errors.append(
                f"Server-Ca-Cert '{value}' not found in "
                "certificate/remote or certificate/ca"
            )        
        return errors    
    async def validate_all_references(self, client: Any) -> list[str]:
        """
        Validate ALL datasource references in this model.
        
        Convenience method that runs all validate_*_references() methods
        and aggregates the results.
        
        Args:
            client: FortiOS client instance (from fgt._client)
            
        Returns:
            List of all validation errors found
            
        Example:
            >>> errors = await policy.validate_all_references(fgt._client)
            >>> if errors:
            ...     for error in errors:
            ...         print(f"  - {error}")
        """
        all_errors = []
        
        errors = await self.validate_proxy_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_vdom_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_oci_cert_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_server_cert_references(client)
        all_errors.extend(errors)        
        errors = await self.validate_server_ca_cert_references(client)
        all_errors.extend(errors)        
        return all_errors

# ============================================================================
# Type Aliases for Convenience
# ============================================================================

Dict = dict[str, Any]  # For backward compatibility

# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "SdnConnectorModel",    "SdnConnectorServerList",    "SdnConnectorExternalAccountList",    "SdnConnectorExternalAccountList.RegionList",    "SdnConnectorNic",    "SdnConnectorNic.Ip",    "SdnConnectorRouteTable",    "SdnConnectorRouteTable.Route",    "SdnConnectorCompartmentList",    "SdnConnectorOciRegionList",    "SdnConnectorExternalIp",    "SdnConnectorRoute",    "SdnConnectorGcpProjectList",    "SdnConnectorGcpProjectList.GcpZoneList",    "SdnConnectorForwardingRule",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:55.405312Z
# ============================================================================