r'''
# `google_dialogflow_cx_tool`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_tool`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool).
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


class DialogflowCxTool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxTool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool google_dialogflow_cx_tool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        description: builtins.str,
        display_name: builtins.str,
        data_store_spec: typing.Optional[typing.Union["DialogflowCxToolDataStoreSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        function_spec: typing.Optional[typing.Union["DialogflowCxToolFunctionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        open_api_spec: typing.Optional[typing.Union["DialogflowCxToolOpenApiSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxToolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool google_dialogflow_cx_tool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: High level description of the Tool and its usage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#description DialogflowCxTool#description}
        :param display_name: The human-readable name of the tool, unique within the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#display_name DialogflowCxTool#display_name}
        :param data_store_spec: data_store_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#data_store_spec DialogflowCxTool#data_store_spec}
        :param function_spec: function_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#function_spec DialogflowCxTool#function_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#id DialogflowCxTool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param open_api_spec: open_api_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#open_api_spec DialogflowCxTool#open_api_spec}
        :param parent: The agent to create a Tool for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#parent DialogflowCxTool#parent}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#timeouts DialogflowCxTool#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37a21657ba01f827dd1fe503f075ddfa8e3bcc55017aa25488225cda6d953d2a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DialogflowCxToolConfig(
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
        '''Generates CDKTF code for importing a DialogflowCxTool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DialogflowCxTool to import.
        :param import_from_id: The id of the existing DialogflowCxTool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DialogflowCxTool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd6987e0bc7062a9e00dd0ee4d3e5b31abeec21fd49b9de56db8057d8ca84509)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataStoreSpec")
    def put_data_store_spec(
        self,
        *,
        data_store_connections: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxToolDataStoreSpecDataStoreConnections", typing.Dict[builtins.str, typing.Any]]]],
        fallback_prompt: typing.Union["DialogflowCxToolDataStoreSpecFallbackPrompt", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param data_store_connections: data_store_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#data_store_connections DialogflowCxTool#data_store_connections}
        :param fallback_prompt: fallback_prompt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#fallback_prompt DialogflowCxTool#fallback_prompt}
        '''
        value = DialogflowCxToolDataStoreSpec(
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
        :param input_schema: Optional. The JSON schema is encapsulated in a `google.protobuf.Struct <https://protobuf.dev/reference/protobuf/google.protobuf/#struct>`_ to describe the input of the function. This input is a JSON object that contains the function's parameters as properties of the object Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#input_schema DialogflowCxTool#input_schema}
        :param output_schema: Optional. The JSON schema is encapsulated in a `google.protobuf.Struct <https://protobuf.dev/reference/protobuf/google.protobuf/#struct>`_ to describe the output of the function. This output is a JSON object that contains the function's parameters as properties of the object Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#output_schema DialogflowCxTool#output_schema}
        '''
        value = DialogflowCxToolFunctionSpec(
            input_schema=input_schema, output_schema=output_schema
        )

        return typing.cast(None, jsii.invoke(self, "putFunctionSpec", [value]))

    @jsii.member(jsii_name="putOpenApiSpec")
    def put_open_api_spec(
        self,
        *,
        text_schema: builtins.str,
        authentication: typing.Optional[typing.Union["DialogflowCxToolOpenApiSpecAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        service_directory_config: typing.Optional[typing.Union["DialogflowCxToolOpenApiSpecServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_config: typing.Optional[typing.Union["DialogflowCxToolOpenApiSpecTlsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param text_schema: The OpenAPI schema specified as a text. This field is part of a union field 'schema': only one of 'textSchema' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#text_schema DialogflowCxTool#text_schema}
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#authentication DialogflowCxTool#authentication}
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#service_directory_config DialogflowCxTool#service_directory_config}
        :param tls_config: tls_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#tls_config DialogflowCxTool#tls_config}
        '''
        value = DialogflowCxToolOpenApiSpec(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#create DialogflowCxTool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#delete DialogflowCxTool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#update DialogflowCxTool#update}.
        '''
        value = DialogflowCxToolTimeouts(create=create, delete=delete, update=update)

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
    def data_store_spec(self) -> "DialogflowCxToolDataStoreSpecOutputReference":
        return typing.cast("DialogflowCxToolDataStoreSpecOutputReference", jsii.get(self, "dataStoreSpec"))

    @builtins.property
    @jsii.member(jsii_name="functionSpec")
    def function_spec(self) -> "DialogflowCxToolFunctionSpecOutputReference":
        return typing.cast("DialogflowCxToolFunctionSpecOutputReference", jsii.get(self, "functionSpec"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="openApiSpec")
    def open_api_spec(self) -> "DialogflowCxToolOpenApiSpecOutputReference":
        return typing.cast("DialogflowCxToolOpenApiSpecOutputReference", jsii.get(self, "openApiSpec"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DialogflowCxToolTimeoutsOutputReference":
        return typing.cast("DialogflowCxToolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="toolType")
    def tool_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "toolType"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreSpecInput")
    def data_store_spec_input(self) -> typing.Optional["DialogflowCxToolDataStoreSpec"]:
        return typing.cast(typing.Optional["DialogflowCxToolDataStoreSpec"], jsii.get(self, "dataStoreSpecInput"))

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
    def function_spec_input(self) -> typing.Optional["DialogflowCxToolFunctionSpec"]:
        return typing.cast(typing.Optional["DialogflowCxToolFunctionSpec"], jsii.get(self, "functionSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="openApiSpecInput")
    def open_api_spec_input(self) -> typing.Optional["DialogflowCxToolOpenApiSpec"]:
        return typing.cast(typing.Optional["DialogflowCxToolOpenApiSpec"], jsii.get(self, "openApiSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxToolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxToolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b1ebb453fc0303647abdd0a69ee9ce5488dca2c1ba820a416dbbba30d17a272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d24f339f01b0192b9438107f3c11025e86adca765131e1c1854fd83f4ec60c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d2d8cad2940bc61ab1e6078f445ff21fe17b363ab03ae18c4ee1052cb0074e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40356e252e6bceb172d7c130eaabe55a11a6b2d13fbf582284d1e1fe42a7851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolConfig",
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
class DialogflowCxToolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_store_spec: typing.Optional[typing.Union["DialogflowCxToolDataStoreSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        function_spec: typing.Optional[typing.Union["DialogflowCxToolFunctionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        open_api_spec: typing.Optional[typing.Union["DialogflowCxToolOpenApiSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxToolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param description: High level description of the Tool and its usage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#description DialogflowCxTool#description}
        :param display_name: The human-readable name of the tool, unique within the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#display_name DialogflowCxTool#display_name}
        :param data_store_spec: data_store_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#data_store_spec DialogflowCxTool#data_store_spec}
        :param function_spec: function_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#function_spec DialogflowCxTool#function_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#id DialogflowCxTool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param open_api_spec: open_api_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#open_api_spec DialogflowCxTool#open_api_spec}
        :param parent: The agent to create a Tool for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#parent DialogflowCxTool#parent}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#timeouts DialogflowCxTool#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_store_spec, dict):
            data_store_spec = DialogflowCxToolDataStoreSpec(**data_store_spec)
        if isinstance(function_spec, dict):
            function_spec = DialogflowCxToolFunctionSpec(**function_spec)
        if isinstance(open_api_spec, dict):
            open_api_spec = DialogflowCxToolOpenApiSpec(**open_api_spec)
        if isinstance(timeouts, dict):
            timeouts = DialogflowCxToolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b1cc35f61a32d5de1e6820e7fa4c12fc1b097b0d4a4f2190c456f9606dfba3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#description DialogflowCxTool#description}
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The human-readable name of the tool, unique within the agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#display_name DialogflowCxTool#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_store_spec(self) -> typing.Optional["DialogflowCxToolDataStoreSpec"]:
        '''data_store_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#data_store_spec DialogflowCxTool#data_store_spec}
        '''
        result = self._values.get("data_store_spec")
        return typing.cast(typing.Optional["DialogflowCxToolDataStoreSpec"], result)

    @builtins.property
    def function_spec(self) -> typing.Optional["DialogflowCxToolFunctionSpec"]:
        '''function_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#function_spec DialogflowCxTool#function_spec}
        '''
        result = self._values.get("function_spec")
        return typing.cast(typing.Optional["DialogflowCxToolFunctionSpec"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#id DialogflowCxTool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_api_spec(self) -> typing.Optional["DialogflowCxToolOpenApiSpec"]:
        '''open_api_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#open_api_spec DialogflowCxTool#open_api_spec}
        '''
        result = self._values.get("open_api_spec")
        return typing.cast(typing.Optional["DialogflowCxToolOpenApiSpec"], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The agent to create a Tool for. Format: projects//locations//agents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#parent DialogflowCxTool#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DialogflowCxToolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#timeouts DialogflowCxTool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DialogflowCxToolTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolDataStoreSpec",
    jsii_struct_bases=[],
    name_mapping={
        "data_store_connections": "dataStoreConnections",
        "fallback_prompt": "fallbackPrompt",
    },
)
class DialogflowCxToolDataStoreSpec:
    def __init__(
        self,
        *,
        data_store_connections: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxToolDataStoreSpecDataStoreConnections", typing.Dict[builtins.str, typing.Any]]]],
        fallback_prompt: typing.Union["DialogflowCxToolDataStoreSpecFallbackPrompt", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param data_store_connections: data_store_connections block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#data_store_connections DialogflowCxTool#data_store_connections}
        :param fallback_prompt: fallback_prompt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#fallback_prompt DialogflowCxTool#fallback_prompt}
        '''
        if isinstance(fallback_prompt, dict):
            fallback_prompt = DialogflowCxToolDataStoreSpecFallbackPrompt(**fallback_prompt)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de56bff96c9265784f082aad7ab81ea6e761ddc263ffb60cd24ae440f8ca636)
            check_type(argname="argument data_store_connections", value=data_store_connections, expected_type=type_hints["data_store_connections"])
            check_type(argname="argument fallback_prompt", value=fallback_prompt, expected_type=type_hints["fallback_prompt"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_store_connections": data_store_connections,
            "fallback_prompt": fallback_prompt,
        }

    @builtins.property
    def data_store_connections(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxToolDataStoreSpecDataStoreConnections"]]:
        '''data_store_connections block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#data_store_connections DialogflowCxTool#data_store_connections}
        '''
        result = self._values.get("data_store_connections")
        assert result is not None, "Required property 'data_store_connections' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxToolDataStoreSpecDataStoreConnections"]], result)

    @builtins.property
    def fallback_prompt(self) -> "DialogflowCxToolDataStoreSpecFallbackPrompt":
        '''fallback_prompt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#fallback_prompt DialogflowCxTool#fallback_prompt}
        '''
        result = self._values.get("fallback_prompt")
        assert result is not None, "Required property 'fallback_prompt' is missing"
        return typing.cast("DialogflowCxToolDataStoreSpecFallbackPrompt", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolDataStoreSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolDataStoreSpecDataStoreConnections",
    jsii_struct_bases=[],
    name_mapping={
        "data_store": "dataStore",
        "data_store_type": "dataStoreType",
        "document_processing_mode": "documentProcessingMode",
    },
)
class DialogflowCxToolDataStoreSpecDataStoreConnections:
    def __init__(
        self,
        *,
        data_store: typing.Optional[builtins.str] = None,
        data_store_type: typing.Optional[builtins.str] = None,
        document_processing_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_store: The full name of the referenced data store. Formats: projects/{project}/locations/{location}/collections/{collection}/dataStores/{dataStore} projects/{project}/locations/{location}/dataStores/{dataStore}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#data_store DialogflowCxTool#data_store}
        :param data_store_type: The type of the connected data store. See `DataStoreType <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/DataStoreConnection#datastoretype>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#data_store_type DialogflowCxTool#data_store_type}
        :param document_processing_mode: The document processing mode for the data store connection. Should only be set for PUBLIC_WEB and UNSTRUCTURED data stores. If not set it is considered as DOCUMENTS, as this is the legacy mode. See `DocumentProcessingMode <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/DataStoreConnection#documentprocessingmode>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#document_processing_mode DialogflowCxTool#document_processing_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9171c236bde00f3d4eaeff77413324aa534de7aa5d2982f20c087e8f99b9f16e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#data_store DialogflowCxTool#data_store}
        '''
        result = self._values.get("data_store")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_store_type(self) -> typing.Optional[builtins.str]:
        '''The type of the connected data store. See `DataStoreType <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/DataStoreConnection#datastoretype>`_ for valid values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#data_store_type DialogflowCxTool#data_store_type}
        '''
        result = self._values.get("data_store_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_processing_mode(self) -> typing.Optional[builtins.str]:
        '''The document processing mode for the data store connection.

        Should only be set for PUBLIC_WEB and UNSTRUCTURED data stores. If not set it is considered as DOCUMENTS, as this is the legacy mode.
        See `DocumentProcessingMode <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/DataStoreConnection#documentprocessingmode>`_ for valid values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#document_processing_mode DialogflowCxTool#document_processing_mode}
        '''
        result = self._values.get("document_processing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolDataStoreSpecDataStoreConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxToolDataStoreSpecDataStoreConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolDataStoreSpecDataStoreConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07a35f911287dc3b190157c231b1695305d6df4fda7372cb7184a562c1963585)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxToolDataStoreSpecDataStoreConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a12c37b10bcb872e30a1ad7224ce461ab28a894c65774cc0072c6bdb0b26b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxToolDataStoreSpecDataStoreConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f78cd2247275695bb97fc5a4ad71b5351ac060cfccbaa84f79b962a5bde359c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4291764700c5a8d0cae9a4adbbf5c854ce1e80611b047818b15261b9874905c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87a5a0327af8dde55cab294e96b672b0ff6e35469416cebc3050ddffdbdfb39c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxToolDataStoreSpecDataStoreConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxToolDataStoreSpecDataStoreConnections]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxToolDataStoreSpecDataStoreConnections]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8275918f6375f533c18ad0091bc64c8a836ad62143afa0147051a6044a233131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxToolDataStoreSpecDataStoreConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolDataStoreSpecDataStoreConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ac68aba90c84d39fd40b6ef13a8b5826f9a404ce305a4477e8b3d20a1ebcc51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a427c5108066fcbad6b5f22c1ec298c3d166dcb8694b8b83a11d5c4f91778c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStoreType")
    def data_store_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataStoreType"))

    @data_store_type.setter
    def data_store_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65fe041c7fabd6f3ae4a4cc81221bc90440015b741394406d0eb1377a5b34dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStoreType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentProcessingMode")
    def document_processing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentProcessingMode"))

    @document_processing_mode.setter
    def document_processing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23f3ad73076400aea3d6e5e68e6f25384e35a1506d93d0115e4084c80dc4fdf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentProcessingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxToolDataStoreSpecDataStoreConnections]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxToolDataStoreSpecDataStoreConnections]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxToolDataStoreSpecDataStoreConnections]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b0e3a858a3a00e9b44d71394170d915a151cb0d417754bd9c89f0db4de3e1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolDataStoreSpecFallbackPrompt",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowCxToolDataStoreSpecFallbackPrompt:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolDataStoreSpecFallbackPrompt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxToolDataStoreSpecFallbackPromptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolDataStoreSpecFallbackPromptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a34424646a4aff1251b844552bb751a06c35e138294c936d7b98c651a4db135)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxToolDataStoreSpecFallbackPrompt]:
        return typing.cast(typing.Optional[DialogflowCxToolDataStoreSpecFallbackPrompt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxToolDataStoreSpecFallbackPrompt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d94fd1bce5a5e1f5cd8eb8577ac2b014d8f798122eb0e391ff2e5acb25beadcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxToolDataStoreSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolDataStoreSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e245d8af5b7be73768ae082f7c9e0492f07881c76f4556078f23fb81ffac9a70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataStoreConnections")
    def put_data_store_connections(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxToolDataStoreSpecDataStoreConnections, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09c0160ea8feaf3aa0f9697a867440327a9c518d3a998a5039b81248cd73f05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataStoreConnections", [value]))

    @jsii.member(jsii_name="putFallbackPrompt")
    def put_fallback_prompt(self) -> None:
        value = DialogflowCxToolDataStoreSpecFallbackPrompt()

        return typing.cast(None, jsii.invoke(self, "putFallbackPrompt", [value]))

    @builtins.property
    @jsii.member(jsii_name="dataStoreConnections")
    def data_store_connections(
        self,
    ) -> DialogflowCxToolDataStoreSpecDataStoreConnectionsList:
        return typing.cast(DialogflowCxToolDataStoreSpecDataStoreConnectionsList, jsii.get(self, "dataStoreConnections"))

    @builtins.property
    @jsii.member(jsii_name="fallbackPrompt")
    def fallback_prompt(
        self,
    ) -> DialogflowCxToolDataStoreSpecFallbackPromptOutputReference:
        return typing.cast(DialogflowCxToolDataStoreSpecFallbackPromptOutputReference, jsii.get(self, "fallbackPrompt"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreConnectionsInput")
    def data_store_connections_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxToolDataStoreSpecDataStoreConnections]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxToolDataStoreSpecDataStoreConnections]]], jsii.get(self, "dataStoreConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fallbackPromptInput")
    def fallback_prompt_input(
        self,
    ) -> typing.Optional[DialogflowCxToolDataStoreSpecFallbackPrompt]:
        return typing.cast(typing.Optional[DialogflowCxToolDataStoreSpecFallbackPrompt], jsii.get(self, "fallbackPromptInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxToolDataStoreSpec]:
        return typing.cast(typing.Optional[DialogflowCxToolDataStoreSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxToolDataStoreSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ec50c9ee5d04053647a26acdfaf5c0c6ea51e88d9588f671601bfa686a2d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolFunctionSpec",
    jsii_struct_bases=[],
    name_mapping={"input_schema": "inputSchema", "output_schema": "outputSchema"},
)
class DialogflowCxToolFunctionSpec:
    def __init__(
        self,
        *,
        input_schema: typing.Optional[builtins.str] = None,
        output_schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input_schema: Optional. The JSON schema is encapsulated in a `google.protobuf.Struct <https://protobuf.dev/reference/protobuf/google.protobuf/#struct>`_ to describe the input of the function. This input is a JSON object that contains the function's parameters as properties of the object Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#input_schema DialogflowCxTool#input_schema}
        :param output_schema: Optional. The JSON schema is encapsulated in a `google.protobuf.Struct <https://protobuf.dev/reference/protobuf/google.protobuf/#struct>`_ to describe the output of the function. This output is a JSON object that contains the function's parameters as properties of the object Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#output_schema DialogflowCxTool#output_schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52853d41375317febd898000544880de6e9e58efb7d00f900ef4d6631d9bea26)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#input_schema DialogflowCxTool#input_schema}
        '''
        result = self._values.get("input_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_schema(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The JSON schema is encapsulated in a `google.protobuf.Struct <https://protobuf.dev/reference/protobuf/google.protobuf/#struct>`_ to describe the output of the function.
        This output is a JSON object that contains the function's parameters as properties of the object

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#output_schema DialogflowCxTool#output_schema}
        '''
        result = self._values.get("output_schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolFunctionSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxToolFunctionSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolFunctionSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d60377f25b98612573a47cc19c5b88489e38b34f0e7fe08417b649258cd81bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9f12cad0783a11f296e1cbf378a81b3c18f12cfdcb3b6721220a1dfc635fdbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputSchema")
    def output_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputSchema"))

    @output_schema.setter
    def output_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d72732932867d9664f5d930cce587617760d935e0fb52b35a651c65865af0b2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxToolFunctionSpec]:
        return typing.cast(typing.Optional[DialogflowCxToolFunctionSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxToolFunctionSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1097a8a6e0309fe760cb620fafdb484b66b6d579b2dbde0e1106114b050483d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpec",
    jsii_struct_bases=[],
    name_mapping={
        "text_schema": "textSchema",
        "authentication": "authentication",
        "service_directory_config": "serviceDirectoryConfig",
        "tls_config": "tlsConfig",
    },
)
class DialogflowCxToolOpenApiSpec:
    def __init__(
        self,
        *,
        text_schema: builtins.str,
        authentication: typing.Optional[typing.Union["DialogflowCxToolOpenApiSpecAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        service_directory_config: typing.Optional[typing.Union["DialogflowCxToolOpenApiSpecServiceDirectoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_config: typing.Optional[typing.Union["DialogflowCxToolOpenApiSpecTlsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param text_schema: The OpenAPI schema specified as a text. This field is part of a union field 'schema': only one of 'textSchema' may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#text_schema DialogflowCxTool#text_schema}
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#authentication DialogflowCxTool#authentication}
        :param service_directory_config: service_directory_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#service_directory_config DialogflowCxTool#service_directory_config}
        :param tls_config: tls_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#tls_config DialogflowCxTool#tls_config}
        '''
        if isinstance(authentication, dict):
            authentication = DialogflowCxToolOpenApiSpecAuthentication(**authentication)
        if isinstance(service_directory_config, dict):
            service_directory_config = DialogflowCxToolOpenApiSpecServiceDirectoryConfig(**service_directory_config)
        if isinstance(tls_config, dict):
            tls_config = DialogflowCxToolOpenApiSpecTlsConfig(**tls_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d84f7267c185fd4dc1188a447d59ba9098bb953ec06033f3bfe7b43ec5c3d0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#text_schema DialogflowCxTool#text_schema}
        '''
        result = self._values.get("text_schema")
        assert result is not None, "Required property 'text_schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication(
        self,
    ) -> typing.Optional["DialogflowCxToolOpenApiSpecAuthentication"]:
        '''authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#authentication DialogflowCxTool#authentication}
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional["DialogflowCxToolOpenApiSpecAuthentication"], result)

    @builtins.property
    def service_directory_config(
        self,
    ) -> typing.Optional["DialogflowCxToolOpenApiSpecServiceDirectoryConfig"]:
        '''service_directory_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#service_directory_config DialogflowCxTool#service_directory_config}
        '''
        result = self._values.get("service_directory_config")
        return typing.cast(typing.Optional["DialogflowCxToolOpenApiSpecServiceDirectoryConfig"], result)

    @builtins.property
    def tls_config(self) -> typing.Optional["DialogflowCxToolOpenApiSpecTlsConfig"]:
        '''tls_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#tls_config DialogflowCxTool#tls_config}
        '''
        result = self._values.get("tls_config")
        return typing.cast(typing.Optional["DialogflowCxToolOpenApiSpecTlsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolOpenApiSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "api_key_config": "apiKeyConfig",
        "bearer_token_config": "bearerTokenConfig",
        "oauth_config": "oauthConfig",
        "service_agent_auth_config": "serviceAgentAuthConfig",
    },
)
class DialogflowCxToolOpenApiSpecAuthentication:
    def __init__(
        self,
        *,
        api_key_config: typing.Optional[typing.Union["DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        bearer_token_config: typing.Optional[typing.Union["DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_config: typing.Optional[typing.Union["DialogflowCxToolOpenApiSpecAuthenticationOauthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        service_agent_auth_config: typing.Optional[typing.Union["DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_key_config: api_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#api_key_config DialogflowCxTool#api_key_config}
        :param bearer_token_config: bearer_token_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#bearer_token_config DialogflowCxTool#bearer_token_config}
        :param oauth_config: oauth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#oauth_config DialogflowCxTool#oauth_config}
        :param service_agent_auth_config: service_agent_auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#service_agent_auth_config DialogflowCxTool#service_agent_auth_config}
        '''
        if isinstance(api_key_config, dict):
            api_key_config = DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig(**api_key_config)
        if isinstance(bearer_token_config, dict):
            bearer_token_config = DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig(**bearer_token_config)
        if isinstance(oauth_config, dict):
            oauth_config = DialogflowCxToolOpenApiSpecAuthenticationOauthConfig(**oauth_config)
        if isinstance(service_agent_auth_config, dict):
            service_agent_auth_config = DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig(**service_agent_auth_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e79d67d5a284905ff700ab621e62f407523b444144f37d9692b7a9c8ef7e39)
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
    ) -> typing.Optional["DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig"]:
        '''api_key_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#api_key_config DialogflowCxTool#api_key_config}
        '''
        result = self._values.get("api_key_config")
        return typing.cast(typing.Optional["DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig"], result)

    @builtins.property
    def bearer_token_config(
        self,
    ) -> typing.Optional["DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig"]:
        '''bearer_token_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#bearer_token_config DialogflowCxTool#bearer_token_config}
        '''
        result = self._values.get("bearer_token_config")
        return typing.cast(typing.Optional["DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig"], result)

    @builtins.property
    def oauth_config(
        self,
    ) -> typing.Optional["DialogflowCxToolOpenApiSpecAuthenticationOauthConfig"]:
        '''oauth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#oauth_config DialogflowCxTool#oauth_config}
        '''
        result = self._values.get("oauth_config")
        return typing.cast(typing.Optional["DialogflowCxToolOpenApiSpecAuthenticationOauthConfig"], result)

    @builtins.property
    def service_agent_auth_config(
        self,
    ) -> typing.Optional["DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig"]:
        '''service_agent_auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#service_agent_auth_config DialogflowCxTool#service_agent_auth_config}
        '''
        result = self._values.get("service_agent_auth_config")
        return typing.cast(typing.Optional["DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolOpenApiSpecAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig",
    jsii_struct_bases=[],
    name_mapping={
        "key_name": "keyName",
        "request_location": "requestLocation",
        "api_key": "apiKey",
        "secret_version_for_api_key": "secretVersionForApiKey",
    },
)
class DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig:
    def __init__(
        self,
        *,
        key_name: builtins.str,
        request_location: builtins.str,
        api_key: typing.Optional[builtins.str] = None,
        secret_version_for_api_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_name: The parameter name or the header name of the API key. E.g., If the API request is "https://example.com/act?X-Api-Key=", "X-Api-Key" would be the parameter name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#key_name DialogflowCxTool#key_name}
        :param request_location: Key location in the request. See `RequestLocation <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#requestlocation>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#request_location DialogflowCxTool#request_location}
        :param api_key: Optional. The API key. If the 'secretVersionForApiKey'' field is set, this field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#api_key DialogflowCxTool#api_key}
        :param secret_version_for_api_key: Optional. The name of the SecretManager secret version resource storing the API key. If this field is set, the apiKey field will be ignored. Format: projects/{project}/secrets/{secret}/versions/{version} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#secret_version_for_api_key DialogflowCxTool#secret_version_for_api_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3711c78dfa11b7a1e6803d47864acb9ba307e4709a4d4f2d1c68d22ed294f8b1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#key_name DialogflowCxTool#key_name}
        '''
        result = self._values.get("key_name")
        assert result is not None, "Required property 'key_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_location(self) -> builtins.str:
        '''Key location in the request. See `RequestLocation <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#requestlocation>`_ for valid values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#request_location DialogflowCxTool#request_location}
        '''
        result = self._values.get("request_location")
        assert result is not None, "Required property 'request_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        '''Optional. The API key. If the 'secretVersionForApiKey'' field is set, this field will be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#api_key DialogflowCxTool#api_key}
        '''
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_version_for_api_key(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The name of the SecretManager secret version resource storing the API key.
        If this field is set, the apiKey field will be ignored.
        Format: projects/{project}/secrets/{secret}/versions/{version}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#secret_version_for_api_key DialogflowCxTool#secret_version_for_api_key}
        '''
        result = self._values.get("secret_version_for_api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cf2a7a15c7020e642e30e13d901432db1f1f61a3653fac885e4eff1df2296e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5029f5d751bb0a3e6e82f59530c9ffd322810e7a1f3d8d402c8d038d29372489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyName")
    def key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyName"))

    @key_name.setter
    def key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d758e57b2ed491d6cd8b20e13b42f8711b8415e63156f96cb547940c7bd0fd63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestLocation")
    def request_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestLocation"))

    @request_location.setter
    def request_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93278e5c505996f4ea418dda5deb831ee65aef1b0ede38ab3bed12f7057ff6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersionForApiKey")
    def secret_version_for_api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersionForApiKey"))

    @secret_version_for_api_key.setter
    def secret_version_for_api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37ae6597dad294a605ff8fe7a1cb3e4465b83e7f9c789b722b1f9dcbee860b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersionForApiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig]:
        return typing.cast(typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8bd1c9ad8ae796c4950b8436d79f49eb7e64c52622ebf3387b2f4893a002b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig",
    jsii_struct_bases=[],
    name_mapping={
        "secret_version_for_token": "secretVersionForToken",
        "token": "token",
    },
)
class DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig:
    def __init__(
        self,
        *,
        secret_version_for_token: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret_version_for_token: Optional. The name of the SecretManager secret version resource storing the Bearer token. If this field is set, the 'token' field will be ignored. Format: projects/{project}/secrets/{secret}/versions/{version} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#secret_version_for_token DialogflowCxTool#secret_version_for_token}
        :param token: Optional. The text token appended to the text Bearer to the request Authorization header. `Session parameters reference <https://cloud.google.com/dialogflow/cx/docs/concept/parameter#session-ref>`_ can be used to pass the token dynamically, e.g. '$session.params.parameter-id'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#token DialogflowCxTool#token}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1942ecbca7ace786dc7804310a3d16b9de15d262e4a1a8d191a6880b886eb020)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#secret_version_for_token DialogflowCxTool#secret_version_for_token}
        '''
        result = self._values.get("secret_version_for_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The text token appended to the text Bearer to the request Authorization header.
        `Session parameters reference <https://cloud.google.com/dialogflow/cx/docs/concept/parameter#session-ref>`_ can be used to pass the token dynamically, e.g. '$session.params.parameter-id'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#token DialogflowCxTool#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53952afd98dbee826d540022b91604b6f652faec72e1c246f784586d79fcc163)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25e32123251686bfb2a21ff37f2f1384b1f76c246ff3501bab95849415664084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersionForToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @token.setter
    def token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c56386068816eaac4f092c547e7af4b3226eb947ed7d520296fa84fea621d692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig]:
        return typing.cast(typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2613f172c49ca305e97e883164d560caf1210e4f7499cd8aea80e95e41e3cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecAuthenticationOauthConfig",
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
class DialogflowCxToolOpenApiSpecAuthenticationOauthConfig:
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
        :param client_id: The client ID from the OAuth provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#client_id DialogflowCxTool#client_id}
        :param oauth_grant_type: OAuth grant types. See `OauthGrantType <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#oauthgranttype>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#oauth_grant_type DialogflowCxTool#oauth_grant_type}
        :param token_endpoint: The token endpoint in the OAuth provider to exchange for an access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#token_endpoint DialogflowCxTool#token_endpoint}
        :param client_secret: Optional. The client secret from the OAuth provider. If the 'secretVersionForClientSecret' field is set, this field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#client_secret DialogflowCxTool#client_secret}
        :param scopes: Optional. The OAuth scopes to grant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#scopes DialogflowCxTool#scopes}
        :param secret_version_for_client_secret: Optional. The name of the SecretManager secret version resource storing the client secret. If this field is set, the clientSecret field will be ignored. Format: projects/{project}/secrets/{secret}/versions/{version} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#secret_version_for_client_secret DialogflowCxTool#secret_version_for_client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0ebd4f59ff61fe074cb810e290f97a54214cf616298e712ceb4fbf8921c8ce)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#client_id DialogflowCxTool#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_grant_type(self) -> builtins.str:
        '''OAuth grant types. See `OauthGrantType <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#oauthgranttype>`_ for valid values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#oauth_grant_type DialogflowCxTool#oauth_grant_type}
        '''
        result = self._values.get("oauth_grant_type")
        assert result is not None, "Required property 'oauth_grant_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_endpoint(self) -> builtins.str:
        '''The token endpoint in the OAuth provider to exchange for an access token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#token_endpoint DialogflowCxTool#token_endpoint}
        '''
        result = self._values.get("token_endpoint")
        assert result is not None, "Required property 'token_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Optional. The client secret from the OAuth provider. If the 'secretVersionForClientSecret' field is set, this field will be ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#client_secret DialogflowCxTool#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. The OAuth scopes to grant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#scopes DialogflowCxTool#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secret_version_for_client_secret(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The name of the SecretManager secret version resource storing the client secret.
        If this field is set, the clientSecret field will be ignored.
        Format: projects/{project}/secrets/{secret}/versions/{version}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#secret_version_for_client_secret DialogflowCxTool#secret_version_for_client_secret}
        '''
        result = self._values.get("secret_version_for_client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolOpenApiSpecAuthenticationOauthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxToolOpenApiSpecAuthenticationOauthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecAuthenticationOauthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__386b760da867d77ce71a8b2e65803ac32f50e645006cb5052beb629509d19f0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6a972fe70cbde41b38ad399f07977332b1a28160680caff0b4c15085aeebcd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0646a82c2c5a327433081b3485f6632751af69db677c292ffec2db35d2b4de66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthGrantType")
    def oauth_grant_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthGrantType"))

    @oauth_grant_type.setter
    def oauth_grant_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af95d9c4ffff1efadbc5954c179f48aa01654e86ee0cddf71a8c6144a0d1557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthGrantType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8edff927103578be0ecea964127f5571794801197986d854d9188aa27b7b490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersionForClientSecret")
    def secret_version_for_client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersionForClientSecret"))

    @secret_version_for_client_secret.setter
    def secret_version_for_client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d136dcacdd528a4b77c8fbf2c8f027bcafc49569c249f55611e909346175a252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersionForClientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpoint"))

    @token_endpoint.setter
    def token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89beeec1a1c277dfa634b4bf8b73da5da0a0d5831468e6ae30eb18051daaf8c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationOauthConfig]:
        return typing.cast(typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationOauthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationOauthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac66b31faed87261d88a5d476e388c776a033d4dec96b72a8a19812217ff641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxToolOpenApiSpecAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcb9e6c2cc2271b40c199c2a7d5f4ae04253e66ba3ea4c83154b7856e883fb1d)
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
        :param key_name: The parameter name or the header name of the API key. E.g., If the API request is "https://example.com/act?X-Api-Key=", "X-Api-Key" would be the parameter name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#key_name DialogflowCxTool#key_name}
        :param request_location: Key location in the request. See `RequestLocation <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#requestlocation>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#request_location DialogflowCxTool#request_location}
        :param api_key: Optional. The API key. If the 'secretVersionForApiKey'' field is set, this field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#api_key DialogflowCxTool#api_key}
        :param secret_version_for_api_key: Optional. The name of the SecretManager secret version resource storing the API key. If this field is set, the apiKey field will be ignored. Format: projects/{project}/secrets/{secret}/versions/{version} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#secret_version_for_api_key DialogflowCxTool#secret_version_for_api_key}
        '''
        value = DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig(
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
        :param secret_version_for_token: Optional. The name of the SecretManager secret version resource storing the Bearer token. If this field is set, the 'token' field will be ignored. Format: projects/{project}/secrets/{secret}/versions/{version} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#secret_version_for_token DialogflowCxTool#secret_version_for_token}
        :param token: Optional. The text token appended to the text Bearer to the request Authorization header. `Session parameters reference <https://cloud.google.com/dialogflow/cx/docs/concept/parameter#session-ref>`_ can be used to pass the token dynamically, e.g. '$session.params.parameter-id'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#token DialogflowCxTool#token}
        '''
        value = DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig(
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
        :param client_id: The client ID from the OAuth provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#client_id DialogflowCxTool#client_id}
        :param oauth_grant_type: OAuth grant types. See `OauthGrantType <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#oauthgranttype>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#oauth_grant_type DialogflowCxTool#oauth_grant_type}
        :param token_endpoint: The token endpoint in the OAuth provider to exchange for an access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#token_endpoint DialogflowCxTool#token_endpoint}
        :param client_secret: Optional. The client secret from the OAuth provider. If the 'secretVersionForClientSecret' field is set, this field will be ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#client_secret DialogflowCxTool#client_secret}
        :param scopes: Optional. The OAuth scopes to grant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#scopes DialogflowCxTool#scopes}
        :param secret_version_for_client_secret: Optional. The name of the SecretManager secret version resource storing the client secret. If this field is set, the clientSecret field will be ignored. Format: projects/{project}/secrets/{secret}/versions/{version} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#secret_version_for_client_secret DialogflowCxTool#secret_version_for_client_secret}
        '''
        value = DialogflowCxToolOpenApiSpecAuthenticationOauthConfig(
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
        :param service_agent_auth: Optional. Indicate the auth token type generated from the Diglogflow service agent. The generated token is sent in the Authorization header. See `ServiceAgentAuth <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#serviceagentauth>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#service_agent_auth DialogflowCxTool#service_agent_auth}
        '''
        value = DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig(
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
    ) -> DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfigOutputReference:
        return typing.cast(DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfigOutputReference, jsii.get(self, "apiKeyConfig"))

    @builtins.property
    @jsii.member(jsii_name="bearerTokenConfig")
    def bearer_token_config(
        self,
    ) -> DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfigOutputReference:
        return typing.cast(DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfigOutputReference, jsii.get(self, "bearerTokenConfig"))

    @builtins.property
    @jsii.member(jsii_name="oauthConfig")
    def oauth_config(
        self,
    ) -> DialogflowCxToolOpenApiSpecAuthenticationOauthConfigOutputReference:
        return typing.cast(DialogflowCxToolOpenApiSpecAuthenticationOauthConfigOutputReference, jsii.get(self, "oauthConfig"))

    @builtins.property
    @jsii.member(jsii_name="serviceAgentAuthConfig")
    def service_agent_auth_config(
        self,
    ) -> "DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfigOutputReference":
        return typing.cast("DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfigOutputReference", jsii.get(self, "serviceAgentAuthConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyConfigInput")
    def api_key_config_input(
        self,
    ) -> typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig]:
        return typing.cast(typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig], jsii.get(self, "apiKeyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bearerTokenConfigInput")
    def bearer_token_config_input(
        self,
    ) -> typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig]:
        return typing.cast(typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig], jsii.get(self, "bearerTokenConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthConfigInput")
    def oauth_config_input(
        self,
    ) -> typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationOauthConfig]:
        return typing.cast(typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationOauthConfig], jsii.get(self, "oauthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAgentAuthConfigInput")
    def service_agent_auth_config_input(
        self,
    ) -> typing.Optional["DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig"]:
        return typing.cast(typing.Optional["DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig"], jsii.get(self, "serviceAgentAuthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxToolOpenApiSpecAuthentication]:
        return typing.cast(typing.Optional[DialogflowCxToolOpenApiSpecAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxToolOpenApiSpecAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c54e9e59a25219278b269a97ca58dd10f52384d5f6461ac0af11c87c709e973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig",
    jsii_struct_bases=[],
    name_mapping={"service_agent_auth": "serviceAgentAuth"},
)
class DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig:
    def __init__(
        self,
        *,
        service_agent_auth: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_agent_auth: Optional. Indicate the auth token type generated from the Diglogflow service agent. The generated token is sent in the Authorization header. See `ServiceAgentAuth <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.tools#serviceagentauth>`_ for valid values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#service_agent_auth DialogflowCxTool#service_agent_auth}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621dbb1da6937a268781c2180f5e8c3d91d2ef48459b08ad5053da05e3cac979)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#service_agent_auth DialogflowCxTool#service_agent_auth}
        '''
        result = self._values.get("service_agent_auth")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1766bc5dbc9bbf497efc35c673e762de228e16a6b3f48bfaf6f6a2a63743a437)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70ea260f96b5951f9fae6794c199911bf92976572def1b376c5bfbcb5513edd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAgentAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig]:
        return typing.cast(typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa87017c3432f068cb04e6743c4bba2ed9d623c09c9d5e211b3701ca4de1dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxToolOpenApiSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c692448a76d30fa1d3977ed96447f6ad450247a6ca169abec8c5836e413fd911)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthentication")
    def put_authentication(
        self,
        *,
        api_key_config: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        bearer_token_config: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_config: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpecAuthenticationOauthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        service_agent_auth_config: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_key_config: api_key_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#api_key_config DialogflowCxTool#api_key_config}
        :param bearer_token_config: bearer_token_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#bearer_token_config DialogflowCxTool#bearer_token_config}
        :param oauth_config: oauth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#oauth_config DialogflowCxTool#oauth_config}
        :param service_agent_auth_config: service_agent_auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#service_agent_auth_config DialogflowCxTool#service_agent_auth_config}
        '''
        value = DialogflowCxToolOpenApiSpecAuthentication(
            api_key_config=api_key_config,
            bearer_token_config=bearer_token_config,
            oauth_config=oauth_config,
            service_agent_auth_config=service_agent_auth_config,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthentication", [value]))

    @jsii.member(jsii_name="putServiceDirectoryConfig")
    def put_service_directory_config(self, *, service: builtins.str) -> None:
        '''
        :param service: The name of `Service Directory <https://cloud.google.com/service-directory/docs>`_ service. Format: projects//locations//namespaces//services/. LocationID of the service directory must be the same as the location of the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#service DialogflowCxTool#service}
        '''
        value = DialogflowCxToolOpenApiSpecServiceDirectoryConfig(service=service)

        return typing.cast(None, jsii.invoke(self, "putServiceDirectoryConfig", [value]))

    @jsii.member(jsii_name="putTlsConfig")
    def put_tls_config(
        self,
        *,
        ca_certs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxToolOpenApiSpecTlsConfigCaCerts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param ca_certs: ca_certs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#ca_certs DialogflowCxTool#ca_certs}
        '''
        value = DialogflowCxToolOpenApiSpecTlsConfig(ca_certs=ca_certs)

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
    ) -> DialogflowCxToolOpenApiSpecAuthenticationOutputReference:
        return typing.cast(DialogflowCxToolOpenApiSpecAuthenticationOutputReference, jsii.get(self, "authentication"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfig")
    def service_directory_config(
        self,
    ) -> "DialogflowCxToolOpenApiSpecServiceDirectoryConfigOutputReference":
        return typing.cast("DialogflowCxToolOpenApiSpecServiceDirectoryConfigOutputReference", jsii.get(self, "serviceDirectoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="tlsConfig")
    def tls_config(self) -> "DialogflowCxToolOpenApiSpecTlsConfigOutputReference":
        return typing.cast("DialogflowCxToolOpenApiSpecTlsConfigOutputReference", jsii.get(self, "tlsConfig"))

    @builtins.property
    @jsii.member(jsii_name="authenticationInput")
    def authentication_input(
        self,
    ) -> typing.Optional[DialogflowCxToolOpenApiSpecAuthentication]:
        return typing.cast(typing.Optional[DialogflowCxToolOpenApiSpecAuthentication], jsii.get(self, "authenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryConfigInput")
    def service_directory_config_input(
        self,
    ) -> typing.Optional["DialogflowCxToolOpenApiSpecServiceDirectoryConfig"]:
        return typing.cast(typing.Optional["DialogflowCxToolOpenApiSpecServiceDirectoryConfig"], jsii.get(self, "serviceDirectoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="textSchemaInput")
    def text_schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsConfigInput")
    def tls_config_input(
        self,
    ) -> typing.Optional["DialogflowCxToolOpenApiSpecTlsConfig"]:
        return typing.cast(typing.Optional["DialogflowCxToolOpenApiSpecTlsConfig"], jsii.get(self, "tlsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="textSchema")
    def text_schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "textSchema"))

    @text_schema.setter
    def text_schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11c4ea95c7f08d204a2955e9b2a9e7b5cccc871082c928af91d78b088932d592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxToolOpenApiSpec]:
        return typing.cast(typing.Optional[DialogflowCxToolOpenApiSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxToolOpenApiSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da2e94f1ac46d29a1097fd6a41284fba6b7d5117c85606da31585a39162d26ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecServiceDirectoryConfig",
    jsii_struct_bases=[],
    name_mapping={"service": "service"},
)
class DialogflowCxToolOpenApiSpecServiceDirectoryConfig:
    def __init__(self, *, service: builtins.str) -> None:
        '''
        :param service: The name of `Service Directory <https://cloud.google.com/service-directory/docs>`_ service. Format: projects//locations//namespaces//services/. LocationID of the service directory must be the same as the location of the agent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#service DialogflowCxTool#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c9504cedbc60009f5725855c2d3c1c4ef9bab2f918653f1aba38c2f97842ac1)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }

    @builtins.property
    def service(self) -> builtins.str:
        '''The name of `Service Directory <https://cloud.google.com/service-directory/docs>`_ service. Format: projects//locations//namespaces//services/. LocationID of the service directory must be the same as the location of the agent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#service DialogflowCxTool#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolOpenApiSpecServiceDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxToolOpenApiSpecServiceDirectoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecServiceDirectoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5412a597a404b6c862fd7bf71f6121ae637d64ea734fcf7741007645ac0026b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f622284fd51a788cf53788dcaad8be742495b833e60730d9cd244a1246e201f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxToolOpenApiSpecServiceDirectoryConfig]:
        return typing.cast(typing.Optional[DialogflowCxToolOpenApiSpecServiceDirectoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxToolOpenApiSpecServiceDirectoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7053f5936fc4beb65a157b2f055134f081b8387da38aee230b9de09cb0cae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecTlsConfig",
    jsii_struct_bases=[],
    name_mapping={"ca_certs": "caCerts"},
)
class DialogflowCxToolOpenApiSpecTlsConfig:
    def __init__(
        self,
        *,
        ca_certs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxToolOpenApiSpecTlsConfigCaCerts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param ca_certs: ca_certs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#ca_certs DialogflowCxTool#ca_certs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c144f10e973d62d0544b33339251ee814dbf34f1dc825777c83e8246b20c9da)
            check_type(argname="argument ca_certs", value=ca_certs, expected_type=type_hints["ca_certs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ca_certs": ca_certs,
        }

    @builtins.property
    def ca_certs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxToolOpenApiSpecTlsConfigCaCerts"]]:
        '''ca_certs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#ca_certs DialogflowCxTool#ca_certs}
        '''
        result = self._values.get("ca_certs")
        assert result is not None, "Required property 'ca_certs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxToolOpenApiSpecTlsConfigCaCerts"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolOpenApiSpecTlsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecTlsConfigCaCerts",
    jsii_struct_bases=[],
    name_mapping={"cert": "cert", "display_name": "displayName"},
)
class DialogflowCxToolOpenApiSpecTlsConfigCaCerts:
    def __init__(self, *, cert: builtins.str, display_name: builtins.str) -> None:
        '''
        :param cert: The allowed custom CA certificates (in DER format) for HTTPS verification. This overrides the default SSL trust store. If this is empty or unspecified, Dialogflow will use Google's default trust store to verify certificates. N.B. Make sure the HTTPS server certificates are signed with "subject alt name". For instance a certificate can be self-signed using the following command:: openssl x509 -req -days 200 -in example.com.csr \\ -signkey example.com.key \\ -out example.com.crt \\ -extfile <(printf "\\nsubjectAltName='DNS:www.example.com'") A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#cert DialogflowCxTool#cert}
        :param display_name: The name of the allowed custom CA certificates. This can be used to disambiguate the custom CA certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#display_name DialogflowCxTool#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a5077a69932270f8425b33b44926afa4aa272f2eb91a8d5279d09a93ffdc38)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#cert DialogflowCxTool#cert}
        '''
        result = self._values.get("cert")
        assert result is not None, "Required property 'cert' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The name of the allowed custom CA certificates. This can be used to disambiguate the custom CA certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#display_name DialogflowCxTool#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolOpenApiSpecTlsConfigCaCerts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxToolOpenApiSpecTlsConfigCaCertsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecTlsConfigCaCertsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae5d91a574c263175d2813501fcc8d411a17228614f657334e1f37ea80c15249)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxToolOpenApiSpecTlsConfigCaCertsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__285ae9aa63231f0f500734288f72ef31ee0f2ab8415234b88a947709f02aa91f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxToolOpenApiSpecTlsConfigCaCertsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0262c7474977ea905c277c35bb055bd86842fd76b171bf6c03df7ae51b07f21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcbe35469fb94b4c37dfdac7478aad0af5f77df4ddcba739bf491d1d61fd01a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54cf442d5f6ae3819d534ccdc3d785e60fd4353adb29a6eeb6515065b57fd31f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxToolOpenApiSpecTlsConfigCaCerts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxToolOpenApiSpecTlsConfigCaCerts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxToolOpenApiSpecTlsConfigCaCerts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125f9e2b6aa8aa3076f39d9c84a83ac5e50447929ba20e67618428fa2bed7f68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxToolOpenApiSpecTlsConfigCaCertsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecTlsConfigCaCertsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17590b24dd65c4261d31ae50561a695e34c2afe2b9688be0dc9bda12a5340a70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__710330eda21ef19844d3c8ef6f22c9f8840a19197b0005a2be8133673c147078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828acbbc675e24ce12d6905a89c403402cafb000356fd60d1fa2ccc266aa763b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxToolOpenApiSpecTlsConfigCaCerts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxToolOpenApiSpecTlsConfigCaCerts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxToolOpenApiSpecTlsConfigCaCerts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81974f828ea98ef1ffdcd146f91acd2abe36e9ead4d8b3c726c62739a6bd726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxToolOpenApiSpecTlsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolOpenApiSpecTlsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3910764fd54eb62a1e05c8eeb8942e72d56f310a2c5f7c7f11b752f4bea1c310)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCaCerts")
    def put_ca_certs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxToolOpenApiSpecTlsConfigCaCerts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21fde58d5d1b7a5bc3d37bc18dfc531af5f974222fec59cbbac0f8ee6d6920c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCaCerts", [value]))

    @builtins.property
    @jsii.member(jsii_name="caCerts")
    def ca_certs(self) -> DialogflowCxToolOpenApiSpecTlsConfigCaCertsList:
        return typing.cast(DialogflowCxToolOpenApiSpecTlsConfigCaCertsList, jsii.get(self, "caCerts"))

    @builtins.property
    @jsii.member(jsii_name="caCertsInput")
    def ca_certs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxToolOpenApiSpecTlsConfigCaCerts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxToolOpenApiSpecTlsConfigCaCerts]]], jsii.get(self, "caCertsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxToolOpenApiSpecTlsConfig]:
        return typing.cast(typing.Optional[DialogflowCxToolOpenApiSpecTlsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxToolOpenApiSpecTlsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c24e6aacfaa4c63ee4d78c828954e3d61f56833566478848959187ca5c6b3661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DialogflowCxToolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#create DialogflowCxTool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#delete DialogflowCxTool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#update DialogflowCxTool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27de6a2b1b2d3c81f8bac31067e0db4e21731eb600baef179ddcaa50d16c3ad)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#create DialogflowCxTool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#delete DialogflowCxTool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_cx_tool#update DialogflowCxTool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxToolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxToolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxTool.DialogflowCxToolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f41c22c2df7896f9bd87bb6937b26b663a66e20244d52bbb839851842e956c35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea60a52f7d9bf8cd648b550b34dc9ea60eb3fe04faa7935bcc46792a0ff71c6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc2bd07197e8c7056a11c5a109664ab00b024eaa1ac24dc435aaa0500cbed67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57346c8c3519082fbaaf5b37a97a32b49a3087e362f99292350f31179d5896a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxToolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxToolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxToolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c2e6fe54cbbf8327eb7c8171e75915177c5a048db3aa73050e7834c39f4159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DialogflowCxTool",
    "DialogflowCxToolConfig",
    "DialogflowCxToolDataStoreSpec",
    "DialogflowCxToolDataStoreSpecDataStoreConnections",
    "DialogflowCxToolDataStoreSpecDataStoreConnectionsList",
    "DialogflowCxToolDataStoreSpecDataStoreConnectionsOutputReference",
    "DialogflowCxToolDataStoreSpecFallbackPrompt",
    "DialogflowCxToolDataStoreSpecFallbackPromptOutputReference",
    "DialogflowCxToolDataStoreSpecOutputReference",
    "DialogflowCxToolFunctionSpec",
    "DialogflowCxToolFunctionSpecOutputReference",
    "DialogflowCxToolOpenApiSpec",
    "DialogflowCxToolOpenApiSpecAuthentication",
    "DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig",
    "DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfigOutputReference",
    "DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig",
    "DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfigOutputReference",
    "DialogflowCxToolOpenApiSpecAuthenticationOauthConfig",
    "DialogflowCxToolOpenApiSpecAuthenticationOauthConfigOutputReference",
    "DialogflowCxToolOpenApiSpecAuthenticationOutputReference",
    "DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig",
    "DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfigOutputReference",
    "DialogflowCxToolOpenApiSpecOutputReference",
    "DialogflowCxToolOpenApiSpecServiceDirectoryConfig",
    "DialogflowCxToolOpenApiSpecServiceDirectoryConfigOutputReference",
    "DialogflowCxToolOpenApiSpecTlsConfig",
    "DialogflowCxToolOpenApiSpecTlsConfigCaCerts",
    "DialogflowCxToolOpenApiSpecTlsConfigCaCertsList",
    "DialogflowCxToolOpenApiSpecTlsConfigCaCertsOutputReference",
    "DialogflowCxToolOpenApiSpecTlsConfigOutputReference",
    "DialogflowCxToolTimeouts",
    "DialogflowCxToolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__37a21657ba01f827dd1fe503f075ddfa8e3bcc55017aa25488225cda6d953d2a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    description: builtins.str,
    display_name: builtins.str,
    data_store_spec: typing.Optional[typing.Union[DialogflowCxToolDataStoreSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    function_spec: typing.Optional[typing.Union[DialogflowCxToolFunctionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    open_api_spec: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxToolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bd6987e0bc7062a9e00dd0ee4d3e5b31abeec21fd49b9de56db8057d8ca84509(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1ebb453fc0303647abdd0a69ee9ce5488dca2c1ba820a416dbbba30d17a272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d24f339f01b0192b9438107f3c11025e86adca765131e1c1854fd83f4ec60c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d2d8cad2940bc61ab1e6078f445ff21fe17b363ab03ae18c4ee1052cb0074e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40356e252e6bceb172d7c130eaabe55a11a6b2d13fbf582284d1e1fe42a7851(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b1cc35f61a32d5de1e6820e7fa4c12fc1b097b0d4a4f2190c456f9606dfba3(
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
    data_store_spec: typing.Optional[typing.Union[DialogflowCxToolDataStoreSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    function_spec: typing.Optional[typing.Union[DialogflowCxToolFunctionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    open_api_spec: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxToolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de56bff96c9265784f082aad7ab81ea6e761ddc263ffb60cd24ae440f8ca636(
    *,
    data_store_connections: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxToolDataStoreSpecDataStoreConnections, typing.Dict[builtins.str, typing.Any]]]],
    fallback_prompt: typing.Union[DialogflowCxToolDataStoreSpecFallbackPrompt, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9171c236bde00f3d4eaeff77413324aa534de7aa5d2982f20c087e8f99b9f16e(
    *,
    data_store: typing.Optional[builtins.str] = None,
    data_store_type: typing.Optional[builtins.str] = None,
    document_processing_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a35f911287dc3b190157c231b1695305d6df4fda7372cb7184a562c1963585(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a12c37b10bcb872e30a1ad7224ce461ab28a894c65774cc0072c6bdb0b26b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f78cd2247275695bb97fc5a4ad71b5351ac060cfccbaa84f79b962a5bde359c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4291764700c5a8d0cae9a4adbbf5c854ce1e80611b047818b15261b9874905c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a5a0327af8dde55cab294e96b672b0ff6e35469416cebc3050ddffdbdfb39c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8275918f6375f533c18ad0091bc64c8a836ad62143afa0147051a6044a233131(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxToolDataStoreSpecDataStoreConnections]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac68aba90c84d39fd40b6ef13a8b5826f9a404ce305a4477e8b3d20a1ebcc51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a427c5108066fcbad6b5f22c1ec298c3d166dcb8694b8b83a11d5c4f91778c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65fe041c7fabd6f3ae4a4cc81221bc90440015b741394406d0eb1377a5b34dc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f3ad73076400aea3d6e5e68e6f25384e35a1506d93d0115e4084c80dc4fdf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b0e3a858a3a00e9b44d71394170d915a151cb0d417754bd9c89f0db4de3e1a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxToolDataStoreSpecDataStoreConnections]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a34424646a4aff1251b844552bb751a06c35e138294c936d7b98c651a4db135(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94fd1bce5a5e1f5cd8eb8577ac2b014d8f798122eb0e391ff2e5acb25beadcc(
    value: typing.Optional[DialogflowCxToolDataStoreSpecFallbackPrompt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e245d8af5b7be73768ae082f7c9e0492f07881c76f4556078f23fb81ffac9a70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09c0160ea8feaf3aa0f9697a867440327a9c518d3a998a5039b81248cd73f05(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxToolDataStoreSpecDataStoreConnections, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ec50c9ee5d04053647a26acdfaf5c0c6ea51e88d9588f671601bfa686a2d5c(
    value: typing.Optional[DialogflowCxToolDataStoreSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52853d41375317febd898000544880de6e9e58efb7d00f900ef4d6631d9bea26(
    *,
    input_schema: typing.Optional[builtins.str] = None,
    output_schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d60377f25b98612573a47cc19c5b88489e38b34f0e7fe08417b649258cd81bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f12cad0783a11f296e1cbf378a81b3c18f12cfdcb3b6721220a1dfc635fdbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d72732932867d9664f5d930cce587617760d935e0fb52b35a651c65865af0b2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1097a8a6e0309fe760cb620fafdb484b66b6d579b2dbde0e1106114b050483d5(
    value: typing.Optional[DialogflowCxToolFunctionSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d84f7267c185fd4dc1188a447d59ba9098bb953ec06033f3bfe7b43ec5c3d0(
    *,
    text_schema: builtins.str,
    authentication: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpecAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    service_directory_config: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpecServiceDirectoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_config: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpecTlsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e79d67d5a284905ff700ab621e62f407523b444144f37d9692b7a9c8ef7e39(
    *,
    api_key_config: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bearer_token_config: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth_config: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpecAuthenticationOauthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    service_agent_auth_config: typing.Optional[typing.Union[DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3711c78dfa11b7a1e6803d47864acb9ba307e4709a4d4f2d1c68d22ed294f8b1(
    *,
    key_name: builtins.str,
    request_location: builtins.str,
    api_key: typing.Optional[builtins.str] = None,
    secret_version_for_api_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf2a7a15c7020e642e30e13d901432db1f1f61a3653fac885e4eff1df2296e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5029f5d751bb0a3e6e82f59530c9ffd322810e7a1f3d8d402c8d038d29372489(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d758e57b2ed491d6cd8b20e13b42f8711b8415e63156f96cb547940c7bd0fd63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93278e5c505996f4ea418dda5deb831ee65aef1b0ede38ab3bed12f7057ff6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ae6597dad294a605ff8fe7a1cb3e4465b83e7f9c789b722b1f9dcbee860b19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8bd1c9ad8ae796c4950b8436d79f49eb7e64c52622ebf3387b2f4893a002b8(
    value: typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationApiKeyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1942ecbca7ace786dc7804310a3d16b9de15d262e4a1a8d191a6880b886eb020(
    *,
    secret_version_for_token: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53952afd98dbee826d540022b91604b6f652faec72e1c246f784586d79fcc163(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e32123251686bfb2a21ff37f2f1384b1f76c246ff3501bab95849415664084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56386068816eaac4f092c547e7af4b3226eb947ed7d520296fa84fea621d692(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2613f172c49ca305e97e883164d560caf1210e4f7499cd8aea80e95e41e3cdb(
    value: typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationBearerTokenConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0ebd4f59ff61fe074cb810e290f97a54214cf616298e712ceb4fbf8921c8ce(
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

def _typecheckingstub__386b760da867d77ce71a8b2e65803ac32f50e645006cb5052beb629509d19f0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a972fe70cbde41b38ad399f07977332b1a28160680caff0b4c15085aeebcd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0646a82c2c5a327433081b3485f6632751af69db677c292ffec2db35d2b4de66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af95d9c4ffff1efadbc5954c179f48aa01654e86ee0cddf71a8c6144a0d1557(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8edff927103578be0ecea964127f5571794801197986d854d9188aa27b7b490(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d136dcacdd528a4b77c8fbf2c8f027bcafc49569c249f55611e909346175a252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89beeec1a1c277dfa634b4bf8b73da5da0a0d5831468e6ae30eb18051daaf8c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac66b31faed87261d88a5d476e388c776a033d4dec96b72a8a19812217ff641(
    value: typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationOauthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb9e6c2cc2271b40c199c2a7d5f4ae04253e66ba3ea4c83154b7856e883fb1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c54e9e59a25219278b269a97ca58dd10f52384d5f6461ac0af11c87c709e973(
    value: typing.Optional[DialogflowCxToolOpenApiSpecAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621dbb1da6937a268781c2180f5e8c3d91d2ef48459b08ad5053da05e3cac979(
    *,
    service_agent_auth: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1766bc5dbc9bbf497efc35c673e762de228e16a6b3f48bfaf6f6a2a63743a437(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ea260f96b5951f9fae6794c199911bf92976572def1b376c5bfbcb5513edd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa87017c3432f068cb04e6743c4bba2ed9d623c09c9d5e211b3701ca4de1dee(
    value: typing.Optional[DialogflowCxToolOpenApiSpecAuthenticationServiceAgentAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c692448a76d30fa1d3977ed96447f6ad450247a6ca169abec8c5836e413fd911(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c4ea95c7f08d204a2955e9b2a9e7b5cccc871082c928af91d78b088932d592(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2e94f1ac46d29a1097fd6a41284fba6b7d5117c85606da31585a39162d26ba(
    value: typing.Optional[DialogflowCxToolOpenApiSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c9504cedbc60009f5725855c2d3c1c4ef9bab2f918653f1aba38c2f97842ac1(
    *,
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5412a597a404b6c862fd7bf71f6121ae637d64ea734fcf7741007645ac0026b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f622284fd51a788cf53788dcaad8be742495b833e60730d9cd244a1246e201f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7053f5936fc4beb65a157b2f055134f081b8387da38aee230b9de09cb0cae8(
    value: typing.Optional[DialogflowCxToolOpenApiSpecServiceDirectoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c144f10e973d62d0544b33339251ee814dbf34f1dc825777c83e8246b20c9da(
    *,
    ca_certs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxToolOpenApiSpecTlsConfigCaCerts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a5077a69932270f8425b33b44926afa4aa272f2eb91a8d5279d09a93ffdc38(
    *,
    cert: builtins.str,
    display_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5d91a574c263175d2813501fcc8d411a17228614f657334e1f37ea80c15249(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285ae9aa63231f0f500734288f72ef31ee0f2ab8415234b88a947709f02aa91f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0262c7474977ea905c277c35bb055bd86842fd76b171bf6c03df7ae51b07f21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcbe35469fb94b4c37dfdac7478aad0af5f77df4ddcba739bf491d1d61fd01a4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cf442d5f6ae3819d534ccdc3d785e60fd4353adb29a6eeb6515065b57fd31f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125f9e2b6aa8aa3076f39d9c84a83ac5e50447929ba20e67618428fa2bed7f68(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxToolOpenApiSpecTlsConfigCaCerts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17590b24dd65c4261d31ae50561a695e34c2afe2b9688be0dc9bda12a5340a70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710330eda21ef19844d3c8ef6f22c9f8840a19197b0005a2be8133673c147078(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828acbbc675e24ce12d6905a89c403402cafb000356fd60d1fa2ccc266aa763b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81974f828ea98ef1ffdcd146f91acd2abe36e9ead4d8b3c726c62739a6bd726(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxToolOpenApiSpecTlsConfigCaCerts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3910764fd54eb62a1e05c8eeb8942e72d56f310a2c5f7c7f11b752f4bea1c310(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fde58d5d1b7a5bc3d37bc18dfc531af5f974222fec59cbbac0f8ee6d6920c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxToolOpenApiSpecTlsConfigCaCerts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c24e6aacfaa4c63ee4d78c828954e3d61f56833566478848959187ca5c6b3661(
    value: typing.Optional[DialogflowCxToolOpenApiSpecTlsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27de6a2b1b2d3c81f8bac31067e0db4e21731eb600baef179ddcaa50d16c3ad(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41c22c2df7896f9bd87bb6937b26b663a66e20244d52bbb839851842e956c35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea60a52f7d9bf8cd648b550b34dc9ea60eb3fe04faa7935bcc46792a0ff71c6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc2bd07197e8c7056a11c5a109664ab00b024eaa1ac24dc435aaa0500cbed67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57346c8c3519082fbaaf5b37a97a32b49a3087e362f99292350f31179d5896a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c2e6fe54cbbf8327eb7c8171e75915177c5a048db3aa73050e7834c39f4159(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxToolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
