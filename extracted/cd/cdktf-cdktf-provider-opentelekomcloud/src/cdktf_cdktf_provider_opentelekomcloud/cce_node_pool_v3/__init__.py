r'''
# `opentelekomcloud_cce_node_pool_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_cce_node_pool_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3).
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


class CceNodePoolV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodePoolV3.CceNodePoolV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3 opentelekomcloud_cce_node_pool_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_id: builtins.str,
        data_volumes: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodePoolV3DataVolumes", typing.Dict[builtins.str, typing.Any]]]],
        flavor: builtins.str,
        initial_node_count: jsii.Number,
        name: builtins.str,
        root_volume: typing.Union["CceNodePoolV3RootVolume", typing.Dict[builtins.str, typing.Any]],
        agency_name: typing.Optional[builtins.str] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        docker_base_size: typing.Optional[jsii.Number] = None,
        docker_lvm_config_override: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        key_pair: typing.Optional[builtins.str] = None,
        max_node_count: typing.Optional[jsii.Number] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        min_node_count: typing.Optional[jsii.Number] = None,
        os: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        postinstall: typing.Optional[builtins.str] = None,
        preinstall: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        runtime: typing.Optional[builtins.str] = None,
        scale_down_cooldown_time: typing.Optional[jsii.Number] = None,
        scale_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        server_group_reference: typing.Optional[builtins.str] = None,
        storage: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodePoolV3Taints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CceNodePoolV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3 opentelekomcloud_cce_node_pool_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#cluster_id CceNodePoolV3#cluster_id}.
        :param data_volumes: data_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#data_volumes CceNodePoolV3#data_volumes}
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#flavor CceNodePoolV3#flavor}.
        :param initial_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#initial_node_count CceNodePoolV3#initial_node_count}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#name CceNodePoolV3#name}.
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#root_volume CceNodePoolV3#root_volume}
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#agency_name CceNodePoolV3#agency_name}.
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#availability_zone CceNodePoolV3#availability_zone}.
        :param docker_base_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#docker_base_size CceNodePoolV3#docker_base_size}.
        :param docker_lvm_config_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#docker_lvm_config_override CceNodePoolV3#docker_lvm_config_override}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#id CceNodePoolV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param k8_s_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#k8s_tags CceNodePoolV3#k8s_tags}.
        :param key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#key_pair CceNodePoolV3#key_pair}.
        :param max_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#max_node_count CceNodePoolV3#max_node_count}.
        :param max_pods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#max_pods CceNodePoolV3#max_pods}.
        :param min_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#min_node_count CceNodePoolV3#min_node_count}.
        :param os: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#os CceNodePoolV3#os}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#password CceNodePoolV3#password}.
        :param postinstall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#postinstall CceNodePoolV3#postinstall}.
        :param preinstall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#preinstall CceNodePoolV3#preinstall}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#priority CceNodePoolV3#priority}.
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#runtime CceNodePoolV3#runtime}.
        :param scale_down_cooldown_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#scale_down_cooldown_time CceNodePoolV3#scale_down_cooldown_time}.
        :param scale_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#scale_enable CceNodePoolV3#scale_enable}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#security_group_ids CceNodePoolV3#security_group_ids}.
        :param server_group_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#server_group_reference CceNodePoolV3#server_group_reference}.
        :param storage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#storage CceNodePoolV3#storage}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#subnet_id CceNodePoolV3#subnet_id}.
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#taints CceNodePoolV3#taints}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#timeouts CceNodePoolV3#timeouts}
        :param user_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#user_tags CceNodePoolV3#user_tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef71f20745530d8fca9cb356af9046eb1182365c39f14c60a78599acdb23cdb2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CceNodePoolV3Config(
            cluster_id=cluster_id,
            data_volumes=data_volumes,
            flavor=flavor,
            initial_node_count=initial_node_count,
            name=name,
            root_volume=root_volume,
            agency_name=agency_name,
            availability_zone=availability_zone,
            docker_base_size=docker_base_size,
            docker_lvm_config_override=docker_lvm_config_override,
            id=id,
            k8_s_tags=k8_s_tags,
            key_pair=key_pair,
            max_node_count=max_node_count,
            max_pods=max_pods,
            min_node_count=min_node_count,
            os=os,
            password=password,
            postinstall=postinstall,
            preinstall=preinstall,
            priority=priority,
            runtime=runtime,
            scale_down_cooldown_time=scale_down_cooldown_time,
            scale_enable=scale_enable,
            security_group_ids=security_group_ids,
            server_group_reference=server_group_reference,
            storage=storage,
            subnet_id=subnet_id,
            taints=taints,
            timeouts=timeouts,
            user_tags=user_tags,
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
        '''Generates CDKTF code for importing a CceNodePoolV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CceNodePoolV3 to import.
        :param import_from_id: The id of the existing CceNodePoolV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CceNodePoolV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c8c3d97296b5ac5347ba06ce104510613f75798eb94d3347e8b2d88b835002)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataVolumes")
    def put_data_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodePoolV3DataVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9851e88d94010930cc7783ef5ea587612af4436ef386ca704d8de0c489731940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataVolumes", [value]))

    @jsii.member(jsii_name="putRootVolume")
    def put_root_volume(
        self,
        *,
        size: jsii.Number,
        volumetype: builtins.str,
        extend_param: typing.Optional[builtins.str] = None,
        extend_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        kms_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#size CceNodePoolV3#size}.
        :param volumetype: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#volumetype CceNodePoolV3#volumetype}.
        :param extend_param: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#extend_param CceNodePoolV3#extend_param}.
        :param extend_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#extend_params CceNodePoolV3#extend_params}.
        :param kms_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#kms_id CceNodePoolV3#kms_id}.
        '''
        value = CceNodePoolV3RootVolume(
            size=size,
            volumetype=volumetype,
            extend_param=extend_param,
            extend_params=extend_params,
            kms_id=kms_id,
        )

        return typing.cast(None, jsii.invoke(self, "putRootVolume", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodePoolV3Taints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795fbb2d07b29cc1e91142ce75c0c7b386398a3fe301928dbacf6318fbf63551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaints", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#create CceNodePoolV3#create}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#default CceNodePoolV3#default}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#delete CceNodePoolV3#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#update CceNodePoolV3#update}.
        '''
        value = CceNodePoolV3Timeouts(
            create=create, default=default, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAgencyName")
    def reset_agency_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgencyName", []))

    @jsii.member(jsii_name="resetAvailabilityZone")
    def reset_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZone", []))

    @jsii.member(jsii_name="resetDockerBaseSize")
    def reset_docker_base_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerBaseSize", []))

    @jsii.member(jsii_name="resetDockerLvmConfigOverride")
    def reset_docker_lvm_config_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerLvmConfigOverride", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetK8STags")
    def reset_k8_s_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetK8STags", []))

    @jsii.member(jsii_name="resetKeyPair")
    def reset_key_pair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPair", []))

    @jsii.member(jsii_name="resetMaxNodeCount")
    def reset_max_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNodeCount", []))

    @jsii.member(jsii_name="resetMaxPods")
    def reset_max_pods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPods", []))

    @jsii.member(jsii_name="resetMinNodeCount")
    def reset_min_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNodeCount", []))

    @jsii.member(jsii_name="resetOs")
    def reset_os(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOs", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPostinstall")
    def reset_postinstall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostinstall", []))

    @jsii.member(jsii_name="resetPreinstall")
    def reset_preinstall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreinstall", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetRuntime")
    def reset_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntime", []))

    @jsii.member(jsii_name="resetScaleDownCooldownTime")
    def reset_scale_down_cooldown_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleDownCooldownTime", []))

    @jsii.member(jsii_name="resetScaleEnable")
    def reset_scale_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaleEnable", []))

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @jsii.member(jsii_name="resetServerGroupReference")
    def reset_server_group_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerGroupReference", []))

    @jsii.member(jsii_name="resetStorage")
    def reset_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorage", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetTaints")
    def reset_taints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaints", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserTags")
    def reset_user_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTags", []))

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
    @jsii.member(jsii_name="dataVolumes")
    def data_volumes(self) -> "CceNodePoolV3DataVolumesList":
        return typing.cast("CceNodePoolV3DataVolumesList", jsii.get(self, "dataVolumes"))

    @builtins.property
    @jsii.member(jsii_name="rootVolume")
    def root_volume(self) -> "CceNodePoolV3RootVolumeOutputReference":
        return typing.cast("CceNodePoolV3RootVolumeOutputReference", jsii.get(self, "rootVolume"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(self) -> "CceNodePoolV3TaintsList":
        return typing.cast("CceNodePoolV3TaintsList", jsii.get(self, "taints"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CceNodePoolV3TimeoutsOutputReference":
        return typing.cast("CceNodePoolV3TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="agencyNameInput")
    def agency_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataVolumesInput")
    def data_volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodePoolV3DataVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodePoolV3DataVolumes"]]], jsii.get(self, "dataVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerBaseSizeInput")
    def docker_base_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dockerBaseSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerLvmConfigOverrideInput")
    def docker_lvm_config_override_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerLvmConfigOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initialNodeCountInput")
    def initial_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="k8STagsInput")
    def k8_s_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "k8STagsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPairInput")
    def key_pair_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPairInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNodeCountInput")
    def max_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsInput")
    def max_pods_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCountInput")
    def min_node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="osInput")
    def os_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="postinstallInput")
    def postinstall_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postinstallInput"))

    @builtins.property
    @jsii.member(jsii_name="preinstallInput")
    def preinstall_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preinstallInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="rootVolumeInput")
    def root_volume_input(self) -> typing.Optional["CceNodePoolV3RootVolume"]:
        return typing.cast(typing.Optional["CceNodePoolV3RootVolume"], jsii.get(self, "rootVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleDownCooldownTimeInput")
    def scale_down_cooldown_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleDownCooldownTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleEnableInput")
    def scale_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "scaleEnableInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="serverGroupReferenceInput")
    def server_group_reference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverGroupReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodePoolV3Taints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodePoolV3Taints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CceNodePoolV3Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CceNodePoolV3Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userTagsInput")
    def user_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "userTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyName")
    def agency_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agencyName"))

    @agency_name.setter
    def agency_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06d92510c2c8581b43461cfc6a3dae25f3770f23ccadcbe140f7eb322b69fac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d15421b6b416af1d28e9d2c37df032795b626294fe11ec2766614998a11280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__563e3796b555ab11e2750664a39367bd3d25dd5c6da3cf2f02a01da1d41ba465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerBaseSize")
    def docker_base_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dockerBaseSize"))

    @docker_base_size.setter
    def docker_base_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__215369b5a9e99c6cdaea02cc0d2926cf47ba7cfd8cf12859a8514096ac63b944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerBaseSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerLvmConfigOverride")
    def docker_lvm_config_override(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerLvmConfigOverride"))

    @docker_lvm_config_override.setter
    def docker_lvm_config_override(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599b9204d6013fe1a9281e2c68b26bd6e1ba30600265c6d5ea6bde5ca4b0477f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerLvmConfigOverride", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @flavor.setter
    def flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43c16f8c65c1a29486801cac932031a6f2fdd85da460b730d0a10ea0aa437dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4031c702b5a17d5caefb6082c73f198b196ec8508a30ce3fae8c0c4f9b1b487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialNodeCount")
    def initial_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialNodeCount"))

    @initial_node_count.setter
    def initial_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9397b5f4cd5ac5c69e8b2a914dbb4833fe4315e34ac3ae1a1be519d2ed3422cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="k8STags")
    def k8_s_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "k8STags"))

    @k8_s_tags.setter
    def k8_s_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f3bfe2b560d27782482f1e74fcd2940d3d80e7619e548c55fa67ba3b45c8a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "k8STags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyPair")
    def key_pair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPair"))

    @key_pair.setter
    def key_pair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84fce04278e7d12a1c721a80fe8b901b71cb6c89cd83300827f80afeb2a24c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxNodeCount")
    def max_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNodeCount"))

    @max_node_count.setter
    def max_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43369b6d7a76ee31d1ec199dd1797591f07770ff6ebfca229a51c1dcdb76f01b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPods")
    def max_pods(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPods"))

    @max_pods.setter
    def max_pods(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1457f7037f7ecaebe184bd06919c7257133b1e56dd9794e434098c0388a3d6b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCount")
    def min_node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCount"))

    @min_node_count.setter
    def min_node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9778d25b3f25bcb5770f1eb56f7cdb0ead79865974d2e6206d81e5191f81eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf1c973936e2f3da03421f90b67cd74f903b460791ed4e4eb73f82408274bbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="os")
    def os(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "os"))

    @os.setter
    def os(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce47e074a56ba9518ee2cb41a8c2aebf71dd473c2083c72c7068e93e50f2718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "os", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fb55db9194af2c67d588182af3dc9613f05f67e4ead6110769e942e2912a4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postinstall")
    def postinstall(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postinstall"))

    @postinstall.setter
    def postinstall(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078d6a75652143c1d9f2e22ce79fd0c0be75f8e6fed21b12e0015b2c751b89ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postinstall", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preinstall")
    def preinstall(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preinstall"))

    @preinstall.setter
    def preinstall(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee036ab3587338cf75921149f4c9f42205f4f5816216d1c7db9e3475a5d6daa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preinstall", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f1743b7941ed8f28e88afd97eab0addc86dfea99823c32cf69d020f2839e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e82f6456ce82f547684fd437d3674647a8b104f47e993fe4a37b1057c613ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleDownCooldownTime")
    def scale_down_cooldown_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleDownCooldownTime"))

    @scale_down_cooldown_time.setter
    def scale_down_cooldown_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a260da67d94c294f5064064ac38405456d303f2ad999ae4930a0ec46d56ac968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleDownCooldownTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleEnable")
    def scale_enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "scaleEnable"))

    @scale_enable.setter
    def scale_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa12bec5b2628f722259e70e0c9bcac74c2d032078d55584f305678439a60972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8344939f6fdb6b7f95a5cfa7828e5e79c1c4678e9280fd234ca2b9559ee0ce3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverGroupReference")
    def server_group_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverGroupReference"))

    @server_group_reference.setter
    def server_group_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3353c5f72f686a8b326c114af504bbf354a02754703c125be1d3d5216cb1788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverGroupReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storage"))

    @storage.setter
    def storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59993fd57881cbe8aacc4cebfd4b51d12414242081751ffbb585a6f406cc4c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e4a2e113e965a6ff26893db9a58b39c91197828fb2e6239b0017640fd0ad3e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTags")
    def user_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "userTags"))

    @user_tags.setter
    def user_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c01ca0cf534acf320a7b2dacb1e3c12095e272506230b10966c7fae904ad4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodePoolV3.CceNodePoolV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_id": "clusterId",
        "data_volumes": "dataVolumes",
        "flavor": "flavor",
        "initial_node_count": "initialNodeCount",
        "name": "name",
        "root_volume": "rootVolume",
        "agency_name": "agencyName",
        "availability_zone": "availabilityZone",
        "docker_base_size": "dockerBaseSize",
        "docker_lvm_config_override": "dockerLvmConfigOverride",
        "id": "id",
        "k8_s_tags": "k8STags",
        "key_pair": "keyPair",
        "max_node_count": "maxNodeCount",
        "max_pods": "maxPods",
        "min_node_count": "minNodeCount",
        "os": "os",
        "password": "password",
        "postinstall": "postinstall",
        "preinstall": "preinstall",
        "priority": "priority",
        "runtime": "runtime",
        "scale_down_cooldown_time": "scaleDownCooldownTime",
        "scale_enable": "scaleEnable",
        "security_group_ids": "securityGroupIds",
        "server_group_reference": "serverGroupReference",
        "storage": "storage",
        "subnet_id": "subnetId",
        "taints": "taints",
        "timeouts": "timeouts",
        "user_tags": "userTags",
    },
)
class CceNodePoolV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_id: builtins.str,
        data_volumes: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodePoolV3DataVolumes", typing.Dict[builtins.str, typing.Any]]]],
        flavor: builtins.str,
        initial_node_count: jsii.Number,
        name: builtins.str,
        root_volume: typing.Union["CceNodePoolV3RootVolume", typing.Dict[builtins.str, typing.Any]],
        agency_name: typing.Optional[builtins.str] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        docker_base_size: typing.Optional[jsii.Number] = None,
        docker_lvm_config_override: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        key_pair: typing.Optional[builtins.str] = None,
        max_node_count: typing.Optional[jsii.Number] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        min_node_count: typing.Optional[jsii.Number] = None,
        os: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        postinstall: typing.Optional[builtins.str] = None,
        preinstall: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        runtime: typing.Optional[builtins.str] = None,
        scale_down_cooldown_time: typing.Optional[jsii.Number] = None,
        scale_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        server_group_reference: typing.Optional[builtins.str] = None,
        storage: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodePoolV3Taints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CceNodePoolV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#cluster_id CceNodePoolV3#cluster_id}.
        :param data_volumes: data_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#data_volumes CceNodePoolV3#data_volumes}
        :param flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#flavor CceNodePoolV3#flavor}.
        :param initial_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#initial_node_count CceNodePoolV3#initial_node_count}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#name CceNodePoolV3#name}.
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#root_volume CceNodePoolV3#root_volume}
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#agency_name CceNodePoolV3#agency_name}.
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#availability_zone CceNodePoolV3#availability_zone}.
        :param docker_base_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#docker_base_size CceNodePoolV3#docker_base_size}.
        :param docker_lvm_config_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#docker_lvm_config_override CceNodePoolV3#docker_lvm_config_override}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#id CceNodePoolV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param k8_s_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#k8s_tags CceNodePoolV3#k8s_tags}.
        :param key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#key_pair CceNodePoolV3#key_pair}.
        :param max_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#max_node_count CceNodePoolV3#max_node_count}.
        :param max_pods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#max_pods CceNodePoolV3#max_pods}.
        :param min_node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#min_node_count CceNodePoolV3#min_node_count}.
        :param os: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#os CceNodePoolV3#os}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#password CceNodePoolV3#password}.
        :param postinstall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#postinstall CceNodePoolV3#postinstall}.
        :param preinstall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#preinstall CceNodePoolV3#preinstall}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#priority CceNodePoolV3#priority}.
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#runtime CceNodePoolV3#runtime}.
        :param scale_down_cooldown_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#scale_down_cooldown_time CceNodePoolV3#scale_down_cooldown_time}.
        :param scale_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#scale_enable CceNodePoolV3#scale_enable}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#security_group_ids CceNodePoolV3#security_group_ids}.
        :param server_group_reference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#server_group_reference CceNodePoolV3#server_group_reference}.
        :param storage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#storage CceNodePoolV3#storage}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#subnet_id CceNodePoolV3#subnet_id}.
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#taints CceNodePoolV3#taints}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#timeouts CceNodePoolV3#timeouts}
        :param user_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#user_tags CceNodePoolV3#user_tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(root_volume, dict):
            root_volume = CceNodePoolV3RootVolume(**root_volume)
        if isinstance(timeouts, dict):
            timeouts = CceNodePoolV3Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79095f7f14baadc72faad8b3bbb6a491ea82aba2cfbbf008eec0d9b0a5eef049)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument data_volumes", value=data_volumes, expected_type=type_hints["data_volumes"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument initial_node_count", value=initial_node_count, expected_type=type_hints["initial_node_count"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument root_volume", value=root_volume, expected_type=type_hints["root_volume"])
            check_type(argname="argument agency_name", value=agency_name, expected_type=type_hints["agency_name"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument docker_base_size", value=docker_base_size, expected_type=type_hints["docker_base_size"])
            check_type(argname="argument docker_lvm_config_override", value=docker_lvm_config_override, expected_type=type_hints["docker_lvm_config_override"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument k8_s_tags", value=k8_s_tags, expected_type=type_hints["k8_s_tags"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument max_node_count", value=max_node_count, expected_type=type_hints["max_node_count"])
            check_type(argname="argument max_pods", value=max_pods, expected_type=type_hints["max_pods"])
            check_type(argname="argument min_node_count", value=min_node_count, expected_type=type_hints["min_node_count"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument postinstall", value=postinstall, expected_type=type_hints["postinstall"])
            check_type(argname="argument preinstall", value=preinstall, expected_type=type_hints["preinstall"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument scale_down_cooldown_time", value=scale_down_cooldown_time, expected_type=type_hints["scale_down_cooldown_time"])
            check_type(argname="argument scale_enable", value=scale_enable, expected_type=type_hints["scale_enable"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument server_group_reference", value=server_group_reference, expected_type=type_hints["server_group_reference"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_tags", value=user_tags, expected_type=type_hints["user_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
            "data_volumes": data_volumes,
            "flavor": flavor,
            "initial_node_count": initial_node_count,
            "name": name,
            "root_volume": root_volume,
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
        if agency_name is not None:
            self._values["agency_name"] = agency_name
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if docker_base_size is not None:
            self._values["docker_base_size"] = docker_base_size
        if docker_lvm_config_override is not None:
            self._values["docker_lvm_config_override"] = docker_lvm_config_override
        if id is not None:
            self._values["id"] = id
        if k8_s_tags is not None:
            self._values["k8_s_tags"] = k8_s_tags
        if key_pair is not None:
            self._values["key_pair"] = key_pair
        if max_node_count is not None:
            self._values["max_node_count"] = max_node_count
        if max_pods is not None:
            self._values["max_pods"] = max_pods
        if min_node_count is not None:
            self._values["min_node_count"] = min_node_count
        if os is not None:
            self._values["os"] = os
        if password is not None:
            self._values["password"] = password
        if postinstall is not None:
            self._values["postinstall"] = postinstall
        if preinstall is not None:
            self._values["preinstall"] = preinstall
        if priority is not None:
            self._values["priority"] = priority
        if runtime is not None:
            self._values["runtime"] = runtime
        if scale_down_cooldown_time is not None:
            self._values["scale_down_cooldown_time"] = scale_down_cooldown_time
        if scale_enable is not None:
            self._values["scale_enable"] = scale_enable
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if server_group_reference is not None:
            self._values["server_group_reference"] = server_group_reference
        if storage is not None:
            self._values["storage"] = storage
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if taints is not None:
            self._values["taints"] = taints
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_tags is not None:
            self._values["user_tags"] = user_tags

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
    def cluster_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#cluster_id CceNodePoolV3#cluster_id}.'''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_volumes(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodePoolV3DataVolumes"]]:
        '''data_volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#data_volumes CceNodePoolV3#data_volumes}
        '''
        result = self._values.get("data_volumes")
        assert result is not None, "Required property 'data_volumes' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodePoolV3DataVolumes"]], result)

    @builtins.property
    def flavor(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#flavor CceNodePoolV3#flavor}.'''
        result = self._values.get("flavor")
        assert result is not None, "Required property 'flavor' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_node_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#initial_node_count CceNodePoolV3#initial_node_count}.'''
        result = self._values.get("initial_node_count")
        assert result is not None, "Required property 'initial_node_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#name CceNodePoolV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_volume(self) -> "CceNodePoolV3RootVolume":
        '''root_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#root_volume CceNodePoolV3#root_volume}
        '''
        result = self._values.get("root_volume")
        assert result is not None, "Required property 'root_volume' is missing"
        return typing.cast("CceNodePoolV3RootVolume", result)

    @builtins.property
    def agency_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#agency_name CceNodePoolV3#agency_name}.'''
        result = self._values.get("agency_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#availability_zone CceNodePoolV3#availability_zone}.'''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_base_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#docker_base_size CceNodePoolV3#docker_base_size}.'''
        result = self._values.get("docker_base_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_lvm_config_override(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#docker_lvm_config_override CceNodePoolV3#docker_lvm_config_override}.'''
        result = self._values.get("docker_lvm_config_override")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#id CceNodePoolV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def k8_s_tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#k8s_tags CceNodePoolV3#k8s_tags}.'''
        result = self._values.get("k8_s_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def key_pair(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#key_pair CceNodePoolV3#key_pair}.'''
        result = self._values.get("key_pair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_node_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#max_node_count CceNodePoolV3#max_node_count}.'''
        result = self._values.get("max_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pods(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#max_pods CceNodePoolV3#max_pods}.'''
        result = self._values.get("max_pods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_node_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#min_node_count CceNodePoolV3#min_node_count}.'''
        result = self._values.get("min_node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def os(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#os CceNodePoolV3#os}.'''
        result = self._values.get("os")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#password CceNodePoolV3#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postinstall(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#postinstall CceNodePoolV3#postinstall}.'''
        result = self._values.get("postinstall")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preinstall(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#preinstall CceNodePoolV3#preinstall}.'''
        result = self._values.get("preinstall")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#priority CceNodePoolV3#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#runtime CceNodePoolV3#runtime}.'''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_cooldown_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#scale_down_cooldown_time CceNodePoolV3#scale_down_cooldown_time}.'''
        result = self._values.get("scale_down_cooldown_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scale_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#scale_enable CceNodePoolV3#scale_enable}.'''
        result = self._values.get("scale_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#security_group_ids CceNodePoolV3#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def server_group_reference(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#server_group_reference CceNodePoolV3#server_group_reference}.'''
        result = self._values.get("server_group_reference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#storage CceNodePoolV3#storage}.'''
        result = self._values.get("storage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#subnet_id CceNodePoolV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodePoolV3Taints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#taints CceNodePoolV3#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodePoolV3Taints"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CceNodePoolV3Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#timeouts CceNodePoolV3#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CceNodePoolV3Timeouts"], result)

    @builtins.property
    def user_tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#user_tags CceNodePoolV3#user_tags}.'''
        result = self._values.get("user_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodePoolV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodePoolV3.CceNodePoolV3DataVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "size": "size",
        "volumetype": "volumetype",
        "extend_param": "extendParam",
        "extend_params": "extendParams",
        "kms_id": "kmsId",
    },
)
class CceNodePoolV3DataVolumes:
    def __init__(
        self,
        *,
        size: jsii.Number,
        volumetype: builtins.str,
        extend_param: typing.Optional[builtins.str] = None,
        extend_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        kms_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#size CceNodePoolV3#size}.
        :param volumetype: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#volumetype CceNodePoolV3#volumetype}.
        :param extend_param: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#extend_param CceNodePoolV3#extend_param}.
        :param extend_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#extend_params CceNodePoolV3#extend_params}.
        :param kms_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#kms_id CceNodePoolV3#kms_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907228f26e61905fb25aac4fa0997f4ccd86a856a66c871dcedcd52e07a49928)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument volumetype", value=volumetype, expected_type=type_hints["volumetype"])
            check_type(argname="argument extend_param", value=extend_param, expected_type=type_hints["extend_param"])
            check_type(argname="argument extend_params", value=extend_params, expected_type=type_hints["extend_params"])
            check_type(argname="argument kms_id", value=kms_id, expected_type=type_hints["kms_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "size": size,
            "volumetype": volumetype,
        }
        if extend_param is not None:
            self._values["extend_param"] = extend_param
        if extend_params is not None:
            self._values["extend_params"] = extend_params
        if kms_id is not None:
            self._values["kms_id"] = kms_id

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#size CceNodePoolV3#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volumetype(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#volumetype CceNodePoolV3#volumetype}.'''
        result = self._values.get("volumetype")
        assert result is not None, "Required property 'volumetype' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def extend_param(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#extend_param CceNodePoolV3#extend_param}.'''
        result = self._values.get("extend_param")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extend_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#extend_params CceNodePoolV3#extend_params}.'''
        result = self._values.get("extend_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def kms_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#kms_id CceNodePoolV3#kms_id}.'''
        result = self._values.get("kms_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodePoolV3DataVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodePoolV3DataVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodePoolV3.CceNodePoolV3DataVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e7c455bc904e62be7d0ce1e09dee1ed0d23a1b61e1ae0bd01c6a2b3540041a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CceNodePoolV3DataVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7461c3edebc50540f24aacf2503b8e775cb14a6e17497066026f38406f14e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceNodePoolV3DataVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf80459722721cb921fb2267ad898997eebfae50c40b736bb617ab844bf4099)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18915192a94942f6c5c5c4ead92036007306b3c1456ee6d7b51cf740e731b814)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12080455cae174a5f8e1cc4ea5cdffbc9f4b5fc7c4220dc81f6f2ce77a33a2a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodePoolV3DataVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodePoolV3DataVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodePoolV3DataVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd7ff23960cbd03dbb8b8ca6421a31db3a2a793f2a5877977e9fbc3f4bb665f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CceNodePoolV3DataVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodePoolV3.CceNodePoolV3DataVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c4e3c60b0ba350b75a8db10c57850d5963d014c95ce17fe59849a0003aa151f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExtendParam")
    def reset_extend_param(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendParam", []))

    @jsii.member(jsii_name="resetExtendParams")
    def reset_extend_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendParams", []))

    @jsii.member(jsii_name="resetKmsId")
    def reset_kms_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsId", []))

    @builtins.property
    @jsii.member(jsii_name="extendParamInput")
    def extend_param_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extendParamInput"))

    @builtins.property
    @jsii.member(jsii_name="extendParamsInput")
    def extend_params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extendParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsIdInput")
    def kms_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumetypeInput")
    def volumetype_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumetypeInput"))

    @builtins.property
    @jsii.member(jsii_name="extendParam")
    def extend_param(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extendParam"))

    @extend_param.setter
    def extend_param(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b1c5371991b456719ad74fd7a4fa15e8e4d1fbe3a08219b31da23980f4a8378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParam", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extendParams")
    def extend_params(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extendParams"))

    @extend_params.setter
    def extend_params(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45398e8845e38abb3210bc171a6286da526df6c9a975e39e786434908a10dfba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsId")
    def kms_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsId"))

    @kms_id.setter
    def kms_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb54dc315c896939beab8210aa874f435cfebf0ddfba481f3f4dfe040c3cda8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e635df988fdf10ab389a4382a03f560c1fed95347276077ec87d45b6d7f8bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumetype")
    def volumetype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumetype"))

    @volumetype.setter
    def volumetype(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f846cab6c5e2b6d1427b842d2f277da58315dd283980389d195eb1b9cc082b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumetype", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodePoolV3DataVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodePoolV3DataVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodePoolV3DataVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773baab74f784deb08bea8bd5b594fb4d012db5643facc0a04f3b26fdba7b861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodePoolV3.CceNodePoolV3RootVolume",
    jsii_struct_bases=[],
    name_mapping={
        "size": "size",
        "volumetype": "volumetype",
        "extend_param": "extendParam",
        "extend_params": "extendParams",
        "kms_id": "kmsId",
    },
)
class CceNodePoolV3RootVolume:
    def __init__(
        self,
        *,
        size: jsii.Number,
        volumetype: builtins.str,
        extend_param: typing.Optional[builtins.str] = None,
        extend_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        kms_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#size CceNodePoolV3#size}.
        :param volumetype: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#volumetype CceNodePoolV3#volumetype}.
        :param extend_param: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#extend_param CceNodePoolV3#extend_param}.
        :param extend_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#extend_params CceNodePoolV3#extend_params}.
        :param kms_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#kms_id CceNodePoolV3#kms_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dccf5e4fa7ef2a5c9bb7f61b245bf953731a9adb1119dac1b12df982dd0ee52b)
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument volumetype", value=volumetype, expected_type=type_hints["volumetype"])
            check_type(argname="argument extend_param", value=extend_param, expected_type=type_hints["extend_param"])
            check_type(argname="argument extend_params", value=extend_params, expected_type=type_hints["extend_params"])
            check_type(argname="argument kms_id", value=kms_id, expected_type=type_hints["kms_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "size": size,
            "volumetype": volumetype,
        }
        if extend_param is not None:
            self._values["extend_param"] = extend_param
        if extend_params is not None:
            self._values["extend_params"] = extend_params
        if kms_id is not None:
            self._values["kms_id"] = kms_id

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#size CceNodePoolV3#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volumetype(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#volumetype CceNodePoolV3#volumetype}.'''
        result = self._values.get("volumetype")
        assert result is not None, "Required property 'volumetype' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def extend_param(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#extend_param CceNodePoolV3#extend_param}.'''
        result = self._values.get("extend_param")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extend_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#extend_params CceNodePoolV3#extend_params}.'''
        result = self._values.get("extend_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def kms_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#kms_id CceNodePoolV3#kms_id}.'''
        result = self._values.get("kms_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodePoolV3RootVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodePoolV3RootVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodePoolV3.CceNodePoolV3RootVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2483167117089d9bc770ea9f48a39e5dbc6d325bfdf4e053a089f3e77f21a337)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExtendParam")
    def reset_extend_param(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendParam", []))

    @jsii.member(jsii_name="resetExtendParams")
    def reset_extend_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendParams", []))

    @jsii.member(jsii_name="resetKmsId")
    def reset_kms_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsId", []))

    @builtins.property
    @jsii.member(jsii_name="extendParamInput")
    def extend_param_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extendParamInput"))

    @builtins.property
    @jsii.member(jsii_name="extendParamsInput")
    def extend_params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "extendParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsIdInput")
    def kms_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumetypeInput")
    def volumetype_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumetypeInput"))

    @builtins.property
    @jsii.member(jsii_name="extendParam")
    def extend_param(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extendParam"))

    @extend_param.setter
    def extend_param(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37fc699df2b5dfa7d389f20f1e875527aa96fc8503b73a046682265b240d38aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParam", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extendParams")
    def extend_params(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extendParams"))

    @extend_params.setter
    def extend_params(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47fb3bf63911ac5beee5b970eb631bb4807edc090dbe5bbcd90d2b553bd7ded0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsId")
    def kms_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsId"))

    @kms_id.setter
    def kms_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ddcf9274120561c67fd27ac4bf344f5694e35fbd53679d25aeeca560777a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc555e10639c5c0820632edcde1ecf0736a22cd907d690b4a91fd2f50d77e23b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumetype")
    def volumetype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumetype"))

    @volumetype.setter
    def volumetype(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6221ea88c7d8557a9d7522ebccad6a4a611402552c1da2ecb513ecd2d2208eec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumetype", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CceNodePoolV3RootVolume]:
        return typing.cast(typing.Optional[CceNodePoolV3RootVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CceNodePoolV3RootVolume]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bba7c6bca85767d5faec86c6bcf9dc34e3f20e21bd82786863d6ed781270b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodePoolV3.CceNodePoolV3Taints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class CceNodePoolV3Taints:
    def __init__(
        self,
        *,
        effect: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param effect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#effect CceNodePoolV3#effect}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#key CceNodePoolV3#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#value CceNodePoolV3#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7f8e8363e827c3b7c33ce5f2640c9a184ce5112df6a9cca172cf61656426b5)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "effect": effect,
            "key": key,
            "value": value,
        }

    @builtins.property
    def effect(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#effect CceNodePoolV3#effect}.'''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#key CceNodePoolV3#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#value CceNodePoolV3#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodePoolV3Taints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodePoolV3TaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodePoolV3.CceNodePoolV3TaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad778f4a5fdef430518f7801a071956baf255a4799acd2052e8f4c780c7a5bb0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CceNodePoolV3TaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af1a8f316b5241f2670eb4fc7b2b323b123f2e78cfb6b0c1cfd75e8da85c2462)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceNodePoolV3TaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f1d1e4f2a4f6eee8f6716bea3172a0fdd19786989d52c6ac0500b00df8096a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1763a51bf394ff9908c4792c16cfe19241509a82c2eb31207f692f81cd16ead2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79e7897fd7b97c7285697fcb4208190d88d8350462aad39b4ced9bbd95b7c6c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodePoolV3Taints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodePoolV3Taints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodePoolV3Taints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13dafab7a689a8e63eb7aa66605e130a889639ad62c4dd7c98e942bc6094f726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CceNodePoolV3TaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodePoolV3.CceNodePoolV3TaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eedf85b06f68f236369a8730c2e4b15cafb3be5c0f04f31f6169d4169f47b216)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="effectInput")
    def effect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76991452e8b6b2c1443b7c79da799145a5ed0c6596216f75354f8087f3aafaf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0692c3e5669a213b4a569cb519d62837819037b8e2cc1feff6b468aa8fd94f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b55bfe39e82a689f8ccda299ae060ac349207b5e42d742d0ea30c5dbf0e0ae5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodePoolV3Taints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodePoolV3Taints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodePoolV3Taints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e7e0e4213e9727e556f372422369d0270d2a7fe1d763891eb05a850a481ac81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodePoolV3.CceNodePoolV3Timeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "default": "default",
        "delete": "delete",
        "update": "update",
    },
)
class CceNodePoolV3Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#create CceNodePoolV3#create}.
        :param default: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#default CceNodePoolV3#default}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#delete CceNodePoolV3#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#update CceNodePoolV3#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eba4d3c70e1ca8860fa09427f3ba6d3871ede1c3d3fcddb9941a5f4ecc901c2)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if default is not None:
            self._values["default"] = default
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#create CceNodePoolV3#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#default CceNodePoolV3#default}.'''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#delete CceNodePoolV3#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_pool_v3#update CceNodePoolV3#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodePoolV3Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodePoolV3TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodePoolV3.CceNodePoolV3TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31eb07890e159da5c570a9798b3ec81ee20f1fe9d4eac31bff16fbb040138fbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDefault")
    def reset_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefault", []))

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
    @jsii.member(jsii_name="defaultInput")
    def default_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d47de795ed994896e4e895270bff16832b392a1790319588277df45251c15d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @default.setter
    def default(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97246d4ecfadf78544a3d892d8ca420458921dd9b19f5b5a8cee2e9728a7f9a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7344950f04cb7a749258af2b1ccadb33e75db7edc258451bdfdaa7b311c863e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3c221f8ca30438623a4afc2fbde54fda155b53a4f0aa4ee6e33d8ec1300600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodePoolV3Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodePoolV3Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodePoolV3Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b53d038373e1c4180194fa5eaeb4d6c56faf3f994c4f1be9fd43402d88d0c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CceNodePoolV3",
    "CceNodePoolV3Config",
    "CceNodePoolV3DataVolumes",
    "CceNodePoolV3DataVolumesList",
    "CceNodePoolV3DataVolumesOutputReference",
    "CceNodePoolV3RootVolume",
    "CceNodePoolV3RootVolumeOutputReference",
    "CceNodePoolV3Taints",
    "CceNodePoolV3TaintsList",
    "CceNodePoolV3TaintsOutputReference",
    "CceNodePoolV3Timeouts",
    "CceNodePoolV3TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ef71f20745530d8fca9cb356af9046eb1182365c39f14c60a78599acdb23cdb2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_id: builtins.str,
    data_volumes: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodePoolV3DataVolumes, typing.Dict[builtins.str, typing.Any]]]],
    flavor: builtins.str,
    initial_node_count: jsii.Number,
    name: builtins.str,
    root_volume: typing.Union[CceNodePoolV3RootVolume, typing.Dict[builtins.str, typing.Any]],
    agency_name: typing.Optional[builtins.str] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    docker_base_size: typing.Optional[jsii.Number] = None,
    docker_lvm_config_override: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    key_pair: typing.Optional[builtins.str] = None,
    max_node_count: typing.Optional[jsii.Number] = None,
    max_pods: typing.Optional[jsii.Number] = None,
    min_node_count: typing.Optional[jsii.Number] = None,
    os: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    postinstall: typing.Optional[builtins.str] = None,
    preinstall: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    runtime: typing.Optional[builtins.str] = None,
    scale_down_cooldown_time: typing.Optional[jsii.Number] = None,
    scale_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    server_group_reference: typing.Optional[builtins.str] = None,
    storage: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodePoolV3Taints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[CceNodePoolV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__c3c8c3d97296b5ac5347ba06ce104510613f75798eb94d3347e8b2d88b835002(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9851e88d94010930cc7783ef5ea587612af4436ef386ca704d8de0c489731940(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodePoolV3DataVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795fbb2d07b29cc1e91142ce75c0c7b386398a3fe301928dbacf6318fbf63551(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodePoolV3Taints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d92510c2c8581b43461cfc6a3dae25f3770f23ccadcbe140f7eb322b69fac4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d15421b6b416af1d28e9d2c37df032795b626294fe11ec2766614998a11280(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__563e3796b555ab11e2750664a39367bd3d25dd5c6da3cf2f02a01da1d41ba465(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215369b5a9e99c6cdaea02cc0d2926cf47ba7cfd8cf12859a8514096ac63b944(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599b9204d6013fe1a9281e2c68b26bd6e1ba30600265c6d5ea6bde5ca4b0477f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c16f8c65c1a29486801cac932031a6f2fdd85da460b730d0a10ea0aa437dca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4031c702b5a17d5caefb6082c73f198b196ec8508a30ce3fae8c0c4f9b1b487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9397b5f4cd5ac5c69e8b2a914dbb4833fe4315e34ac3ae1a1be519d2ed3422cf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f3bfe2b560d27782482f1e74fcd2940d3d80e7619e548c55fa67ba3b45c8a4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84fce04278e7d12a1c721a80fe8b901b71cb6c89cd83300827f80afeb2a24c91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43369b6d7a76ee31d1ec199dd1797591f07770ff6ebfca229a51c1dcdb76f01b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1457f7037f7ecaebe184bd06919c7257133b1e56dd9794e434098c0388a3d6b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9778d25b3f25bcb5770f1eb56f7cdb0ead79865974d2e6206d81e5191f81eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf1c973936e2f3da03421f90b67cd74f903b460791ed4e4eb73f82408274bbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce47e074a56ba9518ee2cb41a8c2aebf71dd473c2083c72c7068e93e50f2718(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fb55db9194af2c67d588182af3dc9613f05f67e4ead6110769e942e2912a4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078d6a75652143c1d9f2e22ce79fd0c0be75f8e6fed21b12e0015b2c751b89ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee036ab3587338cf75921149f4c9f42205f4f5816216d1c7db9e3475a5d6daa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f1743b7941ed8f28e88afd97eab0addc86dfea99823c32cf69d020f2839e21(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e82f6456ce82f547684fd437d3674647a8b104f47e993fe4a37b1057c613ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a260da67d94c294f5064064ac38405456d303f2ad999ae4930a0ec46d56ac968(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa12bec5b2628f722259e70e0c9bcac74c2d032078d55584f305678439a60972(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8344939f6fdb6b7f95a5cfa7828e5e79c1c4678e9280fd234ca2b9559ee0ce3d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3353c5f72f686a8b326c114af504bbf354a02754703c125be1d3d5216cb1788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59993fd57881cbe8aacc4cebfd4b51d12414242081751ffbb585a6f406cc4c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e4a2e113e965a6ff26893db9a58b39c91197828fb2e6239b0017640fd0ad3e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c01ca0cf534acf320a7b2dacb1e3c12095e272506230b10966c7fae904ad4e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79095f7f14baadc72faad8b3bbb6a491ea82aba2cfbbf008eec0d9b0a5eef049(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_id: builtins.str,
    data_volumes: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodePoolV3DataVolumes, typing.Dict[builtins.str, typing.Any]]]],
    flavor: builtins.str,
    initial_node_count: jsii.Number,
    name: builtins.str,
    root_volume: typing.Union[CceNodePoolV3RootVolume, typing.Dict[builtins.str, typing.Any]],
    agency_name: typing.Optional[builtins.str] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    docker_base_size: typing.Optional[jsii.Number] = None,
    docker_lvm_config_override: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    key_pair: typing.Optional[builtins.str] = None,
    max_node_count: typing.Optional[jsii.Number] = None,
    max_pods: typing.Optional[jsii.Number] = None,
    min_node_count: typing.Optional[jsii.Number] = None,
    os: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    postinstall: typing.Optional[builtins.str] = None,
    preinstall: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    runtime: typing.Optional[builtins.str] = None,
    scale_down_cooldown_time: typing.Optional[jsii.Number] = None,
    scale_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    server_group_reference: typing.Optional[builtins.str] = None,
    storage: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodePoolV3Taints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[CceNodePoolV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907228f26e61905fb25aac4fa0997f4ccd86a856a66c871dcedcd52e07a49928(
    *,
    size: jsii.Number,
    volumetype: builtins.str,
    extend_param: typing.Optional[builtins.str] = None,
    extend_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    kms_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7c455bc904e62be7d0ce1e09dee1ed0d23a1b61e1ae0bd01c6a2b3540041a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7461c3edebc50540f24aacf2503b8e775cb14a6e17497066026f38406f14e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf80459722721cb921fb2267ad898997eebfae50c40b736bb617ab844bf4099(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18915192a94942f6c5c5c4ead92036007306b3c1456ee6d7b51cf740e731b814(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12080455cae174a5f8e1cc4ea5cdffbc9f4b5fc7c4220dc81f6f2ce77a33a2a6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd7ff23960cbd03dbb8b8ca6421a31db3a2a793f2a5877977e9fbc3f4bb665f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodePoolV3DataVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4e3c60b0ba350b75a8db10c57850d5963d014c95ce17fe59849a0003aa151f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1c5371991b456719ad74fd7a4fa15e8e4d1fbe3a08219b31da23980f4a8378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45398e8845e38abb3210bc171a6286da526df6c9a975e39e786434908a10dfba(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb54dc315c896939beab8210aa874f435cfebf0ddfba481f3f4dfe040c3cda8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e635df988fdf10ab389a4382a03f560c1fed95347276077ec87d45b6d7f8bc7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f846cab6c5e2b6d1427b842d2f277da58315dd283980389d195eb1b9cc082b69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773baab74f784deb08bea8bd5b594fb4d012db5643facc0a04f3b26fdba7b861(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodePoolV3DataVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dccf5e4fa7ef2a5c9bb7f61b245bf953731a9adb1119dac1b12df982dd0ee52b(
    *,
    size: jsii.Number,
    volumetype: builtins.str,
    extend_param: typing.Optional[builtins.str] = None,
    extend_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    kms_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2483167117089d9bc770ea9f48a39e5dbc6d325bfdf4e053a089f3e77f21a337(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fc699df2b5dfa7d389f20f1e875527aa96fc8503b73a046682265b240d38aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fb3bf63911ac5beee5b970eb631bb4807edc090dbe5bbcd90d2b553bd7ded0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ddcf9274120561c67fd27ac4bf344f5694e35fbd53679d25aeeca560777a7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc555e10639c5c0820632edcde1ecf0736a22cd907d690b4a91fd2f50d77e23b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6221ea88c7d8557a9d7522ebccad6a4a611402552c1da2ecb513ecd2d2208eec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bba7c6bca85767d5faec86c6bcf9dc34e3f20e21bd82786863d6ed781270b81(
    value: typing.Optional[CceNodePoolV3RootVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7f8e8363e827c3b7c33ce5f2640c9a184ce5112df6a9cca172cf61656426b5(
    *,
    effect: builtins.str,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad778f4a5fdef430518f7801a071956baf255a4799acd2052e8f4c780c7a5bb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1a8f316b5241f2670eb4fc7b2b323b123f2e78cfb6b0c1cfd75e8da85c2462(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f1d1e4f2a4f6eee8f6716bea3172a0fdd19786989d52c6ac0500b00df8096a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1763a51bf394ff9908c4792c16cfe19241509a82c2eb31207f692f81cd16ead2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e7897fd7b97c7285697fcb4208190d88d8350462aad39b4ced9bbd95b7c6c3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13dafab7a689a8e63eb7aa66605e130a889639ad62c4dd7c98e942bc6094f726(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodePoolV3Taints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eedf85b06f68f236369a8730c2e4b15cafb3be5c0f04f31f6169d4169f47b216(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76991452e8b6b2c1443b7c79da799145a5ed0c6596216f75354f8087f3aafaf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0692c3e5669a213b4a569cb519d62837819037b8e2cc1feff6b468aa8fd94f73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55bfe39e82a689f8ccda299ae060ac349207b5e42d742d0ea30c5dbf0e0ae5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7e0e4213e9727e556f372422369d0270d2a7fe1d763891eb05a850a481ac81(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodePoolV3Taints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eba4d3c70e1ca8860fa09427f3ba6d3871ede1c3d3fcddb9941a5f4ecc901c2(
    *,
    create: typing.Optional[builtins.str] = None,
    default: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31eb07890e159da5c570a9798b3ec81ee20f1fe9d4eac31bff16fbb040138fbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47de795ed994896e4e895270bff16832b392a1790319588277df45251c15d87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97246d4ecfadf78544a3d892d8ca420458921dd9b19f5b5a8cee2e9728a7f9a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7344950f04cb7a749258af2b1ccadb33e75db7edc258451bdfdaa7b311c863e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3c221f8ca30438623a4afc2fbde54fda155b53a4f0aa4ee6e33d8ec1300600(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b53d038373e1c4180194fa5eaeb4d6c56faf3f994c4f1be9fd43402d88d0c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodePoolV3Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
