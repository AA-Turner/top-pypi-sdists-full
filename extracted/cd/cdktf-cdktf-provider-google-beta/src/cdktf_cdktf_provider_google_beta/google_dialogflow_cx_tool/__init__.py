r'''
# `google_dialogflow_cx_tool`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_tool`](https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool).
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


class GoogleDialogflowCxTool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxTool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool google_dialogflow_cx_tool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        description: builtins.str,
        display_name: builtins.str,
        data_store_spec: typing.Optional[typing.Union["GoogleDialogflowCxToolDataStoreSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        function_spec: typing.Optional[typing.Union["GoogleDialogflowCxToolFunctionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        open_api_spec: typing.Optional[typing.Union["GoogleDialogflowCxToolOpenApiSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowCxToolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool google_dialogflow_cx_tool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: High level description of the Tool and its usage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#description GoogleDialogflowCxTool#description}
        :param display_name: The human-readable name of the tool, unique within the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#display_name GoogleDialogflowCxTool#display_name}
        :param data_store_spec: data_store_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#data_store_spec GoogleDialogflowCxTool#data_store_spec}
        :param function_spec: function_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#function_spec GoogleDialogflowCxTool#function_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#id GoogleDialogflowCxTool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param open_api_spec: open_api_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#open_api_spec GoogleDialogflowCxTool#open_api_spec}
        :param parent: The agent to create a Tool for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#parent GoogleDialogflowCxTool#parent}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#timeouts GoogleDialogflowCxTool#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15d805081d9c45d88022969c7cf246c4c3c20e7944162b6d44eed662ecdd531)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDialogflowCxToolConfig(
            description=description,
            display_name=display_name,
            data_store_spec=data_store_spec,
            function_spec=function_spec,
            id=id,
            open_api_spec=open_api_spec,
            parent=parent,
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
        '''Generates CDKTF code for importing a GoogleDialogflowCxTool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDialogflowCxTool to import.
        :param import_from_id: The id of the existing GoogleDialogflowCxTool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDialogflowCxTool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3525e3b1e74271de92292453cbf3e7823059ffc6088cd38d22f7cfeef7d4b9cf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataStoreSpec")
    def put_data_store_spec(
        self,
        *,
        data_store_connections: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxToolDataStoreSpecDataStoreConnections", typing.Dict[builtins.str, typing.Any]]]],
        fallback_prompt: typing.Union["GoogleDialogflowCxToolDataStoreSpecFallbackPrompt", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param data_store_connections: data_store_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#data_store_connections GoogleDialogflowCxTool#data_store_connections}
        :param fallback_prompt: fallback_prompt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#fallback_prompt GoogleDialogflowCxTool#fallback_prompt}
        '''
        value = GoogleDialogflowCxToolDataStoreSpec(
            data_store_connections=data_store_connections,
            fallback_prompt=fallback_prompt,
        )

        return typing.cast(None, jsii.invoke(self, "putDataStoreSpec", [value]))

    @jsii.member(jsii_name="putFunctionSpec")
    def put_function_spec(
        self,
        *,
        input_schema: typing.Optional[builtins.str] = None,
        output_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input_schema: Optional. The JSON schema is encapsulated in a `google.protobuf.Struct <https://protobuf.dev/reference/protobuf/google.protobuf/#struct>`_ to describe the input of the function. This input is a JSON object that contains the function's parameters as properties of the object Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#input_schema GoogleDialogflowCxTool#input_schema}
        :param output_schema: Optional. The JSON schema is encapsulated in a `google.protobuf.Struct <https://protobuf.dev/reference/protobuf/google.protobuf/#struct>`_ to describe the output of the function. This output is a JSON object that contains the function's parameters as properties of the object Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#output_schema GoogleDialogflowCxTool#output_schema}
        '''
        value = GoogleDialogflowCxToolFunctionSpec(
            input_schema=input_schema, output_schema=output_schema
        )

        return typing.cast(None, jsii.invoke(self, "putFunctionSpec", [value]))

    @jsii.member(jsii_name="putOpenApiSpec")
    def put_open_api_spec(
        self,
        *,
        text_schema: builtins.str,
        authentication: typing.Optional[typing.Union["GoogleDialogflowCxToolOpenApiSpecAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        service_directory_config: typing.Optional[typing.Union["GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_config: typing.Optional[typing.Union["GoogleDialogflowCxToolOpenApiSpecTlsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param text_schema: The OpenAPI schema specified as a text. This field is part of a union field 'schema': only one of 'textSchema' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#text_schema GoogleDialogflowCxTool#text_schema}
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#authentication GoogleDialogflowCxTool#authentication}
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#service_directory_config GoogleDialogflowCxTool#service_directory_config}
        :param tls_config: tls_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#tls_config GoogleDialogflowCxTool#tls_config}
        '''
        value = GoogleDialogflowCxToolOpenApiSpec(
            text_schema=text_schema,
            authentication=authentication,
            service_directory_config=service_directory_config,
            tls_config=tls_config,
        )

        return typing.cast(None, jsii.invoke(self, "putOpenApiSpec", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#create GoogleDialogflowCxTool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#delete GoogleDialogflowCxTool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#update GoogleDialogflowCxTool#update}.
        '''
        value = GoogleDialogflowCxToolTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDataStoreSpec")
    def reset_data_store_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStoreSpec", []))

    @jsii.member(jsii_name="resetFunctionSpec")
    def reset_function_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionSpec", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOpenApiSpec")
    def reset_open_api_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpenApiSpec", []))

    @jsii.member(jsii_name="resetParent")
    def reset_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParent", []))

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
    @jsii.member(jsii_name="dataStoreSpec")
    def data_store_spec(self) -> "GoogleDialogflowCxToolDataStoreSpecOutputReference":
        return typing.cast("GoogleDialogflowCxToolDataStoreSpecOutputReference", jsii.get(self, "dataStoreSpec"))

    @builtins.property
    @jsii.member(jsii_name="functionSpec")
    def function_spec(self) -> "GoogleDialogflowCxToolFunctionSpecOutputReference":
        return typing.cast("GoogleDialogflowCxToolFunctionSpecOutputReference", jsii.get(self, "functionSpec"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="openApiSpec")
    def open_api_spec(self) -> "GoogleDialogflowCxToolOpenApiSpecOutputReference":
        return typing.cast("GoogleDialogflowCxToolOpenApiSpecOutputReference", jsii.get(self, "openApiSpec"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDialogflowCxToolTimeoutsOutputReference":
        return typing.cast("GoogleDialogflowCxToolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="toolType")
    def tool_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "toolType"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreSpecInput")
    def data_store_spec_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolDataStoreSpec"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxToolDataStoreSpec"], jsii.get(self, "dataStoreSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="functionSpecInput")
    def function_spec_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolFunctionSpec"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxToolFunctionSpec"], jsii.get(self, "functionSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="openApiSpecInput")
    def open_api_spec_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolOpenApiSpec"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxToolOpenApiSpec"], jsii.get(self, "openApiSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowCxToolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDialogflowCxToolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c30947b1e94f2aa0cee2586274f21e9547da2a1701f04bfae56c508df3d866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2972b439d1eb4dce828ddf41c1a2cad2301796cb246da9306299f8288029300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d92eb76c71c62cfbc544b6d7f4ea4b458964a5b1bc001bc603cf1507db88b7ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f808f2839f05bb8f8c176013b7175cb6747160fc8eb6ae5ee658d147d085dd85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "description": "description",
        "display_name": "displayName",
        "data_store_spec": "dataStoreSpec",
        "function_spec": "functionSpec",
        "id": "id",
        "open_api_spec": "openApiSpec",
        "parent": "parent",
        "timeouts": "timeouts",
    },
)
class GoogleDialogflowCxToolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: builtins.str,
        display_name: builtins.str,
        data_store_spec: typing.Optional[typing.Union["GoogleDialogflowCxToolDataStoreSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        function_spec: typing.Optional[typing.Union["GoogleDialogflowCxToolFunctionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        open_api_spec: typing.Optional[typing.Union["GoogleDialogflowCxToolOpenApiSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDialogflowCxToolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param description: High level description of the Tool and its usage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#description GoogleDialogflowCxTool#description}
        :param display_name: The human-readable name of the tool, unique within the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#display_name GoogleDialogflowCxTool#display_name}
        :param data_store_spec: data_store_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#data_store_spec GoogleDialogflowCxTool#data_store_spec}
        :param function_spec: function_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#function_spec GoogleDialogflowCxTool#function_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#id GoogleDialogflowCxTool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param open_api_spec: open_api_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#open_api_spec GoogleDialogflowCxTool#open_api_spec}
        :param parent: The agent to create a Tool for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#parent GoogleDialogflowCxTool#parent}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#timeouts GoogleDialogflowCxTool#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_store_spec, dict):
            data_store_spec = GoogleDialogflowCxToolDataStoreSpec(**data_store_spec)
        if isinstance(function_spec, dict):
            function_spec = GoogleDialogflowCxToolFunctionSpec(**function_spec)
        if isinstance(open_api_spec, dict):
            open_api_spec = GoogleDialogflowCxToolOpenApiSpec(**open_api_spec)
        if isinstance(timeouts, dict):
            timeouts = GoogleDialogflowCxToolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a1e710a050333000e7b3ffa3af2d6edc8bf5ddea3c13490edc3b1bb01cad3b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument data_store_spec", value=data_store_spec, expected_type=type_hints["data_store_spec"])
            check_type(argname="argument function_spec", value=function_spec, expected_type=type_hints["function_spec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument open_api_spec", value=open_api_spec, expected_type=type_hints["open_api_spec"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "display_name": display_name,
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
        if data_store_spec is not None:
            self._values["data_store_spec"] = data_store_spec
        if function_spec is not None:
            self._values["function_spec"] = function_spec
        if id is not None:
            self._values["id"] = id
        if open_api_spec is not None:
            self._values["open_api_spec"] = open_api_spec
        if parent is not None:
            self._values["parent"] = parent
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
    def description(self) -> builtins.str:
        '''High level description of the Tool and its usage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#description GoogleDialogflowCxTool#description}
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The human-readable name of the tool, unique within the agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#display_name GoogleDialogflowCxTool#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_store_spec(self) -> typing.Optional["GoogleDialogflowCxToolDataStoreSpec"]:
        '''data_store_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#data_store_spec GoogleDialogflowCxTool#data_store_spec}
        '''
        result = self._values.get("data_store_spec")
        return typing.cast(typing.Optional["GoogleDialogflowCxToolDataStoreSpec"], result)

    @builtins.property
    def function_spec(self) -> typing.Optional["GoogleDialogflowCxToolFunctionSpec"]:
        '''function_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#function_spec GoogleDialogflowCxTool#function_spec}
        '''
        result = self._values.get("function_spec")
        return typing.cast(typing.Optional["GoogleDialogflowCxToolFunctionSpec"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#id GoogleDialogflowCxTool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_api_spec(self) -> typing.Optional["GoogleDialogflowCxToolOpenApiSpec"]:
        '''open_api_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#open_api_spec GoogleDialogflowCxTool#open_api_spec}
        '''
        result = self._values.get("open_api_spec")
        return typing.cast(typing.Optional["GoogleDialogflowCxToolOpenApiSpec"], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The agent to create a Tool for. Format: projects//locations//agents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#parent GoogleDialogflowCxTool#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDialogflowCxToolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#timeouts GoogleDialogflowCxTool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDialogflowCxToolTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolDataStoreSpec",
    jsii_struct_bases=[],
    name_mapping={
        "data_store_connections": "dataStoreConnections",
        "fallback_prompt": "fallbackPrompt",
    },
)
class GoogleDialogflowCxToolDataStoreSpec:
    def __init__(
        self,
        *,
        data_store_connections: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxToolDataStoreSpecDataStoreConnections", typing.Dict[builtins.str, typing.Any]]]],
        fallback_prompt: typing.Union["GoogleDialogflowCxToolDataStoreSpecFallbackPrompt", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param data_store_connections: data_store_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#data_store_connections GoogleDialogflowCxTool#data_store_connections}
        :param fallback_prompt: fallback_prompt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#fallback_prompt GoogleDialogflowCxTool#fallback_prompt}
        '''
        if isinstance(fallback_prompt, dict):
            fallback_prompt = GoogleDialogflowCxToolDataStoreSpecFallbackPrompt(**fallback_prompt)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9be93ab35fd4535bb1706741a32c35d7577a2849629adf7425501d5ad0e6ea3)
            check_type(argname="argument data_store_connections", value=data_store_connections, expected_type=type_hints["data_store_connections"])
            check_type(argname="argument fallback_prompt", value=fallback_prompt, expected_type=type_hints["fallback_prompt"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_store_connections": data_store_connections,
            "fallback_prompt": fallback_prompt,
        }

    @builtins.property
    def data_store_connections(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxToolDataStoreSpecDataStoreConnections"]]:
        '''data_store_connections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#data_store_connections GoogleDialogflowCxTool#data_store_connections}
        '''
        result = self._values.get("data_store_connections")
        assert result is not None, "Required property 'data_store_connections' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxToolDataStoreSpecDataStoreConnections"]], result)

    @builtins.property
    def fallback_prompt(self) -> "GoogleDialogflowCxToolDataStoreSpecFallbackPrompt":
        '''fallback_prompt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#fallback_prompt GoogleDialogflowCxTool#fallback_prompt}
        '''
        result = self._values.get("fallback_prompt")
        assert result is not None, "Required property 'fallback_prompt' is missing"
        return typing.cast("GoogleDialogflowCxToolDataStoreSpecFallbackPrompt", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolDataStoreSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolDataStoreSpecDataStoreConnections",
    jsii_struct_bases=[],
    name_mapping={
        "data_store": "dataStore",
        "data_store_type": "dataStoreType",
        "document_processing_mode": "documentProcessingMode",
    },
)
class GoogleDialogflowCxToolDataStoreSpecDataStoreConnections:
    def __init__(
        self,
        *,
        data_store: typing.Optional[builtins.str] = None,
        data_store_type: typing.Optional[builtins.str] = None,
        document_processing_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_store: The full name of the referenced data store. Formats: projects/{project}/locations/{location}/collections/{collection}/dataStores/{dataStore} projects/{project}/locations/{location}/dataStores/{dataStore}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#data_store GoogleDialogflowCxTool#data_store}
        :param data_store_type: The type of the connected data store. See `DataStoreType <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/DataStoreConnection#datastoretype>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#data_store_type GoogleDialogflowCxTool#data_store_type}
        :param document_processing_mode: The document processing mode for the data store connection. Should only be set for PUBLIC_WEB and UNSTRUCTURED data stores. If not set it is considered as DOCUMENTS, as this is the legacy mode. See `DocumentProcessingMode <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/DataStoreConnection#documentprocessingmode>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#document_processing_mode GoogleDialogflowCxTool#document_processing_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a493cb8a63c887c9c40d6ded239ce5939f0ad817d6cb1be3712846c3f0847de)
            check_type(argname="argument data_store", value=data_store, expected_type=type_hints["data_store"])
            check_type(argname="argument data_store_type", value=data_store_type, expected_type=type_hints["data_store_type"])
            check_type(argname="argument document_processing_mode", value=document_processing_mode, expected_type=type_hints["document_processing_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_store is not None:
            self._values["data_store"] = data_store
        if data_store_type is not None:
            self._values["data_store_type"] = data_store_type
        if document_processing_mode is not None:
            self._values["document_processing_mode"] = document_processing_mode

    @builtins.property
    def data_store(self) -> typing.Optional[builtins.str]:
        '''The full name of the referenced data store. Formats: projects/{project}/locations/{location}/collections/{collection}/dataStores/{dataStore} projects/{project}/locations/{location}/dataStores/{dataStore}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#data_store GoogleDialogflowCxTool#data_store}
        '''
        result = self._values.get("data_store")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_store_type(self) -> typing.Optional[builtins.str]:
        '''The type of the connected data store. See `DataStoreType <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/DataStoreConnection#datastoretype>`_ for valid values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#data_store_type GoogleDialogflowCxTool#data_store_type}
        '''
        result = self._values.get("data_store_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_processing_mode(self) -> typing.Optional[builtins.str]:
        '''The document processing mode for the data store connection.

        Should only be set for PUBLIC_WEB and UNSTRUCTURED data stores. If not set it is considered as DOCUMENTS, as this is the legacy mode.
        See `DocumentProcessingMode <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/DataStoreConnection#documentprocessingmode>`_ for valid values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#document_processing_mode GoogleDialogflowCxTool#document_processing_mode}
        '''
        result = self._values.get("document_processing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolDataStoreSpecDataStoreConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxToolDataStoreSpecDataStoreConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolDataStoreSpecDataStoreConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9a6c34edf65e023a50f3a51cd4444ddb5407ec65c7edc7e977619f717cc7f7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxToolDataStoreSpecDataStoreConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be74758044c705ce12263d417af5bceb7672047a07d41c6f4cc5ac9ed08628ee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxToolDataStoreSpecDataStoreConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c990cfc09d2f8106827a42954ba0108af1159227ab2154090db90405f00b1867)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6891715c158ac7febca84778e92ca78ed0f87a202b137f547fbb06058e7b2524)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b74552165f2b99ede3991eb03b1cd9f9a74bbcd34abe00961ffdb172b27b73a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxToolDataStoreSpecDataStoreConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxToolDataStoreSpecDataStoreConnections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxToolDataStoreSpecDataStoreConnections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362a885f97dc2e36b072740420e2a849e11369f0d995c38350bd2c077f7cdd70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxToolDataStoreSpecDataStoreConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolDataStoreSpecDataStoreConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__842f0577f1a68784bede3cfd237cf61c19b8b8cd9b78c02c94ae514292934a05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDataStore")
    def reset_data_store(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStore", []))

    @jsii.member(jsii_name="resetDataStoreType")
    def reset_data_store_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStoreType", []))

    @jsii.member(jsii_name="resetDocumentProcessingMode")
    def reset_document_processing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentProcessingMode", []))

    @builtins.property
    @jsii.member(jsii_name="dataStoreInput")
    def data_store_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreTypeInput")
    def data_store_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataStoreTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="documentProcessingModeInput")
    def document_processing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentProcessingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStore")
    def data_store(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataStore"))

    @data_store.setter
    def data_store(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a4c9a94b15b84d4c4b12e06508ffc14ef5fd978927370e23f39ffa6ace68801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStoreType")
    def data_store_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataStoreType"))

    @data_store_type.setter
    def data_store_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a720d1ecbe69e4151c7f2acfbd0ed4352651dc1de3744111f18254e8624328e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentProcessingMode")
    def document_processing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentProcessingMode"))

    @document_processing_mode.setter
    def document_processing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d00c999e4c1bc8394973dc45561d24a6bf4ec6d18d3721b1e43e9f8ad47817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentProcessingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxToolDataStoreSpecDataStoreConnections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxToolDataStoreSpecDataStoreConnections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxToolDataStoreSpecDataStoreConnections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d84147deaef834c6ed2eb201e8a6bed72136079909f7371fc5ff4c705ee7ba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolDataStoreSpecFallbackPrompt",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDialogflowCxToolDataStoreSpecFallbackPrompt:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolDataStoreSpecFallbackPrompt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxToolDataStoreSpecFallbackPromptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolDataStoreSpecFallbackPromptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff193dfc2e77989b2034c54b2a24bfbdfff8efb2a461a1397981ab131809aba2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolDataStoreSpecFallbackPrompt]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolDataStoreSpecFallbackPrompt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxToolDataStoreSpecFallbackPrompt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46332e64eac97cac9222c77aba11755c50cd8c7d3b9684a810599a19da387ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxToolDataStoreSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolDataStoreSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__969cf064b190093c58466c0583e5f8a45d46cf48d91e2b805c5b445762434c1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataStoreConnections")
    def put_data_store_connections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxToolDataStoreSpecDataStoreConnections, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d3b10f26231a90deead0e6ec505e1d9a43dfaa950ad6a18ebf9479fb98fc78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataStoreConnections", [value]))

    @jsii.member(jsii_name="putFallbackPrompt")
    def put_fallback_prompt(self) -> None:
        value = GoogleDialogflowCxToolDataStoreSpecFallbackPrompt()

        return typing.cast(None, jsii.invoke(self, "putFallbackPrompt", [value]))

    @builtins.property
    @jsii.member(jsii_name="dataStoreConnections")
    def data_store_connections(
        self,
    ) -> GoogleDialogflowCxToolDataStoreSpecDataStoreConnectionsList:
        return typing.cast(GoogleDialogflowCxToolDataStoreSpecDataStoreConnectionsList, jsii.get(self, "dataStoreConnections"))

    @builtins.property
    @jsii.member(jsii_name="fallbackPrompt")
    def fallback_prompt(
        self,
    ) -> GoogleDialogflowCxToolDataStoreSpecFallbackPromptOutputReference:
        return typing.cast(GoogleDialogflowCxToolDataStoreSpecFallbackPromptOutputReference, jsii.get(self, "fallbackPrompt"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreConnectionsInput")
    def data_store_connections_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxToolDataStoreSpecDataStoreConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxToolDataStoreSpecDataStoreConnections]]], jsii.get(self, "dataStoreConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fallbackPromptInput")
    def fallback_prompt_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolDataStoreSpecFallbackPrompt]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolDataStoreSpecFallbackPrompt], jsii.get(self, "fallbackPromptInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDialogflowCxToolDataStoreSpec]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolDataStoreSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxToolDataStoreSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6f91aaf06b490c5f406d9aa6d24c73958560bbce1d61b4d9c05019d62eb013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolFunctionSpec",
    jsii_struct_bases=[],
    name_mapping={"input_schema": "inputSchema", "output_schema": "outputSchema"},
)
class GoogleDialogflowCxToolFunctionSpec:
    def __init__(
        self,
        *,
        input_schema: typing.Optional[builtins.str] = None,
        output_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input_schema: Optional. The JSON schema is encapsulated in a `google.protobuf.Struct <https://protobuf.dev/reference/protobuf/google.protobuf/#struct>`_ to describe the input of the function. This input is a JSON object that contains the function's parameters as properties of the object Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#input_schema GoogleDialogflowCxTool#input_schema}
        :param output_schema: Optional. The JSON schema is encapsulated in a `google.protobuf.Struct <https://protobuf.dev/reference/protobuf/google.protobuf/#struct>`_ to describe the output of the function. This output is a JSON object that contains the function's parameters as properties of the object Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#output_schema GoogleDialogflowCxTool#output_schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52eb615b90f04e8f5ac08fa8585f8815ab5c7737d21b6a500fd71bac701952e2)
            check_type(argname="argument input_schema", value=input_schema, expected_type=type_hints["input_schema"])
            check_type(argname="argument output_schema", value=output_schema, expected_type=type_hints["output_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_schema is not None:
            self._values["input_schema"] = input_schema
        if output_schema is not None:
            self._values["output_schema"] = output_schema

    @builtins.property
    def input_schema(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The JSON schema is encapsulated in a `google.protobuf.Struct <https://protobuf.dev/reference/protobuf/google.protobuf/#struct>`_ to describe the input of the function.
        This input is a JSON object that contains the function's parameters as properties of the object

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#input_schema GoogleDialogflowCxTool#input_schema}
        '''
        result = self._values.get("input_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_schema(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The JSON schema is encapsulated in a `google.protobuf.Struct <https://protobuf.dev/reference/protobuf/google.protobuf/#struct>`_ to describe the output of the function.
        This output is a JSON object that contains the function's parameters as properties of the object

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#output_schema GoogleDialogflowCxTool#output_schema}
        '''
        result = self._values.get("output_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolFunctionSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxToolFunctionSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolFunctionSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ec6e1201233b8fd9bbacf0588b0d73ffdcb28b5ae33c72f63d687e8f1987625)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInputSchema")
    def reset_input_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputSchema", []))

    @jsii.member(jsii_name="resetOutputSchema")
    def reset_output_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputSchema", []))

    @builtins.property
    @jsii.member(jsii_name="inputSchemaInput")
    def input_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="outputSchemaInput")
    def output_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="inputSchema")
    def input_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputSchema"))

    @input_schema.setter
    def input_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19274c7bd4c5b03aafdaf7babe185981910802211f0f035229754467c22f868e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputSchema")
    def output_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputSchema"))

    @output_schema.setter
    def output_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5221c6446a380b42e27abedf082b91fedc91161077e79fe142be7caf7d34e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDialogflowCxToolFunctionSpec]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolFunctionSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxToolFunctionSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2caa6dac16c044d03d62516186122ba6afc4be002a7151e2ab0d9a643d258650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpec",
    jsii_struct_bases=[],
    name_mapping={
        "text_schema": "textSchema",
        "authentication": "authentication",
        "service_directory_config": "serviceDirectoryConfig",
        "tls_config": "tlsConfig",
    },
)
class GoogleDialogflowCxToolOpenApiSpec:
    def __init__(
        self,
        *,
        text_schema: builtins.str,
        authentication: typing.Optional[typing.Union["GoogleDialogflowCxToolOpenApiSpecAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        service_directory_config: typing.Optional[typing.Union["GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_config: typing.Optional[typing.Union["GoogleDialogflowCxToolOpenApiSpecTlsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param text_schema: The OpenAPI schema specified as a text. This field is part of a union field 'schema': only one of 'textSchema' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#text_schema GoogleDialogflowCxTool#text_schema}
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#authentication GoogleDialogflowCxTool#authentication}
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#service_directory_config GoogleDialogflowCxTool#service_directory_config}
        :param tls_config: tls_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#tls_config GoogleDialogflowCxTool#tls_config}
        '''
        if isinstance(authentication, dict):
            authentication = GoogleDialogflowCxToolOpenApiSpecAuthentication(**authentication)
        if isinstance(service_directory_config, dict):
            service_directory_config = GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig(**service_directory_config)
        if isinstance(tls_config, dict):
            tls_config = GoogleDialogflowCxToolOpenApiSpecTlsConfig(**tls_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d3468afb071c3e661fd19251e70ba9c118e26fb384757b4aa9f3c895a7758c)
            check_type(argname="argument text_schema", value=text_schema, expected_type=type_hints["text_schema"])
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
            check_type(argname="argument service_directory_config", value=service_directory_config, expected_type=type_hints["service_directory_config"])
            check_type(argname="argument tls_config", value=tls_config, expected_type=type_hints["tls_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "text_schema": text_schema,
        }
        if authentication is not None:
            self._values["authentication"] = authentication
        if service_directory_config is not None:
            self._values["service_directory_config"] = service_directory_config
        if tls_config is not None:
            self._values["tls_config"] = tls_config

    @builtins.property
    def text_schema(self) -> builtins.str:
        '''The OpenAPI schema specified as a text.

        This field is part of a union field 'schema': only one of 'textSchema' may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#text_schema GoogleDialogflowCxTool#text_schema}
        '''
        result = self._values.get("text_schema")
        assert result is not None, "Required property 'text_schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolOpenApiSpecAuthentication"]:
        '''authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#authentication GoogleDialogflowCxTool#authentication}
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional["GoogleDialogflowCxToolOpenApiSpecAuthentication"], result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#service_directory_config GoogleDialogflowCxTool#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig"], result)

    @builtins.property
    def tls_config(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolOpenApiSpecTlsConfig"]:
        '''tls_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#tls_config GoogleDialogflowCxTool#tls_config}
        '''
        result = self._values.get("tls_config")
        return typing.cast(typing.Optional["GoogleDialogflowCxToolOpenApiSpecTlsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolOpenApiSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "api_key_config": "apiKeyConfig",
        "bearer_token_config": "bearerTokenConfig",
        "oauth_config": "oauthConfig",
        "service_agent_auth_config": "serviceAgentAuthConfig",
    },
)
class GoogleDialogflowCxToolOpenApiSpecAuthentication:
    def __init__(
        self,
        *,
        api_key_config: typing.Optional[typing.Union["GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        bearer_token_config: typing.Optional[typing.Union["GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_config: typing.Optional[typing.Union["GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        service_agent_auth_config: typing.Optional[typing.Union["GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_key_config: api_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#api_key_config GoogleDialogflowCxTool#api_key_config}
        :param bearer_token_config: bearer_token_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#bearer_token_config GoogleDialogflowCxTool#bearer_token_config}
        :param oauth_config: oauth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#oauth_config GoogleDialogflowCxTool#oauth_config}
        :param service_agent_auth_config: service_agent_auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#service_agent_auth_config GoogleDialogflowCxTool#service_agent_auth_config}
        '''
        if isinstance(api_key_config, dict):
            api_key_config = GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig(**api_key_config)
        if isinstance(bearer_token_config, dict):
            bearer_token_config = GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig(**bearer_token_config)
        if isinstance(oauth_config, dict):
            oauth_config = GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig(**oauth_config)
        if isinstance(service_agent_auth_config, dict):
            service_agent_auth_config = GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig(**service_agent_auth_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300ed473d4605c2cbb752bca95a5cdced3b8e717ca3fe5c5a51a103788642d69)
            check_type(argname="argument api_key_config", value=api_key_config, expected_type=type_hints["api_key_config"])
            check_type(argname="argument bearer_token_config", value=bearer_token_config, expected_type=type_hints["bearer_token_config"])
            check_type(argname="argument oauth_config", value=oauth_config, expected_type=type_hints["oauth_config"])
            check_type(argname="argument service_agent_auth_config", value=service_agent_auth_config, expected_type=type_hints["service_agent_auth_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_key_config is not None:
            self._values["api_key_config"] = api_key_config
        if bearer_token_config is not None:
            self._values["bearer_token_config"] = bearer_token_config
        if oauth_config is not None:
            self._values["oauth_config"] = oauth_config
        if service_agent_auth_config is not None:
            self._values["service_agent_auth_config"] = service_agent_auth_config

    @builtins.property
    def api_key_config(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig"]:
        '''api_key_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#api_key_config GoogleDialogflowCxTool#api_key_config}
        '''
        result = self._values.get("api_key_config")
        return typing.cast(typing.Optional["GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig"], result)

    @builtins.property
    def bearer_token_config(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig"]:
        '''bearer_token_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#bearer_token_config GoogleDialogflowCxTool#bearer_token_config}
        '''
        result = self._values.get("bearer_token_config")
        return typing.cast(typing.Optional["GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig"], result)

    @builtins.property
    def oauth_config(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig"]:
        '''oauth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#oauth_config GoogleDialogflowCxTool#oauth_config}
        '''
        result = self._values.get("oauth_config")
        return typing.cast(typing.Optional["GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig"], result)

    @builtins.property
    def service_agent_auth_config(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig"]:
        '''service_agent_auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#service_agent_auth_config GoogleDialogflowCxTool#service_agent_auth_config}
        '''
        result = self._values.get("service_agent_auth_config")
        return typing.cast(typing.Optional["GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolOpenApiSpecAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig",
    jsii_struct_bases=[],
    name_mapping={
        "key_name": "keyName",
        "request_location": "requestLocation",
        "api_key": "apiKey",
        "secret_version_for_api_key": "secretVersionForApiKey",
    },
)
class GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig:
    def __init__(
        self,
        *,
        key_name: builtins.str,
        request_location: builtins.str,
        api_key: typing.Optional[builtins.str] = None,
        secret_version_for_api_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_name: The parameter name or the header name of the API key. E.g., If the API request is "https://example.com/act?X-Api-Key=", "X-Api-Key" would be the parameter name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#key_name GoogleDialogflowCxTool#key_name}
        :param request_location: Key location in the request. See `RequestLocation <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#requestlocation>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#request_location GoogleDialogflowCxTool#request_location}
        :param api_key: Optional. The API key. If the 'secretVersionForApiKey'' field is set, this field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#api_key GoogleDialogflowCxTool#api_key}
        :param secret_version_for_api_key: Optional. The name of the SecretManager secret version resource storing the API key. If this field is set, the apiKey field will be ignored. Format: projects/{project}/secrets/{secret}/versions/{version} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#secret_version_for_api_key GoogleDialogflowCxTool#secret_version_for_api_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0729af0f54fd03c0d8e3a91b16cb26a3bcf8a710630cbf9b235e0ca3ff375f42)
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument request_location", value=request_location, expected_type=type_hints["request_location"])
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument secret_version_for_api_key", value=secret_version_for_api_key, expected_type=type_hints["secret_version_for_api_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_name": key_name,
            "request_location": request_location,
        }
        if api_key is not None:
            self._values["api_key"] = api_key
        if secret_version_for_api_key is not None:
            self._values["secret_version_for_api_key"] = secret_version_for_api_key

    @builtins.property
    def key_name(self) -> builtins.str:
        '''The parameter name or the header name of the API key.

        E.g., If the API request is "https://example.com/act?X-Api-Key=", "X-Api-Key" would be the parameter name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#key_name GoogleDialogflowCxTool#key_name}
        '''
        result = self._values.get("key_name")
        assert result is not None, "Required property 'key_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_location(self) -> builtins.str:
        '''Key location in the request. See `RequestLocation <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#requestlocation>`_ for valid values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#request_location GoogleDialogflowCxTool#request_location}
        '''
        result = self._values.get("request_location")
        assert result is not None, "Required property 'request_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        '''Optional. The API key. If the 'secretVersionForApiKey'' field is set, this field will be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#api_key GoogleDialogflowCxTool#api_key}
        '''
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_version_for_api_key(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The name of the SecretManager secret version resource storing the API key.
        If this field is set, the apiKey field will be ignored.
        Format: projects/{project}/secrets/{secret}/versions/{version}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#secret_version_for_api_key GoogleDialogflowCxTool#secret_version_for_api_key}
        '''
        result = self._values.get("secret_version_for_api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0d5c7b13f3dd42124c062b0c84f840c5e14097af5fb88e1ee892c8507a36c97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApiKey")
    def reset_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKey", []))

    @jsii.member(jsii_name="resetSecretVersionForApiKey")
    def reset_secret_version_for_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVersionForApiKey", []))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="keyNameInput")
    def key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="requestLocationInput")
    def request_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionForApiKeyInput")
    def secret_version_for_api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionForApiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8070d54e65829bbf8cf9c799365328673dd40a744a0b5c2f846714a33727af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyName")
    def key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyName"))

    @key_name.setter
    def key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7715ecc33be80781e7927d204d6896987e209dfcf31af1f91497443965ce28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestLocation")
    def request_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestLocation"))

    @request_location.setter
    def request_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455b6d27e2e094d2447801624269441fe2d22393f63db6aa71f175ee5035fe2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersionForApiKey")
    def secret_version_for_api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersionForApiKey"))

    @secret_version_for_api_key.setter
    def secret_version_for_api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d24cf35953a8771c324d6434968b3bd053b5f8dadab0a2ea2af825f27939cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersionForApiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc463ae569e0a2ec0594fd1b5c86a194ebcabf1da9dc225a3e1f969947f0235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig",
    jsii_struct_bases=[],
    name_mapping={
        "secret_version_for_token": "secretVersionForToken",
        "token": "token",
    },
)
class GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig:
    def __init__(
        self,
        *,
        secret_version_for_token: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_version_for_token: Optional. The name of the SecretManager secret version resource storing the Bearer token. If this field is set, the 'token' field will be ignored. Format: projects/{project}/secrets/{secret}/versions/{version} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#secret_version_for_token GoogleDialogflowCxTool#secret_version_for_token}
        :param token: Optional. The text token appended to the text Bearer to the request Authorization header. `Session parameters reference <https://cloud.google.com/dialogflow/cx/docs/concept/parameter#session-ref>`_ can be used to pass the token dynamically, e.g. '$session.params.parameter-id'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#token GoogleDialogflowCxTool#token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721713aee34d9ccb0c64ddf2cd59da14bc1c3ad9c03bdab5d07aedba2387985a)
            check_type(argname="argument secret_version_for_token", value=secret_version_for_token, expected_type=type_hints["secret_version_for_token"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if secret_version_for_token is not None:
            self._values["secret_version_for_token"] = secret_version_for_token
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def secret_version_for_token(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The name of the SecretManager secret version resource storing the Bearer token. If this field is set, the 'token' field will be ignored.
        Format: projects/{project}/secrets/{secret}/versions/{version}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#secret_version_for_token GoogleDialogflowCxTool#secret_version_for_token}
        '''
        result = self._values.get("secret_version_for_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The text token appended to the text Bearer to the request Authorization header.
        `Session parameters reference <https://cloud.google.com/dialogflow/cx/docs/concept/parameter#session-ref>`_ can be used to pass the token dynamically, e.g. '$session.params.parameter-id'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#token GoogleDialogflowCxTool#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0672ca772a8520d31a6da6720cdca075e781a2918a4987d61074f5dbc504e041)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSecretVersionForToken")
    def reset_secret_version_for_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVersionForToken", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @builtins.property
    @jsii.member(jsii_name="secretVersionForTokenInput")
    def secret_version_for_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionForTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionForToken")
    def secret_version_for_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersionForToken"))

    @secret_version_for_token.setter
    def secret_version_for_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1bfb89bebfc4fe700e8c80a4893dad19a8d0627230c36a7fb84d5783b7fd46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersionForToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @token.setter
    def token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e444615e8fa1a66fcadffed5da6d7a99871fd469c4f39ef87a034e938c96cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793104b5ad89713a8cb17b3ef57e9c4837b974a3832364f1f4d1632ffa4dcc0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "oauth_grant_type": "oauthGrantType",
        "token_endpoint": "tokenEndpoint",
        "client_secret": "clientSecret",
        "scopes": "scopes",
        "secret_version_for_client_secret": "secretVersionForClientSecret",
    },
)
class GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        oauth_grant_type: builtins.str,
        token_endpoint: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_version_for_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The client ID from the OAuth provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#client_id GoogleDialogflowCxTool#client_id}
        :param oauth_grant_type: OAuth grant types. See `OauthGrantType <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#oauthgranttype>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#oauth_grant_type GoogleDialogflowCxTool#oauth_grant_type}
        :param token_endpoint: The token endpoint in the OAuth provider to exchange for an access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#token_endpoint GoogleDialogflowCxTool#token_endpoint}
        :param client_secret: Optional. The client secret from the OAuth provider. If the 'secretVersionForClientSecret' field is set, this field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#client_secret GoogleDialogflowCxTool#client_secret}
        :param scopes: Optional. The OAuth scopes to grant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#scopes GoogleDialogflowCxTool#scopes}
        :param secret_version_for_client_secret: Optional. The name of the SecretManager secret version resource storing the client secret. If this field is set, the clientSecret field will be ignored. Format: projects/{project}/secrets/{secret}/versions/{version} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#secret_version_for_client_secret GoogleDialogflowCxTool#secret_version_for_client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe330cebbe08b530547ad11eee30f27fb0d0c058cd721637b36fd2f85304348)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument oauth_grant_type", value=oauth_grant_type, expected_type=type_hints["oauth_grant_type"])
            check_type(argname="argument token_endpoint", value=token_endpoint, expected_type=type_hints["token_endpoint"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument secret_version_for_client_secret", value=secret_version_for_client_secret, expected_type=type_hints["secret_version_for_client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "oauth_grant_type": oauth_grant_type,
            "token_endpoint": token_endpoint,
        }
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if scopes is not None:
            self._values["scopes"] = scopes
        if secret_version_for_client_secret is not None:
            self._values["secret_version_for_client_secret"] = secret_version_for_client_secret

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The client ID from the OAuth provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#client_id GoogleDialogflowCxTool#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_grant_type(self) -> builtins.str:
        '''OAuth grant types. See `OauthGrantType <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#oauthgranttype>`_ for valid values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#oauth_grant_type GoogleDialogflowCxTool#oauth_grant_type}
        '''
        result = self._values.get("oauth_grant_type")
        assert result is not None, "Required property 'oauth_grant_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_endpoint(self) -> builtins.str:
        '''The token endpoint in the OAuth provider to exchange for an access token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#token_endpoint GoogleDialogflowCxTool#token_endpoint}
        '''
        result = self._values.get("token_endpoint")
        assert result is not None, "Required property 'token_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Optional. The client secret from the OAuth provider. If the 'secretVersionForClientSecret' field is set, this field will be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#client_secret GoogleDialogflowCxTool#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. The OAuth scopes to grant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#scopes GoogleDialogflowCxTool#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secret_version_for_client_secret(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The name of the SecretManager secret version resource storing the client secret.
        If this field is set, the clientSecret field will be ignored.
        Format: projects/{project}/secrets/{secret}/versions/{version}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#secret_version_for_client_secret GoogleDialogflowCxTool#secret_version_for_client_secret}
        '''
        result = self._values.get("secret_version_for_client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c85433e4ba40e3034edb799897ef9c00fd851542c494c9980e07319c0ee9fc09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @jsii.member(jsii_name="resetSecretVersionForClientSecret")
    def reset_secret_version_for_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretVersionForClientSecret", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthGrantTypeInput")
    def oauth_grant_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthGrantTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionForClientSecretInput")
    def secret_version_for_client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionForClientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenEndpointInput")
    def token_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa57b4c143df9a20d92ca7d776938ba10ad65ae668572d3f90b92949211be98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ccf5034b4bd65d5cf3bd4127775c20a1b48938aedbb16ff36ecd284a964158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthGrantType")
    def oauth_grant_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthGrantType"))

    @oauth_grant_type.setter
    def oauth_grant_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11cc1a023dee0e81debe4da76a4dacceb9f13bce3b61fe5b962d67f4834358eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthGrantType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb60fda4d31cf7ba535605338c66f05f6c98da048256533177c5be27ae6f01b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersionForClientSecret")
    def secret_version_for_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersionForClientSecret"))

    @secret_version_for_client_secret.setter
    def secret_version_for_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10187c91c262efbc63a84c2d851e39f0245235b0425de2519bd5ea21e8477a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersionForClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpoint"))

    @token_endpoint.setter
    def token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab23f730cf59b57de3f0d1434028bf0bf1185b90f5292323b46da0b2cc3490f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04728985fb908b179cba0c39583291a51faf003778a4e17df4acafa93a02ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxToolOpenApiSpecAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd05d4439f77725cb630e8252451112485fdc5ef934e4c667ee5e86b91d78251)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApiKeyConfig")
    def put_api_key_config(
        self,
        *,
        key_name: builtins.str,
        request_location: builtins.str,
        api_key: typing.Optional[builtins.str] = None,
        secret_version_for_api_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_name: The parameter name or the header name of the API key. E.g., If the API request is "https://example.com/act?X-Api-Key=", "X-Api-Key" would be the parameter name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#key_name GoogleDialogflowCxTool#key_name}
        :param request_location: Key location in the request. See `RequestLocation <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#requestlocation>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#request_location GoogleDialogflowCxTool#request_location}
        :param api_key: Optional. The API key. If the 'secretVersionForApiKey'' field is set, this field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#api_key GoogleDialogflowCxTool#api_key}
        :param secret_version_for_api_key: Optional. The name of the SecretManager secret version resource storing the API key. If this field is set, the apiKey field will be ignored. Format: projects/{project}/secrets/{secret}/versions/{version} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#secret_version_for_api_key GoogleDialogflowCxTool#secret_version_for_api_key}
        '''
        value = GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig(
            key_name=key_name,
            request_location=request_location,
            api_key=api_key,
            secret_version_for_api_key=secret_version_for_api_key,
        )

        return typing.cast(None, jsii.invoke(self, "putApiKeyConfig", [value]))

    @jsii.member(jsii_name="putBearerTokenConfig")
    def put_bearer_token_config(
        self,
        *,
        secret_version_for_token: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_version_for_token: Optional. The name of the SecretManager secret version resource storing the Bearer token. If this field is set, the 'token' field will be ignored. Format: projects/{project}/secrets/{secret}/versions/{version} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#secret_version_for_token GoogleDialogflowCxTool#secret_version_for_token}
        :param token: Optional. The text token appended to the text Bearer to the request Authorization header. `Session parameters reference <https://cloud.google.com/dialogflow/cx/docs/concept/parameter#session-ref>`_ can be used to pass the token dynamically, e.g. '$session.params.parameter-id'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#token GoogleDialogflowCxTool#token}
        '''
        value = GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig(
            secret_version_for_token=secret_version_for_token, token=token
        )

        return typing.cast(None, jsii.invoke(self, "putBearerTokenConfig", [value]))

    @jsii.member(jsii_name="putOauthConfig")
    def put_oauth_config(
        self,
        *,
        client_id: builtins.str,
        oauth_grant_type: builtins.str,
        token_endpoint: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret_version_for_client_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The client ID from the OAuth provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#client_id GoogleDialogflowCxTool#client_id}
        :param oauth_grant_type: OAuth grant types. See `OauthGrantType <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#oauthgranttype>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#oauth_grant_type GoogleDialogflowCxTool#oauth_grant_type}
        :param token_endpoint: The token endpoint in the OAuth provider to exchange for an access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#token_endpoint GoogleDialogflowCxTool#token_endpoint}
        :param client_secret: Optional. The client secret from the OAuth provider. If the 'secretVersionForClientSecret' field is set, this field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#client_secret GoogleDialogflowCxTool#client_secret}
        :param scopes: Optional. The OAuth scopes to grant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#scopes GoogleDialogflowCxTool#scopes}
        :param secret_version_for_client_secret: Optional. The name of the SecretManager secret version resource storing the client secret. If this field is set, the clientSecret field will be ignored. Format: projects/{project}/secrets/{secret}/versions/{version} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#secret_version_for_client_secret GoogleDialogflowCxTool#secret_version_for_client_secret}
        '''
        value = GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig(
            client_id=client_id,
            oauth_grant_type=oauth_grant_type,
            token_endpoint=token_endpoint,
            client_secret=client_secret,
            scopes=scopes,
            secret_version_for_client_secret=secret_version_for_client_secret,
        )

        return typing.cast(None, jsii.invoke(self, "putOauthConfig", [value]))

    @jsii.member(jsii_name="putServiceAgentAuthConfig")
    def put_service_agent_auth_config(
        self,
        *,
        service_agent_auth: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_agent_auth: Optional. Indicate the auth token type generated from the Diglogflow service agent. The generated token is sent in the Authorization header. See `ServiceAgentAuth <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#serviceagentauth>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#service_agent_auth GoogleDialogflowCxTool#service_agent_auth}
        '''
        value = GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig(
            service_agent_auth=service_agent_auth
        )

        return typing.cast(None, jsii.invoke(self, "putServiceAgentAuthConfig", [value]))

    @jsii.member(jsii_name="resetApiKeyConfig")
    def reset_api_key_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKeyConfig", []))

    @jsii.member(jsii_name="resetBearerTokenConfig")
    def reset_bearer_token_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBearerTokenConfig", []))

    @jsii.member(jsii_name="resetOauthConfig")
    def reset_oauth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthConfig", []))

    @jsii.member(jsii_name="resetServiceAgentAuthConfig")
    def reset_service_agent_auth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAgentAuthConfig", []))

    @builtins.property
    @jsii.member(jsii_name="apiKeyConfig")
    def api_key_config(
        self,
    ) -> GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfigOutputReference:
        return typing.cast(GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfigOutputReference, jsii.get(self, "apiKeyConfig"))

    @builtins.property
    @jsii.member(jsii_name="bearerTokenConfig")
    def bearer_token_config(
        self,
    ) -> GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfigOutputReference:
        return typing.cast(GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfigOutputReference, jsii.get(self, "bearerTokenConfig"))

    @builtins.property
    @jsii.member(jsii_name="oauthConfig")
    def oauth_config(
        self,
    ) -> GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfigOutputReference:
        return typing.cast(GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfigOutputReference, jsii.get(self, "oauthConfig"))

    @builtins.property
    @jsii.member(jsii_name="serviceAgentAuthConfig")
    def service_agent_auth_config(
        self,
    ) -> "GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfigOutputReference":
        return typing.cast("GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfigOutputReference", jsii.get(self, "serviceAgentAuthConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyConfigInput")
    def api_key_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig], jsii.get(self, "apiKeyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bearerTokenConfigInput")
    def bearer_token_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig], jsii.get(self, "bearerTokenConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthConfigInput")
    def oauth_config_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig], jsii.get(self, "oauthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAgentAuthConfigInput")
    def service_agent_auth_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig"], jsii.get(self, "serviceAgentAuthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthentication]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdcd0d7586c5deb09fbb7a433a5317e11812ca45a69d9a3bd6acb3d86629ae9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig",
    jsii_struct_bases=[],
    name_mapping={"service_agent_auth": "serviceAgentAuth"},
)
class GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig:
    def __init__(
        self,
        *,
        service_agent_auth: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_agent_auth: Optional. Indicate the auth token type generated from the Diglogflow service agent. The generated token is sent in the Authorization header. See `ServiceAgentAuth <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#serviceagentauth>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#service_agent_auth GoogleDialogflowCxTool#service_agent_auth}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__981865e24cb64754a43e893005d3dce748e6dd056115571d7d85e0b75d472855)
            check_type(argname="argument service_agent_auth", value=service_agent_auth, expected_type=type_hints["service_agent_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if service_agent_auth is not None:
            self._values["service_agent_auth"] = service_agent_auth

    @builtins.property
    def service_agent_auth(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Indicate the auth token type generated from the Diglogflow service agent.
        The generated token is sent in the Authorization header.
        See `ServiceAgentAuth <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#serviceagentauth>`_ for valid values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#service_agent_auth GoogleDialogflowCxTool#service_agent_auth}
        '''
        result = self._values.get("service_agent_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__621d191827c88cb22168a4e128ca303b01363e6b9eabd83310c61485949d1277)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetServiceAgentAuth")
    def reset_service_agent_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAgentAuth", []))

    @builtins.property
    @jsii.member(jsii_name="serviceAgentAuthInput")
    def service_agent_auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAgentAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAgentAuth")
    def service_agent_auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAgentAuth"))

    @service_agent_auth.setter
    def service_agent_auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1979576c8da9b9962b1624fe020e4fb1541f5b63ec18eeafc827007e2754ce46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAgentAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1c90f62f4e10b9afbbea30a2dc9f50fdbf0f049a36cfe575e4f57a202aa4e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxToolOpenApiSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e2b51d7159fed7510232e3c92f06d8b402cfee3deb1200157eec077539d72c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthentication")
    def put_authentication(
        self,
        *,
        api_key_config: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        bearer_token_config: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_config: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        service_agent_auth_config: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_key_config: api_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#api_key_config GoogleDialogflowCxTool#api_key_config}
        :param bearer_token_config: bearer_token_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#bearer_token_config GoogleDialogflowCxTool#bearer_token_config}
        :param oauth_config: oauth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#oauth_config GoogleDialogflowCxTool#oauth_config}
        :param service_agent_auth_config: service_agent_auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#service_agent_auth_config GoogleDialogflowCxTool#service_agent_auth_config}
        '''
        value = GoogleDialogflowCxToolOpenApiSpecAuthentication(
            api_key_config=api_key_config,
            bearer_token_config=bearer_token_config,
            oauth_config=oauth_config,
            service_agent_auth_config=service_agent_auth_config,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthentication", [value]))

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: The name of `Service Directory <https://cloud.google.com/service-directory/docs>`_ service. Format: projects//locations//namespaces//services/. LocationID of the service directory must be the same as the location of the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#service GoogleDialogflowCxTool#service}
        '''
        value = GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig(
            service=service
        )

        return typing.cast(None, jsii.invoke(self, "putServiceDirectoryConfig", [value]))

    @jsii.member(jsii_name="putTlsConfig")
    def put_tls_config(
        self,
        *,
        ca_certs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param ca_certs: ca_certs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#ca_certs GoogleDialogflowCxTool#ca_certs}
        '''
        value = GoogleDialogflowCxToolOpenApiSpecTlsConfig(ca_certs=ca_certs)

        return typing.cast(None, jsii.invoke(self, "putTlsConfig", [value]))

    @jsii.member(jsii_name="resetAuthentication")
    def reset_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthentication", []))

    @jsii.member(jsii_name="resetServiceDirectoryConfig")
    def reset_service_directory_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceDirectoryConfig", []))

    @jsii.member(jsii_name="resetTlsConfig")
    def reset_tls_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsConfig", []))

    @builtins.property
    @jsii.member(jsii_name="authentication")
    def authentication(
        self,
    ) -> GoogleDialogflowCxToolOpenApiSpecAuthenticationOutputReference:
        return typing.cast(GoogleDialogflowCxToolOpenApiSpecAuthenticationOutputReference, jsii.get(self, "authentication"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfigOutputReference":
        return typing.cast("GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="tlsConfig")
    def tls_config(self) -> "GoogleDialogflowCxToolOpenApiSpecTlsConfigOutputReference":
        return typing.cast("GoogleDialogflowCxToolOpenApiSpecTlsConfigOutputReference", jsii.get(self, "tlsConfig"))

    @builtins.property
    @jsii.member(jsii_name="authenticationInput")
    def authentication_input(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthentication]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthentication], jsii.get(self, "authenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfigInput")
    def service_directory_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="textSchemaInput")
    def text_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsConfigInput")
    def tls_config_input(
        self,
    ) -> typing.Optional["GoogleDialogflowCxToolOpenApiSpecTlsConfig"]:
        return typing.cast(typing.Optional["GoogleDialogflowCxToolOpenApiSpecTlsConfig"], jsii.get(self, "tlsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="textSchema")
    def text_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "textSchema"))

    @text_schema.setter
    def text_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61d42c15f366d48900d69baf35afd1427aa5510fb6f5ea674012b8459404c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDialogflowCxToolOpenApiSpec]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolOpenApiSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxToolOpenApiSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5750551ef0542b23596e0811d29ac2d051082e50306c49253e95d42ed6866869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: The name of `Service Directory <https://cloud.google.com/service-directory/docs>`_ service. Format: projects//locations//namespaces//services/. LocationID of the service directory must be the same as the location of the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#service GoogleDialogflowCxTool#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c651253ba09247b15b358dad1b342e086ff5ac9c1c099b381181da58fdf818d0)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''The name of `Service Directory <https://cloud.google.com/service-directory/docs>`_ service. Format: projects//locations//namespaces//services/. LocationID of the service directory must be the same as the location of the agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#service GoogleDialogflowCxTool#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d12709b83057663088e0e23c1eb147434bbec6bf5c786f12e972dd662edad470)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd3836d315c43c53f1914909b2aeffea9d803939b2fd1ff545c6e24631bf06fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b68272f2aff0d0f9a2a50576c27b6d2c297a0bcdf8dc804a6500b2182a25e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecTlsConfig",
    jsii_struct_bases=[],
    name_mapping={"ca_certs": "caCerts"},
)
class GoogleDialogflowCxToolOpenApiSpecTlsConfig:
    def __init__(
        self,
        *,
        ca_certs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param ca_certs: ca_certs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#ca_certs GoogleDialogflowCxTool#ca_certs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935d3cccb8fa278c2d1c05fc0a13293c9010f4027aa6acfd2645fa57c090bee4)
            check_type(argname="argument ca_certs", value=ca_certs, expected_type=type_hints["ca_certs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ca_certs": ca_certs,
        }

    @builtins.property
    def ca_certs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts"]]:
        '''ca_certs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#ca_certs GoogleDialogflowCxTool#ca_certs}
        '''
        result = self._values.get("ca_certs")
        assert result is not None, "Required property 'ca_certs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolOpenApiSpecTlsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts",
    jsii_struct_bases=[],
    name_mapping={"cert": "cert", "display_name": "displayName"},
)
class GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts:
    def __init__(self, *, cert: builtins.str, display_name: builtins.str) -> None:
        '''
        :param cert: The allowed custom CA certificates (in DER format) for HTTPS verification. This overrides the default SSL trust store. If this is empty or unspecified, Dialogflow will use Google's default trust store to verify certificates. N.B. Make sure the HTTPS server certificates are signed with "subject alt name". For instance a certificate can be self-signed using the following command:: openssl x509 -req -days 200 -in example.com.csr \\ -signkey example.com.key \\ -out example.com.crt \\ -extfile <(printf "\\nsubjectAltName='DNS:www.example.com'") A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#cert GoogleDialogflowCxTool#cert}
        :param display_name: The name of the allowed custom CA certificates. This can be used to disambiguate the custom CA certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#display_name GoogleDialogflowCxTool#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2de2e459c596b4b2d0a8f30300d1356bcb12ce978c04c85e6b1b291f9c339a4)
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cert": cert,
            "display_name": display_name,
        }

    @builtins.property
    def cert(self) -> builtins.str:
        '''The allowed custom CA certificates (in DER format) for HTTPS verification.

        This overrides the default SSL trust store.
        If this is empty or unspecified, Dialogflow will use Google's default trust store to verify certificates.
        N.B. Make sure the HTTPS server certificates are signed with "subject alt name".
        For instance a certificate can be self-signed using the following command::

             openssl x509 -req -days 200 -in example.com.csr \\
               -signkey example.com.key \\
               -out example.com.crt \\
               -extfile <(printf "\\nsubjectAltName='DNS:www.example.com'")

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#cert GoogleDialogflowCxTool#cert}
        '''
        result = self._values.get("cert")
        assert result is not None, "Required property 'cert' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The name of the allowed custom CA certificates. This can be used to disambiguate the custom CA certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#display_name GoogleDialogflowCxTool#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCertsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCertsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d18e6cd563433000926daa4d5449fdd94ec1ec4eb228f1d501f2dca3fec92cdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCertsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca179b56d31854f0d55ccaa331338d235836d2562550851a2f181ca8364c078b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCertsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1722269560cc46332649e1a5791ca35690f54be70dcd983634c3bb7a81173f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fe019efcc00866a20f87accb9bc336063938f09d7dd00d8bcb975e8e1e76615)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21416a6ee26d99028b69c208f689fb171103705d718ef1fd51a6880b07f1286d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d2e658d5419191d7d6a0ad55cec7ec8500ffad097dd902f104f752d5493810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCertsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCertsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a21abc10a7a960b4fb9611922df25a0863c59d491de0d21ba4934756071590ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="certInput")
    def cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cert"))

    @cert.setter
    def cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327902525446e86306a145b10e91ec45b6df4322c7625387aee28a22bcb515a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913f7245b05d4125a935a7fab9cbfef8e6ab8d616be053e44d8cc8e8a372c117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b06fd7add0c9dc5e943049e531127742aea940db2a3d3bc112d5f6dc6b40f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDialogflowCxToolOpenApiSpecTlsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolOpenApiSpecTlsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f5f48cb34e742d3096a31fe5c7a0ad368b61b8dab4efcf6b5c227d8eea2472b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCaCerts")
    def put_ca_certs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd66bad3200a9972795bd4f05ce88f989e5fc83384f7409b40f01a3daecae76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCaCerts", [value]))

    @builtins.property
    @jsii.member(jsii_name="caCerts")
    def ca_certs(self) -> GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCertsList:
        return typing.cast(GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCertsList, jsii.get(self, "caCerts"))

    @builtins.property
    @jsii.member(jsii_name="caCertsInput")
    def ca_certs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts]]], jsii.get(self, "caCertsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDialogflowCxToolOpenApiSpecTlsConfig]:
        return typing.cast(typing.Optional[GoogleDialogflowCxToolOpenApiSpecTlsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecTlsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407c12e883d45fad8bb510f62c22604741c05264d3311d4e1de8d90c3a83fa44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDialogflowCxToolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#create GoogleDialogflowCxTool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#delete GoogleDialogflowCxTool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#update GoogleDialogflowCxTool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c99a40866197a29bec99d8827d8565bc555560a9b528de1a29d152e8ffd219c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#create GoogleDialogflowCxTool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#delete GoogleDialogflowCxTool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.42.0/docs/resources/google_dialogflow_cx_tool#update GoogleDialogflowCxTool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDialogflowCxToolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDialogflowCxToolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDialogflowCxTool.GoogleDialogflowCxToolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51760a0424714112b63d5b5f1b04ed8fd53124aea6a42ccabcfa763572021041)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2c0fa169d2d1f58079697d702d9ffdc715e5882e9efaa17bc774851d75d8f9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6560c7962e3ccc5603509ea40604bdcc4a8eb03f3b57d13a4f07f991bb70dc5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5773c4484501474596521e13687c39604ae2862bffe9d84f83119218ffc000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxToolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxToolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxToolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e770459f3db8a7269f90980370672d954dccf1c2ad4fa77e5cd7964900f44a17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDialogflowCxTool",
    "GoogleDialogflowCxToolConfig",
    "GoogleDialogflowCxToolDataStoreSpec",
    "GoogleDialogflowCxToolDataStoreSpecDataStoreConnections",
    "GoogleDialogflowCxToolDataStoreSpecDataStoreConnectionsList",
    "GoogleDialogflowCxToolDataStoreSpecDataStoreConnectionsOutputReference",
    "GoogleDialogflowCxToolDataStoreSpecFallbackPrompt",
    "GoogleDialogflowCxToolDataStoreSpecFallbackPromptOutputReference",
    "GoogleDialogflowCxToolDataStoreSpecOutputReference",
    "GoogleDialogflowCxToolFunctionSpec",
    "GoogleDialogflowCxToolFunctionSpecOutputReference",
    "GoogleDialogflowCxToolOpenApiSpec",
    "GoogleDialogflowCxToolOpenApiSpecAuthentication",
    "GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig",
    "GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfigOutputReference",
    "GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig",
    "GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfigOutputReference",
    "GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig",
    "GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfigOutputReference",
    "GoogleDialogflowCxToolOpenApiSpecAuthenticationOutputReference",
    "GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig",
    "GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfigOutputReference",
    "GoogleDialogflowCxToolOpenApiSpecOutputReference",
    "GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig",
    "GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfigOutputReference",
    "GoogleDialogflowCxToolOpenApiSpecTlsConfig",
    "GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts",
    "GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCertsList",
    "GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCertsOutputReference",
    "GoogleDialogflowCxToolOpenApiSpecTlsConfigOutputReference",
    "GoogleDialogflowCxToolTimeouts",
    "GoogleDialogflowCxToolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d15d805081d9c45d88022969c7cf246c4c3c20e7944162b6d44eed662ecdd531(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    description: builtins.str,
    display_name: builtins.str,
    data_store_spec: typing.Optional[typing.Union[GoogleDialogflowCxToolDataStoreSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    function_spec: typing.Optional[typing.Union[GoogleDialogflowCxToolFunctionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    open_api_spec: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowCxToolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3525e3b1e74271de92292453cbf3e7823059ffc6088cd38d22f7cfeef7d4b9cf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c30947b1e94f2aa0cee2586274f21e9547da2a1701f04bfae56c508df3d866(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2972b439d1eb4dce828ddf41c1a2cad2301796cb246da9306299f8288029300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d92eb76c71c62cfbc544b6d7f4ea4b458964a5b1bc001bc603cf1507db88b7ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f808f2839f05bb8f8c176013b7175cb6747160fc8eb6ae5ee658d147d085dd85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a1e710a050333000e7b3ffa3af2d6edc8bf5ddea3c13490edc3b1bb01cad3b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: builtins.str,
    display_name: builtins.str,
    data_store_spec: typing.Optional[typing.Union[GoogleDialogflowCxToolDataStoreSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    function_spec: typing.Optional[typing.Union[GoogleDialogflowCxToolFunctionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    open_api_spec: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDialogflowCxToolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9be93ab35fd4535bb1706741a32c35d7577a2849629adf7425501d5ad0e6ea3(
    *,
    data_store_connections: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxToolDataStoreSpecDataStoreConnections, typing.Dict[builtins.str, typing.Any]]]],
    fallback_prompt: typing.Union[GoogleDialogflowCxToolDataStoreSpecFallbackPrompt, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a493cb8a63c887c9c40d6ded239ce5939f0ad817d6cb1be3712846c3f0847de(
    *,
    data_store: typing.Optional[builtins.str] = None,
    data_store_type: typing.Optional[builtins.str] = None,
    document_processing_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a6c34edf65e023a50f3a51cd4444ddb5407ec65c7edc7e977619f717cc7f7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be74758044c705ce12263d417af5bceb7672047a07d41c6f4cc5ac9ed08628ee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c990cfc09d2f8106827a42954ba0108af1159227ab2154090db90405f00b1867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6891715c158ac7febca84778e92ca78ed0f87a202b137f547fbb06058e7b2524(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74552165f2b99ede3991eb03b1cd9f9a74bbcd34abe00961ffdb172b27b73a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362a885f97dc2e36b072740420e2a849e11369f0d995c38350bd2c077f7cdd70(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxToolDataStoreSpecDataStoreConnections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842f0577f1a68784bede3cfd237cf61c19b8b8cd9b78c02c94ae514292934a05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4c9a94b15b84d4c4b12e06508ffc14ef5fd978927370e23f39ffa6ace68801(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a720d1ecbe69e4151c7f2acfbd0ed4352651dc1de3744111f18254e8624328e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d00c999e4c1bc8394973dc45561d24a6bf4ec6d18d3721b1e43e9f8ad47817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d84147deaef834c6ed2eb201e8a6bed72136079909f7371fc5ff4c705ee7ba1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxToolDataStoreSpecDataStoreConnections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff193dfc2e77989b2034c54b2a24bfbdfff8efb2a461a1397981ab131809aba2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46332e64eac97cac9222c77aba11755c50cd8c7d3b9684a810599a19da387ebf(
    value: typing.Optional[GoogleDialogflowCxToolDataStoreSpecFallbackPrompt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969cf064b190093c58466c0583e5f8a45d46cf48d91e2b805c5b445762434c1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d3b10f26231a90deead0e6ec505e1d9a43dfaa950ad6a18ebf9479fb98fc78(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxToolDataStoreSpecDataStoreConnections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6f91aaf06b490c5f406d9aa6d24c73958560bbce1d61b4d9c05019d62eb013(
    value: typing.Optional[GoogleDialogflowCxToolDataStoreSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52eb615b90f04e8f5ac08fa8585f8815ab5c7737d21b6a500fd71bac701952e2(
    *,
    input_schema: typing.Optional[builtins.str] = None,
    output_schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec6e1201233b8fd9bbacf0588b0d73ffdcb28b5ae33c72f63d687e8f1987625(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19274c7bd4c5b03aafdaf7babe185981910802211f0f035229754467c22f868e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5221c6446a380b42e27abedf082b91fedc91161077e79fe142be7caf7d34e39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2caa6dac16c044d03d62516186122ba6afc4be002a7151e2ab0d9a643d258650(
    value: typing.Optional[GoogleDialogflowCxToolFunctionSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d3468afb071c3e661fd19251e70ba9c118e26fb384757b4aa9f3c895a7758c(
    *,
    text_schema: builtins.str,
    authentication: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpecAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    service_directory_config: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_config: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpecTlsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300ed473d4605c2cbb752bca95a5cdced3b8e717ca3fe5c5a51a103788642d69(
    *,
    api_key_config: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bearer_token_config: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth_config: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    service_agent_auth_config: typing.Optional[typing.Union[GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0729af0f54fd03c0d8e3a91b16cb26a3bcf8a710630cbf9b235e0ca3ff375f42(
    *,
    key_name: builtins.str,
    request_location: builtins.str,
    api_key: typing.Optional[builtins.str] = None,
    secret_version_for_api_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d5c7b13f3dd42124c062b0c84f840c5e14097af5fb88e1ee892c8507a36c97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8070d54e65829bbf8cf9c799365328673dd40a744a0b5c2f846714a33727af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7715ecc33be80781e7927d204d6896987e209dfcf31af1f91497443965ce28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455b6d27e2e094d2447801624269441fe2d22393f63db6aa71f175ee5035fe2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d24cf35953a8771c324d6434968b3bd053b5f8dadab0a2ea2af825f27939cf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc463ae569e0a2ec0594fd1b5c86a194ebcabf1da9dc225a3e1f969947f0235(
    value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721713aee34d9ccb0c64ddf2cd59da14bc1c3ad9c03bdab5d07aedba2387985a(
    *,
    secret_version_for_token: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0672ca772a8520d31a6da6720cdca075e781a2918a4987d61074f5dbc504e041(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1bfb89bebfc4fe700e8c80a4893dad19a8d0627230c36a7fb84d5783b7fd46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e444615e8fa1a66fcadffed5da6d7a99871fd469c4f39ef87a034e938c96cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793104b5ad89713a8cb17b3ef57e9c4837b974a3832364f1f4d1632ffa4dcc0d(
    value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe330cebbe08b530547ad11eee30f27fb0d0c058cd721637b36fd2f85304348(
    *,
    client_id: builtins.str,
    oauth_grant_type: builtins.str,
    token_endpoint: builtins.str,
    client_secret: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_version_for_client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85433e4ba40e3034edb799897ef9c00fd851542c494c9980e07319c0ee9fc09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa57b4c143df9a20d92ca7d776938ba10ad65ae668572d3f90b92949211be98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ccf5034b4bd65d5cf3bd4127775c20a1b48938aedbb16ff36ecd284a964158(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11cc1a023dee0e81debe4da76a4dacceb9f13bce3b61fe5b962d67f4834358eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb60fda4d31cf7ba535605338c66f05f6c98da048256533177c5be27ae6f01b3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10187c91c262efbc63a84c2d851e39f0245235b0425de2519bd5ea21e8477a8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab23f730cf59b57de3f0d1434028bf0bf1185b90f5292323b46da0b2cc3490f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04728985fb908b179cba0c39583291a51faf003778a4e17df4acafa93a02ca8(
    value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationOauthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd05d4439f77725cb630e8252451112485fdc5ef934e4c667ee5e86b91d78251(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdcd0d7586c5deb09fbb7a433a5317e11812ca45a69d9a3bd6acb3d86629ae9f(
    value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981865e24cb64754a43e893005d3dce748e6dd056115571d7d85e0b75d472855(
    *,
    service_agent_auth: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621d191827c88cb22168a4e128ca303b01363e6b9eabd83310c61485949d1277(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1979576c8da9b9962b1624fe020e4fb1541f5b63ec18eeafc827007e2754ce46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1c90f62f4e10b9afbbea30a2dc9f50fdbf0f049a36cfe575e4f57a202aa4e8(
    value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2b51d7159fed7510232e3c92f06d8b402cfee3deb1200157eec077539d72c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61d42c15f366d48900d69baf35afd1427aa5510fb6f5ea674012b8459404c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5750551ef0542b23596e0811d29ac2d051082e50306c49253e95d42ed6866869(
    value: typing.Optional[GoogleDialogflowCxToolOpenApiSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c651253ba09247b15b358dad1b342e086ff5ac9c1c099b381181da58fdf818d0(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12709b83057663088e0e23c1eb147434bbec6bf5c786f12e972dd662edad470(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd3836d315c43c53f1914909b2aeffea9d803939b2fd1ff545c6e24631bf06fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b68272f2aff0d0f9a2a50576c27b6d2c297a0bcdf8dc804a6500b2182a25e8(
    value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935d3cccb8fa278c2d1c05fc0a13293c9010f4027aa6acfd2645fa57c090bee4(
    *,
    ca_certs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2de2e459c596b4b2d0a8f30300d1356bcb12ce978c04c85e6b1b291f9c339a4(
    *,
    cert: builtins.str,
    display_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18e6cd563433000926daa4d5449fdd94ec1ec4eb228f1d501f2dca3fec92cdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca179b56d31854f0d55ccaa331338d235836d2562550851a2f181ca8364c078b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1722269560cc46332649e1a5791ca35690f54be70dcd983634c3bb7a81173f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe019efcc00866a20f87accb9bc336063938f09d7dd00d8bcb975e8e1e76615(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21416a6ee26d99028b69c208f689fb171103705d718ef1fd51a6880b07f1286d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d2e658d5419191d7d6a0ad55cec7ec8500ffad097dd902f104f752d5493810(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21abc10a7a960b4fb9611922df25a0863c59d491de0d21ba4934756071590ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327902525446e86306a145b10e91ec45b6df4322c7625387aee28a22bcb515a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913f7245b05d4125a935a7fab9cbfef8e6ab8d616be053e44d8cc8e8a372c117(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b06fd7add0c9dc5e943049e531127742aea940db2a3d3bc112d5f6dc6b40f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5f48cb34e742d3096a31fe5c7a0ad368b61b8dab4efcf6b5c227d8eea2472b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd66bad3200a9972795bd4f05ce88f989e5fc83384f7409b40f01a3daecae76(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDialogflowCxToolOpenApiSpecTlsConfigCaCerts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407c12e883d45fad8bb510f62c22604741c05264d3311d4e1de8d90c3a83fa44(
    value: typing.Optional[GoogleDialogflowCxToolOpenApiSpecTlsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c99a40866197a29bec99d8827d8565bc555560a9b528de1a29d152e8ffd219c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51760a0424714112b63d5b5f1b04ed8fd53124aea6a42ccabcfa763572021041(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c0fa169d2d1f58079697d702d9ffdc715e5882e9efaa17bc774851d75d8f9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6560c7962e3ccc5603509ea40604bdcc4a8eb03f3b57d13a4f07f991bb70dc5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5773c4484501474596521e13687c39604ae2862bffe9d84f83119218ffc000(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e770459f3db8a7269f90980370672d954dccf1c2ad4fa77e5cd7964900f44a17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDialogflowCxToolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
