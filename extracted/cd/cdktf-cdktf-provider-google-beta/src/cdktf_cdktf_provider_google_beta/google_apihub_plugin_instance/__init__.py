r'''
# `google_apihub_plugin_instance`

Refer to the Terraform Registry for docs: [`google_apihub_plugin_instance`](https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance).
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


class GoogleApihubPluginInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance google_apihub_plugin_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        plugin: builtins.str,
        plugin_instance_id: builtins.str,
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApihubPluginInstanceActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_config: typing.Optional[typing.Union["GoogleApihubPluginInstanceAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApihubPluginInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance google_apihub_plugin_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The display name for this plugin instance. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#display_name GoogleApihubPluginInstance#display_name}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#location GoogleApihubPluginInstance#location}
        :param plugin: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#plugin GoogleApihubPluginInstance#plugin}
        :param plugin_instance_id: The ID to use for the plugin instance, which will become the final component of the plugin instance's resource name. This field is optional. - If provided, the same will be used. The service will throw an error if the specified id is already used by another plugin instance in the plugin resource. - If not provided, a system generated id will be used. This value should be 4-63 characters, and valid characters are /a-z[0-9]-_/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#plugin_instance_id GoogleApihubPluginInstance#plugin_instance_id}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#actions GoogleApihubPluginInstance#actions}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#auth_config GoogleApihubPluginInstance#auth_config}
        :param disable: The display name for this plugin instance. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#disable GoogleApihubPluginInstance#disable}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#id GoogleApihubPluginInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#project GoogleApihubPluginInstance#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#timeouts GoogleApihubPluginInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ccc9b3d88fd05a17a6059a3e956f2088497f4048e43f74eafa7452ea03e79d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleApihubPluginInstanceConfig(
            display_name=display_name,
            location=location,
            plugin=plugin,
            plugin_instance_id=plugin_instance_id,
            actions=actions,
            auth_config=auth_config,
            disable=disable,
            id=id,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleApihubPluginInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleApihubPluginInstance to import.
        :param import_from_id: The id of the existing GoogleApihubPluginInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleApihubPluginInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ad6aff47c4c29c35873205e2bb49e86370aa3c1aed8641380fb36767cb814c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApihubPluginInstanceActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21eae5bb8d2fd4f389626e57b609cf155618f67dfcf02ef0aabf891a95046038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putAuthConfig")
    def put_auth_config(
        self,
        *,
        auth_type: builtins.str,
        api_key_config: typing.Optional[typing.Union["GoogleApihubPluginInstanceAuthConfigApiKeyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        google_service_account_config: typing.Optional[typing.Union["GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_client_credentials_config: typing.Optional[typing.Union["GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        user_password_config: typing.Optional[typing.Union["GoogleApihubPluginInstanceAuthConfigUserPasswordConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auth_type: Possible values: AUTH_TYPE_UNSPECIFIED NO_AUTH GOOGLE_SERVICE_ACCOUNT USER_PASSWORD API_KEY OAUTH2_CLIENT_CREDENTIALS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#auth_type GoogleApihubPluginInstance#auth_type}
        :param api_key_config: api_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#api_key_config GoogleApihubPluginInstance#api_key_config}
        :param google_service_account_config: google_service_account_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#google_service_account_config GoogleApihubPluginInstance#google_service_account_config}
        :param oauth2_client_credentials_config: oauth2_client_credentials_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#oauth2_client_credentials_config GoogleApihubPluginInstance#oauth2_client_credentials_config}
        :param user_password_config: user_password_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#user_password_config GoogleApihubPluginInstance#user_password_config}
        '''
        value = GoogleApihubPluginInstanceAuthConfig(
            auth_type=auth_type,
            api_key_config=api_key_config,
            google_service_account_config=google_service_account_config,
            oauth2_client_credentials_config=oauth2_client_credentials_config,
            user_password_config=user_password_config,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#create GoogleApihubPluginInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#delete GoogleApihubPluginInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#update GoogleApihubPluginInstance#update}.
        '''
        value = GoogleApihubPluginInstanceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @jsii.member(jsii_name="resetAuthConfig")
    def reset_auth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthConfig", []))

    @jsii.member(jsii_name="resetDisable")
    def reset_disable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisable", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="actions")
    def actions(self) -> "GoogleApihubPluginInstanceActionsList":
        return typing.cast("GoogleApihubPluginInstanceActionsList", jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="authConfig")
    def auth_config(self) -> "GoogleApihubPluginInstanceAuthConfigOutputReference":
        return typing.cast("GoogleApihubPluginInstanceAuthConfigOutputReference", jsii.get(self, "authConfig"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleApihubPluginInstanceTimeoutsOutputReference":
        return typing.cast("GoogleApihubPluginInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApihubPluginInstanceActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApihubPluginInstanceActions"]]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="authConfigInput")
    def auth_config_input(
        self,
    ) -> typing.Optional["GoogleApihubPluginInstanceAuthConfig"]:
        return typing.cast(typing.Optional["GoogleApihubPluginInstanceAuthConfig"], jsii.get(self, "authConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="disableInput")
    def disable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginInput")
    def plugin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginInstanceIdInput")
    def plugin_instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginInstanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApihubPluginInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApihubPluginInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="disable")
    def disable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disable"))

    @disable.setter
    def disable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1bc90ff03840cc9e1e61121b1f00b81dcff03801ce06565d12fba8a5f8bb127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ab06da9858798cd0126dfed07eae7e1cda5d8d494520ce767f2dca4e08af07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3fcd612ba6647fd34b2a8fc49c057a34c257dfa301fa888bac5cec800a6e34c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27af8d3142ea2267ee2ee75562ecdfe7845562b6a235aabd270344d4863c169c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="plugin")
    def plugin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "plugin"))

    @plugin.setter
    def plugin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0123c1d4e78f6eca68d04ade0e35472ec7c4df9d8767df28920142bb1548a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plugin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginInstanceId")
    def plugin_instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginInstanceId"))

    @plugin_instance_id.setter
    def plugin_instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e075d201d09512ad7ddce3221c8e55b59e95bbbe1e1c93331a6473df4c9486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginInstanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67e2c8f2df477af1b777a7ada5214daafb0dd6736752f6d166b6557d2be2e341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActions",
    jsii_struct_bases=[],
    name_mapping={
        "action_id": "actionId",
        "curation_config": "curationConfig",
        "schedule_cron_expression": "scheduleCronExpression",
        "schedule_time_zone": "scheduleTimeZone",
    },
)
class GoogleApihubPluginInstanceActions:
    def __init__(
        self,
        *,
        action_id: builtins.str,
        curation_config: typing.Optional[typing.Union["GoogleApihubPluginInstanceActionsCurationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule_cron_expression: typing.Optional[builtins.str] = None,
        schedule_time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action_id: This should map to one of the action id specified in actions_config in the plugin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#action_id GoogleApihubPluginInstance#action_id}
        :param curation_config: curation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#curation_config GoogleApihubPluginInstance#curation_config}
        :param schedule_cron_expression: The schedule for this plugin instance action. This can only be set if the plugin supports API_HUB_SCHEDULE_TRIGGER mode for this action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#schedule_cron_expression GoogleApihubPluginInstance#schedule_cron_expression}
        :param schedule_time_zone: The time zone for the schedule cron expression. If not provided, UTC will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#schedule_time_zone GoogleApihubPluginInstance#schedule_time_zone}
        '''
        if isinstance(curation_config, dict):
            curation_config = GoogleApihubPluginInstanceActionsCurationConfig(**curation_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5d8556f880e09f4e550118d3dbc0a60d17cd48ce8b8c3bff741ccf8f06a720)
            check_type(argname="argument action_id", value=action_id, expected_type=type_hints["action_id"])
            check_type(argname="argument curation_config", value=curation_config, expected_type=type_hints["curation_config"])
            check_type(argname="argument schedule_cron_expression", value=schedule_cron_expression, expected_type=type_hints["schedule_cron_expression"])
            check_type(argname="argument schedule_time_zone", value=schedule_time_zone, expected_type=type_hints["schedule_time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_id": action_id,
        }
        if curation_config is not None:
            self._values["curation_config"] = curation_config
        if schedule_cron_expression is not None:
            self._values["schedule_cron_expression"] = schedule_cron_expression
        if schedule_time_zone is not None:
            self._values["schedule_time_zone"] = schedule_time_zone

    @builtins.property
    def action_id(self) -> builtins.str:
        '''This should map to one of the action id specified in actions_config in the plugin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#action_id GoogleApihubPluginInstance#action_id}
        '''
        result = self._values.get("action_id")
        assert result is not None, "Required property 'action_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def curation_config(
        self,
    ) -> typing.Optional["GoogleApihubPluginInstanceActionsCurationConfig"]:
        '''curation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#curation_config GoogleApihubPluginInstance#curation_config}
        '''
        result = self._values.get("curation_config")
        return typing.cast(typing.Optional["GoogleApihubPluginInstanceActionsCurationConfig"], result)

    @builtins.property
    def schedule_cron_expression(self) -> typing.Optional[builtins.str]:
        '''The schedule for this plugin instance action.

        This can only be set if the
        plugin supports API_HUB_SCHEDULE_TRIGGER mode for this action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#schedule_cron_expression GoogleApihubPluginInstance#schedule_cron_expression}
        '''
        result = self._values.get("schedule_cron_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone for the schedule cron expression. If not provided, UTC will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#schedule_time_zone GoogleApihubPluginInstance#schedule_time_zone}
        '''
        result = self._values.get("schedule_time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActionsCurationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "curation_type": "curationType",
        "custom_curation": "customCuration",
    },
)
class GoogleApihubPluginInstanceActionsCurationConfig:
    def __init__(
        self,
        *,
        curation_type: typing.Optional[builtins.str] = None,
        custom_curation: typing.Optional[typing.Union["GoogleApihubPluginInstanceActionsCurationConfigCustomCuration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param curation_type: Possible values: CURATION_TYPE_UNSPECIFIED DEFAULT_CURATION_FOR_API_METADATA CUSTOM_CURATION_FOR_API_METADATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#curation_type GoogleApihubPluginInstance#curation_type}
        :param custom_curation: custom_curation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#custom_curation GoogleApihubPluginInstance#custom_curation}
        '''
        if isinstance(custom_curation, dict):
            custom_curation = GoogleApihubPluginInstanceActionsCurationConfigCustomCuration(**custom_curation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb3fa19e4f3ba55ced4930d156023dcb7e2a966febc99650a798558bb0c51f6)
            check_type(argname="argument curation_type", value=curation_type, expected_type=type_hints["curation_type"])
            check_type(argname="argument custom_curation", value=custom_curation, expected_type=type_hints["custom_curation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if curation_type is not None:
            self._values["curation_type"] = curation_type
        if custom_curation is not None:
            self._values["custom_curation"] = custom_curation

    @builtins.property
    def curation_type(self) -> typing.Optional[builtins.str]:
        '''Possible values: CURATION_TYPE_UNSPECIFIED DEFAULT_CURATION_FOR_API_METADATA CUSTOM_CURATION_FOR_API_METADATA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#curation_type GoogleApihubPluginInstance#curation_type}
        '''
        result = self._values.get("curation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_curation(
        self,
    ) -> typing.Optional["GoogleApihubPluginInstanceActionsCurationConfigCustomCuration"]:
        '''custom_curation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#custom_curation GoogleApihubPluginInstance#custom_curation}
        '''
        result = self._values.get("custom_curation")
        return typing.cast(typing.Optional["GoogleApihubPluginInstanceActionsCurationConfigCustomCuration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceActionsCurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActionsCurationConfigCustomCuration",
    jsii_struct_bases=[],
    name_mapping={"curation": "curation"},
)
class GoogleApihubPluginInstanceActionsCurationConfigCustomCuration:
    def __init__(self, *, curation: builtins.str) -> None:
        '''
        :param curation: The unique name of the curation resource. This will be the name of the curation resource in the format: 'projects/{project}/locations/{location}/curations/{curation}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#curation GoogleApihubPluginInstance#curation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38b8d7e93fede7b6da25ded43fb2ed49d5c455c9f15197510938917723dad77e)
            check_type(argname="argument curation", value=curation, expected_type=type_hints["curation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "curation": curation,
        }

    @builtins.property
    def curation(self) -> builtins.str:
        '''The unique name of the curation resource. This will be the name of the curation resource in the format: 'projects/{project}/locations/{location}/curations/{curation}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#curation GoogleApihubPluginInstance#curation}
        '''
        result = self._values.get("curation")
        assert result is not None, "Required property 'curation' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceActionsCurationConfigCustomCuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginInstanceActionsCurationConfigCustomCurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActionsCurationConfigCustomCurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d1d83d34a332b4a71e5fb5713fef2ae5b948ab38d836e268a28335cb6c45a16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="curationInput")
    def curation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "curationInput"))

    @builtins.property
    @jsii.member(jsii_name="curation")
    def curation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "curation"))

    @curation.setter
    def curation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed03eda1ccc04a6428fd0d87b2f927b9420b1d4c02f00886cc472bc3230530f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "curation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceActionsCurationConfigCustomCuration]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceActionsCurationConfigCustomCuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginInstanceActionsCurationConfigCustomCuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9e18374d0aa0553b940a4a7bdddcbcf0f8f61bfd0491bb0080ed16a5f98077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginInstanceActionsCurationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActionsCurationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66ec4a321371ffcdae82f5b7c44663afeafd1e29f5d45ece755e1e3c9d5890af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomCuration")
    def put_custom_curation(self, *, curation: builtins.str) -> None:
        '''
        :param curation: The unique name of the curation resource. This will be the name of the curation resource in the format: 'projects/{project}/locations/{location}/curations/{curation}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#curation GoogleApihubPluginInstance#curation}
        '''
        value = GoogleApihubPluginInstanceActionsCurationConfigCustomCuration(
            curation=curation
        )

        return typing.cast(None, jsii.invoke(self, "putCustomCuration", [value]))

    @jsii.member(jsii_name="resetCurationType")
    def reset_curation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCurationType", []))

    @jsii.member(jsii_name="resetCustomCuration")
    def reset_custom_curation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomCuration", []))

    @builtins.property
    @jsii.member(jsii_name="customCuration")
    def custom_curation(
        self,
    ) -> GoogleApihubPluginInstanceActionsCurationConfigCustomCurationOutputReference:
        return typing.cast(GoogleApihubPluginInstanceActionsCurationConfigCustomCurationOutputReference, jsii.get(self, "customCuration"))

    @builtins.property
    @jsii.member(jsii_name="curationTypeInput")
    def curation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "curationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="customCurationInput")
    def custom_curation_input(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceActionsCurationConfigCustomCuration]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceActionsCurationConfigCustomCuration], jsii.get(self, "customCurationInput"))

    @builtins.property
    @jsii.member(jsii_name="curationType")
    def curation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "curationType"))

    @curation_type.setter
    def curation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821cfeae9090b668eeaea1889bd4e56b402276a6a5b4b8ce61610aad75c00385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "curationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceActionsCurationConfig]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceActionsCurationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginInstanceActionsCurationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ab4fe69299a799de67f968b1f4ced03aaea25c651808747b2323332d22c292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActionsHubInstanceAction",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleApihubPluginInstanceActionsHubInstanceAction:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceActionsHubInstanceAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActionsHubInstanceActionLastExecution",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleApihubPluginInstanceActionsHubInstanceActionLastExecution:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceActionsHubInstanceActionLastExecution(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginInstanceActionsHubInstanceActionLastExecutionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActionsHubInstanceActionLastExecutionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e22d4e3e7e4a901fce03a59e30c42c48a5d3ea4cedef1edd8b05a4a6f88762c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApihubPluginInstanceActionsHubInstanceActionLastExecutionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b386c213e81f1fdd371bbd3af0bc351baddb9fde46ffcd1b4cdb3e5b37a19f68)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApihubPluginInstanceActionsHubInstanceActionLastExecutionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f70a546762cb5c9d95da7083497f40a61905e9149fbf83c5e46d5a4d66b0f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eff7e9a562f1d94429c3bb8021bb0e71bfed943a9fdbe77df13171d9fd150bd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05e1a39f85a6c48d26b1a43298e44f32cc4f8b2931deaa6c5db8af6ef8c98c6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginInstanceActionsHubInstanceActionLastExecutionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActionsHubInstanceActionLastExecutionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8dc8e33a7a3e3b1722db2518e9a1bd6065cb53ccb263e5237959f834465fe88)
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
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "result"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceActionsHubInstanceActionLastExecution]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceActionsHubInstanceActionLastExecution], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginInstanceActionsHubInstanceActionLastExecution],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39df146f3b03fcf918a37394f80046ff8d03f7f1127854f8bd6cd826cdea589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginInstanceActionsHubInstanceActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActionsHubInstanceActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20294e3fd2c4534c59d49955fe1674d4baa80bc0d0c231b4a9628ea343860300)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApihubPluginInstanceActionsHubInstanceActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b3c882f0bd7b4ba67ce20243ec1d4dbbf374f1d44e26e333995c72e6081d5b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApihubPluginInstanceActionsHubInstanceActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750a749f17979be9d91dd4d24c8716591ec0578768a173db534cd9bde339cd89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6802dcf83e6f4c4ceafe4fa1f138f8dd614e5e6fc8f595c7d42489415bb6c6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__205689bf7c44803bd56aba8e4753d1ee763211b942f9deac109c7b89f59a4a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginInstanceActionsHubInstanceActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActionsHubInstanceActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bb999efac53709dc5526376dd1d103609d14cca713c056f79f783111cf33564)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="currentExecutionState")
    def current_execution_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "currentExecutionState"))

    @builtins.property
    @jsii.member(jsii_name="lastExecution")
    def last_execution(
        self,
    ) -> GoogleApihubPluginInstanceActionsHubInstanceActionLastExecutionList:
        return typing.cast(GoogleApihubPluginInstanceActionsHubInstanceActionLastExecutionList, jsii.get(self, "lastExecution"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceActionsHubInstanceAction]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceActionsHubInstanceAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginInstanceActionsHubInstanceAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4367edf0ede925ad02a5700c728c014bd35ae7cbb2a099f88e5e6282d990dba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginInstanceActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2d4dce70166597f0f185795148e5490115cf64d7dc55ae904570653ac9e8516)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApihubPluginInstanceActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8bae74f180974d14a979fd23e396d7223e1e50c970001b2f5eedc15e46e5a5c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApihubPluginInstanceActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d8bdd3a179dbf5754645b77e1e8932e9790191dd733ecfcadd3ddb082982d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6758ebca1acee0d4bc0f569a2e7c74b8edeb9de30a333093d1aba43369cde492)
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
            type_hints = typing.get_type_hints(_typecheckingstub__739a917473870108531773e9c3372ea6ff44eff64cb8f6fbf5c9b1d7e6317bd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginInstanceActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginInstanceActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginInstanceActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2192a8188c6b1b0e93b7f518c59538ed3afcc0ab19e933a392db7aa90994138a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginInstanceActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09bab300ed39caba829039decbc60ff681b69ee1e218800c0b3ea7cb76d4e744)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCurationConfig")
    def put_curation_config(
        self,
        *,
        curation_type: typing.Optional[builtins.str] = None,
        custom_curation: typing.Optional[typing.Union[GoogleApihubPluginInstanceActionsCurationConfigCustomCuration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param curation_type: Possible values: CURATION_TYPE_UNSPECIFIED DEFAULT_CURATION_FOR_API_METADATA CUSTOM_CURATION_FOR_API_METADATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#curation_type GoogleApihubPluginInstance#curation_type}
        :param custom_curation: custom_curation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#custom_curation GoogleApihubPluginInstance#custom_curation}
        '''
        value = GoogleApihubPluginInstanceActionsCurationConfig(
            curation_type=curation_type, custom_curation=custom_curation
        )

        return typing.cast(None, jsii.invoke(self, "putCurationConfig", [value]))

    @jsii.member(jsii_name="resetCurationConfig")
    def reset_curation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCurationConfig", []))

    @jsii.member(jsii_name="resetScheduleCronExpression")
    def reset_schedule_cron_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleCronExpression", []))

    @jsii.member(jsii_name="resetScheduleTimeZone")
    def reset_schedule_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleTimeZone", []))

    @builtins.property
    @jsii.member(jsii_name="curationConfig")
    def curation_config(
        self,
    ) -> GoogleApihubPluginInstanceActionsCurationConfigOutputReference:
        return typing.cast(GoogleApihubPluginInstanceActionsCurationConfigOutputReference, jsii.get(self, "curationConfig"))

    @builtins.property
    @jsii.member(jsii_name="hubInstanceAction")
    def hub_instance_action(
        self,
    ) -> GoogleApihubPluginInstanceActionsHubInstanceActionList:
        return typing.cast(GoogleApihubPluginInstanceActionsHubInstanceActionList, jsii.get(self, "hubInstanceAction"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="actionIdInput")
    def action_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="curationConfigInput")
    def curation_config_input(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceActionsCurationConfig]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceActionsCurationConfig], jsii.get(self, "curationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleCronExpressionInput")
    def schedule_cron_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleCronExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleTimeZoneInput")
    def schedule_time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleTimeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="actionId")
    def action_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionId"))

    @action_id.setter
    def action_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4784f6a74f2f4983d1a523b0df8fd973fc37cf40f26223adb1c2ba8ed30e172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleCronExpression")
    def schedule_cron_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleCronExpression"))

    @schedule_cron_expression.setter
    def schedule_cron_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20002f6a16aadc495dfca630c4ebd945c42f14c44113d79e27cd2e7d4b58e40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleCronExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleTimeZone")
    def schedule_time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleTimeZone"))

    @schedule_time_zone.setter
    def schedule_time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424baaed2767132817fee57085f32dc0e090c853395e17ee920ec8826ff8192d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleTimeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginInstanceActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginInstanceActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginInstanceActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c629af21315effa47f538af108bfa958c7229b5e7b098254323de6a1602cad7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "api_key_config": "apiKeyConfig",
        "google_service_account_config": "googleServiceAccountConfig",
        "oauth2_client_credentials_config": "oauth2ClientCredentialsConfig",
        "user_password_config": "userPasswordConfig",
    },
)
class GoogleApihubPluginInstanceAuthConfig:
    def __init__(
        self,
        *,
        auth_type: builtins.str,
        api_key_config: typing.Optional[typing.Union["GoogleApihubPluginInstanceAuthConfigApiKeyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        google_service_account_config: typing.Optional[typing.Union["GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_client_credentials_config: typing.Optional[typing.Union["GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        user_password_config: typing.Optional[typing.Union["GoogleApihubPluginInstanceAuthConfigUserPasswordConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auth_type: Possible values: AUTH_TYPE_UNSPECIFIED NO_AUTH GOOGLE_SERVICE_ACCOUNT USER_PASSWORD API_KEY OAUTH2_CLIENT_CREDENTIALS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#auth_type GoogleApihubPluginInstance#auth_type}
        :param api_key_config: api_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#api_key_config GoogleApihubPluginInstance#api_key_config}
        :param google_service_account_config: google_service_account_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#google_service_account_config GoogleApihubPluginInstance#google_service_account_config}
        :param oauth2_client_credentials_config: oauth2_client_credentials_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#oauth2_client_credentials_config GoogleApihubPluginInstance#oauth2_client_credentials_config}
        :param user_password_config: user_password_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#user_password_config GoogleApihubPluginInstance#user_password_config}
        '''
        if isinstance(api_key_config, dict):
            api_key_config = GoogleApihubPluginInstanceAuthConfigApiKeyConfig(**api_key_config)
        if isinstance(google_service_account_config, dict):
            google_service_account_config = GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig(**google_service_account_config)
        if isinstance(oauth2_client_credentials_config, dict):
            oauth2_client_credentials_config = GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig(**oauth2_client_credentials_config)
        if isinstance(user_password_config, dict):
            user_password_config = GoogleApihubPluginInstanceAuthConfigUserPasswordConfig(**user_password_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03369ea77fd7db0e56baee463044c4095cd83f556be726d23ea2aef4f03359bf)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument api_key_config", value=api_key_config, expected_type=type_hints["api_key_config"])
            check_type(argname="argument google_service_account_config", value=google_service_account_config, expected_type=type_hints["google_service_account_config"])
            check_type(argname="argument oauth2_client_credentials_config", value=oauth2_client_credentials_config, expected_type=type_hints["oauth2_client_credentials_config"])
            check_type(argname="argument user_password_config", value=user_password_config, expected_type=type_hints["user_password_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_type": auth_type,
        }
        if api_key_config is not None:
            self._values["api_key_config"] = api_key_config
        if google_service_account_config is not None:
            self._values["google_service_account_config"] = google_service_account_config
        if oauth2_client_credentials_config is not None:
            self._values["oauth2_client_credentials_config"] = oauth2_client_credentials_config
        if user_password_config is not None:
            self._values["user_password_config"] = user_password_config

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''Possible values: AUTH_TYPE_UNSPECIFIED NO_AUTH GOOGLE_SERVICE_ACCOUNT USER_PASSWORD API_KEY OAUTH2_CLIENT_CREDENTIALS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#auth_type GoogleApihubPluginInstance#auth_type}
        '''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key_config(
        self,
    ) -> typing.Optional["GoogleApihubPluginInstanceAuthConfigApiKeyConfig"]:
        '''api_key_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#api_key_config GoogleApihubPluginInstance#api_key_config}
        '''
        result = self._values.get("api_key_config")
        return typing.cast(typing.Optional["GoogleApihubPluginInstanceAuthConfigApiKeyConfig"], result)

    @builtins.property
    def google_service_account_config(
        self,
    ) -> typing.Optional["GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig"]:
        '''google_service_account_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#google_service_account_config GoogleApihubPluginInstance#google_service_account_config}
        '''
        result = self._values.get("google_service_account_config")
        return typing.cast(typing.Optional["GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig"], result)

    @builtins.property
    def oauth2_client_credentials_config(
        self,
    ) -> typing.Optional["GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig"]:
        '''oauth2_client_credentials_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#oauth2_client_credentials_config GoogleApihubPluginInstance#oauth2_client_credentials_config}
        '''
        result = self._values.get("oauth2_client_credentials_config")
        return typing.cast(typing.Optional["GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig"], result)

    @builtins.property
    def user_password_config(
        self,
    ) -> typing.Optional["GoogleApihubPluginInstanceAuthConfigUserPasswordConfig"]:
        '''user_password_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#user_password_config GoogleApihubPluginInstance#user_password_config}
        '''
        result = self._values.get("user_password_config")
        return typing.cast(typing.Optional["GoogleApihubPluginInstanceAuthConfigUserPasswordConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigApiKeyConfig",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "http_element_location": "httpElementLocation",
        "name": "name",
    },
)
class GoogleApihubPluginInstanceAuthConfigApiKeyConfig:
    def __init__(
        self,
        *,
        api_key: typing.Union["GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey", typing.Dict[builtins.str, typing.Any]],
        http_element_location: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param api_key: api_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#api_key GoogleApihubPluginInstance#api_key}
        :param http_element_location: The location of the API key. The default value is QUERY. Possible values: HTTP_ELEMENT_LOCATION_UNSPECIFIED QUERY HEADER PATH BODY COOKIE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#http_element_location GoogleApihubPluginInstance#http_element_location}
        :param name: The parameter name of the API key. E.g. If the API request is "https://example.com/act?api_key=", "api_key" would be the parameter name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#name GoogleApihubPluginInstance#name}
        '''
        if isinstance(api_key, dict):
            api_key = GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey(**api_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c091ddb93b07e9aef151f33d620b1fca4f116f148f0e417a12d28532dbb6e34)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument http_element_location", value=http_element_location, expected_type=type_hints["http_element_location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
            "http_element_location": http_element_location,
            "name": name,
        }

    @builtins.property
    def api_key(self) -> "GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey":
        '''api_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#api_key GoogleApihubPluginInstance#api_key}
        '''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast("GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey", result)

    @builtins.property
    def http_element_location(self) -> builtins.str:
        '''The location of the API key. The default value is QUERY. Possible values: HTTP_ELEMENT_LOCATION_UNSPECIFIED QUERY HEADER PATH BODY COOKIE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#http_element_location GoogleApihubPluginInstance#http_element_location}
        '''
        result = self._values.get("http_element_location")
        assert result is not None, "Required property 'http_element_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The parameter name of the API key. E.g. If the API request is "https://example.com/act?api_key=", "api_key" would be the parameter name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#name GoogleApihubPluginInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceAuthConfigApiKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#secret_version GoogleApihubPluginInstance#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0620c0a89d17901cccbef23336b489660538119539dbbb2c54cf8806168a4863)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#secret_version GoogleApihubPluginInstance#secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efdc3a20628fa734a39f6a2e9d914f59f6f1f7549feba30ed063771d9113e5e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6791817aa58675b2f0cb926356aa4dfe9d51825d25156e8c2900a50b7a958bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be00dcba2e3c5f4dbbc4cf268d70b755c5295ad42a7c45a785b03ed47823b773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginInstanceAuthConfigApiKeyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigApiKeyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abe512089d9f88744a35d6d2abae9d5041abb66327488ef45e11d8d783cda9ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApiKey")
    def put_api_key(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#secret_version GoogleApihubPluginInstance#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putApiKey", [value]))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(
        self,
    ) -> GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKeyOutputReference:
        return typing.cast(GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKeyOutputReference, jsii.get(self, "apiKey"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="httpElementLocationInput")
    def http_element_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpElementLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="httpElementLocation")
    def http_element_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpElementLocation"))

    @http_element_location.setter
    def http_element_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b9850da348c2d27003071823c0a8e521950a9901a78d146a79f0ea2199b48c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpElementLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56815e20f9b2cbf2e13b73b4d73fc5ce94608ba353106f2f51a79f6d2c0b10d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceAuthConfigApiKeyConfig]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfigApiKeyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginInstanceAuthConfigApiKeyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3bff4cb7a6de9e22c6c1132409a12baeafb1d513ec24c6b2a229a56aa55737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig",
    jsii_struct_bases=[],
    name_mapping={"service_account": "serviceAccount"},
)
class GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig:
    def __init__(self, *, service_account: builtins.str) -> None:
        '''
        :param service_account: The service account to be used for authenticating request. The 'iam.serviceAccounts.getAccessToken' permission should be granted on this service account to the impersonator service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#service_account GoogleApihubPluginInstance#service_account}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d05d862c0fdcfaeb15a90adf8e6893ba905b5756ede9eb9f7ab385ca0be8b2)
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account": service_account,
        }

    @builtins.property
    def service_account(self) -> builtins.str:
        '''The service account to be used for authenticating request.

        The 'iam.serviceAccounts.getAccessToken' permission should be granted on
        this service account to the impersonator service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#service_account GoogleApihubPluginInstance#service_account}
        '''
        result = self._values.get("service_account")
        assert result is not None, "Required property 'service_account' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13ed57d6a2af5e3618e547a43a78be74a9fbeabe4c7a7df3e8105731dab33fe4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc8558345f846a840d4ce5adc581e73dcb588591d001052450b1d41e9075e6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad175373c9129f4514e2e922d9857849fdeb927f51faadc07ad66bcab607f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
)
class GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Union["GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param client_id: The client identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#client_id GoogleApihubPluginInstance#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#client_secret GoogleApihubPluginInstance#client_secret}
        '''
        if isinstance(client_secret, dict):
            client_secret = GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret(**client_secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176ac709881d2b483d35fa47b63ad81bab3267a390c4985e209a366e31926ec2)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The client identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#client_id GoogleApihubPluginInstance#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(
        self,
    ) -> "GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret":
        '''client_secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#client_secret GoogleApihubPluginInstance#client_secret}
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast("GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#secret_version GoogleApihubPluginInstance#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf3685ec3afff571ba4f9d8457db9c724e3385b2d91b9d9d0793a65d6a5a390)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#secret_version GoogleApihubPluginInstance#secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7dcca08fe7483063ce66abc35245009c814c4c7facde9dd544ada7f18a59308)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c633c223845163999918eb426c92d5b8901181e116166d15dbb2b3dc564ad651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7393480a22a2d598bdf08f44933f0c3616aac61091404f1ad5004ee0a2742080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db85646c61ab131742359ca96c49eebc88292e96113c1356cf272740572635f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientSecret")
    def put_client_secret(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#secret_version GoogleApihubPluginInstance#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putClientSecret", [value]))

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(
        self,
    ) -> GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecretOutputReference:
        return typing.cast(GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecretOutputReference, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514992f4bf347404e3c34671b1279f9b45ad48bb2c74a6a4056fdf17da3f5091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9868ee3c9b6e0ae0c1f530e738dd8fce902bcb87bce807c1b27b7214d969b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginInstanceAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fcd25ca802b0664be051b4e1921fc03f08944e1b1537879555f2c54a910c72c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApiKeyConfig")
    def put_api_key_config(
        self,
        *,
        api_key: typing.Union[GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey, typing.Dict[builtins.str, typing.Any]],
        http_element_location: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param api_key: api_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#api_key GoogleApihubPluginInstance#api_key}
        :param http_element_location: The location of the API key. The default value is QUERY. Possible values: HTTP_ELEMENT_LOCATION_UNSPECIFIED QUERY HEADER PATH BODY COOKIE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#http_element_location GoogleApihubPluginInstance#http_element_location}
        :param name: The parameter name of the API key. E.g. If the API request is "https://example.com/act?api_key=", "api_key" would be the parameter name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#name GoogleApihubPluginInstance#name}
        '''
        value = GoogleApihubPluginInstanceAuthConfigApiKeyConfig(
            api_key=api_key, http_element_location=http_element_location, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putApiKeyConfig", [value]))

    @jsii.member(jsii_name="putGoogleServiceAccountConfig")
    def put_google_service_account_config(
        self,
        *,
        service_account: builtins.str,
    ) -> None:
        '''
        :param service_account: The service account to be used for authenticating request. The 'iam.serviceAccounts.getAccessToken' permission should be granted on this service account to the impersonator service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#service_account GoogleApihubPluginInstance#service_account}
        '''
        value = GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig(
            service_account=service_account
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleServiceAccountConfig", [value]))

    @jsii.member(jsii_name="putOauth2ClientCredentialsConfig")
    def put_oauth2_client_credentials_config(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Union[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param client_id: The client identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#client_id GoogleApihubPluginInstance#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#client_secret GoogleApihubPluginInstance#client_secret}
        '''
        value = GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig(
            client_id=client_id, client_secret=client_secret
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2ClientCredentialsConfig", [value]))

    @jsii.member(jsii_name="putUserPasswordConfig")
    def put_user_password_config(
        self,
        *,
        password: typing.Union["GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword", typing.Dict[builtins.str, typing.Any]],
        username: builtins.str,
    ) -> None:
        '''
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#password GoogleApihubPluginInstance#password}
        :param username: Username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#username GoogleApihubPluginInstance#username}
        '''
        value = GoogleApihubPluginInstanceAuthConfigUserPasswordConfig(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putUserPasswordConfig", [value]))

    @jsii.member(jsii_name="resetApiKeyConfig")
    def reset_api_key_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKeyConfig", []))

    @jsii.member(jsii_name="resetGoogleServiceAccountConfig")
    def reset_google_service_account_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleServiceAccountConfig", []))

    @jsii.member(jsii_name="resetOauth2ClientCredentialsConfig")
    def reset_oauth2_client_credentials_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2ClientCredentialsConfig", []))

    @jsii.member(jsii_name="resetUserPasswordConfig")
    def reset_user_password_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPasswordConfig", []))

    @builtins.property
    @jsii.member(jsii_name="apiKeyConfig")
    def api_key_config(
        self,
    ) -> GoogleApihubPluginInstanceAuthConfigApiKeyConfigOutputReference:
        return typing.cast(GoogleApihubPluginInstanceAuthConfigApiKeyConfigOutputReference, jsii.get(self, "apiKeyConfig"))

    @builtins.property
    @jsii.member(jsii_name="googleServiceAccountConfig")
    def google_service_account_config(
        self,
    ) -> GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfigOutputReference:
        return typing.cast(GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfigOutputReference, jsii.get(self, "googleServiceAccountConfig"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentialsConfig")
    def oauth2_client_credentials_config(
        self,
    ) -> GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigOutputReference:
        return typing.cast(GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigOutputReference, jsii.get(self, "oauth2ClientCredentialsConfig"))

    @builtins.property
    @jsii.member(jsii_name="userPasswordConfig")
    def user_password_config(
        self,
    ) -> "GoogleApihubPluginInstanceAuthConfigUserPasswordConfigOutputReference":
        return typing.cast("GoogleApihubPluginInstanceAuthConfigUserPasswordConfigOutputReference", jsii.get(self, "userPasswordConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyConfigInput")
    def api_key_config_input(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceAuthConfigApiKeyConfig]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfigApiKeyConfig], jsii.get(self, "apiKeyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="googleServiceAccountConfigInput")
    def google_service_account_config_input(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig], jsii.get(self, "googleServiceAccountConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentialsConfigInput")
    def oauth2_client_credentials_config_input(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig], jsii.get(self, "oauth2ClientCredentialsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="userPasswordConfigInput")
    def user_password_config_input(
        self,
    ) -> typing.Optional["GoogleApihubPluginInstanceAuthConfigUserPasswordConfig"]:
        return typing.cast(typing.Optional["GoogleApihubPluginInstanceAuthConfigUserPasswordConfig"], jsii.get(self, "userPasswordConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe7667698f444afb8786716fc58a7eab5e07b3810a3218c86fd424491ad7bd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApihubPluginInstanceAuthConfig]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginInstanceAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4cf583d96b6f64e474277e03bc1673e02fcd6cc864279ff9430a6c116b57b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigUserPasswordConfig",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class GoogleApihubPluginInstanceAuthConfigUserPasswordConfig:
    def __init__(
        self,
        *,
        password: typing.Union["GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword", typing.Dict[builtins.str, typing.Any]],
        username: builtins.str,
    ) -> None:
        '''
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#password GoogleApihubPluginInstance#password}
        :param username: Username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#username GoogleApihubPluginInstance#username}
        '''
        if isinstance(password, dict):
            password = GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword(**password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc378c147f76359945ea105cef1a03b2cdac4c20841af54597ce3fb15570645)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(
        self,
    ) -> "GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword":
        '''password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#password GoogleApihubPluginInstance#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast("GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword", result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#username GoogleApihubPluginInstance#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceAuthConfigUserPasswordConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginInstanceAuthConfigUserPasswordConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigUserPasswordConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75670dd3ebed07f027cab88edd18524b300e100cc3302457d21edebe8178242a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPassword")
    def put_password(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#secret_version GoogleApihubPluginInstance#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putPassword", [value]))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(
        self,
    ) -> "GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPasswordOutputReference":
        return typing.cast("GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPasswordOutputReference", jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(
        self,
    ) -> typing.Optional["GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword"]:
        return typing.cast(typing.Optional["GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword"], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d557aef5cfe6ebc233343e20601ec3b9fffeb7dc6eb00096c9801f6bb7b3e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceAuthConfigUserPasswordConfig]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfigUserPasswordConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginInstanceAuthConfigUserPasswordConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00508ff6edf86e51e8addc92c7d6eaa979d533ad77a219f29d6c702cf546c9c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#secret_version GoogleApihubPluginInstance#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0988080ce481931ec8eced09b27f7f17499b4cd6b21ed53d89a3aa781edfc7)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#secret_version GoogleApihubPluginInstance#secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7dd88744e719bf46da9429031516e750d8096206699fec7746f467d5b09831a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b0f9ef633bad01afe3e3dd443a1aedbd343d44e8a76a6e6c6526db2968290d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword]:
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0288c86a4dff3948d46864436ae55d730a6343b8c54ebf3135dfd21b1008202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "location": "location",
        "plugin": "plugin",
        "plugin_instance_id": "pluginInstanceId",
        "actions": "actions",
        "auth_config": "authConfig",
        "disable": "disable",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleApihubPluginInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        location: builtins.str,
        plugin: builtins.str,
        plugin_instance_id: builtins.str,
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginInstanceActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_config: typing.Optional[typing.Union[GoogleApihubPluginInstanceAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApihubPluginInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The display name for this plugin instance. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#display_name GoogleApihubPluginInstance#display_name}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#location GoogleApihubPluginInstance#location}
        :param plugin: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#plugin GoogleApihubPluginInstance#plugin}
        :param plugin_instance_id: The ID to use for the plugin instance, which will become the final component of the plugin instance's resource name. This field is optional. - If provided, the same will be used. The service will throw an error if the specified id is already used by another plugin instance in the plugin resource. - If not provided, a system generated id will be used. This value should be 4-63 characters, and valid characters are /a-z[0-9]-_/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#plugin_instance_id GoogleApihubPluginInstance#plugin_instance_id}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#actions GoogleApihubPluginInstance#actions}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#auth_config GoogleApihubPluginInstance#auth_config}
        :param disable: The display name for this plugin instance. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#disable GoogleApihubPluginInstance#disable}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#id GoogleApihubPluginInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#project GoogleApihubPluginInstance#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#timeouts GoogleApihubPluginInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auth_config, dict):
            auth_config = GoogleApihubPluginInstanceAuthConfig(**auth_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleApihubPluginInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3105be53b790df01e5217739f6f5a81515c8422db184a3179012fd77ff3fdb5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument plugin", value=plugin, expected_type=type_hints["plugin"])
            check_type(argname="argument plugin_instance_id", value=plugin_instance_id, expected_type=type_hints["plugin_instance_id"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument auth_config", value=auth_config, expected_type=type_hints["auth_config"])
            check_type(argname="argument disable", value=disable, expected_type=type_hints["disable"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "location": location,
            "plugin": plugin,
            "plugin_instance_id": plugin_instance_id,
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
        if actions is not None:
            self._values["actions"] = actions
        if auth_config is not None:
            self._values["auth_config"] = auth_config
        if disable is not None:
            self._values["disable"] = disable
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
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
    def display_name(self) -> builtins.str:
        '''The display name for this plugin instance. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#display_name GoogleApihubPluginInstance#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#location GoogleApihubPluginInstance#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plugin(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#plugin GoogleApihubPluginInstance#plugin}
        '''
        result = self._values.get("plugin")
        assert result is not None, "Required property 'plugin' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plugin_instance_id(self) -> builtins.str:
        '''The ID to use for the plugin instance, which will become the final component of the plugin instance's resource name.

        This field is optional.

        - If provided, the same will be used. The service will throw an error if
          the specified id is already used by another plugin instance in the plugin
          resource.
        - If not provided, a system generated id will be used.

        This value should be 4-63 characters, and valid characters
        are /a-z[0-9]-_/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#plugin_instance_id GoogleApihubPluginInstance#plugin_instance_id}
        '''
        result = self._values.get("plugin_instance_id")
        assert result is not None, "Required property 'plugin_instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginInstanceActions]]]:
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#actions GoogleApihubPluginInstance#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginInstanceActions]]], result)

    @builtins.property
    def auth_config(self) -> typing.Optional[GoogleApihubPluginInstanceAuthConfig]:
        '''auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#auth_config GoogleApihubPluginInstance#auth_config}
        '''
        result = self._values.get("auth_config")
        return typing.cast(typing.Optional[GoogleApihubPluginInstanceAuthConfig], result)

    @builtins.property
    def disable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The display name for this plugin instance. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#disable GoogleApihubPluginInstance#disable}
        '''
        result = self._values.get("disable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#id GoogleApihubPluginInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#project GoogleApihubPluginInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleApihubPluginInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#timeouts GoogleApihubPluginInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleApihubPluginInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleApihubPluginInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#create GoogleApihubPluginInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#delete GoogleApihubPluginInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#update GoogleApihubPluginInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7fc1d958c1911598dfb4f7eb32baa736b6c232f6afef0b5d8ace596ef79398)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#create GoogleApihubPluginInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#delete GoogleApihubPluginInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin_instance#update GoogleApihubPluginInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPluginInstance.GoogleApihubPluginInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__208b1693eccf0f929164e436eb7d9b1f939c01ec259870ff7178f1367da2235f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90bdc4323829749a247eb834971aa50efcebab77f7d2c0af2e6c8d8a273880d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502ef8571022f091050d297f1c2a704d530d2d5c1e5ccc887a40dc52ab4be5db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c048dfceb22c3add577b2540164aaa73d03daa7f73802d9ab9267423b8d985a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a27f467cbaef0da1f23a661de4ae7692d569e2a7d1870de6de4dc043c89648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleApihubPluginInstance",
    "GoogleApihubPluginInstanceActions",
    "GoogleApihubPluginInstanceActionsCurationConfig",
    "GoogleApihubPluginInstanceActionsCurationConfigCustomCuration",
    "GoogleApihubPluginInstanceActionsCurationConfigCustomCurationOutputReference",
    "GoogleApihubPluginInstanceActionsCurationConfigOutputReference",
    "GoogleApihubPluginInstanceActionsHubInstanceAction",
    "GoogleApihubPluginInstanceActionsHubInstanceActionLastExecution",
    "GoogleApihubPluginInstanceActionsHubInstanceActionLastExecutionList",
    "GoogleApihubPluginInstanceActionsHubInstanceActionLastExecutionOutputReference",
    "GoogleApihubPluginInstanceActionsHubInstanceActionList",
    "GoogleApihubPluginInstanceActionsHubInstanceActionOutputReference",
    "GoogleApihubPluginInstanceActionsList",
    "GoogleApihubPluginInstanceActionsOutputReference",
    "GoogleApihubPluginInstanceAuthConfig",
    "GoogleApihubPluginInstanceAuthConfigApiKeyConfig",
    "GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey",
    "GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKeyOutputReference",
    "GoogleApihubPluginInstanceAuthConfigApiKeyConfigOutputReference",
    "GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig",
    "GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfigOutputReference",
    "GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig",
    "GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret",
    "GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecretOutputReference",
    "GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigOutputReference",
    "GoogleApihubPluginInstanceAuthConfigOutputReference",
    "GoogleApihubPluginInstanceAuthConfigUserPasswordConfig",
    "GoogleApihubPluginInstanceAuthConfigUserPasswordConfigOutputReference",
    "GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword",
    "GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPasswordOutputReference",
    "GoogleApihubPluginInstanceConfig",
    "GoogleApihubPluginInstanceTimeouts",
    "GoogleApihubPluginInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__70ccc9b3d88fd05a17a6059a3e956f2088497f4048e43f74eafa7452ea03e79d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    plugin: builtins.str,
    plugin_instance_id: builtins.str,
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginInstanceActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_config: typing.Optional[typing.Union[GoogleApihubPluginInstanceAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApihubPluginInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__55ad6aff47c4c29c35873205e2bb49e86370aa3c1aed8641380fb36767cb814c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21eae5bb8d2fd4f389626e57b609cf155618f67dfcf02ef0aabf891a95046038(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginInstanceActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1bc90ff03840cc9e1e61121b1f00b81dcff03801ce06565d12fba8a5f8bb127(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ab06da9858798cd0126dfed07eae7e1cda5d8d494520ce767f2dca4e08af07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fcd612ba6647fd34b2a8fc49c057a34c257dfa301fa888bac5cec800a6e34c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27af8d3142ea2267ee2ee75562ecdfe7845562b6a235aabd270344d4863c169c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0123c1d4e78f6eca68d04ade0e35472ec7c4df9d8767df28920142bb1548a87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e075d201d09512ad7ddce3221c8e55b59e95bbbe1e1c93331a6473df4c9486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e2c8f2df477af1b777a7ada5214daafb0dd6736752f6d166b6557d2be2e341(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5d8556f880e09f4e550118d3dbc0a60d17cd48ce8b8c3bff741ccf8f06a720(
    *,
    action_id: builtins.str,
    curation_config: typing.Optional[typing.Union[GoogleApihubPluginInstanceActionsCurationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule_cron_expression: typing.Optional[builtins.str] = None,
    schedule_time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb3fa19e4f3ba55ced4930d156023dcb7e2a966febc99650a798558bb0c51f6(
    *,
    curation_type: typing.Optional[builtins.str] = None,
    custom_curation: typing.Optional[typing.Union[GoogleApihubPluginInstanceActionsCurationConfigCustomCuration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b8d7e93fede7b6da25ded43fb2ed49d5c455c9f15197510938917723dad77e(
    *,
    curation: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1d83d34a332b4a71e5fb5713fef2ae5b948ab38d836e268a28335cb6c45a16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed03eda1ccc04a6428fd0d87b2f927b9420b1d4c02f00886cc472bc3230530f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9e18374d0aa0553b940a4a7bdddcbcf0f8f61bfd0491bb0080ed16a5f98077(
    value: typing.Optional[GoogleApihubPluginInstanceActionsCurationConfigCustomCuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ec4a321371ffcdae82f5b7c44663afeafd1e29f5d45ece755e1e3c9d5890af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821cfeae9090b668eeaea1889bd4e56b402276a6a5b4b8ce61610aad75c00385(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ab4fe69299a799de67f968b1f4ced03aaea25c651808747b2323332d22c292(
    value: typing.Optional[GoogleApihubPluginInstanceActionsCurationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e22d4e3e7e4a901fce03a59e30c42c48a5d3ea4cedef1edd8b05a4a6f88762c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b386c213e81f1fdd371bbd3af0bc351baddb9fde46ffcd1b4cdb3e5b37a19f68(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f70a546762cb5c9d95da7083497f40a61905e9149fbf83c5e46d5a4d66b0f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff7e9a562f1d94429c3bb8021bb0e71bfed943a9fdbe77df13171d9fd150bd2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e1a39f85a6c48d26b1a43298e44f32cc4f8b2931deaa6c5db8af6ef8c98c6a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8dc8e33a7a3e3b1722db2518e9a1bd6065cb53ccb263e5237959f834465fe88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39df146f3b03fcf918a37394f80046ff8d03f7f1127854f8bd6cd826cdea589(
    value: typing.Optional[GoogleApihubPluginInstanceActionsHubInstanceActionLastExecution],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20294e3fd2c4534c59d49955fe1674d4baa80bc0d0c231b4a9628ea343860300(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b3c882f0bd7b4ba67ce20243ec1d4dbbf374f1d44e26e333995c72e6081d5b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750a749f17979be9d91dd4d24c8716591ec0578768a173db534cd9bde339cd89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6802dcf83e6f4c4ceafe4fa1f138f8dd614e5e6fc8f595c7d42489415bb6c6f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205689bf7c44803bd56aba8e4753d1ee763211b942f9deac109c7b89f59a4a69(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb999efac53709dc5526376dd1d103609d14cca713c056f79f783111cf33564(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4367edf0ede925ad02a5700c728c014bd35ae7cbb2a099f88e5e6282d990dba8(
    value: typing.Optional[GoogleApihubPluginInstanceActionsHubInstanceAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d4dce70166597f0f185795148e5490115cf64d7dc55ae904570653ac9e8516(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8bae74f180974d14a979fd23e396d7223e1e50c970001b2f5eedc15e46e5a5c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d8bdd3a179dbf5754645b77e1e8932e9790191dd733ecfcadd3ddb082982d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6758ebca1acee0d4bc0f569a2e7c74b8edeb9de30a333093d1aba43369cde492(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739a917473870108531773e9c3372ea6ff44eff64cb8f6fbf5c9b1d7e6317bd5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2192a8188c6b1b0e93b7f518c59538ed3afcc0ab19e933a392db7aa90994138a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginInstanceActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09bab300ed39caba829039decbc60ff681b69ee1e218800c0b3ea7cb76d4e744(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4784f6a74f2f4983d1a523b0df8fd973fc37cf40f26223adb1c2ba8ed30e172(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20002f6a16aadc495dfca630c4ebd945c42f14c44113d79e27cd2e7d4b58e40f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424baaed2767132817fee57085f32dc0e090c853395e17ee920ec8826ff8192d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c629af21315effa47f538af108bfa958c7229b5e7b098254323de6a1602cad7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginInstanceActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03369ea77fd7db0e56baee463044c4095cd83f556be726d23ea2aef4f03359bf(
    *,
    auth_type: builtins.str,
    api_key_config: typing.Optional[typing.Union[GoogleApihubPluginInstanceAuthConfigApiKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    google_service_account_config: typing.Optional[typing.Union[GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2_client_credentials_config: typing.Optional[typing.Union[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    user_password_config: typing.Optional[typing.Union[GoogleApihubPluginInstanceAuthConfigUserPasswordConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c091ddb93b07e9aef151f33d620b1fca4f116f148f0e417a12d28532dbb6e34(
    *,
    api_key: typing.Union[GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey, typing.Dict[builtins.str, typing.Any]],
    http_element_location: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0620c0a89d17901cccbef23336b489660538119539dbbb2c54cf8806168a4863(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdc3a20628fa734a39f6a2e9d914f59f6f1f7549feba30ed063771d9113e5e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6791817aa58675b2f0cb926356aa4dfe9d51825d25156e8c2900a50b7a958bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be00dcba2e3c5f4dbbc4cf268d70b755c5295ad42a7c45a785b03ed47823b773(
    value: typing.Optional[GoogleApihubPluginInstanceAuthConfigApiKeyConfigApiKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe512089d9f88744a35d6d2abae9d5041abb66327488ef45e11d8d783cda9ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b9850da348c2d27003071823c0a8e521950a9901a78d146a79f0ea2199b48c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56815e20f9b2cbf2e13b73b4d73fc5ce94608ba353106f2f51a79f6d2c0b10d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3bff4cb7a6de9e22c6c1132409a12baeafb1d513ec24c6b2a229a56aa55737(
    value: typing.Optional[GoogleApihubPluginInstanceAuthConfigApiKeyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d05d862c0fdcfaeb15a90adf8e6893ba905b5756ede9eb9f7ab385ca0be8b2(
    *,
    service_account: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ed57d6a2af5e3618e547a43a78be74a9fbeabe4c7a7df3e8105731dab33fe4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc8558345f846a840d4ce5adc581e73dcb588591d001052450b1d41e9075e6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad175373c9129f4514e2e922d9857849fdeb927f51faadc07ad66bcab607f2d(
    value: typing.Optional[GoogleApihubPluginInstanceAuthConfigGoogleServiceAccountConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176ac709881d2b483d35fa47b63ad81bab3267a390c4985e209a366e31926ec2(
    *,
    client_id: builtins.str,
    client_secret: typing.Union[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf3685ec3afff571ba4f9d8457db9c724e3385b2d91b9d9d0793a65d6a5a390(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7dcca08fe7483063ce66abc35245009c814c4c7facde9dd544ada7f18a59308(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c633c223845163999918eb426c92d5b8901181e116166d15dbb2b3dc564ad651(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7393480a22a2d598bdf08f44933f0c3616aac61091404f1ad5004ee0a2742080(
    value: typing.Optional[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db85646c61ab131742359ca96c49eebc88292e96113c1356cf272740572635f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514992f4bf347404e3c34671b1279f9b45ad48bb2c74a6a4056fdf17da3f5091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9868ee3c9b6e0ae0c1f530e738dd8fce902bcb87bce807c1b27b7214d969b0(
    value: typing.Optional[GoogleApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fcd25ca802b0664be051b4e1921fc03f08944e1b1537879555f2c54a910c72c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe7667698f444afb8786716fc58a7eab5e07b3810a3218c86fd424491ad7bd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4cf583d96b6f64e474277e03bc1673e02fcd6cc864279ff9430a6c116b57b8(
    value: typing.Optional[GoogleApihubPluginInstanceAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc378c147f76359945ea105cef1a03b2cdac4c20841af54597ce3fb15570645(
    *,
    password: typing.Union[GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword, typing.Dict[builtins.str, typing.Any]],
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75670dd3ebed07f027cab88edd18524b300e100cc3302457d21edebe8178242a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d557aef5cfe6ebc233343e20601ec3b9fffeb7dc6eb00096c9801f6bb7b3e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00508ff6edf86e51e8addc92c7d6eaa979d533ad77a219f29d6c702cf546c9c3(
    value: typing.Optional[GoogleApihubPluginInstanceAuthConfigUserPasswordConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0988080ce481931ec8eced09b27f7f17499b4cd6b21ed53d89a3aa781edfc7(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7dd88744e719bf46da9429031516e750d8096206699fec7746f467d5b09831a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b0f9ef633bad01afe3e3dd443a1aedbd343d44e8a76a6e6c6526db2968290d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0288c86a4dff3948d46864436ae55d730a6343b8c54ebf3135dfd21b1008202(
    value: typing.Optional[GoogleApihubPluginInstanceAuthConfigUserPasswordConfigPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3105be53b790df01e5217739f6f5a81515c8422db184a3179012fd77ff3fdb5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    location: builtins.str,
    plugin: builtins.str,
    plugin_instance_id: builtins.str,
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginInstanceActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_config: typing.Optional[typing.Union[GoogleApihubPluginInstanceAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApihubPluginInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7fc1d958c1911598dfb4f7eb32baa736b6c232f6afef0b5d8ace596ef79398(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208b1693eccf0f929164e436eb7d9b1f939c01ec259870ff7178f1367da2235f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90bdc4323829749a247eb834971aa50efcebab77f7d2c0af2e6c8d8a273880d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502ef8571022f091050d297f1c2a704d530d2d5c1e5ccc887a40dc52ab4be5db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c048dfceb22c3add577b2540164aaa73d03daa7f73802d9ab9267423b8d985a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a27f467cbaef0da1f23a661de4ae7692d569e2a7d1870de6de4dc043c89648(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
