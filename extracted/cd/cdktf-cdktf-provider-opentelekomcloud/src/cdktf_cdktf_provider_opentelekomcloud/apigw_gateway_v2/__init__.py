r'''
# `opentelekomcloud_apigw_gateway_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_apigw_gateway_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2).
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


class ApigwGatewayV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwGatewayV2.ApigwGatewayV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2 opentelekomcloud_apigw_gateway_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zones: typing.Sequence[builtins.str],
        name: builtins.str,
        security_group_id: builtins.str,
        spec_id: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        bandwidth_charging_mode: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        enterprise_project_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ingress_bandwidth_charging_mode: typing.Optional[builtins.str] = None,
        ingress_bandwidth_size: typing.Optional[jsii.Number] = None,
        loadbalancer_provider: typing.Optional[builtins.str] = None,
        maintain_begin: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApigwGatewayV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2 opentelekomcloud_apigw_gateway_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#availability_zones ApigwGatewayV2#availability_zones}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#name ApigwGatewayV2#name}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#security_group_id ApigwGatewayV2#security_group_id}.
        :param spec_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#spec_id ApigwGatewayV2#spec_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#subnet_id ApigwGatewayV2#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#vpc_id ApigwGatewayV2#vpc_id}.
        :param bandwidth_charging_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#bandwidth_charging_mode ApigwGatewayV2#bandwidth_charging_mode}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#bandwidth_size ApigwGatewayV2#bandwidth_size}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#description ApigwGatewayV2#description}.
        :param enterprise_project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#enterprise_project_id ApigwGatewayV2#enterprise_project_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#id ApigwGatewayV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress_bandwidth_charging_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#ingress_bandwidth_charging_mode ApigwGatewayV2#ingress_bandwidth_charging_mode}.
        :param ingress_bandwidth_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#ingress_bandwidth_size ApigwGatewayV2#ingress_bandwidth_size}.
        :param loadbalancer_provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#loadbalancer_provider ApigwGatewayV2#loadbalancer_provider}.
        :param maintain_begin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#maintain_begin ApigwGatewayV2#maintain_begin}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#timeouts ApigwGatewayV2#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f2d003d3d8af3e8032970b81dedecb566047ea1e71839342594de7e5f7e6d1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApigwGatewayV2Config(
            availability_zones=availability_zones,
            name=name,
            security_group_id=security_group_id,
            spec_id=spec_id,
            subnet_id=subnet_id,
            vpc_id=vpc_id,
            bandwidth_charging_mode=bandwidth_charging_mode,
            bandwidth_size=bandwidth_size,
            description=description,
            enterprise_project_id=enterprise_project_id,
            id=id,
            ingress_bandwidth_charging_mode=ingress_bandwidth_charging_mode,
            ingress_bandwidth_size=ingress_bandwidth_size,
            loadbalancer_provider=loadbalancer_provider,
            maintain_begin=maintain_begin,
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
        '''Generates CDKTF code for importing a ApigwGatewayV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApigwGatewayV2 to import.
        :param import_from_id: The id of the existing ApigwGatewayV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApigwGatewayV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa4a63195af0036d63bcb2722d243f02169ae54ad214653e4fb07cafe822fd4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#create ApigwGatewayV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#delete ApigwGatewayV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#update ApigwGatewayV2#update}.
        '''
        value = ApigwGatewayV2Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBandwidthChargingMode")
    def reset_bandwidth_charging_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthChargingMode", []))

    @jsii.member(jsii_name="resetBandwidthSize")
    def reset_bandwidth_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthSize", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnterpriseProjectId")
    def reset_enterprise_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnterpriseProjectId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIngressBandwidthChargingMode")
    def reset_ingress_bandwidth_charging_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressBandwidthChargingMode", []))

    @jsii.member(jsii_name="resetIngressBandwidthSize")
    def reset_ingress_bandwidth_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressBandwidthSize", []))

    @jsii.member(jsii_name="resetLoadbalancerProvider")
    def reset_loadbalancer_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadbalancerProvider", []))

    @jsii.member(jsii_name="resetMaintainBegin")
    def reset_maintain_begin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainBegin", []))

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
    @jsii.member(jsii_name="maintainEnd")
    def maintain_end(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainEnd"))

    @builtins.property
    @jsii.member(jsii_name="privateEgressAddresses")
    def private_egress_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privateEgressAddresses"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="publicEgressAddress")
    def public_egress_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicEgressAddress"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="supportedFeatures")
    def supported_features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedFeatures"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApigwGatewayV2TimeoutsOutputReference":
        return typing.cast("ApigwGatewayV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcepServiceName")
    def vpcep_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcepServiceName"))

    @builtins.property
    @jsii.member(jsii_name="vpcIngressAddress")
    def vpc_ingress_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcIngressAddress"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZonesInput")
    def availability_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthChargingModeInput")
    def bandwidth_charging_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthChargingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthSizeInput")
    def bandwidth_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseProjectIdInput")
    def enterprise_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enterpriseProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressBandwidthChargingModeInput")
    def ingress_bandwidth_charging_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ingressBandwidthChargingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressBandwidthSizeInput")
    def ingress_bandwidth_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ingressBandwidthSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="loadbalancerProviderInput")
    def loadbalancer_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadbalancerProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="maintainBeginInput")
    def maintain_begin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintainBeginInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdInput")
    def security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="specIdInput")
    def spec_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "specIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigwGatewayV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigwGatewayV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea978bfa18c7eaad29e73da80afbdbda5fa73730a632042f6ba0d2bb92a7655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidthChargingMode")
    def bandwidth_charging_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthChargingMode"))

    @bandwidth_charging_mode.setter
    def bandwidth_charging_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb88166944583f446c6d7ae90dc0cb7d6d6feb84843d2628785769a1c58097cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthChargingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidthSize")
    def bandwidth_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthSize"))

    @bandwidth_size.setter
    def bandwidth_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4d13109958ccc1034eed7d7b03ec2dfe839fff2084c750bf5e8414633e8ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d6a14ac8988ae78b3149889c2f96e1f862a4825ad46fa6f162420ef5c19f90a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enterpriseProjectId")
    def enterprise_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enterpriseProjectId"))

    @enterprise_project_id.setter
    def enterprise_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f76d247bef5646012e8a42a3c640aa2a6a0f57b545a020e9d917e6fbc3e276b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterpriseProjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff47ac872e46c96647e38b8bc480f9f43d44ab9a89b8423351da914be6ec812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressBandwidthChargingMode")
    def ingress_bandwidth_charging_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressBandwidthChargingMode"))

    @ingress_bandwidth_charging_mode.setter
    def ingress_bandwidth_charging_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ea2bb7e8db1073cac3939d9b1ef5c477d6e4c674d61300e3f16b072643c3f02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressBandwidthChargingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingressBandwidthSize")
    def ingress_bandwidth_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressBandwidthSize"))

    @ingress_bandwidth_size.setter
    def ingress_bandwidth_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1f9ce2f0b7e7e5e8b0b464ebb0a2b396546c1044763fb35556340b5c1eb110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressBandwidthSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadbalancerProvider")
    def loadbalancer_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadbalancerProvider"))

    @loadbalancer_provider.setter
    def loadbalancer_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64cc39b1a3ba5ace22548660cf870c602190935eec5fb4c99e1bfaa41837c5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadbalancerProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainBegin")
    def maintain_begin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainBegin"))

    @maintain_begin.setter
    def maintain_begin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3d8964e065cb20259ef8cb57464e8130cc7c880c8ce961994ed5d54e4a7408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainBegin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10621dbdc1e1250d2ccfd7eb3c7011d81c92aaf3f0dd8071118b1fdc074ee77d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3247fb274366afa2d8082f6eb4ca653c02f6250eba33f9f40b6902d04431bf65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="specId")
    def spec_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "specId"))

    @spec_id.setter
    def spec_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f49aad259676192e01dc1506c6e2c38ab3e5a66eb83854a1429585a1c6fdac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "specId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2e43201bd21d7228618b90e19498817753ad463e8b4587f7a448f942d5380b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a92ab0b4c6da694e52f47d8b12f15ee001a049c9c536e89dae9ddb4c623964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwGatewayV2.ApigwGatewayV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zones": "availabilityZones",
        "name": "name",
        "security_group_id": "securityGroupId",
        "spec_id": "specId",
        "subnet_id": "subnetId",
        "vpc_id": "vpcId",
        "bandwidth_charging_mode": "bandwidthChargingMode",
        "bandwidth_size": "bandwidthSize",
        "description": "description",
        "enterprise_project_id": "enterpriseProjectId",
        "id": "id",
        "ingress_bandwidth_charging_mode": "ingressBandwidthChargingMode",
        "ingress_bandwidth_size": "ingressBandwidthSize",
        "loadbalancer_provider": "loadbalancerProvider",
        "maintain_begin": "maintainBegin",
        "timeouts": "timeouts",
    },
)
class ApigwGatewayV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zones: typing.Sequence[builtins.str],
        name: builtins.str,
        security_group_id: builtins.str,
        spec_id: builtins.str,
        subnet_id: builtins.str,
        vpc_id: builtins.str,
        bandwidth_charging_mode: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        enterprise_project_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ingress_bandwidth_charging_mode: typing.Optional[builtins.str] = None,
        ingress_bandwidth_size: typing.Optional[jsii.Number] = None,
        loadbalancer_provider: typing.Optional[builtins.str] = None,
        maintain_begin: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApigwGatewayV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#availability_zones ApigwGatewayV2#availability_zones}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#name ApigwGatewayV2#name}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#security_group_id ApigwGatewayV2#security_group_id}.
        :param spec_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#spec_id ApigwGatewayV2#spec_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#subnet_id ApigwGatewayV2#subnet_id}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#vpc_id ApigwGatewayV2#vpc_id}.
        :param bandwidth_charging_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#bandwidth_charging_mode ApigwGatewayV2#bandwidth_charging_mode}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#bandwidth_size ApigwGatewayV2#bandwidth_size}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#description ApigwGatewayV2#description}.
        :param enterprise_project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#enterprise_project_id ApigwGatewayV2#enterprise_project_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#id ApigwGatewayV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress_bandwidth_charging_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#ingress_bandwidth_charging_mode ApigwGatewayV2#ingress_bandwidth_charging_mode}.
        :param ingress_bandwidth_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#ingress_bandwidth_size ApigwGatewayV2#ingress_bandwidth_size}.
        :param loadbalancer_provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#loadbalancer_provider ApigwGatewayV2#loadbalancer_provider}.
        :param maintain_begin: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#maintain_begin ApigwGatewayV2#maintain_begin}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#timeouts ApigwGatewayV2#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ApigwGatewayV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300f66f70de76f9bf3070a06177ae87f6fdec756b80374bd168a922f8e81012b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument spec_id", value=spec_id, expected_type=type_hints["spec_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument bandwidth_charging_mode", value=bandwidth_charging_mode, expected_type=type_hints["bandwidth_charging_mode"])
            check_type(argname="argument bandwidth_size", value=bandwidth_size, expected_type=type_hints["bandwidth_size"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enterprise_project_id", value=enterprise_project_id, expected_type=type_hints["enterprise_project_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ingress_bandwidth_charging_mode", value=ingress_bandwidth_charging_mode, expected_type=type_hints["ingress_bandwidth_charging_mode"])
            check_type(argname="argument ingress_bandwidth_size", value=ingress_bandwidth_size, expected_type=type_hints["ingress_bandwidth_size"])
            check_type(argname="argument loadbalancer_provider", value=loadbalancer_provider, expected_type=type_hints["loadbalancer_provider"])
            check_type(argname="argument maintain_begin", value=maintain_begin, expected_type=type_hints["maintain_begin"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zones": availability_zones,
            "name": name,
            "security_group_id": security_group_id,
            "spec_id": spec_id,
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
        if bandwidth_charging_mode is not None:
            self._values["bandwidth_charging_mode"] = bandwidth_charging_mode
        if bandwidth_size is not None:
            self._values["bandwidth_size"] = bandwidth_size
        if description is not None:
            self._values["description"] = description
        if enterprise_project_id is not None:
            self._values["enterprise_project_id"] = enterprise_project_id
        if id is not None:
            self._values["id"] = id
        if ingress_bandwidth_charging_mode is not None:
            self._values["ingress_bandwidth_charging_mode"] = ingress_bandwidth_charging_mode
        if ingress_bandwidth_size is not None:
            self._values["ingress_bandwidth_size"] = ingress_bandwidth_size
        if loadbalancer_provider is not None:
            self._values["loadbalancer_provider"] = loadbalancer_provider
        if maintain_begin is not None:
            self._values["maintain_begin"] = maintain_begin
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
    def availability_zones(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#availability_zones ApigwGatewayV2#availability_zones}.'''
        result = self._values.get("availability_zones")
        assert result is not None, "Required property 'availability_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#name ApigwGatewayV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#security_group_id ApigwGatewayV2#security_group_id}.'''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spec_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#spec_id ApigwGatewayV2#spec_id}.'''
        result = self._values.get("spec_id")
        assert result is not None, "Required property 'spec_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#subnet_id ApigwGatewayV2#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#vpc_id ApigwGatewayV2#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bandwidth_charging_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#bandwidth_charging_mode ApigwGatewayV2#bandwidth_charging_mode}.'''
        result = self._values.get("bandwidth_charging_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bandwidth_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#bandwidth_size ApigwGatewayV2#bandwidth_size}.'''
        result = self._values.get("bandwidth_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#description ApigwGatewayV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enterprise_project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#enterprise_project_id ApigwGatewayV2#enterprise_project_id}.'''
        result = self._values.get("enterprise_project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#id ApigwGatewayV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress_bandwidth_charging_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#ingress_bandwidth_charging_mode ApigwGatewayV2#ingress_bandwidth_charging_mode}.'''
        result = self._values.get("ingress_bandwidth_charging_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress_bandwidth_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#ingress_bandwidth_size ApigwGatewayV2#ingress_bandwidth_size}.'''
        result = self._values.get("ingress_bandwidth_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def loadbalancer_provider(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#loadbalancer_provider ApigwGatewayV2#loadbalancer_provider}.'''
        result = self._values.get("loadbalancer_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintain_begin(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#maintain_begin ApigwGatewayV2#maintain_begin}.'''
        result = self._values.get("maintain_begin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApigwGatewayV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#timeouts ApigwGatewayV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApigwGatewayV2Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwGatewayV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwGatewayV2.ApigwGatewayV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ApigwGatewayV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#create ApigwGatewayV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#delete ApigwGatewayV2#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#update ApigwGatewayV2#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea60c3a827f83e646673e2fa32a4efa6447096b0130c9710c161e79357532bd)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#create ApigwGatewayV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#delete ApigwGatewayV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_gateway_v2#update ApigwGatewayV2#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwGatewayV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwGatewayV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwGatewayV2.ApigwGatewayV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__926c6726d717edcf5c30b4e6f4549681b3e8da4184d1334974fcdf76ebe8b1e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ee4e68a1a7d3fb5697a053a2c25a8a2997ee0ddc37b9ce26c781f7695fc2f18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3887171c42fe5a0576b5998810891b90f1648a67c5074146b7779adb1ee1820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f2102acbf5f4ba0ff68115873f776ccbada3c3014db1fc29cafaf1aa665085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwGatewayV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwGatewayV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwGatewayV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78db11e89fc5e828cbb5bcaef7c2066059e93cce2087d961b0843444cc09414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApigwGatewayV2",
    "ApigwGatewayV2Config",
    "ApigwGatewayV2Timeouts",
    "ApigwGatewayV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__26f2d003d3d8af3e8032970b81dedecb566047ea1e71839342594de7e5f7e6d1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zones: typing.Sequence[builtins.str],
    name: builtins.str,
    security_group_id: builtins.str,
    spec_id: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    bandwidth_charging_mode: typing.Optional[builtins.str] = None,
    bandwidth_size: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    enterprise_project_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ingress_bandwidth_charging_mode: typing.Optional[builtins.str] = None,
    ingress_bandwidth_size: typing.Optional[jsii.Number] = None,
    loadbalancer_provider: typing.Optional[builtins.str] = None,
    maintain_begin: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApigwGatewayV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4fa4a63195af0036d63bcb2722d243f02169ae54ad214653e4fb07cafe822fd4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea978bfa18c7eaad29e73da80afbdbda5fa73730a632042f6ba0d2bb92a7655(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb88166944583f446c6d7ae90dc0cb7d6d6feb84843d2628785769a1c58097cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4d13109958ccc1034eed7d7b03ec2dfe839fff2084c750bf5e8414633e8ce3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6a14ac8988ae78b3149889c2f96e1f862a4825ad46fa6f162420ef5c19f90a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76d247bef5646012e8a42a3c640aa2a6a0f57b545a020e9d917e6fbc3e276b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff47ac872e46c96647e38b8bc480f9f43d44ab9a89b8423351da914be6ec812(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea2bb7e8db1073cac3939d9b1ef5c477d6e4c674d61300e3f16b072643c3f02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1f9ce2f0b7e7e5e8b0b464ebb0a2b396546c1044763fb35556340b5c1eb110(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64cc39b1a3ba5ace22548660cf870c602190935eec5fb4c99e1bfaa41837c5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3d8964e065cb20259ef8cb57464e8130cc7c880c8ce961994ed5d54e4a7408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10621dbdc1e1250d2ccfd7eb3c7011d81c92aaf3f0dd8071118b1fdc074ee77d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3247fb274366afa2d8082f6eb4ca653c02f6250eba33f9f40b6902d04431bf65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f49aad259676192e01dc1506c6e2c38ab3e5a66eb83854a1429585a1c6fdac2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2e43201bd21d7228618b90e19498817753ad463e8b4587f7a448f942d5380b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a92ab0b4c6da694e52f47d8b12f15ee001a049c9c536e89dae9ddb4c623964(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300f66f70de76f9bf3070a06177ae87f6fdec756b80374bd168a922f8e81012b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zones: typing.Sequence[builtins.str],
    name: builtins.str,
    security_group_id: builtins.str,
    spec_id: builtins.str,
    subnet_id: builtins.str,
    vpc_id: builtins.str,
    bandwidth_charging_mode: typing.Optional[builtins.str] = None,
    bandwidth_size: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    enterprise_project_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ingress_bandwidth_charging_mode: typing.Optional[builtins.str] = None,
    ingress_bandwidth_size: typing.Optional[jsii.Number] = None,
    loadbalancer_provider: typing.Optional[builtins.str] = None,
    maintain_begin: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApigwGatewayV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea60c3a827f83e646673e2fa32a4efa6447096b0130c9710c161e79357532bd(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926c6726d717edcf5c30b4e6f4549681b3e8da4184d1334974fcdf76ebe8b1e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee4e68a1a7d3fb5697a053a2c25a8a2997ee0ddc37b9ce26c781f7695fc2f18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3887171c42fe5a0576b5998810891b90f1648a67c5074146b7779adb1ee1820(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f2102acbf5f4ba0ff68115873f776ccbada3c3014db1fc29cafaf1aa665085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78db11e89fc5e828cbb5bcaef7c2066059e93cce2087d961b0843444cc09414(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwGatewayV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
