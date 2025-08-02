r'''
# `opentelekomcloud_identity_login_policy_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_identity_login_policy_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3).
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


class IdentityLoginPolicyV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityLoginPolicyV3.IdentityLoginPolicyV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3 opentelekomcloud_identity_login_policy_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_validity_period: typing.Optional[jsii.Number] = None,
        custom_info_for_login: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lockout_duration: typing.Optional[jsii.Number] = None,
        login_failed_times: typing.Optional[jsii.Number] = None,
        period_with_login_failures: typing.Optional[jsii.Number] = None,
        session_timeout: typing.Optional[jsii.Number] = None,
        show_recent_login_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3 opentelekomcloud_identity_login_policy_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_validity_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#account_validity_period IdentityLoginPolicyV3#account_validity_period}.
        :param custom_info_for_login: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#custom_info_for_login IdentityLoginPolicyV3#custom_info_for_login}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#id IdentityLoginPolicyV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lockout_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#lockout_duration IdentityLoginPolicyV3#lockout_duration}.
        :param login_failed_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#login_failed_times IdentityLoginPolicyV3#login_failed_times}.
        :param period_with_login_failures: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#period_with_login_failures IdentityLoginPolicyV3#period_with_login_failures}.
        :param session_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#session_timeout IdentityLoginPolicyV3#session_timeout}.
        :param show_recent_login_info: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#show_recent_login_info IdentityLoginPolicyV3#show_recent_login_info}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2dbbe59dc46f2945668fe940d4bf831eeb9858940223cf32ee3c814ad2ff83)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IdentityLoginPolicyV3Config(
            account_validity_period=account_validity_period,
            custom_info_for_login=custom_info_for_login,
            id=id,
            lockout_duration=lockout_duration,
            login_failed_times=login_failed_times,
            period_with_login_failures=period_with_login_failures,
            session_timeout=session_timeout,
            show_recent_login_info=show_recent_login_info,
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
        '''Generates CDKTF code for importing a IdentityLoginPolicyV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IdentityLoginPolicyV3 to import.
        :param import_from_id: The id of the existing IdentityLoginPolicyV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IdentityLoginPolicyV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e2793f6f3c8970c4b79c51895de4707ec9ebb9d781c1b3080ce87b5873dfb7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccountValidityPeriod")
    def reset_account_validity_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountValidityPeriod", []))

    @jsii.member(jsii_name="resetCustomInfoForLogin")
    def reset_custom_info_for_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomInfoForLogin", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLockoutDuration")
    def reset_lockout_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockoutDuration", []))

    @jsii.member(jsii_name="resetLoginFailedTimes")
    def reset_login_failed_times(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginFailedTimes", []))

    @jsii.member(jsii_name="resetPeriodWithLoginFailures")
    def reset_period_with_login_failures(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodWithLoginFailures", []))

    @jsii.member(jsii_name="resetSessionTimeout")
    def reset_session_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionTimeout", []))

    @jsii.member(jsii_name="resetShowRecentLoginInfo")
    def reset_show_recent_login_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShowRecentLoginInfo", []))

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
    @jsii.member(jsii_name="accountValidityPeriodInput")
    def account_validity_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountValidityPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="customInfoForLoginInput")
    def custom_info_for_login_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customInfoForLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lockoutDurationInput")
    def lockout_duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lockoutDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="loginFailedTimesInput")
    def login_failed_times_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "loginFailedTimesInput"))

    @builtins.property
    @jsii.member(jsii_name="periodWithLoginFailuresInput")
    def period_with_login_failures_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodWithLoginFailuresInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionTimeoutInput")
    def session_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="showRecentLoginInfoInput")
    def show_recent_login_info_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "showRecentLoginInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="accountValidityPeriod")
    def account_validity_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountValidityPeriod"))

    @account_validity_period.setter
    def account_validity_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc75e8e09901e5b810a1933a79541968384176151084a178c4b3d56a7f593421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountValidityPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customInfoForLogin")
    def custom_info_for_login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customInfoForLogin"))

    @custom_info_for_login.setter
    def custom_info_for_login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b169b04ff2fe6bc95773cc767b24685bad8538480cbc29ecd3f4448b78e9ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customInfoForLogin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__132126d556bf923995db9aba0bc798c02dd9898ea1e71ec7023feac1d8c8d5b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockoutDuration")
    def lockout_duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lockoutDuration"))

    @lockout_duration.setter
    def lockout_duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5484203cfb60717e46088c67a8adbb0a71fcca9d07002644fc9f9341dd0f0361)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockoutDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginFailedTimes")
    def login_failed_times(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "loginFailedTimes"))

    @login_failed_times.setter
    def login_failed_times(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ed341f3e41b3f96e8ff3684eb3509d07bfe92d97326a4689ec1c302989c21f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginFailedTimes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodWithLoginFailures")
    def period_with_login_failures(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodWithLoginFailures"))

    @period_with_login_failures.setter
    def period_with_login_failures(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6431cbe07e38d5e2538aff64cad68d312102fc083ad7b2612d0a35c32f55219b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodWithLoginFailures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionTimeout")
    def session_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionTimeout"))

    @session_timeout.setter
    def session_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b03fb75797e95eac2ae4638be52007ba1391215d506532623977a18a38cfd47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="showRecentLoginInfo")
    def show_recent_login_info(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "showRecentLoginInfo"))

    @show_recent_login_info.setter
    def show_recent_login_info(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d910a150ed4ab3548317a746aaa103d062249c19d93d9e90c870d6db987ca7d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "showRecentLoginInfo", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.identityLoginPolicyV3.IdentityLoginPolicyV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_validity_period": "accountValidityPeriod",
        "custom_info_for_login": "customInfoForLogin",
        "id": "id",
        "lockout_duration": "lockoutDuration",
        "login_failed_times": "loginFailedTimes",
        "period_with_login_failures": "periodWithLoginFailures",
        "session_timeout": "sessionTimeout",
        "show_recent_login_info": "showRecentLoginInfo",
    },
)
class IdentityLoginPolicyV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_validity_period: typing.Optional[jsii.Number] = None,
        custom_info_for_login: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        lockout_duration: typing.Optional[jsii.Number] = None,
        login_failed_times: typing.Optional[jsii.Number] = None,
        period_with_login_failures: typing.Optional[jsii.Number] = None,
        session_timeout: typing.Optional[jsii.Number] = None,
        show_recent_login_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_validity_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#account_validity_period IdentityLoginPolicyV3#account_validity_period}.
        :param custom_info_for_login: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#custom_info_for_login IdentityLoginPolicyV3#custom_info_for_login}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#id IdentityLoginPolicyV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lockout_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#lockout_duration IdentityLoginPolicyV3#lockout_duration}.
        :param login_failed_times: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#login_failed_times IdentityLoginPolicyV3#login_failed_times}.
        :param period_with_login_failures: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#period_with_login_failures IdentityLoginPolicyV3#period_with_login_failures}.
        :param session_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#session_timeout IdentityLoginPolicyV3#session_timeout}.
        :param show_recent_login_info: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#show_recent_login_info IdentityLoginPolicyV3#show_recent_login_info}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f8e2811434c5c33b911d9f169c64dc9a805a9eb70f9704089d51b395a5a50a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_validity_period", value=account_validity_period, expected_type=type_hints["account_validity_period"])
            check_type(argname="argument custom_info_for_login", value=custom_info_for_login, expected_type=type_hints["custom_info_for_login"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lockout_duration", value=lockout_duration, expected_type=type_hints["lockout_duration"])
            check_type(argname="argument login_failed_times", value=login_failed_times, expected_type=type_hints["login_failed_times"])
            check_type(argname="argument period_with_login_failures", value=period_with_login_failures, expected_type=type_hints["period_with_login_failures"])
            check_type(argname="argument session_timeout", value=session_timeout, expected_type=type_hints["session_timeout"])
            check_type(argname="argument show_recent_login_info", value=show_recent_login_info, expected_type=type_hints["show_recent_login_info"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if account_validity_period is not None:
            self._values["account_validity_period"] = account_validity_period
        if custom_info_for_login is not None:
            self._values["custom_info_for_login"] = custom_info_for_login
        if id is not None:
            self._values["id"] = id
        if lockout_duration is not None:
            self._values["lockout_duration"] = lockout_duration
        if login_failed_times is not None:
            self._values["login_failed_times"] = login_failed_times
        if period_with_login_failures is not None:
            self._values["period_with_login_failures"] = period_with_login_failures
        if session_timeout is not None:
            self._values["session_timeout"] = session_timeout
        if show_recent_login_info is not None:
            self._values["show_recent_login_info"] = show_recent_login_info

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
    def account_validity_period(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#account_validity_period IdentityLoginPolicyV3#account_validity_period}.'''
        result = self._values.get("account_validity_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_info_for_login(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#custom_info_for_login IdentityLoginPolicyV3#custom_info_for_login}.'''
        result = self._values.get("custom_info_for_login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#id IdentityLoginPolicyV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lockout_duration(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#lockout_duration IdentityLoginPolicyV3#lockout_duration}.'''
        result = self._values.get("lockout_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def login_failed_times(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#login_failed_times IdentityLoginPolicyV3#login_failed_times}.'''
        result = self._values.get("login_failed_times")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_with_login_failures(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#period_with_login_failures IdentityLoginPolicyV3#period_with_login_failures}.'''
        result = self._values.get("period_with_login_failures")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def session_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#session_timeout IdentityLoginPolicyV3#session_timeout}.'''
        result = self._values.get("session_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def show_recent_login_info(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_login_policy_v3#show_recent_login_info IdentityLoginPolicyV3#show_recent_login_info}.'''
        result = self._values.get("show_recent_login_info")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityLoginPolicyV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IdentityLoginPolicyV3",
    "IdentityLoginPolicyV3Config",
]

publication.publish()

def _typecheckingstub__5c2dbbe59dc46f2945668fe940d4bf831eeb9858940223cf32ee3c814ad2ff83(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_validity_period: typing.Optional[jsii.Number] = None,
    custom_info_for_login: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lockout_duration: typing.Optional[jsii.Number] = None,
    login_failed_times: typing.Optional[jsii.Number] = None,
    period_with_login_failures: typing.Optional[jsii.Number] = None,
    session_timeout: typing.Optional[jsii.Number] = None,
    show_recent_login_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__b8e2793f6f3c8970c4b79c51895de4707ec9ebb9d781c1b3080ce87b5873dfb7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc75e8e09901e5b810a1933a79541968384176151084a178c4b3d56a7f593421(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b169b04ff2fe6bc95773cc767b24685bad8538480cbc29ecd3f4448b78e9ef0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132126d556bf923995db9aba0bc798c02dd9898ea1e71ec7023feac1d8c8d5b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5484203cfb60717e46088c67a8adbb0a71fcca9d07002644fc9f9341dd0f0361(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ed341f3e41b3f96e8ff3684eb3509d07bfe92d97326a4689ec1c302989c21f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6431cbe07e38d5e2538aff64cad68d312102fc083ad7b2612d0a35c32f55219b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b03fb75797e95eac2ae4638be52007ba1391215d506532623977a18a38cfd47(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d910a150ed4ab3548317a746aaa103d062249c19d93d9e90c870d6db987ca7d3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f8e2811434c5c33b911d9f169c64dc9a805a9eb70f9704089d51b395a5a50a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_validity_period: typing.Optional[jsii.Number] = None,
    custom_info_for_login: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    lockout_duration: typing.Optional[jsii.Number] = None,
    login_failed_times: typing.Optional[jsii.Number] = None,
    period_with_login_failures: typing.Optional[jsii.Number] = None,
    session_timeout: typing.Optional[jsii.Number] = None,
    show_recent_login_info: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
