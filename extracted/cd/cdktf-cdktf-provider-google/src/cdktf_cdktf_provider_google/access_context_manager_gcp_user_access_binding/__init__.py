r'''
# `google_access_context_manager_gcp_user_access_binding`

Refer to the Terraform Registry for docs: [`google_access_context_manager_gcp_user_access_binding`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding).
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


class AccessContextManagerGcpUserAccessBinding(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBinding",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding google_access_context_manager_gcp_user_access_binding}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        group_key: builtins.str,
        organization_id: builtins.str,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        scoped_access_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerGcpUserAccessBindingScopedAccessSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        session_settings: typing.Optional[typing.Union["AccessContextManagerGcpUserAccessBindingSessionSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerGcpUserAccessBindingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding google_access_context_manager_gcp_user_access_binding} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param group_key: Required. Immutable. Google Group id whose members are subject to this binding's restrictions. See "id" in the G Suite Directory API's Groups resource. If a group's email address/alias is changed, this resource will continue to point at the changed group. This field does not accept group email addresses or aliases. Example: "01d520gv4vjcrht" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#group_key AccessContextManagerGcpUserAccessBinding#group_key}
        :param organization_id: Required. ID of the parent organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#organization_id AccessContextManagerGcpUserAccessBinding#organization_id}
        :param access_levels: Optional. Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#access_levels AccessContextManagerGcpUserAccessBinding#access_levels}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#id AccessContextManagerGcpUserAccessBinding#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scoped_access_settings: scoped_access_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#scoped_access_settings AccessContextManagerGcpUserAccessBinding#scoped_access_settings}
        :param session_settings: session_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_settings AccessContextManagerGcpUserAccessBinding#session_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#timeouts AccessContextManagerGcpUserAccessBinding#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889ea81f81401bfde8d61166d72730feb49d5ecefac0189d077741a0880209ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessContextManagerGcpUserAccessBindingConfig(
            group_key=group_key,
            organization_id=organization_id,
            access_levels=access_levels,
            id=id,
            scoped_access_settings=scoped_access_settings,
            session_settings=session_settings,
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
        '''Generates CDKTF code for importing a AccessContextManagerGcpUserAccessBinding resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessContextManagerGcpUserAccessBinding to import.
        :param import_from_id: The id of the existing AccessContextManagerGcpUserAccessBinding that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessContextManagerGcpUserAccessBinding to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b07c9c3efc6358dea4bb527963e93898a58e47929ba49459aaafd7627436cfc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putScopedAccessSettings")
    def put_scoped_access_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerGcpUserAccessBindingScopedAccessSettings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec482f15aeaa81c559f914a6eca0c7b5d811eb96a1b0df1154acb65e015098c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScopedAccessSettings", [value]))

    @jsii.member(jsii_name="putSessionSettings")
    def put_session_settings(
        self,
        *,
        max_inactivity: typing.Optional[builtins.str] = None,
        session_length: typing.Optional[builtins.str] = None,
        session_length_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_reauth_method: typing.Optional[builtins.str] = None,
        use_oidc_max_age: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param max_inactivity: Optional. How long a user is allowed to take between actions before a new access token must be issued. Only set for Google Cloud apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#max_inactivity AccessContextManagerGcpUserAccessBinding#max_inactivity}
        :param session_length: Optional. The session length. Setting this field to zero is equal to disabling session. Also can set infinite session by flipping the enabled bit to false below. If useOidcMaxAge is true, for OIDC apps, the session length will be the minimum of this field and OIDC max_age param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_length AccessContextManagerGcpUserAccessBinding#session_length}
        :param session_length_enabled: Optional. This field enables or disables Google Cloud session length. When false, all fields set above will be disregarded and the session length is basically infinite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_length_enabled AccessContextManagerGcpUserAccessBinding#session_length_enabled}
        :param session_reauth_method: Optional. The session challenges proposed to users when the Google Cloud session length is up. Possible values: ["LOGIN", "SECURITY_KEY", "PASSWORD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_reauth_method AccessContextManagerGcpUserAccessBinding#session_reauth_method}
        :param use_oidc_max_age: Optional. Only useful for OIDC apps. When false, the OIDC max_age param, if passed in the authentication request will be ignored. When true, the re-auth period will be the minimum of the sessionLength field and the max_age OIDC param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#use_oidc_max_age AccessContextManagerGcpUserAccessBinding#use_oidc_max_age}
        '''
        value = AccessContextManagerGcpUserAccessBindingSessionSettings(
            max_inactivity=max_inactivity,
            session_length=session_length,
            session_length_enabled=session_length_enabled,
            session_reauth_method=session_reauth_method,
            use_oidc_max_age=use_oidc_max_age,
        )

        return typing.cast(None, jsii.invoke(self, "putSessionSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#create AccessContextManagerGcpUserAccessBinding#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#delete AccessContextManagerGcpUserAccessBinding#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#update AccessContextManagerGcpUserAccessBinding#update}.
        '''
        value = AccessContextManagerGcpUserAccessBindingTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessLevels")
    def reset_access_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevels", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetScopedAccessSettings")
    def reset_scoped_access_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopedAccessSettings", []))

    @jsii.member(jsii_name="resetSessionSettings")
    def reset_session_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionSettings", []))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="scopedAccessSettings")
    def scoped_access_settings(
        self,
    ) -> "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsList":
        return typing.cast("AccessContextManagerGcpUserAccessBindingScopedAccessSettingsList", jsii.get(self, "scopedAccessSettings"))

    @builtins.property
    @jsii.member(jsii_name="sessionSettings")
    def session_settings(
        self,
    ) -> "AccessContextManagerGcpUserAccessBindingSessionSettingsOutputReference":
        return typing.cast("AccessContextManagerGcpUserAccessBindingSessionSettingsOutputReference", jsii.get(self, "sessionSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "AccessContextManagerGcpUserAccessBindingTimeoutsOutputReference":
        return typing.cast("AccessContextManagerGcpUserAccessBindingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelsInput")
    def access_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupKeyInput")
    def group_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationIdInput")
    def organization_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scopedAccessSettingsInput")
    def scoped_access_settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerGcpUserAccessBindingScopedAccessSettings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerGcpUserAccessBindingScopedAccessSettings"]]], jsii.get(self, "scopedAccessSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionSettingsInput")
    def session_settings_input(
        self,
    ) -> typing.Optional["AccessContextManagerGcpUserAccessBindingSessionSettings"]:
        return typing.cast(typing.Optional["AccessContextManagerGcpUserAccessBindingSessionSettings"], jsii.get(self, "sessionSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerGcpUserAccessBindingTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AccessContextManagerGcpUserAccessBindingTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevels")
    def access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessLevels"))

    @access_levels.setter
    def access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a191fb52320d18773dad2f54f3c5ec6db30d54e8e3c3065f870f1f088214b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupKey")
    def group_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupKey"))

    @group_key.setter
    def group_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5c38fe74065a471e17bbfd3353828d3ffe2a1f5fe3b10224ee0fca487e60b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b68b291408d496c8ee8bbddf1b4cd10ea4002fd36098b2524a516279680f618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @organization_id.setter
    def organization_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273b2491be50ff66e9e28cffa54086d71e84c6edca67b40ba116fa80a59958ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "group_key": "groupKey",
        "organization_id": "organizationId",
        "access_levels": "accessLevels",
        "id": "id",
        "scoped_access_settings": "scopedAccessSettings",
        "session_settings": "sessionSettings",
        "timeouts": "timeouts",
    },
)
class AccessContextManagerGcpUserAccessBindingConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        group_key: builtins.str,
        organization_id: builtins.str,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        scoped_access_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessContextManagerGcpUserAccessBindingScopedAccessSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        session_settings: typing.Optional[typing.Union["AccessContextManagerGcpUserAccessBindingSessionSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AccessContextManagerGcpUserAccessBindingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param group_key: Required. Immutable. Google Group id whose members are subject to this binding's restrictions. See "id" in the G Suite Directory API's Groups resource. If a group's email address/alias is changed, this resource will continue to point at the changed group. This field does not accept group email addresses or aliases. Example: "01d520gv4vjcrht" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#group_key AccessContextManagerGcpUserAccessBinding#group_key}
        :param organization_id: Required. ID of the parent organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#organization_id AccessContextManagerGcpUserAccessBinding#organization_id}
        :param access_levels: Optional. Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#access_levels AccessContextManagerGcpUserAccessBinding#access_levels}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#id AccessContextManagerGcpUserAccessBinding#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scoped_access_settings: scoped_access_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#scoped_access_settings AccessContextManagerGcpUserAccessBinding#scoped_access_settings}
        :param session_settings: session_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_settings AccessContextManagerGcpUserAccessBinding#session_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#timeouts AccessContextManagerGcpUserAccessBinding#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(session_settings, dict):
            session_settings = AccessContextManagerGcpUserAccessBindingSessionSettings(**session_settings)
        if isinstance(timeouts, dict):
            timeouts = AccessContextManagerGcpUserAccessBindingTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f2a36d38b38360d45489be0eaab2d9689c2fba3fb5749b0f83c4cc3df051e1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument group_key", value=group_key, expected_type=type_hints["group_key"])
            check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
            check_type(argname="argument access_levels", value=access_levels, expected_type=type_hints["access_levels"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument scoped_access_settings", value=scoped_access_settings, expected_type=type_hints["scoped_access_settings"])
            check_type(argname="argument session_settings", value=session_settings, expected_type=type_hints["session_settings"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_key": group_key,
            "organization_id": organization_id,
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
        if access_levels is not None:
            self._values["access_levels"] = access_levels
        if id is not None:
            self._values["id"] = id
        if scoped_access_settings is not None:
            self._values["scoped_access_settings"] = scoped_access_settings
        if session_settings is not None:
            self._values["session_settings"] = session_settings
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
    def group_key(self) -> builtins.str:
        '''Required.

        Immutable. Google Group id whose members are subject to this binding's restrictions. See "id" in the G Suite Directory API's Groups resource. If a group's email address/alias is changed, this resource will continue to point at the changed group. This field does not accept group email addresses or aliases. Example: "01d520gv4vjcrht"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#group_key AccessContextManagerGcpUserAccessBinding#group_key}
        '''
        result = self._values.get("group_key")
        assert result is not None, "Required property 'group_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization_id(self) -> builtins.str:
        '''Required. ID of the parent organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#organization_id AccessContextManagerGcpUserAccessBinding#organization_id}
        '''
        result = self._values.get("organization_id")
        assert result is not None, "Required property 'organization_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#access_levels AccessContextManagerGcpUserAccessBinding#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#id AccessContextManagerGcpUserAccessBinding#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scoped_access_settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerGcpUserAccessBindingScopedAccessSettings"]]]:
        '''scoped_access_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#scoped_access_settings AccessContextManagerGcpUserAccessBinding#scoped_access_settings}
        '''
        result = self._values.get("scoped_access_settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessContextManagerGcpUserAccessBindingScopedAccessSettings"]]], result)

    @builtins.property
    def session_settings(
        self,
    ) -> typing.Optional["AccessContextManagerGcpUserAccessBindingSessionSettings"]:
        '''session_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_settings AccessContextManagerGcpUserAccessBinding#session_settings}
        '''
        result = self._values.get("session_settings")
        return typing.cast(typing.Optional["AccessContextManagerGcpUserAccessBindingSessionSettings"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["AccessContextManagerGcpUserAccessBindingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#timeouts AccessContextManagerGcpUserAccessBinding#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AccessContextManagerGcpUserAccessBindingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerGcpUserAccessBindingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettings",
    jsii_struct_bases=[],
    name_mapping={
        "active_settings": "activeSettings",
        "dry_run_settings": "dryRunSettings",
        "scope": "scope",
    },
)
class AccessContextManagerGcpUserAccessBindingScopedAccessSettings:
    def __init__(
        self,
        *,
        active_settings: typing.Optional[typing.Union["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        dry_run_settings: typing.Optional[typing.Union["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        scope: typing.Optional[typing.Union["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param active_settings: active_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#active_settings AccessContextManagerGcpUserAccessBinding#active_settings}
        :param dry_run_settings: dry_run_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#dry_run_settings AccessContextManagerGcpUserAccessBinding#dry_run_settings}
        :param scope: scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#scope AccessContextManagerGcpUserAccessBinding#scope}
        '''
        if isinstance(active_settings, dict):
            active_settings = AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings(**active_settings)
        if isinstance(dry_run_settings, dict):
            dry_run_settings = AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings(**dry_run_settings)
        if isinstance(scope, dict):
            scope = AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope(**scope)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5195c566261ba2492637888f0999c1f78c73c7eac3fd06c4a728a16344540412)
            check_type(argname="argument active_settings", value=active_settings, expected_type=type_hints["active_settings"])
            check_type(argname="argument dry_run_settings", value=dry_run_settings, expected_type=type_hints["dry_run_settings"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_settings is not None:
            self._values["active_settings"] = active_settings
        if dry_run_settings is not None:
            self._values["dry_run_settings"] = dry_run_settings
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def active_settings(
        self,
    ) -> typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings"]:
        '''active_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#active_settings AccessContextManagerGcpUserAccessBinding#active_settings}
        '''
        result = self._values.get("active_settings")
        return typing.cast(typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings"], result)

    @builtins.property
    def dry_run_settings(
        self,
    ) -> typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings"]:
        '''dry_run_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#dry_run_settings AccessContextManagerGcpUserAccessBinding#dry_run_settings}
        '''
        result = self._values.get("dry_run_settings")
        return typing.cast(typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings"], result)

    @builtins.property
    def scope(
        self,
    ) -> typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope"]:
        '''scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#scope AccessContextManagerGcpUserAccessBinding#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerGcpUserAccessBindingScopedAccessSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings",
    jsii_struct_bases=[],
    name_mapping={
        "access_levels": "accessLevels",
        "session_settings": "sessionSettings",
    },
)
class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings:
    def __init__(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_settings: typing.Optional[typing.Union["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: Optional. Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#access_levels AccessContextManagerGcpUserAccessBinding#access_levels}
        :param session_settings: session_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_settings AccessContextManagerGcpUserAccessBinding#session_settings}
        '''
        if isinstance(session_settings, dict):
            session_settings = AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings(**session_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4abc8c667ddda5800fa0d1ec52c296b525d8d893dff012d9fda537817f55173)
            check_type(argname="argument access_levels", value=access_levels, expected_type=type_hints["access_levels"])
            check_type(argname="argument session_settings", value=session_settings, expected_type=type_hints["session_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_levels is not None:
            self._values["access_levels"] = access_levels
        if session_settings is not None:
            self._values["session_settings"] = session_settings

    @builtins.property
    def access_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#access_levels AccessContextManagerGcpUserAccessBinding#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def session_settings(
        self,
    ) -> typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings"]:
        '''session_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_settings AccessContextManagerGcpUserAccessBinding#session_settings}
        '''
        result = self._values.get("session_settings")
        return typing.cast(typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f74951235c60bdc709457917d006a92d317b5055918e03f84b14e552d4ef715)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSessionSettings")
    def put_session_settings(
        self,
        *,
        max_inactivity: typing.Optional[builtins.str] = None,
        session_length: typing.Optional[builtins.str] = None,
        session_length_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_reauth_method: typing.Optional[builtins.str] = None,
        use_oidc_max_age: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param max_inactivity: Optional. How long a user is allowed to take between actions before a new access token must be issued. Only set for Google Cloud apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#max_inactivity AccessContextManagerGcpUserAccessBinding#max_inactivity}
        :param session_length: Optional. The session length. Setting this field to zero is equal to disabling session. Also can set infinite session by flipping the enabled bit to false below. If useOidcMaxAge is true, for OIDC apps, the session length will be the minimum of this field and OIDC max_age param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_length AccessContextManagerGcpUserAccessBinding#session_length}
        :param session_length_enabled: Optional. This field enables or disables Google Cloud session length. When false, all fields set above will be disregarded and the session length is basically infinite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_length_enabled AccessContextManagerGcpUserAccessBinding#session_length_enabled}
        :param session_reauth_method: Optional. The session challenges proposed to users when the Google Cloud session length is up. Possible values: ["LOGIN", "SECURITY_KEY", "PASSWORD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_reauth_method AccessContextManagerGcpUserAccessBinding#session_reauth_method}
        :param use_oidc_max_age: Optional. Only useful for OIDC apps. When false, the OIDC max_age param, if passed in the authentication request will be ignored. When true, the re-auth period will be the minimum of the sessionLength field and the max_age OIDC param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#use_oidc_max_age AccessContextManagerGcpUserAccessBinding#use_oidc_max_age}
        '''
        value = AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings(
            max_inactivity=max_inactivity,
            session_length=session_length,
            session_length_enabled=session_length_enabled,
            session_reauth_method=session_reauth_method,
            use_oidc_max_age=use_oidc_max_age,
        )

        return typing.cast(None, jsii.invoke(self, "putSessionSettings", [value]))

    @jsii.member(jsii_name="resetAccessLevels")
    def reset_access_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevels", []))

    @jsii.member(jsii_name="resetSessionSettings")
    def reset_session_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionSettings", []))

    @builtins.property
    @jsii.member(jsii_name="sessionSettings")
    def session_settings(
        self,
    ) -> "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettingsOutputReference":
        return typing.cast("AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettingsOutputReference", jsii.get(self, "sessionSettings"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelsInput")
    def access_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionSettingsInput")
    def session_settings_input(
        self,
    ) -> typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings"]:
        return typing.cast(typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings"], jsii.get(self, "sessionSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevels")
    def access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessLevels"))

    @access_levels.setter
    def access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b3d71c3ce59a05964c3f77e7e213aaa1a7e8d7774ee9303f03b8e977f4a8db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings]:
        return typing.cast(typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee8ce009dba6b55b18092e823fa2967146f762feb1424bd9f1c70d5c6ba3fd9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings",
    jsii_struct_bases=[],
    name_mapping={
        "max_inactivity": "maxInactivity",
        "session_length": "sessionLength",
        "session_length_enabled": "sessionLengthEnabled",
        "session_reauth_method": "sessionReauthMethod",
        "use_oidc_max_age": "useOidcMaxAge",
    },
)
class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings:
    def __init__(
        self,
        *,
        max_inactivity: typing.Optional[builtins.str] = None,
        session_length: typing.Optional[builtins.str] = None,
        session_length_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_reauth_method: typing.Optional[builtins.str] = None,
        use_oidc_max_age: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param max_inactivity: Optional. How long a user is allowed to take between actions before a new access token must be issued. Only set for Google Cloud apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#max_inactivity AccessContextManagerGcpUserAccessBinding#max_inactivity}
        :param session_length: Optional. The session length. Setting this field to zero is equal to disabling session. Also can set infinite session by flipping the enabled bit to false below. If useOidcMaxAge is true, for OIDC apps, the session length will be the minimum of this field and OIDC max_age param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_length AccessContextManagerGcpUserAccessBinding#session_length}
        :param session_length_enabled: Optional. This field enables or disables Google Cloud session length. When false, all fields set above will be disregarded and the session length is basically infinite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_length_enabled AccessContextManagerGcpUserAccessBinding#session_length_enabled}
        :param session_reauth_method: Optional. The session challenges proposed to users when the Google Cloud session length is up. Possible values: ["LOGIN", "SECURITY_KEY", "PASSWORD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_reauth_method AccessContextManagerGcpUserAccessBinding#session_reauth_method}
        :param use_oidc_max_age: Optional. Only useful for OIDC apps. When false, the OIDC max_age param, if passed in the authentication request will be ignored. When true, the re-auth period will be the minimum of the sessionLength field and the max_age OIDC param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#use_oidc_max_age AccessContextManagerGcpUserAccessBinding#use_oidc_max_age}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce225d1e620356d1be4b7f8b755c4a0a40b49983771fc1fe9bb35ecf05f6e53)
            check_type(argname="argument max_inactivity", value=max_inactivity, expected_type=type_hints["max_inactivity"])
            check_type(argname="argument session_length", value=session_length, expected_type=type_hints["session_length"])
            check_type(argname="argument session_length_enabled", value=session_length_enabled, expected_type=type_hints["session_length_enabled"])
            check_type(argname="argument session_reauth_method", value=session_reauth_method, expected_type=type_hints["session_reauth_method"])
            check_type(argname="argument use_oidc_max_age", value=use_oidc_max_age, expected_type=type_hints["use_oidc_max_age"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_inactivity is not None:
            self._values["max_inactivity"] = max_inactivity
        if session_length is not None:
            self._values["session_length"] = session_length
        if session_length_enabled is not None:
            self._values["session_length_enabled"] = session_length_enabled
        if session_reauth_method is not None:
            self._values["session_reauth_method"] = session_reauth_method
        if use_oidc_max_age is not None:
            self._values["use_oidc_max_age"] = use_oidc_max_age

    @builtins.property
    def max_inactivity(self) -> typing.Optional[builtins.str]:
        '''Optional.

        How long a user is allowed to take between actions before a new access token must be issued. Only set for Google Cloud apps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#max_inactivity AccessContextManagerGcpUserAccessBinding#max_inactivity}
        '''
        result = self._values.get("max_inactivity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_length(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The session length. Setting this field to zero is equal to disabling session. Also can set infinite session by flipping the enabled bit to false below. If useOidcMaxAge is true, for OIDC apps, the session length will be the minimum of this field and OIDC max_age param.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_length AccessContextManagerGcpUserAccessBinding#session_length}
        '''
        result = self._values.get("session_length")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_length_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        This field enables or disables Google Cloud session length. When false, all fields set above will be disregarded and the session length is basically infinite.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_length_enabled AccessContextManagerGcpUserAccessBinding#session_length_enabled}
        '''
        result = self._values.get("session_length_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def session_reauth_method(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The session challenges proposed to users when the Google Cloud session length is up. Possible values: ["LOGIN", "SECURITY_KEY", "PASSWORD"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_reauth_method AccessContextManagerGcpUserAccessBinding#session_reauth_method}
        '''
        result = self._values.get("session_reauth_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_oidc_max_age(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Only useful for OIDC apps. When false, the OIDC max_age param, if passed in the authentication request will be ignored. When true, the re-auth period will be the minimum of the sessionLength field and the max_age OIDC param.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#use_oidc_max_age AccessContextManagerGcpUserAccessBinding#use_oidc_max_age}
        '''
        result = self._values.get("use_oidc_max_age")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4e724ce03342ad7ef9ab3141ce6a31825c40675c360f59b8204b1a2f688d9c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxInactivity")
    def reset_max_inactivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInactivity", []))

    @jsii.member(jsii_name="resetSessionLength")
    def reset_session_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionLength", []))

    @jsii.member(jsii_name="resetSessionLengthEnabled")
    def reset_session_length_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionLengthEnabled", []))

    @jsii.member(jsii_name="resetSessionReauthMethod")
    def reset_session_reauth_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionReauthMethod", []))

    @jsii.member(jsii_name="resetUseOidcMaxAge")
    def reset_use_oidc_max_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseOidcMaxAge", []))

    @builtins.property
    @jsii.member(jsii_name="maxInactivityInput")
    def max_inactivity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxInactivityInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionLengthEnabledInput")
    def session_length_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sessionLengthEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionLengthInput")
    def session_length_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionReauthMethodInput")
    def session_reauth_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionReauthMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="useOidcMaxAgeInput")
    def use_oidc_max_age_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useOidcMaxAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInactivity")
    def max_inactivity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxInactivity"))

    @max_inactivity.setter
    def max_inactivity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b95bce46e64b5aeededb8f39828523166169b55ebad91b2fa1b770b8c693053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInactivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionLength")
    def session_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionLength"))

    @session_length.setter
    def session_length(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c048a7238005eac82da543b0f76ff2e244b86c4f13c4ed9bb0c19387e2bb238a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionLengthEnabled")
    def session_length_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sessionLengthEnabled"))

    @session_length_enabled.setter
    def session_length_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54449a1c21cc4bdc29f86162fd7331d56ef14743dfd22e6d4874f843f8b1536b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionLengthEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionReauthMethod")
    def session_reauth_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionReauthMethod"))

    @session_reauth_method.setter
    def session_reauth_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4570dd722f8a6d6ed362ef224215fd087ba287876af2e342366d36498ac5cabe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionReauthMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useOidcMaxAge")
    def use_oidc_max_age(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useOidcMaxAge"))

    @use_oidc_max_age.setter
    def use_oidc_max_age(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79354a57f03e15a8a2be7e2925b92da4441bc9e029ab2b776446e458bb4745b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useOidcMaxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings]:
        return typing.cast(typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c658d656a6d000416b34424bfe85eba3a05bf8b6b8f7c1ed67a8b47950129b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings",
    jsii_struct_bases=[],
    name_mapping={"access_levels": "accessLevels"},
)
class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings:
    def __init__(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_levels: Optional. Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#access_levels AccessContextManagerGcpUserAccessBinding#access_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a6870f5594b8c9b074d966ed7b80acd86f08ca48fe6cf7250a32a6fafb22d09)
            check_type(argname="argument access_levels", value=access_levels, expected_type=type_hints["access_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_levels is not None:
            self._values["access_levels"] = access_levels

    @builtins.property
    def access_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#access_levels AccessContextManagerGcpUserAccessBinding#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a661b331389769c7ebb91644fade6192159bf014453c0257aa127fb296c8dfda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessLevels")
    def reset_access_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessLevels", []))

    @builtins.property
    @jsii.member(jsii_name="accessLevelsInput")
    def access_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevels")
    def access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessLevels"))

    @access_levels.setter
    def access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__233ac1247eae6e14a507620b1dc895c2f35fca95e306728ca27782c140a5e666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings]:
        return typing.cast(typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510b69dcebfc20dd75a5fa1fc9067d0660962d81dd413f920169bb97748827ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab7d861dd4c6c332b6f723be1d0e33731971c86f7ce7ae2d7aa2ad5b6a9987f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f133f901bf382ec9f0fd154a342525aeb4d50658162bdc923cd1e62092592c03)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessContextManagerGcpUserAccessBindingScopedAccessSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4501011107e6b6fb7ba92556b115d9d8ec7e89bb116fe9735734055006520ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a2fd1ca2ffcf86a27536f43dc9a300fab8ac2f174659051f96de2980b2f1d99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__021a74c0c77f6fc0ad92bc63430275cb34b15e97faf177c04ced26ee8746fdb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerGcpUserAccessBindingScopedAccessSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerGcpUserAccessBindingScopedAccessSettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerGcpUserAccessBindingScopedAccessSettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28fe1d2f3ac3b02e15b10442684cc68e082bfe6b51d40a4c12bc1c18eff45a0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f12da91f75578d77c2002d14cec3e7b928bbffabcfd0d40d102812a0f62a8850)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putActiveSettings")
    def put_active_settings(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_settings: typing.Optional[typing.Union[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: Optional. Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#access_levels AccessContextManagerGcpUserAccessBinding#access_levels}
        :param session_settings: session_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_settings AccessContextManagerGcpUserAccessBinding#session_settings}
        '''
        value = AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings(
            access_levels=access_levels, session_settings=session_settings
        )

        return typing.cast(None, jsii.invoke(self, "putActiveSettings", [value]))

    @jsii.member(jsii_name="putDryRunSettings")
    def put_dry_run_settings(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_levels: Optional. Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#access_levels AccessContextManagerGcpUserAccessBinding#access_levels}
        '''
        value = AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings(
            access_levels=access_levels
        )

        return typing.cast(None, jsii.invoke(self, "putDryRunSettings", [value]))

    @jsii.member(jsii_name="putScope")
    def put_scope(
        self,
        *,
        client_scope: typing.Optional[typing.Union["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_scope: client_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#client_scope AccessContextManagerGcpUserAccessBinding#client_scope}
        '''
        value = AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope(
            client_scope=client_scope
        )

        return typing.cast(None, jsii.invoke(self, "putScope", [value]))

    @jsii.member(jsii_name="resetActiveSettings")
    def reset_active_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveSettings", []))

    @jsii.member(jsii_name="resetDryRunSettings")
    def reset_dry_run_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDryRunSettings", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @builtins.property
    @jsii.member(jsii_name="activeSettings")
    def active_settings(
        self,
    ) -> AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsOutputReference:
        return typing.cast(AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsOutputReference, jsii.get(self, "activeSettings"))

    @builtins.property
    @jsii.member(jsii_name="dryRunSettings")
    def dry_run_settings(
        self,
    ) -> AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettingsOutputReference:
        return typing.cast(AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettingsOutputReference, jsii.get(self, "dryRunSettings"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(
        self,
    ) -> "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeOutputReference":
        return typing.cast("AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeOutputReference", jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="activeSettingsInput")
    def active_settings_input(
        self,
    ) -> typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings]:
        return typing.cast(typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings], jsii.get(self, "activeSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="dryRunSettingsInput")
    def dry_run_settings_input(
        self,
    ) -> typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings]:
        return typing.cast(typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings], jsii.get(self, "dryRunSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(
        self,
    ) -> typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope"]:
        return typing.cast(typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope"], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerGcpUserAccessBindingScopedAccessSettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerGcpUserAccessBindingScopedAccessSettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerGcpUserAccessBindingScopedAccessSettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b56a28111efac6b1ad56a9c0e7621d884c9c94bf5875ebc68f9b1847a028585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope",
    jsii_struct_bases=[],
    name_mapping={"client_scope": "clientScope"},
)
class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope:
    def __init__(
        self,
        *,
        client_scope: typing.Optional[typing.Union["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_scope: client_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#client_scope AccessContextManagerGcpUserAccessBinding#client_scope}
        '''
        if isinstance(client_scope, dict):
            client_scope = AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope(**client_scope)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63c13a3e0b07d6a6bffffd2ea384a7ab84d40c761f822d401e75eae71754872)
            check_type(argname="argument client_scope", value=client_scope, expected_type=type_hints["client_scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_scope is not None:
            self._values["client_scope"] = client_scope

    @builtins.property
    def client_scope(
        self,
    ) -> typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope"]:
        '''client_scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#client_scope AccessContextManagerGcpUserAccessBinding#client_scope}
        '''
        result = self._values.get("client_scope")
        return typing.cast(typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope",
    jsii_struct_bases=[],
    name_mapping={"restricted_client_application": "restrictedClientApplication"},
)
class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope:
    def __init__(
        self,
        *,
        restricted_client_application: typing.Optional[typing.Union["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param restricted_client_application: restricted_client_application block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#restricted_client_application AccessContextManagerGcpUserAccessBinding#restricted_client_application}
        '''
        if isinstance(restricted_client_application, dict):
            restricted_client_application = AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication(**restricted_client_application)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d13d2a8e6f60af1e6d2dee3e9da911fc81b55259a8d9c8093025cd530509c27)
            check_type(argname="argument restricted_client_application", value=restricted_client_application, expected_type=type_hints["restricted_client_application"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if restricted_client_application is not None:
            self._values["restricted_client_application"] = restricted_client_application

    @builtins.property
    def restricted_client_application(
        self,
    ) -> typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication"]:
        '''restricted_client_application block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#restricted_client_application AccessContextManagerGcpUserAccessBinding#restricted_client_application}
        '''
        result = self._values.get("restricted_client_application")
        return typing.cast(typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfe665b57d8c9a193e7016c09cfe75e30c2a65fc33af0e89c5fe3c63f5de62a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRestrictedClientApplication")
    def put_restricted_client_application(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The OAuth client ID of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#client_id AccessContextManagerGcpUserAccessBinding#client_id}
        :param name: The name of the application. Example: "Cloud Console". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#name AccessContextManagerGcpUserAccessBinding#name}
        '''
        value = AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication(
            client_id=client_id, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putRestrictedClientApplication", [value]))

    @jsii.member(jsii_name="resetRestrictedClientApplication")
    def reset_restricted_client_application(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedClientApplication", []))

    @builtins.property
    @jsii.member(jsii_name="restrictedClientApplication")
    def restricted_client_application(
        self,
    ) -> "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplicationOutputReference":
        return typing.cast("AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplicationOutputReference", jsii.get(self, "restrictedClientApplication"))

    @builtins.property
    @jsii.member(jsii_name="restrictedClientApplicationInput")
    def restricted_client_application_input(
        self,
    ) -> typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication"]:
        return typing.cast(typing.Optional["AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication"], jsii.get(self, "restrictedClientApplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope]:
        return typing.cast(typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6184803ed0e30c99a3b7bdc05fb51819dbe50b09113393e53b483ab9861e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "name": "name"},
)
class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication:
    def __init__(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The OAuth client ID of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#client_id AccessContextManagerGcpUserAccessBinding#client_id}
        :param name: The name of the application. Example: "Cloud Console". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#name AccessContextManagerGcpUserAccessBinding#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fc1c55667fd795af85d327a6cd5709d089eca8da9494870106d0d3a5bba53d)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The OAuth client ID of the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#client_id AccessContextManagerGcpUserAccessBinding#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application. Example: "Cloud Console".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#name AccessContextManagerGcpUserAccessBinding#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afa0dcdad85564afdd1bd725b116094d7e90f14c630fa402458e56518fdeb41e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b2f927dc296ea1267bc0c72f1372b5d7284f31c98cc23fdf90305807bbf577d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8284d18ed297d17fad25a675a540fad308c4424579eadd2c9ca7320b92678c33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication]:
        return typing.cast(typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb80c12daf5a1bad38d7748ac45822dc0c9ddb49298af3f9c712476e374eb640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b39ab1e7f019bae4fa5f90cb77629a08253b403ff6ab6c68b2c1dbc084354bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientScope")
    def put_client_scope(
        self,
        *,
        restricted_client_application: typing.Optional[typing.Union[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param restricted_client_application: restricted_client_application block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#restricted_client_application AccessContextManagerGcpUserAccessBinding#restricted_client_application}
        '''
        value = AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope(
            restricted_client_application=restricted_client_application
        )

        return typing.cast(None, jsii.invoke(self, "putClientScope", [value]))

    @jsii.member(jsii_name="resetClientScope")
    def reset_client_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientScope", []))

    @builtins.property
    @jsii.member(jsii_name="clientScope")
    def client_scope(
        self,
    ) -> AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeOutputReference:
        return typing.cast(AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeOutputReference, jsii.get(self, "clientScope"))

    @builtins.property
    @jsii.member(jsii_name="clientScopeInput")
    def client_scope_input(
        self,
    ) -> typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope]:
        return typing.cast(typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope], jsii.get(self, "clientScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope]:
        return typing.cast(typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da809c597a31a712e604dd5d00d1a1ab143f6ce8915534c821f99ac9f6a3df5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingSessionSettings",
    jsii_struct_bases=[],
    name_mapping={
        "max_inactivity": "maxInactivity",
        "session_length": "sessionLength",
        "session_length_enabled": "sessionLengthEnabled",
        "session_reauth_method": "sessionReauthMethod",
        "use_oidc_max_age": "useOidcMaxAge",
    },
)
class AccessContextManagerGcpUserAccessBindingSessionSettings:
    def __init__(
        self,
        *,
        max_inactivity: typing.Optional[builtins.str] = None,
        session_length: typing.Optional[builtins.str] = None,
        session_length_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_reauth_method: typing.Optional[builtins.str] = None,
        use_oidc_max_age: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param max_inactivity: Optional. How long a user is allowed to take between actions before a new access token must be issued. Only set for Google Cloud apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#max_inactivity AccessContextManagerGcpUserAccessBinding#max_inactivity}
        :param session_length: Optional. The session length. Setting this field to zero is equal to disabling session. Also can set infinite session by flipping the enabled bit to false below. If useOidcMaxAge is true, for OIDC apps, the session length will be the minimum of this field and OIDC max_age param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_length AccessContextManagerGcpUserAccessBinding#session_length}
        :param session_length_enabled: Optional. This field enables or disables Google Cloud session length. When false, all fields set above will be disregarded and the session length is basically infinite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_length_enabled AccessContextManagerGcpUserAccessBinding#session_length_enabled}
        :param session_reauth_method: Optional. The session challenges proposed to users when the Google Cloud session length is up. Possible values: ["LOGIN", "SECURITY_KEY", "PASSWORD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_reauth_method AccessContextManagerGcpUserAccessBinding#session_reauth_method}
        :param use_oidc_max_age: Optional. Only useful for OIDC apps. When false, the OIDC max_age param, if passed in the authentication request will be ignored. When true, the re-auth period will be the minimum of the sessionLength field and the max_age OIDC param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#use_oidc_max_age AccessContextManagerGcpUserAccessBinding#use_oidc_max_age}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c2982884e2382942312539ace966b67f8e255e21e5d24c48f9449cfd8e340f)
            check_type(argname="argument max_inactivity", value=max_inactivity, expected_type=type_hints["max_inactivity"])
            check_type(argname="argument session_length", value=session_length, expected_type=type_hints["session_length"])
            check_type(argname="argument session_length_enabled", value=session_length_enabled, expected_type=type_hints["session_length_enabled"])
            check_type(argname="argument session_reauth_method", value=session_reauth_method, expected_type=type_hints["session_reauth_method"])
            check_type(argname="argument use_oidc_max_age", value=use_oidc_max_age, expected_type=type_hints["use_oidc_max_age"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_inactivity is not None:
            self._values["max_inactivity"] = max_inactivity
        if session_length is not None:
            self._values["session_length"] = session_length
        if session_length_enabled is not None:
            self._values["session_length_enabled"] = session_length_enabled
        if session_reauth_method is not None:
            self._values["session_reauth_method"] = session_reauth_method
        if use_oidc_max_age is not None:
            self._values["use_oidc_max_age"] = use_oidc_max_age

    @builtins.property
    def max_inactivity(self) -> typing.Optional[builtins.str]:
        '''Optional.

        How long a user is allowed to take between actions before a new access token must be issued. Only set for Google Cloud apps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#max_inactivity AccessContextManagerGcpUserAccessBinding#max_inactivity}
        '''
        result = self._values.get("max_inactivity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_length(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The session length. Setting this field to zero is equal to disabling session. Also can set infinite session by flipping the enabled bit to false below. If useOidcMaxAge is true, for OIDC apps, the session length will be the minimum of this field and OIDC max_age param.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_length AccessContextManagerGcpUserAccessBinding#session_length}
        '''
        result = self._values.get("session_length")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_length_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        This field enables or disables Google Cloud session length. When false, all fields set above will be disregarded and the session length is basically infinite.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_length_enabled AccessContextManagerGcpUserAccessBinding#session_length_enabled}
        '''
        result = self._values.get("session_length_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def session_reauth_method(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The session challenges proposed to users when the Google Cloud session length is up. Possible values: ["LOGIN", "SECURITY_KEY", "PASSWORD"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#session_reauth_method AccessContextManagerGcpUserAccessBinding#session_reauth_method}
        '''
        result = self._values.get("session_reauth_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_oidc_max_age(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Only useful for OIDC apps. When false, the OIDC max_age param, if passed in the authentication request will be ignored. When true, the re-auth period will be the minimum of the sessionLength field and the max_age OIDC param.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#use_oidc_max_age AccessContextManagerGcpUserAccessBinding#use_oidc_max_age}
        '''
        result = self._values.get("use_oidc_max_age")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerGcpUserAccessBindingSessionSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerGcpUserAccessBindingSessionSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingSessionSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e82b4283ae6f2fcc78691ffefa1c321aff1549212237e218bd55cdb457d01ff6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxInactivity")
    def reset_max_inactivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInactivity", []))

    @jsii.member(jsii_name="resetSessionLength")
    def reset_session_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionLength", []))

    @jsii.member(jsii_name="resetSessionLengthEnabled")
    def reset_session_length_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionLengthEnabled", []))

    @jsii.member(jsii_name="resetSessionReauthMethod")
    def reset_session_reauth_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionReauthMethod", []))

    @jsii.member(jsii_name="resetUseOidcMaxAge")
    def reset_use_oidc_max_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseOidcMaxAge", []))

    @builtins.property
    @jsii.member(jsii_name="maxInactivityInput")
    def max_inactivity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxInactivityInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionLengthEnabledInput")
    def session_length_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sessionLengthEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionLengthInput")
    def session_length_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionReauthMethodInput")
    def session_reauth_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionReauthMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="useOidcMaxAgeInput")
    def use_oidc_max_age_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useOidcMaxAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInactivity")
    def max_inactivity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxInactivity"))

    @max_inactivity.setter
    def max_inactivity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31be4e707b24c44bbffddbfc0aa29d2d6431b59f4a7f78de40e6baa7d84c0d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInactivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionLength")
    def session_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionLength"))

    @session_length.setter
    def session_length(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7849f5c869681af6969412e2eafc684b4c46f55f76bc5b8a58a83b8b3e5e8af2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionLengthEnabled")
    def session_length_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sessionLengthEnabled"))

    @session_length_enabled.setter
    def session_length_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9bab1006255e9aa1006c37da85f2ed837d289dce70f967133f4acf5bdd78bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionLengthEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionReauthMethod")
    def session_reauth_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionReauthMethod"))

    @session_reauth_method.setter
    def session_reauth_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306435d2f699876cf3fdf8b2c50a7e26e68cef4ed7372f1010c1f218c3097e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionReauthMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useOidcMaxAge")
    def use_oidc_max_age(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useOidcMaxAge"))

    @use_oidc_max_age.setter
    def use_oidc_max_age(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20cbeb4273e4cbbf94e1fff1160a71242337126c1f002fe2d6637c3bd776fb80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useOidcMaxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessContextManagerGcpUserAccessBindingSessionSettings]:
        return typing.cast(typing.Optional[AccessContextManagerGcpUserAccessBindingSessionSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessContextManagerGcpUserAccessBindingSessionSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1df56a1f3da0c172cf750b72d67e3e06ec745df2c215b53ae439433e3c93f48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AccessContextManagerGcpUserAccessBindingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#create AccessContextManagerGcpUserAccessBinding#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#delete AccessContextManagerGcpUserAccessBinding#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#update AccessContextManagerGcpUserAccessBinding#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819a427524b390739c361ab9e4e4706ce16818b08541007a66659ebbf3be786a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#create AccessContextManagerGcpUserAccessBinding#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#delete AccessContextManagerGcpUserAccessBinding#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/access_context_manager_gcp_user_access_binding#update AccessContextManagerGcpUserAccessBinding#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessContextManagerGcpUserAccessBindingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessContextManagerGcpUserAccessBindingTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.accessContextManagerGcpUserAccessBinding.AccessContextManagerGcpUserAccessBindingTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68c8017df5db117ce93d4f807e1ac58570302f402524022deef933667b2221e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6527442ed3a55f27ba2f38b41077693d2b60661a789bbd49d15646870cba549c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0710383e37d4d9f05ca1d0b828f3a681fb7858ebb4bc2c194f07323e5d52b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef7ceecf3554e9ed68d4da301a16dc062814f5f7615366d23fd3127a1d9e2edb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerGcpUserAccessBindingTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerGcpUserAccessBindingTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerGcpUserAccessBindingTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36bc7a743898e7cc33befa0208ea5ae0d13168a11e4b2baeb931cc11ff99757b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessContextManagerGcpUserAccessBinding",
    "AccessContextManagerGcpUserAccessBindingConfig",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettings",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsOutputReference",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettingsOutputReference",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettingsOutputReference",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsList",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsOutputReference",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeOutputReference",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplicationOutputReference",
    "AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeOutputReference",
    "AccessContextManagerGcpUserAccessBindingSessionSettings",
    "AccessContextManagerGcpUserAccessBindingSessionSettingsOutputReference",
    "AccessContextManagerGcpUserAccessBindingTimeouts",
    "AccessContextManagerGcpUserAccessBindingTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__889ea81f81401bfde8d61166d72730feb49d5ecefac0189d077741a0880209ec(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    group_key: builtins.str,
    organization_id: builtins.str,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    scoped_access_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerGcpUserAccessBindingScopedAccessSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    session_settings: typing.Optional[typing.Union[AccessContextManagerGcpUserAccessBindingSessionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerGcpUserAccessBindingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6b07c9c3efc6358dea4bb527963e93898a58e47929ba49459aaafd7627436cfc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec482f15aeaa81c559f914a6eca0c7b5d811eb96a1b0df1154acb65e015098c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerGcpUserAccessBindingScopedAccessSettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a191fb52320d18773dad2f54f3c5ec6db30d54e8e3c3065f870f1f088214b55(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5c38fe74065a471e17bbfd3353828d3ffe2a1f5fe3b10224ee0fca487e60b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b68b291408d496c8ee8bbddf1b4cd10ea4002fd36098b2524a516279680f618(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273b2491be50ff66e9e28cffa54086d71e84c6edca67b40ba116fa80a59958ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f2a36d38b38360d45489be0eaab2d9689c2fba3fb5749b0f83c4cc3df051e1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group_key: builtins.str,
    organization_id: builtins.str,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    scoped_access_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessContextManagerGcpUserAccessBindingScopedAccessSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    session_settings: typing.Optional[typing.Union[AccessContextManagerGcpUserAccessBindingSessionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AccessContextManagerGcpUserAccessBindingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5195c566261ba2492637888f0999c1f78c73c7eac3fd06c4a728a16344540412(
    *,
    active_settings: typing.Optional[typing.Union[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    dry_run_settings: typing.Optional[typing.Union[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    scope: typing.Optional[typing.Union[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4abc8c667ddda5800fa0d1ec52c296b525d8d893dff012d9fda537817f55173(
    *,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_settings: typing.Optional[typing.Union[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f74951235c60bdc709457917d006a92d317b5055918e03f84b14e552d4ef715(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b3d71c3ce59a05964c3f77e7e213aaa1a7e8d7774ee9303f03b8e977f4a8db(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee8ce009dba6b55b18092e823fa2967146f762feb1424bd9f1c70d5c6ba3fd9e(
    value: typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce225d1e620356d1be4b7f8b755c4a0a40b49983771fc1fe9bb35ecf05f6e53(
    *,
    max_inactivity: typing.Optional[builtins.str] = None,
    session_length: typing.Optional[builtins.str] = None,
    session_length_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_reauth_method: typing.Optional[builtins.str] = None,
    use_oidc_max_age: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e724ce03342ad7ef9ab3141ce6a31825c40675c360f59b8204b1a2f688d9c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b95bce46e64b5aeededb8f39828523166169b55ebad91b2fa1b770b8c693053(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c048a7238005eac82da543b0f76ff2e244b86c4f13c4ed9bb0c19387e2bb238a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54449a1c21cc4bdc29f86162fd7331d56ef14743dfd22e6d4874f843f8b1536b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4570dd722f8a6d6ed362ef224215fd087ba287876af2e342366d36498ac5cabe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79354a57f03e15a8a2be7e2925b92da4441bc9e029ab2b776446e458bb4745b4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c658d656a6d000416b34424bfe85eba3a05bf8b6b8f7c1ed67a8b47950129b7(
    value: typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6870f5594b8c9b074d966ed7b80acd86f08ca48fe6cf7250a32a6fafb22d09(
    *,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a661b331389769c7ebb91644fade6192159bf014453c0257aa127fb296c8dfda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233ac1247eae6e14a507620b1dc895c2f35fca95e306728ca27782c140a5e666(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510b69dcebfc20dd75a5fa1fc9067d0660962d81dd413f920169bb97748827ba(
    value: typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7d861dd4c6c332b6f723be1d0e33731971c86f7ce7ae2d7aa2ad5b6a9987f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f133f901bf382ec9f0fd154a342525aeb4d50658162bdc923cd1e62092592c03(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4501011107e6b6fb7ba92556b115d9d8ec7e89bb116fe9735734055006520ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2fd1ca2ffcf86a27536f43dc9a300fab8ac2f174659051f96de2980b2f1d99(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021a74c0c77f6fc0ad92bc63430275cb34b15e97faf177c04ced26ee8746fdb6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fe1d2f3ac3b02e15b10442684cc68e082bfe6b51d40a4c12bc1c18eff45a0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessContextManagerGcpUserAccessBindingScopedAccessSettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12da91f75578d77c2002d14cec3e7b928bbffabcfd0d40d102812a0f62a8850(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b56a28111efac6b1ad56a9c0e7621d884c9c94bf5875ebc68f9b1847a028585(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerGcpUserAccessBindingScopedAccessSettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63c13a3e0b07d6a6bffffd2ea384a7ab84d40c761f822d401e75eae71754872(
    *,
    client_scope: typing.Optional[typing.Union[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d13d2a8e6f60af1e6d2dee3e9da911fc81b55259a8d9c8093025cd530509c27(
    *,
    restricted_client_application: typing.Optional[typing.Union[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe665b57d8c9a193e7016c09cfe75e30c2a65fc33af0e89c5fe3c63f5de62a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6184803ed0e30c99a3b7bdc05fb51819dbe50b09113393e53b483ab9861e68(
    value: typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fc1c55667fd795af85d327a6cd5709d089eca8da9494870106d0d3a5bba53d(
    *,
    client_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa0dcdad85564afdd1bd725b116094d7e90f14c630fa402458e56518fdeb41e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2f927dc296ea1267bc0c72f1372b5d7284f31c98cc23fdf90305807bbf577d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8284d18ed297d17fad25a675a540fad308c4424579eadd2c9ca7320b92678c33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb80c12daf5a1bad38d7748ac45822dc0c9ddb49298af3f9c712476e374eb640(
    value: typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b39ab1e7f019bae4fa5f90cb77629a08253b403ff6ab6c68b2c1dbc084354bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da809c597a31a712e604dd5d00d1a1ab143f6ce8915534c821f99ac9f6a3df5(
    value: typing.Optional[AccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c2982884e2382942312539ace966b67f8e255e21e5d24c48f9449cfd8e340f(
    *,
    max_inactivity: typing.Optional[builtins.str] = None,
    session_length: typing.Optional[builtins.str] = None,
    session_length_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_reauth_method: typing.Optional[builtins.str] = None,
    use_oidc_max_age: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82b4283ae6f2fcc78691ffefa1c321aff1549212237e218bd55cdb457d01ff6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31be4e707b24c44bbffddbfc0aa29d2d6431b59f4a7f78de40e6baa7d84c0d4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7849f5c869681af6969412e2eafc684b4c46f55f76bc5b8a58a83b8b3e5e8af2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9bab1006255e9aa1006c37da85f2ed837d289dce70f967133f4acf5bdd78bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306435d2f699876cf3fdf8b2c50a7e26e68cef4ed7372f1010c1f218c3097e73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20cbeb4273e4cbbf94e1fff1160a71242337126c1f002fe2d6637c3bd776fb80(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1df56a1f3da0c172cf750b72d67e3e06ec745df2c215b53ae439433e3c93f48(
    value: typing.Optional[AccessContextManagerGcpUserAccessBindingSessionSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819a427524b390739c361ab9e4e4706ce16818b08541007a66659ebbf3be786a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c8017df5db117ce93d4f807e1ac58570302f402524022deef933667b2221e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6527442ed3a55f27ba2f38b41077693d2b60661a789bbd49d15646870cba549c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0710383e37d4d9f05ca1d0b828f3a681fb7858ebb4bc2c194f07323e5d52b34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7ceecf3554e9ed68d4da301a16dc062814f5f7615366d23fd3127a1d9e2edb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36bc7a743898e7cc33befa0208ea5ae0d13168a11e4b2baeb931cc11ff99757b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessContextManagerGcpUserAccessBindingTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
