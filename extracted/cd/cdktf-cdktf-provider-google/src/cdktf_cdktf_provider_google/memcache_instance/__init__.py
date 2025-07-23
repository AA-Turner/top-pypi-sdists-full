r'''
# `google_memcache_instance`

Refer to the Terraform Registry for docs: [`google_memcache_instance`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class MemcacheInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance google_memcache_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        node_config: typing.Union["MemcacheInstanceNodeConfig", typing.Dict[builtins.str, typing.Any]],
        node_count: jsii.Number,
        authorized_network: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_policy: typing.Optional[typing.Union["MemcacheInstanceMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        memcache_parameters: typing.Optional[typing.Union["MemcacheInstanceMemcacheParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        memcache_version: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reserved_ip_range_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MemcacheInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance google_memcache_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The resource name of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#name MemcacheInstance#name}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#node_config MemcacheInstance#node_config}
        :param node_count: Number of nodes in the memcache instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#node_count MemcacheInstance#node_count}
        :param authorized_network: The full name of the GCE network to connect the instance to. If not provided, 'default' will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#authorized_network MemcacheInstance#authorized_network}
        :param display_name: A user-visible name for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#display_name MemcacheInstance#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#id MemcacheInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#labels MemcacheInstance#labels}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#maintenance_policy MemcacheInstance#maintenance_policy}
        :param memcache_parameters: memcache_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#memcache_parameters MemcacheInstance#memcache_parameters}
        :param memcache_version: The major version of Memcached software. If not provided, latest supported version will be used. Currently the latest supported major version is MEMCACHE_1_5. The minor version will be automatically determined by our system based on the latest supported minor version. Default value: "MEMCACHE_1_5" Possible values: ["MEMCACHE_1_5", "MEMCACHE_1_6_15"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#memcache_version MemcacheInstance#memcache_version}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#project MemcacheInstance#project}.
        :param region: The region of the Memcache instance. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#region MemcacheInstance#region}
        :param reserved_ip_range_id: Contains the name of allocated IP address ranges associated with the private service access connection for example, "test-default" associated with IP range 10.0.0.0/29. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#reserved_ip_range_id MemcacheInstance#reserved_ip_range_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#timeouts MemcacheInstance#timeouts}
        :param zones: Zones where memcache nodes should be provisioned. If not provided, all zones will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#zones MemcacheInstance#zones}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e48e7d09ccd276fccb92df55e8a82b931e29b13f9ac7df4d2b1d8c8f48e1fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MemcacheInstanceConfig(
            name=name,
            node_config=node_config,
            node_count=node_count,
            authorized_network=authorized_network,
            display_name=display_name,
            id=id,
            labels=labels,
            maintenance_policy=maintenance_policy,
            memcache_parameters=memcache_parameters,
            memcache_version=memcache_version,
            project=project,
            region=region,
            reserved_ip_range_id=reserved_ip_range_id,
            timeouts=timeouts,
            zones=zones,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a MemcacheInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MemcacheInstance to import.
        :param import_from_id: The id of the existing MemcacheInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MemcacheInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9bdc31240e4e785ea35c88e23d23bcbe788d7b713ad9440e32d9511ca9ff97)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMaintenancePolicy")
    def put_maintenance_policy(
        self,
        *,
        weekly_maintenance_window: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param weekly_maintenance_window: weekly_maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#weekly_maintenance_window MemcacheInstance#weekly_maintenance_window}
        :param description: Optional. Description of what this policy is for. Create/Update methods return INVALID_ARGUMENT if the length is greater than 512. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#description MemcacheInstance#description}
        '''
        value = MemcacheInstanceMaintenancePolicy(
            weekly_maintenance_window=weekly_maintenance_window,
            description=description,
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenancePolicy", [value]))

    @jsii.member(jsii_name="putMemcacheParameters")
    def put_memcache_parameters(
        self,
        *,
        params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param params: User-defined set of parameters to use in the memcache process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#params MemcacheInstance#params}
        '''
        value = MemcacheInstanceMemcacheParameters(params=params)

        return typing.cast(None, jsii.invoke(self, "putMemcacheParameters", [value]))

    @jsii.member(jsii_name="putNodeConfig")
    def put_node_config(
        self,
        *,
        cpu_count: jsii.Number,
        memory_size_mb: jsii.Number,
    ) -> None:
        '''
        :param cpu_count: Number of CPUs per node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#cpu_count MemcacheInstance#cpu_count}
        :param memory_size_mb: Memory size in Mebibytes for each memcache node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#memory_size_mb MemcacheInstance#memory_size_mb}
        '''
        value = MemcacheInstanceNodeConfig(
            cpu_count=cpu_count, memory_size_mb=memory_size_mb
        )

        return typing.cast(None, jsii.invoke(self, "putNodeConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#create MemcacheInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#delete MemcacheInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#update MemcacheInstance#update}.
        '''
        value = MemcacheInstanceTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuthorizedNetwork")
    def reset_authorized_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizedNetwork", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaintenancePolicy")
    def reset_maintenance_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenancePolicy", []))

    @jsii.member(jsii_name="resetMemcacheParameters")
    def reset_memcache_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemcacheParameters", []))

    @jsii.member(jsii_name="resetMemcacheVersion")
    def reset_memcache_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemcacheVersion", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetReservedIpRangeId")
    def reset_reserved_ip_range_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedIpRangeId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetZones")
    def reset_zones(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZones", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="discoveryEndpoint")
    def discovery_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "discoveryEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicy")
    def maintenance_policy(self) -> "MemcacheInstanceMaintenancePolicyOutputReference":
        return typing.cast("MemcacheInstanceMaintenancePolicyOutputReference", jsii.get(self, "maintenancePolicy"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceSchedule")
    def maintenance_schedule(self) -> "MemcacheInstanceMaintenanceScheduleList":
        return typing.cast("MemcacheInstanceMaintenanceScheduleList", jsii.get(self, "maintenanceSchedule"))

    @builtins.property
    @jsii.member(jsii_name="memcacheFullVersion")
    def memcache_full_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memcacheFullVersion"))

    @builtins.property
    @jsii.member(jsii_name="memcacheNodes")
    def memcache_nodes(self) -> "MemcacheInstanceMemcacheNodesList":
        return typing.cast("MemcacheInstanceMemcacheNodesList", jsii.get(self, "memcacheNodes"))

    @builtins.property
    @jsii.member(jsii_name="memcacheParameters")
    def memcache_parameters(
        self,
    ) -> "MemcacheInstanceMemcacheParametersOutputReference":
        return typing.cast("MemcacheInstanceMemcacheParametersOutputReference", jsii.get(self, "memcacheParameters"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfig")
    def node_config(self) -> "MemcacheInstanceNodeConfigOutputReference":
        return typing.cast("MemcacheInstanceNodeConfigOutputReference", jsii.get(self, "nodeConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MemcacheInstanceTimeoutsOutputReference":
        return typing.cast("MemcacheInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="authorizedNetworkInput")
    def authorized_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizedNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenancePolicyInput")
    def maintenance_policy_input(
        self,
    ) -> typing.Optional["MemcacheInstanceMaintenancePolicy"]:
        return typing.cast(typing.Optional["MemcacheInstanceMaintenancePolicy"], jsii.get(self, "maintenancePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="memcacheParametersInput")
    def memcache_parameters_input(
        self,
    ) -> typing.Optional["MemcacheInstanceMemcacheParameters"]:
        return typing.cast(typing.Optional["MemcacheInstanceMemcacheParameters"], jsii.get(self, "memcacheParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="memcacheVersionInput")
    def memcache_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memcacheVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigInput")
    def node_config_input(self) -> typing.Optional["MemcacheInstanceNodeConfig"]:
        return typing.cast(typing.Optional["MemcacheInstanceNodeConfig"], jsii.get(self, "nodeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedIpRangeIdInput")
    def reserved_ip_range_id_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "reservedIpRangeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MemcacheInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MemcacheInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zonesInput")
    def zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "zonesInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedNetwork")
    def authorized_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizedNetwork"))

    @authorized_network.setter
    def authorized_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1aa83fe4d151cd0c097df20e124d6772f012f1cec65ac5fbc8071af1943c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizedNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17def6254c05212f27493b02521d101099fdedf66d48034a3c9fbc7b4f8c515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ea69da1c434bd81dfa1d2944c006fdad578b550ff45938ad214a77650f779c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7128567bcb4fc080cf8d013855fa20f288606c760bd44e2606c3fdacf19ff276)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memcacheVersion")
    def memcache_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memcacheVersion"))

    @memcache_version.setter
    def memcache_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e8e136d880c18a19a4a81a25a7f3eadac4f8db161f390f7944e859b8b63f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memcacheVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10f9891cf5a1364880121094db1f2a457e5c724c46eee919f02ea9c9cd5a1af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29aad7564600209b9a4b7655474b0a846f55c4da7f0d8ea32d4ba83012bca3bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7500736ed16e00cd835612079da9e8d4e0acc1a0e5580fc763cad1772f032bc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbe9af554f147ba2a61f58e4617b23f717485f38833a70c7292153f5be25f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedIpRangeId")
    def reserved_ip_range_id(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "reservedIpRangeId"))

    @reserved_ip_range_id.setter
    def reserved_ip_range_id(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4598cb878840915d4288137f25b11a6f6c14b9a0ddbd76c3f6dbf497190b5111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedIpRangeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zones")
    def zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "zones"))

    @zones.setter
    def zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2f72fe8fe65b9d6b1125a6b7a7cb80a25c956bb4a863315ad94e2a56064b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zones", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "node_config": "nodeConfig",
        "node_count": "nodeCount",
        "authorized_network": "authorizedNetwork",
        "display_name": "displayName",
        "id": "id",
        "labels": "labels",
        "maintenance_policy": "maintenancePolicy",
        "memcache_parameters": "memcacheParameters",
        "memcache_version": "memcacheVersion",
        "project": "project",
        "region": "region",
        "reserved_ip_range_id": "reservedIpRangeId",
        "timeouts": "timeouts",
        "zones": "zones",
    },
)
class MemcacheInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: builtins.str,
        node_config: typing.Union["MemcacheInstanceNodeConfig", typing.Dict[builtins.str, typing.Any]],
        node_count: jsii.Number,
        authorized_network: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_policy: typing.Optional[typing.Union["MemcacheInstanceMaintenancePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        memcache_parameters: typing.Optional[typing.Union["MemcacheInstanceMemcacheParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        memcache_version: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reserved_ip_range_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MemcacheInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The resource name of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#name MemcacheInstance#name}
        :param node_config: node_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#node_config MemcacheInstance#node_config}
        :param node_count: Number of nodes in the memcache instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#node_count MemcacheInstance#node_count}
        :param authorized_network: The full name of the GCE network to connect the instance to. If not provided, 'default' will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#authorized_network MemcacheInstance#authorized_network}
        :param display_name: A user-visible name for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#display_name MemcacheInstance#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#id MemcacheInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#labels MemcacheInstance#labels}
        :param maintenance_policy: maintenance_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#maintenance_policy MemcacheInstance#maintenance_policy}
        :param memcache_parameters: memcache_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#memcache_parameters MemcacheInstance#memcache_parameters}
        :param memcache_version: The major version of Memcached software. If not provided, latest supported version will be used. Currently the latest supported major version is MEMCACHE_1_5. The minor version will be automatically determined by our system based on the latest supported minor version. Default value: "MEMCACHE_1_5" Possible values: ["MEMCACHE_1_5", "MEMCACHE_1_6_15"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#memcache_version MemcacheInstance#memcache_version}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#project MemcacheInstance#project}.
        :param region: The region of the Memcache instance. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#region MemcacheInstance#region}
        :param reserved_ip_range_id: Contains the name of allocated IP address ranges associated with the private service access connection for example, "test-default" associated with IP range 10.0.0.0/29. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#reserved_ip_range_id MemcacheInstance#reserved_ip_range_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#timeouts MemcacheInstance#timeouts}
        :param zones: Zones where memcache nodes should be provisioned. If not provided, all zones will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#zones MemcacheInstance#zones}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(node_config, dict):
            node_config = MemcacheInstanceNodeConfig(**node_config)
        if isinstance(maintenance_policy, dict):
            maintenance_policy = MemcacheInstanceMaintenancePolicy(**maintenance_policy)
        if isinstance(memcache_parameters, dict):
            memcache_parameters = MemcacheInstanceMemcacheParameters(**memcache_parameters)
        if isinstance(timeouts, dict):
            timeouts = MemcacheInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e2394a8c875d0a810911088908fece46dc0e7cfac2654d2e797dae82d92965)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_config", value=node_config, expected_type=type_hints["node_config"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
            check_type(argname="argument authorized_network", value=authorized_network, expected_type=type_hints["authorized_network"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument maintenance_policy", value=maintenance_policy, expected_type=type_hints["maintenance_policy"])
            check_type(argname="argument memcache_parameters", value=memcache_parameters, expected_type=type_hints["memcache_parameters"])
            check_type(argname="argument memcache_version", value=memcache_version, expected_type=type_hints["memcache_version"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument reserved_ip_range_id", value=reserved_ip_range_id, expected_type=type_hints["reserved_ip_range_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument zones", value=zones, expected_type=type_hints["zones"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "node_config": node_config,
            "node_count": node_count,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if authorized_network is not None:
            self._values["authorized_network"] = authorized_network
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if maintenance_policy is not None:
            self._values["maintenance_policy"] = maintenance_policy
        if memcache_parameters is not None:
            self._values["memcache_parameters"] = memcache_parameters
        if memcache_version is not None:
            self._values["memcache_version"] = memcache_version
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if reserved_ip_range_id is not None:
            self._values["reserved_ip_range_id"] = reserved_ip_range_id
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if zones is not None:
            self._values["zones"] = zones

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#name MemcacheInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_config(self) -> "MemcacheInstanceNodeConfig":
        '''node_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#node_config MemcacheInstance#node_config}
        '''
        result = self._values.get("node_config")
        assert result is not None, "Required property 'node_config' is missing"
        return typing.cast("MemcacheInstanceNodeConfig", result)

    @builtins.property
    def node_count(self) -> jsii.Number:
        '''Number of nodes in the memcache instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#node_count MemcacheInstance#node_count}
        '''
        result = self._values.get("node_count")
        assert result is not None, "Required property 'node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def authorized_network(self) -> typing.Optional[builtins.str]:
        '''The full name of the GCE network to connect the instance to.  If not provided, 'default' will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#authorized_network MemcacheInstance#authorized_network}
        '''
        result = self._values.get("authorized_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A user-visible name for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#display_name MemcacheInstance#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#id MemcacheInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource labels to represent user-provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#labels MemcacheInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def maintenance_policy(
        self,
    ) -> typing.Optional["MemcacheInstanceMaintenancePolicy"]:
        '''maintenance_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#maintenance_policy MemcacheInstance#maintenance_policy}
        '''
        result = self._values.get("maintenance_policy")
        return typing.cast(typing.Optional["MemcacheInstanceMaintenancePolicy"], result)

    @builtins.property
    def memcache_parameters(
        self,
    ) -> typing.Optional["MemcacheInstanceMemcacheParameters"]:
        '''memcache_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#memcache_parameters MemcacheInstance#memcache_parameters}
        '''
        result = self._values.get("memcache_parameters")
        return typing.cast(typing.Optional["MemcacheInstanceMemcacheParameters"], result)

    @builtins.property
    def memcache_version(self) -> typing.Optional[builtins.str]:
        '''The major version of Memcached software.

        If not provided, latest supported version will be used.
        Currently the latest supported major version is MEMCACHE_1_5. The minor version will be automatically
        determined by our system based on the latest supported minor version. Default value: "MEMCACHE_1_5" Possible values: ["MEMCACHE_1_5", "MEMCACHE_1_6_15"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#memcache_version MemcacheInstance#memcache_version}
        '''
        result = self._values.get("memcache_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#project MemcacheInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the Memcache instance. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#region MemcacheInstance#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_ip_range_id(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the name of allocated IP address ranges associated with the private service access connection for example, "test-default" associated with IP range 10.0.0.0/29.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#reserved_ip_range_id MemcacheInstance#reserved_ip_range_id}
        '''
        result = self._values.get("reserved_ip_range_id")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MemcacheInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#timeouts MemcacheInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MemcacheInstanceTimeouts"], result)

    @builtins.property
    def zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Zones where memcache nodes should be provisioned.  If not provided, all zones will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#zones MemcacheInstance#zones}
        '''
        result = self._values.get("zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemcacheInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMaintenancePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "weekly_maintenance_window": "weeklyMaintenanceWindow",
        "description": "description",
    },
)
class MemcacheInstanceMaintenancePolicy:
    def __init__(
        self,
        *,
        weekly_maintenance_window: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param weekly_maintenance_window: weekly_maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#weekly_maintenance_window MemcacheInstance#weekly_maintenance_window}
        :param description: Optional. Description of what this policy is for. Create/Update methods return INVALID_ARGUMENT if the length is greater than 512. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#description MemcacheInstance#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41d8f02d23b2d0758077a1fdddb4ff96818b89d3843462fb860354ffe85b771d)
            check_type(argname="argument weekly_maintenance_window", value=weekly_maintenance_window, expected_type=type_hints["weekly_maintenance_window"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "weekly_maintenance_window": weekly_maintenance_window,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def weekly_maintenance_window(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]:
        '''weekly_maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#weekly_maintenance_window MemcacheInstance#weekly_maintenance_window}
        '''
        result = self._values.get("weekly_maintenance_window")
        assert result is not None, "Required property 'weekly_maintenance_window' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of what this policy is for. Create/Update methods return INVALID_ARGUMENT if the length is greater than 512.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#description MemcacheInstance#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemcacheInstanceMaintenancePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemcacheInstanceMaintenancePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMaintenancePolicyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d7903a4ab9dacdcd1ddb2b8e48e6fac20cbf4e68317c52f8e4929dfa75b8f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWeeklyMaintenanceWindow")
    def put_weekly_maintenance_window(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa3e09e446575bb213d13ac1a047485d646b2b61b0281e91cfed12f25ecc3f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWeeklyMaintenanceWindow", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="weeklyMaintenanceWindow")
    def weekly_maintenance_window(
        self,
    ) -> "MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowList":
        return typing.cast("MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowList", jsii.get(self, "weeklyMaintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyMaintenanceWindowInput")
    def weekly_maintenance_window_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow"]]], jsii.get(self, "weeklyMaintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84df8269d37d624365a4e6720ed1a5c4a535ffec91569c0fbce829e5b68a9dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemcacheInstanceMaintenancePolicy]:
        return typing.cast(typing.Optional[MemcacheInstanceMaintenancePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemcacheInstanceMaintenancePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30a3f11a8e3ce604af73eff4d90a97ee27f29ffc90a9a25f86138226f36d092c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "duration": "duration", "start_time": "startTime"},
)
class MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow:
    def __init__(
        self,
        *,
        day: builtins.str,
        duration: builtins.str,
        start_time: typing.Union["MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param day: Required. The day of week that maintenance updates occur. - DAY_OF_WEEK_UNSPECIFIED: The day of the week is unspecified. - MONDAY: Monday - TUESDAY: Tuesday - WEDNESDAY: Wednesday - THURSDAY: Thursday - FRIDAY: Friday - SATURDAY: Saturday - SUNDAY: Sunday Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#day MemcacheInstance#day}
        :param duration: Required. The length of the maintenance window, ranging from 3 hours to 8 hours. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#duration MemcacheInstance#duration}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#start_time MemcacheInstance#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a33c721f857dc094f0c26e786b1472ddb3a647894efa102dea099ef53c9187)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "duration": duration,
            "start_time": start_time,
        }

    @builtins.property
    def day(self) -> builtins.str:
        '''Required.

        The day of week that maintenance updates occur.

        - DAY_OF_WEEK_UNSPECIFIED: The day of the week is unspecified.
        - MONDAY: Monday
        - TUESDAY: Tuesday
        - WEDNESDAY: Wednesday
        - THURSDAY: Thursday
        - FRIDAY: Friday
        - SATURDAY: Saturday
        - SUNDAY: Sunday Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#day MemcacheInstance#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(self) -> builtins.str:
        '''Required.

        The length of the maintenance window, ranging from 3 hours to 8 hours.
        A duration in seconds with up to nine fractional digits,
        terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#duration MemcacheInstance#duration}
        '''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(
        self,
    ) -> "MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#start_time MemcacheInstance#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519486328a1ed1ba79650e4a5d678d3816878d0b973ee994072facc0c72e5a4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879a044dd1f79d2b03fa50ae15e90dbfda2bd7c2d808fa892c11cf36f5582cbe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e449621a0e43fda74217c5c87b7e6274428873b0fdbbf37c5c54f51d4c7fdb2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ba2f48ce6475fa60c644904743f05a134f9298c6a7f4739df15621eae2ed76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93cd25c155828bf87aed38df664a2538444b777df8e1e2523cdfd74f864ebba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ae87a4611e4f316c37bd43614aea311fb1c8f5833d29b4edacb51f75752523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282b2d58a082693166870f03efbd5ea151e7c8758a39641b713ade6e05271621)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putStartTime")
    def put_start_time(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#hours MemcacheInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#minutes MemcacheInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#nanos MemcacheInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#seconds MemcacheInstance#seconds}
        '''
        value = MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference":
        return typing.cast("MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime"]:
        return typing.cast(typing.Optional["MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16aa9acc722d7914b6b664d0ba7a3c28e914f07f254ae6bd38d7fd80d007ba24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5781bea76d97ce7a4d477d4baed15a80c7901e58eb55381a370a414bf2e2b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__746ea88bae585d5dfc31639f154dcdd6f0dfa74ed5cf9e251d9ed2319b949913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#hours MemcacheInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#minutes MemcacheInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#nanos MemcacheInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. An API may allow the value 60 if it allows leap-seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#seconds MemcacheInstance#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96410136183ef85e97b06bc7036d5cac035d80660fe6dca8d5875d35d304159b)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of day in 24 hour format.

        Should be from 0 to 23.
        An API may choose to allow the value "24:00:00" for scenarios like business closing time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#hours MemcacheInstance#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#minutes MemcacheInstance#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#nanos MemcacheInstance#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time.

        Must normally be from 0 to 59.
        An API may allow the value 60 if it allows leap-seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#seconds MemcacheInstance#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b5495841d62aff534ea296bad77d9115274d5ef9cffb23dac7cbf9eeb305e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12dc93424a7a89cd5a734a9f4f261874e35e3739e01690a4bff20a0dbaacc7af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7743d9ca6dee4e1b94ecdbfd9452c9d0c239b70e68066e4af4a2f462c4fa8f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92172f29653d9ca039b42a3ce434e5ef6f9d42fda4dbae6b17ea2ca88be855f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d26dd347f11ee00b63d3324a1853edbd5d9611e11af062d53480b3d728fe27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime]:
        return typing.cast(typing.Optional[MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ac9e35b6a2a48e8731ff5dd54dc006f41da3160834312e557becf2f16aaeb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMaintenanceSchedule",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemcacheInstanceMaintenanceSchedule:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemcacheInstanceMaintenanceSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemcacheInstanceMaintenanceScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMaintenanceScheduleList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a6b91b4faa560dca4fb12632fcae4eab1c2ba6e5bdfece3b6fb97ef2d103869)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MemcacheInstanceMaintenanceScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f42e8e43a6b1155a0b5d2966bdf69d2e9cd45a272cca65472bf6fba7165534)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemcacheInstanceMaintenanceScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81a94558c6cb4bc200e724a035b089bf129fd8fe23f6a434f2247529600643f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7338c42c1e52e8444e888258804c26cd831ef83d0b427771581470a01793777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf57e5e2691389b850dc9034d633e9780289b7282b2c3f7aaad542da462b3f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemcacheInstanceMaintenanceScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMaintenanceScheduleOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5707d12eb02a43a17a8031597de34f2cd09d924ae7a4e9a262c4c401ba42aa24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="scheduleDeadlineTime")
    def schedule_deadline_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleDeadlineTime"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemcacheInstanceMaintenanceSchedule]:
        return typing.cast(typing.Optional[MemcacheInstanceMaintenanceSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemcacheInstanceMaintenanceSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c90614e39d50e418f7ce9685d96a2754044aa79697037f1613b2f6f1b7090a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMemcacheNodes",
    jsii_struct_bases=[],
    name_mapping={},
)
class MemcacheInstanceMemcacheNodes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemcacheInstanceMemcacheNodes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemcacheInstanceMemcacheNodesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMemcacheNodesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c32dff20f45f7a155b122ebd585771aea00da3da963cac50ab7ad367dda0203)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MemcacheInstanceMemcacheNodesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5d11405d060c8af47afdef05101b0eae61a7ca3857e933dc6f68395f060f9a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MemcacheInstanceMemcacheNodesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cbf2091156d3e312576888b2f79989cbd53995fc5f70bd806237d0111117189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063dffa42d2d526e6c76c60e15726f8525f153da67522e3f4b0dee7bae616cae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76738ae0d74a57d935b1a813837ba685eaa4d6f793971e6f92c5f7b7f10897a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class MemcacheInstanceMemcacheNodesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMemcacheNodesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d3b71e582b648c89314895604da06a148a8a05f8206a30d8447c35cf02497c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeId"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemcacheInstanceMemcacheNodes]:
        return typing.cast(typing.Optional[MemcacheInstanceMemcacheNodes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemcacheInstanceMemcacheNodes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76dae47dac582da92758e09210d8f52b82d24270bf63adb3bd9e270f1f7090b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMemcacheParameters",
    jsii_struct_bases=[],
    name_mapping={"params": "params"},
)
class MemcacheInstanceMemcacheParameters:
    def __init__(
        self,
        *,
        params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param params: User-defined set of parameters to use in the memcache process. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#params MemcacheInstance#params}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df79ba568c61bf29fe2dddde911c85ea241d6d9daa4adfca448de4283f269720)
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if params is not None:
            self._values["params"] = params

    @builtins.property
    def params(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined set of parameters to use in the memcache process.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#params MemcacheInstance#params}
        '''
        result = self._values.get("params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemcacheInstanceMemcacheParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemcacheInstanceMemcacheParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceMemcacheParametersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe084e2476dfa4d77966cfda503dc1ede2b632143afc123fa9cdafed1aa5b9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParams")
    def reset_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParams", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="paramsInput")
    def params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "paramsInput"))

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "params"))

    @params.setter
    def params(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ce9987ee08a66f15aceb43da329f61f88490d1738150bce453109fcdfe759b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "params", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemcacheInstanceMemcacheParameters]:
        return typing.cast(typing.Optional[MemcacheInstanceMemcacheParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemcacheInstanceMemcacheParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__680b1ef863eae4a6acd51f29d148514fb19fcbde62f54b020a3cec20e5941fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceNodeConfig",
    jsii_struct_bases=[],
    name_mapping={"cpu_count": "cpuCount", "memory_size_mb": "memorySizeMb"},
)
class MemcacheInstanceNodeConfig:
    def __init__(self, *, cpu_count: jsii.Number, memory_size_mb: jsii.Number) -> None:
        '''
        :param cpu_count: Number of CPUs per node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#cpu_count MemcacheInstance#cpu_count}
        :param memory_size_mb: Memory size in Mebibytes for each memcache node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#memory_size_mb MemcacheInstance#memory_size_mb}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109ea1cdefa96b338da7779608f9f9fbb937aa18d3d5c0a9464950444a50b210)
            check_type(argname="argument cpu_count", value=cpu_count, expected_type=type_hints["cpu_count"])
            check_type(argname="argument memory_size_mb", value=memory_size_mb, expected_type=type_hints["memory_size_mb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu_count": cpu_count,
            "memory_size_mb": memory_size_mb,
        }

    @builtins.property
    def cpu_count(self) -> jsii.Number:
        '''Number of CPUs per node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#cpu_count MemcacheInstance#cpu_count}
        '''
        result = self._values.get("cpu_count")
        assert result is not None, "Required property 'cpu_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def memory_size_mb(self) -> jsii.Number:
        '''Memory size in Mebibytes for each memcache node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#memory_size_mb MemcacheInstance#memory_size_mb}
        '''
        result = self._values.get("memory_size_mb")
        assert result is not None, "Required property 'memory_size_mb' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemcacheInstanceNodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemcacheInstanceNodeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceNodeConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123d360ecd61340172670002a3f86cc4bef2e4a374c785c7bcd3ef2a57a80368)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="cpuCountInput")
    def cpu_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuCountInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeMbInput")
    def memory_size_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySizeMbInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCount")
    def cpu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCount"))

    @cpu_count.setter
    def cpu_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68f3964dd51a5c445d31f765115e965c30b528cc70e5f74ed10d4e4fa899bac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySizeMb")
    def memory_size_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeMb"))

    @memory_size_mb.setter
    def memory_size_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49b1d61a03bc2eadffdca3afb1bb6c4db2b14b8ff9cdf41e6c882cbf937b0293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySizeMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MemcacheInstanceNodeConfig]:
        return typing.cast(typing.Optional[MemcacheInstanceNodeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MemcacheInstanceNodeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e8c1f9d25dd1f1656638f22b617d891bde9bdf4258b0a81dfb2a1170c4324e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class MemcacheInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#create MemcacheInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#delete MemcacheInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#update MemcacheInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86e25a192ec66e1fb241d59e18e072bdddf9dfbc552daba09032bbb605038593)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#create MemcacheInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#delete MemcacheInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/memcache_instance#update MemcacheInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemcacheInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MemcacheInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.memcacheInstance.MemcacheInstanceTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d322a14e38699a399b9d6d0f3bac50c1b19d5c8c55e261664818e8600aa086f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba0f0168f7a9d91cd108fbd259aa8fb7b32a9b7eb5673c5b109818fd392f3f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348c3cb870df52186fc4da197449975fbb12cbdc0501f3bc7c5e106316283b4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b491d5ab687f372910d86055727c8b0c5ce2a34185bcc2de7962a6a12f3a6b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemcacheInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemcacheInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemcacheInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6def35c1d1fb2269d14c40535f59eb9da164a1a5f3e2a49237e6ef030cbef959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MemcacheInstance",
    "MemcacheInstanceConfig",
    "MemcacheInstanceMaintenancePolicy",
    "MemcacheInstanceMaintenancePolicyOutputReference",
    "MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow",
    "MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowList",
    "MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowOutputReference",
    "MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime",
    "MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTimeOutputReference",
    "MemcacheInstanceMaintenanceSchedule",
    "MemcacheInstanceMaintenanceScheduleList",
    "MemcacheInstanceMaintenanceScheduleOutputReference",
    "MemcacheInstanceMemcacheNodes",
    "MemcacheInstanceMemcacheNodesList",
    "MemcacheInstanceMemcacheNodesOutputReference",
    "MemcacheInstanceMemcacheParameters",
    "MemcacheInstanceMemcacheParametersOutputReference",
    "MemcacheInstanceNodeConfig",
    "MemcacheInstanceNodeConfigOutputReference",
    "MemcacheInstanceTimeouts",
    "MemcacheInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__79e48e7d09ccd276fccb92df55e8a82b931e29b13f9ac7df4d2b1d8c8f48e1fd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    node_config: typing.Union[MemcacheInstanceNodeConfig, typing.Dict[builtins.str, typing.Any]],
    node_count: jsii.Number,
    authorized_network: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_policy: typing.Optional[typing.Union[MemcacheInstanceMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    memcache_parameters: typing.Optional[typing.Union[MemcacheInstanceMemcacheParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    memcache_version: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reserved_ip_range_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MemcacheInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9bdc31240e4e785ea35c88e23d23bcbe788d7b713ad9440e32d9511ca9ff97(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1aa83fe4d151cd0c097df20e124d6772f012f1cec65ac5fbc8071af1943c1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17def6254c05212f27493b02521d101099fdedf66d48034a3c9fbc7b4f8c515(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ea69da1c434bd81dfa1d2944c006fdad578b550ff45938ad214a77650f779c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7128567bcb4fc080cf8d013855fa20f288606c760bd44e2606c3fdacf19ff276(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e8e136d880c18a19a4a81a25a7f3eadac4f8db161f390f7944e859b8b63f80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10f9891cf5a1364880121094db1f2a457e5c724c46eee919f02ea9c9cd5a1af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29aad7564600209b9a4b7655474b0a846f55c4da7f0d8ea32d4ba83012bca3bd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7500736ed16e00cd835612079da9e8d4e0acc1a0e5580fc763cad1772f032bc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbe9af554f147ba2a61f58e4617b23f717485f38833a70c7292153f5be25f3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4598cb878840915d4288137f25b11a6f6c14b9a0ddbd76c3f6dbf497190b5111(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2f72fe8fe65b9d6b1125a6b7a7cb80a25c956bb4a863315ad94e2a56064b98(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e2394a8c875d0a810911088908fece46dc0e7cfac2654d2e797dae82d92965(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    node_config: typing.Union[MemcacheInstanceNodeConfig, typing.Dict[builtins.str, typing.Any]],
    node_count: jsii.Number,
    authorized_network: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_policy: typing.Optional[typing.Union[MemcacheInstanceMaintenancePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    memcache_parameters: typing.Optional[typing.Union[MemcacheInstanceMemcacheParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    memcache_version: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reserved_ip_range_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MemcacheInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d8f02d23b2d0758077a1fdddb4ff96818b89d3843462fb860354ffe85b771d(
    *,
    weekly_maintenance_window: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d7903a4ab9dacdcd1ddb2b8e48e6fac20cbf4e68317c52f8e4929dfa75b8f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa3e09e446575bb213d13ac1a047485d646b2b61b0281e91cfed12f25ecc3f1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84df8269d37d624365a4e6720ed1a5c4a535ffec91569c0fbce829e5b68a9dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a3f11a8e3ce604af73eff4d90a97ee27f29ffc90a9a25f86138226f36d092c(
    value: typing.Optional[MemcacheInstanceMaintenancePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a33c721f857dc094f0c26e786b1472ddb3a647894efa102dea099ef53c9187(
    *,
    day: builtins.str,
    duration: builtins.str,
    start_time: typing.Union[MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519486328a1ed1ba79650e4a5d678d3816878d0b973ee994072facc0c72e5a4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879a044dd1f79d2b03fa50ae15e90dbfda2bd7c2d808fa892c11cf36f5582cbe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e449621a0e43fda74217c5c87b7e6274428873b0fdbbf37c5c54f51d4c7fdb2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ba2f48ce6475fa60c644904743f05a134f9298c6a7f4739df15621eae2ed76(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93cd25c155828bf87aed38df664a2538444b777df8e1e2523cdfd74f864ebba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ae87a4611e4f316c37bd43614aea311fb1c8f5833d29b4edacb51f75752523(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282b2d58a082693166870f03efbd5ea151e7c8758a39641b713ade6e05271621(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16aa9acc722d7914b6b664d0ba7a3c28e914f07f254ae6bd38d7fd80d007ba24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5781bea76d97ce7a4d477d4baed15a80c7901e58eb55381a370a414bf2e2b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746ea88bae585d5dfc31639f154dcdd6f0dfa74ed5cf9e251d9ed2319b949913(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindow]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96410136183ef85e97b06bc7036d5cac035d80660fe6dca8d5875d35d304159b(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b5495841d62aff534ea296bad77d9115274d5ef9cffb23dac7cbf9eeb305e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12dc93424a7a89cd5a734a9f4f261874e35e3739e01690a4bff20a0dbaacc7af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7743d9ca6dee4e1b94ecdbfd9452c9d0c239b70e68066e4af4a2f462c4fa8f4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92172f29653d9ca039b42a3ce434e5ef6f9d42fda4dbae6b17ea2ca88be855f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d26dd347f11ee00b63d3324a1853edbd5d9611e11af062d53480b3d728fe27c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ac9e35b6a2a48e8731ff5dd54dc006f41da3160834312e557becf2f16aaeb7(
    value: typing.Optional[MemcacheInstanceMaintenancePolicyWeeklyMaintenanceWindowStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6b91b4faa560dca4fb12632fcae4eab1c2ba6e5bdfece3b6fb97ef2d103869(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f42e8e43a6b1155a0b5d2966bdf69d2e9cd45a272cca65472bf6fba7165534(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81a94558c6cb4bc200e724a035b089bf129fd8fe23f6a434f2247529600643f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7338c42c1e52e8444e888258804c26cd831ef83d0b427771581470a01793777(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf57e5e2691389b850dc9034d633e9780289b7282b2c3f7aaad542da462b3f0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5707d12eb02a43a17a8031597de34f2cd09d924ae7a4e9a262c4c401ba42aa24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c90614e39d50e418f7ce9685d96a2754044aa79697037f1613b2f6f1b7090a8(
    value: typing.Optional[MemcacheInstanceMaintenanceSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c32dff20f45f7a155b122ebd585771aea00da3da963cac50ab7ad367dda0203(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5d11405d060c8af47afdef05101b0eae61a7ca3857e933dc6f68395f060f9a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cbf2091156d3e312576888b2f79989cbd53995fc5f70bd806237d0111117189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063dffa42d2d526e6c76c60e15726f8525f153da67522e3f4b0dee7bae616cae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76738ae0d74a57d935b1a813837ba685eaa4d6f793971e6f92c5f7b7f10897a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d3b71e582b648c89314895604da06a148a8a05f8206a30d8447c35cf02497c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76dae47dac582da92758e09210d8f52b82d24270bf63adb3bd9e270f1f7090b4(
    value: typing.Optional[MemcacheInstanceMemcacheNodes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df79ba568c61bf29fe2dddde911c85ea241d6d9daa4adfca448de4283f269720(
    *,
    params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe084e2476dfa4d77966cfda503dc1ede2b632143afc123fa9cdafed1aa5b9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce9987ee08a66f15aceb43da329f61f88490d1738150bce453109fcdfe759b9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680b1ef863eae4a6acd51f29d148514fb19fcbde62f54b020a3cec20e5941fe2(
    value: typing.Optional[MemcacheInstanceMemcacheParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109ea1cdefa96b338da7779608f9f9fbb937aa18d3d5c0a9464950444a50b210(
    *,
    cpu_count: jsii.Number,
    memory_size_mb: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123d360ecd61340172670002a3f86cc4bef2e4a374c785c7bcd3ef2a57a80368(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f3964dd51a5c445d31f765115e965c30b528cc70e5f74ed10d4e4fa899bac0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b1d61a03bc2eadffdca3afb1bb6c4db2b14b8ff9cdf41e6c882cbf937b0293(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e8c1f9d25dd1f1656638f22b617d891bde9bdf4258b0a81dfb2a1170c4324e(
    value: typing.Optional[MemcacheInstanceNodeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e25a192ec66e1fb241d59e18e072bdddf9dfbc552daba09032bbb605038593(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d322a14e38699a399b9d6d0f3bac50c1b19d5c8c55e261664818e8600aa086f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0f0168f7a9d91cd108fbd259aa8fb7b32a9b7eb5673c5b109818fd392f3f9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348c3cb870df52186fc4da197449975fbb12cbdc0501f3bc7c5e106316283b4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b491d5ab687f372910d86055727c8b0c5ce2a34185bcc2de7962a6a12f3a6b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6def35c1d1fb2269d14c40535f59eb9da164a1a5f3e2a49237e6ef030cbef959(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MemcacheInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
