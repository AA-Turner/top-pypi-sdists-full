r'''
# `google_access_context_manager_gcp_user_access_binding`

Refer to the Terraform Registry for docs: [`google_access_context_manager_gcp_user_access_binding`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding).
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


class GoogleAccessContextManagerGcpUserAccessBinding(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBinding",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding google_access_context_manager_gcp_user_access_binding}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        group_key: builtins.str,
        organization_id: builtins.str,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        scoped_access_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        session_settings: typing.Optional[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingSessionSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding google_access_context_manager_gcp_user_access_binding} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param group_key: Required. Immutable. Google Group id whose members are subject to this binding's restrictions. See "id" in the G Suite Directory API's Groups resource. If a group's email address/alias is changed, this resource will continue to point at the changed group. This field does not accept group email addresses or aliases. Example: "01d520gv4vjcrht" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#group_key GoogleAccessContextManagerGcpUserAccessBinding#group_key}
        :param organization_id: Required. ID of the parent organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#organization_id GoogleAccessContextManagerGcpUserAccessBinding#organization_id}
        :param access_levels: Optional. Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#access_levels GoogleAccessContextManagerGcpUserAccessBinding#access_levels}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#id GoogleAccessContextManagerGcpUserAccessBinding#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scoped_access_settings: scoped_access_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#scoped_access_settings GoogleAccessContextManagerGcpUserAccessBinding#scoped_access_settings}
        :param session_settings: session_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_settings GoogleAccessContextManagerGcpUserAccessBinding#session_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#timeouts GoogleAccessContextManagerGcpUserAccessBinding#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3563eef857c9b90c264366ee0b2362f0d585af4e1d61b13e9ce404a08d57a402)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleAccessContextManagerGcpUserAccessBindingConfig(
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
        '''Generates CDKTF code for importing a GoogleAccessContextManagerGcpUserAccessBinding resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleAccessContextManagerGcpUserAccessBinding to import.
        :param import_from_id: The id of the existing GoogleAccessContextManagerGcpUserAccessBinding that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleAccessContextManagerGcpUserAccessBinding to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02bd0507e6a822815cb9667fa1f57848357d38499994dfa354b6214bdd18950f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putScopedAccessSettings")
    def put_scoped_access_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be3ddd5757d21b49c47ad4538eadcebb1d474c444e8424d79452a1d2f90cfe1)
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
        :param max_inactivity: Optional. How long a user is allowed to take between actions before a new access token must be issued. Only set for Google Cloud apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#max_inactivity GoogleAccessContextManagerGcpUserAccessBinding#max_inactivity}
        :param session_length: Optional. The session length. Setting this field to zero is equal to disabling session. Also can set infinite session by flipping the enabled bit to false below. If useOidcMaxAge is true, for OIDC apps, the session length will be the minimum of this field and OIDC max_age param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_length GoogleAccessContextManagerGcpUserAccessBinding#session_length}
        :param session_length_enabled: Optional. This field enables or disables Google Cloud session length. When false, all fields set above will be disregarded and the session length is basically infinite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_length_enabled GoogleAccessContextManagerGcpUserAccessBinding#session_length_enabled}
        :param session_reauth_method: Optional. The session challenges proposed to users when the Google Cloud session length is up. Possible values: ["LOGIN", "SECURITY_KEY", "PASSWORD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_reauth_method GoogleAccessContextManagerGcpUserAccessBinding#session_reauth_method}
        :param use_oidc_max_age: Optional. Only useful for OIDC apps. When false, the OIDC max_age param, if passed in the authentication request will be ignored. When true, the re-auth period will be the minimum of the sessionLength field and the max_age OIDC param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#use_oidc_max_age GoogleAccessContextManagerGcpUserAccessBinding#use_oidc_max_age}
        '''
        value = GoogleAccessContextManagerGcpUserAccessBindingSessionSettings(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#create GoogleAccessContextManagerGcpUserAccessBinding#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#delete GoogleAccessContextManagerGcpUserAccessBinding#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#update GoogleAccessContextManagerGcpUserAccessBinding#update}.
        '''
        value = GoogleAccessContextManagerGcpUserAccessBindingTimeouts(
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
    ) -> "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsList":
        return typing.cast("GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsList", jsii.get(self, "scopedAccessSettings"))

    @builtins.property
    @jsii.member(jsii_name="sessionSettings")
    def session_settings(
        self,
    ) -> "GoogleAccessContextManagerGcpUserAccessBindingSessionSettingsOutputReference":
        return typing.cast("GoogleAccessContextManagerGcpUserAccessBindingSessionSettingsOutputReference", jsii.get(self, "sessionSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleAccessContextManagerGcpUserAccessBindingTimeoutsOutputReference":
        return typing.cast("GoogleAccessContextManagerGcpUserAccessBindingTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings"]]], jsii.get(self, "scopedAccessSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionSettingsInput")
    def session_settings_input(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingSessionSettings"]:
        return typing.cast(typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingSessionSettings"], jsii.get(self, "sessionSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAccessContextManagerGcpUserAccessBindingTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAccessContextManagerGcpUserAccessBindingTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevels")
    def access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessLevels"))

    @access_levels.setter
    def access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8a7022d4d5ba8d8722c976429e7cb009bd4328825a5c3c1771c51872b60d0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupKey")
    def group_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupKey"))

    @group_key.setter
    def group_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7437a8874475cf0fa9418b421fdf89ac723e44cb31cdfd822f1ce92aad2dc96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cbf7ae26aa966f82dfb38d3c89a50cdee693560b78c397fa13f000fb71a5a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @organization_id.setter
    def organization_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a30844792b7f1b49fbd7f15bcf3746366a9eef6b37144149700b45f6a478fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingConfig",
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
class GoogleAccessContextManagerGcpUserAccessBindingConfig(
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
        scoped_access_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        session_settings: typing.Optional[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingSessionSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param group_key: Required. Immutable. Google Group id whose members are subject to this binding's restrictions. See "id" in the G Suite Directory API's Groups resource. If a group's email address/alias is changed, this resource will continue to point at the changed group. This field does not accept group email addresses or aliases. Example: "01d520gv4vjcrht" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#group_key GoogleAccessContextManagerGcpUserAccessBinding#group_key}
        :param organization_id: Required. ID of the parent organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#organization_id GoogleAccessContextManagerGcpUserAccessBinding#organization_id}
        :param access_levels: Optional. Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#access_levels GoogleAccessContextManagerGcpUserAccessBinding#access_levels}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#id GoogleAccessContextManagerGcpUserAccessBinding#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scoped_access_settings: scoped_access_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#scoped_access_settings GoogleAccessContextManagerGcpUserAccessBinding#scoped_access_settings}
        :param session_settings: session_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_settings GoogleAccessContextManagerGcpUserAccessBinding#session_settings}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#timeouts GoogleAccessContextManagerGcpUserAccessBinding#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(session_settings, dict):
            session_settings = GoogleAccessContextManagerGcpUserAccessBindingSessionSettings(**session_settings)
        if isinstance(timeouts, dict):
            timeouts = GoogleAccessContextManagerGcpUserAccessBindingTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f55bdde560983b7b2bd1445ad59ea0a68b9e6ff89f05b22cea93bfcb7157f6e5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#group_key GoogleAccessContextManagerGcpUserAccessBinding#group_key}
        '''
        result = self._values.get("group_key")
        assert result is not None, "Required property 'group_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization_id(self) -> builtins.str:
        '''Required. ID of the parent organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#organization_id GoogleAccessContextManagerGcpUserAccessBinding#organization_id}
        '''
        result = self._values.get("organization_id")
        assert result is not None, "Required property 'organization_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#access_levels GoogleAccessContextManagerGcpUserAccessBinding#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#id GoogleAccessContextManagerGcpUserAccessBinding#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scoped_access_settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings"]]]:
        '''scoped_access_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#scoped_access_settings GoogleAccessContextManagerGcpUserAccessBinding#scoped_access_settings}
        '''
        result = self._values.get("scoped_access_settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings"]]], result)

    @builtins.property
    def session_settings(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingSessionSettings"]:
        '''session_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_settings GoogleAccessContextManagerGcpUserAccessBinding#session_settings}
        '''
        result = self._values.get("session_settings")
        return typing.cast(typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingSessionSettings"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#timeouts GoogleAccessContextManagerGcpUserAccessBinding#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerGcpUserAccessBindingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings",
    jsii_struct_bases=[],
    name_mapping={
        "active_settings": "activeSettings",
        "dry_run_settings": "dryRunSettings",
        "scope": "scope",
    },
)
class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings:
    def __init__(
        self,
        *,
        active_settings: typing.Optional[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        dry_run_settings: typing.Optional[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        scope: typing.Optional[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param active_settings: active_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#active_settings GoogleAccessContextManagerGcpUserAccessBinding#active_settings}
        :param dry_run_settings: dry_run_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#dry_run_settings GoogleAccessContextManagerGcpUserAccessBinding#dry_run_settings}
        :param scope: scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#scope GoogleAccessContextManagerGcpUserAccessBinding#scope}
        '''
        if isinstance(active_settings, dict):
            active_settings = GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings(**active_settings)
        if isinstance(dry_run_settings, dict):
            dry_run_settings = GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings(**dry_run_settings)
        if isinstance(scope, dict):
            scope = GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope(**scope)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8035a3ea3ae31c319717de94cb441041e2a7d3735cfb7841ee15cf208c34488b)
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
    ) -> typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings"]:
        '''active_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#active_settings GoogleAccessContextManagerGcpUserAccessBinding#active_settings}
        '''
        result = self._values.get("active_settings")
        return typing.cast(typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings"], result)

    @builtins.property
    def dry_run_settings(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings"]:
        '''dry_run_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#dry_run_settings GoogleAccessContextManagerGcpUserAccessBinding#dry_run_settings}
        '''
        result = self._values.get("dry_run_settings")
        return typing.cast(typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings"], result)

    @builtins.property
    def scope(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope"]:
        '''scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#scope GoogleAccessContextManagerGcpUserAccessBinding#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings",
    jsii_struct_bases=[],
    name_mapping={
        "access_levels": "accessLevels",
        "session_settings": "sessionSettings",
    },
)
class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings:
    def __init__(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_settings: typing.Optional[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: Optional. Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#access_levels GoogleAccessContextManagerGcpUserAccessBinding#access_levels}
        :param session_settings: session_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_settings GoogleAccessContextManagerGcpUserAccessBinding#session_settings}
        '''
        if isinstance(session_settings, dict):
            session_settings = GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings(**session_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1460dd2847b2489da7d4182ed2cc8e795855b94b9696ab848cf50f4c38de87e5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#access_levels GoogleAccessContextManagerGcpUserAccessBinding#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def session_settings(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings"]:
        '''session_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_settings GoogleAccessContextManagerGcpUserAccessBinding#session_settings}
        '''
        result = self._values.get("session_settings")
        return typing.cast(typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc14a3659a3e5f7cc509fa53da84c2cd512b45d5fc03a03a4392ce21e9e5560b)
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
        :param max_inactivity: Optional. How long a user is allowed to take between actions before a new access token must be issued. Only set for Google Cloud apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#max_inactivity GoogleAccessContextManagerGcpUserAccessBinding#max_inactivity}
        :param session_length: Optional. The session length. Setting this field to zero is equal to disabling session. Also can set infinite session by flipping the enabled bit to false below. If useOidcMaxAge is true, for OIDC apps, the session length will be the minimum of this field and OIDC max_age param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_length GoogleAccessContextManagerGcpUserAccessBinding#session_length}
        :param session_length_enabled: Optional. This field enables or disables Google Cloud session length. When false, all fields set above will be disregarded and the session length is basically infinite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_length_enabled GoogleAccessContextManagerGcpUserAccessBinding#session_length_enabled}
        :param session_reauth_method: Optional. The session challenges proposed to users when the Google Cloud session length is up. Possible values: ["LOGIN", "SECURITY_KEY", "PASSWORD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_reauth_method GoogleAccessContextManagerGcpUserAccessBinding#session_reauth_method}
        :param use_oidc_max_age: Optional. Only useful for OIDC apps. When false, the OIDC max_age param, if passed in the authentication request will be ignored. When true, the re-auth period will be the minimum of the sessionLength field and the max_age OIDC param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#use_oidc_max_age GoogleAccessContextManagerGcpUserAccessBinding#use_oidc_max_age}
        '''
        value = GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings(
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
    ) -> "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettingsOutputReference":
        return typing.cast("GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettingsOutputReference", jsii.get(self, "sessionSettings"))

    @builtins.property
    @jsii.member(jsii_name="accessLevelsInput")
    def access_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accessLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionSettingsInput")
    def session_settings_input(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings"]:
        return typing.cast(typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings"], jsii.get(self, "sessionSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessLevels")
    def access_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accessLevels"))

    @access_levels.setter
    def access_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64a89113002d095e1e559ae37934f7b5831a62d567f415cf54351966fe2d464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac74bc37a4df6f3167d9794bec6ee3249d8b223f4021388a4bb087d6b662d181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings",
    jsii_struct_bases=[],
    name_mapping={
        "max_inactivity": "maxInactivity",
        "session_length": "sessionLength",
        "session_length_enabled": "sessionLengthEnabled",
        "session_reauth_method": "sessionReauthMethod",
        "use_oidc_max_age": "useOidcMaxAge",
    },
)
class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings:
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
        :param max_inactivity: Optional. How long a user is allowed to take between actions before a new access token must be issued. Only set for Google Cloud apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#max_inactivity GoogleAccessContextManagerGcpUserAccessBinding#max_inactivity}
        :param session_length: Optional. The session length. Setting this field to zero is equal to disabling session. Also can set infinite session by flipping the enabled bit to false below. If useOidcMaxAge is true, for OIDC apps, the session length will be the minimum of this field and OIDC max_age param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_length GoogleAccessContextManagerGcpUserAccessBinding#session_length}
        :param session_length_enabled: Optional. This field enables or disables Google Cloud session length. When false, all fields set above will be disregarded and the session length is basically infinite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_length_enabled GoogleAccessContextManagerGcpUserAccessBinding#session_length_enabled}
        :param session_reauth_method: Optional. The session challenges proposed to users when the Google Cloud session length is up. Possible values: ["LOGIN", "SECURITY_KEY", "PASSWORD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_reauth_method GoogleAccessContextManagerGcpUserAccessBinding#session_reauth_method}
        :param use_oidc_max_age: Optional. Only useful for OIDC apps. When false, the OIDC max_age param, if passed in the authentication request will be ignored. When true, the re-auth period will be the minimum of the sessionLength field and the max_age OIDC param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#use_oidc_max_age GoogleAccessContextManagerGcpUserAccessBinding#use_oidc_max_age}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f44a0e5acdcd3e58ec0c36b61d293892cc2bd595ffab3b73d7b06a524a2e1d00)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#max_inactivity GoogleAccessContextManagerGcpUserAccessBinding#max_inactivity}
        '''
        result = self._values.get("max_inactivity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_length(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The session length. Setting this field to zero is equal to disabling session. Also can set infinite session by flipping the enabled bit to false below. If useOidcMaxAge is true, for OIDC apps, the session length will be the minimum of this field and OIDC max_age param.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_length GoogleAccessContextManagerGcpUserAccessBinding#session_length}
        '''
        result = self._values.get("session_length")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_length_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        This field enables or disables Google Cloud session length. When false, all fields set above will be disregarded and the session length is basically infinite.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_length_enabled GoogleAccessContextManagerGcpUserAccessBinding#session_length_enabled}
        '''
        result = self._values.get("session_length_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def session_reauth_method(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The session challenges proposed to users when the Google Cloud session length is up. Possible values: ["LOGIN", "SECURITY_KEY", "PASSWORD"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_reauth_method GoogleAccessContextManagerGcpUserAccessBinding#session_reauth_method}
        '''
        result = self._values.get("session_reauth_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_oidc_max_age(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Only useful for OIDC apps. When false, the OIDC max_age param, if passed in the authentication request will be ignored. When true, the re-auth period will be the minimum of the sessionLength field and the max_age OIDC param.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#use_oidc_max_age GoogleAccessContextManagerGcpUserAccessBinding#use_oidc_max_age}
        '''
        result = self._values.get("use_oidc_max_age")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9715ec1c5c57288ce4c2ef7abe6ee20898de831cacc78328cf62e6989ede94b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3071403c9adf91969588b304ad4451268a23b1ec8432cc7f261e31f1ca8f831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInactivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionLength")
    def session_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionLength"))

    @session_length.setter
    def session_length(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d8166c165b4e4b869ad20e1be5757d8ed37a78202a46998a22c5f592716c38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22e806cd81056c40fac44783a232503645774b28a51b5ac6636f47ea0fcdbce1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionLengthEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionReauthMethod")
    def session_reauth_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionReauthMethod"))

    @session_reauth_method.setter
    def session_reauth_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1f0db711a30e6e76ac251f9b51686738714917797336ac104234f4b9bb5427)
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
            type_hints = typing.get_type_hints(_typecheckingstub__979be6a32be7518992d8ef344d9dc2cfbdfc6af587ffc004c5f62307cb95dcf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useOidcMaxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f534fed98b8939eaef8d36e00830b8d8bdf0af5190535c7f48c77d4251f084f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings",
    jsii_struct_bases=[],
    name_mapping={"access_levels": "accessLevels"},
)
class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings:
    def __init__(
        self,
        *,
        access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param access_levels: Optional. Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#access_levels GoogleAccessContextManagerGcpUserAccessBinding#access_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e5e979de289f62c4ab9aa390d9a536b580450b40c14b1955e4b122def19c76)
            check_type(argname="argument access_levels", value=access_levels, expected_type=type_hints["access_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_levels is not None:
            self._values["access_levels"] = access_levels

    @builtins.property
    def access_levels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#access_levels GoogleAccessContextManagerGcpUserAccessBinding#access_levels}
        '''
        result = self._values.get("access_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23fbc7b0a5e017b63e1f1e2b32fc7bebcf0cf1dd8c79c8cc635dc2e3113d4477)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7fb515912bd86aa360b560fbffca87360b9c3590f7d46d35598f5e240e6fa71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c005ba9e8c03f1bafe50d04d05ee6dbc291531a741c2d050328b7d59baa2e786)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36279e5f0311e47948420a2232e09ac5c4a4691f5bfb27ef007f62b6e2f0510d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394a4aa05f835b1e81cdf813460fcf783c1e47db1fef887fd703513459eced6d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d55c277b3f2a9eaf8f26bc95ac4dfa84bbf7256c3df764da769375748f323d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76e902543f9853978909b7073a764a3631cbebfb8b855b38b1a9bfaa8053348e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c8b8525a73ae87f902cd1ceef449527f806686fde6d1d69acfe7b8a9c178dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd2153682030daf7f5389eb5c16769b18111eeba8624681673ce68275517db53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78879642bf0773addc87c92c892f86ff7c066eba164d2a3d3703c943abe86b9f)
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
        session_settings: typing.Optional[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param access_levels: Optional. Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#access_levels GoogleAccessContextManagerGcpUserAccessBinding#access_levels}
        :param session_settings: session_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_settings GoogleAccessContextManagerGcpUserAccessBinding#session_settings}
        '''
        value = GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings(
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
        :param access_levels: Optional. Access level that a user must have to be granted access. Only one access level is supported, not multiple. This repeated field must have exactly one element. Example: "accessPolicies/9522/accessLevels/device_trusted" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#access_levels GoogleAccessContextManagerGcpUserAccessBinding#access_levels}
        '''
        value = GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings(
            access_levels=access_levels
        )

        return typing.cast(None, jsii.invoke(self, "putDryRunSettings", [value]))

    @jsii.member(jsii_name="putScope")
    def put_scope(
        self,
        *,
        client_scope: typing.Optional[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_scope: client_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#client_scope GoogleAccessContextManagerGcpUserAccessBinding#client_scope}
        '''
        value = GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope(
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
    ) -> GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsOutputReference:
        return typing.cast(GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsOutputReference, jsii.get(self, "activeSettings"))

    @builtins.property
    @jsii.member(jsii_name="dryRunSettings")
    def dry_run_settings(
        self,
    ) -> GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettingsOutputReference:
        return typing.cast(GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettingsOutputReference, jsii.get(self, "dryRunSettings"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(
        self,
    ) -> "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeOutputReference":
        return typing.cast("GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeOutputReference", jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="activeSettingsInput")
    def active_settings_input(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings], jsii.get(self, "activeSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="dryRunSettingsInput")
    def dry_run_settings_input(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings], jsii.get(self, "dryRunSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope"]:
        return typing.cast(typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope"], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af7b02ba6460656180a7035d5c13b711fb0a0e11eb35f9853141d2869852ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope",
    jsii_struct_bases=[],
    name_mapping={"client_scope": "clientScope"},
)
class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope:
    def __init__(
        self,
        *,
        client_scope: typing.Optional[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_scope: client_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#client_scope GoogleAccessContextManagerGcpUserAccessBinding#client_scope}
        '''
        if isinstance(client_scope, dict):
            client_scope = GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope(**client_scope)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf4e9c2ae885524ccb248eb5e9089ea822d27c5711d5a0fbf7a217ba8f5a40f)
            check_type(argname="argument client_scope", value=client_scope, expected_type=type_hints["client_scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_scope is not None:
            self._values["client_scope"] = client_scope

    @builtins.property
    def client_scope(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope"]:
        '''client_scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#client_scope GoogleAccessContextManagerGcpUserAccessBinding#client_scope}
        '''
        result = self._values.get("client_scope")
        return typing.cast(typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope",
    jsii_struct_bases=[],
    name_mapping={"restricted_client_application": "restrictedClientApplication"},
)
class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope:
    def __init__(
        self,
        *,
        restricted_client_application: typing.Optional[typing.Union["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param restricted_client_application: restricted_client_application block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#restricted_client_application GoogleAccessContextManagerGcpUserAccessBinding#restricted_client_application}
        '''
        if isinstance(restricted_client_application, dict):
            restricted_client_application = GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication(**restricted_client_application)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36803fa252ac38f1e520e358128366b2c8c07e2d50718ed52750c5f1b1d0e130)
            check_type(argname="argument restricted_client_application", value=restricted_client_application, expected_type=type_hints["restricted_client_application"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if restricted_client_application is not None:
            self._values["restricted_client_application"] = restricted_client_application

    @builtins.property
    def restricted_client_application(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication"]:
        '''restricted_client_application block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#restricted_client_application GoogleAccessContextManagerGcpUserAccessBinding#restricted_client_application}
        '''
        result = self._values.get("restricted_client_application")
        return typing.cast(typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5222787b40de32a5d4fd0ec1aa2e6e1d82e7659812319e4116d789f3dcfe099c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRestrictedClientApplication")
    def put_restricted_client_application(
        self,
        *,
        client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The OAuth client ID of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#client_id GoogleAccessContextManagerGcpUserAccessBinding#client_id}
        '''
        value = GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication(
            client_id=client_id
        )

        return typing.cast(None, jsii.invoke(self, "putRestrictedClientApplication", [value]))

    @jsii.member(jsii_name="resetRestrictedClientApplication")
    def reset_restricted_client_application(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedClientApplication", []))

    @builtins.property
    @jsii.member(jsii_name="restrictedClientApplication")
    def restricted_client_application(
        self,
    ) -> "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplicationOutputReference":
        return typing.cast("GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplicationOutputReference", jsii.get(self, "restrictedClientApplication"))

    @builtins.property
    @jsii.member(jsii_name="restrictedClientApplicationInput")
    def restricted_client_application_input(
        self,
    ) -> typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication"]:
        return typing.cast(typing.Optional["GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication"], jsii.get(self, "restrictedClientApplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40728d7d362906b95b04afa243da645f543a4f3296792dd478e0553538d6d193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId"},
)
class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication:
    def __init__(self, *, client_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param client_id: The OAuth client ID of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#client_id GoogleAccessContextManagerGcpUserAccessBinding#client_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47df5a668b7d3ffb41031d043547cf657a27cf21fe1d7b80e68c9f2eddbbdf61)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id is not None:
            self._values["client_id"] = client_id

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The OAuth client ID of the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#client_id GoogleAccessContextManagerGcpUserAccessBinding#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1065ddbbce7e4a7728bca55b19a060fdd8b88422b562d19d8545f957e3344149)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d938e232d742cefd2726c683e5c4ea9127d487e010e48196ad909b36dbbccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e567ed8269f125a27034912d0de4ada3beee042df7440ab2d86efbfe6d3cb32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b739e0244933d7afec08c79c6872b8c48692a097871acd998d7094643f50a833)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientScope")
    def put_client_scope(
        self,
        *,
        restricted_client_application: typing.Optional[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param restricted_client_application: restricted_client_application block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#restricted_client_application GoogleAccessContextManagerGcpUserAccessBinding#restricted_client_application}
        '''
        value = GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope(
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
    ) -> GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeOutputReference:
        return typing.cast(GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeOutputReference, jsii.get(self, "clientScope"))

    @builtins.property
    @jsii.member(jsii_name="clientScopeInput")
    def client_scope_input(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope], jsii.get(self, "clientScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975c5eb7c5940f768264b713c9d917675706e0264f7f10dbf02fb16eb36b6589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingSessionSettings",
    jsii_struct_bases=[],
    name_mapping={
        "max_inactivity": "maxInactivity",
        "session_length": "sessionLength",
        "session_length_enabled": "sessionLengthEnabled",
        "session_reauth_method": "sessionReauthMethod",
        "use_oidc_max_age": "useOidcMaxAge",
    },
)
class GoogleAccessContextManagerGcpUserAccessBindingSessionSettings:
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
        :param max_inactivity: Optional. How long a user is allowed to take between actions before a new access token must be issued. Only set for Google Cloud apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#max_inactivity GoogleAccessContextManagerGcpUserAccessBinding#max_inactivity}
        :param session_length: Optional. The session length. Setting this field to zero is equal to disabling session. Also can set infinite session by flipping the enabled bit to false below. If useOidcMaxAge is true, for OIDC apps, the session length will be the minimum of this field and OIDC max_age param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_length GoogleAccessContextManagerGcpUserAccessBinding#session_length}
        :param session_length_enabled: Optional. This field enables or disables Google Cloud session length. When false, all fields set above will be disregarded and the session length is basically infinite. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_length_enabled GoogleAccessContextManagerGcpUserAccessBinding#session_length_enabled}
        :param session_reauth_method: Optional. The session challenges proposed to users when the Google Cloud session length is up. Possible values: ["LOGIN", "SECURITY_KEY", "PASSWORD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_reauth_method GoogleAccessContextManagerGcpUserAccessBinding#session_reauth_method}
        :param use_oidc_max_age: Optional. Only useful for OIDC apps. When false, the OIDC max_age param, if passed in the authentication request will be ignored. When true, the re-auth period will be the minimum of the sessionLength field and the max_age OIDC param. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#use_oidc_max_age GoogleAccessContextManagerGcpUserAccessBinding#use_oidc_max_age}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225901749683b718a251d4765eb66bd8903f3482fa531131bdeee8f8d12d322f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#max_inactivity GoogleAccessContextManagerGcpUserAccessBinding#max_inactivity}
        '''
        result = self._values.get("max_inactivity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_length(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The session length. Setting this field to zero is equal to disabling session. Also can set infinite session by flipping the enabled bit to false below. If useOidcMaxAge is true, for OIDC apps, the session length will be the minimum of this field and OIDC max_age param.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_length GoogleAccessContextManagerGcpUserAccessBinding#session_length}
        '''
        result = self._values.get("session_length")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_length_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        This field enables or disables Google Cloud session length. When false, all fields set above will be disregarded and the session length is basically infinite.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_length_enabled GoogleAccessContextManagerGcpUserAccessBinding#session_length_enabled}
        '''
        result = self._values.get("session_length_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def session_reauth_method(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The session challenges proposed to users when the Google Cloud session length is up. Possible values: ["LOGIN", "SECURITY_KEY", "PASSWORD"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#session_reauth_method GoogleAccessContextManagerGcpUserAccessBinding#session_reauth_method}
        '''
        result = self._values.get("session_reauth_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_oidc_max_age(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Only useful for OIDC apps. When false, the OIDC max_age param, if passed in the authentication request will be ignored. When true, the re-auth period will be the minimum of the sessionLength field and the max_age OIDC param.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#use_oidc_max_age GoogleAccessContextManagerGcpUserAccessBinding#use_oidc_max_age}
        '''
        result = self._values.get("use_oidc_max_age")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerGcpUserAccessBindingSessionSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerGcpUserAccessBindingSessionSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingSessionSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1db5bb8d38085a40d4fe1307391e48888a67ba7e993209921c078206ebf8aa22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__921bd1776e44064ccb7124afe521a15ef5ada0de5c297c9cc0d216b81cf61ee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInactivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionLength")
    def session_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionLength"))

    @session_length.setter
    def session_length(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50bb56a2a200b68bae691b8e9f4f17a9d271be655debf35fc75064aef09313f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04053d9f02eaf00991522b7f29e3eed89db2ed0f21e202e5a08c732e81f24c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionLengthEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionReauthMethod")
    def session_reauth_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionReauthMethod"))

    @session_reauth_method.setter
    def session_reauth_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4144e3aca8d150171cc3b0208e59a6070b52f824434a049c0ba827ca8b16e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af9eb0624283ce4dcc5a76446ffe17ac9dd2e98196d7fc7fff9f242fec5aef99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useOidcMaxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingSessionSettings]:
        return typing.cast(typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingSessionSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingSessionSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134a38429729156d70824fbaa298ccecacb9f05b83f6f440053fb6118e464ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleAccessContextManagerGcpUserAccessBindingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#create GoogleAccessContextManagerGcpUserAccessBinding#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#delete GoogleAccessContextManagerGcpUserAccessBinding#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#update GoogleAccessContextManagerGcpUserAccessBinding#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3efc4d949aad457ea1ef105b335e7c5a38808fa9b70193adce40d974f32634b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#create GoogleAccessContextManagerGcpUserAccessBinding#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#delete GoogleAccessContextManagerGcpUserAccessBinding#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_access_context_manager_gcp_user_access_binding#update GoogleAccessContextManagerGcpUserAccessBinding#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAccessContextManagerGcpUserAccessBindingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAccessContextManagerGcpUserAccessBindingTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAccessContextManagerGcpUserAccessBinding.GoogleAccessContextManagerGcpUserAccessBindingTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e369be2e811aff9730356c52cbe32bead767ac1bfd15c5a0a32fe6c1d0acc08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74a3d4b6e0877042690517977f5dde2d0d5e8d090f992e04ae1262079b68ffe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158258389906622096c712cb0f1a59bc3a81ad207351d1c0071d428ed2bcb93e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7af4b3306193a40a386691e67d0015a19c74f95ec21f7e3868ca4bb5cf788e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerGcpUserAccessBindingTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerGcpUserAccessBindingTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerGcpUserAccessBindingTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab551fbbccf9f9bb2d24495e741016450badb3c7370cf1fad1e72443d548ad0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleAccessContextManagerGcpUserAccessBinding",
    "GoogleAccessContextManagerGcpUserAccessBindingConfig",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsOutputReference",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettingsOutputReference",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettingsOutputReference",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsList",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsOutputReference",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeOutputReference",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplicationOutputReference",
    "GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeOutputReference",
    "GoogleAccessContextManagerGcpUserAccessBindingSessionSettings",
    "GoogleAccessContextManagerGcpUserAccessBindingSessionSettingsOutputReference",
    "GoogleAccessContextManagerGcpUserAccessBindingTimeouts",
    "GoogleAccessContextManagerGcpUserAccessBindingTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3563eef857c9b90c264366ee0b2362f0d585af4e1d61b13e9ce404a08d57a402(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    group_key: builtins.str,
    organization_id: builtins.str,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    scoped_access_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    session_settings: typing.Optional[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingSessionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__02bd0507e6a822815cb9667fa1f57848357d38499994dfa354b6214bdd18950f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be3ddd5757d21b49c47ad4538eadcebb1d474c444e8424d79452a1d2f90cfe1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8a7022d4d5ba8d8722c976429e7cb009bd4328825a5c3c1771c51872b60d0e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7437a8874475cf0fa9418b421fdf89ac723e44cb31cdfd822f1ce92aad2dc96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cbf7ae26aa966f82dfb38d3c89a50cdee693560b78c397fa13f000fb71a5a04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a30844792b7f1b49fbd7f15bcf3746366a9eef6b37144149700b45f6a478fca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f55bdde560983b7b2bd1445ad59ea0a68b9e6ff89f05b22cea93bfcb7157f6e5(
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
    scoped_access_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    session_settings: typing.Optional[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingSessionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8035a3ea3ae31c319717de94cb441041e2a7d3735cfb7841ee15cf208c34488b(
    *,
    active_settings: typing.Optional[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    dry_run_settings: typing.Optional[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    scope: typing.Optional[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1460dd2847b2489da7d4182ed2cc8e795855b94b9696ab848cf50f4c38de87e5(
    *,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_settings: typing.Optional[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc14a3659a3e5f7cc509fa53da84c2cd512b45d5fc03a03a4392ce21e9e5560b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64a89113002d095e1e559ae37934f7b5831a62d567f415cf54351966fe2d464(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac74bc37a4df6f3167d9794bec6ee3249d8b223f4021388a4bb087d6b662d181(
    value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44a0e5acdcd3e58ec0c36b61d293892cc2bd595ffab3b73d7b06a524a2e1d00(
    *,
    max_inactivity: typing.Optional[builtins.str] = None,
    session_length: typing.Optional[builtins.str] = None,
    session_length_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_reauth_method: typing.Optional[builtins.str] = None,
    use_oidc_max_age: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9715ec1c5c57288ce4c2ef7abe6ee20898de831cacc78328cf62e6989ede94b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3071403c9adf91969588b304ad4451268a23b1ec8432cc7f261e31f1ca8f831(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d8166c165b4e4b869ad20e1be5757d8ed37a78202a46998a22c5f592716c38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e806cd81056c40fac44783a232503645774b28a51b5ac6636f47ea0fcdbce1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1f0db711a30e6e76ac251f9b51686738714917797336ac104234f4b9bb5427(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979be6a32be7518992d8ef344d9dc2cfbdfc6af587ffc004c5f62307cb95dcf2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f534fed98b8939eaef8d36e00830b8d8bdf0af5190535c7f48c77d4251f084f3(
    value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsActiveSettingsSessionSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e5e979de289f62c4ab9aa390d9a536b580450b40c14b1955e4b122def19c76(
    *,
    access_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23fbc7b0a5e017b63e1f1e2b32fc7bebcf0cf1dd8c79c8cc635dc2e3113d4477(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7fb515912bd86aa360b560fbffca87360b9c3590f7d46d35598f5e240e6fa71(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c005ba9e8c03f1bafe50d04d05ee6dbc291531a741c2d050328b7d59baa2e786(
    value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsDryRunSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36279e5f0311e47948420a2232e09ac5c4a4691f5bfb27ef007f62b6e2f0510d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394a4aa05f835b1e81cdf813460fcf783c1e47db1fef887fd703513459eced6d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d55c277b3f2a9eaf8f26bc95ac4dfa84bbf7256c3df764da769375748f323d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e902543f9853978909b7073a764a3631cbebfb8b855b38b1a9bfaa8053348e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8b8525a73ae87f902cd1ceef449527f806686fde6d1d69acfe7b8a9c178dea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2153682030daf7f5389eb5c16769b18111eeba8624681673ce68275517db53(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78879642bf0773addc87c92c892f86ff7c066eba164d2a3d3703c943abe86b9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af7b02ba6460656180a7035d5c13b711fb0a0e11eb35f9853141d2869852ac3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf4e9c2ae885524ccb248eb5e9089ea822d27c5711d5a0fbf7a217ba8f5a40f(
    *,
    client_scope: typing.Optional[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36803fa252ac38f1e520e358128366b2c8c07e2d50718ed52750c5f1b1d0e130(
    *,
    restricted_client_application: typing.Optional[typing.Union[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5222787b40de32a5d4fd0ec1aa2e6e1d82e7659812319e4116d789f3dcfe099c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40728d7d362906b95b04afa243da645f543a4f3296792dd478e0553538d6d193(
    value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47df5a668b7d3ffb41031d043547cf657a27cf21fe1d7b80e68c9f2eddbbdf61(
    *,
    client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1065ddbbce7e4a7728bca55b19a060fdd8b88422b562d19d8545f957e3344149(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d938e232d742cefd2726c683e5c4ea9127d487e010e48196ad909b36dbbccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e567ed8269f125a27034912d0de4ada3beee042df7440ab2d86efbfe6d3cb32(
    value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScopeClientScopeRestrictedClientApplication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b739e0244933d7afec08c79c6872b8c48692a097871acd998d7094643f50a833(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975c5eb7c5940f768264b713c9d917675706e0264f7f10dbf02fb16eb36b6589(
    value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingScopedAccessSettingsScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225901749683b718a251d4765eb66bd8903f3482fa531131bdeee8f8d12d322f(
    *,
    max_inactivity: typing.Optional[builtins.str] = None,
    session_length: typing.Optional[builtins.str] = None,
    session_length_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_reauth_method: typing.Optional[builtins.str] = None,
    use_oidc_max_age: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db5bb8d38085a40d4fe1307391e48888a67ba7e993209921c078206ebf8aa22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921bd1776e44064ccb7124afe521a15ef5ada0de5c297c9cc0d216b81cf61ee8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50bb56a2a200b68bae691b8e9f4f17a9d271be655debf35fc75064aef09313f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04053d9f02eaf00991522b7f29e3eed89db2ed0f21e202e5a08c732e81f24c1a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4144e3aca8d150171cc3b0208e59a6070b52f824434a049c0ba827ca8b16e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9eb0624283ce4dcc5a76446ffe17ac9dd2e98196d7fc7fff9f242fec5aef99(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134a38429729156d70824fbaa298ccecacb9f05b83f6f440053fb6118e464ca8(
    value: typing.Optional[GoogleAccessContextManagerGcpUserAccessBindingSessionSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3efc4d949aad457ea1ef105b335e7c5a38808fa9b70193adce40d974f32634b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e369be2e811aff9730356c52cbe32bead767ac1bfd15c5a0a32fe6c1d0acc08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a3d4b6e0877042690517977f5dde2d0d5e8d090f992e04ae1262079b68ffe9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158258389906622096c712cb0f1a59bc3a81ad207351d1c0071d428ed2bcb93e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7af4b3306193a40a386691e67d0015a19c74f95ec21f7e3868ca4bb5cf788e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab551fbbccf9f9bb2d24495e741016450badb3c7370cf1fad1e72443d548ad0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAccessContextManagerGcpUserAccessBindingTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
