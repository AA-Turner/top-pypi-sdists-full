r'''
# `google_document_ai_warehouse_document_schema`

Refer to the Terraform Registry for docs: [`google_document_ai_warehouse_document_schema`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema).
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


class DocumentAiWarehouseDocumentSchema(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchema",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema google_document_ai_warehouse_document_schema}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        project_number: builtins.str,
        property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitions", typing.Dict[builtins.str, typing.Any]]]],
        document_is_folder: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema google_document_ai_warehouse_document_schema} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Name of the schema given by the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#display_name DocumentAiWarehouseDocumentSchema#display_name}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#location DocumentAiWarehouseDocumentSchema#location}
        :param project_number: The unique identifier of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#project_number DocumentAiWarehouseDocumentSchema#project_number}
        :param property_definitions: property_definitions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#property_definitions DocumentAiWarehouseDocumentSchema#property_definitions}
        :param document_is_folder: Tells whether the document is a folder or a typical document. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#document_is_folder DocumentAiWarehouseDocumentSchema#document_is_folder}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#id DocumentAiWarehouseDocumentSchema#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#timeouts DocumentAiWarehouseDocumentSchema#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44412add24ccbf1adfdbe529bdb9b76d31c2e7d9e023da149b18fadfc81b9c72)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DocumentAiWarehouseDocumentSchemaConfig(
            display_name=display_name,
            location=location,
            project_number=project_number,
            property_definitions=property_definitions,
            document_is_folder=document_is_folder,
            id=id,
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
        '''Generates CDKTF code for importing a DocumentAiWarehouseDocumentSchema resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DocumentAiWarehouseDocumentSchema to import.
        :param import_from_id: The id of the existing DocumentAiWarehouseDocumentSchema that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DocumentAiWarehouseDocumentSchema to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc3136d5c589014bd869499b53d2a7633c55336a413d2c9172edbccee2536fc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPropertyDefinitions")
    def put_property_definitions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddcefe3704819d7aba8951ed15e7347a9d7fa5a8c5bb1568a808f729db1ff73c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPropertyDefinitions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#create DocumentAiWarehouseDocumentSchema#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#delete DocumentAiWarehouseDocumentSchema#delete}.
        '''
        value = DocumentAiWarehouseDocumentSchemaTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDocumentIsFolder")
    def reset_document_is_folder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentIsFolder", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="propertyDefinitions")
    def property_definitions(
        self,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsList":
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsList", jsii.get(self, "propertyDefinitions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DocumentAiWarehouseDocumentSchemaTimeoutsOutputReference":
        return typing.cast("DocumentAiWarehouseDocumentSchemaTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="documentIsFolderInput")
    def document_is_folder_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "documentIsFolderInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectNumberInput")
    def project_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="propertyDefinitionsInput")
    def property_definitions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitions"]]], jsii.get(self, "propertyDefinitionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DocumentAiWarehouseDocumentSchemaTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DocumentAiWarehouseDocumentSchemaTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a31b18a0816345e0ec5311b5499f2ac23170dd372fc176fe3bf568e24d72b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentIsFolder")
    def document_is_folder(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "documentIsFolder"))

    @document_is_folder.setter
    def document_is_folder(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c15b5d2f1cd4ae95bf9c6c9787110f5059c0a17d388129fb84d1cb16dce9efe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentIsFolder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08125b1b03b903a076a4bc57ef6334cb274531c8f272da9fec6318ee3cc933a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79486966817d66d3f7f11f9b37bc8d7dac337cf72e3578cd24be28e1aad54706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectNumber")
    def project_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectNumber"))

    @project_number.setter
    def project_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e25d26075c7102d594a6e2a6a6c8190fba7c9cdcf5abf9fcacfd86d847b1398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectNumber", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaConfig",
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
        "project_number": "projectNumber",
        "property_definitions": "propertyDefinitions",
        "document_is_folder": "documentIsFolder",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class DocumentAiWarehouseDocumentSchemaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        project_number: builtins.str,
        property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitions", typing.Dict[builtins.str, typing.Any]]]],
        document_is_folder: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Name of the schema given by the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#display_name DocumentAiWarehouseDocumentSchema#display_name}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#location DocumentAiWarehouseDocumentSchema#location}
        :param project_number: The unique identifier of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#project_number DocumentAiWarehouseDocumentSchema#project_number}
        :param property_definitions: property_definitions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#property_definitions DocumentAiWarehouseDocumentSchema#property_definitions}
        :param document_is_folder: Tells whether the document is a folder or a typical document. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#document_is_folder DocumentAiWarehouseDocumentSchema#document_is_folder}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#id DocumentAiWarehouseDocumentSchema#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#timeouts DocumentAiWarehouseDocumentSchema#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DocumentAiWarehouseDocumentSchemaTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d7609ac2d57055ce8cf52dbd373cad02d2b1ab35fd9cb1983861935afc90bf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project_number", value=project_number, expected_type=type_hints["project_number"])
            check_type(argname="argument property_definitions", value=property_definitions, expected_type=type_hints["property_definitions"])
            check_type(argname="argument document_is_folder", value=document_is_folder, expected_type=type_hints["document_is_folder"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "location": location,
            "project_number": project_number,
            "property_definitions": property_definitions,
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
        if document_is_folder is not None:
            self._values["document_is_folder"] = document_is_folder
        if id is not None:
            self._values["id"] = id
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
        '''Name of the schema given by the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#display_name DocumentAiWarehouseDocumentSchema#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#location DocumentAiWarehouseDocumentSchema#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_number(self) -> builtins.str:
        '''The unique identifier of the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#project_number DocumentAiWarehouseDocumentSchema#project_number}
        '''
        result = self._values.get("project_number")
        assert result is not None, "Required property 'project_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def property_definitions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitions"]]:
        '''property_definitions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#property_definitions DocumentAiWarehouseDocumentSchema#property_definitions}
        '''
        result = self._values.get("property_definitions")
        assert result is not None, "Required property 'property_definitions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitions"]], result)

    @builtins.property
    def document_is_folder(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Tells whether the document is a folder or a typical document.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#document_is_folder DocumentAiWarehouseDocumentSchema#document_is_folder}
        '''
        result = self._values.get("document_is_folder")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#id DocumentAiWarehouseDocumentSchema#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DocumentAiWarehouseDocumentSchemaTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#timeouts DocumentAiWarehouseDocumentSchema#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "date_time_type_options": "dateTimeTypeOptions",
        "display_name": "displayName",
        "enum_type_options": "enumTypeOptions",
        "float_type_options": "floatTypeOptions",
        "integer_type_options": "integerTypeOptions",
        "is_filterable": "isFilterable",
        "is_metadata": "isMetadata",
        "is_repeatable": "isRepeatable",
        "is_required": "isRequired",
        "is_searchable": "isSearchable",
        "map_type_options": "mapTypeOptions",
        "property_type_options": "propertyTypeOptions",
        "retrieval_importance": "retrievalImportance",
        "schema_sources": "schemaSources",
        "text_type_options": "textTypeOptions",
        "timestamp_type_options": "timestampTypeOptions",
    },
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitions:
    def __init__(
        self,
        *,
        name: builtins.str,
        date_time_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        enum_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        float_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        is_filterable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_repeatable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        map_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        property_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        retrieval_importance: typing.Optional[builtins.str] = None,
        schema_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        text_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timestamp_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: The name of the metadata property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#name DocumentAiWarehouseDocumentSchema#name}
        :param date_time_type_options: date_time_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#date_time_type_options DocumentAiWarehouseDocumentSchema#date_time_type_options}
        :param display_name: The display-name for the property, used for front-end. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#display_name DocumentAiWarehouseDocumentSchema#display_name}
        :param enum_type_options: enum_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#enum_type_options DocumentAiWarehouseDocumentSchema#enum_type_options}
        :param float_type_options: float_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#float_type_options DocumentAiWarehouseDocumentSchema#float_type_options}
        :param integer_type_options: integer_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#integer_type_options DocumentAiWarehouseDocumentSchema#integer_type_options}
        :param is_filterable: Whether the property can be filtered. If this is a sub-property, all the parent properties must be marked filterable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_filterable DocumentAiWarehouseDocumentSchema#is_filterable}
        :param is_metadata: Whether the property is user supplied metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_metadata DocumentAiWarehouseDocumentSchema#is_metadata}
        :param is_repeatable: Whether the property can have multiple values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_repeatable DocumentAiWarehouseDocumentSchema#is_repeatable}
        :param is_required: Whether the property is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_required DocumentAiWarehouseDocumentSchema#is_required}
        :param is_searchable: Indicates that the property should be included in a global search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_searchable DocumentAiWarehouseDocumentSchema#is_searchable}
        :param map_type_options: map_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#map_type_options DocumentAiWarehouseDocumentSchema#map_type_options}
        :param property_type_options: property_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#property_type_options DocumentAiWarehouseDocumentSchema#property_type_options}
        :param retrieval_importance: Stores the retrieval importance. Possible values: ["HIGHEST", "HIGHER", "HIGH", "MEDIUM", "LOW", "LOWEST"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#retrieval_importance DocumentAiWarehouseDocumentSchema#retrieval_importance}
        :param schema_sources: schema_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#schema_sources DocumentAiWarehouseDocumentSchema#schema_sources}
        :param text_type_options: text_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#text_type_options DocumentAiWarehouseDocumentSchema#text_type_options}
        :param timestamp_type_options: timestamp_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#timestamp_type_options DocumentAiWarehouseDocumentSchema#timestamp_type_options}
        '''
        if isinstance(date_time_type_options, dict):
            date_time_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions(**date_time_type_options)
        if isinstance(enum_type_options, dict):
            enum_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions(**enum_type_options)
        if isinstance(float_type_options, dict):
            float_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions(**float_type_options)
        if isinstance(integer_type_options, dict):
            integer_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions(**integer_type_options)
        if isinstance(map_type_options, dict):
            map_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions(**map_type_options)
        if isinstance(property_type_options, dict):
            property_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions(**property_type_options)
        if isinstance(text_type_options, dict):
            text_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions(**text_type_options)
        if isinstance(timestamp_type_options, dict):
            timestamp_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions(**timestamp_type_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df6c8c2b3a234533b2135e3c60be0ed98222e5320106227bcf506013553464c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument date_time_type_options", value=date_time_type_options, expected_type=type_hints["date_time_type_options"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enum_type_options", value=enum_type_options, expected_type=type_hints["enum_type_options"])
            check_type(argname="argument float_type_options", value=float_type_options, expected_type=type_hints["float_type_options"])
            check_type(argname="argument integer_type_options", value=integer_type_options, expected_type=type_hints["integer_type_options"])
            check_type(argname="argument is_filterable", value=is_filterable, expected_type=type_hints["is_filterable"])
            check_type(argname="argument is_metadata", value=is_metadata, expected_type=type_hints["is_metadata"])
            check_type(argname="argument is_repeatable", value=is_repeatable, expected_type=type_hints["is_repeatable"])
            check_type(argname="argument is_required", value=is_required, expected_type=type_hints["is_required"])
            check_type(argname="argument is_searchable", value=is_searchable, expected_type=type_hints["is_searchable"])
            check_type(argname="argument map_type_options", value=map_type_options, expected_type=type_hints["map_type_options"])
            check_type(argname="argument property_type_options", value=property_type_options, expected_type=type_hints["property_type_options"])
            check_type(argname="argument retrieval_importance", value=retrieval_importance, expected_type=type_hints["retrieval_importance"])
            check_type(argname="argument schema_sources", value=schema_sources, expected_type=type_hints["schema_sources"])
            check_type(argname="argument text_type_options", value=text_type_options, expected_type=type_hints["text_type_options"])
            check_type(argname="argument timestamp_type_options", value=timestamp_type_options, expected_type=type_hints["timestamp_type_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if date_time_type_options is not None:
            self._values["date_time_type_options"] = date_time_type_options
        if display_name is not None:
            self._values["display_name"] = display_name
        if enum_type_options is not None:
            self._values["enum_type_options"] = enum_type_options
        if float_type_options is not None:
            self._values["float_type_options"] = float_type_options
        if integer_type_options is not None:
            self._values["integer_type_options"] = integer_type_options
        if is_filterable is not None:
            self._values["is_filterable"] = is_filterable
        if is_metadata is not None:
            self._values["is_metadata"] = is_metadata
        if is_repeatable is not None:
            self._values["is_repeatable"] = is_repeatable
        if is_required is not None:
            self._values["is_required"] = is_required
        if is_searchable is not None:
            self._values["is_searchable"] = is_searchable
        if map_type_options is not None:
            self._values["map_type_options"] = map_type_options
        if property_type_options is not None:
            self._values["property_type_options"] = property_type_options
        if retrieval_importance is not None:
            self._values["retrieval_importance"] = retrieval_importance
        if schema_sources is not None:
            self._values["schema_sources"] = schema_sources
        if text_type_options is not None:
            self._values["text_type_options"] = text_type_options
        if timestamp_type_options is not None:
            self._values["timestamp_type_options"] = timestamp_type_options

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the metadata property.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#name DocumentAiWarehouseDocumentSchema#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def date_time_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions"]:
        '''date_time_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#date_time_type_options DocumentAiWarehouseDocumentSchema#date_time_type_options}
        '''
        result = self._values.get("date_time_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display-name for the property, used for front-end.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#display_name DocumentAiWarehouseDocumentSchema#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enum_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions"]:
        '''enum_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#enum_type_options DocumentAiWarehouseDocumentSchema#enum_type_options}
        '''
        result = self._values.get("enum_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions"], result)

    @builtins.property
    def float_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions"]:
        '''float_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#float_type_options DocumentAiWarehouseDocumentSchema#float_type_options}
        '''
        result = self._values.get("float_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions"], result)

    @builtins.property
    def integer_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions"]:
        '''integer_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#integer_type_options DocumentAiWarehouseDocumentSchema#integer_type_options}
        '''
        result = self._values.get("integer_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions"], result)

    @builtins.property
    def is_filterable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property can be filtered. If this is a sub-property, all the parent properties must be marked filterable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_filterable DocumentAiWarehouseDocumentSchema#is_filterable}
        '''
        result = self._values.get("is_filterable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_metadata(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property is user supplied metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_metadata DocumentAiWarehouseDocumentSchema#is_metadata}
        '''
        result = self._values.get("is_metadata")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_repeatable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property can have multiple values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_repeatable DocumentAiWarehouseDocumentSchema#is_repeatable}
        '''
        result = self._values.get("is_repeatable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property is mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_required DocumentAiWarehouseDocumentSchema#is_required}
        '''
        result = self._values.get("is_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_searchable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates that the property should be included in a global search.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_searchable DocumentAiWarehouseDocumentSchema#is_searchable}
        '''
        result = self._values.get("is_searchable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def map_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions"]:
        '''map_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#map_type_options DocumentAiWarehouseDocumentSchema#map_type_options}
        '''
        result = self._values.get("map_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions"], result)

    @builtins.property
    def property_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions"]:
        '''property_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#property_type_options DocumentAiWarehouseDocumentSchema#property_type_options}
        '''
        result = self._values.get("property_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions"], result)

    @builtins.property
    def retrieval_importance(self) -> typing.Optional[builtins.str]:
        '''Stores the retrieval importance. Possible values: ["HIGHEST", "HIGHER", "HIGH", "MEDIUM", "LOW", "LOWEST"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#retrieval_importance DocumentAiWarehouseDocumentSchema#retrieval_importance}
        '''
        result = self._values.get("retrieval_importance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources"]]]:
        '''schema_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#schema_sources DocumentAiWarehouseDocumentSchema#schema_sources}
        '''
        result = self._values.get("schema_sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources"]]], result)

    @builtins.property
    def text_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions"]:
        '''text_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#text_type_options DocumentAiWarehouseDocumentSchema#text_type_options}
        '''
        result = self._values.get("text_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions"], result)

    @builtins.property
    def timestamp_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions"]:
        '''timestamp_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#timestamp_type_options DocumentAiWarehouseDocumentSchema#timestamp_type_options}
        '''
        result = self._values.get("timestamp_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01f7ecc48e122154aebdffc18cd97060d5b6991b990ef4fe8f1a5e1329bf4a61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57e5603496b3710567eb800a85873f0c6d6e9767037a4e7f4d692e851bd7c25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "possible_values": "possibleValues",
        "validation_check_disabled": "validationCheckDisabled",
    },
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions:
    def __init__(
        self,
        *,
        possible_values: typing.Sequence[builtins.str],
        validation_check_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param possible_values: List of possible enum values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#possible_values DocumentAiWarehouseDocumentSchema#possible_values}
        :param validation_check_disabled: Make sure the enum property value provided in the document is in the possile value list during document creation. The validation check runs by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#validation_check_disabled DocumentAiWarehouseDocumentSchema#validation_check_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5c001684df8336e263d15445529a5bc41695aad337760e0b24be4300a66760)
            check_type(argname="argument possible_values", value=possible_values, expected_type=type_hints["possible_values"])
            check_type(argname="argument validation_check_disabled", value=validation_check_disabled, expected_type=type_hints["validation_check_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "possible_values": possible_values,
        }
        if validation_check_disabled is not None:
            self._values["validation_check_disabled"] = validation_check_disabled

    @builtins.property
    def possible_values(self) -> typing.List[builtins.str]:
        '''List of possible enum values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#possible_values DocumentAiWarehouseDocumentSchema#possible_values}
        '''
        result = self._values.get("possible_values")
        assert result is not None, "Required property 'possible_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def validation_check_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Make sure the enum property value provided in the document is in the possile value list during document creation.

        The validation check runs by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#validation_check_disabled DocumentAiWarehouseDocumentSchema#validation_check_disabled}
        '''
        result = self._values.get("validation_check_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86b4b0a40588b0342719628a29be560e4942210e959a9fcaa3b3ba8cb2ce65cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetValidationCheckDisabled")
    def reset_validation_check_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidationCheckDisabled", []))

    @builtins.property
    @jsii.member(jsii_name="possibleValuesInput")
    def possible_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "possibleValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="validationCheckDisabledInput")
    def validation_check_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validationCheckDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="possibleValues")
    def possible_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "possibleValues"))

    @possible_values.setter
    def possible_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8711da901a3b53f22a6ca5e7f7183208e1e4dce35fc4c6fe0293718496c3564a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "possibleValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validationCheckDisabled")
    def validation_check_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validationCheckDisabled"))

    @validation_check_disabled.setter
    def validation_check_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e753337aa895a276e6e26415e9adf83ce91f09bfb5488651ec5b0ee4973319ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validationCheckDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3f2f8ab37c6d524ffb22616bafe6701b61a823506fb0a1d2b7b0a20d4c0ffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c10600c583a9edec0102c359f05a3881421f123a3e1ac91b05cb95c15ea23b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b27c3576fb2eb82e3d72ed65c4fcafb8e3f79a510795c0bc8db9d6184e85d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75ed1028983c634feb3c91da21adf422a3e831f1fc3adaf945faeb1101b51f6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90fa29ad4296adec39d97f2a430135e6f95e3be618f93dc8fa5dee53e3338e9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ada366f67defcd42b528099093ba92d09359b4e13f80e8a789d542d9c631a0f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647bd272c03da1ba8ab7390f15d262d58f62c12900c74c87e84af701350c15be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8808b5296996c580c290028e2df5bf7f573cfa3afad7b9f034065a87cde0c635)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5273a8c0e658f42ac7639c1a31f2ed832c98bc98f38ae497d6b139f93c652712)
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
            type_hints = typing.get_type_hints(_typecheckingstub__415f7985567f14b9e368029bb1e2f4020d781408bf12ff4f7f63f73b05f0b73c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf24d5653edc46496e44492fa23b51f866bcdc4e82f773aa8d0490c696fe52f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__408794ac35a6b4ea544d2791a33555caa9d7c72f8c9ca5c869623c863f30b53d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a8ae6e5188ec422097192d59ff3f2741c09e6407fbf0c14e24b60a43df32c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b8cf57ff138b2bc0614362fd1d1e6fca785ec525636b9c0423ffab09e758bfd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDateTimeTypeOptions")
    def put_date_time_type_options(self) -> None:
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putDateTimeTypeOptions", [value]))

    @jsii.member(jsii_name="putEnumTypeOptions")
    def put_enum_type_options(
        self,
        *,
        possible_values: typing.Sequence[builtins.str],
        validation_check_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param possible_values: List of possible enum values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#possible_values DocumentAiWarehouseDocumentSchema#possible_values}
        :param validation_check_disabled: Make sure the enum property value provided in the document is in the possile value list during document creation. The validation check runs by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#validation_check_disabled DocumentAiWarehouseDocumentSchema#validation_check_disabled}
        '''
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions(
            possible_values=possible_values,
            validation_check_disabled=validation_check_disabled,
        )

        return typing.cast(None, jsii.invoke(self, "putEnumTypeOptions", [value]))

    @jsii.member(jsii_name="putFloatTypeOptions")
    def put_float_type_options(self) -> None:
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putFloatTypeOptions", [value]))

    @jsii.member(jsii_name="putIntegerTypeOptions")
    def put_integer_type_options(self) -> None:
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putIntegerTypeOptions", [value]))

    @jsii.member(jsii_name="putMapTypeOptions")
    def put_map_type_options(self) -> None:
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putMapTypeOptions", [value]))

    @jsii.member(jsii_name="putPropertyTypeOptions")
    def put_property_type_options(
        self,
        *,
        property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param property_definitions: property_definitions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#property_definitions DocumentAiWarehouseDocumentSchema#property_definitions}
        '''
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions(
            property_definitions=property_definitions
        )

        return typing.cast(None, jsii.invoke(self, "putPropertyTypeOptions", [value]))

    @jsii.member(jsii_name="putSchemaSources")
    def put_schema_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f01445f0a6b9e8d40badf89bf3182d24657d54818756a6e4d96732a39263e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchemaSources", [value]))

    @jsii.member(jsii_name="putTextTypeOptions")
    def put_text_type_options(self) -> None:
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putTextTypeOptions", [value]))

    @jsii.member(jsii_name="putTimestampTypeOptions")
    def put_timestamp_type_options(self) -> None:
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putTimestampTypeOptions", [value]))

    @jsii.member(jsii_name="resetDateTimeTypeOptions")
    def reset_date_time_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateTimeTypeOptions", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetEnumTypeOptions")
    def reset_enum_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnumTypeOptions", []))

    @jsii.member(jsii_name="resetFloatTypeOptions")
    def reset_float_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFloatTypeOptions", []))

    @jsii.member(jsii_name="resetIntegerTypeOptions")
    def reset_integer_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegerTypeOptions", []))

    @jsii.member(jsii_name="resetIsFilterable")
    def reset_is_filterable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsFilterable", []))

    @jsii.member(jsii_name="resetIsMetadata")
    def reset_is_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsMetadata", []))

    @jsii.member(jsii_name="resetIsRepeatable")
    def reset_is_repeatable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsRepeatable", []))

    @jsii.member(jsii_name="resetIsRequired")
    def reset_is_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsRequired", []))

    @jsii.member(jsii_name="resetIsSearchable")
    def reset_is_searchable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSearchable", []))

    @jsii.member(jsii_name="resetMapTypeOptions")
    def reset_map_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapTypeOptions", []))

    @jsii.member(jsii_name="resetPropertyTypeOptions")
    def reset_property_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPropertyTypeOptions", []))

    @jsii.member(jsii_name="resetRetrievalImportance")
    def reset_retrieval_importance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetrievalImportance", []))

    @jsii.member(jsii_name="resetSchemaSources")
    def reset_schema_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaSources", []))

    @jsii.member(jsii_name="resetTextTypeOptions")
    def reset_text_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTextTypeOptions", []))

    @jsii.member(jsii_name="resetTimestampTypeOptions")
    def reset_timestamp_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampTypeOptions", []))

    @builtins.property
    @jsii.member(jsii_name="dateTimeTypeOptions")
    def date_time_type_options(
        self,
    ) -> DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptionsOutputReference:
        return typing.cast(DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptionsOutputReference, jsii.get(self, "dateTimeTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="enumTypeOptions")
    def enum_type_options(
        self,
    ) -> DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptionsOutputReference:
        return typing.cast(DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptionsOutputReference, jsii.get(self, "enumTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="floatTypeOptions")
    def float_type_options(
        self,
    ) -> DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptionsOutputReference:
        return typing.cast(DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptionsOutputReference, jsii.get(self, "floatTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="integerTypeOptions")
    def integer_type_options(
        self,
    ) -> DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptionsOutputReference:
        return typing.cast(DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptionsOutputReference, jsii.get(self, "integerTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="mapTypeOptions")
    def map_type_options(
        self,
    ) -> DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptionsOutputReference:
        return typing.cast(DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptionsOutputReference, jsii.get(self, "mapTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="propertyTypeOptions")
    def property_type_options(
        self,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsOutputReference":
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsOutputReference", jsii.get(self, "propertyTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="schemaSources")
    def schema_sources(
        self,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesList":
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesList", jsii.get(self, "schemaSources"))

    @builtins.property
    @jsii.member(jsii_name="textTypeOptions")
    def text_type_options(
        self,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptionsOutputReference":
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptionsOutputReference", jsii.get(self, "textTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeOptions")
    def timestamp_type_options(
        self,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptionsOutputReference":
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptionsOutputReference", jsii.get(self, "timestampTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="dateTimeTypeOptionsInput")
    def date_time_type_options_input(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions], jsii.get(self, "dateTimeTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enumTypeOptionsInput")
    def enum_type_options_input(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions], jsii.get(self, "enumTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="floatTypeOptionsInput")
    def float_type_options_input(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions], jsii.get(self, "floatTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="integerTypeOptionsInput")
    def integer_type_options_input(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions], jsii.get(self, "integerTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="isFilterableInput")
    def is_filterable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isFilterableInput"))

    @builtins.property
    @jsii.member(jsii_name="isMetadataInput")
    def is_metadata_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="isRepeatableInput")
    def is_repeatable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isRepeatableInput"))

    @builtins.property
    @jsii.member(jsii_name="isRequiredInput")
    def is_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="isSearchableInput")
    def is_searchable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSearchableInput"))

    @builtins.property
    @jsii.member(jsii_name="mapTypeOptionsInput")
    def map_type_options_input(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions], jsii.get(self, "mapTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="propertyTypeOptionsInput")
    def property_type_options_input(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions"]:
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions"], jsii.get(self, "propertyTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="retrievalImportanceInput")
    def retrieval_importance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retrievalImportanceInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaSourcesInput")
    def schema_sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources"]]], jsii.get(self, "schemaSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="textTypeOptionsInput")
    def text_type_options_input(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions"]:
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions"], jsii.get(self, "textTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeOptionsInput")
    def timestamp_type_options_input(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions"]:
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions"], jsii.get(self, "timestampTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf55e76097c9242613f66e5e6fc97684e0f35894781f811c5efc9eb9698b98e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isFilterable")
    def is_filterable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isFilterable"))

    @is_filterable.setter
    def is_filterable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a0f2692df3b9eaf0a057983eec1c8f2059a846aebab11b7ae71ef15a78773d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isFilterable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isMetadata")
    def is_metadata(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isMetadata"))

    @is_metadata.setter
    def is_metadata(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24125284e70dd131c9f3072a62c4834196b0c4c2f8e90f270dfb30e8e318d993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isMetadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isRepeatable")
    def is_repeatable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isRepeatable"))

    @is_repeatable.setter
    def is_repeatable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7001f45a50386f37ecd0ce31779accfb08a3e1da9a1f88f24c3c7ca06c27f21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isRepeatable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isRequired")
    def is_required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isRequired"))

    @is_required.setter
    def is_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6264549051867290036c9a8a67908724e2d87de9c25b36964beaae1c83aea1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSearchable")
    def is_searchable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSearchable"))

    @is_searchable.setter
    def is_searchable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9ef264fd9addef50453466c0a0f705fabc416df130f50bbe44c55602722c278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSearchable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff110739be5fc77f24ac4e0198ecd4e8b77183f8bc45b7c37e406b1d58c9943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retrievalImportance")
    def retrieval_importance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retrievalImportance"))

    @retrieval_importance.setter
    def retrieval_importance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62d51607f8cc39865dd3f60783da3205443283b3620f4d18744ef07c9ba4cd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retrievalImportance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2daa6023efd3678e7fd0d23ff21ce231a8a5efa4f89f35be474cd16957f79a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions",
    jsii_struct_bases=[],
    name_mapping={"property_definitions": "propertyDefinitions"},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions:
    def __init__(
        self,
        *,
        property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param property_definitions: property_definitions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#property_definitions DocumentAiWarehouseDocumentSchema#property_definitions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a66766e1229b0e62bd6a215a12ebfe47a83880c84831698296fe5778a529f8d)
            check_type(argname="argument property_definitions", value=property_definitions, expected_type=type_hints["property_definitions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "property_definitions": property_definitions,
        }

    @builtins.property
    def property_definitions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions"]]:
        '''property_definitions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#property_definitions DocumentAiWarehouseDocumentSchema#property_definitions}
        '''
        result = self._values.get("property_definitions")
        assert result is not None, "Required property 'property_definitions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf374afe26003fa33ed9d1764a2dc650d65c35bafe0fe4556008efc9793523ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPropertyDefinitions")
    def put_property_definitions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f64a7634e42cd7007bda48f7153cdeeac438f268c7bcf48a7c4546d81a45c74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPropertyDefinitions", [value]))

    @builtins.property
    @jsii.member(jsii_name="propertyDefinitions")
    def property_definitions(
        self,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsList":
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsList", jsii.get(self, "propertyDefinitions"))

    @builtins.property
    @jsii.member(jsii_name="propertyDefinitionsInput")
    def property_definitions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions"]]], jsii.get(self, "propertyDefinitionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c6e4e008945ce3a7b758e3cc797211211c3316581dffe6bc492624b816c7c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "date_time_type_options": "dateTimeTypeOptions",
        "display_name": "displayName",
        "enum_type_options": "enumTypeOptions",
        "float_type_options": "floatTypeOptions",
        "integer_type_options": "integerTypeOptions",
        "is_filterable": "isFilterable",
        "is_metadata": "isMetadata",
        "is_repeatable": "isRepeatable",
        "is_required": "isRequired",
        "is_searchable": "isSearchable",
        "map_type_options": "mapTypeOptions",
        "retrieval_importance": "retrievalImportance",
        "schema_sources": "schemaSources",
        "text_type_options": "textTypeOptions",
        "timestamp_type_options": "timestampTypeOptions",
    },
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions:
    def __init__(
        self,
        *,
        name: builtins.str,
        date_time_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        enum_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        float_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        is_filterable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_repeatable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        map_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        retrieval_importance: typing.Optional[builtins.str] = None,
        schema_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        text_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timestamp_type_options: typing.Optional[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: The name of the metadata property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#name DocumentAiWarehouseDocumentSchema#name}
        :param date_time_type_options: date_time_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#date_time_type_options DocumentAiWarehouseDocumentSchema#date_time_type_options}
        :param display_name: The display-name for the property, used for front-end. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#display_name DocumentAiWarehouseDocumentSchema#display_name}
        :param enum_type_options: enum_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#enum_type_options DocumentAiWarehouseDocumentSchema#enum_type_options}
        :param float_type_options: float_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#float_type_options DocumentAiWarehouseDocumentSchema#float_type_options}
        :param integer_type_options: integer_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#integer_type_options DocumentAiWarehouseDocumentSchema#integer_type_options}
        :param is_filterable: Whether the property can be filtered. If this is a sub-property, all the parent properties must be marked filterable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_filterable DocumentAiWarehouseDocumentSchema#is_filterable}
        :param is_metadata: Whether the property is user supplied metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_metadata DocumentAiWarehouseDocumentSchema#is_metadata}
        :param is_repeatable: Whether the property can have multiple values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_repeatable DocumentAiWarehouseDocumentSchema#is_repeatable}
        :param is_required: Whether the property is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_required DocumentAiWarehouseDocumentSchema#is_required}
        :param is_searchable: Indicates that the property should be included in a global search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_searchable DocumentAiWarehouseDocumentSchema#is_searchable}
        :param map_type_options: map_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#map_type_options DocumentAiWarehouseDocumentSchema#map_type_options}
        :param retrieval_importance: Stores the retrieval importance. Possible values: ["HIGHEST", "HIGHER", "HIGH", "MEDIUM", "LOW", "LOWEST"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#retrieval_importance DocumentAiWarehouseDocumentSchema#retrieval_importance}
        :param schema_sources: schema_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#schema_sources DocumentAiWarehouseDocumentSchema#schema_sources}
        :param text_type_options: text_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#text_type_options DocumentAiWarehouseDocumentSchema#text_type_options}
        :param timestamp_type_options: timestamp_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#timestamp_type_options DocumentAiWarehouseDocumentSchema#timestamp_type_options}
        '''
        if isinstance(date_time_type_options, dict):
            date_time_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions(**date_time_type_options)
        if isinstance(enum_type_options, dict):
            enum_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions(**enum_type_options)
        if isinstance(float_type_options, dict):
            float_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions(**float_type_options)
        if isinstance(integer_type_options, dict):
            integer_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions(**integer_type_options)
        if isinstance(map_type_options, dict):
            map_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions(**map_type_options)
        if isinstance(text_type_options, dict):
            text_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions(**text_type_options)
        if isinstance(timestamp_type_options, dict):
            timestamp_type_options = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions(**timestamp_type_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9a598be4c09abd2e512c758a0c9163601c27cdbfebbee589b791a34af01c31)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument date_time_type_options", value=date_time_type_options, expected_type=type_hints["date_time_type_options"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enum_type_options", value=enum_type_options, expected_type=type_hints["enum_type_options"])
            check_type(argname="argument float_type_options", value=float_type_options, expected_type=type_hints["float_type_options"])
            check_type(argname="argument integer_type_options", value=integer_type_options, expected_type=type_hints["integer_type_options"])
            check_type(argname="argument is_filterable", value=is_filterable, expected_type=type_hints["is_filterable"])
            check_type(argname="argument is_metadata", value=is_metadata, expected_type=type_hints["is_metadata"])
            check_type(argname="argument is_repeatable", value=is_repeatable, expected_type=type_hints["is_repeatable"])
            check_type(argname="argument is_required", value=is_required, expected_type=type_hints["is_required"])
            check_type(argname="argument is_searchable", value=is_searchable, expected_type=type_hints["is_searchable"])
            check_type(argname="argument map_type_options", value=map_type_options, expected_type=type_hints["map_type_options"])
            check_type(argname="argument retrieval_importance", value=retrieval_importance, expected_type=type_hints["retrieval_importance"])
            check_type(argname="argument schema_sources", value=schema_sources, expected_type=type_hints["schema_sources"])
            check_type(argname="argument text_type_options", value=text_type_options, expected_type=type_hints["text_type_options"])
            check_type(argname="argument timestamp_type_options", value=timestamp_type_options, expected_type=type_hints["timestamp_type_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if date_time_type_options is not None:
            self._values["date_time_type_options"] = date_time_type_options
        if display_name is not None:
            self._values["display_name"] = display_name
        if enum_type_options is not None:
            self._values["enum_type_options"] = enum_type_options
        if float_type_options is not None:
            self._values["float_type_options"] = float_type_options
        if integer_type_options is not None:
            self._values["integer_type_options"] = integer_type_options
        if is_filterable is not None:
            self._values["is_filterable"] = is_filterable
        if is_metadata is not None:
            self._values["is_metadata"] = is_metadata
        if is_repeatable is not None:
            self._values["is_repeatable"] = is_repeatable
        if is_required is not None:
            self._values["is_required"] = is_required
        if is_searchable is not None:
            self._values["is_searchable"] = is_searchable
        if map_type_options is not None:
            self._values["map_type_options"] = map_type_options
        if retrieval_importance is not None:
            self._values["retrieval_importance"] = retrieval_importance
        if schema_sources is not None:
            self._values["schema_sources"] = schema_sources
        if text_type_options is not None:
            self._values["text_type_options"] = text_type_options
        if timestamp_type_options is not None:
            self._values["timestamp_type_options"] = timestamp_type_options

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the metadata property.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#name DocumentAiWarehouseDocumentSchema#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def date_time_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions"]:
        '''date_time_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#date_time_type_options DocumentAiWarehouseDocumentSchema#date_time_type_options}
        '''
        result = self._values.get("date_time_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display-name for the property, used for front-end.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#display_name DocumentAiWarehouseDocumentSchema#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enum_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions"]:
        '''enum_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#enum_type_options DocumentAiWarehouseDocumentSchema#enum_type_options}
        '''
        result = self._values.get("enum_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions"], result)

    @builtins.property
    def float_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions"]:
        '''float_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#float_type_options DocumentAiWarehouseDocumentSchema#float_type_options}
        '''
        result = self._values.get("float_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions"], result)

    @builtins.property
    def integer_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions"]:
        '''integer_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#integer_type_options DocumentAiWarehouseDocumentSchema#integer_type_options}
        '''
        result = self._values.get("integer_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions"], result)

    @builtins.property
    def is_filterable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property can be filtered. If this is a sub-property, all the parent properties must be marked filterable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_filterable DocumentAiWarehouseDocumentSchema#is_filterable}
        '''
        result = self._values.get("is_filterable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_metadata(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property is user supplied metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_metadata DocumentAiWarehouseDocumentSchema#is_metadata}
        '''
        result = self._values.get("is_metadata")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_repeatable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property can have multiple values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_repeatable DocumentAiWarehouseDocumentSchema#is_repeatable}
        '''
        result = self._values.get("is_repeatable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property is mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_required DocumentAiWarehouseDocumentSchema#is_required}
        '''
        result = self._values.get("is_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_searchable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates that the property should be included in a global search.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#is_searchable DocumentAiWarehouseDocumentSchema#is_searchable}
        '''
        result = self._values.get("is_searchable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def map_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions"]:
        '''map_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#map_type_options DocumentAiWarehouseDocumentSchema#map_type_options}
        '''
        result = self._values.get("map_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions"], result)

    @builtins.property
    def retrieval_importance(self) -> typing.Optional[builtins.str]:
        '''Stores the retrieval importance. Possible values: ["HIGHEST", "HIGHER", "HIGH", "MEDIUM", "LOW", "LOWEST"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#retrieval_importance DocumentAiWarehouseDocumentSchema#retrieval_importance}
        '''
        result = self._values.get("retrieval_importance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources"]]]:
        '''schema_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#schema_sources DocumentAiWarehouseDocumentSchema#schema_sources}
        '''
        result = self._values.get("schema_sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources"]]], result)

    @builtins.property
    def text_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions"]:
        '''text_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#text_type_options DocumentAiWarehouseDocumentSchema#text_type_options}
        '''
        result = self._values.get("text_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions"], result)

    @builtins.property
    def timestamp_type_options(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions"]:
        '''timestamp_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#timestamp_type_options DocumentAiWarehouseDocumentSchema#timestamp_type_options}
        '''
        result = self._values.get("timestamp_type_options")
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8e96067373be4a436552a316dd335436db7bcac6b6c1ac694812e3c3be25df3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1c3afe78913814956e324b6b40a5ed16e87827216a9a892fbb6644ea4e6fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "possible_values": "possibleValues",
        "validation_check_disabled": "validationCheckDisabled",
    },
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions:
    def __init__(
        self,
        *,
        possible_values: typing.Sequence[builtins.str],
        validation_check_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param possible_values: List of possible enum values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#possible_values DocumentAiWarehouseDocumentSchema#possible_values}
        :param validation_check_disabled: Make sure the enum property value provided in the document is in the possile value list during document creation. The validation check runs by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#validation_check_disabled DocumentAiWarehouseDocumentSchema#validation_check_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__170ea08a55f7da3172ca0c1d50ddfc041f7e79afd73ec9a4d43e90db3a076722)
            check_type(argname="argument possible_values", value=possible_values, expected_type=type_hints["possible_values"])
            check_type(argname="argument validation_check_disabled", value=validation_check_disabled, expected_type=type_hints["validation_check_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "possible_values": possible_values,
        }
        if validation_check_disabled is not None:
            self._values["validation_check_disabled"] = validation_check_disabled

    @builtins.property
    def possible_values(self) -> typing.List[builtins.str]:
        '''List of possible enum values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#possible_values DocumentAiWarehouseDocumentSchema#possible_values}
        '''
        result = self._values.get("possible_values")
        assert result is not None, "Required property 'possible_values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def validation_check_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Make sure the enum property value provided in the document is in the possile value list during document creation.

        The validation check runs by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#validation_check_disabled DocumentAiWarehouseDocumentSchema#validation_check_disabled}
        '''
        result = self._values.get("validation_check_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__833573e7cd41d4eb4262491b81a13a63cef0817110ea72be0f340d011fdf91d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetValidationCheckDisabled")
    def reset_validation_check_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidationCheckDisabled", []))

    @builtins.property
    @jsii.member(jsii_name="possibleValuesInput")
    def possible_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "possibleValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="validationCheckDisabledInput")
    def validation_check_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validationCheckDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="possibleValues")
    def possible_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "possibleValues"))

    @possible_values.setter
    def possible_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e0eb2a3d2efc37b453044b6b415e737fe85ec9a93d900a2b0ac308e46674ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "possibleValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validationCheckDisabled")
    def validation_check_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validationCheckDisabled"))

    @validation_check_disabled.setter
    def validation_check_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4f9dc6d979eb9c3b564897322bf6920ad8af29a19628b6ebd94343b639b120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validationCheckDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb83f4a1086a56671eafd0803644d364ee47924ae7057c64c2f7c3824e8864d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8155229a09526eb66d93aece52d4c808a6aed3ae191013def8c11db29d67c796)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61047bd6b883dd12a7c4b5dd245460943a8cf9d5aa58b846a504ddea5522d332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26a610600b720a889676de56097e42f996cff3006733e32c4d032c80dcee9248)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a26eaec6d932717a31f035086b667e95ca6a1f457e3ae67c56a0ce7da2e2642b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1de661cbe81553e0327857c1607838e99034fafd710c5c5108614a9fcbfa53c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44bd415329cc78c3370aa58c5c5cb2506298a6c60d49ce612f1edeb19c2c2478)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cf39f71350cd6e9f0dae65b9b27f2c40d60147c20e47fef1221dfe3afbd4575)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfdf828af5eaef19f68f8b2768db90940245b9340aab0a5f7481c992deb79210)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6cd56edddf1d8f403a85ab98efaac02ddb5c1b17f69640d89b6f3c4ced8a1da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8823bc1dc5ef9aee406415c84f550a40467ab067c3509dcb707c036be7aec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__299d75d58017ba9c1195251682cfe48b4dcb8e54f3325753519f7cbda1bb27a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c093f3666d736cb3a575bb802e5b6f09bc421752d96906c3dbdc10503d0ff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2eaa1c0d573fe33a40e20eda78b39589c376c7e63e406e3fcdc338046d7836d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDateTimeTypeOptions")
    def put_date_time_type_options(self) -> None:
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putDateTimeTypeOptions", [value]))

    @jsii.member(jsii_name="putEnumTypeOptions")
    def put_enum_type_options(
        self,
        *,
        possible_values: typing.Sequence[builtins.str],
        validation_check_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param possible_values: List of possible enum values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#possible_values DocumentAiWarehouseDocumentSchema#possible_values}
        :param validation_check_disabled: Make sure the enum property value provided in the document is in the possile value list during document creation. The validation check runs by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#validation_check_disabled DocumentAiWarehouseDocumentSchema#validation_check_disabled}
        '''
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions(
            possible_values=possible_values,
            validation_check_disabled=validation_check_disabled,
        )

        return typing.cast(None, jsii.invoke(self, "putEnumTypeOptions", [value]))

    @jsii.member(jsii_name="putFloatTypeOptions")
    def put_float_type_options(self) -> None:
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putFloatTypeOptions", [value]))

    @jsii.member(jsii_name="putIntegerTypeOptions")
    def put_integer_type_options(self) -> None:
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putIntegerTypeOptions", [value]))

    @jsii.member(jsii_name="putMapTypeOptions")
    def put_map_type_options(self) -> None:
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putMapTypeOptions", [value]))

    @jsii.member(jsii_name="putSchemaSources")
    def put_schema_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd40e00135a6c4fbe5d962fe283c3f8f986d16657ac98a053d6dd0f936ffdabb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchemaSources", [value]))

    @jsii.member(jsii_name="putTextTypeOptions")
    def put_text_type_options(self) -> None:
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putTextTypeOptions", [value]))

    @jsii.member(jsii_name="putTimestampTypeOptions")
    def put_timestamp_type_options(self) -> None:
        value = DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putTimestampTypeOptions", [value]))

    @jsii.member(jsii_name="resetDateTimeTypeOptions")
    def reset_date_time_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateTimeTypeOptions", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetEnumTypeOptions")
    def reset_enum_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnumTypeOptions", []))

    @jsii.member(jsii_name="resetFloatTypeOptions")
    def reset_float_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFloatTypeOptions", []))

    @jsii.member(jsii_name="resetIntegerTypeOptions")
    def reset_integer_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegerTypeOptions", []))

    @jsii.member(jsii_name="resetIsFilterable")
    def reset_is_filterable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsFilterable", []))

    @jsii.member(jsii_name="resetIsMetadata")
    def reset_is_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsMetadata", []))

    @jsii.member(jsii_name="resetIsRepeatable")
    def reset_is_repeatable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsRepeatable", []))

    @jsii.member(jsii_name="resetIsRequired")
    def reset_is_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsRequired", []))

    @jsii.member(jsii_name="resetIsSearchable")
    def reset_is_searchable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSearchable", []))

    @jsii.member(jsii_name="resetMapTypeOptions")
    def reset_map_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapTypeOptions", []))

    @jsii.member(jsii_name="resetRetrievalImportance")
    def reset_retrieval_importance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetrievalImportance", []))

    @jsii.member(jsii_name="resetSchemaSources")
    def reset_schema_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaSources", []))

    @jsii.member(jsii_name="resetTextTypeOptions")
    def reset_text_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTextTypeOptions", []))

    @jsii.member(jsii_name="resetTimestampTypeOptions")
    def reset_timestamp_type_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampTypeOptions", []))

    @builtins.property
    @jsii.member(jsii_name="dateTimeTypeOptions")
    def date_time_type_options(
        self,
    ) -> DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptionsOutputReference:
        return typing.cast(DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptionsOutputReference, jsii.get(self, "dateTimeTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="enumTypeOptions")
    def enum_type_options(
        self,
    ) -> DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptionsOutputReference:
        return typing.cast(DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptionsOutputReference, jsii.get(self, "enumTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="floatTypeOptions")
    def float_type_options(
        self,
    ) -> DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptionsOutputReference:
        return typing.cast(DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptionsOutputReference, jsii.get(self, "floatTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="integerTypeOptions")
    def integer_type_options(
        self,
    ) -> DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptionsOutputReference:
        return typing.cast(DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptionsOutputReference, jsii.get(self, "integerTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="mapTypeOptions")
    def map_type_options(
        self,
    ) -> DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptionsOutputReference:
        return typing.cast(DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptionsOutputReference, jsii.get(self, "mapTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="schemaSources")
    def schema_sources(
        self,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesList":
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesList", jsii.get(self, "schemaSources"))

    @builtins.property
    @jsii.member(jsii_name="textTypeOptions")
    def text_type_options(
        self,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptionsOutputReference":
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptionsOutputReference", jsii.get(self, "textTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeOptions")
    def timestamp_type_options(
        self,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptionsOutputReference":
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptionsOutputReference", jsii.get(self, "timestampTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="dateTimeTypeOptionsInput")
    def date_time_type_options_input(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions], jsii.get(self, "dateTimeTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enumTypeOptionsInput")
    def enum_type_options_input(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions], jsii.get(self, "enumTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="floatTypeOptionsInput")
    def float_type_options_input(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions], jsii.get(self, "floatTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="integerTypeOptionsInput")
    def integer_type_options_input(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions], jsii.get(self, "integerTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="isFilterableInput")
    def is_filterable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isFilterableInput"))

    @builtins.property
    @jsii.member(jsii_name="isMetadataInput")
    def is_metadata_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="isRepeatableInput")
    def is_repeatable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isRepeatableInput"))

    @builtins.property
    @jsii.member(jsii_name="isRequiredInput")
    def is_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="isSearchableInput")
    def is_searchable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSearchableInput"))

    @builtins.property
    @jsii.member(jsii_name="mapTypeOptionsInput")
    def map_type_options_input(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions], jsii.get(self, "mapTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="retrievalImportanceInput")
    def retrieval_importance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retrievalImportanceInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaSourcesInput")
    def schema_sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources"]]], jsii.get(self, "schemaSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="textTypeOptionsInput")
    def text_type_options_input(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions"]:
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions"], jsii.get(self, "textTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeOptionsInput")
    def timestamp_type_options_input(
        self,
    ) -> typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions"]:
        return typing.cast(typing.Optional["DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions"], jsii.get(self, "timestampTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1412beea5deccec3eeeb9da02c6b5106f24ccc877de90f3ae093f048255a6ecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isFilterable")
    def is_filterable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isFilterable"))

    @is_filterable.setter
    def is_filterable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__559aca631b0b304cd4c24173926791a203993c507d10910a7f180fc97f198451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isFilterable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isMetadata")
    def is_metadata(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isMetadata"))

    @is_metadata.setter
    def is_metadata(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6919082e4d3c455176a478737d65a5a042c617bbda5cc0233e319cf3feb46907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isMetadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isRepeatable")
    def is_repeatable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isRepeatable"))

    @is_repeatable.setter
    def is_repeatable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c947fd8db5dfad7f28b4c800553423e145e64ff510474e12d92c75c3148a98aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isRepeatable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isRequired")
    def is_required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isRequired"))

    @is_required.setter
    def is_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a858873a53bb73a7a1b1afa668114c7b41ccf570b670797bb3ab5eeca2f42c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSearchable")
    def is_searchable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSearchable"))

    @is_searchable.setter
    def is_searchable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abba4d8e6b32a1ca47e36048e0ec4c8b8b886e95650fe318e7e7f1605d8a934f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSearchable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbd7236d477dd346a90e5079bda69cabeb68442809ebd5b8e945cfd775475692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retrievalImportance")
    def retrieval_importance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retrievalImportance"))

    @retrieval_importance.setter
    def retrieval_importance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91010ed9fb0e887214e4e1815052d2fc64775b55c80a2dd27427b986efa8036f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retrievalImportance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b8c250ec766007abb920c13936356f85a2e2cb95ef50643539ac01057a09496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "processor_type": "processorType"},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        processor_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The schema name in the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#name DocumentAiWarehouseDocumentSchema#name}
        :param processor_type: The Doc AI processor type name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#processor_type DocumentAiWarehouseDocumentSchema#processor_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8076039499deac37b7f0fa6983be8c449ad6a4be7de2b0bbfc5c538ed540b0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument processor_type", value=processor_type, expected_type=type_hints["processor_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if processor_type is not None:
            self._values["processor_type"] = processor_type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The schema name in the source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#name DocumentAiWarehouseDocumentSchema#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processor_type(self) -> typing.Optional[builtins.str]:
        '''The Doc AI processor type name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#processor_type DocumentAiWarehouseDocumentSchema#processor_type}
        '''
        result = self._values.get("processor_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf12fb946bf099e8ad73253bb1d4cfc32ffa7f8b2049573fa5fe641783e7facc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7017e4ceb590c5a20bb42fad3a789f69392154391028d1cc8e4c76529c0f68)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f089bc70971755196bf28cd8bc1ae46a3a83459f3453e18665fd0f55b2252cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34b66bb3335509addb367ce160f7033fe4364e823d12f4127038b5994543e0c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62de88addf50f949122bd680b523494957d44d0c6653107276103bc884a69f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe1f8a5e8350ec147bde324a38d541d3cff90cf2aa492e5f8012f038e9989f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5258859c561f7ea3d961292dc8c74271b688df529152539f5fb13480db786066)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProcessorType")
    def reset_processor_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessorType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="processorTypeInput")
    def processor_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "processorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a36076e2b43dc2c486c51390d7b581e724ff438d1bd518431063dda81bc138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="processorType")
    def processor_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processorType"))

    @processor_type.setter
    def processor_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea04876422dff17b78790675612183b05a6596c6e007696564fafa00319f435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "processorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f86a947b1d3161c83cf6c356ef1c6a8876adcc3f0fa54aea283982b2d378cee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fa26a96c966396b72964616d3370a06b3c5451c7bdce22595b99b27f5eba895)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5803687a8c784c95cce1744c3350687b4acb2bb5c5bc86fa96c3820c69bba290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c6648fb3390f2bf31263dcc6014d3229c95d4e809d42c17f3a669cfe925ddcd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a791b4e0c5461b3de290e11a23fb6398f83e71a4c08134565a6b3adc8aed7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "processor_type": "processorType"},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        processor_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The schema name in the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#name DocumentAiWarehouseDocumentSchema#name}
        :param processor_type: The Doc AI processor type name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#processor_type DocumentAiWarehouseDocumentSchema#processor_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aeb682281abda81b9bd3c9353a0e4646da85407b630f1c6baf68a18e28bd194)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument processor_type", value=processor_type, expected_type=type_hints["processor_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if processor_type is not None:
            self._values["processor_type"] = processor_type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The schema name in the source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#name DocumentAiWarehouseDocumentSchema#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processor_type(self) -> typing.Optional[builtins.str]:
        '''The Doc AI processor type name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#processor_type DocumentAiWarehouseDocumentSchema#processor_type}
        '''
        result = self._values.get("processor_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__985022f4dc2ef7d61b72b62cdbb99e6b9240f2527ee5acc6552f715c20378132)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc83e13fb91caa8a40f525f2930dcf655dac1e7e8c4ff6511159029d8907a598)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b9107829eb7c82fd91204c5d13362b90094ca2c854f623efacdf81e83c5be9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__653ec8c843eadb0f235ecc8f45f82bb5df82372fdb0ea7a44819e695b2f8fde2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58613c13b049a2a248f2ff0a6f690debcc247c3571b3a463a60f58b0fe43293c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8010ef82726a054f4089338e54a253e1cd5da1e7e7de75724b84c0f8ce67cb55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ca04618106a23f33e4e6bc6740f8325b81ea3b4b4f70b87a37a5688850a837c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProcessorType")
    def reset_processor_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessorType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="processorTypeInput")
    def processor_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "processorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1efe73a6832877dd6e4d1eda6e0c02f7006d4aedae6ba9ccfcd18703bd2bcf12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="processorType")
    def processor_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processorType"))

    @processor_type.setter
    def processor_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120b089ee6f25e79aa278cdd42e2539f3dc1dce9b2313e22da8d0d45210290b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "processorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ce25eaf3b9ff791b1481c860fb5d3f2da3ab3f2e66f3f1aae81ee40c4ff236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a6f3a09329a18324cfee7f53a4dba0643026b4d94a6faa4bf1a1c0a9cea6897)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f26be2ae359c74735b67f0da4182b6b645f9e583f9c616fc6323f1ca1a6064e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__111349344ecc7b2892d81423033fe0969e8a00672d49ac224cfa7333e15cc0d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions]:
        return typing.cast(typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02079c3041bb81b5d021e8ecccd173ebc9a8225eb6fb2b18a222b5b7dfe7a296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class DocumentAiWarehouseDocumentSchemaTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#create DocumentAiWarehouseDocumentSchema#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#delete DocumentAiWarehouseDocumentSchema#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb41202a2690efb614f068360889db3bfe3392c079695a84d69cf80e7f1d93f3)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#create DocumentAiWarehouseDocumentSchema#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_document_schema#delete DocumentAiWarehouseDocumentSchema#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseDocumentSchemaTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseDocumentSchemaTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseDocumentSchema.DocumentAiWarehouseDocumentSchemaTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4dc8f6eae5efad21d46ee1e362b5e10e7d4cc3f270473b91a29e70c5b144618)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67ee551c505c48c7a4f5cf41a56c063c2ec56da14f0e67aff9545c833c665c34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f5bea7c7d899511b22d2a630feb3173b629a9d3e8e2b68a14d0ee5400a2f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe13780824572bdf33a220664c0a3d4cdaf5d598e1e17c8f91cd31e771d152af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DocumentAiWarehouseDocumentSchema",
    "DocumentAiWarehouseDocumentSchemaConfig",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsList",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsList",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesList",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesList",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions",
    "DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptionsOutputReference",
    "DocumentAiWarehouseDocumentSchemaTimeouts",
    "DocumentAiWarehouseDocumentSchemaTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__44412add24ccbf1adfdbe529bdb9b76d31c2e7d9e023da149b18fadfc81b9c72(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    project_number: builtins.str,
    property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitions, typing.Dict[builtins.str, typing.Any]]]],
    document_is_folder: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ddc3136d5c589014bd869499b53d2a7633c55336a413d2c9172edbccee2536fc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddcefe3704819d7aba8951ed15e7347a9d7fa5a8c5bb1568a808f729db1ff73c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a31b18a0816345e0ec5311b5499f2ac23170dd372fc176fe3bf568e24d72b4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c15b5d2f1cd4ae95bf9c6c9787110f5059c0a17d388129fb84d1cb16dce9efe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08125b1b03b903a076a4bc57ef6334cb274531c8f272da9fec6318ee3cc933a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79486966817d66d3f7f11f9b37bc8d7dac337cf72e3578cd24be28e1aad54706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e25d26075c7102d594a6e2a6a6c8190fba7c9cdcf5abf9fcacfd86d847b1398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d7609ac2d57055ce8cf52dbd373cad02d2b1ab35fd9cb1983861935afc90bf(
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
    project_number: builtins.str,
    property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitions, typing.Dict[builtins.str, typing.Any]]]],
    document_is_folder: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df6c8c2b3a234533b2135e3c60be0ed98222e5320106227bcf506013553464c(
    *,
    name: builtins.str,
    date_time_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    enum_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    float_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    is_filterable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_repeatable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    map_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    property_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    retrieval_importance: typing.Optional[builtins.str] = None,
    schema_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    text_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timestamp_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f7ecc48e122154aebdffc18cd97060d5b6991b990ef4fe8f1a5e1329bf4a61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57e5603496b3710567eb800a85873f0c6d6e9767037a4e7f4d692e851bd7c25(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5c001684df8336e263d15445529a5bc41695aad337760e0b24be4300a66760(
    *,
    possible_values: typing.Sequence[builtins.str],
    validation_check_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b4b0a40588b0342719628a29be560e4942210e959a9fcaa3b3ba8cb2ce65cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8711da901a3b53f22a6ca5e7f7183208e1e4dce35fc4c6fe0293718496c3564a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e753337aa895a276e6e26415e9adf83ce91f09bfb5488651ec5b0ee4973319ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3f2f8ab37c6d524ffb22616bafe6701b61a823506fb0a1d2b7b0a20d4c0ffa(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c10600c583a9edec0102c359f05a3881421f123a3e1ac91b05cb95c15ea23b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b27c3576fb2eb82e3d72ed65c4fcafb8e3f79a510795c0bc8db9d6184e85d9(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ed1028983c634feb3c91da21adf422a3e831f1fc3adaf945faeb1101b51f6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90fa29ad4296adec39d97f2a430135e6f95e3be618f93dc8fa5dee53e3338e9a(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada366f67defcd42b528099093ba92d09359b4e13f80e8a789d542d9c631a0f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647bd272c03da1ba8ab7390f15d262d58f62c12900c74c87e84af701350c15be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8808b5296996c580c290028e2df5bf7f573cfa3afad7b9f034065a87cde0c635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5273a8c0e658f42ac7639c1a31f2ed832c98bc98f38ae497d6b139f93c652712(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415f7985567f14b9e368029bb1e2f4020d781408bf12ff4f7f63f73b05f0b73c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf24d5653edc46496e44492fa23b51f866bcdc4e82f773aa8d0490c696fe52f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408794ac35a6b4ea544d2791a33555caa9d7c72f8c9ca5c869623c863f30b53d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a8ae6e5188ec422097192d59ff3f2741c09e6407fbf0c14e24b60a43df32c9(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8cf57ff138b2bc0614362fd1d1e6fca785ec525636b9c0423ffab09e758bfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f01445f0a6b9e8d40badf89bf3182d24657d54818756a6e4d96732a39263e13(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf55e76097c9242613f66e5e6fc97684e0f35894781f811c5efc9eb9698b98e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a0f2692df3b9eaf0a057983eec1c8f2059a846aebab11b7ae71ef15a78773d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24125284e70dd131c9f3072a62c4834196b0c4c2f8e90f270dfb30e8e318d993(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7001f45a50386f37ecd0ce31779accfb08a3e1da9a1f88f24c3c7ca06c27f21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6264549051867290036c9a8a67908724e2d87de9c25b36964beaae1c83aea1e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ef264fd9addef50453466c0a0f705fabc416df130f50bbe44c55602722c278(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff110739be5fc77f24ac4e0198ecd4e8b77183f8bc45b7c37e406b1d58c9943(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62d51607f8cc39865dd3f60783da3205443283b3620f4d18744ef07c9ba4cd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2daa6023efd3678e7fd0d23ff21ce231a8a5efa4f89f35be474cd16957f79a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a66766e1229b0e62bd6a215a12ebfe47a83880c84831698296fe5778a529f8d(
    *,
    property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf374afe26003fa33ed9d1764a2dc650d65c35bafe0fe4556008efc9793523ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f64a7634e42cd7007bda48f7153cdeeac438f268c7bcf48a7c4546d81a45c74(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c6e4e008945ce3a7b758e3cc797211211c3316581dffe6bc492624b816c7c9(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9a598be4c09abd2e512c758a0c9163601c27cdbfebbee589b791a34af01c31(
    *,
    name: builtins.str,
    date_time_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    enum_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    float_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    is_filterable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_repeatable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    map_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    retrieval_importance: typing.Optional[builtins.str] = None,
    schema_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    text_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timestamp_type_options: typing.Optional[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e96067373be4a436552a316dd335436db7bcac6b6c1ac694812e3c3be25df3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1c3afe78913814956e324b6b40a5ed16e87827216a9a892fbb6644ea4e6fe2(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170ea08a55f7da3172ca0c1d50ddfc041f7e79afd73ec9a4d43e90db3a076722(
    *,
    possible_values: typing.Sequence[builtins.str],
    validation_check_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833573e7cd41d4eb4262491b81a13a63cef0817110ea72be0f340d011fdf91d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e0eb2a3d2efc37b453044b6b415e737fe85ec9a93d900a2b0ac308e46674ec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4f9dc6d979eb9c3b564897322bf6920ad8af29a19628b6ebd94343b639b120(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb83f4a1086a56671eafd0803644d364ee47924ae7057c64c2f7c3824e8864d(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8155229a09526eb66d93aece52d4c808a6aed3ae191013def8c11db29d67c796(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61047bd6b883dd12a7c4b5dd245460943a8cf9d5aa58b846a504ddea5522d332(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a610600b720a889676de56097e42f996cff3006733e32c4d032c80dcee9248(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26eaec6d932717a31f035086b667e95ca6a1f457e3ae67c56a0ce7da2e2642b(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de661cbe81553e0327857c1607838e99034fafd710c5c5108614a9fcbfa53c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bd415329cc78c3370aa58c5c5cb2506298a6c60d49ce612f1edeb19c2c2478(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf39f71350cd6e9f0dae65b9b27f2c40d60147c20e47fef1221dfe3afbd4575(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfdf828af5eaef19f68f8b2768db90940245b9340aab0a5f7481c992deb79210(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6cd56edddf1d8f403a85ab98efaac02ddb5c1b17f69640d89b6f3c4ced8a1da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8823bc1dc5ef9aee406415c84f550a40467ab067c3509dcb707c036be7aec3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299d75d58017ba9c1195251682cfe48b4dcb8e54f3325753519f7cbda1bb27a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c093f3666d736cb3a575bb802e5b6f09bc421752d96906c3dbdc10503d0ff7(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2eaa1c0d573fe33a40e20eda78b39589c376c7e63e406e3fcdc338046d7836d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd40e00135a6c4fbe5d962fe283c3f8f986d16657ac98a053d6dd0f936ffdabb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1412beea5deccec3eeeb9da02c6b5106f24ccc877de90f3ae093f048255a6ecc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559aca631b0b304cd4c24173926791a203993c507d10910a7f180fc97f198451(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6919082e4d3c455176a478737d65a5a042c617bbda5cc0233e319cf3feb46907(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c947fd8db5dfad7f28b4c800553423e145e64ff510474e12d92c75c3148a98aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a858873a53bb73a7a1b1afa668114c7b41ccf570b670797bb3ab5eeca2f42c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abba4d8e6b32a1ca47e36048e0ec4c8b8b886e95650fe318e7e7f1605d8a934f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd7236d477dd346a90e5079bda69cabeb68442809ebd5b8e945cfd775475692(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91010ed9fb0e887214e4e1815052d2fc64775b55c80a2dd27427b986efa8036f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b8c250ec766007abb920c13936356f85a2e2cb95ef50643539ac01057a09496(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8076039499deac37b7f0fa6983be8c449ad6a4be7de2b0bbfc5c538ed540b0(
    *,
    name: typing.Optional[builtins.str] = None,
    processor_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf12fb946bf099e8ad73253bb1d4cfc32ffa7f8b2049573fa5fe641783e7facc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7017e4ceb590c5a20bb42fad3a789f69392154391028d1cc8e4c76529c0f68(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f089bc70971755196bf28cd8bc1ae46a3a83459f3453e18665fd0f55b2252cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b66bb3335509addb367ce160f7033fe4364e823d12f4127038b5994543e0c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62de88addf50f949122bd680b523494957d44d0c6653107276103bc884a69f0d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe1f8a5e8350ec147bde324a38d541d3cff90cf2aa492e5f8012f038e9989f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5258859c561f7ea3d961292dc8c74271b688df529152539f5fb13480db786066(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a36076e2b43dc2c486c51390d7b581e724ff438d1bd518431063dda81bc138(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea04876422dff17b78790675612183b05a6596c6e007696564fafa00319f435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86a947b1d3161c83cf6c356ef1c6a8876adcc3f0fa54aea283982b2d378cee7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa26a96c966396b72964616d3370a06b3c5451c7bdce22595b99b27f5eba895(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5803687a8c784c95cce1744c3350687b4acb2bb5c5bc86fa96c3820c69bba290(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c6648fb3390f2bf31263dcc6014d3229c95d4e809d42c17f3a669cfe925ddcd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a791b4e0c5461b3de290e11a23fb6398f83e71a4c08134565a6b3adc8aed7c(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aeb682281abda81b9bd3c9353a0e4646da85407b630f1c6baf68a18e28bd194(
    *,
    name: typing.Optional[builtins.str] = None,
    processor_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985022f4dc2ef7d61b72b62cdbb99e6b9240f2527ee5acc6552f715c20378132(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc83e13fb91caa8a40f525f2930dcf655dac1e7e8c4ff6511159029d8907a598(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b9107829eb7c82fd91204c5d13362b90094ca2c854f623efacdf81e83c5be9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653ec8c843eadb0f235ecc8f45f82bb5df82372fdb0ea7a44819e695b2f8fde2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58613c13b049a2a248f2ff0a6f690debcc247c3571b3a463a60f58b0fe43293c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8010ef82726a054f4089338e54a253e1cd5da1e7e7de75724b84c0f8ce67cb55(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca04618106a23f33e4e6bc6740f8325b81ea3b4b4f70b87a37a5688850a837c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efe73a6832877dd6e4d1eda6e0c02f7006d4aedae6ba9ccfcd18703bd2bcf12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120b089ee6f25e79aa278cdd42e2539f3dc1dce9b2313e22da8d0d45210290b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ce25eaf3b9ff791b1481c860fb5d3f2da3ab3f2e66f3f1aae81ee40c4ff236(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6f3a09329a18324cfee7f53a4dba0643026b4d94a6faa4bf1a1c0a9cea6897(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f26be2ae359c74735b67f0da4182b6b645f9e583f9c616fc6323f1ca1a6064e(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111349344ecc7b2892d81423033fe0969e8a00672d49ac224cfa7333e15cc0d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02079c3041bb81b5d021e8ecccd173ebc9a8225eb6fb2b18a222b5b7dfe7a296(
    value: typing.Optional[DocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb41202a2690efb614f068360889db3bfe3392c079695a84d69cf80e7f1d93f3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4dc8f6eae5efad21d46ee1e362b5e10e7d4cc3f270473b91a29e70c5b144618(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ee551c505c48c7a4f5cf41a56c063c2ec56da14f0e67aff9545c833c665c34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f5bea7c7d899511b22d2a630feb3173b629a9d3e8e2b68a14d0ee5400a2f6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe13780824572bdf33a220664c0a3d4cdaf5d598e1e17c8f91cd31e771d152af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseDocumentSchemaTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
