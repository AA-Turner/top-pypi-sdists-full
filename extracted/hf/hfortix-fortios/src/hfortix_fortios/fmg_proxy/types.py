"""
Type definitions for FortiManager Proxy objects.

These TypedDicts define the structure of ADOMs, devices, and other
FMG-specific objects returned by the proxy client.
"""

from typing import TYPE_CHECKING, TypedDict, Literal

if TYPE_CHECKING:
    # Import FortiObject for creating typed wrappers
    from hfortix_fortios.models import FortiObject


class FMGAdomDict(TypedDict, total=False):
    """
    FortiManager ADOM (Administrative Domain) object.
    
    Common fields returned by get_adoms().
    """
    name: str  # ADOM name
    oid: int  # Object ID
    desc: str  # Description
    flags: int | list[str]  # ADOM flags
    mode: str  # ADOM mode
    mr: int  # Management region
    restricted_prds: str  # Restricted products
    state: int  # ADOM state
    uuid: str  # Unique identifier
    workspace_mode: int  # Workspace mode


class FMGHASlave(TypedDict, total=False):
    """HA slave device information."""
    conf_status: int  # Configuration status
    did: str  # Device ID
    flags: list[str] | None  # Device flags
    idx: int  # Index
    name: str  # Device name
    oid: int  # Object ID
    prio: int  # Priority
    role: Literal["master", "slave"]  # HA role
    sn: str  # Serial number
    status: int  # Status code


class FMGDeviceDict(TypedDict, total=False):
    """
    FortiManager device object.
    
    Common fields returned by get_devices() and get_device().
    Based on FortiManager API device structure.
    """
    # Basic identification
    name: str  # Device name
    sn: str  # Serial number
    hostname: str  # Device hostname
    desc: str  # Description
    
    # Network information
    ip: str  # IP address
    eip: str  # External IP
    mgmt_if: str  # Management interface
    mgmt_mode: Literal["fmgfaz", "fmg", "faz", "unreg"]  # Management mode
    mgmt_uuid: str  # Management UUID
    
    # Status and connection
    conn_mode: Literal["active", "passive"]  # Connection mode
    conn_status: Literal["up", "down"]  # Connection status
    conf_status: Literal["insync", "outofsync", "unknown"]  # Config sync status
    db_status: Literal["nomod", "mod"]  # Database status
    dev_status: str  # Device status
    
    # Version information
    os_type: Literal["FortiGate", "FortiWiFi", "FortiSwitch", "FortiAP", "FortiExtender"]  # OS type
    os_ver: str  # OS version (e.g., "7.0")
    patch: int  # Patch level
    build: int  # Build number
    branch_pt: int  # Branch point
    mr: int  # Major release
    
    # Hardware information
    platform_str: str  # Platform string (e.g., "FortiGate-100F")
    hw_rev_major: int  # Hardware revision major
    hw_rev_minor: int  # Hardware revision minor
    hw_generation: int  # Hardware generation
    maxvdom: int  # Maximum VDOMs
    
    # License information
    lic_flags: int  # License flags
    lic_region: str  # License region
    foslic_type: Literal["permanent", "trial", "temporary"]  # License type
    foslic_cpu: int  # Licensed CPU count
    foslic_ram: int  # Licensed RAM
    foslic_utm: str | None  # UTM license
    foslic_dr_site: Literal["enable", "disable"]  # DR site license
    
    # Storage
    hdisk_size: int  # Hard disk size (MB)
    logdisk_size: int  # Log disk size (MB)
    
    # High Availability
    ha_mode: Literal["AP", "AA", "standalone"]  # HA mode
    ha_group_id: int  # HA group ID
    ha_group_name: str  # HA group name
    ha_slave: list[FMGHASlave]  # HA slave devices
    ha_upgrade_mode: int  # HA upgrade mode
    
    # VDOM information
    mgt_vdom: str  # Management VDOM
    vdom: list[dict[str, str | int]] | None  # VDOMs list
    
    # Threat protection versions
    av_ver: str  # Antivirus version
    ips_ver: str  # IPS version
    ips_ext: int  # IPS extended
    app_ver: str  # Application control version
    
    # Geographic location
    latitude: str  # Latitude
    longitude: str  # Longitude
    location_from: Literal["diag", "gps", "manual"]  # Location source
    
    # Timestamps
    first_tunnel_up: int  # First tunnel up timestamp
    last_checked: int  # Last checked timestamp
    last_resync: int  # Last resync timestamp
    
    # FortiAnalyzer
    faz_full_act: int  # FAZ full activation
    faz_perm: int  # FAZ permissions
    faz_quota: int  # FAZ quota
    faz_used: int  # FAZ used space
    
    # Counts
    fap_cnt: int  # FortiAP count
    fsw_cnt: int  # FortiSwitch count
    fex_cnt: int  # FortiExtender count
    
    # Other
    adm_usr: str  # Admin username
    adm_pass: list[str]  # Admin password (encrypted)
    beta: int  # Beta flag
    checksum: str  # Configuration checksum
    cluster_worker: str  # Cluster worker
    flags: list[str]  # Device flags
    hyperscale: int  # Hyperscale flag
    module_sn: str  # Module serial number
    oid: int  # Object ID
    prefer_img_ver: str  # Preferred image version
    psk: str  # Pre-shared key
    vm_cpu: int  # VM CPU count
    vm_cpu_limit: int  # VM CPU limit
    vm_lic_expire: int  # VM license expiry
    vm_mem: int  # VM memory
    vm_mem_limit: int  # VM memory limit
    vm_status: int  # VM status
