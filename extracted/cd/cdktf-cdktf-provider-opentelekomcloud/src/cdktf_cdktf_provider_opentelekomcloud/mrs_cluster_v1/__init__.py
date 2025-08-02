r'''
# `opentelekomcloud_mrs_cluster_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_mrs_cluster_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1).
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


class MrsClusterV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1 opentelekomcloud_mrs_cluster_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        available_zone_id: builtins.str,
        billing_type: jsii.Number,
        cluster_name: builtins.str,
        cluster_version: builtins.str,
        component_list: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MrsClusterV1ComponentListStruct", typing.Dict[builtins.str, typing.Any]]]],
        core_node_num: jsii.Number,
        core_node_size: builtins.str,
        master_node_num: jsii.Number,
        master_node_size: builtins.str,
        node_public_cert_name: builtins.str,
        safe_mode: jsii.Number,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        add_jobs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MrsClusterV1AddJobs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        bootstrap_scripts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MrsClusterV1BootstrapScripts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster_admin_secret: typing.Optional[builtins.str] = None,
        cluster_type: typing.Optional[jsii.Number] = None,
        core_data_volume_count: typing.Optional[jsii.Number] = None,
        core_data_volume_size: typing.Optional[jsii.Number] = None,
        core_data_volume_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_collection: typing.Optional[jsii.Number] = None,
        master_data_volume_count: typing.Optional[jsii.Number] = None,
        master_data_volume_size: typing.Optional[jsii.Number] = None,
        master_data_volume_type: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MrsClusterV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1 opentelekomcloud_mrs_cluster_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param available_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#available_zone_id MrsClusterV1#available_zone_id}.
        :param billing_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#billing_type MrsClusterV1#billing_type}.
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#cluster_name MrsClusterV1#cluster_name}.
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#cluster_version MrsClusterV1#cluster_version}.
        :param component_list: component_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#component_list MrsClusterV1#component_list}
        :param core_node_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_node_num MrsClusterV1#core_node_num}.
        :param core_node_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_node_size MrsClusterV1#core_node_size}.
        :param master_node_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_node_num MrsClusterV1#master_node_num}.
        :param master_node_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_node_size MrsClusterV1#master_node_size}.
        :param node_public_cert_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#node_public_cert_name MrsClusterV1#node_public_cert_name}.
        :param safe_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#safe_mode MrsClusterV1#safe_mode}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#subnet_id MrsClusterV1#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#vpc_id MrsClusterV1#vpc_id}.
        :param add_jobs: add_jobs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#add_jobs MrsClusterV1#add_jobs}
        :param bootstrap_scripts: bootstrap_scripts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#bootstrap_scripts MrsClusterV1#bootstrap_scripts}
        :param cluster_admin_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#cluster_admin_secret MrsClusterV1#cluster_admin_secret}.
        :param cluster_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#cluster_type MrsClusterV1#cluster_type}.
        :param core_data_volume_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_data_volume_count MrsClusterV1#core_data_volume_count}.
        :param core_data_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_data_volume_size MrsClusterV1#core_data_volume_size}.
        :param core_data_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_data_volume_type MrsClusterV1#core_data_volume_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#id MrsClusterV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_collection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#log_collection MrsClusterV1#log_collection}.
        :param master_data_volume_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_data_volume_count MrsClusterV1#master_data_volume_count}.
        :param master_data_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_data_volume_size MrsClusterV1#master_data_volume_size}.
        :param master_data_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_data_volume_type MrsClusterV1#master_data_volume_type}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#region MrsClusterV1#region}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#tags MrsClusterV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#timeouts MrsClusterV1#timeouts}
        :param volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#volume_size MrsClusterV1#volume_size}.
        :param volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#volume_type MrsClusterV1#volume_type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4cf5b9a71acca554b63b84bf153eeb88002e1e4ba5b6c3c5cb1935b7991d8a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MrsClusterV1Config(
            available_zone_id=available_zone_id,
            billing_type=billing_type,
            cluster_name=cluster_name,
            cluster_version=cluster_version,
            component_list=component_list,
            core_node_num=core_node_num,
            core_node_size=core_node_size,
            master_node_num=master_node_num,
            master_node_size=master_node_size,
            node_public_cert_name=node_public_cert_name,
            safe_mode=safe_mode,
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            add_jobs=add_jobs,
            bootstrap_scripts=bootstrap_scripts,
            cluster_admin_secret=cluster_admin_secret,
            cluster_type=cluster_type,
            core_data_volume_count=core_data_volume_count,
            core_data_volume_size=core_data_volume_size,
            core_data_volume_type=core_data_volume_type,
            id=id,
            log_collection=log_collection,
            master_data_volume_count=master_data_volume_count,
            master_data_volume_size=master_data_volume_size,
            master_data_volume_type=master_data_volume_type,
            region=region,
            tags=tags,
            timeouts=timeouts,
            volume_size=volume_size,
            volume_type=volume_type,
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
        '''Generates CDKTF code for importing a MrsClusterV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MrsClusterV1 to import.
        :param import_from_id: The id of the existing MrsClusterV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MrsClusterV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6970b1d223650a8239252f811b8b4a6b442d6e357c9567ba0f5de2979ba14016)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAddJobs")
    def put_add_jobs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MrsClusterV1AddJobs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1555129de50ad741fbe0d0991c895c88dd65a78ccf7cb8217754ba46e1b7d3e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAddJobs", [value]))

    @jsii.member(jsii_name="putBootstrapScripts")
    def put_bootstrap_scripts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MrsClusterV1BootstrapScripts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e817d8be74934d9c5ad2d6b93f4cbbb5c00edd5bc90c4c7869ababacc86b6e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBootstrapScripts", [value]))

    @jsii.member(jsii_name="putComponentList")
    def put_component_list(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MrsClusterV1ComponentListStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3828f6a085aae462072a5567bb7cd0e4c09ab8076a1781a42ae5f3ea845ad25a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putComponentList", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#create MrsClusterV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#delete MrsClusterV1#delete}.
        '''
        value = MrsClusterV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAddJobs")
    def reset_add_jobs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddJobs", []))

    @jsii.member(jsii_name="resetBootstrapScripts")
    def reset_bootstrap_scripts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootstrapScripts", []))

    @jsii.member(jsii_name="resetClusterAdminSecret")
    def reset_cluster_admin_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterAdminSecret", []))

    @jsii.member(jsii_name="resetClusterType")
    def reset_cluster_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterType", []))

    @jsii.member(jsii_name="resetCoreDataVolumeCount")
    def reset_core_data_volume_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoreDataVolumeCount", []))

    @jsii.member(jsii_name="resetCoreDataVolumeSize")
    def reset_core_data_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoreDataVolumeSize", []))

    @jsii.member(jsii_name="resetCoreDataVolumeType")
    def reset_core_data_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoreDataVolumeType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogCollection")
    def reset_log_collection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogCollection", []))

    @jsii.member(jsii_name="resetMasterDataVolumeCount")
    def reset_master_data_volume_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterDataVolumeCount", []))

    @jsii.member(jsii_name="resetMasterDataVolumeSize")
    def reset_master_data_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterDataVolumeSize", []))

    @jsii.member(jsii_name="resetMasterDataVolumeType")
    def reset_master_data_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterDataVolumeType", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVolumeSize")
    def reset_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeSize", []))

    @jsii.member(jsii_name="resetVolumeType")
    def reset_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeType", []))

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
    @jsii.member(jsii_name="addJobs")
    def add_jobs(self) -> "MrsClusterV1AddJobsList":
        return typing.cast("MrsClusterV1AddJobsList", jsii.get(self, "addJobs"))

    @builtins.property
    @jsii.member(jsii_name="availableZoneName")
    def available_zone_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availableZoneName"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapScripts")
    def bootstrap_scripts(self) -> "MrsClusterV1BootstrapScriptsList":
        return typing.cast("MrsClusterV1BootstrapScriptsList", jsii.get(self, "bootstrapScripts"))

    @builtins.property
    @jsii.member(jsii_name="chargingStartTime")
    def charging_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chargingStartTime"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @builtins.property
    @jsii.member(jsii_name="clusterState")
    def cluster_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterState"))

    @builtins.property
    @jsii.member(jsii_name="componentList")
    def component_list(self) -> "MrsClusterV1ComponentListStructList":
        return typing.cast("MrsClusterV1ComponentListStructList", jsii.get(self, "componentList"))

    @builtins.property
    @jsii.member(jsii_name="coreNodeProductId")
    def core_node_product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coreNodeProductId"))

    @builtins.property
    @jsii.member(jsii_name="coreNodeSpecId")
    def core_node_spec_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coreNodeSpecId"))

    @builtins.property
    @jsii.member(jsii_name="createAt")
    def create_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createAt"))

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentId"))

    @builtins.property
    @jsii.member(jsii_name="errorInfo")
    def error_info(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorInfo"))

    @builtins.property
    @jsii.member(jsii_name="externalAlternateIp")
    def external_alternate_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalAlternateIp"))

    @builtins.property
    @jsii.member(jsii_name="externalIp")
    def external_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalIp"))

    @builtins.property
    @jsii.member(jsii_name="fee")
    def fee(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fee"))

    @builtins.property
    @jsii.member(jsii_name="hadoopVersion")
    def hadoop_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hadoopVersion"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="internalIp")
    def internal_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "internalIp"))

    @builtins.property
    @jsii.member(jsii_name="masterNodeIp")
    def master_node_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterNodeIp"))

    @builtins.property
    @jsii.member(jsii_name="masterNodeProductId")
    def master_node_product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterNodeProductId"))

    @builtins.property
    @jsii.member(jsii_name="masterNodeSpecId")
    def master_node_spec_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterNodeSpecId"))

    @builtins.property
    @jsii.member(jsii_name="orderId")
    def order_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orderId"))

    @builtins.property
    @jsii.member(jsii_name="privateIpFirst")
    def private_ip_first(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIpFirst"))

    @builtins.property
    @jsii.member(jsii_name="remark")
    def remark(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remark"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsId")
    def security_groups_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupsId"))

    @builtins.property
    @jsii.member(jsii_name="slaveSecurityGroupsId")
    def slave_security_groups_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slaveSecurityGroupsId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MrsClusterV1TimeoutsOutputReference":
        return typing.cast("MrsClusterV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateAt")
    def update_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateAt"))

    @builtins.property
    @jsii.member(jsii_name="vnc")
    def vnc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vnc"))

    @builtins.property
    @jsii.member(jsii_name="addJobsInput")
    def add_jobs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MrsClusterV1AddJobs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MrsClusterV1AddJobs"]]], jsii.get(self, "addJobsInput"))

    @builtins.property
    @jsii.member(jsii_name="availableZoneIdInput")
    def available_zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availableZoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="billingTypeInput")
    def billing_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "billingTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapScriptsInput")
    def bootstrap_scripts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MrsClusterV1BootstrapScripts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MrsClusterV1BootstrapScripts"]]], jsii.get(self, "bootstrapScriptsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterAdminSecretInput")
    def cluster_admin_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterAdminSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterTypeInput")
    def cluster_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clusterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterVersionInput")
    def cluster_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="componentListInput")
    def component_list_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MrsClusterV1ComponentListStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MrsClusterV1ComponentListStruct"]]], jsii.get(self, "componentListInput"))

    @builtins.property
    @jsii.member(jsii_name="coreDataVolumeCountInput")
    def core_data_volume_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coreDataVolumeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="coreDataVolumeSizeInput")
    def core_data_volume_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coreDataVolumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="coreDataVolumeTypeInput")
    def core_data_volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coreDataVolumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="coreNodeNumInput")
    def core_node_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coreNodeNumInput"))

    @builtins.property
    @jsii.member(jsii_name="coreNodeSizeInput")
    def core_node_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coreNodeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logCollectionInput")
    def log_collection_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "logCollectionInput"))

    @builtins.property
    @jsii.member(jsii_name="masterDataVolumeCountInput")
    def master_data_volume_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "masterDataVolumeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="masterDataVolumeSizeInput")
    def master_data_volume_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "masterDataVolumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="masterDataVolumeTypeInput")
    def master_data_volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterDataVolumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="masterNodeNumInput")
    def master_node_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "masterNodeNumInput"))

    @builtins.property
    @jsii.member(jsii_name="masterNodeSizeInput")
    def master_node_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterNodeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePublicCertNameInput")
    def node_public_cert_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodePublicCertNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="safeModeInput")
    def safe_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "safeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MrsClusterV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MrsClusterV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInput")
    def volume_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availableZoneId")
    def available_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availableZoneId"))

    @available_zone_id.setter
    def available_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee07aa87026d8e7e9090fabf5d5d07b84d3ea02a133c0b344bb7399687cf7696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableZoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingType")
    def billing_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "billingType"))

    @billing_type.setter
    def billing_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775561a818523def286d43eaf33456b15170e1c88207d6c148a9a13b7a79b11d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterAdminSecret")
    def cluster_admin_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterAdminSecret"))

    @cluster_admin_secret.setter
    def cluster_admin_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa974db44589a3a1c0b6c947d93f85bf7f69d51e580f4748ce12ceb569d8bb92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterAdminSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7e8649b702885081080fecdfa67ac05389ce0ddff1f39410aae789be6f8817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterType")
    def cluster_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clusterType"))

    @cluster_type.setter
    def cluster_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67289e37706c364a7febdfd11349bec75664801cfbefc427dc79596691e8a8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterVersion")
    def cluster_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterVersion"))

    @cluster_version.setter
    def cluster_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b27e868bffe20efba15c50ad61ad28369d20e596c8c2fe1a9b0f0018f7fdb632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coreDataVolumeCount")
    def core_data_volume_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coreDataVolumeCount"))

    @core_data_volume_count.setter
    def core_data_volume_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e301624c54e33b7e12733844c6a5a1d7aaf2adb5a6a0770e3a005ccb86f5fc55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreDataVolumeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coreDataVolumeSize")
    def core_data_volume_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coreDataVolumeSize"))

    @core_data_volume_size.setter
    def core_data_volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0be86c7eb15a6ca4e4b35249bd80a2f755f05e1ff1029eb53d8a688fe6f2014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreDataVolumeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coreDataVolumeType")
    def core_data_volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coreDataVolumeType"))

    @core_data_volume_type.setter
    def core_data_volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a6e6c86a010a7f3daa840675c1ea415d33b3ba287d20b2b0a09d7fbd7de3743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreDataVolumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coreNodeNum")
    def core_node_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coreNodeNum"))

    @core_node_num.setter
    def core_node_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09be1c4de07dffc1bb46f4029daa26be1862856f70edb585d950b45506bde80d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreNodeNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="coreNodeSize")
    def core_node_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coreNodeSize"))

    @core_node_size.setter
    def core_node_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a553924a7c12f4ee2b6e0c2cb438b6e13bad108fe96fdda685f11e34422c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreNodeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1365ab64b4ae84aa159752b2ce5d8e5651d4623f9f4591f0483bddbd72fa8eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logCollection")
    def log_collection(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "logCollection"))

    @log_collection.setter
    def log_collection(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372a9e285773ee8c7315f67167d5ef65a1903e9d36bc02527b9dfc3762a7152f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logCollection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterDataVolumeCount")
    def master_data_volume_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "masterDataVolumeCount"))

    @master_data_volume_count.setter
    def master_data_volume_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdff16b2109df43418a3369f0bea4e147d6ee0dc82ee166db5177833964cc1c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterDataVolumeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterDataVolumeSize")
    def master_data_volume_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "masterDataVolumeSize"))

    @master_data_volume_size.setter
    def master_data_volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f833c3b10bbc5dbc04e0dece3ee8c8f07ea367c19b68fdc4eb65e5c30a2abc8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterDataVolumeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterDataVolumeType")
    def master_data_volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterDataVolumeType"))

    @master_data_volume_type.setter
    def master_data_volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c965b73b356e02bf31d5532ca57d50cafc3100342349e5584e3a914d7d82bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterDataVolumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterNodeNum")
    def master_node_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "masterNodeNum"))

    @master_node_num.setter
    def master_node_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8361109f748ecb364a40ad083c3961d2d40a4dcefd87881a60fa410fd2ebe03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterNodeNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterNodeSize")
    def master_node_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterNodeSize"))

    @master_node_size.setter
    def master_node_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e739926643822345fa95f249f958cd06f8ab2d2f9688524f1810d5ef0dbbf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterNodeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodePublicCertName")
    def node_public_cert_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodePublicCertName"))

    @node_public_cert_name.setter
    def node_public_cert_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07adf3e1cc552577a4f4b11bbd6a99127ad879d5339b79d0382227bab1ddb46f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodePublicCertName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29df6e99958748b0699e065387924002aff66bd62dc53e13d36940a3ddfe4b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="safeMode")
    def safe_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "safeMode"))

    @safe_mode.setter
    def safe_mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c515c71aeab6d76436e1bc639e0063d6193ecaade474461a85e4a42636bd9463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "safeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c49fc4504aa4a852668b5e191d7d778cf7c9d57dfd6ebdad56339d986469b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5621c320619cfc3cad68c99887ca71c826e0444a12017edccbda9316a215f239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSize")
    def volume_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeSize"))

    @volume_size.setter
    def volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f5d13355409b09576e4aba1cc8306355da4978e454273af76d53a8447562feb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5950612da575ba6d09f98ae057998774142248078d05d93af802ea6b389bb27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68fe745cae291028b1f462bd88cc395aa4de603e01224403e2413680ef61c409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1AddJobs",
    jsii_struct_bases=[],
    name_mapping={
        "jar_path": "jarPath",
        "job_name": "jobName",
        "job_type": "jobType",
        "submit_job_once_cluster_run": "submitJobOnceClusterRun",
        "arguments": "arguments",
        "file_action": "fileAction",
        "hive_script_path": "hiveScriptPath",
        "hql": "hql",
        "input": "input",
        "job_log": "jobLog",
        "output": "output",
        "shutdown_cluster": "shutdownCluster",
    },
)
class MrsClusterV1AddJobs:
    def __init__(
        self,
        *,
        jar_path: builtins.str,
        job_name: builtins.str,
        job_type: jsii.Number,
        submit_job_once_cluster_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        arguments: typing.Optional[builtins.str] = None,
        file_action: typing.Optional[builtins.str] = None,
        hive_script_path: typing.Optional[builtins.str] = None,
        hql: typing.Optional[builtins.str] = None,
        input: typing.Optional[builtins.str] = None,
        job_log: typing.Optional[builtins.str] = None,
        output: typing.Optional[builtins.str] = None,
        shutdown_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param jar_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#jar_path MrsClusterV1#jar_path}.
        :param job_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#job_name MrsClusterV1#job_name}.
        :param job_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#job_type MrsClusterV1#job_type}.
        :param submit_job_once_cluster_run: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#submit_job_once_cluster_run MrsClusterV1#submit_job_once_cluster_run}.
        :param arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#arguments MrsClusterV1#arguments}.
        :param file_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#file_action MrsClusterV1#file_action}.
        :param hive_script_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#hive_script_path MrsClusterV1#hive_script_path}.
        :param hql: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#hql MrsClusterV1#hql}.
        :param input: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#input MrsClusterV1#input}.
        :param job_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#job_log MrsClusterV1#job_log}.
        :param output: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#output MrsClusterV1#output}.
        :param shutdown_cluster: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#shutdown_cluster MrsClusterV1#shutdown_cluster}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeab201972cfbe87f9c41acea37e25148c53915b930b0ebc40ca30aac59f61a6)
            check_type(argname="argument jar_path", value=jar_path, expected_type=type_hints["jar_path"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_type", value=job_type, expected_type=type_hints["job_type"])
            check_type(argname="argument submit_job_once_cluster_run", value=submit_job_once_cluster_run, expected_type=type_hints["submit_job_once_cluster_run"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument file_action", value=file_action, expected_type=type_hints["file_action"])
            check_type(argname="argument hive_script_path", value=hive_script_path, expected_type=type_hints["hive_script_path"])
            check_type(argname="argument hql", value=hql, expected_type=type_hints["hql"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument job_log", value=job_log, expected_type=type_hints["job_log"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            check_type(argname="argument shutdown_cluster", value=shutdown_cluster, expected_type=type_hints["shutdown_cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "jar_path": jar_path,
            "job_name": job_name,
            "job_type": job_type,
            "submit_job_once_cluster_run": submit_job_once_cluster_run,
        }
        if arguments is not None:
            self._values["arguments"] = arguments
        if file_action is not None:
            self._values["file_action"] = file_action
        if hive_script_path is not None:
            self._values["hive_script_path"] = hive_script_path
        if hql is not None:
            self._values["hql"] = hql
        if input is not None:
            self._values["input"] = input
        if job_log is not None:
            self._values["job_log"] = job_log
        if output is not None:
            self._values["output"] = output
        if shutdown_cluster is not None:
            self._values["shutdown_cluster"] = shutdown_cluster

    @builtins.property
    def jar_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#jar_path MrsClusterV1#jar_path}.'''
        result = self._values.get("jar_path")
        assert result is not None, "Required property 'jar_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#job_name MrsClusterV1#job_name}.'''
        result = self._values.get("job_name")
        assert result is not None, "Required property 'job_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def job_type(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#job_type MrsClusterV1#job_type}.'''
        result = self._values.get("job_type")
        assert result is not None, "Required property 'job_type' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def submit_job_once_cluster_run(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#submit_job_once_cluster_run MrsClusterV1#submit_job_once_cluster_run}.'''
        result = self._values.get("submit_job_once_cluster_run")
        assert result is not None, "Required property 'submit_job_once_cluster_run' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def arguments(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#arguments MrsClusterV1#arguments}.'''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#file_action MrsClusterV1#file_action}.'''
        result = self._values.get("file_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hive_script_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#hive_script_path MrsClusterV1#hive_script_path}.'''
        result = self._values.get("hive_script_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hql(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#hql MrsClusterV1#hql}.'''
        result = self._values.get("hql")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#input MrsClusterV1#input}.'''
        result = self._values.get("input")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_log(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#job_log MrsClusterV1#job_log}.'''
        result = self._values.get("job_log")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#output MrsClusterV1#output}.'''
        result = self._values.get("output")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shutdown_cluster(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#shutdown_cluster MrsClusterV1#shutdown_cluster}.'''
        result = self._values.get("shutdown_cluster")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MrsClusterV1AddJobs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MrsClusterV1AddJobsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1AddJobsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41230fc87e2b4fa0741c88209fbb26ac441b8a68858fe0f3914f1ea9b9ee73eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MrsClusterV1AddJobsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dbebdcf1fb2c98d4fd73896c10b78b8841ec6c5269a33a3511312ef12b6f3e2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MrsClusterV1AddJobsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d709ea1b1f5e957aab1f570114f9769128f930e84a8226c292f6db1f4da641c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bde02eefe8809548883a5a0985363ecdabf25168e5d44b96bbd06d51ea29334)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea869ff65b7570492dacd0e8bad8bd00d157b85d9f8ff4d1df15ddef2fcda256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1AddJobs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1AddJobs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1AddJobs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a205c63087273e38638566869d1f352ff794b55c8aa21a6e834294a0b044aeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MrsClusterV1AddJobsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1AddJobsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e7edda94b70dc9b48709414cfbc83eab9b33c28a097f63b0b3b7c719831b1c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetArguments")
    def reset_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArguments", []))

    @jsii.member(jsii_name="resetFileAction")
    def reset_file_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileAction", []))

    @jsii.member(jsii_name="resetHiveScriptPath")
    def reset_hive_script_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHiveScriptPath", []))

    @jsii.member(jsii_name="resetHql")
    def reset_hql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHql", []))

    @jsii.member(jsii_name="resetInput")
    def reset_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInput", []))

    @jsii.member(jsii_name="resetJobLog")
    def reset_job_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobLog", []))

    @jsii.member(jsii_name="resetOutput")
    def reset_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutput", []))

    @jsii.member(jsii_name="resetShutdownCluster")
    def reset_shutdown_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShutdownCluster", []))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "argumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileActionInput")
    def file_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileActionInput"))

    @builtins.property
    @jsii.member(jsii_name="hiveScriptPathInput")
    def hive_script_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hiveScriptPathInput"))

    @builtins.property
    @jsii.member(jsii_name="hqlInput")
    def hql_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hqlInput"))

    @builtins.property
    @jsii.member(jsii_name="inputInput")
    def input_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputInput"))

    @builtins.property
    @jsii.member(jsii_name="jarPathInput")
    def jar_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jarPathInput"))

    @builtins.property
    @jsii.member(jsii_name="jobLogInput")
    def job_log_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobLogInput"))

    @builtins.property
    @jsii.member(jsii_name="jobNameInput")
    def job_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobNameInput"))

    @builtins.property
    @jsii.member(jsii_name="jobTypeInput")
    def job_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "jobTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="outputInput")
    def output_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputInput"))

    @builtins.property
    @jsii.member(jsii_name="shutdownClusterInput")
    def shutdown_cluster_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "shutdownClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="submitJobOnceClusterRunInput")
    def submit_job_once_cluster_run_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "submitJobOnceClusterRunInput"))

    @builtins.property
    @jsii.member(jsii_name="arguments")
    def arguments(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arguments"))

    @arguments.setter
    def arguments(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef21f7327c0d996c5417e1332e9592fca1499694fd2ccd0241b6e2de714f73dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arguments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileAction")
    def file_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileAction"))

    @file_action.setter
    def file_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b1ee2876cd360c5fbce0fdc3add39f0275d6fcd2f07769ae0b2bdfd4bf16d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hiveScriptPath")
    def hive_script_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hiveScriptPath"))

    @hive_script_path.setter
    def hive_script_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__093d0486a468458af825b8f0d2a092df4f3a074d1288b1191d1b48a35c624fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hiveScriptPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hql")
    def hql(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hql"))

    @hql.setter
    def hql(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c56680ed0aca9acf8d71eeaac7c165a9cd8c368cb3695f4a4b6a2b2bddcc780b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hql", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="input")
    def input(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "input"))

    @input.setter
    def input(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ba4a4eca5f29b85b2ca4b5b26366b55a6e92e0ce05120f49a66a6bc24bf13e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "input", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarPath")
    def jar_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jarPath"))

    @jar_path.setter
    def jar_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50aa8240c5f87fdf63b9a60f134695667252b86e1fe3fa96488e616bd3f2af74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobLog")
    def job_log(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobLog"))

    @job_log.setter
    def job_log(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14439309adbe238fe30734c613d433d3f4d84c134be6af3c4635e1698644daf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobLog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @job_name.setter
    def job_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630d8f24d91ec1e4dd61f9f18626667fa7e3c375ddb73bae9cb1cac2c9793de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobType")
    def job_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "jobType"))

    @job_type.setter
    def job_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__484887e1305b3a724448ce986fad5e81b92e3133f06046601458173cc876c078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="output")
    def output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "output"))

    @output.setter
    def output(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__977c92811b64791b0280ab5853997d372ad7b3b608f85f0a90fa312a7bd3b744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "output", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shutdownCluster")
    def shutdown_cluster(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "shutdownCluster"))

    @shutdown_cluster.setter
    def shutdown_cluster(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df7a3ee493c6050ec7c86b462beecf98b1601eb2c4717f383774a148d20553e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shutdownCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="submitJobOnceClusterRun")
    def submit_job_once_cluster_run(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "submitJobOnceClusterRun"))

    @submit_job_once_cluster_run.setter
    def submit_job_once_cluster_run(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce7a41c150bb1d6b843287748c4ef52bfde382261769d4350a457f12b8adf61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "submitJobOnceClusterRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1AddJobs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1AddJobs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1AddJobs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e54e59a2cd47143b90ddf4f2602db3c6d0f5c8f88b7d4ff4d99d40efb2c401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1BootstrapScripts",
    jsii_struct_bases=[],
    name_mapping={
        "fail_action": "failAction",
        "name": "name",
        "nodes": "nodes",
        "uri": "uri",
        "active_master": "activeMaster",
        "before_component_start": "beforeComponentStart",
        "parameters": "parameters",
    },
)
class MrsClusterV1BootstrapScripts:
    def __init__(
        self,
        *,
        fail_action: builtins.str,
        name: builtins.str,
        nodes: typing.Sequence[builtins.str],
        uri: builtins.str,
        active_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        before_component_start: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        parameters: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fail_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#fail_action MrsClusterV1#fail_action}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#name MrsClusterV1#name}.
        :param nodes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#nodes MrsClusterV1#nodes}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#uri MrsClusterV1#uri}.
        :param active_master: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#active_master MrsClusterV1#active_master}.
        :param before_component_start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#before_component_start MrsClusterV1#before_component_start}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#parameters MrsClusterV1#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5adeac6b80ae85a20793e28376b81064244966a3b56c93d50540647850d158fa)
            check_type(argname="argument fail_action", value=fail_action, expected_type=type_hints["fail_action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument nodes", value=nodes, expected_type=type_hints["nodes"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument active_master", value=active_master, expected_type=type_hints["active_master"])
            check_type(argname="argument before_component_start", value=before_component_start, expected_type=type_hints["before_component_start"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fail_action": fail_action,
            "name": name,
            "nodes": nodes,
            "uri": uri,
        }
        if active_master is not None:
            self._values["active_master"] = active_master
        if before_component_start is not None:
            self._values["before_component_start"] = before_component_start
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def fail_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#fail_action MrsClusterV1#fail_action}.'''
        result = self._values.get("fail_action")
        assert result is not None, "Required property 'fail_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#name MrsClusterV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nodes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#nodes MrsClusterV1#nodes}.'''
        result = self._values.get("nodes")
        assert result is not None, "Required property 'nodes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#uri MrsClusterV1#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active_master(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#active_master MrsClusterV1#active_master}.'''
        result = self._values.get("active_master")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def before_component_start(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#before_component_start MrsClusterV1#before_component_start}.'''
        result = self._values.get("before_component_start")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#parameters MrsClusterV1#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MrsClusterV1BootstrapScripts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MrsClusterV1BootstrapScriptsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1BootstrapScriptsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f81d8be4002653d4935d1d711d9dadc138dfb1763dcdd44b4d382fab119484b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MrsClusterV1BootstrapScriptsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eed72ebf523f5dbd79e9243d5c6e6295bf8c2eaa53ac4ed8982baf203719598)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MrsClusterV1BootstrapScriptsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70aade2036d97ae915a6ba0be159e753c6fb801e40e4fb60b735d567b1ddf100)
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
            type_hints = typing.get_type_hints(_typecheckingstub__314fdc5cd2996eea80018dae2a76908462dd0a0d64989fa2f0e586769cb17693)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51736ae159228a17ae1620fd8a60c28a217fe88426571f5687d35485a723695c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1BootstrapScripts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1BootstrapScripts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1BootstrapScripts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3107475520931c3573c157d758634c6f48458e6902f2651ce5998322e8d3b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MrsClusterV1BootstrapScriptsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1BootstrapScriptsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d11d57402176a7b29a47e980b442b3f6412eb2eaeb355ce9cf77d65a7c10af3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetActiveMaster")
    def reset_active_master(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveMaster", []))

    @jsii.member(jsii_name="resetBeforeComponentStart")
    def reset_before_component_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBeforeComponentStart", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="activeMasterInput")
    def active_master_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "activeMasterInput"))

    @builtins.property
    @jsii.member(jsii_name="beforeComponentStartInput")
    def before_component_start_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "beforeComponentStartInput"))

    @builtins.property
    @jsii.member(jsii_name="failActionInput")
    def fail_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failActionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodesInput")
    def nodes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nodesInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="activeMaster")
    def active_master(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "activeMaster"))

    @active_master.setter
    def active_master(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fbd77e7a7dc18432e707394e68542358363b4198ceba736c6dff8a42f7744d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeMaster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="beforeComponentStart")
    def before_component_start(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "beforeComponentStart"))

    @before_component_start.setter
    def before_component_start(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a1da23588b228c5e9640fab18515fe2700f07878a261f347297195b3992fcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "beforeComponentStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failAction")
    def fail_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failAction"))

    @fail_action.setter
    def fail_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88011e9f0952810deffd9ea3b6d50d6200bff5d2a938693f5148dde3af3bf618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee8bff7c1dca22464e85f27d5dcb79631c03f0d8b0f0d5252453a406c06d484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nodes"))

    @nodes.setter
    def nodes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f06d139cba75ad22c95a3bf2e7d36a1e6151d8f104eb3d0e60a0a4857b5943e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a518b6d94e9f1400904a22875c2dd1c6f1a38a19388af85b1d10983b761f11bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5f9db2b39693b5412f514a5d4edd2352dbde4702553c4666e8d95b9fffcdd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1BootstrapScripts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1BootstrapScripts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1BootstrapScripts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2effcd90558d611d5972f4947ad107f24444321666ad582d5f54849d457c805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1ComponentListStruct",
    jsii_struct_bases=[],
    name_mapping={"component_name": "componentName"},
)
class MrsClusterV1ComponentListStruct:
    def __init__(self, *, component_name: builtins.str) -> None:
        '''
        :param component_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#component_name MrsClusterV1#component_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8083d53c5c7e565a2fa9b4fe30c349e18de3405056b526a12a743424344ee312)
            check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "component_name": component_name,
        }

    @builtins.property
    def component_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#component_name MrsClusterV1#component_name}.'''
        result = self._values.get("component_name")
        assert result is not None, "Required property 'component_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MrsClusterV1ComponentListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MrsClusterV1ComponentListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1ComponentListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f15d3b95cdb0d809693aefe1dc76a57f4fe717f6ce7f2484f612f734c5c96b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MrsClusterV1ComponentListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49f1df27041eeac218c03e734370665db1e1d78fe411bf39ee0885c88b34d06)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MrsClusterV1ComponentListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26a715031da90b6d375169dc30d158c9582f62b4a17aedb64fe11a212b29e56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b4f2ac25ac571c14b223fed45555a4b1041f3dc48a3b5c7961a1feae379d1d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad50185401665ce2707ca0bb2709d42cc8a1389cf091dc57c418fccaab1cb70a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1ComponentListStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1ComponentListStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1ComponentListStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc80fe8581dcd33ddb1495269b5c87b287e5acf16c060fd017228cf65526d616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MrsClusterV1ComponentListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1ComponentListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c791c7847ff302d55396586d69723932609451124090d681ab3d5ef4c1d3a3ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="componentDesc")
    def component_desc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "componentDesc"))

    @builtins.property
    @jsii.member(jsii_name="componentId")
    def component_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "componentId"))

    @builtins.property
    @jsii.member(jsii_name="componentVersion")
    def component_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "componentVersion"))

    @builtins.property
    @jsii.member(jsii_name="componentNameInput")
    def component_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "componentNameInput"))

    @builtins.property
    @jsii.member(jsii_name="componentName")
    def component_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "componentName"))

    @component_name.setter
    def component_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208c03d559348c20276afe2a40302808b960bfdbeb63f91847d16401be84fd3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1ComponentListStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1ComponentListStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1ComponentListStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb7a91b173a57d3f3d9a07485eee372af05b67be31bab69261561f82729a1edc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "available_zone_id": "availableZoneId",
        "billing_type": "billingType",
        "cluster_name": "clusterName",
        "cluster_version": "clusterVersion",
        "component_list": "componentList",
        "core_node_num": "coreNodeNum",
        "core_node_size": "coreNodeSize",
        "master_node_num": "masterNodeNum",
        "master_node_size": "masterNodeSize",
        "node_public_cert_name": "nodePublicCertName",
        "safe_mode": "safeMode",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
        "add_jobs": "addJobs",
        "bootstrap_scripts": "bootstrapScripts",
        "cluster_admin_secret": "clusterAdminSecret",
        "cluster_type": "clusterType",
        "core_data_volume_count": "coreDataVolumeCount",
        "core_data_volume_size": "coreDataVolumeSize",
        "core_data_volume_type": "coreDataVolumeType",
        "id": "id",
        "log_collection": "logCollection",
        "master_data_volume_count": "masterDataVolumeCount",
        "master_data_volume_size": "masterDataVolumeSize",
        "master_data_volume_type": "masterDataVolumeType",
        "region": "region",
        "tags": "tags",
        "timeouts": "timeouts",
        "volume_size": "volumeSize",
        "volume_type": "volumeType",
    },
)
class MrsClusterV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        available_zone_id: builtins.str,
        billing_type: jsii.Number,
        cluster_name: builtins.str,
        cluster_version: builtins.str,
        component_list: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MrsClusterV1ComponentListStruct, typing.Dict[builtins.str, typing.Any]]]],
        core_node_num: jsii.Number,
        core_node_size: builtins.str,
        master_node_num: jsii.Number,
        master_node_size: builtins.str,
        node_public_cert_name: builtins.str,
        safe_mode: jsii.Number,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        add_jobs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MrsClusterV1AddJobs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        bootstrap_scripts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MrsClusterV1BootstrapScripts, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster_admin_secret: typing.Optional[builtins.str] = None,
        cluster_type: typing.Optional[jsii.Number] = None,
        core_data_volume_count: typing.Optional[jsii.Number] = None,
        core_data_volume_size: typing.Optional[jsii.Number] = None,
        core_data_volume_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_collection: typing.Optional[jsii.Number] = None,
        master_data_volume_count: typing.Optional[jsii.Number] = None,
        master_data_volume_size: typing.Optional[jsii.Number] = None,
        master_data_volume_type: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MrsClusterV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param available_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#available_zone_id MrsClusterV1#available_zone_id}.
        :param billing_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#billing_type MrsClusterV1#billing_type}.
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#cluster_name MrsClusterV1#cluster_name}.
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#cluster_version MrsClusterV1#cluster_version}.
        :param component_list: component_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#component_list MrsClusterV1#component_list}
        :param core_node_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_node_num MrsClusterV1#core_node_num}.
        :param core_node_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_node_size MrsClusterV1#core_node_size}.
        :param master_node_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_node_num MrsClusterV1#master_node_num}.
        :param master_node_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_node_size MrsClusterV1#master_node_size}.
        :param node_public_cert_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#node_public_cert_name MrsClusterV1#node_public_cert_name}.
        :param safe_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#safe_mode MrsClusterV1#safe_mode}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#subnet_id MrsClusterV1#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#vpc_id MrsClusterV1#vpc_id}.
        :param add_jobs: add_jobs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#add_jobs MrsClusterV1#add_jobs}
        :param bootstrap_scripts: bootstrap_scripts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#bootstrap_scripts MrsClusterV1#bootstrap_scripts}
        :param cluster_admin_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#cluster_admin_secret MrsClusterV1#cluster_admin_secret}.
        :param cluster_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#cluster_type MrsClusterV1#cluster_type}.
        :param core_data_volume_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_data_volume_count MrsClusterV1#core_data_volume_count}.
        :param core_data_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_data_volume_size MrsClusterV1#core_data_volume_size}.
        :param core_data_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_data_volume_type MrsClusterV1#core_data_volume_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#id MrsClusterV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_collection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#log_collection MrsClusterV1#log_collection}.
        :param master_data_volume_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_data_volume_count MrsClusterV1#master_data_volume_count}.
        :param master_data_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_data_volume_size MrsClusterV1#master_data_volume_size}.
        :param master_data_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_data_volume_type MrsClusterV1#master_data_volume_type}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#region MrsClusterV1#region}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#tags MrsClusterV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#timeouts MrsClusterV1#timeouts}
        :param volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#volume_size MrsClusterV1#volume_size}.
        :param volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#volume_type MrsClusterV1#volume_type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = MrsClusterV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47df84f0728f96ba2b311bac10a3538cb1f9649f64b6db9b01667b0f49dfca09)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument available_zone_id", value=available_zone_id, expected_type=type_hints["available_zone_id"])
            check_type(argname="argument billing_type", value=billing_type, expected_type=type_hints["billing_type"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument cluster_version", value=cluster_version, expected_type=type_hints["cluster_version"])
            check_type(argname="argument component_list", value=component_list, expected_type=type_hints["component_list"])
            check_type(argname="argument core_node_num", value=core_node_num, expected_type=type_hints["core_node_num"])
            check_type(argname="argument core_node_size", value=core_node_size, expected_type=type_hints["core_node_size"])
            check_type(argname="argument master_node_num", value=master_node_num, expected_type=type_hints["master_node_num"])
            check_type(argname="argument master_node_size", value=master_node_size, expected_type=type_hints["master_node_size"])
            check_type(argname="argument node_public_cert_name", value=node_public_cert_name, expected_type=type_hints["node_public_cert_name"])
            check_type(argname="argument safe_mode", value=safe_mode, expected_type=type_hints["safe_mode"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument add_jobs", value=add_jobs, expected_type=type_hints["add_jobs"])
            check_type(argname="argument bootstrap_scripts", value=bootstrap_scripts, expected_type=type_hints["bootstrap_scripts"])
            check_type(argname="argument cluster_admin_secret", value=cluster_admin_secret, expected_type=type_hints["cluster_admin_secret"])
            check_type(argname="argument cluster_type", value=cluster_type, expected_type=type_hints["cluster_type"])
            check_type(argname="argument core_data_volume_count", value=core_data_volume_count, expected_type=type_hints["core_data_volume_count"])
            check_type(argname="argument core_data_volume_size", value=core_data_volume_size, expected_type=type_hints["core_data_volume_size"])
            check_type(argname="argument core_data_volume_type", value=core_data_volume_type, expected_type=type_hints["core_data_volume_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_collection", value=log_collection, expected_type=type_hints["log_collection"])
            check_type(argname="argument master_data_volume_count", value=master_data_volume_count, expected_type=type_hints["master_data_volume_count"])
            check_type(argname="argument master_data_volume_size", value=master_data_volume_size, expected_type=type_hints["master_data_volume_size"])
            check_type(argname="argument master_data_volume_type", value=master_data_volume_type, expected_type=type_hints["master_data_volume_type"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "available_zone_id": available_zone_id,
            "billing_type": billing_type,
            "cluster_name": cluster_name,
            "cluster_version": cluster_version,
            "component_list": component_list,
            "core_node_num": core_node_num,
            "core_node_size": core_node_size,
            "master_node_num": master_node_num,
            "master_node_size": master_node_size,
            "node_public_cert_name": node_public_cert_name,
            "safe_mode": safe_mode,
            "subnet_id": subnet_id,
            "vpc_id": vpc_id,
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
        if add_jobs is not None:
            self._values["add_jobs"] = add_jobs
        if bootstrap_scripts is not None:
            self._values["bootstrap_scripts"] = bootstrap_scripts
        if cluster_admin_secret is not None:
            self._values["cluster_admin_secret"] = cluster_admin_secret
        if cluster_type is not None:
            self._values["cluster_type"] = cluster_type
        if core_data_volume_count is not None:
            self._values["core_data_volume_count"] = core_data_volume_count
        if core_data_volume_size is not None:
            self._values["core_data_volume_size"] = core_data_volume_size
        if core_data_volume_type is not None:
            self._values["core_data_volume_type"] = core_data_volume_type
        if id is not None:
            self._values["id"] = id
        if log_collection is not None:
            self._values["log_collection"] = log_collection
        if master_data_volume_count is not None:
            self._values["master_data_volume_count"] = master_data_volume_count
        if master_data_volume_size is not None:
            self._values["master_data_volume_size"] = master_data_volume_size
        if master_data_volume_type is not None:
            self._values["master_data_volume_type"] = master_data_volume_type
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if volume_size is not None:
            self._values["volume_size"] = volume_size
        if volume_type is not None:
            self._values["volume_type"] = volume_type

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
    def available_zone_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#available_zone_id MrsClusterV1#available_zone_id}.'''
        result = self._values.get("available_zone_id")
        assert result is not None, "Required property 'available_zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def billing_type(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#billing_type MrsClusterV1#billing_type}.'''
        result = self._values.get("billing_type")
        assert result is not None, "Required property 'billing_type' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def cluster_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#cluster_name MrsClusterV1#cluster_name}.'''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#cluster_version MrsClusterV1#cluster_version}.'''
        result = self._values.get("cluster_version")
        assert result is not None, "Required property 'cluster_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def component_list(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1ComponentListStruct]]:
        '''component_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#component_list MrsClusterV1#component_list}
        '''
        result = self._values.get("component_list")
        assert result is not None, "Required property 'component_list' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1ComponentListStruct]], result)

    @builtins.property
    def core_node_num(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_node_num MrsClusterV1#core_node_num}.'''
        result = self._values.get("core_node_num")
        assert result is not None, "Required property 'core_node_num' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def core_node_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_node_size MrsClusterV1#core_node_size}.'''
        result = self._values.get("core_node_size")
        assert result is not None, "Required property 'core_node_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def master_node_num(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_node_num MrsClusterV1#master_node_num}.'''
        result = self._values.get("master_node_num")
        assert result is not None, "Required property 'master_node_num' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def master_node_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_node_size MrsClusterV1#master_node_size}.'''
        result = self._values.get("master_node_size")
        assert result is not None, "Required property 'master_node_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_public_cert_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#node_public_cert_name MrsClusterV1#node_public_cert_name}.'''
        result = self._values.get("node_public_cert_name")
        assert result is not None, "Required property 'node_public_cert_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def safe_mode(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#safe_mode MrsClusterV1#safe_mode}.'''
        result = self._values.get("safe_mode")
        assert result is not None, "Required property 'safe_mode' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#subnet_id MrsClusterV1#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#vpc_id MrsClusterV1#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def add_jobs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1AddJobs]]]:
        '''add_jobs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#add_jobs MrsClusterV1#add_jobs}
        '''
        result = self._values.get("add_jobs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1AddJobs]]], result)

    @builtins.property
    def bootstrap_scripts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1BootstrapScripts]]]:
        '''bootstrap_scripts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#bootstrap_scripts MrsClusterV1#bootstrap_scripts}
        '''
        result = self._values.get("bootstrap_scripts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1BootstrapScripts]]], result)

    @builtins.property
    def cluster_admin_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#cluster_admin_secret MrsClusterV1#cluster_admin_secret}.'''
        result = self._values.get("cluster_admin_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#cluster_type MrsClusterV1#cluster_type}.'''
        result = self._values.get("cluster_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def core_data_volume_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_data_volume_count MrsClusterV1#core_data_volume_count}.'''
        result = self._values.get("core_data_volume_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def core_data_volume_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_data_volume_size MrsClusterV1#core_data_volume_size}.'''
        result = self._values.get("core_data_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def core_data_volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#core_data_volume_type MrsClusterV1#core_data_volume_type}.'''
        result = self._values.get("core_data_volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#id MrsClusterV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_collection(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#log_collection MrsClusterV1#log_collection}.'''
        result = self._values.get("log_collection")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def master_data_volume_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_data_volume_count MrsClusterV1#master_data_volume_count}.'''
        result = self._values.get("master_data_volume_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def master_data_volume_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_data_volume_size MrsClusterV1#master_data_volume_size}.'''
        result = self._values.get("master_data_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def master_data_volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#master_data_volume_type MrsClusterV1#master_data_volume_type}.'''
        result = self._values.get("master_data_volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#region MrsClusterV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#tags MrsClusterV1#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MrsClusterV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#timeouts MrsClusterV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MrsClusterV1Timeouts"], result)

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#volume_size MrsClusterV1#volume_size}.'''
        result = self._values.get("volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#volume_type MrsClusterV1#volume_type}.'''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MrsClusterV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class MrsClusterV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#create MrsClusterV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#delete MrsClusterV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138cf2bfdcf9c3a8d57158c552e2b73bf45deda4ae8985d9ea3a121364275302)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#create MrsClusterV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/mrs_cluster_v1#delete MrsClusterV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MrsClusterV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MrsClusterV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.mrsClusterV1.MrsClusterV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ce3e2027d680b66224857403b9ddb8aa0f223c8af51eb3b1c38cbab47bf37ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e6e1e41c60a41cd3c0eed4b716c869cef447f0fdf65696273caff63960fedd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3293d5d6de711790a6206584ede356b5ec9fb61c17ae2f674ab228c6da18c30b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306c85971153e408f3bf140a9d8b20c5b7723803ae8441b7fa4a55b451254ec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MrsClusterV1",
    "MrsClusterV1AddJobs",
    "MrsClusterV1AddJobsList",
    "MrsClusterV1AddJobsOutputReference",
    "MrsClusterV1BootstrapScripts",
    "MrsClusterV1BootstrapScriptsList",
    "MrsClusterV1BootstrapScriptsOutputReference",
    "MrsClusterV1ComponentListStruct",
    "MrsClusterV1ComponentListStructList",
    "MrsClusterV1ComponentListStructOutputReference",
    "MrsClusterV1Config",
    "MrsClusterV1Timeouts",
    "MrsClusterV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c4cf5b9a71acca554b63b84bf153eeb88002e1e4ba5b6c3c5cb1935b7991d8a8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    available_zone_id: builtins.str,
    billing_type: jsii.Number,
    cluster_name: builtins.str,
    cluster_version: builtins.str,
    component_list: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MrsClusterV1ComponentListStruct, typing.Dict[builtins.str, typing.Any]]]],
    core_node_num: jsii.Number,
    core_node_size: builtins.str,
    master_node_num: jsii.Number,
    master_node_size: builtins.str,
    node_public_cert_name: builtins.str,
    safe_mode: jsii.Number,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    add_jobs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MrsClusterV1AddJobs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bootstrap_scripts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MrsClusterV1BootstrapScripts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_admin_secret: typing.Optional[builtins.str] = None,
    cluster_type: typing.Optional[jsii.Number] = None,
    core_data_volume_count: typing.Optional[jsii.Number] = None,
    core_data_volume_size: typing.Optional[jsii.Number] = None,
    core_data_volume_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_collection: typing.Optional[jsii.Number] = None,
    master_data_volume_count: typing.Optional[jsii.Number] = None,
    master_data_volume_size: typing.Optional[jsii.Number] = None,
    master_data_volume_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MrsClusterV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__6970b1d223650a8239252f811b8b4a6b442d6e357c9567ba0f5de2979ba14016(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1555129de50ad741fbe0d0991c895c88dd65a78ccf7cb8217754ba46e1b7d3e8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MrsClusterV1AddJobs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e817d8be74934d9c5ad2d6b93f4cbbb5c00edd5bc90c4c7869ababacc86b6e89(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MrsClusterV1BootstrapScripts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3828f6a085aae462072a5567bb7cd0e4c09ab8076a1781a42ae5f3ea845ad25a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MrsClusterV1ComponentListStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee07aa87026d8e7e9090fabf5d5d07b84d3ea02a133c0b344bb7399687cf7696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775561a818523def286d43eaf33456b15170e1c88207d6c148a9a13b7a79b11d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa974db44589a3a1c0b6c947d93f85bf7f69d51e580f4748ce12ceb569d8bb92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7e8649b702885081080fecdfa67ac05389ce0ddff1f39410aae789be6f8817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67289e37706c364a7febdfd11349bec75664801cfbefc427dc79596691e8a8fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27e868bffe20efba15c50ad61ad28369d20e596c8c2fe1a9b0f0018f7fdb632(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e301624c54e33b7e12733844c6a5a1d7aaf2adb5a6a0770e3a005ccb86f5fc55(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0be86c7eb15a6ca4e4b35249bd80a2f755f05e1ff1029eb53d8a688fe6f2014(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6e6c86a010a7f3daa840675c1ea415d33b3ba287d20b2b0a09d7fbd7de3743(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09be1c4de07dffc1bb46f4029daa26be1862856f70edb585d950b45506bde80d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a553924a7c12f4ee2b6e0c2cb438b6e13bad108fe96fdda685f11e34422c3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1365ab64b4ae84aa159752b2ce5d8e5651d4623f9f4591f0483bddbd72fa8eae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372a9e285773ee8c7315f67167d5ef65a1903e9d36bc02527b9dfc3762a7152f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdff16b2109df43418a3369f0bea4e147d6ee0dc82ee166db5177833964cc1c4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f833c3b10bbc5dbc04e0dece3ee8c8f07ea367c19b68fdc4eb65e5c30a2abc8f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c965b73b356e02bf31d5532ca57d50cafc3100342349e5584e3a914d7d82bf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8361109f748ecb364a40ad083c3961d2d40a4dcefd87881a60fa410fd2ebe03(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e739926643822345fa95f249f958cd06f8ab2d2f9688524f1810d5ef0dbbf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07adf3e1cc552577a4f4b11bbd6a99127ad879d5339b79d0382227bab1ddb46f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29df6e99958748b0699e065387924002aff66bd62dc53e13d36940a3ddfe4b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c515c71aeab6d76436e1bc639e0063d6193ecaade474461a85e4a42636bd9463(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c49fc4504aa4a852668b5e191d7d778cf7c9d57dfd6ebdad56339d986469b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5621c320619cfc3cad68c99887ca71c826e0444a12017edccbda9316a215f239(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5d13355409b09576e4aba1cc8306355da4978e454273af76d53a8447562feb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5950612da575ba6d09f98ae057998774142248078d05d93af802ea6b389bb27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68fe745cae291028b1f462bd88cc395aa4de603e01224403e2413680ef61c409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeab201972cfbe87f9c41acea37e25148c53915b930b0ebc40ca30aac59f61a6(
    *,
    jar_path: builtins.str,
    job_name: builtins.str,
    job_type: jsii.Number,
    submit_job_once_cluster_run: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    arguments: typing.Optional[builtins.str] = None,
    file_action: typing.Optional[builtins.str] = None,
    hive_script_path: typing.Optional[builtins.str] = None,
    hql: typing.Optional[builtins.str] = None,
    input: typing.Optional[builtins.str] = None,
    job_log: typing.Optional[builtins.str] = None,
    output: typing.Optional[builtins.str] = None,
    shutdown_cluster: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41230fc87e2b4fa0741c88209fbb26ac441b8a68858fe0f3914f1ea9b9ee73eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dbebdcf1fb2c98d4fd73896c10b78b8841ec6c5269a33a3511312ef12b6f3e2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d709ea1b1f5e957aab1f570114f9769128f930e84a8226c292f6db1f4da641c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bde02eefe8809548883a5a0985363ecdabf25168e5d44b96bbd06d51ea29334(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea869ff65b7570492dacd0e8bad8bd00d157b85d9f8ff4d1df15ddef2fcda256(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a205c63087273e38638566869d1f352ff794b55c8aa21a6e834294a0b044aeb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1AddJobs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7edda94b70dc9b48709414cfbc83eab9b33c28a097f63b0b3b7c719831b1c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef21f7327c0d996c5417e1332e9592fca1499694fd2ccd0241b6e2de714f73dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b1ee2876cd360c5fbce0fdc3add39f0275d6fcd2f07769ae0b2bdfd4bf16d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093d0486a468458af825b8f0d2a092df4f3a074d1288b1191d1b48a35c624fe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56680ed0aca9acf8d71eeaac7c165a9cd8c368cb3695f4a4b6a2b2bddcc780b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ba4a4eca5f29b85b2ca4b5b26366b55a6e92e0ce05120f49a66a6bc24bf13e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50aa8240c5f87fdf63b9a60f134695667252b86e1fe3fa96488e616bd3f2af74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14439309adbe238fe30734c613d433d3f4d84c134be6af3c4635e1698644daf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630d8f24d91ec1e4dd61f9f18626667fa7e3c375ddb73bae9cb1cac2c9793de9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484887e1305b3a724448ce986fad5e81b92e3133f06046601458173cc876c078(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__977c92811b64791b0280ab5853997d372ad7b3b608f85f0a90fa312a7bd3b744(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df7a3ee493c6050ec7c86b462beecf98b1601eb2c4717f383774a148d20553e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce7a41c150bb1d6b843287748c4ef52bfde382261769d4350a457f12b8adf61(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e54e59a2cd47143b90ddf4f2602db3c6d0f5c8f88b7d4ff4d99d40efb2c401(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1AddJobs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5adeac6b80ae85a20793e28376b81064244966a3b56c93d50540647850d158fa(
    *,
    fail_action: builtins.str,
    name: builtins.str,
    nodes: typing.Sequence[builtins.str],
    uri: builtins.str,
    active_master: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    before_component_start: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81d8be4002653d4935d1d711d9dadc138dfb1763dcdd44b4d382fab119484b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eed72ebf523f5dbd79e9243d5c6e6295bf8c2eaa53ac4ed8982baf203719598(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70aade2036d97ae915a6ba0be159e753c6fb801e40e4fb60b735d567b1ddf100(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314fdc5cd2996eea80018dae2a76908462dd0a0d64989fa2f0e586769cb17693(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51736ae159228a17ae1620fd8a60c28a217fe88426571f5687d35485a723695c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3107475520931c3573c157d758634c6f48458e6902f2651ce5998322e8d3b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1BootstrapScripts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d11d57402176a7b29a47e980b442b3f6412eb2eaeb355ce9cf77d65a7c10af3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbd77e7a7dc18432e707394e68542358363b4198ceba736c6dff8a42f7744d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a1da23588b228c5e9640fab18515fe2700f07878a261f347297195b3992fcf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88011e9f0952810deffd9ea3b6d50d6200bff5d2a938693f5148dde3af3bf618(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee8bff7c1dca22464e85f27d5dcb79631c03f0d8b0f0d5252453a406c06d484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f06d139cba75ad22c95a3bf2e7d36a1e6151d8f104eb3d0e60a0a4857b5943e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a518b6d94e9f1400904a22875c2dd1c6f1a38a19388af85b1d10983b761f11bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5f9db2b39693b5412f514a5d4edd2352dbde4702553c4666e8d95b9fffcdd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2effcd90558d611d5972f4947ad107f24444321666ad582d5f54849d457c805(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1BootstrapScripts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8083d53c5c7e565a2fa9b4fe30c349e18de3405056b526a12a743424344ee312(
    *,
    component_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f15d3b95cdb0d809693aefe1dc76a57f4fe717f6ce7f2484f612f734c5c96b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49f1df27041eeac218c03e734370665db1e1d78fe411bf39ee0885c88b34d06(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26a715031da90b6d375169dc30d158c9582f62b4a17aedb64fe11a212b29e56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4f2ac25ac571c14b223fed45555a4b1041f3dc48a3b5c7961a1feae379d1d8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad50185401665ce2707ca0bb2709d42cc8a1389cf091dc57c418fccaab1cb70a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc80fe8581dcd33ddb1495269b5c87b287e5acf16c060fd017228cf65526d616(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MrsClusterV1ComponentListStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c791c7847ff302d55396586d69723932609451124090d681ab3d5ef4c1d3a3ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208c03d559348c20276afe2a40302808b960bfdbeb63f91847d16401be84fd3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7a91b173a57d3f3d9a07485eee372af05b67be31bab69261561f82729a1edc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1ComponentListStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47df84f0728f96ba2b311bac10a3538cb1f9649f64b6db9b01667b0f49dfca09(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    available_zone_id: builtins.str,
    billing_type: jsii.Number,
    cluster_name: builtins.str,
    cluster_version: builtins.str,
    component_list: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MrsClusterV1ComponentListStruct, typing.Dict[builtins.str, typing.Any]]]],
    core_node_num: jsii.Number,
    core_node_size: builtins.str,
    master_node_num: jsii.Number,
    master_node_size: builtins.str,
    node_public_cert_name: builtins.str,
    safe_mode: jsii.Number,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    add_jobs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MrsClusterV1AddJobs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bootstrap_scripts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MrsClusterV1BootstrapScripts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_admin_secret: typing.Optional[builtins.str] = None,
    cluster_type: typing.Optional[jsii.Number] = None,
    core_data_volume_count: typing.Optional[jsii.Number] = None,
    core_data_volume_size: typing.Optional[jsii.Number] = None,
    core_data_volume_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_collection: typing.Optional[jsii.Number] = None,
    master_data_volume_count: typing.Optional[jsii.Number] = None,
    master_data_volume_size: typing.Optional[jsii.Number] = None,
    master_data_volume_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MrsClusterV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138cf2bfdcf9c3a8d57158c552e2b73bf45deda4ae8985d9ea3a121364275302(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce3e2027d680b66224857403b9ddb8aa0f223c8af51eb3b1c38cbab47bf37ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e6e1e41c60a41cd3c0eed4b716c869cef447f0fdf65696273caff63960fedd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3293d5d6de711790a6206584ede356b5ec9fb61c17ae2f674ab228c6da18c30b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306c85971153e408f3bf140a9d8b20c5b7723803ae8441b7fa4a55b451254ec3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MrsClusterV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
