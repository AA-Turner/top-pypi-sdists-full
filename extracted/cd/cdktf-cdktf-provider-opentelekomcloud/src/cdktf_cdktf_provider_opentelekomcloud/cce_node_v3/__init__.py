r'''
# `opentelekomcloud_cce_node_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_cce_node_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3).
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


class CceNodeV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3 opentelekomcloud_cce_node_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zone: builtins.str,
        cluster_id: builtins.str,
        data_volumes: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeV3DataVolumes", typing.Dict[builtins.str, typing.Any]]]],
        flavor_id: builtins.str,
        key_pair: builtins.str,
        root_volume: typing.Union["CceNodeV3RootVolume", typing.Dict[builtins.str, typing.Any]],
        agency_name: typing.Optional[builtins.str] = None,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bandwidth_charge_mode: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        billing_mode: typing.Optional[jsii.Number] = None,
        dedicated_host_id: typing.Optional[builtins.str] = None,
        docker_base_size: typing.Optional[jsii.Number] = None,
        docker_lvm_config_override: typing.Optional[builtins.str] = None,
        ecs_performance_type: typing.Optional[builtins.str] = None,
        eip_count: typing.Optional[jsii.Number] = None,
        eip_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        extend_param_charging_mode: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        iptype: typing.Optional[builtins.str] = None,
        k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        order_id: typing.Optional[builtins.str] = None,
        os: typing.Optional[builtins.str] = None,
        postinstall: typing.Optional[builtins.str] = None,
        preinstall: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        public_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        sharetype: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeV3Taints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CceNodeV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3 opentelekomcloud_cce_node_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#availability_zone CceNodeV3#availability_zone}.
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#cluster_id CceNodeV3#cluster_id}.
        :param data_volumes: data_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#data_volumes CceNodeV3#data_volumes}
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#flavor_id CceNodeV3#flavor_id}.
        :param key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#key_pair CceNodeV3#key_pair}.
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#root_volume CceNodeV3#root_volume}
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#agency_name CceNodeV3#agency_name}.
        :param annotations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#annotations CceNodeV3#annotations}.
        :param bandwidth_charge_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#bandwidth_charge_mode CceNodeV3#bandwidth_charge_mode}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#bandwidth_size CceNodeV3#bandwidth_size}.
        :param billing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#billing_mode CceNodeV3#billing_mode}.
        :param dedicated_host_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#dedicated_host_id CceNodeV3#dedicated_host_id}.
        :param docker_base_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#docker_base_size CceNodeV3#docker_base_size}.
        :param docker_lvm_config_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#docker_lvm_config_override CceNodeV3#docker_lvm_config_override}.
        :param ecs_performance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#ecs_performance_type CceNodeV3#ecs_performance_type}.
        :param eip_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#eip_count CceNodeV3#eip_count}.
        :param eip_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#eip_ids CceNodeV3#eip_ids}.
        :param extend_param_charging_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_param_charging_mode CceNodeV3#extend_param_charging_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#id CceNodeV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iptype: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#iptype CceNodeV3#iptype}.
        :param k8_s_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#k8s_tags CceNodeV3#k8s_tags}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#labels CceNodeV3#labels}.
        :param max_pods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#max_pods CceNodeV3#max_pods}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#name CceNodeV3#name}.
        :param order_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#order_id CceNodeV3#order_id}.
        :param os: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#os CceNodeV3#os}.
        :param postinstall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#postinstall CceNodeV3#postinstall}.
        :param preinstall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#preinstall CceNodeV3#preinstall}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#private_ip CceNodeV3#private_ip}.
        :param product_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#product_id CceNodeV3#product_id}.
        :param public_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#public_key CceNodeV3#public_key}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#region CceNodeV3#region}.
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#runtime CceNodeV3#runtime}.
        :param sharetype: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#sharetype CceNodeV3#sharetype}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#subnet_id CceNodeV3#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#tags CceNodeV3#tags}.
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#taints CceNodeV3#taints}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#timeouts CceNodeV3#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed3eaf2d4f7d4400b33eb6f20affe5f70a5d85d4e17dcfa68f00410e09073bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CceNodeV3Config(
            availability_zone=availability_zone,
            cluster_id=cluster_id,
            data_volumes=data_volumes,
            flavor_id=flavor_id,
            key_pair=key_pair,
            root_volume=root_volume,
            agency_name=agency_name,
            annotations=annotations,
            bandwidth_charge_mode=bandwidth_charge_mode,
            bandwidth_size=bandwidth_size,
            billing_mode=billing_mode,
            dedicated_host_id=dedicated_host_id,
            docker_base_size=docker_base_size,
            docker_lvm_config_override=docker_lvm_config_override,
            ecs_performance_type=ecs_performance_type,
            eip_count=eip_count,
            eip_ids=eip_ids,
            extend_param_charging_mode=extend_param_charging_mode,
            id=id,
            iptype=iptype,
            k8_s_tags=k8_s_tags,
            labels=labels,
            max_pods=max_pods,
            name=name,
            order_id=order_id,
            os=os,
            postinstall=postinstall,
            preinstall=preinstall,
            private_ip=private_ip,
            product_id=product_id,
            public_key=public_key,
            region=region,
            runtime=runtime,
            sharetype=sharetype,
            subnet_id=subnet_id,
            tags=tags,
            taints=taints,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a CceNodeV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CceNodeV3 to import.
        :param import_from_id: The id of the existing CceNodeV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CceNodeV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21535fafe1c72cdd08216199608a9bc77ad0536086cb3fdea7ff567a918a6e0c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataVolumes")
    def put_data_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeV3DataVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cee5f10554f858fffd5bf30cc023378575242f2548d20b250c31dc6d870642c)
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
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#size CceNodeV3#size}.
        :param volumetype: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#volumetype CceNodeV3#volumetype}.
        :param extend_param: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_param CceNodeV3#extend_param}.
        :param extend_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_params CceNodeV3#extend_params}.
        :param kms_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#kms_id CceNodeV3#kms_id}.
        '''
        value = CceNodeV3RootVolume(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeV3Taints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__add6b6bf8703b0024fdc304763041d239325648a25658b47fa8d47514cd6745b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaints", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#create CceNodeV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#delete CceNodeV3#delete}.
        '''
        value = CceNodeV3Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAgencyName")
    def reset_agency_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgencyName", []))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetBandwidthChargeMode")
    def reset_bandwidth_charge_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthChargeMode", []))

    @jsii.member(jsii_name="resetBandwidthSize")
    def reset_bandwidth_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthSize", []))

    @jsii.member(jsii_name="resetBillingMode")
    def reset_billing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBillingMode", []))

    @jsii.member(jsii_name="resetDedicatedHostId")
    def reset_dedicated_host_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedHostId", []))

    @jsii.member(jsii_name="resetDockerBaseSize")
    def reset_docker_base_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerBaseSize", []))

    @jsii.member(jsii_name="resetDockerLvmConfigOverride")
    def reset_docker_lvm_config_override(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerLvmConfigOverride", []))

    @jsii.member(jsii_name="resetEcsPerformanceType")
    def reset_ecs_performance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEcsPerformanceType", []))

    @jsii.member(jsii_name="resetEipCount")
    def reset_eip_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEipCount", []))

    @jsii.member(jsii_name="resetEipIds")
    def reset_eip_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEipIds", []))

    @jsii.member(jsii_name="resetExtendParamChargingMode")
    def reset_extend_param_charging_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendParamChargingMode", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIptype")
    def reset_iptype(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIptype", []))

    @jsii.member(jsii_name="resetK8STags")
    def reset_k8_s_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetK8STags", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaxPods")
    def reset_max_pods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPods", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOrderId")
    def reset_order_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrderId", []))

    @jsii.member(jsii_name="resetOs")
    def reset_os(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOs", []))

    @jsii.member(jsii_name="resetPostinstall")
    def reset_postinstall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostinstall", []))

    @jsii.member(jsii_name="resetPreinstall")
    def reset_preinstall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreinstall", []))

    @jsii.member(jsii_name="resetPrivateIp")
    def reset_private_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIp", []))

    @jsii.member(jsii_name="resetProductId")
    def reset_product_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProductId", []))

    @jsii.member(jsii_name="resetPublicKey")
    def reset_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicKey", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRuntime")
    def reset_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntime", []))

    @jsii.member(jsii_name="resetSharetype")
    def reset_sharetype(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharetype", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTaints")
    def reset_taints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaints", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    def data_volumes(self) -> "CceNodeV3DataVolumesList":
        return typing.cast("CceNodeV3DataVolumesList", jsii.get(self, "dataVolumes"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="rootVolume")
    def root_volume(self) -> "CceNodeV3RootVolumeOutputReference":
        return typing.cast("CceNodeV3RootVolumeOutputReference", jsii.get(self, "rootVolume"))

    @builtins.property
    @jsii.member(jsii_name="serverId")
    def server_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverId"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(self) -> "CceNodeV3TaintsList":
        return typing.cast("CceNodeV3TaintsList", jsii.get(self, "taints"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CceNodeV3TimeoutsOutputReference":
        return typing.cast("CceNodeV3TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="agencyNameInput")
    def agency_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthChargeModeInput")
    def bandwidth_charge_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthChargeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthSizeInput")
    def bandwidth_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="billingModeInput")
    def billing_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "billingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataVolumesInput")
    def data_volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeV3DataVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeV3DataVolumes"]]], jsii.get(self, "dataVolumesInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedHostIdInput")
    def dedicated_host_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dedicatedHostIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerBaseSizeInput")
    def docker_base_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dockerBaseSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerLvmConfigOverrideInput")
    def docker_lvm_config_override_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerLvmConfigOverrideInput"))

    @builtins.property
    @jsii.member(jsii_name="ecsPerformanceTypeInput")
    def ecs_performance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ecsPerformanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="eipCountInput")
    def eip_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "eipCountInput"))

    @builtins.property
    @jsii.member(jsii_name="eipIdsInput")
    def eip_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eipIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="extendParamChargingModeInput")
    def extend_param_charging_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "extendParamChargingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorIdInput")
    def flavor_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flavorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="iptypeInput")
    def iptype_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iptypeInput"))

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
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsInput")
    def max_pods_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orderIdInput")
    def order_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderIdInput"))

    @builtins.property
    @jsii.member(jsii_name="osInput")
    def os_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osInput"))

    @builtins.property
    @jsii.member(jsii_name="postinstallInput")
    def postinstall_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postinstallInput"))

    @builtins.property
    @jsii.member(jsii_name="preinstallInput")
    def preinstall_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preinstallInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpInput")
    def private_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpInput"))

    @builtins.property
    @jsii.member(jsii_name="productIdInput")
    def product_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productIdInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeyInput")
    def public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="rootVolumeInput")
    def root_volume_input(self) -> typing.Optional["CceNodeV3RootVolume"]:
        return typing.cast(typing.Optional["CceNodeV3RootVolume"], jsii.get(self, "rootVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="sharetypeInput")
    def sharetype_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharetypeInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeV3Taints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeV3Taints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CceNodeV3Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CceNodeV3Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="agencyName")
    def agency_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agencyName"))

    @agency_name.setter
    def agency_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a28a4c23aaa568a2b1fe72ca1a588b514858f131b1d9e1fd7cee3c1e70958f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agencyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2541c3d3a50450b847bf867ca109f49ea8d903c1a49901b9ae30fbc7738365d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868ad33b3989c3ed6aa8ce464edef710bee97d8b175acded23253083510dbe86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidthChargeMode")
    def bandwidth_charge_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthChargeMode"))

    @bandwidth_charge_mode.setter
    def bandwidth_charge_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce355152364ab3022c9ce243752fc5a8e1f25e9737bc9ac1d83338c4c4679bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthChargeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidthSize")
    def bandwidth_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthSize"))

    @bandwidth_size.setter
    def bandwidth_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b049a8cc053dc6b6e81286735433676c58390a9f9573eb91b01e4873f2c054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="billingMode")
    def billing_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "billingMode"))

    @billing_mode.setter
    def billing_mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3c909d7f99ba2146c5fdda45b97561b1ce359fb5b8c82cca000b4784b0a8a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "billingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e094ae6e5591ac0b3141c85854626c7af7d8037ed10765ae4409fd6a7702ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dedicatedHostId")
    def dedicated_host_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dedicatedHostId"))

    @dedicated_host_id.setter
    def dedicated_host_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8afdcdfde165e0d952c5c42c8cd4beed351e047da47938ab4b8842eca289e147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicatedHostId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerBaseSize")
    def docker_base_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dockerBaseSize"))

    @docker_base_size.setter
    def docker_base_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2c488605337caa2de30a7312dbdba867b8ce35be32c8957f9ca0042d88fe56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerBaseSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerLvmConfigOverride")
    def docker_lvm_config_override(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerLvmConfigOverride"))

    @docker_lvm_config_override.setter
    def docker_lvm_config_override(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463d64023cdbfceae4d7ab531938bed012ebe06a6a940561e586d10807b94c5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerLvmConfigOverride", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ecsPerformanceType")
    def ecs_performance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ecsPerformanceType"))

    @ecs_performance_type.setter
    def ecs_performance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1132961c1b88e06bf00725d564280b95b78c36e98f798f870ed514089e20850c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ecsPerformanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eipCount")
    def eip_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "eipCount"))

    @eip_count.setter
    def eip_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102b9412a10f41bb2fc6761501fae98ac9d0c07bcd24c93ec0d1b91a6a2f77e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eipCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eipIds")
    def eip_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eipIds"))

    @eip_ids.setter
    def eip_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912e14d925c05bba0615e1be653aebf0b87d071d0e058361b4bc51e447bbf1c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eipIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extendParamChargingMode")
    def extend_param_charging_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "extendParamChargingMode"))

    @extend_param_charging_mode.setter
    def extend_param_charging_mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d24537ea1c1f6d13b7812fc8f198fd9bb1cf963c23877970a927548a94fdd9c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParamChargingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flavorId")
    def flavor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorId"))

    @flavor_id.setter
    def flavor_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67bb60a0d9494c373190837b5b7819cf9e7258fef9a674a7601b1fd4f5bb85ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flavorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1198481933d2e2cb034759962c7b649a3aaf57adee4cc4fa8874b8fc641de997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iptype")
    def iptype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iptype"))

    @iptype.setter
    def iptype(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12747dbaad23f254aef23601bc9ab8ea398e19d7a2e665076b884d1c4c9c3f0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iptype", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="k8STags")
    def k8_s_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "k8STags"))

    @k8_s_tags.setter
    def k8_s_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a722d908b4a9e1a13869f51ebf7527bed09116d367e787563cce5933caf52b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "k8STags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyPair")
    def key_pair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPair"))

    @key_pair.setter
    def key_pair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c867bbaa68e71692d652e883d47f557b5dc6eca294c2cc30ccc78ae2522df9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0741453b597879571765ca3e44aa701feb49e4866da5a41e923c8c5036c4cc46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPods")
    def max_pods(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPods"))

    @max_pods.setter
    def max_pods(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07bd37459bd9bdb8c2b0e67e48ee940ea298518855b8e13a633af5de2ef391da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88258692bd79acef79c37cfc68fdc502e67d600d1a82ec774092a66f3063cc6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orderId")
    def order_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orderId"))

    @order_id.setter
    def order_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d3a7f1df7505b0f3de9302d3101c6ad7ce5a3e71467b73dd1cbae06bc06bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orderId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="os")
    def os(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "os"))

    @os.setter
    def os(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab4b53fed15eee638143cc7577d570d3c37c922529ea057a289dbcba1dd8c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "os", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postinstall")
    def postinstall(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postinstall"))

    @postinstall.setter
    def postinstall(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ecee2d410c1a0b68163fba2418a1fa43cf5e1114f123ec392e229fef0b6d7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postinstall", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preinstall")
    def preinstall(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preinstall"))

    @preinstall.setter
    def preinstall(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5358e1ab42ea753b9df1171c111a752fc235468515a7945dde4a01d080fa5aa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preinstall", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @private_ip.setter
    def private_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed39712407e540f7a0def7bb9bb3896eaa0caeae3fe15a072b888e60b4681edc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="productId")
    def product_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "productId"))

    @product_id.setter
    def product_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58f85226c1577b3dc73f6574c7a7e05891b364fb4a6a695abe093078b3ea6b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @public_key.setter
    def public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88eb737cbf606c3bab9a08ca870e8cd2b90f00d16fb4d4caf853d9187c7c8a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788d1c79687c2b79ecaf2f7338e7a1e890e909fe538e0e67131959046017d156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b11c3451f5b5a961be2f3b40f29f93217fea97c9c6528b080200cacbee7909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharetype")
    def sharetype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharetype"))

    @sharetype.setter
    def sharetype(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb2a48c5734c91b6462d1d548a8c2b7a8ae375c8f36e8fcfe0aa2f92409bc18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharetype", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe8872d551956156d97573366ec7dc325c9127fba9def1af043d589d7d22a8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c05f9bb84106c2fe34303d158fa9be08e098a3915af115decab0e4bee23050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zone": "availabilityZone",
        "cluster_id": "clusterId",
        "data_volumes": "dataVolumes",
        "flavor_id": "flavorId",
        "key_pair": "keyPair",
        "root_volume": "rootVolume",
        "agency_name": "agencyName",
        "annotations": "annotations",
        "bandwidth_charge_mode": "bandwidthChargeMode",
        "bandwidth_size": "bandwidthSize",
        "billing_mode": "billingMode",
        "dedicated_host_id": "dedicatedHostId",
        "docker_base_size": "dockerBaseSize",
        "docker_lvm_config_override": "dockerLvmConfigOverride",
        "ecs_performance_type": "ecsPerformanceType",
        "eip_count": "eipCount",
        "eip_ids": "eipIds",
        "extend_param_charging_mode": "extendParamChargingMode",
        "id": "id",
        "iptype": "iptype",
        "k8_s_tags": "k8STags",
        "labels": "labels",
        "max_pods": "maxPods",
        "name": "name",
        "order_id": "orderId",
        "os": "os",
        "postinstall": "postinstall",
        "preinstall": "preinstall",
        "private_ip": "privateIp",
        "product_id": "productId",
        "public_key": "publicKey",
        "region": "region",
        "runtime": "runtime",
        "sharetype": "sharetype",
        "subnet_id": "subnetId",
        "tags": "tags",
        "taints": "taints",
        "timeouts": "timeouts",
    },
)
class CceNodeV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zone: builtins.str,
        cluster_id: builtins.str,
        data_volumes: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeV3DataVolumes", typing.Dict[builtins.str, typing.Any]]]],
        flavor_id: builtins.str,
        key_pair: builtins.str,
        root_volume: typing.Union["CceNodeV3RootVolume", typing.Dict[builtins.str, typing.Any]],
        agency_name: typing.Optional[builtins.str] = None,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        bandwidth_charge_mode: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        billing_mode: typing.Optional[jsii.Number] = None,
        dedicated_host_id: typing.Optional[builtins.str] = None,
        docker_base_size: typing.Optional[jsii.Number] = None,
        docker_lvm_config_override: typing.Optional[builtins.str] = None,
        ecs_performance_type: typing.Optional[builtins.str] = None,
        eip_count: typing.Optional[jsii.Number] = None,
        eip_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        extend_param_charging_mode: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        iptype: typing.Optional[builtins.str] = None,
        k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        order_id: typing.Optional[builtins.str] = None,
        os: typing.Optional[builtins.str] = None,
        postinstall: typing.Optional[builtins.str] = None,
        preinstall: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        public_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        sharetype: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeV3Taints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CceNodeV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#availability_zone CceNodeV3#availability_zone}.
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#cluster_id CceNodeV3#cluster_id}.
        :param data_volumes: data_volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#data_volumes CceNodeV3#data_volumes}
        :param flavor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#flavor_id CceNodeV3#flavor_id}.
        :param key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#key_pair CceNodeV3#key_pair}.
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#root_volume CceNodeV3#root_volume}
        :param agency_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#agency_name CceNodeV3#agency_name}.
        :param annotations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#annotations CceNodeV3#annotations}.
        :param bandwidth_charge_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#bandwidth_charge_mode CceNodeV3#bandwidth_charge_mode}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#bandwidth_size CceNodeV3#bandwidth_size}.
        :param billing_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#billing_mode CceNodeV3#billing_mode}.
        :param dedicated_host_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#dedicated_host_id CceNodeV3#dedicated_host_id}.
        :param docker_base_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#docker_base_size CceNodeV3#docker_base_size}.
        :param docker_lvm_config_override: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#docker_lvm_config_override CceNodeV3#docker_lvm_config_override}.
        :param ecs_performance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#ecs_performance_type CceNodeV3#ecs_performance_type}.
        :param eip_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#eip_count CceNodeV3#eip_count}.
        :param eip_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#eip_ids CceNodeV3#eip_ids}.
        :param extend_param_charging_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_param_charging_mode CceNodeV3#extend_param_charging_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#id CceNodeV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iptype: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#iptype CceNodeV3#iptype}.
        :param k8_s_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#k8s_tags CceNodeV3#k8s_tags}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#labels CceNodeV3#labels}.
        :param max_pods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#max_pods CceNodeV3#max_pods}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#name CceNodeV3#name}.
        :param order_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#order_id CceNodeV3#order_id}.
        :param os: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#os CceNodeV3#os}.
        :param postinstall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#postinstall CceNodeV3#postinstall}.
        :param preinstall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#preinstall CceNodeV3#preinstall}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#private_ip CceNodeV3#private_ip}.
        :param product_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#product_id CceNodeV3#product_id}.
        :param public_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#public_key CceNodeV3#public_key}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#region CceNodeV3#region}.
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#runtime CceNodeV3#runtime}.
        :param sharetype: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#sharetype CceNodeV3#sharetype}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#subnet_id CceNodeV3#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#tags CceNodeV3#tags}.
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#taints CceNodeV3#taints}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#timeouts CceNodeV3#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(root_volume, dict):
            root_volume = CceNodeV3RootVolume(**root_volume)
        if isinstance(timeouts, dict):
            timeouts = CceNodeV3Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb692bb67543358844c3922b0114f9bb01735f54bde0818ba55809e0e1caecae)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument data_volumes", value=data_volumes, expected_type=type_hints["data_volumes"])
            check_type(argname="argument flavor_id", value=flavor_id, expected_type=type_hints["flavor_id"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument root_volume", value=root_volume, expected_type=type_hints["root_volume"])
            check_type(argname="argument agency_name", value=agency_name, expected_type=type_hints["agency_name"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument bandwidth_charge_mode", value=bandwidth_charge_mode, expected_type=type_hints["bandwidth_charge_mode"])
            check_type(argname="argument bandwidth_size", value=bandwidth_size, expected_type=type_hints["bandwidth_size"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument dedicated_host_id", value=dedicated_host_id, expected_type=type_hints["dedicated_host_id"])
            check_type(argname="argument docker_base_size", value=docker_base_size, expected_type=type_hints["docker_base_size"])
            check_type(argname="argument docker_lvm_config_override", value=docker_lvm_config_override, expected_type=type_hints["docker_lvm_config_override"])
            check_type(argname="argument ecs_performance_type", value=ecs_performance_type, expected_type=type_hints["ecs_performance_type"])
            check_type(argname="argument eip_count", value=eip_count, expected_type=type_hints["eip_count"])
            check_type(argname="argument eip_ids", value=eip_ids, expected_type=type_hints["eip_ids"])
            check_type(argname="argument extend_param_charging_mode", value=extend_param_charging_mode, expected_type=type_hints["extend_param_charging_mode"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument iptype", value=iptype, expected_type=type_hints["iptype"])
            check_type(argname="argument k8_s_tags", value=k8_s_tags, expected_type=type_hints["k8_s_tags"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument max_pods", value=max_pods, expected_type=type_hints["max_pods"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument order_id", value=order_id, expected_type=type_hints["order_id"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument postinstall", value=postinstall, expected_type=type_hints["postinstall"])
            check_type(argname="argument preinstall", value=preinstall, expected_type=type_hints["preinstall"])
            check_type(argname="argument private_ip", value=private_ip, expected_type=type_hints["private_ip"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument sharetype", value=sharetype, expected_type=type_hints["sharetype"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone": availability_zone,
            "cluster_id": cluster_id,
            "data_volumes": data_volumes,
            "flavor_id": flavor_id,
            "key_pair": key_pair,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if bandwidth_charge_mode is not None:
            self._values["bandwidth_charge_mode"] = bandwidth_charge_mode
        if bandwidth_size is not None:
            self._values["bandwidth_size"] = bandwidth_size
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if dedicated_host_id is not None:
            self._values["dedicated_host_id"] = dedicated_host_id
        if docker_base_size is not None:
            self._values["docker_base_size"] = docker_base_size
        if docker_lvm_config_override is not None:
            self._values["docker_lvm_config_override"] = docker_lvm_config_override
        if ecs_performance_type is not None:
            self._values["ecs_performance_type"] = ecs_performance_type
        if eip_count is not None:
            self._values["eip_count"] = eip_count
        if eip_ids is not None:
            self._values["eip_ids"] = eip_ids
        if extend_param_charging_mode is not None:
            self._values["extend_param_charging_mode"] = extend_param_charging_mode
        if id is not None:
            self._values["id"] = id
        if iptype is not None:
            self._values["iptype"] = iptype
        if k8_s_tags is not None:
            self._values["k8_s_tags"] = k8_s_tags
        if labels is not None:
            self._values["labels"] = labels
        if max_pods is not None:
            self._values["max_pods"] = max_pods
        if name is not None:
            self._values["name"] = name
        if order_id is not None:
            self._values["order_id"] = order_id
        if os is not None:
            self._values["os"] = os
        if postinstall is not None:
            self._values["postinstall"] = postinstall
        if preinstall is not None:
            self._values["preinstall"] = preinstall
        if private_ip is not None:
            self._values["private_ip"] = private_ip
        if product_id is not None:
            self._values["product_id"] = product_id
        if public_key is not None:
            self._values["public_key"] = public_key
        if region is not None:
            self._values["region"] = region
        if runtime is not None:
            self._values["runtime"] = runtime
        if sharetype is not None:
            self._values["sharetype"] = sharetype
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tags is not None:
            self._values["tags"] = tags
        if taints is not None:
            self._values["taints"] = taints
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def availability_zone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#availability_zone CceNodeV3#availability_zone}.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#cluster_id CceNodeV3#cluster_id}.'''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_volumes(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeV3DataVolumes"]]:
        '''data_volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#data_volumes CceNodeV3#data_volumes}
        '''
        result = self._values.get("data_volumes")
        assert result is not None, "Required property 'data_volumes' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeV3DataVolumes"]], result)

    @builtins.property
    def flavor_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#flavor_id CceNodeV3#flavor_id}.'''
        result = self._values.get("flavor_id")
        assert result is not None, "Required property 'flavor_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_pair(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#key_pair CceNodeV3#key_pair}.'''
        result = self._values.get("key_pair")
        assert result is not None, "Required property 'key_pair' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_volume(self) -> "CceNodeV3RootVolume":
        '''root_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#root_volume CceNodeV3#root_volume}
        '''
        result = self._values.get("root_volume")
        assert result is not None, "Required property 'root_volume' is missing"
        return typing.cast("CceNodeV3RootVolume", result)

    @builtins.property
    def agency_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#agency_name CceNodeV3#agency_name}.'''
        result = self._values.get("agency_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#annotations CceNodeV3#annotations}.'''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def bandwidth_charge_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#bandwidth_charge_mode CceNodeV3#bandwidth_charge_mode}.'''
        result = self._values.get("bandwidth_charge_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bandwidth_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#bandwidth_size CceNodeV3#bandwidth_size}.'''
        result = self._values.get("bandwidth_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def billing_mode(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#billing_mode CceNodeV3#billing_mode}.'''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dedicated_host_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#dedicated_host_id CceNodeV3#dedicated_host_id}.'''
        result = self._values.get("dedicated_host_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_base_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#docker_base_size CceNodeV3#docker_base_size}.'''
        result = self._values.get("docker_base_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_lvm_config_override(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#docker_lvm_config_override CceNodeV3#docker_lvm_config_override}.'''
        result = self._values.get("docker_lvm_config_override")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecs_performance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#ecs_performance_type CceNodeV3#ecs_performance_type}.'''
        result = self._values.get("ecs_performance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eip_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#eip_count CceNodeV3#eip_count}.'''
        result = self._values.get("eip_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def eip_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#eip_ids CceNodeV3#eip_ids}.'''
        result = self._values.get("eip_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def extend_param_charging_mode(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_param_charging_mode CceNodeV3#extend_param_charging_mode}.'''
        result = self._values.get("extend_param_charging_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#id CceNodeV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iptype(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#iptype CceNodeV3#iptype}.'''
        result = self._values.get("iptype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def k8_s_tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#k8s_tags CceNodeV3#k8s_tags}.'''
        result = self._values.get("k8_s_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#labels CceNodeV3#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_pods(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#max_pods CceNodeV3#max_pods}.'''
        result = self._values.get("max_pods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#name CceNodeV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#order_id CceNodeV3#order_id}.'''
        result = self._values.get("order_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#os CceNodeV3#os}.'''
        result = self._values.get("os")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postinstall(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#postinstall CceNodeV3#postinstall}.'''
        result = self._values.get("postinstall")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preinstall(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#preinstall CceNodeV3#preinstall}.'''
        result = self._values.get("preinstall")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#private_ip CceNodeV3#private_ip}.'''
        result = self._values.get("private_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#product_id CceNodeV3#product_id}.'''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#public_key CceNodeV3#public_key}.'''
        result = self._values.get("public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#region CceNodeV3#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#runtime CceNodeV3#runtime}.'''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sharetype(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#sharetype CceNodeV3#sharetype}.'''
        result = self._values.get("sharetype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#subnet_id CceNodeV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#tags CceNodeV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeV3Taints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#taints CceNodeV3#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeV3Taints"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CceNodeV3Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#timeouts CceNodeV3#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CceNodeV3Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3DataVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "size": "size",
        "volumetype": "volumetype",
        "extend_param": "extendParam",
        "extend_params": "extendParams",
        "kms_id": "kmsId",
    },
)
class CceNodeV3DataVolumes:
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
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#size CceNodeV3#size}.
        :param volumetype: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#volumetype CceNodeV3#volumetype}.
        :param extend_param: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_param CceNodeV3#extend_param}.
        :param extend_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_params CceNodeV3#extend_params}.
        :param kms_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#kms_id CceNodeV3#kms_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af43670dd4f0e569d78a88e139ce69e42d61dc0628ca9228622d07269810fd2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#size CceNodeV3#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volumetype(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#volumetype CceNodeV3#volumetype}.'''
        result = self._values.get("volumetype")
        assert result is not None, "Required property 'volumetype' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def extend_param(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_param CceNodeV3#extend_param}.'''
        result = self._values.get("extend_param")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extend_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_params CceNodeV3#extend_params}.'''
        result = self._values.get("extend_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def kms_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#kms_id CceNodeV3#kms_id}.'''
        result = self._values.get("kms_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeV3DataVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeV3DataVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3DataVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c28aeba6b9af95afe598da799bdfa11a1973c522d4ce7d4a6ce66df3dcd68295)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CceNodeV3DataVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01091bbfb3d47ae615c3c944a0a64a6ef4416dba1ef794e64ee0cd952df505f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceNodeV3DataVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7a5ea316b98cf72fe0b386dbb52144874d0d2552e3186e6c51cb77dc23d64e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c9a7639ffce1fbf248806be468eaaa1334cfb3eeb1cd4ca781d861d9bfb1533)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce7e5c27c2b5ded3e2b3d6ec49e8ec9d0a149d07236aa626990890712e627455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeV3DataVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeV3DataVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeV3DataVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9542f5837c9ccabd4edebd9da015c2019a83e426d510f6517750b6c458fee7b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CceNodeV3DataVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3DataVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d986b92f3d205d8daf8e0d20eb494952edc8a453b7d0b52d8e80768bdc94f7f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2eb15eaa034d34249f4eb00e1177728dfaa456a0e3408b6e288cc02cfaf006d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParam", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extendParams")
    def extend_params(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extendParams"))

    @extend_params.setter
    def extend_params(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5daf12c5c1200376ff36bf8aca46f9ec6871e0ef526d928dae5457e048e5a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsId")
    def kms_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsId"))

    @kms_id.setter
    def kms_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b871ecac475053f9246d3951ce98d4dc8ea6b7113db4db7e7483c9eb600279f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__866408a0d0d91074bca7855ef10e7ba5cb9b28577ba19445b1ee46abf41d7eda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumetype")
    def volumetype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumetype"))

    @volumetype.setter
    def volumetype(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1eb5d958e1fd8f5bb9c03e542efd3b0a8ce63953efdb6e3e296fa773a8b30e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumetype", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeV3DataVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeV3DataVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeV3DataVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf985642b9e96ddf481f9832e6e547c3c5194c80d1552b117456aea8a59b72ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3RootVolume",
    jsii_struct_bases=[],
    name_mapping={
        "size": "size",
        "volumetype": "volumetype",
        "extend_param": "extendParam",
        "extend_params": "extendParams",
        "kms_id": "kmsId",
    },
)
class CceNodeV3RootVolume:
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
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#size CceNodeV3#size}.
        :param volumetype: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#volumetype CceNodeV3#volumetype}.
        :param extend_param: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_param CceNodeV3#extend_param}.
        :param extend_params: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_params CceNodeV3#extend_params}.
        :param kms_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#kms_id CceNodeV3#kms_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d68e11d017c11913aef23ac35e325e088a6b31b8970b3ffbef7ca51be240ca)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#size CceNodeV3#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volumetype(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#volumetype CceNodeV3#volumetype}.'''
        result = self._values.get("volumetype")
        assert result is not None, "Required property 'volumetype' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def extend_param(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_param CceNodeV3#extend_param}.'''
        result = self._values.get("extend_param")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extend_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#extend_params CceNodeV3#extend_params}.'''
        result = self._values.get("extend_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def kms_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#kms_id CceNodeV3#kms_id}.'''
        result = self._values.get("kms_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeV3RootVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeV3RootVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3RootVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d377456c3fd2339d626f098d56f3f8b5357937e9d56cf98f6fcd0d648f7d0cd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a8291613040ec1937b575c1fc9e8284a10c9c02222f0a0530b2e0cb91b04e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParam", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extendParams")
    def extend_params(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "extendParams"))

    @extend_params.setter
    def extend_params(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612f9c340531d3984da1fb71b6a1755ebd920bc34df9999d8d50270b9be52bf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendParams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsId")
    def kms_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsId"))

    @kms_id.setter
    def kms_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25a97ac08c13d9dea1b7ba63d4e2668376502cdf0bfa277d4c3abba68160d6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6565d6c1d9a7e831c22115a2efea536deebff3bd25db346ebe9b2b37dfad698e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumetype")
    def volumetype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumetype"))

    @volumetype.setter
    def volumetype(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2176022624e8a6314abd1fcc5fb3967a8c835d65e04a6f31a4b01251d9d6306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumetype", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CceNodeV3RootVolume]:
        return typing.cast(typing.Optional[CceNodeV3RootVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CceNodeV3RootVolume]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3c35e396ce549a84946e9d076a9c52aa421fee53bc46b9a9574ec3559a4fa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3Taints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class CceNodeV3Taints:
    def __init__(
        self,
        *,
        effect: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param effect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#effect CceNodeV3#effect}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#key CceNodeV3#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#value CceNodeV3#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5229743c58f1e844dcd5f1c490d7b1b657414263d5d0eac8555c43d6ec849feb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#effect CceNodeV3#effect}.'''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#key CceNodeV3#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#value CceNodeV3#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeV3Taints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeV3TaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3TaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b8bc03766bba07bc9294269f8668cc69dc6439435df7e1a2b6884a137531caa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CceNodeV3TaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8af5abf8627d3664c0f85a7d3e9f9b834c9db67b4630199e8ee3eccf8866d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceNodeV3TaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9082ffc491f6213091ac12e26262745c39134f53f3940e9a147383d8eb61f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0f96ba86c18a57325e0b9da674dadb0b8dcb997e628ee101c2f46bb7dea94bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29aca1c9c6c97a5ca60d696432df74ffced982e6d01670259a4f156f1131942b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeV3Taints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeV3Taints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeV3Taints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dfa256aed961999a272483dd81340e4dcb2ba0fc2f17e9cbdcf7bb8b09b16f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CceNodeV3TaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3TaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c92dd1110a5e36115f8b9578f1ca0efb30c465a3bae85523e743c32a2c78047)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01c92a565dfe96c235ea6073355623127888912502b8971faedb227216e813c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b431bb9c9ec751e6d39c0b1e73218df4f1773c5f7de1c55eff876a0ba6be7633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1813aa20924c65a681b8be84f44dad650de38baf6c2cba80b35351d149f2346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeV3Taints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeV3Taints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeV3Taints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056aa56d8049dbfde23433e80cb04e5275aa0e88258308277c3a00b357b4b8d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class CceNodeV3Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#create CceNodeV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#delete CceNodeV3#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c6202e3cf382c17269a6a96a06de6bdb7e470d436566a0252b986f135f2f88)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#create CceNodeV3#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_v3#delete CceNodeV3#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeV3Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeV3TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeV3.CceNodeV3TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bea73ef265d97f8c6ec1832165a6e281d46abb1cda04c801f368151265aeaba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57bf9e66f99b8b2484b621e5b5fecffe5d576f7baec2da721c7fb89651834129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31207c8e6a9c8a5eb34edacf9cd5ff2c598770a4bc702b36c4d52476bf023c1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeV3Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeV3Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeV3Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b4cc934059df72cd819c5b0c329ad2ea4db31f5bb00cce9c6390c1004a34fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CceNodeV3",
    "CceNodeV3Config",
    "CceNodeV3DataVolumes",
    "CceNodeV3DataVolumesList",
    "CceNodeV3DataVolumesOutputReference",
    "CceNodeV3RootVolume",
    "CceNodeV3RootVolumeOutputReference",
    "CceNodeV3Taints",
    "CceNodeV3TaintsList",
    "CceNodeV3TaintsOutputReference",
    "CceNodeV3Timeouts",
    "CceNodeV3TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5ed3eaf2d4f7d4400b33eb6f20affe5f70a5d85d4e17dcfa68f00410e09073bd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zone: builtins.str,
    cluster_id: builtins.str,
    data_volumes: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeV3DataVolumes, typing.Dict[builtins.str, typing.Any]]]],
    flavor_id: builtins.str,
    key_pair: builtins.str,
    root_volume: typing.Union[CceNodeV3RootVolume, typing.Dict[builtins.str, typing.Any]],
    agency_name: typing.Optional[builtins.str] = None,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bandwidth_charge_mode: typing.Optional[builtins.str] = None,
    bandwidth_size: typing.Optional[jsii.Number] = None,
    billing_mode: typing.Optional[jsii.Number] = None,
    dedicated_host_id: typing.Optional[builtins.str] = None,
    docker_base_size: typing.Optional[jsii.Number] = None,
    docker_lvm_config_override: typing.Optional[builtins.str] = None,
    ecs_performance_type: typing.Optional[builtins.str] = None,
    eip_count: typing.Optional[jsii.Number] = None,
    eip_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    extend_param_charging_mode: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    iptype: typing.Optional[builtins.str] = None,
    k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_pods: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    order_id: typing.Optional[builtins.str] = None,
    os: typing.Optional[builtins.str] = None,
    postinstall: typing.Optional[builtins.str] = None,
    preinstall: typing.Optional[builtins.str] = None,
    private_ip: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
    public_key: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    sharetype: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeV3Taints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[CceNodeV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__21535fafe1c72cdd08216199608a9bc77ad0536086cb3fdea7ff567a918a6e0c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cee5f10554f858fffd5bf30cc023378575242f2548d20b250c31dc6d870642c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeV3DataVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add6b6bf8703b0024fdc304763041d239325648a25658b47fa8d47514cd6745b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeV3Taints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a28a4c23aaa568a2b1fe72ca1a588b514858f131b1d9e1fd7cee3c1e70958f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2541c3d3a50450b847bf867ca109f49ea8d903c1a49901b9ae30fbc7738365d0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868ad33b3989c3ed6aa8ce464edef710bee97d8b175acded23253083510dbe86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce355152364ab3022c9ce243752fc5a8e1f25e9737bc9ac1d83338c4c4679bed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b049a8cc053dc6b6e81286735433676c58390a9f9573eb91b01e4873f2c054(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3c909d7f99ba2146c5fdda45b97561b1ce359fb5b8c82cca000b4784b0a8a7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e094ae6e5591ac0b3141c85854626c7af7d8037ed10765ae4409fd6a7702ae5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afdcdfde165e0d952c5c42c8cd4beed351e047da47938ab4b8842eca289e147(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2c488605337caa2de30a7312dbdba867b8ce35be32c8957f9ca0042d88fe56(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463d64023cdbfceae4d7ab531938bed012ebe06a6a940561e586d10807b94c5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1132961c1b88e06bf00725d564280b95b78c36e98f798f870ed514089e20850c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102b9412a10f41bb2fc6761501fae98ac9d0c07bcd24c93ec0d1b91a6a2f77e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912e14d925c05bba0615e1be653aebf0b87d071d0e058361b4bc51e447bbf1c3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d24537ea1c1f6d13b7812fc8f198fd9bb1cf963c23877970a927548a94fdd9c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67bb60a0d9494c373190837b5b7819cf9e7258fef9a674a7601b1fd4f5bb85ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1198481933d2e2cb034759962c7b649a3aaf57adee4cc4fa8874b8fc641de997(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12747dbaad23f254aef23601bc9ab8ea398e19d7a2e665076b884d1c4c9c3f0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a722d908b4a9e1a13869f51ebf7527bed09116d367e787563cce5933caf52b6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c867bbaa68e71692d652e883d47f557b5dc6eca294c2cc30ccc78ae2522df9cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0741453b597879571765ca3e44aa701feb49e4866da5a41e923c8c5036c4cc46(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07bd37459bd9bdb8c2b0e67e48ee940ea298518855b8e13a633af5de2ef391da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88258692bd79acef79c37cfc68fdc502e67d600d1a82ec774092a66f3063cc6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d3a7f1df7505b0f3de9302d3101c6ad7ce5a3e71467b73dd1cbae06bc06bdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab4b53fed15eee638143cc7577d570d3c37c922529ea057a289dbcba1dd8c5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ecee2d410c1a0b68163fba2418a1fa43cf5e1114f123ec392e229fef0b6d7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5358e1ab42ea753b9df1171c111a752fc235468515a7945dde4a01d080fa5aa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed39712407e540f7a0def7bb9bb3896eaa0caeae3fe15a072b888e60b4681edc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58f85226c1577b3dc73f6574c7a7e05891b364fb4a6a695abe093078b3ea6b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88eb737cbf606c3bab9a08ca870e8cd2b90f00d16fb4d4caf853d9187c7c8a5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788d1c79687c2b79ecaf2f7338e7a1e890e909fe538e0e67131959046017d156(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b11c3451f5b5a961be2f3b40f29f93217fea97c9c6528b080200cacbee7909(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb2a48c5734c91b6462d1d548a8c2b7a8ae375c8f36e8fcfe0aa2f92409bc18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe8872d551956156d97573366ec7dc325c9127fba9def1af043d589d7d22a8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c05f9bb84106c2fe34303d158fa9be08e098a3915af115decab0e4bee23050(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb692bb67543358844c3922b0114f9bb01735f54bde0818ba55809e0e1caecae(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zone: builtins.str,
    cluster_id: builtins.str,
    data_volumes: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeV3DataVolumes, typing.Dict[builtins.str, typing.Any]]]],
    flavor_id: builtins.str,
    key_pair: builtins.str,
    root_volume: typing.Union[CceNodeV3RootVolume, typing.Dict[builtins.str, typing.Any]],
    agency_name: typing.Optional[builtins.str] = None,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    bandwidth_charge_mode: typing.Optional[builtins.str] = None,
    bandwidth_size: typing.Optional[jsii.Number] = None,
    billing_mode: typing.Optional[jsii.Number] = None,
    dedicated_host_id: typing.Optional[builtins.str] = None,
    docker_base_size: typing.Optional[jsii.Number] = None,
    docker_lvm_config_override: typing.Optional[builtins.str] = None,
    ecs_performance_type: typing.Optional[builtins.str] = None,
    eip_count: typing.Optional[jsii.Number] = None,
    eip_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    extend_param_charging_mode: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    iptype: typing.Optional[builtins.str] = None,
    k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_pods: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    order_id: typing.Optional[builtins.str] = None,
    os: typing.Optional[builtins.str] = None,
    postinstall: typing.Optional[builtins.str] = None,
    preinstall: typing.Optional[builtins.str] = None,
    private_ip: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
    public_key: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    sharetype: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeV3Taints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[CceNodeV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af43670dd4f0e569d78a88e139ce69e42d61dc0628ca9228622d07269810fd2(
    *,
    size: jsii.Number,
    volumetype: builtins.str,
    extend_param: typing.Optional[builtins.str] = None,
    extend_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    kms_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28aeba6b9af95afe598da799bdfa11a1973c522d4ce7d4a6ce66df3dcd68295(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01091bbfb3d47ae615c3c944a0a64a6ef4416dba1ef794e64ee0cd952df505f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7a5ea316b98cf72fe0b386dbb52144874d0d2552e3186e6c51cb77dc23d64e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9a7639ffce1fbf248806be468eaaa1334cfb3eeb1cd4ca781d861d9bfb1533(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7e5c27c2b5ded3e2b3d6ec49e8ec9d0a149d07236aa626990890712e627455(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9542f5837c9ccabd4edebd9da015c2019a83e426d510f6517750b6c458fee7b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeV3DataVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d986b92f3d205d8daf8e0d20eb494952edc8a453b7d0b52d8e80768bdc94f7f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb15eaa034d34249f4eb00e1177728dfaa456a0e3408b6e288cc02cfaf006d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5daf12c5c1200376ff36bf8aca46f9ec6871e0ef526d928dae5457e048e5a5d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b871ecac475053f9246d3951ce98d4dc8ea6b7113db4db7e7483c9eb600279f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866408a0d0d91074bca7855ef10e7ba5cb9b28577ba19445b1ee46abf41d7eda(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1eb5d958e1fd8f5bb9c03e542efd3b0a8ce63953efdb6e3e296fa773a8b30e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf985642b9e96ddf481f9832e6e547c3c5194c80d1552b117456aea8a59b72ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeV3DataVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d68e11d017c11913aef23ac35e325e088a6b31b8970b3ffbef7ca51be240ca(
    *,
    size: jsii.Number,
    volumetype: builtins.str,
    extend_param: typing.Optional[builtins.str] = None,
    extend_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    kms_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d377456c3fd2339d626f098d56f3f8b5357937e9d56cf98f6fcd0d648f7d0cd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8291613040ec1937b575c1fc9e8284a10c9c02222f0a0530b2e0cb91b04e2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612f9c340531d3984da1fb71b6a1755ebd920bc34df9999d8d50270b9be52bf5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25a97ac08c13d9dea1b7ba63d4e2668376502cdf0bfa277d4c3abba68160d6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6565d6c1d9a7e831c22115a2efea536deebff3bd25db346ebe9b2b37dfad698e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2176022624e8a6314abd1fcc5fb3967a8c835d65e04a6f31a4b01251d9d6306(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3c35e396ce549a84946e9d076a9c52aa421fee53bc46b9a9574ec3559a4fa5(
    value: typing.Optional[CceNodeV3RootVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5229743c58f1e844dcd5f1c490d7b1b657414263d5d0eac8555c43d6ec849feb(
    *,
    effect: builtins.str,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8bc03766bba07bc9294269f8668cc69dc6439435df7e1a2b6884a137531caa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8af5abf8627d3664c0f85a7d3e9f9b834c9db67b4630199e8ee3eccf8866d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9082ffc491f6213091ac12e26262745c39134f53f3940e9a147383d8eb61f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f96ba86c18a57325e0b9da674dadb0b8dcb997e628ee101c2f46bb7dea94bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29aca1c9c6c97a5ca60d696432df74ffced982e6d01670259a4f156f1131942b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfa256aed961999a272483dd81340e4dcb2ba0fc2f17e9cbdcf7bb8b09b16f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeV3Taints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c92dd1110a5e36115f8b9578f1ca0efb30c465a3bae85523e743c32a2c78047(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c92a565dfe96c235ea6073355623127888912502b8971faedb227216e813c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b431bb9c9ec751e6d39c0b1e73218df4f1773c5f7de1c55eff876a0ba6be7633(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1813aa20924c65a681b8be84f44dad650de38baf6c2cba80b35351d149f2346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056aa56d8049dbfde23433e80cb04e5275aa0e88258308277c3a00b357b4b8d6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeV3Taints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c6202e3cf382c17269a6a96a06de6bdb7e470d436566a0252b986f135f2f88(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bea73ef265d97f8c6ec1832165a6e281d46abb1cda04c801f368151265aeaba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57bf9e66f99b8b2484b621e5b5fecffe5d576f7baec2da721c7fb89651834129(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31207c8e6a9c8a5eb34edacf9cd5ff2c598770a4bc702b36c4d52476bf023c1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b4cc934059df72cd819c5b0c329ad2ea4db31f5bb00cce9c6390c1004a34fe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeV3Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
