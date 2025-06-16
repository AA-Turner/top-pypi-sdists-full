r'''
# `google_document_ai_warehouse_document_schema`

Refer to the Terraform Registry for docs: [`google_document_ai_warehouse_document_schema`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema).
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


class GoogleDocumentAiWarehouseDocumentSchema(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchema",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema google_document_ai_warehouse_document_schema}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        project_number: builtins.str,
        property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions", typing.Dict[builtins.str, typing.Any]]]],
        document_is_folder: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema google_document_ai_warehouse_document_schema} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Name of the schema given by the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#display_name GoogleDocumentAiWarehouseDocumentSchema#display_name}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#location GoogleDocumentAiWarehouseDocumentSchema#location}
        :param project_number: The unique identifier of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#project_number GoogleDocumentAiWarehouseDocumentSchema#project_number}
        :param property_definitions: property_definitions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#property_definitions GoogleDocumentAiWarehouseDocumentSchema#property_definitions}
        :param document_is_folder: Tells whether the document is a folder or a typical document. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#document_is_folder GoogleDocumentAiWarehouseDocumentSchema#document_is_folder}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#id GoogleDocumentAiWarehouseDocumentSchema#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#timeouts GoogleDocumentAiWarehouseDocumentSchema#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fc3ea5d1bc17ada006e966a37aa01e513d25fc2bd09e78e96a3de269e3b5b5b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDocumentAiWarehouseDocumentSchemaConfig(
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
        '''Generates CDKTF code for importing a GoogleDocumentAiWarehouseDocumentSchema resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDocumentAiWarehouseDocumentSchema to import.
        :param import_from_id: The id of the existing GoogleDocumentAiWarehouseDocumentSchema that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDocumentAiWarehouseDocumentSchema to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1b7f3a7bc74329812222291427086fb59697b5b2e4235895543f4191cb8222)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPropertyDefinitions")
    def put_property_definitions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b5f28f37e758469a33ea651fe01bf4a57a92fab45d02b01c8bf8c138680b4e)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#create GoogleDocumentAiWarehouseDocumentSchema#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#delete GoogleDocumentAiWarehouseDocumentSchema#delete}.
        '''
        value = GoogleDocumentAiWarehouseDocumentSchemaTimeouts(
            create=create, delete=delete
        )

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
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsList":
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsList", jsii.get(self, "propertyDefinitions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaTimeoutsOutputReference":
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions"]]], jsii.get(self, "propertyDefinitionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDocumentAiWarehouseDocumentSchemaTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDocumentAiWarehouseDocumentSchemaTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ade059736000ce592f80c9cbcb747209cacdd048081086a73219dddf240a333)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4c15626f679458b5f987a1796fa07681084c6346da22f2c6f95ba1f04c8fe2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentIsFolder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab25c3400bd1bacb313c41ecb2be95f36d5d7b0d7bcc2b70aa70345fc61d8bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931cda6a85f3258e77ba64478f5bc24f3e017fc97c26ebf84e1c72850f172ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectNumber")
    def project_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectNumber"))

    @project_number.setter
    def project_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a45598f53d262da97ae4cf3ceb496780e34e92c1b2e10d522411ce0a346f544d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectNumber", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaConfig",
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
class GoogleDocumentAiWarehouseDocumentSchemaConfig(
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
        display_name: builtins.str,
        location: builtins.str,
        project_number: builtins.str,
        property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions", typing.Dict[builtins.str, typing.Any]]]],
        document_is_folder: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Name of the schema given by the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#display_name GoogleDocumentAiWarehouseDocumentSchema#display_name}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#location GoogleDocumentAiWarehouseDocumentSchema#location}
        :param project_number: The unique identifier of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#project_number GoogleDocumentAiWarehouseDocumentSchema#project_number}
        :param property_definitions: property_definitions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#property_definitions GoogleDocumentAiWarehouseDocumentSchema#property_definitions}
        :param document_is_folder: Tells whether the document is a folder or a typical document. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#document_is_folder GoogleDocumentAiWarehouseDocumentSchema#document_is_folder}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#id GoogleDocumentAiWarehouseDocumentSchema#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#timeouts GoogleDocumentAiWarehouseDocumentSchema#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleDocumentAiWarehouseDocumentSchemaTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144a6ec60bca8fee45f851134b9a0be30760d07860fdecd43f055c590894a1a0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#display_name GoogleDocumentAiWarehouseDocumentSchema#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#location GoogleDocumentAiWarehouseDocumentSchema#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_number(self) -> builtins.str:
        '''The unique identifier of the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#project_number GoogleDocumentAiWarehouseDocumentSchema#project_number}
        '''
        result = self._values.get("project_number")
        assert result is not None, "Required property 'project_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def property_definitions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions"]]:
        '''property_definitions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#property_definitions GoogleDocumentAiWarehouseDocumentSchema#property_definitions}
        '''
        result = self._values.get("property_definitions")
        assert result is not None, "Required property 'property_definitions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions"]], result)

    @builtins.property
    def document_is_folder(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Tells whether the document is a folder or a typical document.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#document_is_folder GoogleDocumentAiWarehouseDocumentSchema#document_is_folder}
        '''
        result = self._values.get("document_is_folder")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#id GoogleDocumentAiWarehouseDocumentSchema#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#timeouts GoogleDocumentAiWarehouseDocumentSchema#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions",
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
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions:
    def __init__(
        self,
        *,
        name: builtins.str,
        date_time_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        enum_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        float_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        is_filterable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_repeatable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        map_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        property_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        retrieval_importance: typing.Optional[builtins.str] = None,
        schema_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        text_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timestamp_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: The name of the metadata property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#name GoogleDocumentAiWarehouseDocumentSchema#name}
        :param date_time_type_options: date_time_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#date_time_type_options GoogleDocumentAiWarehouseDocumentSchema#date_time_type_options}
        :param display_name: The display-name for the property, used for front-end. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#display_name GoogleDocumentAiWarehouseDocumentSchema#display_name}
        :param enum_type_options: enum_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#enum_type_options GoogleDocumentAiWarehouseDocumentSchema#enum_type_options}
        :param float_type_options: float_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#float_type_options GoogleDocumentAiWarehouseDocumentSchema#float_type_options}
        :param integer_type_options: integer_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#integer_type_options GoogleDocumentAiWarehouseDocumentSchema#integer_type_options}
        :param is_filterable: Whether the property can be filtered. If this is a sub-property, all the parent properties must be marked filterable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_filterable GoogleDocumentAiWarehouseDocumentSchema#is_filterable}
        :param is_metadata: Whether the property is user supplied metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_metadata GoogleDocumentAiWarehouseDocumentSchema#is_metadata}
        :param is_repeatable: Whether the property can have multiple values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_repeatable GoogleDocumentAiWarehouseDocumentSchema#is_repeatable}
        :param is_required: Whether the property is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_required GoogleDocumentAiWarehouseDocumentSchema#is_required}
        :param is_searchable: Indicates that the property should be included in a global search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_searchable GoogleDocumentAiWarehouseDocumentSchema#is_searchable}
        :param map_type_options: map_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#map_type_options GoogleDocumentAiWarehouseDocumentSchema#map_type_options}
        :param property_type_options: property_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#property_type_options GoogleDocumentAiWarehouseDocumentSchema#property_type_options}
        :param retrieval_importance: Stores the retrieval importance. Possible values: ["HIGHEST", "HIGHER", "HIGH", "MEDIUM", "LOW", "LOWEST"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#retrieval_importance GoogleDocumentAiWarehouseDocumentSchema#retrieval_importance}
        :param schema_sources: schema_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#schema_sources GoogleDocumentAiWarehouseDocumentSchema#schema_sources}
        :param text_type_options: text_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#text_type_options GoogleDocumentAiWarehouseDocumentSchema#text_type_options}
        :param timestamp_type_options: timestamp_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#timestamp_type_options GoogleDocumentAiWarehouseDocumentSchema#timestamp_type_options}
        '''
        if isinstance(date_time_type_options, dict):
            date_time_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions(**date_time_type_options)
        if isinstance(enum_type_options, dict):
            enum_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions(**enum_type_options)
        if isinstance(float_type_options, dict):
            float_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions(**float_type_options)
        if isinstance(integer_type_options, dict):
            integer_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions(**integer_type_options)
        if isinstance(map_type_options, dict):
            map_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions(**map_type_options)
        if isinstance(property_type_options, dict):
            property_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions(**property_type_options)
        if isinstance(text_type_options, dict):
            text_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions(**text_type_options)
        if isinstance(timestamp_type_options, dict):
            timestamp_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions(**timestamp_type_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9abfc172ff1ed783ed29f5c4b625d3f89d536dae289e31deecc54dab04474dc4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#name GoogleDocumentAiWarehouseDocumentSchema#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def date_time_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions"]:
        '''date_time_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#date_time_type_options GoogleDocumentAiWarehouseDocumentSchema#date_time_type_options}
        '''
        result = self._values.get("date_time_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display-name for the property, used for front-end.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#display_name GoogleDocumentAiWarehouseDocumentSchema#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enum_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions"]:
        '''enum_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#enum_type_options GoogleDocumentAiWarehouseDocumentSchema#enum_type_options}
        '''
        result = self._values.get("enum_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions"], result)

    @builtins.property
    def float_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions"]:
        '''float_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#float_type_options GoogleDocumentAiWarehouseDocumentSchema#float_type_options}
        '''
        result = self._values.get("float_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions"], result)

    @builtins.property
    def integer_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions"]:
        '''integer_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#integer_type_options GoogleDocumentAiWarehouseDocumentSchema#integer_type_options}
        '''
        result = self._values.get("integer_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions"], result)

    @builtins.property
    def is_filterable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property can be filtered. If this is a sub-property, all the parent properties must be marked filterable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_filterable GoogleDocumentAiWarehouseDocumentSchema#is_filterable}
        '''
        result = self._values.get("is_filterable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_metadata(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property is user supplied metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_metadata GoogleDocumentAiWarehouseDocumentSchema#is_metadata}
        '''
        result = self._values.get("is_metadata")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_repeatable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property can have multiple values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_repeatable GoogleDocumentAiWarehouseDocumentSchema#is_repeatable}
        '''
        result = self._values.get("is_repeatable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property is mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_required GoogleDocumentAiWarehouseDocumentSchema#is_required}
        '''
        result = self._values.get("is_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_searchable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates that the property should be included in a global search.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_searchable GoogleDocumentAiWarehouseDocumentSchema#is_searchable}
        '''
        result = self._values.get("is_searchable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def map_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions"]:
        '''map_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#map_type_options GoogleDocumentAiWarehouseDocumentSchema#map_type_options}
        '''
        result = self._values.get("map_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions"], result)

    @builtins.property
    def property_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions"]:
        '''property_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#property_type_options GoogleDocumentAiWarehouseDocumentSchema#property_type_options}
        '''
        result = self._values.get("property_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions"], result)

    @builtins.property
    def retrieval_importance(self) -> typing.Optional[builtins.str]:
        '''Stores the retrieval importance. Possible values: ["HIGHEST", "HIGHER", "HIGH", "MEDIUM", "LOW", "LOWEST"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#retrieval_importance GoogleDocumentAiWarehouseDocumentSchema#retrieval_importance}
        '''
        result = self._values.get("retrieval_importance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources"]]]:
        '''schema_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#schema_sources GoogleDocumentAiWarehouseDocumentSchema#schema_sources}
        '''
        result = self._values.get("schema_sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources"]]], result)

    @builtins.property
    def text_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions"]:
        '''text_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#text_type_options GoogleDocumentAiWarehouseDocumentSchema#text_type_options}
        '''
        result = self._values.get("text_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions"], result)

    @builtins.property
    def timestamp_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions"]:
        '''timestamp_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#timestamp_type_options GoogleDocumentAiWarehouseDocumentSchema#timestamp_type_options}
        '''
        result = self._values.get("timestamp_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__815d3aff0d29d296f9229ad129d13d70cadb932da7340df27c024b9ca4dbe421)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0b8e4a66e11ef380286060b2d55de90c77561f002a903ce6a6ea8631c0dea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "possible_values": "possibleValues",
        "validation_check_disabled": "validationCheckDisabled",
    },
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions:
    def __init__(
        self,
        *,
        possible_values: typing.Sequence[builtins.str],
        validation_check_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param possible_values: List of possible enum values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#possible_values GoogleDocumentAiWarehouseDocumentSchema#possible_values}
        :param validation_check_disabled: Make sure the enum property value provided in the document is in the possile value list during document creation. The validation check runs by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#validation_check_disabled GoogleDocumentAiWarehouseDocumentSchema#validation_check_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7883c36bbddb0989778ed538f40bebe481e91fa2c559af0d5e410dba92d52bd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#possible_values GoogleDocumentAiWarehouseDocumentSchema#possible_values}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#validation_check_disabled GoogleDocumentAiWarehouseDocumentSchema#validation_check_disabled}
        '''
        result = self._values.get("validation_check_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d85b8184e5784b9a247cca1512aa3aca919fb263b16c21f318d8b4bea4a50963)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8bf38d696f9f6fc71c23ee24b1f6d4896be868ba9fb6195dbb111b91582fcfe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c22090ef33962f8a4d6adfdefbbfaf78831f1f1204966dd58d0eb3aef701479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validationCheckDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b425a0be345a5e0bd9c1110c77affac93a7daaada5261557ac59732c5735aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__185ff71d3362317f1a2a6aa28074a4c27b0ef8a621b65229ba0c5e4e6714581c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e39f14ef12f2f4ae8c6a8412e3bc4089262ccb2936f8b31b26b486e26147784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0d89166533159df6d44c27b5c6d47b050a69bbff24a7502e8e218dfb8d533b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2f09969c34f253237eb8df6bb5aad84fef154a489e0b1b8793d88135e16b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58d29167c6b121bd39f16458539519dd5f444188acd1389d3c61ed62ef511892)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff94f53abd425ccbd3f46cd8c6b74c96f1fad8f4265f4b9b0b275e359556129c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa56f22dd0637e58cbb9335561fadf242a715f2e16ce1d464c1c783c64621cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__462bce610889c7e89806f85e06109015f4e9945e1eaf74861557d4fb3b24fc5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae1726c7c88a8c70a0fb680125471f0c6f934a0433c1461430b8025a63c399b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89afba33de53b9e68533e6c30cfbdcdc5637d3e59e974eb82765df2f828feee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f72f28d00f7e2a890c4b1db51cf95b190a09510eee4b854e1f9cf72c41a7e57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed1746d32f07dd8da9df487f8c8f9664757f52df60562ee72e1c2f742804a455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1fde34c6fc6b3002cff50a65f5c88e4f207698136d1b198e1e9727f81d9af04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDateTimeTypeOptions")
    def put_date_time_type_options(self) -> None:
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putDateTimeTypeOptions", [value]))

    @jsii.member(jsii_name="putEnumTypeOptions")
    def put_enum_type_options(
        self,
        *,
        possible_values: typing.Sequence[builtins.str],
        validation_check_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param possible_values: List of possible enum values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#possible_values GoogleDocumentAiWarehouseDocumentSchema#possible_values}
        :param validation_check_disabled: Make sure the enum property value provided in the document is in the possile value list during document creation. The validation check runs by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#validation_check_disabled GoogleDocumentAiWarehouseDocumentSchema#validation_check_disabled}
        '''
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions(
            possible_values=possible_values,
            validation_check_disabled=validation_check_disabled,
        )

        return typing.cast(None, jsii.invoke(self, "putEnumTypeOptions", [value]))

    @jsii.member(jsii_name="putFloatTypeOptions")
    def put_float_type_options(self) -> None:
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putFloatTypeOptions", [value]))

    @jsii.member(jsii_name="putIntegerTypeOptions")
    def put_integer_type_options(self) -> None:
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putIntegerTypeOptions", [value]))

    @jsii.member(jsii_name="putMapTypeOptions")
    def put_map_type_options(self) -> None:
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putMapTypeOptions", [value]))

    @jsii.member(jsii_name="putPropertyTypeOptions")
    def put_property_type_options(
        self,
        *,
        property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param property_definitions: property_definitions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#property_definitions GoogleDocumentAiWarehouseDocumentSchema#property_definitions}
        '''
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions(
            property_definitions=property_definitions
        )

        return typing.cast(None, jsii.invoke(self, "putPropertyTypeOptions", [value]))

    @jsii.member(jsii_name="putSchemaSources")
    def put_schema_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3dc532a9191619471aa68431e262c5dec9c541a0601dcc6065f9e79b8ecd43e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchemaSources", [value]))

    @jsii.member(jsii_name="putTextTypeOptions")
    def put_text_type_options(self) -> None:
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putTextTypeOptions", [value]))

    @jsii.member(jsii_name="putTimestampTypeOptions")
    def put_timestamp_type_options(self) -> None:
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions()

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
    ) -> GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptionsOutputReference:
        return typing.cast(GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptionsOutputReference, jsii.get(self, "dateTimeTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="enumTypeOptions")
    def enum_type_options(
        self,
    ) -> GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptionsOutputReference:
        return typing.cast(GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptionsOutputReference, jsii.get(self, "enumTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="floatTypeOptions")
    def float_type_options(
        self,
    ) -> GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptionsOutputReference:
        return typing.cast(GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptionsOutputReference, jsii.get(self, "floatTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="integerTypeOptions")
    def integer_type_options(
        self,
    ) -> GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptionsOutputReference:
        return typing.cast(GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptionsOutputReference, jsii.get(self, "integerTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="mapTypeOptions")
    def map_type_options(
        self,
    ) -> GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptionsOutputReference:
        return typing.cast(GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptionsOutputReference, jsii.get(self, "mapTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="propertyTypeOptions")
    def property_type_options(
        self,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsOutputReference":
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsOutputReference", jsii.get(self, "propertyTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="schemaSources")
    def schema_sources(
        self,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesList":
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesList", jsii.get(self, "schemaSources"))

    @builtins.property
    @jsii.member(jsii_name="textTypeOptions")
    def text_type_options(
        self,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptionsOutputReference":
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptionsOutputReference", jsii.get(self, "textTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeOptions")
    def timestamp_type_options(
        self,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptionsOutputReference":
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptionsOutputReference", jsii.get(self, "timestampTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="dateTimeTypeOptionsInput")
    def date_time_type_options_input(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions], jsii.get(self, "dateTimeTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enumTypeOptionsInput")
    def enum_type_options_input(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions], jsii.get(self, "enumTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="floatTypeOptionsInput")
    def float_type_options_input(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions], jsii.get(self, "floatTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="integerTypeOptionsInput")
    def integer_type_options_input(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions], jsii.get(self, "integerTypeOptionsInput"))

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
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions], jsii.get(self, "mapTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="propertyTypeOptionsInput")
    def property_type_options_input(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions"]:
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions"], jsii.get(self, "propertyTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="retrievalImportanceInput")
    def retrieval_importance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retrievalImportanceInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaSourcesInput")
    def schema_sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources"]]], jsii.get(self, "schemaSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="textTypeOptionsInput")
    def text_type_options_input(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions"]:
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions"], jsii.get(self, "textTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeOptionsInput")
    def timestamp_type_options_input(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions"]:
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions"], jsii.get(self, "timestampTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194931a750869eec96794dbe34ed107378f27efd8d9c1ebfce9dc160ed0ef3bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c4756b8f805d86aa4111de16aaa7c88ab77590700771d80019447fa3a69e9b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a63c83bba42044568b6ea98c8b4c8658db5cc15834949fec5d88d8a4f6f7465d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f29a303468c526a112d6b9299a20bd423f238f984ccd6fd8619c53182f02ad9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d8fca97856f94a3c2cfce50cd00e3e944762eaf67a24773a2adf31f3d553fc3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee840db2a3dbee2530f70e1bd0355b0d298f2beb7841339e1df62da7b015879e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSearchable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ea58a8c0bd9c803a5a60bd02c6482b2d756031314aa1d65dc5bf2c7178d27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retrievalImportance")
    def retrieval_importance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retrievalImportance"))

    @retrieval_importance.setter
    def retrieval_importance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e0dbaf1ee54a57e59cab6691635518f610a2929ff2d773b52077fa68e5b05d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retrievalImportance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__804fe551c7edf292a42ad8b29bf7b2087202e84203355dfb2833540672a1a6d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions",
    jsii_struct_bases=[],
    name_mapping={"property_definitions": "propertyDefinitions"},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions:
    def __init__(
        self,
        *,
        property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param property_definitions: property_definitions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#property_definitions GoogleDocumentAiWarehouseDocumentSchema#property_definitions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45cbd31e9754650afb9c69038d49b2af88cdea3b96dd0f33fe0ca7f30ace9a23)
            check_type(argname="argument property_definitions", value=property_definitions, expected_type=type_hints["property_definitions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "property_definitions": property_definitions,
        }

    @builtins.property
    def property_definitions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions"]]:
        '''property_definitions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#property_definitions GoogleDocumentAiWarehouseDocumentSchema#property_definitions}
        '''
        result = self._values.get("property_definitions")
        assert result is not None, "Required property 'property_definitions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e750d99a9316f597b2f7d31517c8e65ef183a5e6155813442c5bdc81e851fed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPropertyDefinitions")
    def put_property_definitions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2edf07e051532b3d01d4e8ef3f0510409d6903827e1ea9a5a96c08302104cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPropertyDefinitions", [value]))

    @builtins.property
    @jsii.member(jsii_name="propertyDefinitions")
    def property_definitions(
        self,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsList":
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsList", jsii.get(self, "propertyDefinitions"))

    @builtins.property
    @jsii.member(jsii_name="propertyDefinitionsInput")
    def property_definitions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions"]]], jsii.get(self, "propertyDefinitionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9cf904c4f12fd10685faff33ee7b0b3804d14a68725b643c1d473926e6154e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions",
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
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions:
    def __init__(
        self,
        *,
        name: builtins.str,
        date_time_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        enum_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        float_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        integer_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        is_filterable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_repeatable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        map_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        retrieval_importance: typing.Optional[builtins.str] = None,
        schema_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        text_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timestamp_type_options: typing.Optional[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: The name of the metadata property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#name GoogleDocumentAiWarehouseDocumentSchema#name}
        :param date_time_type_options: date_time_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#date_time_type_options GoogleDocumentAiWarehouseDocumentSchema#date_time_type_options}
        :param display_name: The display-name for the property, used for front-end. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#display_name GoogleDocumentAiWarehouseDocumentSchema#display_name}
        :param enum_type_options: enum_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#enum_type_options GoogleDocumentAiWarehouseDocumentSchema#enum_type_options}
        :param float_type_options: float_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#float_type_options GoogleDocumentAiWarehouseDocumentSchema#float_type_options}
        :param integer_type_options: integer_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#integer_type_options GoogleDocumentAiWarehouseDocumentSchema#integer_type_options}
        :param is_filterable: Whether the property can be filtered. If this is a sub-property, all the parent properties must be marked filterable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_filterable GoogleDocumentAiWarehouseDocumentSchema#is_filterable}
        :param is_metadata: Whether the property is user supplied metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_metadata GoogleDocumentAiWarehouseDocumentSchema#is_metadata}
        :param is_repeatable: Whether the property can have multiple values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_repeatable GoogleDocumentAiWarehouseDocumentSchema#is_repeatable}
        :param is_required: Whether the property is mandatory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_required GoogleDocumentAiWarehouseDocumentSchema#is_required}
        :param is_searchable: Indicates that the property should be included in a global search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_searchable GoogleDocumentAiWarehouseDocumentSchema#is_searchable}
        :param map_type_options: map_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#map_type_options GoogleDocumentAiWarehouseDocumentSchema#map_type_options}
        :param retrieval_importance: Stores the retrieval importance. Possible values: ["HIGHEST", "HIGHER", "HIGH", "MEDIUM", "LOW", "LOWEST"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#retrieval_importance GoogleDocumentAiWarehouseDocumentSchema#retrieval_importance}
        :param schema_sources: schema_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#schema_sources GoogleDocumentAiWarehouseDocumentSchema#schema_sources}
        :param text_type_options: text_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#text_type_options GoogleDocumentAiWarehouseDocumentSchema#text_type_options}
        :param timestamp_type_options: timestamp_type_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#timestamp_type_options GoogleDocumentAiWarehouseDocumentSchema#timestamp_type_options}
        '''
        if isinstance(date_time_type_options, dict):
            date_time_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions(**date_time_type_options)
        if isinstance(enum_type_options, dict):
            enum_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions(**enum_type_options)
        if isinstance(float_type_options, dict):
            float_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions(**float_type_options)
        if isinstance(integer_type_options, dict):
            integer_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions(**integer_type_options)
        if isinstance(map_type_options, dict):
            map_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions(**map_type_options)
        if isinstance(text_type_options, dict):
            text_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions(**text_type_options)
        if isinstance(timestamp_type_options, dict):
            timestamp_type_options = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions(**timestamp_type_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__166753fb341689c7ea665937d7c8e530804df95753f3395ed250980f60285c28)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#name GoogleDocumentAiWarehouseDocumentSchema#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def date_time_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions"]:
        '''date_time_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#date_time_type_options GoogleDocumentAiWarehouseDocumentSchema#date_time_type_options}
        '''
        result = self._values.get("date_time_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions"], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display-name for the property, used for front-end.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#display_name GoogleDocumentAiWarehouseDocumentSchema#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enum_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions"]:
        '''enum_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#enum_type_options GoogleDocumentAiWarehouseDocumentSchema#enum_type_options}
        '''
        result = self._values.get("enum_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions"], result)

    @builtins.property
    def float_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions"]:
        '''float_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#float_type_options GoogleDocumentAiWarehouseDocumentSchema#float_type_options}
        '''
        result = self._values.get("float_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions"], result)

    @builtins.property
    def integer_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions"]:
        '''integer_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#integer_type_options GoogleDocumentAiWarehouseDocumentSchema#integer_type_options}
        '''
        result = self._values.get("integer_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions"], result)

    @builtins.property
    def is_filterable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property can be filtered. If this is a sub-property, all the parent properties must be marked filterable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_filterable GoogleDocumentAiWarehouseDocumentSchema#is_filterable}
        '''
        result = self._values.get("is_filterable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_metadata(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property is user supplied metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_metadata GoogleDocumentAiWarehouseDocumentSchema#is_metadata}
        '''
        result = self._values.get("is_metadata")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_repeatable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property can have multiple values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_repeatable GoogleDocumentAiWarehouseDocumentSchema#is_repeatable}
        '''
        result = self._values.get("is_repeatable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the property is mandatory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_required GoogleDocumentAiWarehouseDocumentSchema#is_required}
        '''
        result = self._values.get("is_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_searchable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates that the property should be included in a global search.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#is_searchable GoogleDocumentAiWarehouseDocumentSchema#is_searchable}
        '''
        result = self._values.get("is_searchable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def map_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions"]:
        '''map_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#map_type_options GoogleDocumentAiWarehouseDocumentSchema#map_type_options}
        '''
        result = self._values.get("map_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions"], result)

    @builtins.property
    def retrieval_importance(self) -> typing.Optional[builtins.str]:
        '''Stores the retrieval importance. Possible values: ["HIGHEST", "HIGHER", "HIGH", "MEDIUM", "LOW", "LOWEST"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#retrieval_importance GoogleDocumentAiWarehouseDocumentSchema#retrieval_importance}
        '''
        result = self._values.get("retrieval_importance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources"]]]:
        '''schema_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#schema_sources GoogleDocumentAiWarehouseDocumentSchema#schema_sources}
        '''
        result = self._values.get("schema_sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources"]]], result)

    @builtins.property
    def text_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions"]:
        '''text_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#text_type_options GoogleDocumentAiWarehouseDocumentSchema#text_type_options}
        '''
        result = self._values.get("text_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions"], result)

    @builtins.property
    def timestamp_type_options(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions"]:
        '''timestamp_type_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#timestamp_type_options GoogleDocumentAiWarehouseDocumentSchema#timestamp_type_options}
        '''
        result = self._values.get("timestamp_type_options")
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d02e640542860bf8c9e2a0fe0ce258bf97c5ee45c6da44555e1ffe79d055d78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d52ed7b7ad368f36c9131440f09e25ae813e5ad04ff06392fc43f6518c0ccce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "possible_values": "possibleValues",
        "validation_check_disabled": "validationCheckDisabled",
    },
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions:
    def __init__(
        self,
        *,
        possible_values: typing.Sequence[builtins.str],
        validation_check_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param possible_values: List of possible enum values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#possible_values GoogleDocumentAiWarehouseDocumentSchema#possible_values}
        :param validation_check_disabled: Make sure the enum property value provided in the document is in the possile value list during document creation. The validation check runs by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#validation_check_disabled GoogleDocumentAiWarehouseDocumentSchema#validation_check_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd07ace774a460fed3a64bd2ce7d74766532da37ac0ca9e601b288f82367f3ff)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#possible_values GoogleDocumentAiWarehouseDocumentSchema#possible_values}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#validation_check_disabled GoogleDocumentAiWarehouseDocumentSchema#validation_check_disabled}
        '''
        result = self._values.get("validation_check_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7a85945f30b1c247535d9bdb8c7631826f06a03ec6e1dc0c253c0aeb59b8413)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d48d8bde83b78f44f94da3cba6f154b397ee5fd14196ee66770f3fac187bef1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e63047a7bb8bfbf6e207da26358614f696672b2d3c458867d864c6fd5e89d4ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validationCheckDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37feb7614de8c01854933ad737340ddf256eccc04ee6cd6829ceb1c101fdf345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ec23700a0139d1b9e317db81afef9b7e03367e5ed0c879bf7a0958066c771c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__189861a609b2642b6a3d8d75bf66302127d648295b7722cdbaca464572b77705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64b1de2e74fca95c7225ed3f7e50790b78985685ba0927b7d0c381b4531aeafc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8146e0361d09411727168b5e7a4a3f653c9ca782b73dfd6eba2df0f6dae046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e7c964c382219481ca05c546dff6e5105c6886afeb3b691076e6a47318ec46a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3272ea18ef5341f97593d4e79de19d3063b9b11758537e1de3bd132c9ba29e7f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e1238ce9ac3b5002414c27d74f43cc014b6f5a491fdfccecbc1d28a973623d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__717bddc1a6dd2c1ce1244a157e07b7faa156de367dc25fdd76c6cdc262f6da35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0952615caf9ee61d7098f6ebbfbfb59eb1affc3e6c3034269f7917ef481cb574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19fb55939bc9b543bf0703482b010c7262b7a217f98eb99d1af24c4d98c8d5eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8bc4c18ac1e07824e25b7be786c2d9ad2adb3718921c05f5c387e42b470b8c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__193523e312160f3e20cafa784cd95596bc1caa0a3af7cb9de18d7d4795ee0c40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d20d93588bc045ecd363f9f5e7226b58e0d3d3168ca28ae1c27bae19b2e467b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDateTimeTypeOptions")
    def put_date_time_type_options(self) -> None:
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putDateTimeTypeOptions", [value]))

    @jsii.member(jsii_name="putEnumTypeOptions")
    def put_enum_type_options(
        self,
        *,
        possible_values: typing.Sequence[builtins.str],
        validation_check_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param possible_values: List of possible enum values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#possible_values GoogleDocumentAiWarehouseDocumentSchema#possible_values}
        :param validation_check_disabled: Make sure the enum property value provided in the document is in the possile value list during document creation. The validation check runs by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#validation_check_disabled GoogleDocumentAiWarehouseDocumentSchema#validation_check_disabled}
        '''
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions(
            possible_values=possible_values,
            validation_check_disabled=validation_check_disabled,
        )

        return typing.cast(None, jsii.invoke(self, "putEnumTypeOptions", [value]))

    @jsii.member(jsii_name="putFloatTypeOptions")
    def put_float_type_options(self) -> None:
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putFloatTypeOptions", [value]))

    @jsii.member(jsii_name="putIntegerTypeOptions")
    def put_integer_type_options(self) -> None:
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putIntegerTypeOptions", [value]))

    @jsii.member(jsii_name="putMapTypeOptions")
    def put_map_type_options(self) -> None:
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putMapTypeOptions", [value]))

    @jsii.member(jsii_name="putSchemaSources")
    def put_schema_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29295285e778c8039549b862f27080721117641b6824c22c5fa256a20af1f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchemaSources", [value]))

    @jsii.member(jsii_name="putTextTypeOptions")
    def put_text_type_options(self) -> None:
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions()

        return typing.cast(None, jsii.invoke(self, "putTextTypeOptions", [value]))

    @jsii.member(jsii_name="putTimestampTypeOptions")
    def put_timestamp_type_options(self) -> None:
        value = GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions()

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
    ) -> GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptionsOutputReference:
        return typing.cast(GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptionsOutputReference, jsii.get(self, "dateTimeTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="enumTypeOptions")
    def enum_type_options(
        self,
    ) -> GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptionsOutputReference:
        return typing.cast(GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptionsOutputReference, jsii.get(self, "enumTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="floatTypeOptions")
    def float_type_options(
        self,
    ) -> GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptionsOutputReference:
        return typing.cast(GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptionsOutputReference, jsii.get(self, "floatTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="integerTypeOptions")
    def integer_type_options(
        self,
    ) -> GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptionsOutputReference:
        return typing.cast(GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptionsOutputReference, jsii.get(self, "integerTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="mapTypeOptions")
    def map_type_options(
        self,
    ) -> GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptionsOutputReference:
        return typing.cast(GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptionsOutputReference, jsii.get(self, "mapTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="schemaSources")
    def schema_sources(
        self,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesList":
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesList", jsii.get(self, "schemaSources"))

    @builtins.property
    @jsii.member(jsii_name="textTypeOptions")
    def text_type_options(
        self,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptionsOutputReference":
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptionsOutputReference", jsii.get(self, "textTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeOptions")
    def timestamp_type_options(
        self,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptionsOutputReference":
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptionsOutputReference", jsii.get(self, "timestampTypeOptions"))

    @builtins.property
    @jsii.member(jsii_name="dateTimeTypeOptionsInput")
    def date_time_type_options_input(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions], jsii.get(self, "dateTimeTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enumTypeOptionsInput")
    def enum_type_options_input(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions], jsii.get(self, "enumTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="floatTypeOptionsInput")
    def float_type_options_input(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions], jsii.get(self, "floatTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="integerTypeOptionsInput")
    def integer_type_options_input(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions], jsii.get(self, "integerTypeOptionsInput"))

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
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions], jsii.get(self, "mapTypeOptionsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources"]]], jsii.get(self, "schemaSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="textTypeOptionsInput")
    def text_type_options_input(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions"]:
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions"], jsii.get(self, "textTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeOptionsInput")
    def timestamp_type_options_input(
        self,
    ) -> typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions"]:
        return typing.cast(typing.Optional["GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions"], jsii.get(self, "timestampTypeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959f63a114b26c1108a95c6d4a42b01f74ace2fde42bf4e56c30a0dd5f781a1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca3553b48e8c98ba7cc18618d66455e8e1be93edaf8d49d7b71a3e3ad05ece23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__149033f6a6ca955719c579f6d540f6930b0119f4b4028a5b131f24a85018c68d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f62f80df7364a0300eb86722644cb2636398b8a3598c7e778c9785a09371ae0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3e9c0efe121faee0ce3c014e45528a8ecf117d1bc841acf5292b7cf5b75057e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__920528d2990fc7910f4a2e9a609b718f6c42d195374a430ef2f5882f0db2af6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSearchable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a508e3c77463d636c02889e934c88c8869a0e41ab0487577e9aa88c54d9663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retrievalImportance")
    def retrieval_importance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retrievalImportance"))

    @retrieval_importance.setter
    def retrieval_importance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf9fd4a9ea149905727df2e3a49dae31e60935e0a7e989b40e67bfe8942e15a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retrievalImportance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7a3006e133f50dd1bff4398f34f171297eae9858ce3471a686b510cb8d3bcaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "processor_type": "processorType"},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        processor_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The schema name in the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#name GoogleDocumentAiWarehouseDocumentSchema#name}
        :param processor_type: The Doc AI processor type name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#processor_type GoogleDocumentAiWarehouseDocumentSchema#processor_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd83772daedcd7cae6c7a55080737f16776b6212d0961f474c19dfb56d6a5c3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#name GoogleDocumentAiWarehouseDocumentSchema#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processor_type(self) -> typing.Optional[builtins.str]:
        '''The Doc AI processor type name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#processor_type GoogleDocumentAiWarehouseDocumentSchema#processor_type}
        '''
        result = self._values.get("processor_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1332aed0a8f6654657b85362b274551828aea2ad63b78413edaf7079b060debb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba147e7f7b6df6726aab49acca5f3f5fe063a2e628d017fe9923f19bcc8e9930)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d545f189fc5c68376546ee79aa1300b227a65cd1093825885f3f15acaa7a4af4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02f48be40030b80f6271277904cb09571fb40913485d48f62ba38df3bd9cd913)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14c67cbfefa251da6d856702adab8fa0b08c4cf11fa4a5ca238cb4ed53fd9736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806c0da9058a2c1af7def273c93141c6d437211accefa564a461babb77efb778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8460a3dbc8b3a5c297dfa11e2888429ac98a13d233cf0e0cd4d051ed096e2ba8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2002d901334f2fbe2494cd2b45f3e416f5bb0e5d32d77de5ae8f9e67d6030d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="processorType")
    def processor_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processorType"))

    @processor_type.setter
    def processor_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6cf4e865d106bb0fe8a08b04e03cf50d41537a5f9bb1b89d5b46eb704e1f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "processorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2032e14ffdee19e260d24301df2a175bd7eddf7648bccb58e53eb8605353e228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40b8af57c707148586d6fb075fe9efe94f6bbe68c615e6767f6f88db81ac6cb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d249d9adbc709c02e53b2b91aaa76acf0a2b10d45603f78ac94efed1427a3b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf2904820e7b0eeb07e2115fc55d6e0e9f9d4e06b04d63006bca782c472500ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855fd02d5a68d8a98c238ba7495f61057af8498bd70ea0987f33ad0dbe7812c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "processor_type": "processorType"},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        processor_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The schema name in the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#name GoogleDocumentAiWarehouseDocumentSchema#name}
        :param processor_type: The Doc AI processor type name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#processor_type GoogleDocumentAiWarehouseDocumentSchema#processor_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__449a4430d2d8a1977f22b5c6f19f1d484ab54c9068b8e19ec384e9225608ae86)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#name GoogleDocumentAiWarehouseDocumentSchema#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processor_type(self) -> typing.Optional[builtins.str]:
        '''The Doc AI processor type name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#processor_type GoogleDocumentAiWarehouseDocumentSchema#processor_type}
        '''
        result = self._values.get("processor_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d46eb158da80cd64a7bee49267b5fce25cb4e9952f583d265d623c61af9146a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2829e3b6684ccc6fca8b6aed5f933c1ccd20905db790e17ae5f3d55f2d6a81c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5198628fc29027538598d8a154a772e6da72f0cc9c9affe0d2d494ca24a4da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c30a9e852b6f5972e77144e476b4a2ef71ba7282f9cd15ed2114fea533ce530)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cbbbfaa16110318cef96e8a2ce3f396c8799045b8318ab775eeb4a5f8a48e2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8f087525ec5650deec962fcaecf46ac0ca4df8bc6e35e3e39a86d9d370a011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc304f56009790ccf5fd55ed1f30ccf0d521de9dd9d8c994728e73b7a5a5ca78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5c2e7048a367995fb3850ca63f1c5ed2311bd01fc8580e41a6348b08812d404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="processorType")
    def processor_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processorType"))

    @processor_type.setter
    def processor_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290c24c573e1734fd374a381e9b15e1ff6873de766537a8dcc6bb952e940cfa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "processorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68f38183cdb5118e222244c245b52b2830e7389df30e8e16ef6bcf665786b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c65dadb65226ad5e02bb124d6cf708b32198f96f3e44294dc3450cdb33f97ebe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d78941c46a9016407b607698725581f2ed4e2143cb5a87638c18143b32331b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f411889aa385a3e0596fc1160b566d4f762172c6aa2290b78bce5bcfbb28484)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions]:
        return typing.cast(typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__526e251768d8c8a4ca9f03db947698fbef8c166d518461cc36ed65ca015691a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleDocumentAiWarehouseDocumentSchemaTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#create GoogleDocumentAiWarehouseDocumentSchema#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#delete GoogleDocumentAiWarehouseDocumentSchema#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa964db869ee67f09116c68d5d2b5ecf8f03579a7fd4ffce3657b6e4cb4ee0e0)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#create GoogleDocumentAiWarehouseDocumentSchema#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_document_ai_warehouse_document_schema#delete GoogleDocumentAiWarehouseDocumentSchema#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDocumentAiWarehouseDocumentSchemaTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDocumentAiWarehouseDocumentSchemaTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDocumentAiWarehouseDocumentSchema.GoogleDocumentAiWarehouseDocumentSchemaTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b235438cc40dfec074cce621e456c48429da942548300ba7bc4ffd3b07ff6dd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3362bd69334d583788d1815b23658d33a8196f130d7ed260eb674840ebeeced5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd8055ff009781d74ac89af20ab3cf2f64c3dc6fa76f7b0fbab18ed73507913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f305060d2ae650637ea50056134f096a0ab2f6f3bbc2a57eecdc9b69e46e1e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDocumentAiWarehouseDocumentSchema",
    "GoogleDocumentAiWarehouseDocumentSchemaConfig",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsList",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsList",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesList",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSourcesOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesList",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSourcesOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions",
    "GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptionsOutputReference",
    "GoogleDocumentAiWarehouseDocumentSchemaTimeouts",
    "GoogleDocumentAiWarehouseDocumentSchemaTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0fc3ea5d1bc17ada006e966a37aa01e513d25fc2bd09e78e96a3de269e3b5b5b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    project_number: builtins.str,
    property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions, typing.Dict[builtins.str, typing.Any]]]],
    document_is_folder: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ff1b7f3a7bc74329812222291427086fb59697b5b2e4235895543f4191cb8222(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b5f28f37e758469a33ea651fe01bf4a57a92fab45d02b01c8bf8c138680b4e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ade059736000ce592f80c9cbcb747209cacdd048081086a73219dddf240a333(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c15626f679458b5f987a1796fa07681084c6346da22f2c6f95ba1f04c8fe2a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab25c3400bd1bacb313c41ecb2be95f36d5d7b0d7bcc2b70aa70345fc61d8bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931cda6a85f3258e77ba64478f5bc24f3e017fc97c26ebf84e1c72850f172ac9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45598f53d262da97ae4cf3ceb496780e34e92c1b2e10d522411ce0a346f544d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144a6ec60bca8fee45f851134b9a0be30760d07860fdecd43f055c590894a1a0(
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
    property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions, typing.Dict[builtins.str, typing.Any]]]],
    document_is_folder: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9abfc172ff1ed783ed29f5c4b625d3f89d536dae289e31deecc54dab04474dc4(
    *,
    name: builtins.str,
    date_time_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    enum_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    float_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    is_filterable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_repeatable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    map_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    property_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    retrieval_importance: typing.Optional[builtins.str] = None,
    schema_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    text_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timestamp_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815d3aff0d29d296f9229ad129d13d70cadb932da7340df27c024b9ca4dbe421(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0b8e4a66e11ef380286060b2d55de90c77561f002a903ce6a6ea8631c0dea1(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsDateTimeTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7883c36bbddb0989778ed538f40bebe481e91fa2c559af0d5e410dba92d52bd(
    *,
    possible_values: typing.Sequence[builtins.str],
    validation_check_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85b8184e5784b9a247cca1512aa3aca919fb263b16c21f318d8b4bea4a50963(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8bf38d696f9f6fc71c23ee24b1f6d4896be868ba9fb6195dbb111b91582fcfe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c22090ef33962f8a4d6adfdefbbfaf78831f1f1204966dd58d0eb3aef701479(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b425a0be345a5e0bd9c1110c77affac93a7daaada5261557ac59732c5735aa(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsEnumTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185ff71d3362317f1a2a6aa28074a4c27b0ef8a621b65229ba0c5e4e6714581c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e39f14ef12f2f4ae8c6a8412e3bc4089262ccb2936f8b31b26b486e26147784(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsFloatTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d89166533159df6d44c27b5c6d47b050a69bbff24a7502e8e218dfb8d533b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2f09969c34f253237eb8df6bb5aad84fef154a489e0b1b8793d88135e16b6b(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsIntegerTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d29167c6b121bd39f16458539519dd5f444188acd1389d3c61ed62ef511892(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff94f53abd425ccbd3f46cd8c6b74c96f1fad8f4265f4b9b0b275e359556129c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa56f22dd0637e58cbb9335561fadf242a715f2e16ce1d464c1c783c64621cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462bce610889c7e89806f85e06109015f4e9945e1eaf74861557d4fb3b24fc5f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1726c7c88a8c70a0fb680125471f0c6f934a0433c1461430b8025a63c399b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89afba33de53b9e68533e6c30cfbdcdc5637d3e59e974eb82765df2f828feee6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f72f28d00f7e2a890c4b1db51cf95b190a09510eee4b854e1f9cf72c41a7e57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1746d32f07dd8da9df487f8c8f9664757f52df60562ee72e1c2f742804a455(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsMapTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fde34c6fc6b3002cff50a65f5c88e4f207698136d1b198e1e9727f81d9af04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3dc532a9191619471aa68431e262c5dec9c541a0601dcc6065f9e79b8ecd43e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194931a750869eec96794dbe34ed107378f27efd8d9c1ebfce9dc160ed0ef3bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4756b8f805d86aa4111de16aaa7c88ab77590700771d80019447fa3a69e9b4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63c83bba42044568b6ea98c8b4c8658db5cc15834949fec5d88d8a4f6f7465d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29a303468c526a112d6b9299a20bd423f238f984ccd6fd8619c53182f02ad9c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d8fca97856f94a3c2cfce50cd00e3e944762eaf67a24773a2adf31f3d553fc3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee840db2a3dbee2530f70e1bd0355b0d298f2beb7841339e1df62da7b015879e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ea58a8c0bd9c803a5a60bd02c6482b2d756031314aa1d65dc5bf2c7178d27a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0dbaf1ee54a57e59cab6691635518f610a2929ff2d773b52077fa68e5b05d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804fe551c7edf292a42ad8b29bf7b2087202e84203355dfb2833540672a1a6d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45cbd31e9754650afb9c69038d49b2af88cdea3b96dd0f33fe0ca7f30ace9a23(
    *,
    property_definitions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e750d99a9316f597b2f7d31517c8e65ef183a5e6155813442c5bdc81e851fed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2edf07e051532b3d01d4e8ef3f0510409d6903827e1ea9a5a96c08302104cad(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9cf904c4f12fd10685faff33ee7b0b3804d14a68725b643c1d473926e6154e(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166753fb341689c7ea665937d7c8e530804df95753f3395ed250980f60285c28(
    *,
    name: builtins.str,
    date_time_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    enum_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    float_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    integer_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    is_filterable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_metadata: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_repeatable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_searchable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    map_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    retrieval_importance: typing.Optional[builtins.str] = None,
    schema_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    text_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timestamp_type_options: typing.Optional[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d02e640542860bf8c9e2a0fe0ce258bf97c5ee45c6da44555e1ffe79d055d78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d52ed7b7ad368f36c9131440f09e25ae813e5ad04ff06392fc43f6518c0ccce(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsDateTimeTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd07ace774a460fed3a64bd2ce7d74766532da37ac0ca9e601b288f82367f3ff(
    *,
    possible_values: typing.Sequence[builtins.str],
    validation_check_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a85945f30b1c247535d9bdb8c7631826f06a03ec6e1dc0c253c0aeb59b8413(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d48d8bde83b78f44f94da3cba6f154b397ee5fd14196ee66770f3fac187bef1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63047a7bb8bfbf6e207da26358614f696672b2d3c458867d864c6fd5e89d4ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37feb7614de8c01854933ad737340ddf256eccc04ee6cd6829ceb1c101fdf345(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsEnumTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec23700a0139d1b9e317db81afef9b7e03367e5ed0c879bf7a0958066c771c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__189861a609b2642b6a3d8d75bf66302127d648295b7722cdbaca464572b77705(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsFloatTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b1de2e74fca95c7225ed3f7e50790b78985685ba0927b7d0c381b4531aeafc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8146e0361d09411727168b5e7a4a3f653c9ca782b73dfd6eba2df0f6dae046(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsIntegerTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7c964c382219481ca05c546dff6e5105c6886afeb3b691076e6a47318ec46a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3272ea18ef5341f97593d4e79de19d3063b9b11758537e1de3bd132c9ba29e7f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e1238ce9ac3b5002414c27d74f43cc014b6f5a491fdfccecbc1d28a973623d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__717bddc1a6dd2c1ce1244a157e07b7faa156de367dc25fdd76c6cdc262f6da35(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0952615caf9ee61d7098f6ebbfbfb59eb1affc3e6c3034269f7917ef481cb574(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19fb55939bc9b543bf0703482b010c7262b7a217f98eb99d1af24c4d98c8d5eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bc4c18ac1e07824e25b7be786c2d9ad2adb3718921c05f5c387e42b470b8c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__193523e312160f3e20cafa784cd95596bc1caa0a3af7cb9de18d7d4795ee0c40(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsMapTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20d93588bc045ecd363f9f5e7226b58e0d3d3168ca28ae1c27bae19b2e467b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29295285e778c8039549b862f27080721117641b6824c22c5fa256a20af1f7f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959f63a114b26c1108a95c6d4a42b01f74ace2fde42bf4e56c30a0dd5f781a1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca3553b48e8c98ba7cc18618d66455e8e1be93edaf8d49d7b71a3e3ad05ece23(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149033f6a6ca955719c579f6d540f6930b0119f4b4028a5b131f24a85018c68d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62f80df7364a0300eb86722644cb2636398b8a3598c7e778c9785a09371ae0b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e9c0efe121faee0ce3c014e45528a8ecf117d1bc841acf5292b7cf5b75057e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920528d2990fc7910f4a2e9a609b718f6c42d195374a430ef2f5882f0db2af6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a508e3c77463d636c02889e934c88c8869a0e41ab0487577e9aa88c54d9663(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf9fd4a9ea149905727df2e3a49dae31e60935e0a7e989b40e67bfe8942e15a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a3006e133f50dd1bff4398f34f171297eae9858ce3471a686b510cb8d3bcaa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd83772daedcd7cae6c7a55080737f16776b6212d0961f474c19dfb56d6a5c3(
    *,
    name: typing.Optional[builtins.str] = None,
    processor_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1332aed0a8f6654657b85362b274551828aea2ad63b78413edaf7079b060debb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba147e7f7b6df6726aab49acca5f3f5fe063a2e628d017fe9923f19bcc8e9930(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d545f189fc5c68376546ee79aa1300b227a65cd1093825885f3f15acaa7a4af4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f48be40030b80f6271277904cb09571fb40913485d48f62ba38df3bd9cd913(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c67cbfefa251da6d856702adab8fa0b08c4cf11fa4a5ca238cb4ed53fd9736(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806c0da9058a2c1af7def273c93141c6d437211accefa564a461babb77efb778(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8460a3dbc8b3a5c297dfa11e2888429ac98a13d233cf0e0cd4d051ed096e2ba8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2002d901334f2fbe2494cd2b45f3e416f5bb0e5d32d77de5ae8f9e67d6030d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6cf4e865d106bb0fe8a08b04e03cf50d41537a5f9bb1b89d5b46eb704e1f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2032e14ffdee19e260d24301df2a175bd7eddf7648bccb58e53eb8605353e228(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsSchemaSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b8af57c707148586d6fb075fe9efe94f6bbe68c615e6767f6f88db81ac6cb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d249d9adbc709c02e53b2b91aaa76acf0a2b10d45603f78ac94efed1427a3b00(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTextTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2904820e7b0eeb07e2115fc55d6e0e9f9d4e06b04d63006bca782c472500ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855fd02d5a68d8a98c238ba7495f61057af8498bd70ea0987f33ad0dbe7812c4(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsPropertyTypeOptionsPropertyDefinitionsTimestampTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449a4430d2d8a1977f22b5c6f19f1d484ab54c9068b8e19ec384e9225608ae86(
    *,
    name: typing.Optional[builtins.str] = None,
    processor_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d46eb158da80cd64a7bee49267b5fce25cb4e9952f583d265d623c61af9146a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2829e3b6684ccc6fca8b6aed5f933c1ccd20905db790e17ae5f3d55f2d6a81c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5198628fc29027538598d8a154a772e6da72f0cc9c9affe0d2d494ca24a4da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c30a9e852b6f5972e77144e476b4a2ef71ba7282f9cd15ed2114fea533ce530(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cbbbfaa16110318cef96e8a2ce3f396c8799045b8318ab775eeb4a5f8a48e2f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8f087525ec5650deec962fcaecf46ac0ca4df8bc6e35e3e39a86d9d370a011(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc304f56009790ccf5fd55ed1f30ccf0d521de9dd9d8c994728e73b7a5a5ca78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c2e7048a367995fb3850ca63f1c5ed2311bd01fc8580e41a6348b08812d404(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290c24c573e1734fd374a381e9b15e1ff6873de766537a8dcc6bb952e940cfa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68f38183cdb5118e222244c245b52b2830e7389df30e8e16ef6bcf665786b43(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsSchemaSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65dadb65226ad5e02bb124d6cf708b32198f96f3e44294dc3450cdb33f97ebe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d78941c46a9016407b607698725581f2ed4e2143cb5a87638c18143b32331b(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTextTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f411889aa385a3e0596fc1160b566d4f762172c6aa2290b78bce5bcfbb28484(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__526e251768d8c8a4ca9f03db947698fbef8c166d518461cc36ed65ca015691a3(
    value: typing.Optional[GoogleDocumentAiWarehouseDocumentSchemaPropertyDefinitionsTimestampTypeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa964db869ee67f09116c68d5d2b5ecf8f03579a7fd4ffce3657b6e4cb4ee0e0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b235438cc40dfec074cce621e456c48429da942548300ba7bc4ffd3b07ff6dd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3362bd69334d583788d1815b23658d33a8196f130d7ed260eb674840ebeeced5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd8055ff009781d74ac89af20ab3cf2f64c3dc6fa76f7b0fbab18ed73507913(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f305060d2ae650637ea50056134f096a0ab2f6f3bbc2a57eecdc9b69e46e1e17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDocumentAiWarehouseDocumentSchemaTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
