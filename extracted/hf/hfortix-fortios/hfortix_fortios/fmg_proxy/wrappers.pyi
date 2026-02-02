"""
Typed FortiObject wrappers for FortiManager proxy objects.

These are stub-only classes that provide proper type hints for FMG objects.
At runtime, they're just FortiObject instances, but Pylance sees typed attributes.
"""

from typing import TYPE_CHECKING, Literal, Any

if TYPE_CHECKING:
    from hfortix_fortios.models import FortiObject
    from .types import FMGDeviceDict, FMGAdomDict, FMGHASlave


class FMGDevice:
    """
    Typed wrapper for FortiManager device objects.
    
    Provides full autocomplete for all FMG device fields.
    At runtime, this is actually a FortiObject[FMGDeviceDict].
    """
    
    # Basic identification
    name: str
    sn: str
    hostname: str
    desc: str
    
    # Network information  
    ip: str
    eip: str
    mgmt_if: str
    mgmt_mode: Literal["fmgfaz", "fmg", "faz", "unreg"]
    mgmt_uuid: str
    
    # Status and connection
    conn_mode: Literal["active", "passive"]
    conn_status: Literal["up", "down"]
    conf_status: Literal["insync", "outofsync", "unknown"]
    db_status: Literal["nomod", "mod"]
    dev_status: str
    
    # Version information
    os_type: Literal["FortiGate", "FortiWiFi", "FortiSwitch", "FortiAP", "FortiExtender"]
    os_ver: str
    patch: int
    build: int
    branch_pt: int
    mr: int
    
    # Hardware information
    platform_str: str
    hw_rev_major: int
    hw_rev_minor: int
    hw_generation: int
    maxvdom: int
    
    # License information
    lic_flags: int
    lic_region: str
    foslic_type: Literal["permanent", "trial", "temporary"]
    foslic_cpu: int
    foslic_ram: int
    foslic_utm: str | None
    foslic_dr_site: Literal["enable", "disable"]
    
    # Storage
    hdisk_size: int
    logdisk_size: int
    
    # High Availability
    ha_mode: Literal["AP", "AA", "standalone"]
    ha_group_id: int
    ha_group_name: str
    ha_slave: list[FMGHASlave]
    ha_upgrade_mode: int
    
    # VDOM information
    mgt_vdom: str
    vdom: list[dict[str, str | int]] | None
    
    # Threat protection versions
    av_ver: str
    ips_ver: str
    ips_ext: int
    app_ver: str
    
    # Geographic location
    latitude: str
    longitude: str
    location_from: Literal["diag", "gps", "manual"]
    
    # Timestamps
    first_tunnel_up: int
    last_checked: int
    last_resync: int
    
    # FortiAnalyzer
    faz_full_act: int
    faz_perm: int
    faz_quota: int
    faz_used: int
    
    # Counts
    fap_cnt: int
    fsw_cnt: int
    fex_cnt: int
    
    # Other
    adm_usr: str
    adm_pass: list[str]
    beta: int
    checksum: str
    cluster_worker: str
    flags: list[str]
    hyperscale: int
    module_sn: str
    oid: int
    prefer_img_ver: str
    psk: str
    vm_cpu: int
    vm_cpu_limit: int
    vm_lic_expire: int
    vm_mem: int
    vm_mem_limit: int
    vm_status: int
    
    # FortiObject methods
    @property
    def dict(self) -> FMGDeviceDict: ...
    @property
    def json(self) -> str: ...
    @property
    def raw(self) -> dict[str, Any]: ...
    def to_dict(self) -> FMGDeviceDict: ...
    def get_full(self, name: str) -> Any: ...


class FMGAdom:
    """
    Typed wrapper for FortiManager ADOM objects.
    
    Provides full autocomplete for all FMG ADOM fields.
    At runtime, this is actually a FortiObject[FMGAdomDict].
    """
    
    name: str
    oid: int
    desc: str
    flags: int | list[str]
    mode: str
    mr: int
    restricted_prds: str
    state: int
    uuid: str
    workspace_mode: int
    
    # FortiObject methods
    @property
    def dict(self) -> FMGAdomDict: ...
    @property
    def json(self) -> str: ...
    @property
    def raw(self) -> dict[str, Any]: ...
    def to_dict(self) -> FMGAdomDict: ...
    def get_full(self, name: str) -> Any: ...
