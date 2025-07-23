r'''
# `google_apihub_plugin`

Refer to the Terraform Registry for docs: [`google_apihub_plugin`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin).
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


class ApihubPlugin(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPlugin",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin google_apihub_plugin}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        plugin_id: builtins.str,
        actions_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApihubPluginActionsConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_template: typing.Optional[typing.Union["ApihubPluginConfigTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[typing.Union["ApihubPluginDocumentation", typing.Dict[builtins.str, typing.Any]]] = None,
        hosting_service: typing.Optional[typing.Union["ApihubPluginHostingService", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        plugin_category: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApihubPluginTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin google_apihub_plugin} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The display name of the plugin. Max length is 50 characters (Unicode code points). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#display_name ApihubPlugin#display_name}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#location ApihubPlugin#location}
        :param plugin_id: The ID to use for the Plugin resource, which will become the final component of the Plugin's resource name. This field is optional. - If provided, the same will be used. The service will throw an error if the specified id is already used by another Plugin resource in the API hub instance. - If not provided, a system generated id will be used. This value should be 4-63 characters, overall resource name which will be of format 'projects/{project}/locations/{location}/plugins/{plugin}', its length is limited to 1000 characters and valid characters are /a-z[0-9]-_/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#plugin_id ApihubPlugin#plugin_id}
        :param actions_config: actions_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#actions_config ApihubPlugin#actions_config}
        :param config_template: config_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#config_template ApihubPlugin#config_template}
        :param description: The plugin description. Max length is 2000 characters (Unicode code points). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#description ApihubPlugin#description}
        :param documentation: documentation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#documentation ApihubPlugin#documentation}
        :param hosting_service: hosting_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#hosting_service ApihubPlugin#hosting_service}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#id ApihubPlugin#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param plugin_category: Possible values: PLUGIN_CATEGORY_UNSPECIFIED API_GATEWAY API_PRODUCER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#plugin_category ApihubPlugin#plugin_category}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#project ApihubPlugin#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#timeouts ApihubPlugin#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6c1e1e2735681c89af7278d4cba91da36db227c450af0955c5e1208d1f6e8e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApihubPluginConfig(
            display_name=display_name,
            location=location,
            plugin_id=plugin_id,
            actions_config=actions_config,
            config_template=config_template,
            description=description,
            documentation=documentation,
            hosting_service=hosting_service,
            id=id,
            plugin_category=plugin_category,
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
        '''Generates CDKTF code for importing a ApihubPlugin resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApihubPlugin to import.
        :param import_from_id: The id of the existing ApihubPlugin that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApihubPlugin to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154f015722919b59cb301a491eb9525c117ae61291240fb850f3c26f73f112bf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActionsConfig")
    def put_actions_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApihubPluginActionsConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30cc69e1c2fc04e4197e81081612b09e25b83dee00ac34bda9c390fd2767bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActionsConfig", [value]))

    @jsii.member(jsii_name="putConfigTemplate")
    def put_config_template(
        self,
        *,
        additional_config_template: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApihubPluginConfigTemplateAdditionalConfigTemplate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_config_template: typing.Optional[typing.Union["ApihubPluginConfigTemplateAuthConfigTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param additional_config_template: additional_config_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#additional_config_template ApihubPlugin#additional_config_template}
        :param auth_config_template: auth_config_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#auth_config_template ApihubPlugin#auth_config_template}
        '''
        value = ApihubPluginConfigTemplate(
            additional_config_template=additional_config_template,
            auth_config_template=auth_config_template,
        )

        return typing.cast(None, jsii.invoke(self, "putConfigTemplate", [value]))

    @jsii.member(jsii_name="putDocumentation")
    def put_documentation(
        self,
        *,
        external_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param external_uri: The uri of the externally hosted documentation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#external_uri ApihubPlugin#external_uri}
        '''
        value = ApihubPluginDocumentation(external_uri=external_uri)

        return typing.cast(None, jsii.invoke(self, "putDocumentation", [value]))

    @jsii.member(jsii_name="putHostingService")
    def put_hosting_service(
        self,
        *,
        service_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_uri: The URI of the service implemented by the plugin developer, used to invoke the plugin's functionality. This information is only required for user defined plugins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#service_uri ApihubPlugin#service_uri}
        '''
        value = ApihubPluginHostingService(service_uri=service_uri)

        return typing.cast(None, jsii.invoke(self, "putHostingService", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#create ApihubPlugin#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#delete ApihubPlugin#delete}.
        '''
        value = ApihubPluginTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetActionsConfig")
    def reset_actions_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionsConfig", []))

    @jsii.member(jsii_name="resetConfigTemplate")
    def reset_config_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigTemplate", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDocumentation")
    def reset_documentation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentation", []))

    @jsii.member(jsii_name="resetHostingService")
    def reset_hosting_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostingService", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPluginCategory")
    def reset_plugin_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginCategory", []))

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
    @jsii.member(jsii_name="actionsConfig")
    def actions_config(self) -> "ApihubPluginActionsConfigList":
        return typing.cast("ApihubPluginActionsConfigList", jsii.get(self, "actionsConfig"))

    @builtins.property
    @jsii.member(jsii_name="configTemplate")
    def config_template(self) -> "ApihubPluginConfigTemplateOutputReference":
        return typing.cast("ApihubPluginConfigTemplateOutputReference", jsii.get(self, "configTemplate"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="documentation")
    def documentation(self) -> "ApihubPluginDocumentationOutputReference":
        return typing.cast("ApihubPluginDocumentationOutputReference", jsii.get(self, "documentation"))

    @builtins.property
    @jsii.member(jsii_name="hostingService")
    def hosting_service(self) -> "ApihubPluginHostingServiceOutputReference":
        return typing.cast("ApihubPluginHostingServiceOutputReference", jsii.get(self, "hostingService"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="ownershipType")
    def ownership_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownershipType"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApihubPluginTimeoutsOutputReference":
        return typing.cast("ApihubPluginTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="actionsConfigInput")
    def actions_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApihubPluginActionsConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApihubPluginActionsConfig"]]], jsii.get(self, "actionsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="configTemplateInput")
    def config_template_input(self) -> typing.Optional["ApihubPluginConfigTemplate"]:
        return typing.cast(typing.Optional["ApihubPluginConfigTemplate"], jsii.get(self, "configTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="documentationInput")
    def documentation_input(self) -> typing.Optional["ApihubPluginDocumentation"]:
        return typing.cast(typing.Optional["ApihubPluginDocumentation"], jsii.get(self, "documentationInput"))

    @builtins.property
    @jsii.member(jsii_name="hostingServiceInput")
    def hosting_service_input(self) -> typing.Optional["ApihubPluginHostingService"]:
        return typing.cast(typing.Optional["ApihubPluginHostingService"], jsii.get(self, "hostingServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginCategoryInput")
    def plugin_category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginCategoryInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginIdInput")
    def plugin_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApihubPluginTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApihubPluginTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f73f97fb46b61de1c27e57f1b22d0b60db887a5c45e185404a0d579bb0d51e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583a468729bcaad29d967c790bae0982f60fe17a1b08e5658c8e2b86d867510a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876c3cca0bd761fe61b029cab62c1cc82a7072623261630c74f043281a07ebab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20606d41291d1755420305f9ea5262988fa08a58c412a7be0991856d26e75c8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginCategory")
    def plugin_category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginCategory"))

    @plugin_category.setter
    def plugin_category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d4adc996fa34674258eda5d6b38c78788f95b7ef4b420bd8f74f9de393f2e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginCategory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginId")
    def plugin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginId"))

    @plugin_id.setter
    def plugin_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__462f1124a443552ec18cc849f09923f162bb5b3756448b75272742463557219c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6bf2d4d717859b740610c89b3265b35d1f5ee8a2defedc63cae09831affea09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginActionsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "trigger_mode": "triggerMode",
    },
)
class ApihubPluginActionsConfig:
    def __init__(
        self,
        *,
        description: builtins.str,
        display_name: builtins.str,
        id: builtins.str,
        trigger_mode: builtins.str,
    ) -> None:
        '''
        :param description: The description of the operation performed by the action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#description ApihubPlugin#description}
        :param display_name: The display name of the action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#display_name ApihubPlugin#display_name}
        :param id: The id of the action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#id ApihubPlugin#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param trigger_mode: The trigger mode supported by the action. Possible values: TRIGGER_MODE_UNSPECIFIED API_HUB_ON_DEMAND_TRIGGER API_HUB_SCHEDULE_TRIGGER NON_API_HUB_MANAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#trigger_mode ApihubPlugin#trigger_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee6e4673175caeb489a36ea014b36def0f0f757a4d596be7c6d5ffe4cbec695)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument trigger_mode", value=trigger_mode, expected_type=type_hints["trigger_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "display_name": display_name,
            "id": id,
            "trigger_mode": trigger_mode,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''The description of the operation performed by the action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#description ApihubPlugin#description}
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name of the action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#display_name ApihubPlugin#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The id of the action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#id ApihubPlugin#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_mode(self) -> builtins.str:
        '''The trigger mode supported by the action. Possible values: TRIGGER_MODE_UNSPECIFIED API_HUB_ON_DEMAND_TRIGGER API_HUB_SCHEDULE_TRIGGER NON_API_HUB_MANAGED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#trigger_mode ApihubPlugin#trigger_mode}
        '''
        result = self._values.get("trigger_mode")
        assert result is not None, "Required property 'trigger_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginActionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginActionsConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginActionsConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96576aaabace562099c8405073ad34d1043a6fe1dd924e870917752f59111716)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ApihubPluginActionsConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aff5708c6a50e0506323f98a28aafc6d7ea70cb0ca073845509bd47759c978a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApihubPluginActionsConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fcca01f75d5734f545dd34e78a59684a3ffc0d44ebd8af25996da3979741183)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71699f280e23a5a07b5206a859d74ebe07070f9d0c9d78e2b82554b8e82b287b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24e8bb94bb272d8cff44c9b7fc703f782ba8c52ac8bd95cfb379ed3a8b34366e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginActionsConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginActionsConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginActionsConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd83890986fd4f90a9d412854ef45d727e3c1f9c58ea7dd460611bae4fee61a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginActionsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginActionsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6074f44ab60b118264eda7b1c26427d631ad31cbf0b133dcb9e98e447f76db16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerModeInput")
    def trigger_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerModeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ed7f8aa4df159729946683f78ed390e026c2cc1abdaf8e62addeb5d19038f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ed14ec5158941a53d803e5e36a25b8092ab86435b934aaa10c911bc4c4e96c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9d7d6524bb25854f5c5c80f7827afaeb82737ed32506a834189acb18e94064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerMode")
    def trigger_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerMode"))

    @trigger_mode.setter
    def trigger_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3562d2cd1c9fbea28c321ca1591c15c6d393f30cf7ea79916915e40f2b9919a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginActionsConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginActionsConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginActionsConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__672998105ae43b731c256372e11916182f3ae53e366ae7d38b8d8d1a84639209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfig",
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
        "plugin_id": "pluginId",
        "actions_config": "actionsConfig",
        "config_template": "configTemplate",
        "description": "description",
        "documentation": "documentation",
        "hosting_service": "hostingService",
        "id": "id",
        "plugin_category": "pluginCategory",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class ApihubPluginConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        plugin_id: builtins.str,
        actions_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginActionsConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_template: typing.Optional[typing.Union["ApihubPluginConfigTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[typing.Union["ApihubPluginDocumentation", typing.Dict[builtins.str, typing.Any]]] = None,
        hosting_service: typing.Optional[typing.Union["ApihubPluginHostingService", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        plugin_category: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApihubPluginTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The display name of the plugin. Max length is 50 characters (Unicode code points). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#display_name ApihubPlugin#display_name}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#location ApihubPlugin#location}
        :param plugin_id: The ID to use for the Plugin resource, which will become the final component of the Plugin's resource name. This field is optional. - If provided, the same will be used. The service will throw an error if the specified id is already used by another Plugin resource in the API hub instance. - If not provided, a system generated id will be used. This value should be 4-63 characters, overall resource name which will be of format 'projects/{project}/locations/{location}/plugins/{plugin}', its length is limited to 1000 characters and valid characters are /a-z[0-9]-_/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#plugin_id ApihubPlugin#plugin_id}
        :param actions_config: actions_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#actions_config ApihubPlugin#actions_config}
        :param config_template: config_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#config_template ApihubPlugin#config_template}
        :param description: The plugin description. Max length is 2000 characters (Unicode code points). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#description ApihubPlugin#description}
        :param documentation: documentation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#documentation ApihubPlugin#documentation}
        :param hosting_service: hosting_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#hosting_service ApihubPlugin#hosting_service}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#id ApihubPlugin#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param plugin_category: Possible values: PLUGIN_CATEGORY_UNSPECIFIED API_GATEWAY API_PRODUCER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#plugin_category ApihubPlugin#plugin_category}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#project ApihubPlugin#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#timeouts ApihubPlugin#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config_template, dict):
            config_template = ApihubPluginConfigTemplate(**config_template)
        if isinstance(documentation, dict):
            documentation = ApihubPluginDocumentation(**documentation)
        if isinstance(hosting_service, dict):
            hosting_service = ApihubPluginHostingService(**hosting_service)
        if isinstance(timeouts, dict):
            timeouts = ApihubPluginTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62cf6d8dc9d675c6d1156e6d9d5e2a94151eb38ac14e00000058a94335c6b73)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument plugin_id", value=plugin_id, expected_type=type_hints["plugin_id"])
            check_type(argname="argument actions_config", value=actions_config, expected_type=type_hints["actions_config"])
            check_type(argname="argument config_template", value=config_template, expected_type=type_hints["config_template"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument documentation", value=documentation, expected_type=type_hints["documentation"])
            check_type(argname="argument hosting_service", value=hosting_service, expected_type=type_hints["hosting_service"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument plugin_category", value=plugin_category, expected_type=type_hints["plugin_category"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "location": location,
            "plugin_id": plugin_id,
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
        if actions_config is not None:
            self._values["actions_config"] = actions_config
        if config_template is not None:
            self._values["config_template"] = config_template
        if description is not None:
            self._values["description"] = description
        if documentation is not None:
            self._values["documentation"] = documentation
        if hosting_service is not None:
            self._values["hosting_service"] = hosting_service
        if id is not None:
            self._values["id"] = id
        if plugin_category is not None:
            self._values["plugin_category"] = plugin_category
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
        '''The display name of the plugin. Max length is 50 characters (Unicode code points).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#display_name ApihubPlugin#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#location ApihubPlugin#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plugin_id(self) -> builtins.str:
        '''The ID to use for the Plugin resource, which will become the final component of the Plugin's resource name.

        This field is optional.

        - If provided, the same will be used. The service will throw an error if
          the specified id is already used by another Plugin resource in the API hub
          instance.
        - If not provided, a system generated id will be used.

        This value should be 4-63 characters, overall resource name which will be
        of format
        'projects/{project}/locations/{location}/plugins/{plugin}',
        its length is limited to 1000 characters and valid characters are
        /a-z[0-9]-_/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#plugin_id ApihubPlugin#plugin_id}
        '''
        result = self._values.get("plugin_id")
        assert result is not None, "Required property 'plugin_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginActionsConfig]]]:
        '''actions_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#actions_config ApihubPlugin#actions_config}
        '''
        result = self._values.get("actions_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginActionsConfig]]], result)

    @builtins.property
    def config_template(self) -> typing.Optional["ApihubPluginConfigTemplate"]:
        '''config_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#config_template ApihubPlugin#config_template}
        '''
        result = self._values.get("config_template")
        return typing.cast(typing.Optional["ApihubPluginConfigTemplate"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The plugin description. Max length is 2000 characters (Unicode code points).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#description ApihubPlugin#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def documentation(self) -> typing.Optional["ApihubPluginDocumentation"]:
        '''documentation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#documentation ApihubPlugin#documentation}
        '''
        result = self._values.get("documentation")
        return typing.cast(typing.Optional["ApihubPluginDocumentation"], result)

    @builtins.property
    def hosting_service(self) -> typing.Optional["ApihubPluginHostingService"]:
        '''hosting_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#hosting_service ApihubPlugin#hosting_service}
        '''
        result = self._values.get("hosting_service")
        return typing.cast(typing.Optional["ApihubPluginHostingService"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#id ApihubPlugin#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_category(self) -> typing.Optional[builtins.str]:
        '''Possible values: PLUGIN_CATEGORY_UNSPECIFIED API_GATEWAY API_PRODUCER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#plugin_category ApihubPlugin#plugin_category}
        '''
        result = self._values.get("plugin_category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#project ApihubPlugin#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApihubPluginTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#timeouts ApihubPlugin#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApihubPluginTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "additional_config_template": "additionalConfigTemplate",
        "auth_config_template": "authConfigTemplate",
    },
)
class ApihubPluginConfigTemplate:
    def __init__(
        self,
        *,
        additional_config_template: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApihubPluginConfigTemplateAdditionalConfigTemplate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_config_template: typing.Optional[typing.Union["ApihubPluginConfigTemplateAuthConfigTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param additional_config_template: additional_config_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#additional_config_template ApihubPlugin#additional_config_template}
        :param auth_config_template: auth_config_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#auth_config_template ApihubPlugin#auth_config_template}
        '''
        if isinstance(auth_config_template, dict):
            auth_config_template = ApihubPluginConfigTemplateAuthConfigTemplate(**auth_config_template)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37a72efd9296128334333c292653ef22754be0704eca8220ae5ee1499f3f8d0)
            check_type(argname="argument additional_config_template", value=additional_config_template, expected_type=type_hints["additional_config_template"])
            check_type(argname="argument auth_config_template", value=auth_config_template, expected_type=type_hints["auth_config_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_config_template is not None:
            self._values["additional_config_template"] = additional_config_template
        if auth_config_template is not None:
            self._values["auth_config_template"] = auth_config_template

    @builtins.property
    def additional_config_template(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApihubPluginConfigTemplateAdditionalConfigTemplate"]]]:
        '''additional_config_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#additional_config_template ApihubPlugin#additional_config_template}
        '''
        result = self._values.get("additional_config_template")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApihubPluginConfigTemplateAdditionalConfigTemplate"]]], result)

    @builtins.property
    def auth_config_template(
        self,
    ) -> typing.Optional["ApihubPluginConfigTemplateAuthConfigTemplate"]:
        '''auth_config_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#auth_config_template ApihubPlugin#auth_config_template}
        '''
        result = self._values.get("auth_config_template")
        return typing.cast(typing.Optional["ApihubPluginConfigTemplateAuthConfigTemplate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginConfigTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAdditionalConfigTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "value_type": "valueType",
        "description": "description",
        "enum_options": "enumOptions",
        "multi_select_options": "multiSelectOptions",
        "required": "required",
        "validation_regex": "validationRegex",
    },
)
class ApihubPluginConfigTemplateAdditionalConfigTemplate:
    def __init__(
        self,
        *,
        id: builtins.str,
        value_type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enum_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        multi_select_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        validation_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: ID of the config variable. Must be unique within the configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#id ApihubPlugin#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param value_type: Type of the parameter: string, int, bool etc. Possible values: VALUE_TYPE_UNSPECIFIED STRING INT BOOL SECRET ENUM MULTI_SELECT MULTI_STRING MULTI_INT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#value_type ApihubPlugin#value_type}
        :param description: Description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#description ApihubPlugin#description}
        :param enum_options: enum_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#enum_options ApihubPlugin#enum_options}
        :param multi_select_options: multi_select_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#multi_select_options ApihubPlugin#multi_select_options}
        :param required: Flag represents that this 'ConfigVariable' must be provided for a PluginInstance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#required ApihubPlugin#required}
        :param validation_regex: Regular expression in RE2 syntax used for validating the 'value' of a 'ConfigVariable'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#validation_regex ApihubPlugin#validation_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a1cc17b7ddccf268a969fcf562a5a83b13e8776ed6115728ced3a80f2291fe8)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument value_type", value=value_type, expected_type=type_hints["value_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enum_options", value=enum_options, expected_type=type_hints["enum_options"])
            check_type(argname="argument multi_select_options", value=multi_select_options, expected_type=type_hints["multi_select_options"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument validation_regex", value=validation_regex, expected_type=type_hints["validation_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "value_type": value_type,
        }
        if description is not None:
            self._values["description"] = description
        if enum_options is not None:
            self._values["enum_options"] = enum_options
        if multi_select_options is not None:
            self._values["multi_select_options"] = multi_select_options
        if required is not None:
            self._values["required"] = required
        if validation_regex is not None:
            self._values["validation_regex"] = validation_regex

    @builtins.property
    def id(self) -> builtins.str:
        '''ID of the config variable. Must be unique within the configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#id ApihubPlugin#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value_type(self) -> builtins.str:
        '''Type of the parameter: string, int, bool etc. Possible values: VALUE_TYPE_UNSPECIFIED STRING INT BOOL SECRET ENUM MULTI_SELECT MULTI_STRING MULTI_INT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#value_type ApihubPlugin#value_type}
        '''
        result = self._values.get("value_type")
        assert result is not None, "Required property 'value_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#description ApihubPlugin#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enum_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions"]]]:
        '''enum_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#enum_options ApihubPlugin#enum_options}
        '''
        result = self._values.get("enum_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions"]]], result)

    @builtins.property
    def multi_select_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions"]]]:
        '''multi_select_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#multi_select_options ApihubPlugin#multi_select_options}
        '''
        result = self._values.get("multi_select_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions"]]], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag represents that this 'ConfigVariable' must be provided for a PluginInstance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#required ApihubPlugin#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def validation_regex(self) -> typing.Optional[builtins.str]:
        '''Regular expression in RE2 syntax used for validating the 'value' of a 'ConfigVariable'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#validation_regex ApihubPlugin#validation_regex}
        '''
        result = self._values.get("validation_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginConfigTemplateAdditionalConfigTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "id": "id",
        "description": "description",
    },
)
class ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        id: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Display name of the option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#display_name ApihubPlugin#display_name}
        :param id: Id of the option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#id ApihubPlugin#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param description: Description of the option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#description ApihubPlugin#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f680f8fc4291901f3bdb5615d6ee5ca9bf3884cb361eb0acbab86a20ae1a95b7)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "id": id,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Display name of the option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#display_name ApihubPlugin#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Id of the option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#id ApihubPlugin#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#description ApihubPlugin#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecbdb29118bd899c1050b9fd63b070c5e7c18de173303c0b581e91684759835a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99aa9c2bb9d383ae8df469ef1b4c8b2019f3c6abe1d758cca71a502d835dd83)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da7fb5dc08a6579e156a8b93048bd90a6bd57ebcaa2e487d0a527c3a8566677)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df7057e7e017796ca96513e78d1c7b7ac5605bb8438c6359fd4e63935b7e2d3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c28f7beb04ef9ce744af55eb897ca0be2f7dcf1d9ae08edc7e3c7f4bbf4ae89c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05fa2f66afb7a74f5c121ca374b3c310fd590da576605f7e8cb407775ad925d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cac062d58f46c79c4d84f34591b32b6a4f116e9ffd57017db81fa49a9547238)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__597aa1d57412507e7244c62c853769f47ecda24996c68c900109c4342b7a9e2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c497fd3d70ce8603701a3ecab409d439c3b36827c9c41f228584f75d1d4706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e31f23b4cac79114e7432c209cc7b88469279f78c805e276effd350a461ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d095d95acdb9a7c0154fc0b9b872d3ae926a91e20c4f0ab56a7d41d43ac489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginConfigTemplateAdditionalConfigTemplateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAdditionalConfigTemplateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa46c48807cb2e22a8a777709e1e2a7c0c6a35e3d64cd9ee7083706a48a03157)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApihubPluginConfigTemplateAdditionalConfigTemplateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab4efcb62582331f059a992a4c08d03ab37ba79d3ef728ad1b2c95f42e8be363)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApihubPluginConfigTemplateAdditionalConfigTemplateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006c9f6effc935c8d407ecc8f57684044f399082df0ecce1b6686355a3e09195)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce715e407e533290e77ccd455785a42f76320539331b48296bbd041b1d20d299)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db3136c47592d2738e763a997ec23faacd5a2bd9f52125a2d94cb059bbd4aa7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1bbfe37ca4ced38841b220c1e0232abb8a85a10f16d7a4a8fa712bea5730130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "id": "id",
        "description": "description",
    },
)
class ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        id: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Display name of the option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#display_name ApihubPlugin#display_name}
        :param id: Id of the option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#id ApihubPlugin#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param description: Description of the option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#description ApihubPlugin#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69bb3fa4ffd8b90422dc9dbb0571cd53333112da45922a8c342a662a12123739)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "id": id,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Display name of the option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#display_name ApihubPlugin#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Id of the option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#id ApihubPlugin#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#description ApihubPlugin#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f6723264df2d5ef894be01b46369f50f0e81266de8acf060f4c286cd69707dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f7895a9a1dd1ce2b52ef607755216b9f39e569c6ffe92d19bbd387818a6580)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a712de3ab84c82064387f8cfc8453669319e50ef97fbd3d926224e5e1f87f908)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aaf29204dc6d5a4b26fb85a2cc1a2dbcab04574b00da9973be68df827e4446e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ac4d4a3d167242df2d1b7d5aac375b302a20a83a0a35e7df87b52d1eb04c568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556b97637f3970f31b0db22a54d6c5a77096b727e4664e6ffadfc519fce02b0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24bb19b80a1e697630841c85ded0afff0a3e8f68800185e4cf973b2538ffafc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1ad847b8d7f601e53e2472f75fc895d06017e2bbfcc09b0deb7cece5a816ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1eefdd96580b7e04e973c5afc2d028687b20eafdf9cdc1f1f2521c0fc5371b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f939c014e67a1f8cb345f3d7c522f7c496f49794d2ce582f727c98fdf1f5319f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7093394141e38af62ef4d6b6da39faab610c7ac857fa43a47c543f3c4f276a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginConfigTemplateAdditionalConfigTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAdditionalConfigTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4771678be547a3103f42c349d787dac79df7690cc509f207c98ba10f3f8d897b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnumOptions")
    def put_enum_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06abc1264219d76254e2ebf56184150864e6a0b2dc25d988bdb537f50e27ebdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnumOptions", [value]))

    @jsii.member(jsii_name="putMultiSelectOptions")
    def put_multi_select_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7dcbc402ffc0ba8093995fde3778912193cf0f23154a4b7cb1709297f85babb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMultiSelectOptions", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnumOptions")
    def reset_enum_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnumOptions", []))

    @jsii.member(jsii_name="resetMultiSelectOptions")
    def reset_multi_select_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiSelectOptions", []))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @jsii.member(jsii_name="resetValidationRegex")
    def reset_validation_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidationRegex", []))

    @builtins.property
    @jsii.member(jsii_name="enumOptions")
    def enum_options(
        self,
    ) -> ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsList:
        return typing.cast(ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsList, jsii.get(self, "enumOptions"))

    @builtins.property
    @jsii.member(jsii_name="multiSelectOptions")
    def multi_select_options(
        self,
    ) -> ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsList:
        return typing.cast(ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsList, jsii.get(self, "multiSelectOptions"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enumOptionsInput")
    def enum_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]], jsii.get(self, "enumOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="multiSelectOptionsInput")
    def multi_select_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]], jsii.get(self, "multiSelectOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="validationRegexInput")
    def validation_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "validationRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="valueTypeInput")
    def value_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce41bbadacf71a98d91b556b534af0e5466a7c63ea265df289571f202a351e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a684580e434bf60b2567160daea25e18fd1ada0078f747a96ba4602c70962512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "required"))

    @required.setter
    def required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd97e966704ad79a79f06c8767bf7135b07ee517347237677b26c8732e1c5ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validationRegex")
    def validation_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validationRegex"))

    @validation_regex.setter
    def validation_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6778b89c6bf361013e6f5e74aa5e369130cbeaba590f339952009d46b314c532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validationRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @value_type.setter
    def value_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d521cfc80119baa8a9079f19cbf23eed3b16a3df4fc839376103d7d8b7b71d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginConfigTemplateAdditionalConfigTemplate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginConfigTemplateAdditionalConfigTemplate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginConfigTemplateAdditionalConfigTemplate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a07417adf8c88a5ccfa514606ddff9f0a68f34cc7cee8805ef98b769d4dfddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAuthConfigTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "supported_auth_types": "supportedAuthTypes",
        "service_account": "serviceAccount",
    },
)
class ApihubPluginConfigTemplateAuthConfigTemplate:
    def __init__(
        self,
        *,
        supported_auth_types: typing.Sequence[builtins.str],
        service_account: typing.Optional[typing.Union["ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param supported_auth_types: The list of authentication types supported by the plugin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#supported_auth_types ApihubPlugin#supported_auth_types}
        :param service_account: service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#service_account ApihubPlugin#service_account}
        '''
        if isinstance(service_account, dict):
            service_account = ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount(**service_account)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3868d830a2f8db5d9b06a02ef4daaa3ae558b7e709f29ce749e592b9e3eddf47)
            check_type(argname="argument supported_auth_types", value=supported_auth_types, expected_type=type_hints["supported_auth_types"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "supported_auth_types": supported_auth_types,
        }
        if service_account is not None:
            self._values["service_account"] = service_account

    @builtins.property
    def supported_auth_types(self) -> typing.List[builtins.str]:
        '''The list of authentication types supported by the plugin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#supported_auth_types ApihubPlugin#supported_auth_types}
        '''
        result = self._values.get("supported_auth_types")
        assert result is not None, "Required property 'supported_auth_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_account(
        self,
    ) -> typing.Optional["ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount"]:
        '''service_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#service_account ApihubPlugin#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional["ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginConfigTemplateAuthConfigTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginConfigTemplateAuthConfigTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAuthConfigTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dc37fd39f3bd8dc3c84e2ae38f3a8632779188d59e3ff8c40ec1bde27754a9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putServiceAccount")
    def put_service_account(self, *, service_account: builtins.str) -> None:
        '''
        :param service_account: The service account to be used for authenticating request. The 'iam.serviceAccounts.getAccessToken' permission should be granted on this service account to the impersonator service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#service_account ApihubPlugin#service_account}
        '''
        value = ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount(
            service_account=service_account
        )

        return typing.cast(None, jsii.invoke(self, "putServiceAccount", [value]))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(
        self,
    ) -> "ApihubPluginConfigTemplateAuthConfigTemplateServiceAccountOutputReference":
        return typing.cast("ApihubPluginConfigTemplateAuthConfigTemplateServiceAccountOutputReference", jsii.get(self, "serviceAccount"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(
        self,
    ) -> typing.Optional["ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount"]:
        return typing.cast(typing.Optional["ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount"], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="supportedAuthTypesInput")
    def supported_auth_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "supportedAuthTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="supportedAuthTypes")
    def supported_auth_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedAuthTypes"))

    @supported_auth_types.setter
    def supported_auth_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc6e435926ca505f568f94cf833fceeb9d7077a2d9b954c51f67a8cb64fc284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportedAuthTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApihubPluginConfigTemplateAuthConfigTemplate]:
        return typing.cast(typing.Optional[ApihubPluginConfigTemplateAuthConfigTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginConfigTemplateAuthConfigTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99eb1891af03e8cc28386a3a0ca069f47a8953f9e7ca6367896afe1b88a62d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount",
    jsii_struct_bases=[],
    name_mapping={"service_account": "serviceAccount"},
)
class ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount:
    def __init__(self, *, service_account: builtins.str) -> None:
        '''
        :param service_account: The service account to be used for authenticating request. The 'iam.serviceAccounts.getAccessToken' permission should be granted on this service account to the impersonator service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#service_account ApihubPlugin#service_account}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__157dae918361baa551d5a4ab8a8468cc48a427894e7d31994dc3a972e7dd5d3d)
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account": service_account,
        }

    @builtins.property
    def service_account(self) -> builtins.str:
        '''The service account to be used for authenticating request.

        The 'iam.serviceAccounts.getAccessToken' permission should be granted on
        this service account to the impersonator service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#service_account ApihubPlugin#service_account}
        '''
        result = self._values.get("service_account")
        assert result is not None, "Required property 'service_account' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginConfigTemplateAuthConfigTemplateServiceAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateAuthConfigTemplateServiceAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb2186319b40a01816cd45aa65be49dad19b0bc81a9ca7c39631dd02eb7973a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca1f77aa93086ac4299e4f60a7c9d46dc98a81cde2ffc88366d38f4c706b80e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount]:
        return typing.cast(typing.Optional[ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9266790cb40c7e58182db7683995b888679ca42c2a48a83eb6f8f86cf7a04ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApihubPluginConfigTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginConfigTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a4847aafd6c59889cea3d4a8603a062ce1d0f4aa47e512095a14a5a38bb47dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalConfigTemplate")
    def put_additional_config_template(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginConfigTemplateAdditionalConfigTemplate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a031de30da17b17522fc9a430ab169914313053c1c447a2edf1da9af70fd95de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalConfigTemplate", [value]))

    @jsii.member(jsii_name="putAuthConfigTemplate")
    def put_auth_config_template(
        self,
        *,
        supported_auth_types: typing.Sequence[builtins.str],
        service_account: typing.Optional[typing.Union[ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param supported_auth_types: The list of authentication types supported by the plugin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#supported_auth_types ApihubPlugin#supported_auth_types}
        :param service_account: service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#service_account ApihubPlugin#service_account}
        '''
        value = ApihubPluginConfigTemplateAuthConfigTemplate(
            supported_auth_types=supported_auth_types, service_account=service_account
        )

        return typing.cast(None, jsii.invoke(self, "putAuthConfigTemplate", [value]))

    @jsii.member(jsii_name="resetAdditionalConfigTemplate")
    def reset_additional_config_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalConfigTemplate", []))

    @jsii.member(jsii_name="resetAuthConfigTemplate")
    def reset_auth_config_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthConfigTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="additionalConfigTemplate")
    def additional_config_template(
        self,
    ) -> ApihubPluginConfigTemplateAdditionalConfigTemplateList:
        return typing.cast(ApihubPluginConfigTemplateAdditionalConfigTemplateList, jsii.get(self, "additionalConfigTemplate"))

    @builtins.property
    @jsii.member(jsii_name="authConfigTemplate")
    def auth_config_template(
        self,
    ) -> ApihubPluginConfigTemplateAuthConfigTemplateOutputReference:
        return typing.cast(ApihubPluginConfigTemplateAuthConfigTemplateOutputReference, jsii.get(self, "authConfigTemplate"))

    @builtins.property
    @jsii.member(jsii_name="additionalConfigTemplateInput")
    def additional_config_template_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplate]]], jsii.get(self, "additionalConfigTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="authConfigTemplateInput")
    def auth_config_template_input(
        self,
    ) -> typing.Optional[ApihubPluginConfigTemplateAuthConfigTemplate]:
        return typing.cast(typing.Optional[ApihubPluginConfigTemplateAuthConfigTemplate], jsii.get(self, "authConfigTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApihubPluginConfigTemplate]:
        return typing.cast(typing.Optional[ApihubPluginConfigTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginConfigTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b340c0208fc416231d8b0fd21a11a442b7aa301d1ff1de43364cf5523e16bd76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginDocumentation",
    jsii_struct_bases=[],
    name_mapping={"external_uri": "externalUri"},
)
class ApihubPluginDocumentation:
    def __init__(self, *, external_uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param external_uri: The uri of the externally hosted documentation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#external_uri ApihubPlugin#external_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c0a2f2d3c92352091f75a56096d4291b6b3c22bf68128f61381b9ab220c325)
            check_type(argname="argument external_uri", value=external_uri, expected_type=type_hints["external_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_uri is not None:
            self._values["external_uri"] = external_uri

    @builtins.property
    def external_uri(self) -> typing.Optional[builtins.str]:
        '''The uri of the externally hosted documentation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#external_uri ApihubPlugin#external_uri}
        '''
        result = self._values.get("external_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginDocumentation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginDocumentationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginDocumentationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f50fcd8f5a5c3ff8a3feba2d778e764a80a5af6a3f0cc45700b71b57b38610c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExternalUri")
    def reset_external_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalUri", []))

    @builtins.property
    @jsii.member(jsii_name="externalUriInput")
    def external_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalUriInput"))

    @builtins.property
    @jsii.member(jsii_name="externalUri")
    def external_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalUri"))

    @external_uri.setter
    def external_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f02464510140560336865a37f8625c3ed8e4f869e1665d0871387ce88f1851a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApihubPluginDocumentation]:
        return typing.cast(typing.Optional[ApihubPluginDocumentation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApihubPluginDocumentation]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd54974c23ea71e87ec30b65d4c801bed453a4dd87dae52eccfa8c67d1b570e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginHostingService",
    jsii_struct_bases=[],
    name_mapping={"service_uri": "serviceUri"},
)
class ApihubPluginHostingService:
    def __init__(self, *, service_uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param service_uri: The URI of the service implemented by the plugin developer, used to invoke the plugin's functionality. This information is only required for user defined plugins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#service_uri ApihubPlugin#service_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda76656782317b99ac286404a9466e678f6595a6cc6520e20a416aedf04b0f0)
            check_type(argname="argument service_uri", value=service_uri, expected_type=type_hints["service_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if service_uri is not None:
            self._values["service_uri"] = service_uri

    @builtins.property
    def service_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the service implemented by the plugin developer, used to invoke the plugin's functionality.

        This information is only required for
        user defined plugins.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#service_uri ApihubPlugin#service_uri}
        '''
        result = self._values.get("service_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginHostingService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginHostingServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginHostingServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43d85ad316aaa993a12ca9ed573e2b1e8344e290c9c7e46ee8f96e25a2e2fe44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetServiceUri")
    def reset_service_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceUri", []))

    @builtins.property
    @jsii.member(jsii_name="serviceUriInput")
    def service_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceUriInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceUri")
    def service_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceUri"))

    @service_uri.setter
    def service_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c718819bb9575f808cfd6a751cd4caad14e298297ee0af10f358494b028f8566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApihubPluginHostingService]:
        return typing.cast(typing.Optional[ApihubPluginHostingService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApihubPluginHostingService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95177f1787f6e996fe917d0743b60149dafb75a489c85dd58d277d5319412ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ApihubPluginTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#create ApihubPlugin#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#delete ApihubPlugin#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04fefff5dcd76d427edb9215c61c3f29d59740bcb4e59afca79db62b84fbfee3)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#create ApihubPlugin#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apihub_plugin#delete ApihubPlugin#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApihubPluginTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApihubPluginTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apihubPlugin.ApihubPluginTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__311126115b88aad3d58c9156bbe0ac2f1b9c1134147d9d86ecb3193e149abe9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e78a4eb54f96a1bb2fa7421acd3bd0ec61d91f4fa0ea6988e24bbafd4f92a883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b036f376412e642a5c30a04f56b63914b0ad058e64ff37ceaf0a75406aa90c4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dbd08d47797bf8fb9b1f065f44b2f25ddbf4caf7c55f13f67f85ccde8448771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApihubPlugin",
    "ApihubPluginActionsConfig",
    "ApihubPluginActionsConfigList",
    "ApihubPluginActionsConfigOutputReference",
    "ApihubPluginConfig",
    "ApihubPluginConfigTemplate",
    "ApihubPluginConfigTemplateAdditionalConfigTemplate",
    "ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions",
    "ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsList",
    "ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsOutputReference",
    "ApihubPluginConfigTemplateAdditionalConfigTemplateList",
    "ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions",
    "ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsList",
    "ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsOutputReference",
    "ApihubPluginConfigTemplateAdditionalConfigTemplateOutputReference",
    "ApihubPluginConfigTemplateAuthConfigTemplate",
    "ApihubPluginConfigTemplateAuthConfigTemplateOutputReference",
    "ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount",
    "ApihubPluginConfigTemplateAuthConfigTemplateServiceAccountOutputReference",
    "ApihubPluginConfigTemplateOutputReference",
    "ApihubPluginDocumentation",
    "ApihubPluginDocumentationOutputReference",
    "ApihubPluginHostingService",
    "ApihubPluginHostingServiceOutputReference",
    "ApihubPluginTimeouts",
    "ApihubPluginTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ae6c1e1e2735681c89af7278d4cba91da36db227c450af0955c5e1208d1f6e8e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    plugin_id: builtins.str,
    actions_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginActionsConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_template: typing.Optional[typing.Union[ApihubPluginConfigTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[typing.Union[ApihubPluginDocumentation, typing.Dict[builtins.str, typing.Any]]] = None,
    hosting_service: typing.Optional[typing.Union[ApihubPluginHostingService, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    plugin_category: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApihubPluginTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__154f015722919b59cb301a491eb9525c117ae61291240fb850f3c26f73f112bf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30cc69e1c2fc04e4197e81081612b09e25b83dee00ac34bda9c390fd2767bd3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginActionsConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f73f97fb46b61de1c27e57f1b22d0b60db887a5c45e185404a0d579bb0d51e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583a468729bcaad29d967c790bae0982f60fe17a1b08e5658c8e2b86d867510a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876c3cca0bd761fe61b029cab62c1cc82a7072623261630c74f043281a07ebab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20606d41291d1755420305f9ea5262988fa08a58c412a7be0991856d26e75c8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d4adc996fa34674258eda5d6b38c78788f95b7ef4b420bd8f74f9de393f2e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462f1124a443552ec18cc849f09923f162bb5b3756448b75272742463557219c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6bf2d4d717859b740610c89b3265b35d1f5ee8a2defedc63cae09831affea09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee6e4673175caeb489a36ea014b36def0f0f757a4d596be7c6d5ffe4cbec695(
    *,
    description: builtins.str,
    display_name: builtins.str,
    id: builtins.str,
    trigger_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96576aaabace562099c8405073ad34d1043a6fe1dd924e870917752f59111716(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aff5708c6a50e0506323f98a28aafc6d7ea70cb0ca073845509bd47759c978a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fcca01f75d5734f545dd34e78a59684a3ffc0d44ebd8af25996da3979741183(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71699f280e23a5a07b5206a859d74ebe07070f9d0c9d78e2b82554b8e82b287b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e8bb94bb272d8cff44c9b7fc703f782ba8c52ac8bd95cfb379ed3a8b34366e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd83890986fd4f90a9d412854ef45d727e3c1f9c58ea7dd460611bae4fee61a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginActionsConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6074f44ab60b118264eda7b1c26427d631ad31cbf0b133dcb9e98e447f76db16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ed7f8aa4df159729946683f78ed390e026c2cc1abdaf8e62addeb5d19038f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ed14ec5158941a53d803e5e36a25b8092ab86435b934aaa10c911bc4c4e96c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9d7d6524bb25854f5c5c80f7827afaeb82737ed32506a834189acb18e94064(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3562d2cd1c9fbea28c321ca1591c15c6d393f30cf7ea79916915e40f2b9919a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672998105ae43b731c256372e11916182f3ae53e366ae7d38b8d8d1a84639209(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginActionsConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62cf6d8dc9d675c6d1156e6d9d5e2a94151eb38ac14e00000058a94335c6b73(
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
    plugin_id: builtins.str,
    actions_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginActionsConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_template: typing.Optional[typing.Union[ApihubPluginConfigTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[typing.Union[ApihubPluginDocumentation, typing.Dict[builtins.str, typing.Any]]] = None,
    hosting_service: typing.Optional[typing.Union[ApihubPluginHostingService, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    plugin_category: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApihubPluginTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37a72efd9296128334333c292653ef22754be0704eca8220ae5ee1499f3f8d0(
    *,
    additional_config_template: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginConfigTemplateAdditionalConfigTemplate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_config_template: typing.Optional[typing.Union[ApihubPluginConfigTemplateAuthConfigTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1cc17b7ddccf268a969fcf562a5a83b13e8776ed6115728ced3a80f2291fe8(
    *,
    id: builtins.str,
    value_type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enum_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    multi_select_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    validation_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f680f8fc4291901f3bdb5615d6ee5ca9bf3884cb361eb0acbab86a20ae1a95b7(
    *,
    display_name: builtins.str,
    id: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbdb29118bd899c1050b9fd63b070c5e7c18de173303c0b581e91684759835a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99aa9c2bb9d383ae8df469ef1b4c8b2019f3c6abe1d758cca71a502d835dd83(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da7fb5dc08a6579e156a8b93048bd90a6bd57ebcaa2e487d0a527c3a8566677(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7057e7e017796ca96513e78d1c7b7ac5605bb8438c6359fd4e63935b7e2d3e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28f7beb04ef9ce744af55eb897ca0be2f7dcf1d9ae08edc7e3c7f4bbf4ae89c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05fa2f66afb7a74f5c121ca374b3c310fd590da576605f7e8cb407775ad925d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cac062d58f46c79c4d84f34591b32b6a4f116e9ffd57017db81fa49a9547238(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597aa1d57412507e7244c62c853769f47ecda24996c68c900109c4342b7a9e2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c497fd3d70ce8603701a3ecab409d439c3b36827c9c41f228584f75d1d4706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e31f23b4cac79114e7432c209cc7b88469279f78c805e276effd350a461ec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d095d95acdb9a7c0154fc0b9b872d3ae926a91e20c4f0ab56a7d41d43ac489(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa46c48807cb2e22a8a777709e1e2a7c0c6a35e3d64cd9ee7083706a48a03157(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4efcb62582331f059a992a4c08d03ab37ba79d3ef728ad1b2c95f42e8be363(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006c9f6effc935c8d407ecc8f57684044f399082df0ecce1b6686355a3e09195(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce715e407e533290e77ccd455785a42f76320539331b48296bbd041b1d20d299(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db3136c47592d2738e763a997ec23faacd5a2bd9f52125a2d94cb059bbd4aa7e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1bbfe37ca4ced38841b220c1e0232abb8a85a10f16d7a4a8fa712bea5730130(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bb3fa4ffd8b90422dc9dbb0571cd53333112da45922a8c342a662a12123739(
    *,
    display_name: builtins.str,
    id: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6723264df2d5ef894be01b46369f50f0e81266de8acf060f4c286cd69707dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f7895a9a1dd1ce2b52ef607755216b9f39e569c6ffe92d19bbd387818a6580(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a712de3ab84c82064387f8cfc8453669319e50ef97fbd3d926224e5e1f87f908(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aaf29204dc6d5a4b26fb85a2cc1a2dbcab04574b00da9973be68df827e4446e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac4d4a3d167242df2d1b7d5aac375b302a20a83a0a35e7df87b52d1eb04c568(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556b97637f3970f31b0db22a54d6c5a77096b727e4664e6ffadfc519fce02b0b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bb19b80a1e697630841c85ded0afff0a3e8f68800185e4cf973b2538ffafc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1ad847b8d7f601e53e2472f75fc895d06017e2bbfcc09b0deb7cece5a816ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1eefdd96580b7e04e973c5afc2d028687b20eafdf9cdc1f1f2521c0fc5371b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f939c014e67a1f8cb345f3d7c522f7c496f49794d2ce582f727c98fdf1f5319f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7093394141e38af62ef4d6b6da39faab610c7ac857fa43a47c543f3c4f276a3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4771678be547a3103f42c349d787dac79df7690cc509f207c98ba10f3f8d897b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06abc1264219d76254e2ebf56184150864e6a0b2dc25d988bdb537f50e27ebdd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7dcbc402ffc0ba8093995fde3778912193cf0f23154a4b7cb1709297f85babb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce41bbadacf71a98d91b556b534af0e5466a7c63ea265df289571f202a351e77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a684580e434bf60b2567160daea25e18fd1ada0078f747a96ba4602c70962512(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd97e966704ad79a79f06c8767bf7135b07ee517347237677b26c8732e1c5ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6778b89c6bf361013e6f5e74aa5e369130cbeaba590f339952009d46b314c532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d521cfc80119baa8a9079f19cbf23eed3b16a3df4fc839376103d7d8b7b71d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a07417adf8c88a5ccfa514606ddff9f0a68f34cc7cee8805ef98b769d4dfddc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginConfigTemplateAdditionalConfigTemplate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3868d830a2f8db5d9b06a02ef4daaa3ae558b7e709f29ce749e592b9e3eddf47(
    *,
    supported_auth_types: typing.Sequence[builtins.str],
    service_account: typing.Optional[typing.Union[ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc37fd39f3bd8dc3c84e2ae38f3a8632779188d59e3ff8c40ec1bde27754a9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc6e435926ca505f568f94cf833fceeb9d7077a2d9b954c51f67a8cb64fc284(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99eb1891af03e8cc28386a3a0ca069f47a8953f9e7ca6367896afe1b88a62d97(
    value: typing.Optional[ApihubPluginConfigTemplateAuthConfigTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157dae918361baa551d5a4ab8a8468cc48a427894e7d31994dc3a972e7dd5d3d(
    *,
    service_account: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2186319b40a01816cd45aa65be49dad19b0bc81a9ca7c39631dd02eb7973a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1f77aa93086ac4299e4f60a7c9d46dc98a81cde2ffc88366d38f4c706b80e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9266790cb40c7e58182db7683995b888679ca42c2a48a83eb6f8f86cf7a04ae(
    value: typing.Optional[ApihubPluginConfigTemplateAuthConfigTemplateServiceAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4847aafd6c59889cea3d4a8603a062ce1d0f4aa47e512095a14a5a38bb47dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a031de30da17b17522fc9a430ab169914313053c1c447a2edf1da9af70fd95de(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApihubPluginConfigTemplateAdditionalConfigTemplate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b340c0208fc416231d8b0fd21a11a442b7aa301d1ff1de43364cf5523e16bd76(
    value: typing.Optional[ApihubPluginConfigTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c0a2f2d3c92352091f75a56096d4291b6b3c22bf68128f61381b9ab220c325(
    *,
    external_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f50fcd8f5a5c3ff8a3feba2d778e764a80a5af6a3f0cc45700b71b57b38610c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02464510140560336865a37f8625c3ed8e4f869e1665d0871387ce88f1851a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd54974c23ea71e87ec30b65d4c801bed453a4dd87dae52eccfa8c67d1b570e(
    value: typing.Optional[ApihubPluginDocumentation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda76656782317b99ac286404a9466e678f6595a6cc6520e20a416aedf04b0f0(
    *,
    service_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d85ad316aaa993a12ca9ed573e2b1e8344e290c9c7e46ee8f96e25a2e2fe44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c718819bb9575f808cfd6a751cd4caad14e298297ee0af10f358494b028f8566(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95177f1787f6e996fe917d0743b60149dafb75a489c85dd58d277d5319412ef0(
    value: typing.Optional[ApihubPluginHostingService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04fefff5dcd76d427edb9215c61c3f29d59740bcb4e59afca79db62b84fbfee3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311126115b88aad3d58c9156bbe0ac2f1b9c1134147d9d86ecb3193e149abe9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78a4eb54f96a1bb2fa7421acd3bd0ec61d91f4fa0ea6988e24bbafd4f92a883(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b036f376412e642a5c30a04f56b63914b0ad058e64ff37ceaf0a75406aa90c4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbd08d47797bf8fb9b1f065f44b2f25ddbf4caf7c55f13f67f85ccde8448771(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApihubPluginTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
