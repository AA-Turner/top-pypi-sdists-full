r'''
# `opentelekomcloud_apigw_vpc_channel_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_apigw_vpc_channel_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2).
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


class ApigwVpcChannelV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2 opentelekomcloud_apigw_vpc_channel_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        gateway_id: builtins.str,
        lb_algorithm: jsii.Number,
        name: builtins.str,
        port: jsii.Number,
        health_check: typing.Optional[typing.Union["ApigwVpcChannelV2HealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        member: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwVpcChannelV2Member", typing.Dict[builtins.str, typing.Any]]]]] = None,
        member_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwVpcChannelV2MemberGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        member_type: typing.Optional[builtins.str] = None,
        microservice: typing.Optional[typing.Union["ApigwVpcChannelV2Microservice", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2 opentelekomcloud_apigw_vpc_channel_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#gateway_id ApigwVpcChannelV2#gateway_id}.
        :param lb_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#lb_algorithm ApigwVpcChannelV2#lb_algorithm}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#name ApigwVpcChannelV2#name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#port ApigwVpcChannelV2#port}.
        :param health_check: health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#health_check ApigwVpcChannelV2#health_check}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#id ApigwVpcChannelV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param member: member block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#member ApigwVpcChannelV2#member}
        :param member_group: member_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#member_group ApigwVpcChannelV2#member_group}
        :param member_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#member_type ApigwVpcChannelV2#member_type}.
        :param microservice: microservice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#microservice ApigwVpcChannelV2#microservice}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#type ApigwVpcChannelV2#type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac40ed6638643ef727f3203fbdd21cbf5307132dd9f8a5595d0a7730339ad511)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApigwVpcChannelV2Config(
            gateway_id=gateway_id,
            lb_algorithm=lb_algorithm,
            name=name,
            port=port,
            health_check=health_check,
            id=id,
            member=member,
            member_group=member_group,
            member_type=member_type,
            microservice=microservice,
            type=type,
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
        '''Generates CDKTF code for importing a ApigwVpcChannelV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApigwVpcChannelV2 to import.
        :param import_from_id: The id of the existing ApigwVpcChannelV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApigwVpcChannelV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c1181e688ab4523b6c86804b5a759dbd1ca501aeec0d2d690f782d12c1aff8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putHealthCheck")
    def put_health_check(
        self,
        *,
        interval: jsii.Number,
        protocol: builtins.str,
        threshold_abnormal: jsii.Number,
        threshold_normal: jsii.Number,
        timeout: jsii.Number,
        enable_client_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_codes: typing.Optional[builtins.str] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        status: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#interval ApigwVpcChannelV2#interval}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#protocol ApigwVpcChannelV2#protocol}.
        :param threshold_abnormal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#threshold_abnormal ApigwVpcChannelV2#threshold_abnormal}.
        :param threshold_normal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#threshold_normal ApigwVpcChannelV2#threshold_normal}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#timeout ApigwVpcChannelV2#timeout}.
        :param enable_client_ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#enable_client_ssl ApigwVpcChannelV2#enable_client_ssl}.
        :param http_codes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#http_codes ApigwVpcChannelV2#http_codes}.
        :param method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#method ApigwVpcChannelV2#method}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#path ApigwVpcChannelV2#path}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#port ApigwVpcChannelV2#port}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#status ApigwVpcChannelV2#status}.
        '''
        value = ApigwVpcChannelV2HealthCheck(
            interval=interval,
            protocol=protocol,
            threshold_abnormal=threshold_abnormal,
            threshold_normal=threshold_normal,
            timeout=timeout,
            enable_client_ssl=enable_client_ssl,
            http_codes=http_codes,
            method=method,
            path=path,
            port=port,
            status=status,
        )

        return typing.cast(None, jsii.invoke(self, "putHealthCheck", [value]))

    @jsii.member(jsii_name="putMember")
    def put_member(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwVpcChannelV2Member", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9d00b4a7fabf564329bd7d8b08dc25341de69ab3043ca0a7b7224ff3ab7c01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMember", [value]))

    @jsii.member(jsii_name="putMemberGroup")
    def put_member_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwVpcChannelV2MemberGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65c3e8605c91f993533cd9c4d6a63d308c56bf51e96855b3d6b07b2097ac51f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMemberGroup", [value]))

    @jsii.member(jsii_name="putMicroservice")
    def put_microservice(
        self,
        *,
        cce_config: typing.Optional[typing.Union["ApigwVpcChannelV2MicroserviceCceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cse_config: typing.Optional[typing.Union["ApigwVpcChannelV2MicroserviceCseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cce_config: cce_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#cce_config ApigwVpcChannelV2#cce_config}
        :param cse_config: cse_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#cse_config ApigwVpcChannelV2#cse_config}
        '''
        value = ApigwVpcChannelV2Microservice(
            cce_config=cce_config, cse_config=cse_config
        )

        return typing.cast(None, jsii.invoke(self, "putMicroservice", [value]))

    @jsii.member(jsii_name="resetHealthCheck")
    def reset_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheck", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMember")
    def reset_member(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMember", []))

    @jsii.member(jsii_name="resetMemberGroup")
    def reset_member_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberGroup", []))

    @jsii.member(jsii_name="resetMemberType")
    def reset_member_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemberType", []))

    @jsii.member(jsii_name="resetMicroservice")
    def reset_microservice(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicroservice", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="healthCheck")
    def health_check(self) -> "ApigwVpcChannelV2HealthCheckOutputReference":
        return typing.cast("ApigwVpcChannelV2HealthCheckOutputReference", jsii.get(self, "healthCheck"))

    @builtins.property
    @jsii.member(jsii_name="member")
    def member(self) -> "ApigwVpcChannelV2MemberList":
        return typing.cast("ApigwVpcChannelV2MemberList", jsii.get(self, "member"))

    @builtins.property
    @jsii.member(jsii_name="memberGroup")
    def member_group(self) -> "ApigwVpcChannelV2MemberGroupList":
        return typing.cast("ApigwVpcChannelV2MemberGroupList", jsii.get(self, "memberGroup"))

    @builtins.property
    @jsii.member(jsii_name="microservice")
    def microservice(self) -> "ApigwVpcChannelV2MicroserviceOutputReference":
        return typing.cast("ApigwVpcChannelV2MicroserviceOutputReference", jsii.get(self, "microservice"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="gatewayIdInput")
    def gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckInput")
    def health_check_input(self) -> typing.Optional["ApigwVpcChannelV2HealthCheck"]:
        return typing.cast(typing.Optional["ApigwVpcChannelV2HealthCheck"], jsii.get(self, "healthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lbAlgorithmInput")
    def lb_algorithm_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lbAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="memberGroupInput")
    def member_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwVpcChannelV2MemberGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwVpcChannelV2MemberGroup"]]], jsii.get(self, "memberGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="memberInput")
    def member_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwVpcChannelV2Member"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwVpcChannelV2Member"]]], jsii.get(self, "memberInput"))

    @builtins.property
    @jsii.member(jsii_name="memberTypeInput")
    def member_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memberTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="microserviceInput")
    def microservice_input(self) -> typing.Optional["ApigwVpcChannelV2Microservice"]:
        return typing.cast(typing.Optional["ApigwVpcChannelV2Microservice"], jsii.get(self, "microserviceInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayId")
    def gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayId"))

    @gateway_id.setter
    def gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089b86d23b140b503bfa66ef511e3c8749af723912ff55dde2d89b97b3148c16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6b4ea16cd6264f5ead6c473259bd171420d158dab0d145b67418660e78bd48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lbAlgorithm")
    def lb_algorithm(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lbAlgorithm"))

    @lb_algorithm.setter
    def lb_algorithm(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc48771331f882f5271491261531a7cae01d01431585b57d10728141e9ae500e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lbAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memberType")
    def member_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memberType"))

    @member_type.setter
    def member_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ca6663e1b6ddd3a9bff887e388c17065f604e07294eb3d0381ee3c8efc3bdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64abe23298ffa9e6f75fe79294939247949ea7abb1240ca72ec25273c3163d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bab6b33f60c8e80afdded67f54a08e89236a139bd6b9483ed5995c9b1db4230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "type"))

    @type.setter
    def type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c91467e1133d28e573ec100637aaf7685937bb92072f2c8f9fe690c5306251b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "gateway_id": "gatewayId",
        "lb_algorithm": "lbAlgorithm",
        "name": "name",
        "port": "port",
        "health_check": "healthCheck",
        "id": "id",
        "member": "member",
        "member_group": "memberGroup",
        "member_type": "memberType",
        "microservice": "microservice",
        "type": "type",
    },
)
class ApigwVpcChannelV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        gateway_id: builtins.str,
        lb_algorithm: jsii.Number,
        name: builtins.str,
        port: jsii.Number,
        health_check: typing.Optional[typing.Union["ApigwVpcChannelV2HealthCheck", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        member: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwVpcChannelV2Member", typing.Dict[builtins.str, typing.Any]]]]] = None,
        member_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwVpcChannelV2MemberGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        member_type: typing.Optional[builtins.str] = None,
        microservice: typing.Optional[typing.Union["ApigwVpcChannelV2Microservice", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#gateway_id ApigwVpcChannelV2#gateway_id}.
        :param lb_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#lb_algorithm ApigwVpcChannelV2#lb_algorithm}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#name ApigwVpcChannelV2#name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#port ApigwVpcChannelV2#port}.
        :param health_check: health_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#health_check ApigwVpcChannelV2#health_check}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#id ApigwVpcChannelV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param member: member block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#member ApigwVpcChannelV2#member}
        :param member_group: member_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#member_group ApigwVpcChannelV2#member_group}
        :param member_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#member_type ApigwVpcChannelV2#member_type}.
        :param microservice: microservice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#microservice ApigwVpcChannelV2#microservice}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#type ApigwVpcChannelV2#type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(health_check, dict):
            health_check = ApigwVpcChannelV2HealthCheck(**health_check)
        if isinstance(microservice, dict):
            microservice = ApigwVpcChannelV2Microservice(**microservice)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a90fc7aa9c7566689818f651c03a0f51c6e0ae0b9bbfc32f4f4b5372fcb5a2e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument gateway_id", value=gateway_id, expected_type=type_hints["gateway_id"])
            check_type(argname="argument lb_algorithm", value=lb_algorithm, expected_type=type_hints["lb_algorithm"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument member", value=member, expected_type=type_hints["member"])
            check_type(argname="argument member_group", value=member_group, expected_type=type_hints["member_group"])
            check_type(argname="argument member_type", value=member_type, expected_type=type_hints["member_type"])
            check_type(argname="argument microservice", value=microservice, expected_type=type_hints["microservice"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gateway_id": gateway_id,
            "lb_algorithm": lb_algorithm,
            "name": name,
            "port": port,
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
        if health_check is not None:
            self._values["health_check"] = health_check
        if id is not None:
            self._values["id"] = id
        if member is not None:
            self._values["member"] = member
        if member_group is not None:
            self._values["member_group"] = member_group
        if member_type is not None:
            self._values["member_type"] = member_type
        if microservice is not None:
            self._values["microservice"] = microservice
        if type is not None:
            self._values["type"] = type

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
    def gateway_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#gateway_id ApigwVpcChannelV2#gateway_id}.'''
        result = self._values.get("gateway_id")
        assert result is not None, "Required property 'gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lb_algorithm(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#lb_algorithm ApigwVpcChannelV2#lb_algorithm}.'''
        result = self._values.get("lb_algorithm")
        assert result is not None, "Required property 'lb_algorithm' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#name ApigwVpcChannelV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#port ApigwVpcChannelV2#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def health_check(self) -> typing.Optional["ApigwVpcChannelV2HealthCheck"]:
        '''health_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#health_check ApigwVpcChannelV2#health_check}
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional["ApigwVpcChannelV2HealthCheck"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#id ApigwVpcChannelV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwVpcChannelV2Member"]]]:
        '''member block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#member ApigwVpcChannelV2#member}
        '''
        result = self._values.get("member")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwVpcChannelV2Member"]]], result)

    @builtins.property
    def member_group(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwVpcChannelV2MemberGroup"]]]:
        '''member_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#member_group ApigwVpcChannelV2#member_group}
        '''
        result = self._values.get("member_group")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwVpcChannelV2MemberGroup"]]], result)

    @builtins.property
    def member_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#member_type ApigwVpcChannelV2#member_type}.'''
        result = self._values.get("member_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def microservice(self) -> typing.Optional["ApigwVpcChannelV2Microservice"]:
        '''microservice block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#microservice ApigwVpcChannelV2#microservice}
        '''
        result = self._values.get("microservice")
        return typing.cast(typing.Optional["ApigwVpcChannelV2Microservice"], result)

    @builtins.property
    def type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#type ApigwVpcChannelV2#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwVpcChannelV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2HealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "interval": "interval",
        "protocol": "protocol",
        "threshold_abnormal": "thresholdAbnormal",
        "threshold_normal": "thresholdNormal",
        "timeout": "timeout",
        "enable_client_ssl": "enableClientSsl",
        "http_codes": "httpCodes",
        "method": "method",
        "path": "path",
        "port": "port",
        "status": "status",
    },
)
class ApigwVpcChannelV2HealthCheck:
    def __init__(
        self,
        *,
        interval: jsii.Number,
        protocol: builtins.str,
        threshold_abnormal: jsii.Number,
        threshold_normal: jsii.Number,
        timeout: jsii.Number,
        enable_client_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_codes: typing.Optional[builtins.str] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        status: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#interval ApigwVpcChannelV2#interval}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#protocol ApigwVpcChannelV2#protocol}.
        :param threshold_abnormal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#threshold_abnormal ApigwVpcChannelV2#threshold_abnormal}.
        :param threshold_normal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#threshold_normal ApigwVpcChannelV2#threshold_normal}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#timeout ApigwVpcChannelV2#timeout}.
        :param enable_client_ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#enable_client_ssl ApigwVpcChannelV2#enable_client_ssl}.
        :param http_codes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#http_codes ApigwVpcChannelV2#http_codes}.
        :param method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#method ApigwVpcChannelV2#method}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#path ApigwVpcChannelV2#path}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#port ApigwVpcChannelV2#port}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#status ApigwVpcChannelV2#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__261c3de2a33117f4dc245e14d2da0d4833887b3b86da06b93fade2f29b0b1467)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument threshold_abnormal", value=threshold_abnormal, expected_type=type_hints["threshold_abnormal"])
            check_type(argname="argument threshold_normal", value=threshold_normal, expected_type=type_hints["threshold_normal"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument enable_client_ssl", value=enable_client_ssl, expected_type=type_hints["enable_client_ssl"])
            check_type(argname="argument http_codes", value=http_codes, expected_type=type_hints["http_codes"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interval": interval,
            "protocol": protocol,
            "threshold_abnormal": threshold_abnormal,
            "threshold_normal": threshold_normal,
            "timeout": timeout,
        }
        if enable_client_ssl is not None:
            self._values["enable_client_ssl"] = enable_client_ssl
        if http_codes is not None:
            self._values["http_codes"] = http_codes
        if method is not None:
            self._values["method"] = method
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#interval ApigwVpcChannelV2#interval}.'''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#protocol ApigwVpcChannelV2#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def threshold_abnormal(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#threshold_abnormal ApigwVpcChannelV2#threshold_abnormal}.'''
        result = self._values.get("threshold_abnormal")
        assert result is not None, "Required property 'threshold_abnormal' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def threshold_normal(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#threshold_normal ApigwVpcChannelV2#threshold_normal}.'''
        result = self._values.get("threshold_normal")
        assert result is not None, "Required property 'threshold_normal' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def timeout(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#timeout ApigwVpcChannelV2#timeout}.'''
        result = self._values.get("timeout")
        assert result is not None, "Required property 'timeout' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def enable_client_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#enable_client_ssl ApigwVpcChannelV2#enable_client_ssl}.'''
        result = self._values.get("enable_client_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http_codes(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#http_codes ApigwVpcChannelV2#http_codes}.'''
        result = self._values.get("http_codes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#method ApigwVpcChannelV2#method}.'''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#path ApigwVpcChannelV2#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#port ApigwVpcChannelV2#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#status ApigwVpcChannelV2#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwVpcChannelV2HealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwVpcChannelV2HealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2HealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9586978b43ec2fa78571e444bd3d7f0db5204ca27aa042f5ead066229eb15411)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableClientSsl")
    def reset_enable_client_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableClientSsl", []))

    @jsii.member(jsii_name="resetHttpCodes")
    def reset_http_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCodes", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="enableClientSslInput")
    def enable_client_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableClientSslInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCodesInput")
    def http_codes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdAbnormalInput")
    def threshold_abnormal_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdAbnormalInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdNormalInput")
    def threshold_normal_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdNormalInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="enableClientSsl")
    def enable_client_ssl(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableClientSsl"))

    @enable_client_ssl.setter
    def enable_client_ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760d2e3831432bdb25fe62370778f3bfdff8d11ccd56ee7b953d1e465fcb6f9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableClientSsl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCodes")
    def http_codes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpCodes"))

    @http_codes.setter
    def http_codes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cd24c802ad9b5d316150d13c71b8f31763c6a01c4b6b5738466d5a302a98dc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a74e891110fbb4972f36362956c4147a93d15028d48170889c5036c50367478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "method"))

    @method.setter
    def method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530171a961419d2b772b76e6bb0589f0a9b5767de3b26b6f63c4efa21a924c3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "method", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bddfa9c4990786cb2337953027a2313c38fbb5fab2c07f2cb4e95d0dbb66e92f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5195251e32895f68012979ad8338d7ec2cd1b8da03dc63ce209e680e67ac9591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e53c879be281a00018ff13137a56d34ddc97e38e5af694f09ffb791553df89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "status"))

    @status.setter
    def status(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4abd16fe9570c8b7560434b445c677579e861bc3bb085fa15f3416063879b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdAbnormal")
    def threshold_abnormal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdAbnormal"))

    @threshold_abnormal.setter
    def threshold_abnormal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aebd0a210e09129fafa661b8e7033f61d120fd1be862b15c12c6403dc2a75a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdAbnormal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdNormal")
    def threshold_normal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdNormal"))

    @threshold_normal.setter
    def threshold_normal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c28a0d28f635d17861278d38b7ddfb5bc62eeff2c4a45d0bed16f8dc678891a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdNormal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7751ca02cd2f660b2526feac42f4dfdf668d83e2852117cfdd3ae21c42b19d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigwVpcChannelV2HealthCheck]:
        return typing.cast(typing.Optional[ApigwVpcChannelV2HealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigwVpcChannelV2HealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2420bdec9c618c1990839f3e463f34204564889f215cc0418daf1fa42fcedaa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2Member",
    jsii_struct_bases=[],
    name_mapping={
        "group_name": "groupName",
        "host": "host",
        "id": "id",
        "is_backup": "isBackup",
        "name": "name",
        "port": "port",
        "status": "status",
        "weight": "weight",
    },
)
class ApigwVpcChannelV2Member:
    def __init__(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        status: typing.Optional[jsii.Number] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#group_name ApigwVpcChannelV2#group_name}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#host ApigwVpcChannelV2#host}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#id ApigwVpcChannelV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_backup: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#is_backup ApigwVpcChannelV2#is_backup}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#name ApigwVpcChannelV2#name}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#port ApigwVpcChannelV2#port}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#status ApigwVpcChannelV2#status}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#weight ApigwVpcChannelV2#weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ff7c6ee88f01776a0440ecc73f24be222d4eba7a2ac0f05cc88233e7511e3d)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_backup", value=is_backup, expected_type=type_hints["is_backup"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_name is not None:
            self._values["group_name"] = group_name
        if host is not None:
            self._values["host"] = host
        if id is not None:
            self._values["id"] = id
        if is_backup is not None:
            self._values["is_backup"] = is_backup
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if status is not None:
            self._values["status"] = status
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#group_name ApigwVpcChannelV2#group_name}.'''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#host ApigwVpcChannelV2#host}.'''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#id ApigwVpcChannelV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#is_backup ApigwVpcChannelV2#is_backup}.'''
        result = self._values.get("is_backup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#name ApigwVpcChannelV2#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#port ApigwVpcChannelV2#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#status ApigwVpcChannelV2#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#weight ApigwVpcChannelV2#weight}.'''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwVpcChannelV2Member(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2MemberGroup",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "microservice_port": "microservicePort",
        "microservice_tags": "microserviceTags",
        "microservice_version": "microserviceVersion",
        "weight": "weight",
    },
)
class ApigwVpcChannelV2MemberGroup:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        microservice_port: typing.Optional[jsii.Number] = None,
        microservice_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        microservice_version: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#name ApigwVpcChannelV2#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#description ApigwVpcChannelV2#description}.
        :param microservice_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#microservice_port ApigwVpcChannelV2#microservice_port}.
        :param microservice_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#microservice_tags ApigwVpcChannelV2#microservice_tags}.
        :param microservice_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#microservice_version ApigwVpcChannelV2#microservice_version}.
        :param weight: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#weight ApigwVpcChannelV2#weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164e8538e273469be7a0b7d9fb7df55c908647c4fb3da533c669861d19e3afeb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument microservice_port", value=microservice_port, expected_type=type_hints["microservice_port"])
            check_type(argname="argument microservice_tags", value=microservice_tags, expected_type=type_hints["microservice_tags"])
            check_type(argname="argument microservice_version", value=microservice_version, expected_type=type_hints["microservice_version"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if microservice_port is not None:
            self._values["microservice_port"] = microservice_port
        if microservice_tags is not None:
            self._values["microservice_tags"] = microservice_tags
        if microservice_version is not None:
            self._values["microservice_version"] = microservice_version
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#name ApigwVpcChannelV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#description ApigwVpcChannelV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def microservice_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#microservice_port ApigwVpcChannelV2#microservice_port}.'''
        result = self._values.get("microservice_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def microservice_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#microservice_tags ApigwVpcChannelV2#microservice_tags}.'''
        result = self._values.get("microservice_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def microservice_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#microservice_version ApigwVpcChannelV2#microservice_version}.'''
        result = self._values.get("microservice_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#weight ApigwVpcChannelV2#weight}.'''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwVpcChannelV2MemberGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwVpcChannelV2MemberGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2MemberGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64ba59387269770710c1d9cd35906f91dcbddcda1ec3c448dbf0eb2ba8b7fdd9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApigwVpcChannelV2MemberGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aecdf050777efaef66ccc08460a80e1c691c3666f2e5415e1e574e95542e2da4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwVpcChannelV2MemberGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91993b84831ff286100f2e574166308fd1ce9bd77415d91673e9ffa9a7515b7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1501819704a3c4c7322c461c7fa7b3ebd758598bf5e2bd5a46f633b2624f77c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02ae32a8e1ee48082fbc6b0961f8382783a3757df3b1d650e40a0965b72efe53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwVpcChannelV2MemberGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwVpcChannelV2MemberGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwVpcChannelV2MemberGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a605976500a365588f2f6249eac523acce16da1a1a6fc0eeabb0edb517a981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwVpcChannelV2MemberGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2MemberGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9eddf1a1eb6f1ecb0ccd61509f507b98a87496c37eeaab9abb82929f290af028)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetMicroservicePort")
    def reset_microservice_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicroservicePort", []))

    @jsii.member(jsii_name="resetMicroserviceTags")
    def reset_microservice_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicroserviceTags", []))

    @jsii.member(jsii_name="resetMicroserviceVersion")
    def reset_microservice_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicroserviceVersion", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="microservicePortInput")
    def microservice_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "microservicePortInput"))

    @builtins.property
    @jsii.member(jsii_name="microserviceTagsInput")
    def microservice_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "microserviceTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="microserviceVersionInput")
    def microservice_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "microserviceVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdbd7e7644471245c5f77a967826124c4e5cc708417da1f8c6e4372819de4885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="microservicePort")
    def microservice_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "microservicePort"))

    @microservice_port.setter
    def microservice_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e90457834deff7e2cee5a67b995aaf66ba2530ee83ff65f842c994b5afcb2b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "microservicePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="microserviceTags")
    def microservice_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "microserviceTags"))

    @microservice_tags.setter
    def microservice_tags(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb678cb66bd03a66e1e05fa2b7cc0ef8e3cadf776401c409311dd13b60b9d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "microserviceTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="microserviceVersion")
    def microservice_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "microserviceVersion"))

    @microservice_version.setter
    def microservice_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef7327ac891072f535326a1a1bd94832699c87126770dee4748866c17f5c512e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "microserviceVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49911ae7d8102bd2183815511e3c64c76b51c31a675db2c09c5bdaf26c658607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__196afd5c41699571dd53878501861e692ffc6d8e520cfc89620e9c32d90b6ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwVpcChannelV2MemberGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwVpcChannelV2MemberGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwVpcChannelV2MemberGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9bb2f6f07cd284df4a49606a751431a654885cb03ecc633b1b03f06edbef95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwVpcChannelV2MemberList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2MemberList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcb2860fd042e490c769a59395b71da9948e01e46c6f25b801b08dc237494929)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApigwVpcChannelV2MemberOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f579b36c5fa79d06d847353c62bcebc3e621ae5b5d1f6b982ea7446396ca9ae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwVpcChannelV2MemberOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a30828a42d3f488168268eed58992cff4a2272ff282bf74254edb3e411fb2435)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d39114fb5868915ae7277a463044dff7665359d1529f71b65f61c51a1fea8a0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__142dd7451a62efd43c85dd39dd27c1068b5312a1e66d2204ef5fc40c97906915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwVpcChannelV2Member]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwVpcChannelV2Member]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwVpcChannelV2Member]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00c8834737da861af870ea3bbaef54f2e3200db2935eb978f711a66494b8b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwVpcChannelV2MemberOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2MemberOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52e9ee709b84a98c5de25dd51be5541ce47ec37533d22fc46f6d3ea3bada34a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetGroupName")
    def reset_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupName", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsBackup")
    def reset_is_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsBackup", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="groupNameInput")
    def group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isBackupInput")
    def is_backup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @group_name.setter
    def group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70133bc694d2f8b3798685ca0ce4740a2f324f80b1f2e89bd2985ed9cd13ebd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4263278643ba34de639d44356850667a2bd0024554f58c1e04d9c9e7017d08f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042d41116aaaebe63e1ea7e64370a554c40188228c1cce345cdb5fd57e516740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isBackup")
    def is_backup(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isBackup"))

    @is_backup.setter
    def is_backup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9b9f6c7f1d37bca65999dd3bfc56e0ed69aaa301399001217155b22921dd29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isBackup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97e955a7fec3ea8e8446e7fc27e53f7db4016c5a89f85a51691fc1adbcab78c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d678155860794873418d70e2ec3df0a402864b38468ff384ecc7c01838aaaa7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "status"))

    @status.setter
    def status(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af8374e0131a2f4dca6471f59d8876aa7df8e1d19c056fa06cc3a80425b7f9b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbcf8bdf33d67e124732019888a4e7f293babd40bef41da45600e76886813591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwVpcChannelV2Member]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwVpcChannelV2Member]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwVpcChannelV2Member]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308fb86692b7a7635c705305810367a398bf28572aea36cc0e7abebafd9dd8bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2Microservice",
    jsii_struct_bases=[],
    name_mapping={"cce_config": "cceConfig", "cse_config": "cseConfig"},
)
class ApigwVpcChannelV2Microservice:
    def __init__(
        self,
        *,
        cce_config: typing.Optional[typing.Union["ApigwVpcChannelV2MicroserviceCceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cse_config: typing.Optional[typing.Union["ApigwVpcChannelV2MicroserviceCseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cce_config: cce_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#cce_config ApigwVpcChannelV2#cce_config}
        :param cse_config: cse_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#cse_config ApigwVpcChannelV2#cse_config}
        '''
        if isinstance(cce_config, dict):
            cce_config = ApigwVpcChannelV2MicroserviceCceConfig(**cce_config)
        if isinstance(cse_config, dict):
            cse_config = ApigwVpcChannelV2MicroserviceCseConfig(**cse_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8beb02fe5f7ee006f0cdf1d2945e8c6b18f2c3b305031a20386f0b19060c22f)
            check_type(argname="argument cce_config", value=cce_config, expected_type=type_hints["cce_config"])
            check_type(argname="argument cse_config", value=cse_config, expected_type=type_hints["cse_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cce_config is not None:
            self._values["cce_config"] = cce_config
        if cse_config is not None:
            self._values["cse_config"] = cse_config

    @builtins.property
    def cce_config(self) -> typing.Optional["ApigwVpcChannelV2MicroserviceCceConfig"]:
        '''cce_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#cce_config ApigwVpcChannelV2#cce_config}
        '''
        result = self._values.get("cce_config")
        return typing.cast(typing.Optional["ApigwVpcChannelV2MicroserviceCceConfig"], result)

    @builtins.property
    def cse_config(self) -> typing.Optional["ApigwVpcChannelV2MicroserviceCseConfig"]:
        '''cse_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#cse_config ApigwVpcChannelV2#cse_config}
        '''
        result = self._values.get("cse_config")
        return typing.cast(typing.Optional["ApigwVpcChannelV2MicroserviceCseConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwVpcChannelV2Microservice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2MicroserviceCceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_id": "clusterId",
        "namespace": "namespace",
        "workload_type": "workloadType",
        "label_key": "labelKey",
        "label_value": "labelValue",
        "workload_name": "workloadName",
    },
)
class ApigwVpcChannelV2MicroserviceCceConfig:
    def __init__(
        self,
        *,
        cluster_id: builtins.str,
        namespace: builtins.str,
        workload_type: builtins.str,
        label_key: typing.Optional[builtins.str] = None,
        label_value: typing.Optional[builtins.str] = None,
        workload_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#cluster_id ApigwVpcChannelV2#cluster_id}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#namespace ApigwVpcChannelV2#namespace}.
        :param workload_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#workload_type ApigwVpcChannelV2#workload_type}.
        :param label_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#label_key ApigwVpcChannelV2#label_key}.
        :param label_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#label_value ApigwVpcChannelV2#label_value}.
        :param workload_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#workload_name ApigwVpcChannelV2#workload_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ed27369f28496e85e8062caf711fae4899eb21ff60ea04266e1dac69b8c9a5)
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument workload_type", value=workload_type, expected_type=type_hints["workload_type"])
            check_type(argname="argument label_key", value=label_key, expected_type=type_hints["label_key"])
            check_type(argname="argument label_value", value=label_value, expected_type=type_hints["label_value"])
            check_type(argname="argument workload_name", value=workload_name, expected_type=type_hints["workload_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
            "namespace": namespace,
            "workload_type": workload_type,
        }
        if label_key is not None:
            self._values["label_key"] = label_key
        if label_value is not None:
            self._values["label_value"] = label_value
        if workload_name is not None:
            self._values["workload_name"] = workload_name

    @builtins.property
    def cluster_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#cluster_id ApigwVpcChannelV2#cluster_id}.'''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#namespace ApigwVpcChannelV2#namespace}.'''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workload_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#workload_type ApigwVpcChannelV2#workload_type}.'''
        result = self._values.get("workload_type")
        assert result is not None, "Required property 'workload_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def label_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#label_key ApigwVpcChannelV2#label_key}.'''
        result = self._values.get("label_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#label_value ApigwVpcChannelV2#label_value}.'''
        result = self._values.get("label_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workload_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#workload_name ApigwVpcChannelV2#workload_name}.'''
        result = self._values.get("workload_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwVpcChannelV2MicroserviceCceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwVpcChannelV2MicroserviceCceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2MicroserviceCceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfe41d486f63d3cb5fdde6a5f139fd755f7bdd8108844dc2580541109c6e6dec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLabelKey")
    def reset_label_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabelKey", []))

    @jsii.member(jsii_name="resetLabelValue")
    def reset_label_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabelValue", []))

    @jsii.member(jsii_name="resetWorkloadName")
    def reset_workload_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadName", []))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="labelKeyInput")
    def label_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="labelValueInput")
    def label_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelValueInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadNameInput")
    def workload_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadNameInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadTypeInput")
    def workload_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0440a79572efdbddfffc31d74542e88b064064a6983cfdae4daa97d8f8f1f143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labelKey")
    def label_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelKey"))

    @label_key.setter
    def label_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45992176454cda6a0e41412cb6b4294481cd3168ad2e58c30a0813aeccbcd919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labelValue")
    def label_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelValue"))

    @label_value.setter
    def label_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6329668299f0ae0a9963c4adcab3da5c73b4ab59c97984fc49ae54a9f57cbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d265f0446a2479038e853b936488b303abb19ffc10820caa255b8321f50e4f5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadName")
    def workload_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadName"))

    @workload_name.setter
    def workload_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d0c1b000e6c961100ead1d9761414a1a1faa40c2490060fbc759d55fc93b88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadType")
    def workload_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadType"))

    @workload_type.setter
    def workload_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d59c7906d8b6c55df931bb5f365b675a8fce4d01dd2979bda839ece2807f09b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigwVpcChannelV2MicroserviceCceConfig]:
        return typing.cast(typing.Optional[ApigwVpcChannelV2MicroserviceCceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigwVpcChannelV2MicroserviceCceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf479467d561e295e87eca0f33c859f4bf49085629244c167cf139ed86b2ca3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2MicroserviceCseConfig",
    jsii_struct_bases=[],
    name_mapping={"engine_id": "engineId", "service_id": "serviceId"},
)
class ApigwVpcChannelV2MicroserviceCseConfig:
    def __init__(self, *, engine_id: builtins.str, service_id: builtins.str) -> None:
        '''
        :param engine_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#engine_id ApigwVpcChannelV2#engine_id}.
        :param service_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#service_id ApigwVpcChannelV2#service_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83766045212722da5af7a6bda24ce826ae5bf6144d56f5e8bb38b9688833d82)
            check_type(argname="argument engine_id", value=engine_id, expected_type=type_hints["engine_id"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine_id": engine_id,
            "service_id": service_id,
        }

    @builtins.property
    def engine_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#engine_id ApigwVpcChannelV2#engine_id}.'''
        result = self._values.get("engine_id")
        assert result is not None, "Required property 'engine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#service_id ApigwVpcChannelV2#service_id}.'''
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwVpcChannelV2MicroserviceCseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwVpcChannelV2MicroserviceCseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2MicroserviceCseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41044830170bd0754b6febf2fc6190a2eff2cee1b5bb1cd8bfbd879bd54dcdff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="engineIdInput")
    def engine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineIdInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceIdInput")
    def service_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="engineId")
    def engine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "engineId"))

    @engine_id.setter
    def engine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916146cbf5846d2e52e52db7082191de28218f2a64eaca23bf32095aac98fa14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @service_id.setter
    def service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a6f10c40344164ce3c0e147588acbadeb006546df363e0c52423fb31005b26f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigwVpcChannelV2MicroserviceCseConfig]:
        return typing.cast(typing.Optional[ApigwVpcChannelV2MicroserviceCseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigwVpcChannelV2MicroserviceCseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b056a359e61e2e1913ed72ec382765148570addc366456a7eec54189b7aef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwVpcChannelV2MicroserviceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwVpcChannelV2.ApigwVpcChannelV2MicroserviceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d734328c74a590751648185ab19b9ee474ac7a370c57950c58980a643ebbd4c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCceConfig")
    def put_cce_config(
        self,
        *,
        cluster_id: builtins.str,
        namespace: builtins.str,
        workload_type: builtins.str,
        label_key: typing.Optional[builtins.str] = None,
        label_value: typing.Optional[builtins.str] = None,
        workload_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#cluster_id ApigwVpcChannelV2#cluster_id}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#namespace ApigwVpcChannelV2#namespace}.
        :param workload_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#workload_type ApigwVpcChannelV2#workload_type}.
        :param label_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#label_key ApigwVpcChannelV2#label_key}.
        :param label_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#label_value ApigwVpcChannelV2#label_value}.
        :param workload_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#workload_name ApigwVpcChannelV2#workload_name}.
        '''
        value = ApigwVpcChannelV2MicroserviceCceConfig(
            cluster_id=cluster_id,
            namespace=namespace,
            workload_type=workload_type,
            label_key=label_key,
            label_value=label_value,
            workload_name=workload_name,
        )

        return typing.cast(None, jsii.invoke(self, "putCceConfig", [value]))

    @jsii.member(jsii_name="putCseConfig")
    def put_cse_config(
        self,
        *,
        engine_id: builtins.str,
        service_id: builtins.str,
    ) -> None:
        '''
        :param engine_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#engine_id ApigwVpcChannelV2#engine_id}.
        :param service_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_vpc_channel_v2#service_id ApigwVpcChannelV2#service_id}.
        '''
        value = ApigwVpcChannelV2MicroserviceCseConfig(
            engine_id=engine_id, service_id=service_id
        )

        return typing.cast(None, jsii.invoke(self, "putCseConfig", [value]))

    @jsii.member(jsii_name="resetCceConfig")
    def reset_cce_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCceConfig", []))

    @jsii.member(jsii_name="resetCseConfig")
    def reset_cse_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCseConfig", []))

    @builtins.property
    @jsii.member(jsii_name="cceConfig")
    def cce_config(self) -> ApigwVpcChannelV2MicroserviceCceConfigOutputReference:
        return typing.cast(ApigwVpcChannelV2MicroserviceCceConfigOutputReference, jsii.get(self, "cceConfig"))

    @builtins.property
    @jsii.member(jsii_name="cseConfig")
    def cse_config(self) -> ApigwVpcChannelV2MicroserviceCseConfigOutputReference:
        return typing.cast(ApigwVpcChannelV2MicroserviceCseConfigOutputReference, jsii.get(self, "cseConfig"))

    @builtins.property
    @jsii.member(jsii_name="cceConfigInput")
    def cce_config_input(
        self,
    ) -> typing.Optional[ApigwVpcChannelV2MicroserviceCceConfig]:
        return typing.cast(typing.Optional[ApigwVpcChannelV2MicroserviceCceConfig], jsii.get(self, "cceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cseConfigInput")
    def cse_config_input(
        self,
    ) -> typing.Optional[ApigwVpcChannelV2MicroserviceCseConfig]:
        return typing.cast(typing.Optional[ApigwVpcChannelV2MicroserviceCseConfig], jsii.get(self, "cseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApigwVpcChannelV2Microservice]:
        return typing.cast(typing.Optional[ApigwVpcChannelV2Microservice], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigwVpcChannelV2Microservice],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf382449f5d6fb74629ac9591624ac7312642288296ea6430a4741de222c155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApigwVpcChannelV2",
    "ApigwVpcChannelV2Config",
    "ApigwVpcChannelV2HealthCheck",
    "ApigwVpcChannelV2HealthCheckOutputReference",
    "ApigwVpcChannelV2Member",
    "ApigwVpcChannelV2MemberGroup",
    "ApigwVpcChannelV2MemberGroupList",
    "ApigwVpcChannelV2MemberGroupOutputReference",
    "ApigwVpcChannelV2MemberList",
    "ApigwVpcChannelV2MemberOutputReference",
    "ApigwVpcChannelV2Microservice",
    "ApigwVpcChannelV2MicroserviceCceConfig",
    "ApigwVpcChannelV2MicroserviceCceConfigOutputReference",
    "ApigwVpcChannelV2MicroserviceCseConfig",
    "ApigwVpcChannelV2MicroserviceCseConfigOutputReference",
    "ApigwVpcChannelV2MicroserviceOutputReference",
]

publication.publish()

def _typecheckingstub__ac40ed6638643ef727f3203fbdd21cbf5307132dd9f8a5595d0a7730339ad511(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    gateway_id: builtins.str,
    lb_algorithm: jsii.Number,
    name: builtins.str,
    port: jsii.Number,
    health_check: typing.Optional[typing.Union[ApigwVpcChannelV2HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    member: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwVpcChannelV2Member, typing.Dict[builtins.str, typing.Any]]]]] = None,
    member_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwVpcChannelV2MemberGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    member_type: typing.Optional[builtins.str] = None,
    microservice: typing.Optional[typing.Union[ApigwVpcChannelV2Microservice, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__c7c1181e688ab4523b6c86804b5a759dbd1ca501aeec0d2d690f782d12c1aff8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9d00b4a7fabf564329bd7d8b08dc25341de69ab3043ca0a7b7224ff3ab7c01(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwVpcChannelV2Member, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65c3e8605c91f993533cd9c4d6a63d308c56bf51e96855b3d6b07b2097ac51f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwVpcChannelV2MemberGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089b86d23b140b503bfa66ef511e3c8749af723912ff55dde2d89b97b3148c16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6b4ea16cd6264f5ead6c473259bd171420d158dab0d145b67418660e78bd48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc48771331f882f5271491261531a7cae01d01431585b57d10728141e9ae500e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ca6663e1b6ddd3a9bff887e388c17065f604e07294eb3d0381ee3c8efc3bdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64abe23298ffa9e6f75fe79294939247949ea7abb1240ca72ec25273c3163d48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bab6b33f60c8e80afdded67f54a08e89236a139bd6b9483ed5995c9b1db4230(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c91467e1133d28e573ec100637aaf7685937bb92072f2c8f9fe690c5306251b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a90fc7aa9c7566689818f651c03a0f51c6e0ae0b9bbfc32f4f4b5372fcb5a2e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gateway_id: builtins.str,
    lb_algorithm: jsii.Number,
    name: builtins.str,
    port: jsii.Number,
    health_check: typing.Optional[typing.Union[ApigwVpcChannelV2HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    member: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwVpcChannelV2Member, typing.Dict[builtins.str, typing.Any]]]]] = None,
    member_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwVpcChannelV2MemberGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    member_type: typing.Optional[builtins.str] = None,
    microservice: typing.Optional[typing.Union[ApigwVpcChannelV2Microservice, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261c3de2a33117f4dc245e14d2da0d4833887b3b86da06b93fade2f29b0b1467(
    *,
    interval: jsii.Number,
    protocol: builtins.str,
    threshold_abnormal: jsii.Number,
    threshold_normal: jsii.Number,
    timeout: jsii.Number,
    enable_client_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_codes: typing.Optional[builtins.str] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    status: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9586978b43ec2fa78571e444bd3d7f0db5204ca27aa042f5ead066229eb15411(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760d2e3831432bdb25fe62370778f3bfdff8d11ccd56ee7b953d1e465fcb6f9e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd24c802ad9b5d316150d13c71b8f31763c6a01c4b6b5738466d5a302a98dc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a74e891110fbb4972f36362956c4147a93d15028d48170889c5036c50367478(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530171a961419d2b772b76e6bb0589f0a9b5767de3b26b6f63c4efa21a924c3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bddfa9c4990786cb2337953027a2313c38fbb5fab2c07f2cb4e95d0dbb66e92f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5195251e32895f68012979ad8338d7ec2cd1b8da03dc63ce209e680e67ac9591(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e53c879be281a00018ff13137a56d34ddc97e38e5af694f09ffb791553df89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4abd16fe9570c8b7560434b445c677579e861bc3bb085fa15f3416063879b9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aebd0a210e09129fafa661b8e7033f61d120fd1be862b15c12c6403dc2a75a62(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c28a0d28f635d17861278d38b7ddfb5bc62eeff2c4a45d0bed16f8dc678891a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7751ca02cd2f660b2526feac42f4dfdf668d83e2852117cfdd3ae21c42b19d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2420bdec9c618c1990839f3e463f34204564889f215cc0418daf1fa42fcedaa9(
    value: typing.Optional[ApigwVpcChannelV2HealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ff7c6ee88f01776a0440ecc73f24be222d4eba7a2ac0f05cc88233e7511e3d(
    *,
    group_name: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    status: typing.Optional[jsii.Number] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164e8538e273469be7a0b7d9fb7df55c908647c4fb3da533c669861d19e3afeb(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    microservice_port: typing.Optional[jsii.Number] = None,
    microservice_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    microservice_version: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ba59387269770710c1d9cd35906f91dcbddcda1ec3c448dbf0eb2ba8b7fdd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecdf050777efaef66ccc08460a80e1c691c3666f2e5415e1e574e95542e2da4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91993b84831ff286100f2e574166308fd1ce9bd77415d91673e9ffa9a7515b7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1501819704a3c4c7322c461c7fa7b3ebd758598bf5e2bd5a46f633b2624f77c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ae32a8e1ee48082fbc6b0961f8382783a3757df3b1d650e40a0965b72efe53(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a605976500a365588f2f6249eac523acce16da1a1a6fc0eeabb0edb517a981(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwVpcChannelV2MemberGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eddf1a1eb6f1ecb0ccd61509f507b98a87496c37eeaab9abb82929f290af028(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbd7e7644471245c5f77a967826124c4e5cc708417da1f8c6e4372819de4885(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e90457834deff7e2cee5a67b995aaf66ba2530ee83ff65f842c994b5afcb2b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb678cb66bd03a66e1e05fa2b7cc0ef8e3cadf776401c409311dd13b60b9d6a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7327ac891072f535326a1a1bd94832699c87126770dee4748866c17f5c512e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49911ae7d8102bd2183815511e3c64c76b51c31a675db2c09c5bdaf26c658607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196afd5c41699571dd53878501861e692ffc6d8e520cfc89620e9c32d90b6ac3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9bb2f6f07cd284df4a49606a751431a654885cb03ecc633b1b03f06edbef95(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwVpcChannelV2MemberGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb2860fd042e490c769a59395b71da9948e01e46c6f25b801b08dc237494929(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f579b36c5fa79d06d847353c62bcebc3e621ae5b5d1f6b982ea7446396ca9ae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30828a42d3f488168268eed58992cff4a2272ff282bf74254edb3e411fb2435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39114fb5868915ae7277a463044dff7665359d1529f71b65f61c51a1fea8a0a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142dd7451a62efd43c85dd39dd27c1068b5312a1e66d2204ef5fc40c97906915(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00c8834737da861af870ea3bbaef54f2e3200db2935eb978f711a66494b8b8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwVpcChannelV2Member]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e9ee709b84a98c5de25dd51be5541ce47ec37533d22fc46f6d3ea3bada34a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70133bc694d2f8b3798685ca0ce4740a2f324f80b1f2e89bd2985ed9cd13ebd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4263278643ba34de639d44356850667a2bd0024554f58c1e04d9c9e7017d08f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042d41116aaaebe63e1ea7e64370a554c40188228c1cce345cdb5fd57e516740(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9b9f6c7f1d37bca65999dd3bfc56e0ed69aaa301399001217155b22921dd29(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e955a7fec3ea8e8446e7fc27e53f7db4016c5a89f85a51691fc1adbcab78c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d678155860794873418d70e2ec3df0a402864b38468ff384ecc7c01838aaaa7f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8374e0131a2f4dca6471f59d8876aa7df8e1d19c056fa06cc3a80425b7f9b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbcf8bdf33d67e124732019888a4e7f293babd40bef41da45600e76886813591(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308fb86692b7a7635c705305810367a398bf28572aea36cc0e7abebafd9dd8bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwVpcChannelV2Member]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8beb02fe5f7ee006f0cdf1d2945e8c6b18f2c3b305031a20386f0b19060c22f(
    *,
    cce_config: typing.Optional[typing.Union[ApigwVpcChannelV2MicroserviceCceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cse_config: typing.Optional[typing.Union[ApigwVpcChannelV2MicroserviceCseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ed27369f28496e85e8062caf711fae4899eb21ff60ea04266e1dac69b8c9a5(
    *,
    cluster_id: builtins.str,
    namespace: builtins.str,
    workload_type: builtins.str,
    label_key: typing.Optional[builtins.str] = None,
    label_value: typing.Optional[builtins.str] = None,
    workload_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe41d486f63d3cb5fdde6a5f139fd755f7bdd8108844dc2580541109c6e6dec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0440a79572efdbddfffc31d74542e88b064064a6983cfdae4daa97d8f8f1f143(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45992176454cda6a0e41412cb6b4294481cd3168ad2e58c30a0813aeccbcd919(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6329668299f0ae0a9963c4adcab3da5c73b4ab59c97984fc49ae54a9f57cbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d265f0446a2479038e853b936488b303abb19ffc10820caa255b8321f50e4f5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d0c1b000e6c961100ead1d9761414a1a1faa40c2490060fbc759d55fc93b88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d59c7906d8b6c55df931bb5f365b675a8fce4d01dd2979bda839ece2807f09b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf479467d561e295e87eca0f33c859f4bf49085629244c167cf139ed86b2ca3c(
    value: typing.Optional[ApigwVpcChannelV2MicroserviceCceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83766045212722da5af7a6bda24ce826ae5bf6144d56f5e8bb38b9688833d82(
    *,
    engine_id: builtins.str,
    service_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41044830170bd0754b6febf2fc6190a2eff2cee1b5bb1cd8bfbd879bd54dcdff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916146cbf5846d2e52e52db7082191de28218f2a64eaca23bf32095aac98fa14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6f10c40344164ce3c0e147588acbadeb006546df363e0c52423fb31005b26f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b056a359e61e2e1913ed72ec382765148570addc366456a7eec54189b7aef8(
    value: typing.Optional[ApigwVpcChannelV2MicroserviceCseConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d734328c74a590751648185ab19b9ee474ac7a370c57950c58980a643ebbd4c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf382449f5d6fb74629ac9591624ac7312642288296ea6430a4741de222c155(
    value: typing.Optional[ApigwVpcChannelV2Microservice],
) -> None:
    """Type checking stubs"""
    pass
