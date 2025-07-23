r'''
# `google_apihub_plugin_instance`

Refer to the Terraform Registry for docs: [`google_apihub_plugin_instance`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance).
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


class ApihubPluginInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance google_apihub_plugin_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        plugin: builtins.str,
        plugin_instance_id: builtins.str,
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApihubPluginInstanceActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_config: typing.Optional[typing.Union["ApihubPluginInstanceAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApihubPluginInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance google_apihub_plugin_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The display name for this plugin instance. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#display_name ApihubPluginInstance#display_name}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#location ApihubPluginInstance#location}
        :param plugin: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#plugin ApihubPluginInstance#plugin}
        :param plugin_instance_id: The ID to use for the plugin instance, which will become the final component of the plugin instance's resource name. This field is optional. - If provided, the same will be used. The service will throw an error if the specified id is already used by another plugin instance in the plugin resource. - If not provided, a system generated id will be used. This value should be 4-63 characters, and valid characters are /a-z[0-9]-_/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#plugin_instance_id ApihubPluginInstance#plugin_instance_id}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#actions ApihubPluginInstance#actions}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#auth_config ApihubPluginInstance#auth_config}
        :param disable: The display name for this plugin instance. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#disable ApihubPluginInstance#disable}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#id ApihubPluginInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#project ApihubPluginInstance#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#timeouts ApihubPluginInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593afa281ec915f6d51a38f60fdae46dc24eadaf232f1416928ef39d4df1faf4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApihubPluginInstanceConfig(
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
        '''Generates CDKTF code for importing a ApihubPluginInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApihubPluginInstance to import.
        :param import_from_id: The id of the existing ApihubPluginInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApihubPluginInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3711db439d7c9dbe0aa0eeaaefa7602bec6eb28f91da4903b94a5d02556adf53)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApihubPluginInstanceActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__636835dea3273121f1b309fa9ac4c238b086aa90f541d553e6b761049fee2e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putAuthConfig")
    def put_auth_config(
        self,
        *,
        auth_type: builtins.str,
        api_key_config: typing.Optional[typing.Union["ApihubPluginInstanceAuthConfigApiKeyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        google_service_account_config: typing.Optional[typing.Union["ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_client_credentials_config: typing.Optional[typing.Union["ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        user_password_config: typing.Optional[typing.Union["ApihubPluginInstanceAuthConfigUserPasswordConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auth_type: Possible values: AUTH_TYPE_UNSPECIFIED NO_AUTH GOOGLE_SERVICE_ACCOUNT USER_PASSWORD API_KEY OAUTH2_CLIENT_CREDENTIALS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#auth_type ApihubPluginInstance#auth_type}
        :param api_key_config: api_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#api_key_config ApihubPluginInstance#api_key_config}
        :param google_service_account_config: google_service_account_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#google_service_account_config ApihubPluginInstance#google_service_account_config}
        :param oauth2_client_credentials_config: oauth2_client_credentials_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#oauth2_client_credentials_config ApihubPluginInstance#oauth2_client_credentials_config}
        :param user_password_config: user_password_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#user_password_config ApihubPluginInstance#user_password_config}
        '''
        value = ApihubPluginInstanceAuthConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#create ApihubPluginInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#delete ApihubPluginInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#update ApihubPluginInstance#update}.
        '''
        value = ApihubPluginInstanceTimeouts(
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
    def actions(self) -> "ApihubPluginInstanceActionsList":
        return typing.cast("ApihubPluginInstanceActionsList", jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="authConfig")
    def auth_config(self) -> "ApihubPluginInstanceAuthConfigOutputReference":
        return typing.cast("ApihubPluginInstanceAuthConfigOutputReference", jsii.get(self, "authConfig"))

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
    def timeouts(self) -> "ApihubPluginInstanceTimeoutsOutputReference":
        return typing.cast("ApihubPluginInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApihubPluginInstanceActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApihubPluginInstanceActions"]]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="authConfigInput")
    def auth_config_input(self) -> typing.Optional["ApihubPluginInstanceAuthConfig"]:
        return typing.cast(typing.Optional["ApihubPluginInstanceAuthConfig"], jsii.get(self, "authConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApihubPluginInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApihubPluginInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__13087f4d259707f8dc327cff69435cc31b992ea982859208c5a8dafd6bcb54da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334f32397f5dbd0bd37e370d38b2dce15f78a88e07a8c708de0280e050a4d41a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0ff77d3bc5c421645f727dc7588d5fa1f6f055bb3590336c9acdede2279d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7018023aff3fd644286be0a39f5a9f04df609c7b82eaeefedfa5fc906e0fe995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="plugin")
    def plugin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "plugin"))

    @plugin.setter
    def plugin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbe855dec0857c0a8c4ca37a47ba084d98551e7ebd62e8ea023f9fedaa2a18e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plugin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginInstanceId")
    def plugin_instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginInstanceId"))

    @plugin_instance_id.setter
    def plugin_instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5785d41444f0491f36baeeeb610579c2100094ea80f425298a5fa8de098563b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginInstanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96235b74515d777cf5462339439c6217f55f64e595b3f7c2ed9a00a21f41b749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActions",
    jsii_struct_bases=[],
    name_mapping={
        "action_id": "actionId",
        "curation_config": "curationConfig",
        "schedule_cron_expression": "scheduleCronExpression",
        "schedule_time_zone": "scheduleTimeZone",
    },
)
class ApihubPluginInstanceActions:
    def __init__(
        self,
        *,
        action_id: builtins.str,
        curation_config: typing.Optional[typing.Union["ApihubPluginInstanceActionsCurationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule_cron_expression: typing.Optional[builtins.str] = None,
        schedule_time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action_id: This should map to one of the action id specified in actions_config in the plugin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#action_id ApihubPluginInstance#action_id}
        :param curation_config: curation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#curation_config ApihubPluginInstance#curation_config}
        :param schedule_cron_expression: The schedule for this plugin instance action. This can only be set if the plugin supports API_HUB_SCHEDULE_TRIGGER mode for this action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#schedule_cron_expression ApihubPluginInstance#schedule_cron_expression}
        :param schedule_time_zone: The time zone for the schedule cron expression. If not provided, UTC will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#schedule_time_zone ApihubPluginInstance#schedule_time_zone}
        '''
        if isinstance(curation_config, dict):
            curation_config = ApihubPluginInstanceActionsCurationConfig(**curation_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddff3dca95db95d9d0baae4a5c878e9828155764fdcec36c99fa629a9e0238bb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#action_id ApihubPluginInstance#action_id}
        '''
        result = self._values.get("action_id")
        assert result is not None, "Required property 'action_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def curation_config(
        self,
    ) -> typing.Optional["ApihubPluginInstanceActionsCurationConfig"]:
        '''curation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#curation_config ApihubPluginInstance#curation_config}
        '''
        result = self._values.get("curation_config")
        return typing.cast(typing.Optional["ApihubPluginInstanceActionsCurationConfig"], result)

    @builtins.property
    def schedule_cron_expression(self) -> typing.Optional[builtins.str]:
        '''The schedule for this plugin instance action.

        This can only be set if the
        plugin supports API_HUB_SCHEDULE_TRIGGER mode for this action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#schedule_cron_expression ApihubPluginInstance#schedule_cron_expression}
        '''
        result = self._values.get("schedule_cron_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone for the schedule cron expression. If not provided, UTC will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#schedule_time_zone ApihubPluginInstance#schedule_time_zone}
        '''
        result = self._values.get("schedule_time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginInstanceActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActionsCurationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "curation_type": "curationType",
        "custom_curation": "customCuration",
    },
)
class ApihubPluginInstanceActionsCurationConfig:
    def __init__(
        self,
        *,
        curation_type: typing.Optional[builtins.str] = None,
        custom_curation: typing.Optional[typing.Union["ApihubPluginInstanceActionsCurationConfigCustomCuration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param curation_type: Possible values: CURATION_TYPE_UNSPECIFIED DEFAULT_CURATION_FOR_API_METADATA CUSTOM_CURATION_FOR_API_METADATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#curation_type ApihubPluginInstance#curation_type}
        :param custom_curation: custom_curation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#custom_curation ApihubPluginInstance#custom_curation}
        '''
        if isinstance(custom_curation, dict):
            custom_curation = ApihubPluginInstanceActionsCurationConfigCustomCuration(**custom_curation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f3cc12ff83e499d7209101b7131b4626668b115bf66895a270d1f09b84be62)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#curation_type ApihubPluginInstance#curation_type}
        '''
        result = self._values.get("curation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_curation(
        self,
    ) -> typing.Optional["ApihubPluginInstanceActionsCurationConfigCustomCuration"]:
        '''custom_curation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#custom_curation ApihubPluginInstance#custom_curation}
        '''
        result = self._values.get("custom_curation")
        return typing.cast(typing.Optional["ApihubPluginInstanceActionsCurationConfigCustomCuration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginInstanceActionsCurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActionsCurationConfigCustomCuration",
    jsii_struct_bases=[],
    name_mapping={"curation": "curation"},
)
class ApihubPluginInstanceActionsCurationConfigCustomCuration:
    def __init__(self, *, curation: builtins.str) -> None:
        '''
        :param curation: The unique name of the curation resource. This will be the name of the curation resource in the format: 'projects/{project}/locations/{location}/curations/{curation}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#curation ApihubPluginInstance#curation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5c5030af187fd168f80e1edeadef260e2994bd4da45a967494191c6c63e940)
            check_type(argname="argument curation", value=curation, expected_type=type_hints["curation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "curation": curation,
        }

    @builtins.property
    def curation(self) -> builtins.str:
        '''The unique name of the curation resource. This will be the name of the curation resource in the format: 'projects/{project}/locations/{location}/curations/{curation}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#curation ApihubPluginInstance#curation}
        '''
        result = self._values.get("curation")
        assert result is not None, "Required property 'curation' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginInstanceActionsCurationConfigCustomCuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginInstanceActionsCurationConfigCustomCurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActionsCurationConfigCustomCurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4809c0d547b2d1eac6bfadc27b17d47a77900e48fbdca916cdde15a486a308e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__150cc910ee6e265f80ed9e72db093c6c4779db25d55b1dd494e4e11102bd9472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "curation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApihubPluginInstanceActionsCurationConfigCustomCuration]:
        return typing.cast(typing.Optional[ApihubPluginInstanceActionsCurationConfigCustomCuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginInstanceActionsCurationConfigCustomCuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe151377cb631c57087bbf21f88c9ae74cc0ffa4aab2ff44021d83f2dd23a76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginInstanceActionsCurationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActionsCurationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97149738bb214f9a3a5e97548963be17701c05a5a2a589cef02b95047696ea9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomCuration")
    def put_custom_curation(self, *, curation: builtins.str) -> None:
        '''
        :param curation: The unique name of the curation resource. This will be the name of the curation resource in the format: 'projects/{project}/locations/{location}/curations/{curation}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#curation ApihubPluginInstance#curation}
        '''
        value = ApihubPluginInstanceActionsCurationConfigCustomCuration(
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
    ) -> ApihubPluginInstanceActionsCurationConfigCustomCurationOutputReference:
        return typing.cast(ApihubPluginInstanceActionsCurationConfigCustomCurationOutputReference, jsii.get(self, "customCuration"))

    @builtins.property
    @jsii.member(jsii_name="curationTypeInput")
    def curation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "curationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="customCurationInput")
    def custom_curation_input(
        self,
    ) -> typing.Optional[ApihubPluginInstanceActionsCurationConfigCustomCuration]:
        return typing.cast(typing.Optional[ApihubPluginInstanceActionsCurationConfigCustomCuration], jsii.get(self, "customCurationInput"))

    @builtins.property
    @jsii.member(jsii_name="curationType")
    def curation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "curationType"))

    @curation_type.setter
    def curation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080d6e3f35f91214b7974581d58df2d77719582232067e4695229b05498c53bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "curationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApihubPluginInstanceActionsCurationConfig]:
        return typing.cast(typing.Optional[ApihubPluginInstanceActionsCurationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginInstanceActionsCurationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51128e69582893b34d93e9daa4fd84a5a4040456481e4c7a68c5e21c26ff6396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActionsHubInstanceAction",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApihubPluginInstanceActionsHubInstanceAction:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginInstanceActionsHubInstanceAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActionsHubInstanceActionLastExecution",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApihubPluginInstanceActionsHubInstanceActionLastExecution:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginInstanceActionsHubInstanceActionLastExecution(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginInstanceActionsHubInstanceActionLastExecutionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActionsHubInstanceActionLastExecutionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64047b760d14fd381bdb26c928321eb1a61be6a1a211810bea286f878699641a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApihubPluginInstanceActionsHubInstanceActionLastExecutionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ad1130a251ce00da529acc295d07f974f42c885a968744fdb07ea38f5396ea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApihubPluginInstanceActionsHubInstanceActionLastExecutionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f42129170d95975656f2c40d613d36d39dda46df30d57b3af82cc90a473012)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6641860af9fb7693eeb2aae92f33eaa2471cb3615bb46ec1b19702279b81b60b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8edc465d7bbdb8eb822407d8e418e388664b3cf792c2cb41bfaf31f54419862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApihubPluginInstanceActionsHubInstanceActionLastExecutionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActionsHubInstanceActionLastExecutionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba3b753d49ec26ac94414132d8b8a58c634771c521ed1098f1df987ed1e6ae8c)
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
    ) -> typing.Optional[ApihubPluginInstanceActionsHubInstanceActionLastExecution]:
        return typing.cast(typing.Optional[ApihubPluginInstanceActionsHubInstanceActionLastExecution], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginInstanceActionsHubInstanceActionLastExecution],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a349e1b0469c02a45802517a81fc3e44f536bb08210b2151b5dfae1b7bb854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginInstanceActionsHubInstanceActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActionsHubInstanceActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__791fd07539fe34a270eb3e7e47e82f70dfc909dd3ddb2866675929eed5b97b9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApihubPluginInstanceActionsHubInstanceActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f13399dc1513332fc2f3a5087509d2baf3ba5e702f7a5449964cf29e05b37f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApihubPluginInstanceActionsHubInstanceActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d6647b75d21405aa7279dea72783f2207cea39b99f4615fb80cfa9b9ff9b40d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__691ad99e3c2c5a605a04be4fae097ec4d9faca0f7756954dfd7fde155282b09c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c13e9c7a7396d41124367d8c2695fb1b19f16499389a8436efae112714efe8c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApihubPluginInstanceActionsHubInstanceActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActionsHubInstanceActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c09a1bb95353ba274b901359cf28257fe6f690ec20f7383668ba0d0ad94870f)
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
    ) -> ApihubPluginInstanceActionsHubInstanceActionLastExecutionList:
        return typing.cast(ApihubPluginInstanceActionsHubInstanceActionLastExecutionList, jsii.get(self, "lastExecution"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApihubPluginInstanceActionsHubInstanceAction]:
        return typing.cast(typing.Optional[ApihubPluginInstanceActionsHubInstanceAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginInstanceActionsHubInstanceAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd8f20704c3b80c30626bcf8c96038be6cc0ab02a49bcac783df4c4d5e1af2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginInstanceActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd6967c2a39a9d2ba04e2aaea0544120a5b8888601db13c20b254883a7b3a34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApihubPluginInstanceActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f4e4ed51b4524c08fe2ec0123de6852b95c01da5ee2435130047a16ce49610)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApihubPluginInstanceActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935b18385d9aa2b33bc55a27d5d9193cc2b7679276b0b1c46bcdf56b8752a1ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d930bec602ca2ba5d58faefda8ede58148db7661c9ac3d73fe2e2e8eba50e38f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffa577202af274f3846442505635ce0ebed2252794a350657a0c5b4b51f1e1c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginInstanceActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginInstanceActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginInstanceActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b06d2d5720bc3675ac40add588d20cb181870fb647b3608ba1b97f1dd97fb02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginInstanceActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e04cedc9b868dc947675cb026091a200b46201bf9c48fc616b327558a1341fbf)
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
        custom_curation: typing.Optional[typing.Union[ApihubPluginInstanceActionsCurationConfigCustomCuration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param curation_type: Possible values: CURATION_TYPE_UNSPECIFIED DEFAULT_CURATION_FOR_API_METADATA CUSTOM_CURATION_FOR_API_METADATA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#curation_type ApihubPluginInstance#curation_type}
        :param custom_curation: custom_curation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#custom_curation ApihubPluginInstance#custom_curation}
        '''
        value = ApihubPluginInstanceActionsCurationConfig(
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
    ) -> ApihubPluginInstanceActionsCurationConfigOutputReference:
        return typing.cast(ApihubPluginInstanceActionsCurationConfigOutputReference, jsii.get(self, "curationConfig"))

    @builtins.property
    @jsii.member(jsii_name="hubInstanceAction")
    def hub_instance_action(self) -> ApihubPluginInstanceActionsHubInstanceActionList:
        return typing.cast(ApihubPluginInstanceActionsHubInstanceActionList, jsii.get(self, "hubInstanceAction"))

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
    ) -> typing.Optional[ApihubPluginInstanceActionsCurationConfig]:
        return typing.cast(typing.Optional[ApihubPluginInstanceActionsCurationConfig], jsii.get(self, "curationConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__87ec17c36b2c79fd9449cfc58134d44544f16c3192d7434aa02846de4c9eb9f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleCronExpression")
    def schedule_cron_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleCronExpression"))

    @schedule_cron_expression.setter
    def schedule_cron_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2cc4779fe05da1a8ce27cf7a85abbdaa02138b11c65a7ff2cd2b173913bb672)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleCronExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleTimeZone")
    def schedule_time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleTimeZone"))

    @schedule_time_zone.setter
    def schedule_time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ca461056b0ee62bb2ee2d2f23808642665e22acf9e28fbbdeec600498ded59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleTimeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginInstanceActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginInstanceActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginInstanceActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abba25ca071676e206e8007eaedc7e2cb109f24a05f2a0b98622e43b23eec097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "api_key_config": "apiKeyConfig",
        "google_service_account_config": "googleServiceAccountConfig",
        "oauth2_client_credentials_config": "oauth2ClientCredentialsConfig",
        "user_password_config": "userPasswordConfig",
    },
)
class ApihubPluginInstanceAuthConfig:
    def __init__(
        self,
        *,
        auth_type: builtins.str,
        api_key_config: typing.Optional[typing.Union["ApihubPluginInstanceAuthConfigApiKeyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        google_service_account_config: typing.Optional[typing.Union["ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_client_credentials_config: typing.Optional[typing.Union["ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        user_password_config: typing.Optional[typing.Union["ApihubPluginInstanceAuthConfigUserPasswordConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auth_type: Possible values: AUTH_TYPE_UNSPECIFIED NO_AUTH GOOGLE_SERVICE_ACCOUNT USER_PASSWORD API_KEY OAUTH2_CLIENT_CREDENTIALS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#auth_type ApihubPluginInstance#auth_type}
        :param api_key_config: api_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#api_key_config ApihubPluginInstance#api_key_config}
        :param google_service_account_config: google_service_account_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#google_service_account_config ApihubPluginInstance#google_service_account_config}
        :param oauth2_client_credentials_config: oauth2_client_credentials_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#oauth2_client_credentials_config ApihubPluginInstance#oauth2_client_credentials_config}
        :param user_password_config: user_password_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#user_password_config ApihubPluginInstance#user_password_config}
        '''
        if isinstance(api_key_config, dict):
            api_key_config = ApihubPluginInstanceAuthConfigApiKeyConfig(**api_key_config)
        if isinstance(google_service_account_config, dict):
            google_service_account_config = ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig(**google_service_account_config)
        if isinstance(oauth2_client_credentials_config, dict):
            oauth2_client_credentials_config = ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig(**oauth2_client_credentials_config)
        if isinstance(user_password_config, dict):
            user_password_config = ApihubPluginInstanceAuthConfigUserPasswordConfig(**user_password_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6fff044d591e14057e937df1ef7b306057bb8742be9b0e9f3db684615c7f18c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#auth_type ApihubPluginInstance#auth_type}
        '''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key_config(
        self,
    ) -> typing.Optional["ApihubPluginInstanceAuthConfigApiKeyConfig"]:
        '''api_key_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#api_key_config ApihubPluginInstance#api_key_config}
        '''
        result = self._values.get("api_key_config")
        return typing.cast(typing.Optional["ApihubPluginInstanceAuthConfigApiKeyConfig"], result)

    @builtins.property
    def google_service_account_config(
        self,
    ) -> typing.Optional["ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig"]:
        '''google_service_account_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#google_service_account_config ApihubPluginInstance#google_service_account_config}
        '''
        result = self._values.get("google_service_account_config")
        return typing.cast(typing.Optional["ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig"], result)

    @builtins.property
    def oauth2_client_credentials_config(
        self,
    ) -> typing.Optional["ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig"]:
        '''oauth2_client_credentials_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#oauth2_client_credentials_config ApihubPluginInstance#oauth2_client_credentials_config}
        '''
        result = self._values.get("oauth2_client_credentials_config")
        return typing.cast(typing.Optional["ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig"], result)

    @builtins.property
    def user_password_config(
        self,
    ) -> typing.Optional["ApihubPluginInstanceAuthConfigUserPasswordConfig"]:
        '''user_password_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#user_password_config ApihubPluginInstance#user_password_config}
        '''
        result = self._values.get("user_password_config")
        return typing.cast(typing.Optional["ApihubPluginInstanceAuthConfigUserPasswordConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginInstanceAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigApiKeyConfig",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "http_element_location": "httpElementLocation",
        "name": "name",
    },
)
class ApihubPluginInstanceAuthConfigApiKeyConfig:
    def __init__(
        self,
        *,
        api_key: typing.Union["ApihubPluginInstanceAuthConfigApiKeyConfigApiKey", typing.Dict[builtins.str, typing.Any]],
        http_element_location: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param api_key: api_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#api_key ApihubPluginInstance#api_key}
        :param http_element_location: The location of the API key. The default value is QUERY. Possible values: HTTP_ELEMENT_LOCATION_UNSPECIFIED QUERY HEADER PATH BODY COOKIE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#http_element_location ApihubPluginInstance#http_element_location}
        :param name: The parameter name of the API key. E.g. If the API request is "https://example.com/act?api_key=", "api_key" would be the parameter name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#name ApihubPluginInstance#name}
        '''
        if isinstance(api_key, dict):
            api_key = ApihubPluginInstanceAuthConfigApiKeyConfigApiKey(**api_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17619b45d823301a07f5221a14e82bdd0321fffb402212355d356376c03b686)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument http_element_location", value=http_element_location, expected_type=type_hints["http_element_location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
            "http_element_location": http_element_location,
            "name": name,
        }

    @builtins.property
    def api_key(self) -> "ApihubPluginInstanceAuthConfigApiKeyConfigApiKey":
        '''api_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#api_key ApihubPluginInstance#api_key}
        '''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast("ApihubPluginInstanceAuthConfigApiKeyConfigApiKey", result)

    @builtins.property
    def http_element_location(self) -> builtins.str:
        '''The location of the API key. The default value is QUERY. Possible values: HTTP_ELEMENT_LOCATION_UNSPECIFIED QUERY HEADER PATH BODY COOKIE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#http_element_location ApihubPluginInstance#http_element_location}
        '''
        result = self._values.get("http_element_location")
        assert result is not None, "Required property 'http_element_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The parameter name of the API key. E.g. If the API request is "https://example.com/act?api_key=", "api_key" would be the parameter name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#name ApihubPluginInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginInstanceAuthConfigApiKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigApiKeyConfigApiKey",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class ApihubPluginInstanceAuthConfigApiKeyConfigApiKey:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#secret_version ApihubPluginInstance#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d663937ba17add16c2639d240343f00cb4647ef2e97beeff5768d58b456396)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#secret_version ApihubPluginInstance#secret_version}

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
        return "ApihubPluginInstanceAuthConfigApiKeyConfigApiKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginInstanceAuthConfigApiKeyConfigApiKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigApiKeyConfigApiKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9627defe7a18500d973fe408f5606a4c38a86a0073fc4aae3b8d566c0d315b8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__521d36737db806619f963f4b8fc8973c700111ef4b6f8758ba5e41201e157ee3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApihubPluginInstanceAuthConfigApiKeyConfigApiKey]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfigApiKeyConfigApiKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginInstanceAuthConfigApiKeyConfigApiKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813d43b990b6702c722a081ae66c239b536db87e5fd7c95c2de2df8f1a18e2f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginInstanceAuthConfigApiKeyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigApiKeyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f78d4a7e460c9572d7406f45370194bf969dc903c9cf32724447f0ab1c927507)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApiKey")
    def put_api_key(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#secret_version ApihubPluginInstance#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = ApihubPluginInstanceAuthConfigApiKeyConfigApiKey(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putApiKey", [value]))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(
        self,
    ) -> ApihubPluginInstanceAuthConfigApiKeyConfigApiKeyOutputReference:
        return typing.cast(ApihubPluginInstanceAuthConfigApiKeyConfigApiKeyOutputReference, jsii.get(self, "apiKey"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(
        self,
    ) -> typing.Optional[ApihubPluginInstanceAuthConfigApiKeyConfigApiKey]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfigApiKeyConfigApiKey], jsii.get(self, "apiKeyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2f1a0d4e05f929cd1186dd83707986765d30a9f52130b04b96e023006ffc1546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpElementLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0bf985b76d2ed793be63a1a40518d38ebd93d1e7df5a17d5f707ad99e55d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApihubPluginInstanceAuthConfigApiKeyConfig]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfigApiKeyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginInstanceAuthConfigApiKeyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c537e4648e5cd7d223a1d7bf9a56ee3fff5271ee697d8b87b4ebc62e70dc93e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig",
    jsii_struct_bases=[],
    name_mapping={"service_account": "serviceAccount"},
)
class ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig:
    def __init__(self, *, service_account: builtins.str) -> None:
        '''
        :param service_account: The service account to be used for authenticating request. The 'iam.serviceAccounts.getAccessToken' permission should be granted on this service account to the impersonator service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#service_account ApihubPluginInstance#service_account}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966d5fc8e6ef2ec9f8f583a3a1e31266f4a4be30980f252cb7e38b1fc4589d0b)
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account": service_account,
        }

    @builtins.property
    def service_account(self) -> builtins.str:
        '''The service account to be used for authenticating request.

        The 'iam.serviceAccounts.getAccessToken' permission should be granted on
        this service account to the impersonator service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#service_account ApihubPluginInstance#service_account}
        '''
        result = self._values.get("service_account")
        assert result is not None, "Required property 'service_account' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginInstanceAuthConfigGoogleServiceAccountConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigGoogleServiceAccountConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b40cf2dd7612c153360f692901d3aaff088d50af7c50397b96a3c627c613fe41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b18949306934e35c7d06e98bc706b7ac7a58ec4529dfc8ac54e4bf8ad77eaff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce869320e3e263b26d07269e00efaba2aa8f4a0d21c7b602ae9031304c39099b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
)
class ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Union["ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param client_id: The client identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#client_id ApihubPluginInstance#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#client_secret ApihubPluginInstance#client_secret}
        '''
        if isinstance(client_secret, dict):
            client_secret = ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret(**client_secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14299cda7a54f6c2b4e13325965f73bb373187aaac72f7f22767531ca153ee20)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The client identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#client_id ApihubPluginInstance#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(
        self,
    ) -> "ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret":
        '''client_secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#client_secret ApihubPluginInstance#client_secret}
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast("ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#secret_version ApihubPluginInstance#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5601e56a966ce40704966e5100547b886a51ec052f87087edcc06a4d02380eb1)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#secret_version ApihubPluginInstance#secret_version}

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
        return "ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d7636bc818ae724bde41daf2789a694f22a7fb83c2c6a54d434731958e2efec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e1306b269e28e417317699bebcc56e3025f82b7ccc053ac7ccf093e371cac18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21913eaaed0ff9c26ebbf9bd61562b73d543388836870e8fc8527f2cd5e76e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0fe19f29d80b3bc216c7bde83e3efbae239d224b268e4f6b2639ff3550b4d25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientSecret")
    def put_client_secret(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#secret_version ApihubPluginInstance#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putClientSecret", [value]))

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(
        self,
    ) -> ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecretOutputReference:
        return typing.cast(ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecretOutputReference, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(
        self,
    ) -> typing.Optional[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2cd1e7352692041d1b81420852161202d4e8c36c9ccd658dceb07646b7d0172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4bed6be98374203f1380bafefa45b2dc0a29f71ab2f4cd5a35663ab3c48ae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginInstanceAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ee3707ab68b6ebe3c244e45f4d8e24afacb43c63d52c668ea459fd483e4cf11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApiKeyConfig")
    def put_api_key_config(
        self,
        *,
        api_key: typing.Union[ApihubPluginInstanceAuthConfigApiKeyConfigApiKey, typing.Dict[builtins.str, typing.Any]],
        http_element_location: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param api_key: api_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#api_key ApihubPluginInstance#api_key}
        :param http_element_location: The location of the API key. The default value is QUERY. Possible values: HTTP_ELEMENT_LOCATION_UNSPECIFIED QUERY HEADER PATH BODY COOKIE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#http_element_location ApihubPluginInstance#http_element_location}
        :param name: The parameter name of the API key. E.g. If the API request is "https://example.com/act?api_key=", "api_key" would be the parameter name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#name ApihubPluginInstance#name}
        '''
        value = ApihubPluginInstanceAuthConfigApiKeyConfig(
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
        :param service_account: The service account to be used for authenticating request. The 'iam.serviceAccounts.getAccessToken' permission should be granted on this service account to the impersonator service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#service_account ApihubPluginInstance#service_account}
        '''
        value = ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig(
            service_account=service_account
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleServiceAccountConfig", [value]))

    @jsii.member(jsii_name="putOauth2ClientCredentialsConfig")
    def put_oauth2_client_credentials_config(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Union[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param client_id: The client identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#client_id ApihubPluginInstance#client_id}
        :param client_secret: client_secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#client_secret ApihubPluginInstance#client_secret}
        '''
        value = ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig(
            client_id=client_id, client_secret=client_secret
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2ClientCredentialsConfig", [value]))

    @jsii.member(jsii_name="putUserPasswordConfig")
    def put_user_password_config(
        self,
        *,
        password: typing.Union["ApihubPluginInstanceAuthConfigUserPasswordConfigPassword", typing.Dict[builtins.str, typing.Any]],
        username: builtins.str,
    ) -> None:
        '''
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#password ApihubPluginInstance#password}
        :param username: Username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#username ApihubPluginInstance#username}
        '''
        value = ApihubPluginInstanceAuthConfigUserPasswordConfig(
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
    ) -> ApihubPluginInstanceAuthConfigApiKeyConfigOutputReference:
        return typing.cast(ApihubPluginInstanceAuthConfigApiKeyConfigOutputReference, jsii.get(self, "apiKeyConfig"))

    @builtins.property
    @jsii.member(jsii_name="googleServiceAccountConfig")
    def google_service_account_config(
        self,
    ) -> ApihubPluginInstanceAuthConfigGoogleServiceAccountConfigOutputReference:
        return typing.cast(ApihubPluginInstanceAuthConfigGoogleServiceAccountConfigOutputReference, jsii.get(self, "googleServiceAccountConfig"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentialsConfig")
    def oauth2_client_credentials_config(
        self,
    ) -> ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigOutputReference:
        return typing.cast(ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigOutputReference, jsii.get(self, "oauth2ClientCredentialsConfig"))

    @builtins.property
    @jsii.member(jsii_name="userPasswordConfig")
    def user_password_config(
        self,
    ) -> "ApihubPluginInstanceAuthConfigUserPasswordConfigOutputReference":
        return typing.cast("ApihubPluginInstanceAuthConfigUserPasswordConfigOutputReference", jsii.get(self, "userPasswordConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyConfigInput")
    def api_key_config_input(
        self,
    ) -> typing.Optional[ApihubPluginInstanceAuthConfigApiKeyConfig]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfigApiKeyConfig], jsii.get(self, "apiKeyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="authTypeInput")
    def auth_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="googleServiceAccountConfigInput")
    def google_service_account_config_input(
        self,
    ) -> typing.Optional[ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig], jsii.get(self, "googleServiceAccountConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2ClientCredentialsConfigInput")
    def oauth2_client_credentials_config_input(
        self,
    ) -> typing.Optional[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig], jsii.get(self, "oauth2ClientCredentialsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="userPasswordConfigInput")
    def user_password_config_input(
        self,
    ) -> typing.Optional["ApihubPluginInstanceAuthConfigUserPasswordConfig"]:
        return typing.cast(typing.Optional["ApihubPluginInstanceAuthConfigUserPasswordConfig"], jsii.get(self, "userPasswordConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf4973cc26519966820a984e34deab63213c3146e648b2a391be0b5665bcbf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApihubPluginInstanceAuthConfig]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginInstanceAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff06382c41dcfd1d60854f398086c78186b3efb458957b6332fc96061a34e590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigUserPasswordConfig",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class ApihubPluginInstanceAuthConfigUserPasswordConfig:
    def __init__(
        self,
        *,
        password: typing.Union["ApihubPluginInstanceAuthConfigUserPasswordConfigPassword", typing.Dict[builtins.str, typing.Any]],
        username: builtins.str,
    ) -> None:
        '''
        :param password: password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#password ApihubPluginInstance#password}
        :param username: Username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#username ApihubPluginInstance#username}
        '''
        if isinstance(password, dict):
            password = ApihubPluginInstanceAuthConfigUserPasswordConfigPassword(**password)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dabfc017fbdac50154d7b4b42866b81583be65b7d76c0ad7f9e55f8842f534f)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> "ApihubPluginInstanceAuthConfigUserPasswordConfigPassword":
        '''password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#password ApihubPluginInstance#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast("ApihubPluginInstanceAuthConfigUserPasswordConfigPassword", result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#username ApihubPluginInstance#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginInstanceAuthConfigUserPasswordConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginInstanceAuthConfigUserPasswordConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigUserPasswordConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9313fd073e5f87a6268d0c3f388a85bc5cae4979e990fcb9a0e95da929c42f58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPassword")
    def put_password(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#secret_version ApihubPluginInstance#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = ApihubPluginInstanceAuthConfigUserPasswordConfigPassword(
            secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putPassword", [value]))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(
        self,
    ) -> "ApihubPluginInstanceAuthConfigUserPasswordConfigPasswordOutputReference":
        return typing.cast("ApihubPluginInstanceAuthConfigUserPasswordConfigPasswordOutputReference", jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(
        self,
    ) -> typing.Optional["ApihubPluginInstanceAuthConfigUserPasswordConfigPassword"]:
        return typing.cast(typing.Optional["ApihubPluginInstanceAuthConfigUserPasswordConfigPassword"], jsii.get(self, "passwordInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e5a4a4d651d26d445de478aa656ed3d9d824e9903c866051601cde938c1656c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApihubPluginInstanceAuthConfigUserPasswordConfig]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfigUserPasswordConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginInstanceAuthConfigUserPasswordConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f67061f5bff1551cee3860585d99def3bcf387fdc3bb9949500e82f0366cd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigUserPasswordConfigPassword",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class ApihubPluginInstanceAuthConfigUserPasswordConfigPassword:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#secret_version ApihubPluginInstance#secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a256daf9402166cb12d295e1b7714e56285f212e9fd96ccc0ca863bc3dbd0d35)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The resource name of the secret version in the format, format as: 'projects/* /secrets/* /versions/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#secret_version ApihubPluginInstance#secret_version}

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
        return "ApihubPluginInstanceAuthConfigUserPasswordConfigPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginInstanceAuthConfigUserPasswordConfigPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceAuthConfigUserPasswordConfigPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b607a6d92c9ba7a9a1e41f4074dd343f6b488c79c900cd317d77ecbe83e23f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c75e76e87a781ff2fb9054837ab50ff4ef305254130e185ec761b275cfcb41c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApihubPluginInstanceAuthConfigUserPasswordConfigPassword]:
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfigUserPasswordConfigPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginInstanceAuthConfigUserPasswordConfigPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__923f0b68fc573bff967ffc07dcd9a9791af6887521ed94b1b7d218c3db6f00d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceConfig",
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
class ApihubPluginInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginInstanceActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_config: typing.Optional[typing.Union[ApihubPluginInstanceAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApihubPluginInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The display name for this plugin instance. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#display_name ApihubPluginInstance#display_name}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#location ApihubPluginInstance#location}
        :param plugin: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#plugin ApihubPluginInstance#plugin}
        :param plugin_instance_id: The ID to use for the plugin instance, which will become the final component of the plugin instance's resource name. This field is optional. - If provided, the same will be used. The service will throw an error if the specified id is already used by another plugin instance in the plugin resource. - If not provided, a system generated id will be used. This value should be 4-63 characters, and valid characters are /a-z[0-9]-_/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#plugin_instance_id ApihubPluginInstance#plugin_instance_id}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#actions ApihubPluginInstance#actions}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#auth_config ApihubPluginInstance#auth_config}
        :param disable: The display name for this plugin instance. Max length is 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#disable ApihubPluginInstance#disable}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#id ApihubPluginInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#project ApihubPluginInstance#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#timeouts ApihubPluginInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auth_config, dict):
            auth_config = ApihubPluginInstanceAuthConfig(**auth_config)
        if isinstance(timeouts, dict):
            timeouts = ApihubPluginInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d1155d3c2b24c736b837f77df32758374b2a911f8f593ab50f55cb414a347f9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#display_name ApihubPluginInstance#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#location ApihubPluginInstance#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plugin(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#plugin ApihubPluginInstance#plugin}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#plugin_instance_id ApihubPluginInstance#plugin_instance_id}
        '''
        result = self._values.get("plugin_instance_id")
        assert result is not None, "Required property 'plugin_instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginInstanceActions]]]:
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#actions ApihubPluginInstance#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginInstanceActions]]], result)

    @builtins.property
    def auth_config(self) -> typing.Optional[ApihubPluginInstanceAuthConfig]:
        '''auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#auth_config ApihubPluginInstance#auth_config}
        '''
        result = self._values.get("auth_config")
        return typing.cast(typing.Optional[ApihubPluginInstanceAuthConfig], result)

    @builtins.property
    def disable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The display name for this plugin instance. Max length is 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#disable ApihubPluginInstance#disable}
        '''
        result = self._values.get("disable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#id ApihubPluginInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#project ApihubPluginInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApihubPluginInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#timeouts ApihubPluginInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApihubPluginInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ApihubPluginInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#create ApihubPluginInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#delete ApihubPluginInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#update ApihubPluginInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9256d4cb6beaddf90c5952bb1d990da3249a72e592a67c8d3b26e1e396a83e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#create ApihubPluginInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#delete ApihubPluginInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin_instance#update ApihubPluginInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPluginInstance.ApihubPluginInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fabe7977eee0054b92cbf84e242b31368e437db12228e9147b4a191876d63610)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ecd51d5d2fc96ba76af9ecc6223a0ec2b2d5ef6c8557bb1609023e27a46954e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e527742550a4806864507044f1b90e0e87bb04157bb9ce3cb660787fcdf1e6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c05ec8f9137c40b07fe4d6901075cb52dc07f2b2af8e0282f54eed3aa3b1a88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc7aa883b99a5099d19c220c41a450f630ccde35831f9c0e1502fce15d5c23bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApihubPluginInstance",
    "ApihubPluginInstanceActions",
    "ApihubPluginInstanceActionsCurationConfig",
    "ApihubPluginInstanceActionsCurationConfigCustomCuration",
    "ApihubPluginInstanceActionsCurationConfigCustomCurationOutputReference",
    "ApihubPluginInstanceActionsCurationConfigOutputReference",
    "ApihubPluginInstanceActionsHubInstanceAction",
    "ApihubPluginInstanceActionsHubInstanceActionLastExecution",
    "ApihubPluginInstanceActionsHubInstanceActionLastExecutionList",
    "ApihubPluginInstanceActionsHubInstanceActionLastExecutionOutputReference",
    "ApihubPluginInstanceActionsHubInstanceActionList",
    "ApihubPluginInstanceActionsHubInstanceActionOutputReference",
    "ApihubPluginInstanceActionsList",
    "ApihubPluginInstanceActionsOutputReference",
    "ApihubPluginInstanceAuthConfig",
    "ApihubPluginInstanceAuthConfigApiKeyConfig",
    "ApihubPluginInstanceAuthConfigApiKeyConfigApiKey",
    "ApihubPluginInstanceAuthConfigApiKeyConfigApiKeyOutputReference",
    "ApihubPluginInstanceAuthConfigApiKeyConfigOutputReference",
    "ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig",
    "ApihubPluginInstanceAuthConfigGoogleServiceAccountConfigOutputReference",
    "ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig",
    "ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret",
    "ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecretOutputReference",
    "ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigOutputReference",
    "ApihubPluginInstanceAuthConfigOutputReference",
    "ApihubPluginInstanceAuthConfigUserPasswordConfig",
    "ApihubPluginInstanceAuthConfigUserPasswordConfigOutputReference",
    "ApihubPluginInstanceAuthConfigUserPasswordConfigPassword",
    "ApihubPluginInstanceAuthConfigUserPasswordConfigPasswordOutputReference",
    "ApihubPluginInstanceConfig",
    "ApihubPluginInstanceTimeouts",
    "ApihubPluginInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__593afa281ec915f6d51a38f60fdae46dc24eadaf232f1416928ef39d4df1faf4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    plugin: builtins.str,
    plugin_instance_id: builtins.str,
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginInstanceActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_config: typing.Optional[typing.Union[ApihubPluginInstanceAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApihubPluginInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3711db439d7c9dbe0aa0eeaaefa7602bec6eb28f91da4903b94a5d02556adf53(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636835dea3273121f1b309fa9ac4c238b086aa90f541d553e6b761049fee2e25(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginInstanceActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13087f4d259707f8dc327cff69435cc31b992ea982859208c5a8dafd6bcb54da(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334f32397f5dbd0bd37e370d38b2dce15f78a88e07a8c708de0280e050a4d41a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0ff77d3bc5c421645f727dc7588d5fa1f6f055bb3590336c9acdede2279d6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7018023aff3fd644286be0a39f5a9f04df609c7b82eaeefedfa5fc906e0fe995(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbe855dec0857c0a8c4ca37a47ba084d98551e7ebd62e8ea023f9fedaa2a18e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5785d41444f0491f36baeeeb610579c2100094ea80f425298a5fa8de098563b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96235b74515d777cf5462339439c6217f55f64e595b3f7c2ed9a00a21f41b749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddff3dca95db95d9d0baae4a5c878e9828155764fdcec36c99fa629a9e0238bb(
    *,
    action_id: builtins.str,
    curation_config: typing.Optional[typing.Union[ApihubPluginInstanceActionsCurationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule_cron_expression: typing.Optional[builtins.str] = None,
    schedule_time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f3cc12ff83e499d7209101b7131b4626668b115bf66895a270d1f09b84be62(
    *,
    curation_type: typing.Optional[builtins.str] = None,
    custom_curation: typing.Optional[typing.Union[ApihubPluginInstanceActionsCurationConfigCustomCuration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5c5030af187fd168f80e1edeadef260e2994bd4da45a967494191c6c63e940(
    *,
    curation: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4809c0d547b2d1eac6bfadc27b17d47a77900e48fbdca916cdde15a486a308e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150cc910ee6e265f80ed9e72db093c6c4779db25d55b1dd494e4e11102bd9472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe151377cb631c57087bbf21f88c9ae74cc0ffa4aab2ff44021d83f2dd23a76(
    value: typing.Optional[ApihubPluginInstanceActionsCurationConfigCustomCuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97149738bb214f9a3a5e97548963be17701c05a5a2a589cef02b95047696ea9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080d6e3f35f91214b7974581d58df2d77719582232067e4695229b05498c53bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51128e69582893b34d93e9daa4fd84a5a4040456481e4c7a68c5e21c26ff6396(
    value: typing.Optional[ApihubPluginInstanceActionsCurationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64047b760d14fd381bdb26c928321eb1a61be6a1a211810bea286f878699641a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ad1130a251ce00da529acc295d07f974f42c885a968744fdb07ea38f5396ea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f42129170d95975656f2c40d613d36d39dda46df30d57b3af82cc90a473012(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6641860af9fb7693eeb2aae92f33eaa2471cb3615bb46ec1b19702279b81b60b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8edc465d7bbdb8eb822407d8e418e388664b3cf792c2cb41bfaf31f54419862(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3b753d49ec26ac94414132d8b8a58c634771c521ed1098f1df987ed1e6ae8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a349e1b0469c02a45802517a81fc3e44f536bb08210b2151b5dfae1b7bb854(
    value: typing.Optional[ApihubPluginInstanceActionsHubInstanceActionLastExecution],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791fd07539fe34a270eb3e7e47e82f70dfc909dd3ddb2866675929eed5b97b9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f13399dc1513332fc2f3a5087509d2baf3ba5e702f7a5449964cf29e05b37f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6647b75d21405aa7279dea72783f2207cea39b99f4615fb80cfa9b9ff9b40d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691ad99e3c2c5a605a04be4fae097ec4d9faca0f7756954dfd7fde155282b09c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13e9c7a7396d41124367d8c2695fb1b19f16499389a8436efae112714efe8c8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c09a1bb95353ba274b901359cf28257fe6f690ec20f7383668ba0d0ad94870f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd8f20704c3b80c30626bcf8c96038be6cc0ab02a49bcac783df4c4d5e1af2f(
    value: typing.Optional[ApihubPluginInstanceActionsHubInstanceAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd6967c2a39a9d2ba04e2aaea0544120a5b8888601db13c20b254883a7b3a34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f4e4ed51b4524c08fe2ec0123de6852b95c01da5ee2435130047a16ce49610(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935b18385d9aa2b33bc55a27d5d9193cc2b7679276b0b1c46bcdf56b8752a1ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d930bec602ca2ba5d58faefda8ede58148db7661c9ac3d73fe2e2e8eba50e38f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa577202af274f3846442505635ce0ebed2252794a350657a0c5b4b51f1e1c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b06d2d5720bc3675ac40add588d20cb181870fb647b3608ba1b97f1dd97fb02(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginInstanceActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04cedc9b868dc947675cb026091a200b46201bf9c48fc616b327558a1341fbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ec17c36b2c79fd9449cfc58134d44544f16c3192d7434aa02846de4c9eb9f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2cc4779fe05da1a8ce27cf7a85abbdaa02138b11c65a7ff2cd2b173913bb672(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ca461056b0ee62bb2ee2d2f23808642665e22acf9e28fbbdeec600498ded59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abba25ca071676e206e8007eaedc7e2cb109f24a05f2a0b98622e43b23eec097(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginInstanceActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fff044d591e14057e937df1ef7b306057bb8742be9b0e9f3db684615c7f18c(
    *,
    auth_type: builtins.str,
    api_key_config: typing.Optional[typing.Union[ApihubPluginInstanceAuthConfigApiKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    google_service_account_config: typing.Optional[typing.Union[ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2_client_credentials_config: typing.Optional[typing.Union[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    user_password_config: typing.Optional[typing.Union[ApihubPluginInstanceAuthConfigUserPasswordConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17619b45d823301a07f5221a14e82bdd0321fffb402212355d356376c03b686(
    *,
    api_key: typing.Union[ApihubPluginInstanceAuthConfigApiKeyConfigApiKey, typing.Dict[builtins.str, typing.Any]],
    http_element_location: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d663937ba17add16c2639d240343f00cb4647ef2e97beeff5768d58b456396(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9627defe7a18500d973fe408f5606a4c38a86a0073fc4aae3b8d566c0d315b8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521d36737db806619f963f4b8fc8973c700111ef4b6f8758ba5e41201e157ee3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813d43b990b6702c722a081ae66c239b536db87e5fd7c95c2de2df8f1a18e2f1(
    value: typing.Optional[ApihubPluginInstanceAuthConfigApiKeyConfigApiKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78d4a7e460c9572d7406f45370194bf969dc903c9cf32724447f0ab1c927507(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1a0d4e05f929cd1186dd83707986765d30a9f52130b04b96e023006ffc1546(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0bf985b76d2ed793be63a1a40518d38ebd93d1e7df5a17d5f707ad99e55d55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c537e4648e5cd7d223a1d7bf9a56ee3fff5271ee697d8b87b4ebc62e70dc93e(
    value: typing.Optional[ApihubPluginInstanceAuthConfigApiKeyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966d5fc8e6ef2ec9f8f583a3a1e31266f4a4be30980f252cb7e38b1fc4589d0b(
    *,
    service_account: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40cf2dd7612c153360f692901d3aaff088d50af7c50397b96a3c627c613fe41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18949306934e35c7d06e98bc706b7ac7a58ec4529dfc8ac54e4bf8ad77eaff7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce869320e3e263b26d07269e00efaba2aa8f4a0d21c7b602ae9031304c39099b(
    value: typing.Optional[ApihubPluginInstanceAuthConfigGoogleServiceAccountConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14299cda7a54f6c2b4e13325965f73bb373187aaac72f7f22767531ca153ee20(
    *,
    client_id: builtins.str,
    client_secret: typing.Union[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5601e56a966ce40704966e5100547b886a51ec052f87087edcc06a4d02380eb1(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7636bc818ae724bde41daf2789a694f22a7fb83c2c6a54d434731958e2efec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1306b269e28e417317699bebcc56e3025f82b7ccc053ac7ccf093e371cac18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21913eaaed0ff9c26ebbf9bd61562b73d543388836870e8fc8527f2cd5e76e0(
    value: typing.Optional[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfigClientSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fe19f29d80b3bc216c7bde83e3efbae239d224b268e4f6b2639ff3550b4d25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2cd1e7352692041d1b81420852161202d4e8c36c9ccd658dceb07646b7d0172(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4bed6be98374203f1380bafefa45b2dc0a29f71ab2f4cd5a35663ab3c48ae7(
    value: typing.Optional[ApihubPluginInstanceAuthConfigOauth2ClientCredentialsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee3707ab68b6ebe3c244e45f4d8e24afacb43c63d52c668ea459fd483e4cf11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf4973cc26519966820a984e34deab63213c3146e648b2a391be0b5665bcbf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff06382c41dcfd1d60854f398086c78186b3efb458957b6332fc96061a34e590(
    value: typing.Optional[ApihubPluginInstanceAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dabfc017fbdac50154d7b4b42866b81583be65b7d76c0ad7f9e55f8842f534f(
    *,
    password: typing.Union[ApihubPluginInstanceAuthConfigUserPasswordConfigPassword, typing.Dict[builtins.str, typing.Any]],
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9313fd073e5f87a6268d0c3f388a85bc5cae4979e990fcb9a0e95da929c42f58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a4a4d651d26d445de478aa656ed3d9d824e9903c866051601cde938c1656c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f67061f5bff1551cee3860585d99def3bcf387fdc3bb9949500e82f0366cd2(
    value: typing.Optional[ApihubPluginInstanceAuthConfigUserPasswordConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a256daf9402166cb12d295e1b7714e56285f212e9fd96ccc0ca863bc3dbd0d35(
    *,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b607a6d92c9ba7a9a1e41f4074dd343f6b488c79c900cd317d77ecbe83e23f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75e76e87a781ff2fb9054837ab50ff4ef305254130e185ec761b275cfcb41c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__923f0b68fc573bff967ffc07dcd9a9791af6887521ed94b1b7d218c3db6f00d1(
    value: typing.Optional[ApihubPluginInstanceAuthConfigUserPasswordConfigPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d1155d3c2b24c736b837f77df32758374b2a911f8f593ab50f55cb414a347f9(
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
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginInstanceActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_config: typing.Optional[typing.Union[ApihubPluginInstanceAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApihubPluginInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9256d4cb6beaddf90c5952bb1d990da3249a72e592a67c8d3b26e1e396a83e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabe7977eee0054b92cbf84e242b31368e437db12228e9147b4a191876d63610(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ecd51d5d2fc96ba76af9ecc6223a0ec2b2d5ef6c8557bb1609023e27a46954e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e527742550a4806864507044f1b90e0e87bb04157bb9ce3cb660787fcdf1e6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c05ec8f9137c40b07fe4d6901075cb52dc07f2b2af8e0282f54eed3aa3b1a88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7aa883b99a5099d19c220c41a450f630ccde35831f9c0e1502fce15d5c23bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
