r'''
# `opentelekomcloud_apigw_throttling_policy_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_apigw_throttling_policy_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2).
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


class ApigwThrottlingPolicyV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwThrottlingPolicyV2.ApigwThrottlingPolicyV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2 opentelekomcloud_apigw_throttling_policy_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_id: builtins.str,
        max_api_requests: jsii.Number,
        name: builtins.str,
        period: jsii.Number,
        app_throttles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwThrottlingPolicyV2AppThrottles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_app_requests: typing.Optional[jsii.Number] = None,
        max_ip_requests: typing.Optional[jsii.Number] = None,
        max_user_requests: typing.Optional[jsii.Number] = None,
        period_unit: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        user_throttles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwThrottlingPolicyV2UserThrottles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2 opentelekomcloud_apigw_throttling_policy_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#instance_id ApigwThrottlingPolicyV2#instance_id}.
        :param max_api_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_api_requests ApigwThrottlingPolicyV2#max_api_requests}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#name ApigwThrottlingPolicyV2#name}.
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#period ApigwThrottlingPolicyV2#period}.
        :param app_throttles: app_throttles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#app_throttles ApigwThrottlingPolicyV2#app_throttles}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#description ApigwThrottlingPolicyV2#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#id ApigwThrottlingPolicyV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_app_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_app_requests ApigwThrottlingPolicyV2#max_app_requests}.
        :param max_ip_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_ip_requests ApigwThrottlingPolicyV2#max_ip_requests}.
        :param max_user_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_user_requests ApigwThrottlingPolicyV2#max_user_requests}.
        :param period_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#period_unit ApigwThrottlingPolicyV2#period_unit}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#type ApigwThrottlingPolicyV2#type}.
        :param user_throttles: user_throttles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#user_throttles ApigwThrottlingPolicyV2#user_throttles}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0795371eddeef984b24e227c743c62e085dd48f26a8e94fecaf3d0912e5637bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApigwThrottlingPolicyV2Config(
            instance_id=instance_id,
            max_api_requests=max_api_requests,
            name=name,
            period=period,
            app_throttles=app_throttles,
            description=description,
            id=id,
            max_app_requests=max_app_requests,
            max_ip_requests=max_ip_requests,
            max_user_requests=max_user_requests,
            period_unit=period_unit,
            type=type,
            user_throttles=user_throttles,
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
        '''Generates CDKTF code for importing a ApigwThrottlingPolicyV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApigwThrottlingPolicyV2 to import.
        :param import_from_id: The id of the existing ApigwThrottlingPolicyV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApigwThrottlingPolicyV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445116031a6491691f04d8febc6e60bc6ca57d40e1dfad255bfba413e4217005)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAppThrottles")
    def put_app_throttles(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwThrottlingPolicyV2AppThrottles", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c842fa531f13ea3725a905d6b4ae0bcc0116925a839a725353fae656eeec46a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAppThrottles", [value]))

    @jsii.member(jsii_name="putUserThrottles")
    def put_user_throttles(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwThrottlingPolicyV2UserThrottles", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d52b25754c2abc1414349629e971cea3188469c7ecd5c2e181588ad2492387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUserThrottles", [value]))

    @jsii.member(jsii_name="resetAppThrottles")
    def reset_app_throttles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppThrottles", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxAppRequests")
    def reset_max_app_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAppRequests", []))

    @jsii.member(jsii_name="resetMaxIpRequests")
    def reset_max_ip_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIpRequests", []))

    @jsii.member(jsii_name="resetMaxUserRequests")
    def reset_max_user_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUserRequests", []))

    @jsii.member(jsii_name="resetPeriodUnit")
    def reset_period_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodUnit", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUserThrottles")
    def reset_user_throttles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserThrottles", []))

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
    @jsii.member(jsii_name="appThrottles")
    def app_throttles(self) -> "ApigwThrottlingPolicyV2AppThrottlesList":
        return typing.cast("ApigwThrottlingPolicyV2AppThrottlesList", jsii.get(self, "appThrottles"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="userThrottles")
    def user_throttles(self) -> "ApigwThrottlingPolicyV2UserThrottlesList":
        return typing.cast("ApigwThrottlingPolicyV2UserThrottlesList", jsii.get(self, "userThrottles"))

    @builtins.property
    @jsii.member(jsii_name="appThrottlesInput")
    def app_throttles_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwThrottlingPolicyV2AppThrottles"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwThrottlingPolicyV2AppThrottles"]]], jsii.get(self, "appThrottlesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="maxApiRequestsInput")
    def max_api_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxApiRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAppRequestsInput")
    def max_app_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAppRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIpRequestsInput")
    def max_ip_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIpRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUserRequestsInput")
    def max_user_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUserRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="periodUnitInput")
    def period_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userThrottlesInput")
    def user_throttles_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwThrottlingPolicyV2UserThrottles"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwThrottlingPolicyV2UserThrottles"]]], jsii.get(self, "userThrottlesInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aca821503c08b062f2768f4fee5a35e929a8f5c171ca173af45c5fa8a096a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e13feb973bfc74adcef3ac844a686812ec971c9f6e6c61ff14c558b4eb46023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9e6df559b3571b3d3ac3333c7715bfdff4dc336a39c08c3f8890d4c41e8b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxApiRequests")
    def max_api_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxApiRequests"))

    @max_api_requests.setter
    def max_api_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ee845bd30b08799a461303fed3b3314c8699e27be61914edfaa9db4c13faca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxApiRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAppRequests")
    def max_app_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAppRequests"))

    @max_app_requests.setter
    def max_app_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d58cfb0b077e7262f8314c7f7cfb1c5fbd5cbc6447c51534005b8bb3dd39a30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAppRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxIpRequests")
    def max_ip_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIpRequests"))

    @max_ip_requests.setter
    def max_ip_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78cd6c58786b28a633e57d9592b2ace315d848831ea9b811cadc3af0bbaaf56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIpRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUserRequests")
    def max_user_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUserRequests"))

    @max_user_requests.setter
    def max_user_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca6ab22f922788ac51a39e2cd817500f9ec79b26a6a3a37b3fdfa20c578df58e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUserRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1687ddb1c41bd3d4693b851ddf170afb493a6f678d03e4bc719f1318072ddcbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "period"))

    @period.setter
    def period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b73d79f6c8fd4670454c81a6d1bcf879bbeff26686de85f7f741eb96307de8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodUnit")
    def period_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "periodUnit"))

    @period_unit.setter
    def period_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac0ddf7bf704f01cae74a3701fe9b687127c68fde2d9796f670015162efb5c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976d780e348e0840f5a32e12bc7044b5afe498e5ee2a73f2288af95785389deb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwThrottlingPolicyV2.ApigwThrottlingPolicyV2AppThrottles",
    jsii_struct_bases=[],
    name_mapping={
        "max_api_requests": "maxApiRequests",
        "throttling_object_id": "throttlingObjectId",
    },
)
class ApigwThrottlingPolicyV2AppThrottles:
    def __init__(
        self,
        *,
        max_api_requests: jsii.Number,
        throttling_object_id: builtins.str,
    ) -> None:
        '''
        :param max_api_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_api_requests ApigwThrottlingPolicyV2#max_api_requests}.
        :param throttling_object_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#throttling_object_id ApigwThrottlingPolicyV2#throttling_object_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85fa3b9883e288d2e054dd3e98a63c51a111c1e966819db7e2ae0f24f257fffc)
            check_type(argname="argument max_api_requests", value=max_api_requests, expected_type=type_hints["max_api_requests"])
            check_type(argname="argument throttling_object_id", value=throttling_object_id, expected_type=type_hints["throttling_object_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_api_requests": max_api_requests,
            "throttling_object_id": throttling_object_id,
        }

    @builtins.property
    def max_api_requests(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_api_requests ApigwThrottlingPolicyV2#max_api_requests}.'''
        result = self._values.get("max_api_requests")
        assert result is not None, "Required property 'max_api_requests' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def throttling_object_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#throttling_object_id ApigwThrottlingPolicyV2#throttling_object_id}.'''
        result = self._values.get("throttling_object_id")
        assert result is not None, "Required property 'throttling_object_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwThrottlingPolicyV2AppThrottles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwThrottlingPolicyV2AppThrottlesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwThrottlingPolicyV2.ApigwThrottlingPolicyV2AppThrottlesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2867d0485e6870174adaf3b9c4d0af6ef09fd53f7292dcd91690dbfbca012af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigwThrottlingPolicyV2AppThrottlesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f627793f86c06a948be5219871749fa2c7460de82471d1e9f6752901d63445d4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwThrottlingPolicyV2AppThrottlesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f83bd780b481054e39420fa25b2c0ee45070b7edacce622d6a698f36dfed0de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02eed2fae7099bfa430aabdbf72808eea76b434d2aa2cbdd0c1671f82eac9cf5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1785075bcf4b54132258d217aa5064603db780959f98da27cf8e412d88ca9515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwThrottlingPolicyV2AppThrottles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwThrottlingPolicyV2AppThrottles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwThrottlingPolicyV2AppThrottles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9018e37d856af99c016ee5b0f953c36fdf3820f68b7f9809a1feb0bb4564e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwThrottlingPolicyV2AppThrottlesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwThrottlingPolicyV2.ApigwThrottlingPolicyV2AppThrottlesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f435d60de989f33cde1cf828c9a56705147a9517a09fbd42fc95e6904f901153)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="throttlingObjectName")
    def throttling_object_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "throttlingObjectName"))

    @builtins.property
    @jsii.member(jsii_name="maxApiRequestsInput")
    def max_api_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxApiRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="throttlingObjectIdInput")
    def throttling_object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "throttlingObjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="maxApiRequests")
    def max_api_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxApiRequests"))

    @max_api_requests.setter
    def max_api_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a336e21e02af6f081219d96e5a527e2323fd074d20b2f6874e73b808230486cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxApiRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throttlingObjectId")
    def throttling_object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "throttlingObjectId"))

    @throttling_object_id.setter
    def throttling_object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf724e50e89d749332284cea16c7207b5bcc64314f5093eaa9aaf89363988b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttlingObjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwThrottlingPolicyV2AppThrottles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwThrottlingPolicyV2AppThrottles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwThrottlingPolicyV2AppThrottles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f078659565b8bb8eea101d1540204d0423e45f999bf2c989635c517cd942e9d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwThrottlingPolicyV2.ApigwThrottlingPolicyV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_id": "instanceId",
        "max_api_requests": "maxApiRequests",
        "name": "name",
        "period": "period",
        "app_throttles": "appThrottles",
        "description": "description",
        "id": "id",
        "max_app_requests": "maxAppRequests",
        "max_ip_requests": "maxIpRequests",
        "max_user_requests": "maxUserRequests",
        "period_unit": "periodUnit",
        "type": "type",
        "user_throttles": "userThrottles",
    },
)
class ApigwThrottlingPolicyV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_id: builtins.str,
        max_api_requests: jsii.Number,
        name: builtins.str,
        period: jsii.Number,
        app_throttles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwThrottlingPolicyV2AppThrottles, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        max_app_requests: typing.Optional[jsii.Number] = None,
        max_ip_requests: typing.Optional[jsii.Number] = None,
        max_user_requests: typing.Optional[jsii.Number] = None,
        period_unit: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        user_throttles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigwThrottlingPolicyV2UserThrottles", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#instance_id ApigwThrottlingPolicyV2#instance_id}.
        :param max_api_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_api_requests ApigwThrottlingPolicyV2#max_api_requests}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#name ApigwThrottlingPolicyV2#name}.
        :param period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#period ApigwThrottlingPolicyV2#period}.
        :param app_throttles: app_throttles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#app_throttles ApigwThrottlingPolicyV2#app_throttles}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#description ApigwThrottlingPolicyV2#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#id ApigwThrottlingPolicyV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_app_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_app_requests ApigwThrottlingPolicyV2#max_app_requests}.
        :param max_ip_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_ip_requests ApigwThrottlingPolicyV2#max_ip_requests}.
        :param max_user_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_user_requests ApigwThrottlingPolicyV2#max_user_requests}.
        :param period_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#period_unit ApigwThrottlingPolicyV2#period_unit}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#type ApigwThrottlingPolicyV2#type}.
        :param user_throttles: user_throttles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#user_throttles ApigwThrottlingPolicyV2#user_throttles}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756be4a7454a107dba5616e656c3f9d1d25e81d3725f74f114bc43076f3092e8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument max_api_requests", value=max_api_requests, expected_type=type_hints["max_api_requests"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument app_throttles", value=app_throttles, expected_type=type_hints["app_throttles"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_app_requests", value=max_app_requests, expected_type=type_hints["max_app_requests"])
            check_type(argname="argument max_ip_requests", value=max_ip_requests, expected_type=type_hints["max_ip_requests"])
            check_type(argname="argument max_user_requests", value=max_user_requests, expected_type=type_hints["max_user_requests"])
            check_type(argname="argument period_unit", value=period_unit, expected_type=type_hints["period_unit"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_throttles", value=user_throttles, expected_type=type_hints["user_throttles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_id": instance_id,
            "max_api_requests": max_api_requests,
            "name": name,
            "period": period,
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
        if app_throttles is not None:
            self._values["app_throttles"] = app_throttles
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if max_app_requests is not None:
            self._values["max_app_requests"] = max_app_requests
        if max_ip_requests is not None:
            self._values["max_ip_requests"] = max_ip_requests
        if max_user_requests is not None:
            self._values["max_user_requests"] = max_user_requests
        if period_unit is not None:
            self._values["period_unit"] = period_unit
        if type is not None:
            self._values["type"] = type
        if user_throttles is not None:
            self._values["user_throttles"] = user_throttles

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
    def instance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#instance_id ApigwThrottlingPolicyV2#instance_id}.'''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_api_requests(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_api_requests ApigwThrottlingPolicyV2#max_api_requests}.'''
        result = self._values.get("max_api_requests")
        assert result is not None, "Required property 'max_api_requests' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#name ApigwThrottlingPolicyV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#period ApigwThrottlingPolicyV2#period}.'''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def app_throttles(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwThrottlingPolicyV2AppThrottles]]]:
        '''app_throttles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#app_throttles ApigwThrottlingPolicyV2#app_throttles}
        '''
        result = self._values.get("app_throttles")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwThrottlingPolicyV2AppThrottles]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#description ApigwThrottlingPolicyV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#id ApigwThrottlingPolicyV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_app_requests(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_app_requests ApigwThrottlingPolicyV2#max_app_requests}.'''
        result = self._values.get("max_app_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_ip_requests(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_ip_requests ApigwThrottlingPolicyV2#max_ip_requests}.'''
        result = self._values.get("max_ip_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_user_requests(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_user_requests ApigwThrottlingPolicyV2#max_user_requests}.'''
        result = self._values.get("max_user_requests")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#period_unit ApigwThrottlingPolicyV2#period_unit}.'''
        result = self._values.get("period_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#type ApigwThrottlingPolicyV2#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_throttles(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwThrottlingPolicyV2UserThrottles"]]]:
        '''user_throttles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#user_throttles ApigwThrottlingPolicyV2#user_throttles}
        '''
        result = self._values.get("user_throttles")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigwThrottlingPolicyV2UserThrottles"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwThrottlingPolicyV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.apigwThrottlingPolicyV2.ApigwThrottlingPolicyV2UserThrottles",
    jsii_struct_bases=[],
    name_mapping={
        "max_api_requests": "maxApiRequests",
        "throttling_object_id": "throttlingObjectId",
    },
)
class ApigwThrottlingPolicyV2UserThrottles:
    def __init__(
        self,
        *,
        max_api_requests: jsii.Number,
        throttling_object_id: builtins.str,
    ) -> None:
        '''
        :param max_api_requests: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_api_requests ApigwThrottlingPolicyV2#max_api_requests}.
        :param throttling_object_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#throttling_object_id ApigwThrottlingPolicyV2#throttling_object_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08ed5d70cf75c40e743e868c183fb0e4021eea4d8b57f50e2dd356b33a57c2d2)
            check_type(argname="argument max_api_requests", value=max_api_requests, expected_type=type_hints["max_api_requests"])
            check_type(argname="argument throttling_object_id", value=throttling_object_id, expected_type=type_hints["throttling_object_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_api_requests": max_api_requests,
            "throttling_object_id": throttling_object_id,
        }

    @builtins.property
    def max_api_requests(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#max_api_requests ApigwThrottlingPolicyV2#max_api_requests}.'''
        result = self._values.get("max_api_requests")
        assert result is not None, "Required property 'max_api_requests' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def throttling_object_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/apigw_throttling_policy_v2#throttling_object_id ApigwThrottlingPolicyV2#throttling_object_id}.'''
        result = self._values.get("throttling_object_id")
        assert result is not None, "Required property 'throttling_object_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigwThrottlingPolicyV2UserThrottles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigwThrottlingPolicyV2UserThrottlesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwThrottlingPolicyV2.ApigwThrottlingPolicyV2UserThrottlesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e022b4076b01852a44f2f9ce6adf74f6718587a19a7daa7a9ef3517c36390a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigwThrottlingPolicyV2UserThrottlesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a477a4c04bedd219319f30f1f69e47377dd75c14228aa5eaa2a1a3266c2d7177)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigwThrottlingPolicyV2UserThrottlesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe20562e5368f08af56b5b39d161cb4f9995df7d28eabbe4fdb0b56d7b3ff481)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15225d762d659561e7b4e8ccd451bb80203fe3ad28d2b17b0abbd9b25a8c7f46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b086ed18e0f1f4a4ba0ea302af97e7817e279fee329d4aa3e6b761a5f19e1673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwThrottlingPolicyV2UserThrottles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwThrottlingPolicyV2UserThrottles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwThrottlingPolicyV2UserThrottles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae395676f6381e4e3a96ded5fc8ec9e774791cc258f92cd8be07acac4eae32c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigwThrottlingPolicyV2UserThrottlesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.apigwThrottlingPolicyV2.ApigwThrottlingPolicyV2UserThrottlesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66d131879255a12c275144c9b74ae9cf00129064a30cdeded8f2b1fc954b30b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="throttlingObjectName")
    def throttling_object_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "throttlingObjectName"))

    @builtins.property
    @jsii.member(jsii_name="maxApiRequestsInput")
    def max_api_requests_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxApiRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="throttlingObjectIdInput")
    def throttling_object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "throttlingObjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="maxApiRequests")
    def max_api_requests(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxApiRequests"))

    @max_api_requests.setter
    def max_api_requests(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b1d5efae05259f0f531a74a6caa43ae3a39de2c4c3e1ff46f1c0ed4231e52cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxApiRequests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throttlingObjectId")
    def throttling_object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "throttlingObjectId"))

    @throttling_object_id.setter
    def throttling_object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d124a5ac010951a2a92f8984a642252e2291a97e842ce1cee57ece5ed5345f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttlingObjectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwThrottlingPolicyV2UserThrottles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwThrottlingPolicyV2UserThrottles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwThrottlingPolicyV2UserThrottles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c997f2f65cea2ae5e81b63a1b20aacbaf1d2b020a3dcbba35d32a89b695fd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApigwThrottlingPolicyV2",
    "ApigwThrottlingPolicyV2AppThrottles",
    "ApigwThrottlingPolicyV2AppThrottlesList",
    "ApigwThrottlingPolicyV2AppThrottlesOutputReference",
    "ApigwThrottlingPolicyV2Config",
    "ApigwThrottlingPolicyV2UserThrottles",
    "ApigwThrottlingPolicyV2UserThrottlesList",
    "ApigwThrottlingPolicyV2UserThrottlesOutputReference",
]

