r'''
# `google_apihub_plugin`

Refer to the Terraform Registry for docs: [`google_apihub_plugin`](https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin).
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


class GoogleApihubPlugin(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPlugin",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin google_apihub_plugin}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        plugin_id: builtins.str,
        actions_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApihubPluginActionsConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_template: typing.Optional[typing.Union["GoogleApihubPluginConfigTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[typing.Union["GoogleApihubPluginDocumentation", typing.Dict[builtins.str, typing.Any]]] = None,
        hosting_service: typing.Optional[typing.Union["GoogleApihubPluginHostingService", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        plugin_category: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApihubPluginTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin google_apihub_plugin} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The display name of the plugin. Max length is 50 characters (Unicode code points). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#display_name GoogleApihubPlugin#display_name}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#location GoogleApihubPlugin#location}
        :param plugin_id: The ID to use for the Plugin resource, which will become the final component of the Plugin's resource name. This field is optional. - If provided, the same will be used. The service will throw an error if the specified id is already used by another Plugin resource in the API hub instance. - If not provided, a system generated id will be used. This value should be 4-63 characters, overall resource name which will be of format 'projects/{project}/locations/{location}/plugins/{plugin}', its length is limited to 1000 characters and valid characters are /a-z[0-9]-_/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#plugin_id GoogleApihubPlugin#plugin_id}
        :param actions_config: actions_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#actions_config GoogleApihubPlugin#actions_config}
        :param config_template: config_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#config_template GoogleApihubPlugin#config_template}
        :param description: The plugin description. Max length is 2000 characters (Unicode code points). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#description GoogleApihubPlugin#description}
        :param documentation: documentation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#documentation GoogleApihubPlugin#documentation}
        :param hosting_service: hosting_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#hosting_service GoogleApihubPlugin#hosting_service}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#id GoogleApihubPlugin#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param plugin_category: Possible values: PLUGIN_CATEGORY_UNSPECIFIED API_GATEWAY API_PRODUCER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#plugin_category GoogleApihubPlugin#plugin_category}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#project GoogleApihubPlugin#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#timeouts GoogleApihubPlugin#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5efd29defc611fbfa2a75ad65364e652595f776513e531b42e7aa6c02b140b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleApihubPluginConfig(
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
        '''Generates CDKTF code for importing a GoogleApihubPlugin resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleApihubPlugin to import.
        :param import_from_id: The id of the existing GoogleApihubPlugin that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleApihubPlugin to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a01ad2954b1e1450c71c963aca2a80d98d0ab01f2d8dc5196dc5154ccb61063)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActionsConfig")
    def put_actions_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApihubPluginActionsConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bafc941b86e596fa3b67427a541b5c03c1bec98272fb7c30891e1943fa06ea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActionsConfig", [value]))

    @jsii.member(jsii_name="putConfigTemplate")
    def put_config_template(
        self,
        *,
        additional_config_template: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApihubPluginConfigTemplateAdditionalConfigTemplate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_config_template: typing.Optional[typing.Union["GoogleApihubPluginConfigTemplateAuthConfigTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param additional_config_template: additional_config_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#additional_config_template GoogleApihubPlugin#additional_config_template}
        :param auth_config_template: auth_config_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#auth_config_template GoogleApihubPlugin#auth_config_template}
        '''
        value = GoogleApihubPluginConfigTemplate(
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
        :param external_uri: The uri of the externally hosted documentation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#external_uri GoogleApihubPlugin#external_uri}
        '''
        value = GoogleApihubPluginDocumentation(external_uri=external_uri)

        return typing.cast(None, jsii.invoke(self, "putDocumentation", [value]))

    @jsii.member(jsii_name="putHostingService")
    def put_hosting_service(
        self,
        *,
        service_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_uri: The URI of the service implemented by the plugin developer, used to invoke the plugin's functionality. This information is only required for user defined plugins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#service_uri GoogleApihubPlugin#service_uri}
        '''
        value = GoogleApihubPluginHostingService(service_uri=service_uri)

        return typing.cast(None, jsii.invoke(self, "putHostingService", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#create GoogleApihubPlugin#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#delete GoogleApihubPlugin#delete}.
        '''
        value = GoogleApihubPluginTimeouts(create=create, delete=delete)

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
    def actions_config(self) -> "GoogleApihubPluginActionsConfigList":
        return typing.cast("GoogleApihubPluginActionsConfigList", jsii.get(self, "actionsConfig"))

    @builtins.property
    @jsii.member(jsii_name="configTemplate")
    def config_template(self) -> "GoogleApihubPluginConfigTemplateOutputReference":
        return typing.cast("GoogleApihubPluginConfigTemplateOutputReference", jsii.get(self, "configTemplate"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="documentation")
    def documentation(self) -> "GoogleApihubPluginDocumentationOutputReference":
        return typing.cast("GoogleApihubPluginDocumentationOutputReference", jsii.get(self, "documentation"))

    @builtins.property
    @jsii.member(jsii_name="hostingService")
    def hosting_service(self) -> "GoogleApihubPluginHostingServiceOutputReference":
        return typing.cast("GoogleApihubPluginHostingServiceOutputReference", jsii.get(self, "hostingService"))

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
    def timeouts(self) -> "GoogleApihubPluginTimeoutsOutputReference":
        return typing.cast("GoogleApihubPluginTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="actionsConfigInput")
    def actions_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApihubPluginActionsConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApihubPluginActionsConfig"]]], jsii.get(self, "actionsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="configTemplateInput")
    def config_template_input(
        self,
    ) -> typing.Optional["GoogleApihubPluginConfigTemplate"]:
        return typing.cast(typing.Optional["GoogleApihubPluginConfigTemplate"], jsii.get(self, "configTemplateInput"))

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
    def documentation_input(self) -> typing.Optional["GoogleApihubPluginDocumentation"]:
        return typing.cast(typing.Optional["GoogleApihubPluginDocumentation"], jsii.get(self, "documentationInput"))

    @builtins.property
    @jsii.member(jsii_name="hostingServiceInput")
    def hosting_service_input(
        self,
    ) -> typing.Optional["GoogleApihubPluginHostingService"]:
        return typing.cast(typing.Optional["GoogleApihubPluginHostingService"], jsii.get(self, "hostingServiceInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApihubPluginTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApihubPluginTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbbf12c4087eeac48c9705c20bda4890aee73f0ae94af6ab183901f2035e5937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2319aa68e748db03c85e516e5136887ba2041bb3a50c174fa5a7ff62be25b97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56de936f5b8740b18efa63db0f80398379d1a09f9a22738ce14ae2010055f0cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb1dbde0ade08eb989dab729b8548feb4fff63767b1fcb1cc60c518e3e123d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginCategory")
    def plugin_category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginCategory"))

    @plugin_category.setter
    def plugin_category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b45c3c8f0feecd88b832654637437bef8bb0fcf33d30756eee5a02ddfff71e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginCategory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginId")
    def plugin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginId"))

    @plugin_id.setter
    def plugin_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbb2a95f30846d4de084c67f24ee8c75dd4146c6dd5f16793be9c9098d35d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d6bb3960690c2731f65cc159e889167823b00457990f743c0de8f578b1e33e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginActionsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "trigger_mode": "triggerMode",
    },
)
class GoogleApihubPluginActionsConfig:
    def __init__(
        self,
        *,
        description: builtins.str,
        display_name: builtins.str,
        id: builtins.str,
        trigger_mode: builtins.str,
    ) -> None:
        '''
        :param description: The description of the operation performed by the action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#description GoogleApihubPlugin#description}
        :param display_name: The display name of the action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#display_name GoogleApihubPlugin#display_name}
        :param id: The id of the action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#id GoogleApihubPlugin#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param trigger_mode: The trigger mode supported by the action. Possible values: TRIGGER_MODE_UNSPECIFIED API_HUB_ON_DEMAND_TRIGGER API_HUB_SCHEDULE_TRIGGER NON_API_HUB_MANAGED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#trigger_mode GoogleApihubPlugin#trigger_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f42b61059e7320459575eca9b9490d9027b8867383af360af0516cefcc562b8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#description GoogleApihubPlugin#description}
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name of the action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#display_name GoogleApihubPlugin#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The id of the action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#id GoogleApihubPlugin#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_mode(self) -> builtins.str:
        '''The trigger mode supported by the action. Possible values: TRIGGER_MODE_UNSPECIFIED API_HUB_ON_DEMAND_TRIGGER API_HUB_SCHEDULE_TRIGGER NON_API_HUB_MANAGED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#trigger_mode GoogleApihubPlugin#trigger_mode}
        '''
        result = self._values.get("trigger_mode")
        assert result is not None, "Required property 'trigger_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginActionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginActionsConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginActionsConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d53e44604288627ddc20b77cdf94c243a05fe8e20d2d1bcc237885ec5534a7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApihubPluginActionsConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f65ea9d2b478c539895a3176b10680472b2e19405a4a24d03be66cf186b51b48)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApihubPluginActionsConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08df86779f6dfe677b7fec1ad3f3c518296ac62ea5a6d4c008d5cbe95b3ab88a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cc495366857c480fcbf7607e9a3a4f1fed519d177b8c10c972078637ceb673a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a2e9f719e9adad488c093d461c26d9e7cec25e799eaba8cb83a10bc8c723b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginActionsConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginActionsConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginActionsConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519653fcca05894735a806ffbddaa3711d87ba48f40468597cecff058b1bfda0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginActionsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginActionsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7467bd5b7f491a608c322989920532cd5d1baf2d809aa9b284f753f0247df64b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e3c9530d9b9e3e9bab5c9886c0b2d434297cde2fbef1e5a31f25e07a5b6a34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f691ba8ef2bbd7d980546758671915af67e4d8ef7571ba47cbebe454906877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f299705606af2ac5d0c0e181a9291e2efca84f57e73b2554767c62b331d047a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerMode")
    def trigger_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerMode"))

    @trigger_mode.setter
    def trigger_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86993bc0ea821dbd228e968b803e219cd60068d0ca3f094c613bf2fb4b7dd8b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginActionsConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginActionsConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginActionsConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7caaa144f5d68f78e4a87abc0b3ea1fa962bb41327d53374c190054d433693b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfig",
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
class GoogleApihubPluginConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        actions_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginActionsConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
        config_template: typing.Optional[typing.Union["GoogleApihubPluginConfigTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[typing.Union["GoogleApihubPluginDocumentation", typing.Dict[builtins.str, typing.Any]]] = None,
        hosting_service: typing.Optional[typing.Union["GoogleApihubPluginHostingService", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        plugin_category: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApihubPluginTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The display name of the plugin. Max length is 50 characters (Unicode code points). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#display_name GoogleApihubPlugin#display_name}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#location GoogleApihubPlugin#location}
        :param plugin_id: The ID to use for the Plugin resource, which will become the final component of the Plugin's resource name. This field is optional. - If provided, the same will be used. The service will throw an error if the specified id is already used by another Plugin resource in the API hub instance. - If not provided, a system generated id will be used. This value should be 4-63 characters, overall resource name which will be of format 'projects/{project}/locations/{location}/plugins/{plugin}', its length is limited to 1000 characters and valid characters are /a-z[0-9]-_/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#plugin_id GoogleApihubPlugin#plugin_id}
        :param actions_config: actions_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#actions_config GoogleApihubPlugin#actions_config}
        :param config_template: config_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#config_template GoogleApihubPlugin#config_template}
        :param description: The plugin description. Max length is 2000 characters (Unicode code points). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#description GoogleApihubPlugin#description}
        :param documentation: documentation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#documentation GoogleApihubPlugin#documentation}
        :param hosting_service: hosting_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#hosting_service GoogleApihubPlugin#hosting_service}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#id GoogleApihubPlugin#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param plugin_category: Possible values: PLUGIN_CATEGORY_UNSPECIFIED API_GATEWAY API_PRODUCER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#plugin_category GoogleApihubPlugin#plugin_category}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#project GoogleApihubPlugin#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#timeouts GoogleApihubPlugin#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config_template, dict):
            config_template = GoogleApihubPluginConfigTemplate(**config_template)
        if isinstance(documentation, dict):
            documentation = GoogleApihubPluginDocumentation(**documentation)
        if isinstance(hosting_service, dict):
            hosting_service = GoogleApihubPluginHostingService(**hosting_service)
        if isinstance(timeouts, dict):
            timeouts = GoogleApihubPluginTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8bc2aee7f17a2c1e465b325c3650fd102a9e679474921906ee8e6e739d8e8c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#display_name GoogleApihubPlugin#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#location GoogleApihubPlugin#location}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#plugin_id GoogleApihubPlugin#plugin_id}
        '''
        result = self._values.get("plugin_id")
        assert result is not None, "Required property 'plugin_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginActionsConfig]]]:
        '''actions_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#actions_config GoogleApihubPlugin#actions_config}
        '''
        result = self._values.get("actions_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginActionsConfig]]], result)

    @builtins.property
    def config_template(self) -> typing.Optional["GoogleApihubPluginConfigTemplate"]:
        '''config_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#config_template GoogleApihubPlugin#config_template}
        '''
        result = self._values.get("config_template")
        return typing.cast(typing.Optional["GoogleApihubPluginConfigTemplate"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The plugin description. Max length is 2000 characters (Unicode code points).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#description GoogleApihubPlugin#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def documentation(self) -> typing.Optional["GoogleApihubPluginDocumentation"]:
        '''documentation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#documentation GoogleApihubPlugin#documentation}
        '''
        result = self._values.get("documentation")
        return typing.cast(typing.Optional["GoogleApihubPluginDocumentation"], result)

    @builtins.property
    def hosting_service(self) -> typing.Optional["GoogleApihubPluginHostingService"]:
        '''hosting_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#hosting_service GoogleApihubPlugin#hosting_service}
        '''
        result = self._values.get("hosting_service")
        return typing.cast(typing.Optional["GoogleApihubPluginHostingService"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#id GoogleApihubPlugin#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_category(self) -> typing.Optional[builtins.str]:
        '''Possible values: PLUGIN_CATEGORY_UNSPECIFIED API_GATEWAY API_PRODUCER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#plugin_category GoogleApihubPlugin#plugin_category}
        '''
        result = self._values.get("plugin_category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#project GoogleApihubPlugin#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleApihubPluginTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#timeouts GoogleApihubPlugin#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleApihubPluginTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "additional_config_template": "additionalConfigTemplate",
        "auth_config_template": "authConfigTemplate",
    },
)
class GoogleApihubPluginConfigTemplate:
    def __init__(
        self,
        *,
        additional_config_template: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApihubPluginConfigTemplateAdditionalConfigTemplate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        auth_config_template: typing.Optional[typing.Union["GoogleApihubPluginConfigTemplateAuthConfigTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param additional_config_template: additional_config_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#additional_config_template GoogleApihubPlugin#additional_config_template}
        :param auth_config_template: auth_config_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#auth_config_template GoogleApihubPlugin#auth_config_template}
        '''
        if isinstance(auth_config_template, dict):
            auth_config_template = GoogleApihubPluginConfigTemplateAuthConfigTemplate(**auth_config_template)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58db66342522b3288b56c04a0456f4990b137da9efa140e8ee9ef2beef52693e)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApihubPluginConfigTemplateAdditionalConfigTemplate"]]]:
        '''additional_config_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#additional_config_template GoogleApihubPlugin#additional_config_template}
        '''
        result = self._values.get("additional_config_template")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApihubPluginConfigTemplateAdditionalConfigTemplate"]]], result)

    @builtins.property
    def auth_config_template(
        self,
    ) -> typing.Optional["GoogleApihubPluginConfigTemplateAuthConfigTemplate"]:
        '''auth_config_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#auth_config_template GoogleApihubPlugin#auth_config_template}
        '''
        result = self._values.get("auth_config_template")
        return typing.cast(typing.Optional["GoogleApihubPluginConfigTemplateAuthConfigTemplate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginConfigTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAdditionalConfigTemplate",
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
class GoogleApihubPluginConfigTemplateAdditionalConfigTemplate:
    def __init__(
        self,
        *,
        id: builtins.str,
        value_type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enum_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        multi_select_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        validation_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: ID of the config variable. Must be unique within the configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#id GoogleApihubPlugin#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param value_type: Type of the parameter: string, int, bool etc. Possible values: VALUE_TYPE_UNSPECIFIED STRING INT BOOL SECRET ENUM MULTI_SELECT MULTI_STRING MULTI_INT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#value_type GoogleApihubPlugin#value_type}
        :param description: Description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#description GoogleApihubPlugin#description}
        :param enum_options: enum_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#enum_options GoogleApihubPlugin#enum_options}
        :param multi_select_options: multi_select_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#multi_select_options GoogleApihubPlugin#multi_select_options}
        :param required: Flag represents that this 'ConfigVariable' must be provided for a PluginInstance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#required GoogleApihubPlugin#required}
        :param validation_regex: Regular expression in RE2 syntax used for validating the 'value' of a 'ConfigVariable'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#validation_regex GoogleApihubPlugin#validation_regex}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb4a767c288a082651bda61d984e6bb362247e074bea1629425042acb4bc587c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#id GoogleApihubPlugin#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value_type(self) -> builtins.str:
        '''Type of the parameter: string, int, bool etc. Possible values: VALUE_TYPE_UNSPECIFIED STRING INT BOOL SECRET ENUM MULTI_SELECT MULTI_STRING MULTI_INT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#value_type GoogleApihubPlugin#value_type}
        '''
        result = self._values.get("value_type")
        assert result is not None, "Required property 'value_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#description GoogleApihubPlugin#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enum_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions"]]]:
        '''enum_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#enum_options GoogleApihubPlugin#enum_options}
        '''
        result = self._values.get("enum_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions"]]], result)

    @builtins.property
    def multi_select_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions"]]]:
        '''multi_select_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#multi_select_options GoogleApihubPlugin#multi_select_options}
        '''
        result = self._values.get("multi_select_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions"]]], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag represents that this 'ConfigVariable' must be provided for a PluginInstance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#required GoogleApihubPlugin#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def validation_regex(self) -> typing.Optional[builtins.str]:
        '''Regular expression in RE2 syntax used for validating the 'value' of a 'ConfigVariable'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#validation_regex GoogleApihubPlugin#validation_regex}
        '''
        result = self._values.get("validation_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginConfigTemplateAdditionalConfigTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "id": "id",
        "description": "description",
    },
)
class GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        id: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Display name of the option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#display_name GoogleApihubPlugin#display_name}
        :param id: Id of the option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#id GoogleApihubPlugin#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param description: Description of the option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#description GoogleApihubPlugin#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8948530177f5065621c078ae986be44350cab4c4aaefea85d2310a55a98ed3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#display_name GoogleApihubPlugin#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Id of the option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#id GoogleApihubPlugin#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#description GoogleApihubPlugin#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eae6cc457729121a95639163d77414c0f6d10fea186ea344aebe4103cf1e9e72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff99a134f0f141f31fca5a786776b94ead1fb9037c76213cc8bcadc965a94a4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31baf367a83e784258e1b7e8b17033afd5b7885d13a30dced552035502f82af2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e27cf2e3cf9b06cb88ec2a61ac05ecb3bf0dbca1769696007aaf6dfedd4a7d1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db948769c74a27a5db94c65616227606ecd1116f057b8830a037130946c3bb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e145f423a420ec26e67a3aee5928dc6c24b8872ddc2b95f9ce95e00d1d754c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eba771fcdf3e1c351a72313146d1221f6e5e84ceb25746552e510c80471bee0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8cc4fcae2e60d9e221575cfc93d510e5c27758d5771d4eeeb617dc6582ec65f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb8cafda26395dfbce7739d5e9b3871296c025fb3c89f54504a0098f8f73287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aafe8cec621e43a6067b66b84ae1b635d06198cfa4b37c76e73899a11f2b98b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51d22e195e5b90ba0d6c19124b4e0cd8465f45d1bc0e30bfc399c983c670a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginConfigTemplateAdditionalConfigTemplateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAdditionalConfigTemplateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88aeffbf4087e1e64a6138af97b3ab0eabfc3e9b3a5c0515ba6a74a53a6489c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7c8d1bce04b2b0b5e41c662b1069667ae4b3e0816b22042b2f61043e5a6c2a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApihubPluginConfigTemplateAdditionalConfigTemplateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d65f602f880a45703fd50751e7d57859824f0dd5ecb5e8192181f531d6f0ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97546fc8ac84eb24b0dcd81047cdceee498a489ae66bad9c659e79a891f1f0aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c5fd16814f5efb43bd3a3be19fe95f5c0c4bdee2c3fecf3e23ac1946f17baee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ef499d9d4635de6b40c2dbdb27be30393f4b2ed19953cfdd03d03d340b98ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "id": "id",
        "description": "description",
    },
)
class GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        id: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: Display name of the option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#display_name GoogleApihubPlugin#display_name}
        :param id: Id of the option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#id GoogleApihubPlugin#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param description: Description of the option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#description GoogleApihubPlugin#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b48a7f9b697d99e805eb7239eeff481e5ac48fe3795010d5362a0f01d895100)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#display_name GoogleApihubPlugin#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Id of the option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#id GoogleApihubPlugin#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#description GoogleApihubPlugin#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa70200cdbe740a204baf9b96c0558ae3e0ee304a9971b99224e40a422fa319b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5ad7ad5cc115a26126f6c6c512492f2807e78e83fd27438f7a084de08d36e6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcd1cf252eb8b9bf763a7b03bc06afd20da99b81859de3bc6a25810934ca526)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24ddc421b714d5a882e80adf607618724273d31a94875ce0802003e320a858db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33d6e749284c5352e2c9d7f2f7c033b9c7a7ca321bc566f9155c9408f62c83ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb7d6720d779cf692db191a341fa4330607fbf64d5de8982f76a873f4322aa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90701267008340ef89daaf743ea6f0fbdf3d5c93a8f110bffc1405d0531555ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b354ef30ad8e47206d7b7009a07161adf97df445d74b39b59cede1b42231e550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e162b65482e96d69d178685ec27c86281801b465227d805fa89e0432df854f68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0672d47c9c015a711cd4f2a5cfd6aeb784e1afa7558b15925bdeb9449c303a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b263a9c9485e40dc7fe696efae789bbbf2d47f748c96f8ea008689e749a0fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginConfigTemplateAdditionalConfigTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAdditionalConfigTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d185edfebd30f4df196b2e1aea7aa7228274e8efa4fcdc4a7fa8cd652265483)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnumOptions")
    def put_enum_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8395f2a2d5864df2bab4502e830f8d9fdcd808767efbab772cbe0a7380f48b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnumOptions", [value]))

    @jsii.member(jsii_name="putMultiSelectOptions")
    def put_multi_select_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0fe7e75b47bd91e80ab078095de8361c0acc11984a94a829b59924932cfa7f4)
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
    ) -> GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsList:
        return typing.cast(GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsList, jsii.get(self, "enumOptions"))

    @builtins.property
    @jsii.member(jsii_name="multiSelectOptions")
    def multi_select_options(
        self,
    ) -> GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsList:
        return typing.cast(GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsList, jsii.get(self, "multiSelectOptions"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enumOptionsInput")
    def enum_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]], jsii.get(self, "enumOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="multiSelectOptionsInput")
    def multi_select_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]], jsii.get(self, "multiSelectOptionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__41e5d5142beafc23e06677446ea5b155c8e6d709706e20c235fb522f8854e85f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d716e7287ab04eb5876c5a14529dca9b21fc186d24d152a4f39199a5a0c2be06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ab04e7aa98bed0c51c7dc53dd8506b137ad555b9869a0e56bd3bd9b1407110f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validationRegex")
    def validation_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validationRegex"))

    @validation_regex.setter
    def validation_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c507300f4fd1e15666a12f9f6ca2ca9b9315133f30d84fd2ad5f3dda98a6690b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validationRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @value_type.setter
    def value_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4b19f58d38174efd2edc4ea3c05efd87ae0ac67fa42c9a9b3f32c4707b8e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginConfigTemplateAdditionalConfigTemplate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginConfigTemplateAdditionalConfigTemplate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginConfigTemplateAdditionalConfigTemplate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cf55e55a9a98a5e5eec4572e20757451d7f2f857113684a2287cd9058c5b11b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAuthConfigTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "supported_auth_types": "supportedAuthTypes",
        "service_account": "serviceAccount",
    },
)
class GoogleApihubPluginConfigTemplateAuthConfigTemplate:
    def __init__(
        self,
        *,
        supported_auth_types: typing.Sequence[builtins.str],
        service_account: typing.Optional[typing.Union["GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param supported_auth_types: The list of authentication types supported by the plugin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#supported_auth_types GoogleApihubPlugin#supported_auth_types}
        :param service_account: service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#service_account GoogleApihubPlugin#service_account}
        '''
        if isinstance(service_account, dict):
            service_account = GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount(**service_account)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae26d2451591f6cd857daa2dc2e99b3282ccd1e2662d94585e94ba900b0eb67b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#supported_auth_types GoogleApihubPlugin#supported_auth_types}
        '''
        result = self._values.get("supported_auth_types")
        assert result is not None, "Required property 'supported_auth_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_account(
        self,
    ) -> typing.Optional["GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount"]:
        '''service_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#service_account GoogleApihubPlugin#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional["GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginConfigTemplateAuthConfigTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginConfigTemplateAuthConfigTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAuthConfigTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__845947805fc17fe8aba8f9d4cf352f7a1b8ef986684bf6f07f5c7a6f818b40dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putServiceAccount")
    def put_service_account(self, *, service_account: builtins.str) -> None:
        '''
        :param service_account: The service account to be used for authenticating request. The 'iam.serviceAccounts.getAccessToken' permission should be granted on this service account to the impersonator service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#service_account GoogleApihubPlugin#service_account}
        '''
        value = GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount(
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
    ) -> "GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccountOutputReference":
        return typing.cast("GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccountOutputReference", jsii.get(self, "serviceAccount"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(
        self,
    ) -> typing.Optional["GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount"]:
        return typing.cast(typing.Optional["GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount"], jsii.get(self, "serviceAccountInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9e46c60b3e7ff9647c68360320c96678aa1f56826212641c1f00982581097248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportedAuthTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginConfigTemplateAuthConfigTemplate]:
        return typing.cast(typing.Optional[GoogleApihubPluginConfigTemplateAuthConfigTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginConfigTemplateAuthConfigTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6d27de63b20ccdc85ee4b793106dd1aaedb7a682f99cbd9f143aeba5f51bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount",
    jsii_struct_bases=[],
    name_mapping={"service_account": "serviceAccount"},
)
class GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount:
    def __init__(self, *, service_account: builtins.str) -> None:
        '''
        :param service_account: The service account to be used for authenticating request. The 'iam.serviceAccounts.getAccessToken' permission should be granted on this service account to the impersonator service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#service_account GoogleApihubPlugin#service_account}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c041d7cf8a18a5dc51f332a35452a39819d98fbdc1feb63f07d58ea9bb00d249)
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account": service_account,
        }

    @builtins.property
    def service_account(self) -> builtins.str:
        '''The service account to be used for authenticating request.

        The 'iam.serviceAccounts.getAccessToken' permission should be granted on
        this service account to the impersonator service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#service_account GoogleApihubPlugin#service_account}
        '''
        result = self._values.get("service_account")
        assert result is not None, "Required property 'service_account' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__867f7bd20c59d27069e05b851cf5589d53a4930a18c1bc3631ee631b9ec5c998)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fb9c333521f4ba1123eb9a3e26b3cfd0a81e8981b1164609b4770ce344a1718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount]:
        return typing.cast(typing.Optional[GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20dc0a01b4ce8e007699b36ddf5b49706bd5a15d60e073dc39e25f321ec9428c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApihubPluginConfigTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginConfigTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc5f81d4385ebd69f32bec8e5f516abcdf103cc28573143edfaddc328af082e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalConfigTemplate")
    def put_additional_config_template(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginConfigTemplateAdditionalConfigTemplate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d326e93e6cd07d392f180666280ac7de61ad11165b90b2bfd3469421689d5b23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalConfigTemplate", [value]))

    @jsii.member(jsii_name="putAuthConfigTemplate")
    def put_auth_config_template(
        self,
        *,
        supported_auth_types: typing.Sequence[builtins.str],
        service_account: typing.Optional[typing.Union[GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param supported_auth_types: The list of authentication types supported by the plugin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#supported_auth_types GoogleApihubPlugin#supported_auth_types}
        :param service_account: service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#service_account GoogleApihubPlugin#service_account}
        '''
        value = GoogleApihubPluginConfigTemplateAuthConfigTemplate(
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
    ) -> GoogleApihubPluginConfigTemplateAdditionalConfigTemplateList:
        return typing.cast(GoogleApihubPluginConfigTemplateAdditionalConfigTemplateList, jsii.get(self, "additionalConfigTemplate"))

    @builtins.property
    @jsii.member(jsii_name="authConfigTemplate")
    def auth_config_template(
        self,
    ) -> GoogleApihubPluginConfigTemplateAuthConfigTemplateOutputReference:
        return typing.cast(GoogleApihubPluginConfigTemplateAuthConfigTemplateOutputReference, jsii.get(self, "authConfigTemplate"))

    @builtins.property
    @jsii.member(jsii_name="additionalConfigTemplateInput")
    def additional_config_template_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplate]]], jsii.get(self, "additionalConfigTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="authConfigTemplateInput")
    def auth_config_template_input(
        self,
    ) -> typing.Optional[GoogleApihubPluginConfigTemplateAuthConfigTemplate]:
        return typing.cast(typing.Optional[GoogleApihubPluginConfigTemplateAuthConfigTemplate], jsii.get(self, "authConfigTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApihubPluginConfigTemplate]:
        return typing.cast(typing.Optional[GoogleApihubPluginConfigTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginConfigTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b08232b54be9d4d7d26054c70c84bbd5646c814d79cca3b7721ce84c853f1eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginDocumentation",
    jsii_struct_bases=[],
    name_mapping={"external_uri": "externalUri"},
)
class GoogleApihubPluginDocumentation:
    def __init__(self, *, external_uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param external_uri: The uri of the externally hosted documentation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#external_uri GoogleApihubPlugin#external_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3816befc05b35a717a1bf2040b3e9fb4d4127f9f021b1a418d5078cb6e2da968)
            check_type(argname="argument external_uri", value=external_uri, expected_type=type_hints["external_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_uri is not None:
            self._values["external_uri"] = external_uri

    @builtins.property
    def external_uri(self) -> typing.Optional[builtins.str]:
        '''The uri of the externally hosted documentation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#external_uri GoogleApihubPlugin#external_uri}
        '''
        result = self._values.get("external_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginDocumentation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginDocumentationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginDocumentationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2491675c8d25e7243e12caad2f1c084abf07caa90601e4bc4e3042322217fc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__462e19bc1380f85a8252e2f9b6b0d1ea1071623b12ad7150421449348eed960e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApihubPluginDocumentation]:
        return typing.cast(typing.Optional[GoogleApihubPluginDocumentation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginDocumentation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab4997c358c20c32b9ce1fb5b2563ccb784cd863a9c2fd98f89212f32a2a2308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginHostingService",
    jsii_struct_bases=[],
    name_mapping={"service_uri": "serviceUri"},
)
class GoogleApihubPluginHostingService:
    def __init__(self, *, service_uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param service_uri: The URI of the service implemented by the plugin developer, used to invoke the plugin's functionality. This information is only required for user defined plugins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#service_uri GoogleApihubPlugin#service_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b25b16464fc79d5c902f098d4026afe4cc7540cc39a4ba569aa38e714381a9a)
            check_type(argname="argument service_uri", value=service_uri, expected_type=type_hints["service_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if service_uri is not None:
            self._values["service_uri"] = service_uri

    @builtins.property
    def service_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the service implemented by the plugin developer, used to invoke the plugin's functionality.

        This information is only required for
        user defined plugins.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#service_uri GoogleApihubPlugin#service_uri}
        '''
        result = self._values.get("service_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginHostingService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginHostingServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginHostingServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3da1467b96b767e48d50ab11bec6b73eed982bd76aeabc9fb2391a6f22c61cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23bddb7bba4aada1eb4e2a5958f23b44d533cba53414b9fc5ea2bdf16353c624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApihubPluginHostingService]:
        return typing.cast(typing.Optional[GoogleApihubPluginHostingService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApihubPluginHostingService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e2b1ae6dbe6a49d70b61f06ec72478f1a36d0faf532784298fe7db7c375998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleApihubPluginTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#create GoogleApihubPlugin#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#delete GoogleApihubPlugin#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5bc52b8e78f34bdf6dc28cebb91cbde14921fac6a0137722527135400cc15a5)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#create GoogleApihubPlugin#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_apihub_plugin#delete GoogleApihubPlugin#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApihubPluginTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApihubPluginTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApihubPlugin.GoogleApihubPluginTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24c5d84f069a45a9280b551bee2678ce87a37f51dfadb4c09799868ef4646f3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39dd0546a2dcaae0200613f0cfeb5db12485bc7680170265725105d42ccb5681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1355366ba5b49a9082d3af5179238a63b8ad16c5c4515b04092dd98b1812cbcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b92c8085ba345937b231542aa85a0060a0dfc69eb0fe872359bb6bcd91fda6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleApihubPlugin",
    "GoogleApihubPluginActionsConfig",
    "GoogleApihubPluginActionsConfigList",
    "GoogleApihubPluginActionsConfigOutputReference",
    "GoogleApihubPluginConfig",
    "GoogleApihubPluginConfigTemplate",
    "GoogleApihubPluginConfigTemplateAdditionalConfigTemplate",
    "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions",
    "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsList",
    "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptionsOutputReference",
    "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateList",
    "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions",
    "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsList",
    "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptionsOutputReference",
    "GoogleApihubPluginConfigTemplateAdditionalConfigTemplateOutputReference",
    "GoogleApihubPluginConfigTemplateAuthConfigTemplate",
    "GoogleApihubPluginConfigTemplateAuthConfigTemplateOutputReference",
    "GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount",
    "GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccountOutputReference",
    "GoogleApihubPluginConfigTemplateOutputReference",
    "GoogleApihubPluginDocumentation",
    "GoogleApihubPluginDocumentationOutputReference",
    "GoogleApihubPluginHostingService",
    "GoogleApihubPluginHostingServiceOutputReference",
    "GoogleApihubPluginTimeouts",
    "GoogleApihubPluginTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e5efd29defc611fbfa2a75ad65364e652595f776513e531b42e7aa6c02b140b9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    plugin_id: builtins.str,
    actions_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginActionsConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_template: typing.Optional[typing.Union[GoogleApihubPluginConfigTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[typing.Union[GoogleApihubPluginDocumentation, typing.Dict[builtins.str, typing.Any]]] = None,
    hosting_service: typing.Optional[typing.Union[GoogleApihubPluginHostingService, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    plugin_category: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApihubPluginTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2a01ad2954b1e1450c71c963aca2a80d98d0ab01f2d8dc5196dc5154ccb61063(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bafc941b86e596fa3b67427a541b5c03c1bec98272fb7c30891e1943fa06ea2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginActionsConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbbf12c4087eeac48c9705c20bda4890aee73f0ae94af6ab183901f2035e5937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2319aa68e748db03c85e516e5136887ba2041bb3a50c174fa5a7ff62be25b97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56de936f5b8740b18efa63db0f80398379d1a09f9a22738ce14ae2010055f0cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb1dbde0ade08eb989dab729b8548feb4fff63767b1fcb1cc60c518e3e123d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b45c3c8f0feecd88b832654637437bef8bb0fcf33d30756eee5a02ddfff71e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbb2a95f30846d4de084c67f24ee8c75dd4146c6dd5f16793be9c9098d35d77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d6bb3960690c2731f65cc159e889167823b00457990f743c0de8f578b1e33e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f42b61059e7320459575eca9b9490d9027b8867383af360af0516cefcc562b8(
    *,
    description: builtins.str,
    display_name: builtins.str,
    id: builtins.str,
    trigger_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d53e44604288627ddc20b77cdf94c243a05fe8e20d2d1bcc237885ec5534a7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65ea9d2b478c539895a3176b10680472b2e19405a4a24d03be66cf186b51b48(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08df86779f6dfe677b7fec1ad3f3c518296ac62ea5a6d4c008d5cbe95b3ab88a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc495366857c480fcbf7607e9a3a4f1fed519d177b8c10c972078637ceb673a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2e9f719e9adad488c093d461c26d9e7cec25e799eaba8cb83a10bc8c723b0e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519653fcca05894735a806ffbddaa3711d87ba48f40468597cecff058b1bfda0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginActionsConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7467bd5b7f491a608c322989920532cd5d1baf2d809aa9b284f753f0247df64b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3c9530d9b9e3e9bab5c9886c0b2d434297cde2fbef1e5a31f25e07a5b6a34e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f691ba8ef2bbd7d980546758671915af67e4d8ef7571ba47cbebe454906877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f299705606af2ac5d0c0e181a9291e2efca84f57e73b2554767c62b331d047a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86993bc0ea821dbd228e968b803e219cd60068d0ca3f094c613bf2fb4b7dd8b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7caaa144f5d68f78e4a87abc0b3ea1fa962bb41327d53374c190054d433693b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginActionsConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8bc2aee7f17a2c1e465b325c3650fd102a9e679474921906ee8e6e739d8e8c(
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
    actions_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginActionsConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_template: typing.Optional[typing.Union[GoogleApihubPluginConfigTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[typing.Union[GoogleApihubPluginDocumentation, typing.Dict[builtins.str, typing.Any]]] = None,
    hosting_service: typing.Optional[typing.Union[GoogleApihubPluginHostingService, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    plugin_category: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApihubPluginTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58db66342522b3288b56c04a0456f4990b137da9efa140e8ee9ef2beef52693e(
    *,
    additional_config_template: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginConfigTemplateAdditionalConfigTemplate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_config_template: typing.Optional[typing.Union[GoogleApihubPluginConfigTemplateAuthConfigTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb4a767c288a082651bda61d984e6bb362247e074bea1629425042acb4bc587c(
    *,
    id: builtins.str,
    value_type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enum_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    multi_select_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    validation_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8948530177f5065621c078ae986be44350cab4c4aaefea85d2310a55a98ed3(
    *,
    display_name: builtins.str,
    id: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae6cc457729121a95639163d77414c0f6d10fea186ea344aebe4103cf1e9e72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff99a134f0f141f31fca5a786776b94ead1fb9037c76213cc8bcadc965a94a4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31baf367a83e784258e1b7e8b17033afd5b7885d13a30dced552035502f82af2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27cf2e3cf9b06cb88ec2a61ac05ecb3bf0dbca1769696007aaf6dfedd4a7d1c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db948769c74a27a5db94c65616227606ecd1116f057b8830a037130946c3bb71(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e145f423a420ec26e67a3aee5928dc6c24b8872ddc2b95f9ce95e00d1d754c0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba771fcdf3e1c351a72313146d1221f6e5e84ceb25746552e510c80471bee0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8cc4fcae2e60d9e221575cfc93d510e5c27758d5771d4eeeb617dc6582ec65f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb8cafda26395dfbce7739d5e9b3871296c025fb3c89f54504a0098f8f73287(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aafe8cec621e43a6067b66b84ae1b635d06198cfa4b37c76e73899a11f2b98b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51d22e195e5b90ba0d6c19124b4e0cd8465f45d1bc0e30bfc399c983c670a44(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88aeffbf4087e1e64a6138af97b3ab0eabfc3e9b3a5c0515ba6a74a53a6489c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7c8d1bce04b2b0b5e41c662b1069667ae4b3e0816b22042b2f61043e5a6c2a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d65f602f880a45703fd50751e7d57859824f0dd5ecb5e8192181f531d6f0ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97546fc8ac84eb24b0dcd81047cdceee498a489ae66bad9c659e79a891f1f0aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5fd16814f5efb43bd3a3be19fe95f5c0c4bdee2c3fecf3e23ac1946f17baee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ef499d9d4635de6b40c2dbdb27be30393f4b2ed19953cfdd03d03d340b98ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b48a7f9b697d99e805eb7239eeff481e5ac48fe3795010d5362a0f01d895100(
    *,
    display_name: builtins.str,
    id: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa70200cdbe740a204baf9b96c0558ae3e0ee304a9971b99224e40a422fa319b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5ad7ad5cc115a26126f6c6c512492f2807e78e83fd27438f7a084de08d36e6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcd1cf252eb8b9bf763a7b03bc06afd20da99b81859de3bc6a25810934ca526(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ddc421b714d5a882e80adf607618724273d31a94875ce0802003e320a858db(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d6e749284c5352e2c9d7f2f7c033b9c7a7ca321bc566f9155c9408f62c83ba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb7d6720d779cf692db191a341fa4330607fbf64d5de8982f76a873f4322aa1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90701267008340ef89daaf743ea6f0fbdf3d5c93a8f110bffc1405d0531555ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b354ef30ad8e47206d7b7009a07161adf97df445d74b39b59cede1b42231e550(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e162b65482e96d69d178685ec27c86281801b465227d805fa89e0432df854f68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0672d47c9c015a711cd4f2a5cfd6aeb784e1afa7558b15925bdeb9449c303a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b263a9c9485e40dc7fe696efae789bbbf2d47f748c96f8ea008689e749a0fd7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d185edfebd30f4df196b2e1aea7aa7228274e8efa4fcdc4a7fa8cd652265483(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8395f2a2d5864df2bab4502e830f8d9fdcd808767efbab772cbe0a7380f48b69(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateEnumOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fe7e75b47bd91e80ab078095de8361c0acc11984a94a829b59924932cfa7f4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginConfigTemplateAdditionalConfigTemplateMultiSelectOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e5d5142beafc23e06677446ea5b155c8e6d709706e20c235fb522f8854e85f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d716e7287ab04eb5876c5a14529dca9b21fc186d24d152a4f39199a5a0c2be06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab04e7aa98bed0c51c7dc53dd8506b137ad555b9869a0e56bd3bd9b1407110f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c507300f4fd1e15666a12f9f6ca2ca9b9315133f30d84fd2ad5f3dda98a6690b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4b19f58d38174efd2edc4ea3c05efd87ae0ac67fa42c9a9b3f32c4707b8e52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf55e55a9a98a5e5eec4572e20757451d7f2f857113684a2287cd9058c5b11b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginConfigTemplateAdditionalConfigTemplate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae26d2451591f6cd857daa2dc2e99b3282ccd1e2662d94585e94ba900b0eb67b(
    *,
    supported_auth_types: typing.Sequence[builtins.str],
    service_account: typing.Optional[typing.Union[GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845947805fc17fe8aba8f9d4cf352f7a1b8ef986684bf6f07f5c7a6f818b40dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e46c60b3e7ff9647c68360320c96678aa1f56826212641c1f00982581097248(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6d27de63b20ccdc85ee4b793106dd1aaedb7a682f99cbd9f143aeba5f51bcd(
    value: typing.Optional[GoogleApihubPluginConfigTemplateAuthConfigTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c041d7cf8a18a5dc51f332a35452a39819d98fbdc1feb63f07d58ea9bb00d249(
    *,
    service_account: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867f7bd20c59d27069e05b851cf5589d53a4930a18c1bc3631ee631b9ec5c998(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb9c333521f4ba1123eb9a3e26b3cfd0a81e8981b1164609b4770ce344a1718(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20dc0a01b4ce8e007699b36ddf5b49706bd5a15d60e073dc39e25f321ec9428c(
    value: typing.Optional[GoogleApihubPluginConfigTemplateAuthConfigTemplateServiceAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5f81d4385ebd69f32bec8e5f516abcdf103cc28573143edfaddc328af082e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d326e93e6cd07d392f180666280ac7de61ad11165b90b2bfd3469421689d5b23(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApihubPluginConfigTemplateAdditionalConfigTemplate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08232b54be9d4d7d26054c70c84bbd5646c814d79cca3b7721ce84c853f1eb8(
    value: typing.Optional[GoogleApihubPluginConfigTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3816befc05b35a717a1bf2040b3e9fb4d4127f9f021b1a418d5078cb6e2da968(
    *,
    external_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2491675c8d25e7243e12caad2f1c084abf07caa90601e4bc4e3042322217fc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462e19bc1380f85a8252e2f9b6b0d1ea1071623b12ad7150421449348eed960e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4997c358c20c32b9ce1fb5b2563ccb784cd863a9c2fd98f89212f32a2a2308(
    value: typing.Optional[GoogleApihubPluginDocumentation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b25b16464fc79d5c902f098d4026afe4cc7540cc39a4ba569aa38e714381a9a(
    *,
    service_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3da1467b96b767e48d50ab11bec6b73eed982bd76aeabc9fb2391a6f22c61cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23bddb7bba4aada1eb4e2a5958f23b44d533cba53414b9fc5ea2bdf16353c624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e2b1ae6dbe6a49d70b61f06ec72478f1a36d0faf532784298fe7db7c375998(
    value: typing.Optional[GoogleApihubPluginHostingService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bc52b8e78f34bdf6dc28cebb91cbde14921fac6a0137722527135400cc15a5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c5d84f069a45a9280b551bee2678ce87a37f51dfadb4c09799868ef4646f3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39dd0546a2dcaae0200613f0cfeb5db12485bc7680170265725105d42ccb5681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1355366ba5b49a9082d3af5179238a63b8ad16c5c4515b04092dd98b1812cbcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b92c8085ba345937b231542aa85a0060a0dfc69eb0fe872359bb6bcd91fda6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApihubPluginTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