publication.publish()

def _typecheckingstub__0795371eddeef984b24e227c743c62e085dd48f26a8e94fecaf3d0912e5637bd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_id: builtins.str,
    max_api_requests: jsii.Number,
    name: builtins.str,
    period: jsii.Number,
    app_throttles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwThrottlingPolicyV2AppThrottles, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_app_requests: typing.Optional[jsii.Number] = None,
    max_ip_requests: typing.Optional[jsii.Number] = None,
    max_user_requests: typing.Optional[jsii.Number] = None,
    period_unit: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_throttles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwThrottlingPolicyV2UserThrottles, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__445116031a6491691f04d8febc6e60bc6ca57d40e1dfad255bfba413e4217005(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c842fa531f13ea3725a905d6b4ae0bcc0116925a839a725353fae656eeec46a2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwThrottlingPolicyV2AppThrottles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d52b25754c2abc1414349629e971cea3188469c7ecd5c2e181588ad2492387(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwThrottlingPolicyV2UserThrottles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aca821503c08b062f2768f4fee5a35e929a8f5c171ca173af45c5fa8a096a12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e13feb973bfc74adcef3ac844a686812ec971c9f6e6c61ff14c558b4eb46023(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9e6df559b3571b3d3ac3333c7715bfdff4dc336a39c08c3f8890d4c41e8b09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ee845bd30b08799a461303fed3b3314c8699e27be61914edfaa9db4c13faca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d58cfb0b077e7262f8314c7f7cfb1c5fbd5cbc6447c51534005b8bb3dd39a30(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78cd6c58786b28a633e57d9592b2ace315d848831ea9b811cadc3af0bbaaf56f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6ab22f922788ac51a39e2cd817500f9ec79b26a6a3a37b3fdfa20c578df58e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1687ddb1c41bd3d4693b851ddf170afb493a6f678d03e4bc719f1318072ddcbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b73d79f6c8fd4670454c81a6d1bcf879bbeff26686de85f7f741eb96307de8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac0ddf7bf704f01cae74a3701fe9b687127c68fde2d9796f670015162efb5c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976d780e348e0840f5a32e12bc7044b5afe498e5ee2a73f2288af95785389deb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85fa3b9883e288d2e054dd3e98a63c51a111c1e966819db7e2ae0f24f257fffc(
    *,
    max_api_requests: jsii.Number,
    throttling_object_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2867d0485e6870174adaf3b9c4d0af6ef09fd53f7292dcd91690dbfbca012af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f627793f86c06a948be5219871749fa2c7460de82471d1e9f6752901d63445d4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f83bd780b481054e39420fa25b2c0ee45070b7edacce622d6a698f36dfed0de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02eed2fae7099bfa430aabdbf72808eea76b434d2aa2cbdd0c1671f82eac9cf5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1785075bcf4b54132258d217aa5064603db780959f98da27cf8e412d88ca9515(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9018e37d856af99c016ee5b0f953c36fdf3820f68b7f9809a1feb0bb4564e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwThrottlingPolicyV2AppThrottles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f435d60de989f33cde1cf828c9a56705147a9517a09fbd42fc95e6904f901153(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a336e21e02af6f081219d96e5a527e2323fd074d20b2f6874e73b808230486cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf724e50e89d749332284cea16c7207b5bcc64314f5093eaa9aaf89363988b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f078659565b8bb8eea101d1540204d0423e45f999bf2c989635c517cd942e9d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwThrottlingPolicyV2AppThrottles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756be4a7454a107dba5616e656c3f9d1d25e81d3725f74f114bc43076f3092e8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_id: builtins.str,
    max_api_requests: jsii.Number,
    name: builtins.str,
    period: jsii.Number,
    app_throttles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwThrottlingPolicyV2AppThrottles, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    max_app_requests: typing.Optional[jsii.Number] = None,
    max_ip_requests: typing.Optional[jsii.Number] = None,
    max_user_requests: typing.Optional[jsii.Number] = None,
    period_unit: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_throttles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigwThrottlingPolicyV2UserThrottles, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ed5d70cf75c40e743e868c183fb0e4021eea4d8b57f50e2dd356b33a57c2d2(
    *,
    max_api_requests: jsii.Number,
    throttling_object_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e022b4076b01852a44f2f9ce6adf74f6718587a19a7daa7a9ef3517c36390a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a477a4c04bedd219319f30f1f69e47377dd75c14228aa5eaa2a1a3266c2d7177(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe20562e5368f08af56b5b39d161cb4f9995df7d28eabbe4fdb0b56d7b3ff481(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15225d762d659561e7b4e8ccd451bb80203fe3ad28d2b17b0abbd9b25a8c7f46(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b086ed18e0f1f4a4ba0ea302af97e7817e279fee329d4aa3e6b761a5f19e1673(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae395676f6381e4e3a96ded5fc8ec9e774791cc258f92cd8be07acac4eae32c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigwThrottlingPolicyV2UserThrottles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d131879255a12c275144c9b74ae9cf00129064a30cdeded8f2b1fc954b30b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1d5efae05259f0f531a74a6caa43ae3a39de2c4c3e1ff46f1c0ed4231e52cf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d124a5ac010951a2a92f8984a642252e2291a97e842ce1cee57ece5ed5345f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c997f2f65cea2ae5e81b63a1b20aacbaf1d2b020a3dcbba35d32a89b695fd6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigwThrottlingPolicyV2UserThrottles]],
) -> None:
    """Type checking stubs"""
    pass
