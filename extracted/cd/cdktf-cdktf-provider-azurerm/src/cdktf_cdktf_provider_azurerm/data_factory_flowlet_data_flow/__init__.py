r'''
# `azurerm_data_factory_flowlet_data_flow`

Refer to the Terraform Registry for docs: [`azurerm_data_factory_flowlet_data_flow`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow).
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


class DataFactoryFlowletDataFlow(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlow",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow azurerm_data_factory_flowlet_data_flow}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_factory_id: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        folder: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
        script_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
        sink: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryFlowletDataFlowSink", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryFlowletDataFlowSource", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryFlowletDataFlowTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transformation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryFlowletDataFlowTransformation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow azurerm_data_factory_flowlet_data_flow} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_factory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#data_factory_id DataFactoryFlowletDataFlow#data_factory_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param annotations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#annotations DataFactoryFlowletDataFlow#annotations}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#description DataFactoryFlowletDataFlow#description}.
        :param folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#folder DataFactoryFlowletDataFlow#folder}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#id DataFactoryFlowletDataFlow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#script DataFactoryFlowletDataFlow#script}.
        :param script_lines: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#script_lines DataFactoryFlowletDataFlow#script_lines}.
        :param sink: sink block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#sink DataFactoryFlowletDataFlow#sink}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#source DataFactoryFlowletDataFlow#source}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#timeouts DataFactoryFlowletDataFlow#timeouts}
        :param transformation: transformation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#transformation DataFactoryFlowletDataFlow#transformation}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58d72bdbfbb75606cd3efe64dc18da8e2b2cdea19c0d18ed7e177dc86478c6fc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataFactoryFlowletDataFlowConfig(
            data_factory_id=data_factory_id,
            name=name,
            annotations=annotations,
            description=description,
            folder=folder,
            id=id,
            script=script,
            script_lines=script_lines,
            sink=sink,
            source=source,
            timeouts=timeouts,
            transformation=transformation,
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
        '''Generates CDKTF code for importing a DataFactoryFlowletDataFlow resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataFactoryFlowletDataFlow to import.
        :param import_from_id: The id of the existing DataFactoryFlowletDataFlow that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataFactoryFlowletDataFlow to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f4f0ae116e1fbf4f32ee897d3145ba51c85be2a94c59174cedc3f3ce57a563)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSink")
    def put_sink(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryFlowletDataFlowSink", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d3208efe972ae4202c001c9c482ef42a2160cfb943516a4c12135cb6a324f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSink", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryFlowletDataFlowSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb23bd95d0252d6280d0d60094db245046662c514aebced0a6c2b998dd524f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#create DataFactoryFlowletDataFlow#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#delete DataFactoryFlowletDataFlow#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#read DataFactoryFlowletDataFlow#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#update DataFactoryFlowletDataFlow#update}.
        '''
        value = DataFactoryFlowletDataFlowTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTransformation")
    def put_transformation(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryFlowletDataFlowTransformation", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ea9e12603a31750ede9779ec0f97d50e6e27f8f086786f8191bfcadabfd476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTransformation", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFolder")
    def reset_folder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFolder", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetScript")
    def reset_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScript", []))

    @jsii.member(jsii_name="resetScriptLines")
    def reset_script_lines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptLines", []))

    @jsii.member(jsii_name="resetSink")
    def reset_sink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSink", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTransformation")
    def reset_transformation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformation", []))

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
    @jsii.member(jsii_name="sink")
    def sink(self) -> "DataFactoryFlowletDataFlowSinkList":
        return typing.cast("DataFactoryFlowletDataFlowSinkList", jsii.get(self, "sink"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "DataFactoryFlowletDataFlowSourceList":
        return typing.cast("DataFactoryFlowletDataFlowSourceList", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataFactoryFlowletDataFlowTimeoutsOutputReference":
        return typing.cast("DataFactoryFlowletDataFlowTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="transformation")
    def transformation(self) -> "DataFactoryFlowletDataFlowTransformationList":
        return typing.cast("DataFactoryFlowletDataFlowTransformationList", jsii.get(self, "transformation"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFactoryIdInput")
    def data_factory_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFactoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="folderInput")
    def folder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "folderInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptInput")
    def script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptLinesInput")
    def script_lines_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scriptLinesInput"))

    @builtins.property
    @jsii.member(jsii_name="sinkInput")
    def sink_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryFlowletDataFlowSink"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryFlowletDataFlowSink"]]], jsii.get(self, "sinkInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryFlowletDataFlowSource"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryFlowletDataFlowSource"]]], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataFactoryFlowletDataFlowTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataFactoryFlowletDataFlowTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transformationInput")
    def transformation_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryFlowletDataFlowTransformation"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryFlowletDataFlowTransformation"]]], jsii.get(self, "transformationInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__768a944bb414a0fc8c95800e95fc1416c206aeab5549d62e77778a98b782b460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataFactoryId")
    def data_factory_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataFactoryId"))

    @data_factory_id.setter
    def data_factory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b192326516e5fe422a2dbb64ae73a38330970493ffee31297c81ebd98dd87d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFactoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956e12ab44b9539a69a9a10e57f3d68151bdff9f9a02ce3b8eeab8e7307cc02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="folder")
    def folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folder"))

    @folder.setter
    def folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04289a93b7a05ba276ce3ded5c65af1529863bd6e79b97573bdc3c7dc244bb0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f987c430edb7815c4e19f45d2ecda409a56a3c04fc02537e92d37b70d2291f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b57edb42d2db5af73d411a58da096726f4a09d18be8575206d52a206538ecbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d92e057157991f33e8dbfc7519a1631794646717d0e6a66d1b533b0e1aebd87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptLines")
    def script_lines(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scriptLines"))

    @script_lines.setter
    def script_lines(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__313e91a9d41cf33b39b2f74825aca2c9544fc3cf49e0ad913f292d6f947bd243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptLines", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_factory_id": "dataFactoryId",
        "name": "name",
        "annotations": "annotations",
        "description": "description",
        "folder": "folder",
        "id": "id",
        "script": "script",
        "script_lines": "scriptLines",
        "sink": "sink",
        "source": "source",
        "timeouts": "timeouts",
        "transformation": "transformation",
    },
)
class DataFactoryFlowletDataFlowConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_factory_id: builtins.str,
        name: builtins.str,
        annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        folder: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
        script_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
        sink: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryFlowletDataFlowSink", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryFlowletDataFlowSource", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryFlowletDataFlowTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transformation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataFactoryFlowletDataFlowTransformation", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_factory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#data_factory_id DataFactoryFlowletDataFlow#data_factory_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param annotations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#annotations DataFactoryFlowletDataFlow#annotations}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#description DataFactoryFlowletDataFlow#description}.
        :param folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#folder DataFactoryFlowletDataFlow#folder}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#id DataFactoryFlowletDataFlow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#script DataFactoryFlowletDataFlow#script}.
        :param script_lines: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#script_lines DataFactoryFlowletDataFlow#script_lines}.
        :param sink: sink block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#sink DataFactoryFlowletDataFlow#sink}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#source DataFactoryFlowletDataFlow#source}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#timeouts DataFactoryFlowletDataFlow#timeouts}
        :param transformation: transformation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#transformation DataFactoryFlowletDataFlow#transformation}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DataFactoryFlowletDataFlowTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2a6b3e92e1364c65c39217aaf055cb2363ce8499648b73fa21f883a6b6492c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_factory_id", value=data_factory_id, expected_type=type_hints["data_factory_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument folder", value=folder, expected_type=type_hints["folder"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument script_lines", value=script_lines, expected_type=type_hints["script_lines"])
            check_type(argname="argument sink", value=sink, expected_type=type_hints["sink"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument transformation", value=transformation, expected_type=type_hints["transformation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_factory_id": data_factory_id,
            "name": name,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if description is not None:
            self._values["description"] = description
        if folder is not None:
            self._values["folder"] = folder
        if id is not None:
            self._values["id"] = id
        if script is not None:
            self._values["script"] = script
        if script_lines is not None:
            self._values["script_lines"] = script_lines
        if sink is not None:
            self._values["sink"] = sink
        if source is not None:
            self._values["source"] = source
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if transformation is not None:
            self._values["transformation"] = transformation

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
    def data_factory_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#data_factory_id DataFactoryFlowletDataFlow#data_factory_id}.'''
        result = self._values.get("data_factory_id")
        assert result is not None, "Required property 'data_factory_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#annotations DataFactoryFlowletDataFlow#annotations}.'''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#description DataFactoryFlowletDataFlow#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def folder(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#folder DataFactoryFlowletDataFlow#folder}.'''
        result = self._values.get("folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#id DataFactoryFlowletDataFlow#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#script DataFactoryFlowletDataFlow#script}.'''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_lines(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#script_lines DataFactoryFlowletDataFlow#script_lines}.'''
        result = self._values.get("script_lines")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sink(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryFlowletDataFlowSink"]]]:
        '''sink block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#sink DataFactoryFlowletDataFlow#sink}
        '''
        result = self._values.get("sink")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryFlowletDataFlowSink"]]], result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryFlowletDataFlowSource"]]]:
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#source DataFactoryFlowletDataFlow#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryFlowletDataFlowSource"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataFactoryFlowletDataFlowTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#timeouts DataFactoryFlowletDataFlow#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowTimeouts"], result)

    @builtins.property
    def transformation(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryFlowletDataFlowTransformation"]]]:
        '''transformation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#transformation DataFactoryFlowletDataFlow#transformation}
        '''
        result = self._values.get("transformation")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataFactoryFlowletDataFlowTransformation"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSink",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "dataset": "dataset",
        "description": "description",
        "flowlet": "flowlet",
        "linked_service": "linkedService",
        "rejected_linked_service": "rejectedLinkedService",
        "schema_linked_service": "schemaLinkedService",
    },
)
class DataFactoryFlowletDataFlowSink:
    def __init__(
        self,
        *,
        name: builtins.str,
        dataset: typing.Optional[typing.Union["DataFactoryFlowletDataFlowSinkDataset", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        flowlet: typing.Optional[typing.Union["DataFactoryFlowletDataFlowSinkFlowlet", typing.Dict[builtins.str, typing.Any]]] = None,
        linked_service: typing.Optional[typing.Union["DataFactoryFlowletDataFlowSinkLinkedService", typing.Dict[builtins.str, typing.Any]]] = None,
        rejected_linked_service: typing.Optional[typing.Union["DataFactoryFlowletDataFlowSinkRejectedLinkedService", typing.Dict[builtins.str, typing.Any]]] = None,
        schema_linked_service: typing.Optional[typing.Union["DataFactoryFlowletDataFlowSinkSchemaLinkedService", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param dataset: dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset DataFactoryFlowletDataFlow#dataset}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#description DataFactoryFlowletDataFlow#description}.
        :param flowlet: flowlet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#flowlet DataFactoryFlowletDataFlow#flowlet}
        :param linked_service: linked_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#linked_service DataFactoryFlowletDataFlow#linked_service}
        :param rejected_linked_service: rejected_linked_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#rejected_linked_service DataFactoryFlowletDataFlow#rejected_linked_service}
        :param schema_linked_service: schema_linked_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#schema_linked_service DataFactoryFlowletDataFlow#schema_linked_service}
        '''
        if isinstance(dataset, dict):
            dataset = DataFactoryFlowletDataFlowSinkDataset(**dataset)
        if isinstance(flowlet, dict):
            flowlet = DataFactoryFlowletDataFlowSinkFlowlet(**flowlet)
        if isinstance(linked_service, dict):
            linked_service = DataFactoryFlowletDataFlowSinkLinkedService(**linked_service)
        if isinstance(rejected_linked_service, dict):
            rejected_linked_service = DataFactoryFlowletDataFlowSinkRejectedLinkedService(**rejected_linked_service)
        if isinstance(schema_linked_service, dict):
            schema_linked_service = DataFactoryFlowletDataFlowSinkSchemaLinkedService(**schema_linked_service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75bad8be205ec8d501358a58070dbc70014b6509275e3b0723c71b1239c0a38)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument flowlet", value=flowlet, expected_type=type_hints["flowlet"])
            check_type(argname="argument linked_service", value=linked_service, expected_type=type_hints["linked_service"])
            check_type(argname="argument rejected_linked_service", value=rejected_linked_service, expected_type=type_hints["rejected_linked_service"])
            check_type(argname="argument schema_linked_service", value=schema_linked_service, expected_type=type_hints["schema_linked_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if dataset is not None:
            self._values["dataset"] = dataset
        if description is not None:
            self._values["description"] = description
        if flowlet is not None:
            self._values["flowlet"] = flowlet
        if linked_service is not None:
            self._values["linked_service"] = linked_service
        if rejected_linked_service is not None:
            self._values["rejected_linked_service"] = rejected_linked_service
        if schema_linked_service is not None:
            self._values["schema_linked_service"] = schema_linked_service

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset(self) -> typing.Optional["DataFactoryFlowletDataFlowSinkDataset"]:
        '''dataset block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset DataFactoryFlowletDataFlow#dataset}
        '''
        result = self._values.get("dataset")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSinkDataset"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#description DataFactoryFlowletDataFlow#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flowlet(self) -> typing.Optional["DataFactoryFlowletDataFlowSinkFlowlet"]:
        '''flowlet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#flowlet DataFactoryFlowletDataFlow#flowlet}
        '''
        result = self._values.get("flowlet")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSinkFlowlet"], result)

    @builtins.property
    def linked_service(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowSinkLinkedService"]:
        '''linked_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#linked_service DataFactoryFlowletDataFlow#linked_service}
        '''
        result = self._values.get("linked_service")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSinkLinkedService"], result)

    @builtins.property
    def rejected_linked_service(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowSinkRejectedLinkedService"]:
        '''rejected_linked_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#rejected_linked_service DataFactoryFlowletDataFlow#rejected_linked_service}
        '''
        result = self._values.get("rejected_linked_service")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSinkRejectedLinkedService"], result)

    @builtins.property
    def schema_linked_service(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowSinkSchemaLinkedService"]:
        '''schema_linked_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#schema_linked_service DataFactoryFlowletDataFlow#schema_linked_service}
        '''
        result = self._values.get("schema_linked_service")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSinkSchemaLinkedService"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowSink(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSinkDataset",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters"},
)
class DataFactoryFlowletDataFlowSinkDataset:
    def __init__(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d0a98caf28529d0a690cbe37bd10c65c896436226952617b1fa4ed08b5dae1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowSinkDataset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowSinkDatasetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSinkDatasetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba25b9aa57c5e559ffcfb79cf802eccd9b9b6f77c6bc5593da5a2a24eaa9d3a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51529b371918ebf8798f02e14b46555c16323beee8f73672f648d8067ea06908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712ecb357692e7c0ab92db826357df38e704fae79702d3842c90e7346b6f9ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataFactoryFlowletDataFlowSinkDataset]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSinkDataset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowSinkDataset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a0c142a196f9f3e242a47229ddd99547ca4e3b11084ec0656d0c36f54b7ea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSinkFlowlet",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "dataset_parameters": "datasetParameters",
        "parameters": "parameters",
    },
)
class DataFactoryFlowletDataFlowSinkFlowlet:
    def __init__(
        self,
        *,
        name: builtins.str,
        dataset_parameters: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param dataset_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset_parameters DataFactoryFlowletDataFlow#dataset_parameters}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2589d3dad67df502c2f93e0793073f3e2f2eb1a6fc212b114f4048e4860fc51)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dataset_parameters", value=dataset_parameters, expected_type=type_hints["dataset_parameters"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if dataset_parameters is not None:
            self._values["dataset_parameters"] = dataset_parameters
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset_parameters DataFactoryFlowletDataFlow#dataset_parameters}.'''
        result = self._values.get("dataset_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowSinkFlowlet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowSinkFlowletOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSinkFlowletOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__180f150a00560296de6d14ca6cd8a67317e4e9efc62f2c82a1dc16898dee3bfd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatasetParameters")
    def reset_dataset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetParameters", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="datasetParametersInput")
    def dataset_parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetParameters")
    def dataset_parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetParameters"))

    @dataset_parameters.setter
    def dataset_parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8666fe5fc9c390539dd219b2d04364ff2f1a5312ea717a6b9a9967698f709cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625b047a35ff7219da0fde4a5e534e94d81d8ea5a3ee352b24957ac305a78928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73262d81fdcbe854d682a636a2729a73adad96284e127741ee6cbb6ff1758526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataFactoryFlowletDataFlowSinkFlowlet]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSinkFlowlet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowSinkFlowlet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61451e6636566250727ff074ac8b796410f2e2696f0cfeec93b5dd59078d3e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSinkLinkedService",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters"},
)
class DataFactoryFlowletDataFlowSinkLinkedService:
    def __init__(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4faba067de4bd5546862cc2e7fac9a94515c166a068370d2ba1aeb7014f02dc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowSinkLinkedService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowSinkLinkedServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSinkLinkedServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae326bbfa7e2663bafcc12e45e6109b18f004361dca16928ce94f01060aa37af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5821051c6a36f682b334bbf53e2b70dbdc15f34c9520c89a02e5a856a607bb1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__896cae44c564c58f12f4aff23b017069a7f91ff67323683cd8d3ea5c5ab87c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowSinkLinkedService]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSinkLinkedService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowSinkLinkedService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f39646ee3d7f4de9f140efb5c4dcc30af0c99c8576905199d10cd0472e59b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryFlowletDataFlowSinkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSinkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b6c56491f285a4c1fdf950bedb293d7163e4322a682e755a51381e997892c17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataFactoryFlowletDataFlowSinkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ace3de93043e281b02df75b82895a266d12409239eea9d5e65f68fee2168d1f2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataFactoryFlowletDataFlowSinkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940836e9dfac79980c3d37cb828b18de98848793de3c59d6ec8b7b16d6a27e3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e5a48d32ea9099b2478afac3aa2626eba8bdeb8255dc9064f1085ef019f5875)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4107c1011ae46b71ac86fb45062bba976d60f542e5363a3354ee2e60fb79be7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryFlowletDataFlowSink]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryFlowletDataFlowSink]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryFlowletDataFlowSink]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4e4ff4f3415d0cfc8ed9aecb41823b36b0d37abc50bc5ea3189dacb87f7535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryFlowletDataFlowSinkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSinkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50fe490fbf77bf50b537c25d5789d4cf9291d978ce38cf122bc88405aa3d3bee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDataset")
    def put_dataset(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowSinkDataset(name=name, parameters=parameters)

        return typing.cast(None, jsii.invoke(self, "putDataset", [value]))

    @jsii.member(jsii_name="putFlowlet")
    def put_flowlet(
        self,
        *,
        name: builtins.str,
        dataset_parameters: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param dataset_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset_parameters DataFactoryFlowletDataFlow#dataset_parameters}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowSinkFlowlet(
            name=name, dataset_parameters=dataset_parameters, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putFlowlet", [value]))

    @jsii.member(jsii_name="putLinkedService")
    def put_linked_service(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowSinkLinkedService(
            name=name, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putLinkedService", [value]))

    @jsii.member(jsii_name="putRejectedLinkedService")
    def put_rejected_linked_service(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowSinkRejectedLinkedService(
            name=name, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putRejectedLinkedService", [value]))

    @jsii.member(jsii_name="putSchemaLinkedService")
    def put_schema_linked_service(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowSinkSchemaLinkedService(
            name=name, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaLinkedService", [value]))

    @jsii.member(jsii_name="resetDataset")
    def reset_dataset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataset", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFlowlet")
    def reset_flowlet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlowlet", []))

    @jsii.member(jsii_name="resetLinkedService")
    def reset_linked_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedService", []))

    @jsii.member(jsii_name="resetRejectedLinkedService")
    def reset_rejected_linked_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRejectedLinkedService", []))

    @jsii.member(jsii_name="resetSchemaLinkedService")
    def reset_schema_linked_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaLinkedService", []))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> DataFactoryFlowletDataFlowSinkDatasetOutputReference:
        return typing.cast(DataFactoryFlowletDataFlowSinkDatasetOutputReference, jsii.get(self, "dataset"))

    @builtins.property
    @jsii.member(jsii_name="flowlet")
    def flowlet(self) -> DataFactoryFlowletDataFlowSinkFlowletOutputReference:
        return typing.cast(DataFactoryFlowletDataFlowSinkFlowletOutputReference, jsii.get(self, "flowlet"))

    @builtins.property
    @jsii.member(jsii_name="linkedService")
    def linked_service(
        self,
    ) -> DataFactoryFlowletDataFlowSinkLinkedServiceOutputReference:
        return typing.cast(DataFactoryFlowletDataFlowSinkLinkedServiceOutputReference, jsii.get(self, "linkedService"))

    @builtins.property
    @jsii.member(jsii_name="rejectedLinkedService")
    def rejected_linked_service(
        self,
    ) -> "DataFactoryFlowletDataFlowSinkRejectedLinkedServiceOutputReference":
        return typing.cast("DataFactoryFlowletDataFlowSinkRejectedLinkedServiceOutputReference", jsii.get(self, "rejectedLinkedService"))

    @builtins.property
    @jsii.member(jsii_name="schemaLinkedService")
    def schema_linked_service(
        self,
    ) -> "DataFactoryFlowletDataFlowSinkSchemaLinkedServiceOutputReference":
        return typing.cast("DataFactoryFlowletDataFlowSinkSchemaLinkedServiceOutputReference", jsii.get(self, "schemaLinkedService"))

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional[DataFactoryFlowletDataFlowSinkDataset]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSinkDataset], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="flowletInput")
    def flowlet_input(self) -> typing.Optional[DataFactoryFlowletDataFlowSinkFlowlet]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSinkFlowlet], jsii.get(self, "flowletInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedServiceInput")
    def linked_service_input(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowSinkLinkedService]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSinkLinkedService], jsii.get(self, "linkedServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="rejectedLinkedServiceInput")
    def rejected_linked_service_input(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowSinkRejectedLinkedService"]:
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSinkRejectedLinkedService"], jsii.get(self, "rejectedLinkedServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaLinkedServiceInput")
    def schema_linked_service_input(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowSinkSchemaLinkedService"]:
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSinkSchemaLinkedService"], jsii.get(self, "schemaLinkedServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682e0d062712a22c392bd48493a987b20c408d2d3092375aa4089005126e42f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d56f791a94f8f8d3bb005627c0d389c29b549707e97072c20e4f1080129773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowSink]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowSink]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowSink]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__877b247a2d605ca95c1fc6aa52eaa93b4d988a8fb2a79554f09f5e746f9f2815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSinkRejectedLinkedService",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters"},
)
class DataFactoryFlowletDataFlowSinkRejectedLinkedService:
    def __init__(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9131372e2f502e32ac34ac890f28e85113a927bb2d04a1be336fef0d78a3167)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowSinkRejectedLinkedService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowSinkRejectedLinkedServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSinkRejectedLinkedServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e17802501c9915fcbef6ce46d0b55758aa4993e893f195c43a6d2f617d78215e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528d05bb4b14902d8042fc6bdb738d6f50dcd3eabf6f70641ba5b8345aa59dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3449630512131e2fef155e7cdce3973e4775a4797c1079076f60090b0d96ada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowSinkRejectedLinkedService]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSinkRejectedLinkedService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowSinkRejectedLinkedService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ba3cdae1440a49ca38cf32d6a6cb008edfb3f2e987e9ab409735297b76d3a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSinkSchemaLinkedService",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters"},
)
class DataFactoryFlowletDataFlowSinkSchemaLinkedService:
    def __init__(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5790bf7110a8d031f6624859e03ba4d0f2f4a7625b357b170b8431839661a9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowSinkSchemaLinkedService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowSinkSchemaLinkedServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSinkSchemaLinkedServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5836c3bc5844c3e4c44d7c29182129fb1378a039e9b783a848b290ffb3c31b14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b073ed8bd8113cd4c3019d6b231b7e140bed7488db3c5a09e95eba1bc8d7d58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3460f37b023edf81d95842681917779db476553d70a9c3a56f70e3fc894fb3ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowSinkSchemaLinkedService]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSinkSchemaLinkedService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowSinkSchemaLinkedService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9c513d5d7d36f5693589581b08e2d6ac533094082070bdb5477b32ebde70c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSource",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "dataset": "dataset",
        "description": "description",
        "flowlet": "flowlet",
        "linked_service": "linkedService",
        "rejected_linked_service": "rejectedLinkedService",
        "schema_linked_service": "schemaLinkedService",
    },
)
class DataFactoryFlowletDataFlowSource:
    def __init__(
        self,
        *,
        name: builtins.str,
        dataset: typing.Optional[typing.Union["DataFactoryFlowletDataFlowSourceDataset", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        flowlet: typing.Optional[typing.Union["DataFactoryFlowletDataFlowSourceFlowlet", typing.Dict[builtins.str, typing.Any]]] = None,
        linked_service: typing.Optional[typing.Union["DataFactoryFlowletDataFlowSourceLinkedService", typing.Dict[builtins.str, typing.Any]]] = None,
        rejected_linked_service: typing.Optional[typing.Union["DataFactoryFlowletDataFlowSourceRejectedLinkedService", typing.Dict[builtins.str, typing.Any]]] = None,
        schema_linked_service: typing.Optional[typing.Union["DataFactoryFlowletDataFlowSourceSchemaLinkedService", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param dataset: dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset DataFactoryFlowletDataFlow#dataset}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#description DataFactoryFlowletDataFlow#description}.
        :param flowlet: flowlet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#flowlet DataFactoryFlowletDataFlow#flowlet}
        :param linked_service: linked_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#linked_service DataFactoryFlowletDataFlow#linked_service}
        :param rejected_linked_service: rejected_linked_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#rejected_linked_service DataFactoryFlowletDataFlow#rejected_linked_service}
        :param schema_linked_service: schema_linked_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#schema_linked_service DataFactoryFlowletDataFlow#schema_linked_service}
        '''
        if isinstance(dataset, dict):
            dataset = DataFactoryFlowletDataFlowSourceDataset(**dataset)
        if isinstance(flowlet, dict):
            flowlet = DataFactoryFlowletDataFlowSourceFlowlet(**flowlet)
        if isinstance(linked_service, dict):
            linked_service = DataFactoryFlowletDataFlowSourceLinkedService(**linked_service)
        if isinstance(rejected_linked_service, dict):
            rejected_linked_service = DataFactoryFlowletDataFlowSourceRejectedLinkedService(**rejected_linked_service)
        if isinstance(schema_linked_service, dict):
            schema_linked_service = DataFactoryFlowletDataFlowSourceSchemaLinkedService(**schema_linked_service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97ff011f6a6b6a4d811367f7c917ae375dcb7725df7e960ce6b2853afb80f4e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument flowlet", value=flowlet, expected_type=type_hints["flowlet"])
            check_type(argname="argument linked_service", value=linked_service, expected_type=type_hints["linked_service"])
            check_type(argname="argument rejected_linked_service", value=rejected_linked_service, expected_type=type_hints["rejected_linked_service"])
            check_type(argname="argument schema_linked_service", value=schema_linked_service, expected_type=type_hints["schema_linked_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if dataset is not None:
            self._values["dataset"] = dataset
        if description is not None:
            self._values["description"] = description
        if flowlet is not None:
            self._values["flowlet"] = flowlet
        if linked_service is not None:
            self._values["linked_service"] = linked_service
        if rejected_linked_service is not None:
            self._values["rejected_linked_service"] = rejected_linked_service
        if schema_linked_service is not None:
            self._values["schema_linked_service"] = schema_linked_service

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset(self) -> typing.Optional["DataFactoryFlowletDataFlowSourceDataset"]:
        '''dataset block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset DataFactoryFlowletDataFlow#dataset}
        '''
        result = self._values.get("dataset")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSourceDataset"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#description DataFactoryFlowletDataFlow#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flowlet(self) -> typing.Optional["DataFactoryFlowletDataFlowSourceFlowlet"]:
        '''flowlet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#flowlet DataFactoryFlowletDataFlow#flowlet}
        '''
        result = self._values.get("flowlet")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSourceFlowlet"], result)

    @builtins.property
    def linked_service(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowSourceLinkedService"]:
        '''linked_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#linked_service DataFactoryFlowletDataFlow#linked_service}
        '''
        result = self._values.get("linked_service")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSourceLinkedService"], result)

    @builtins.property
    def rejected_linked_service(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowSourceRejectedLinkedService"]:
        '''rejected_linked_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#rejected_linked_service DataFactoryFlowletDataFlow#rejected_linked_service}
        '''
        result = self._values.get("rejected_linked_service")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSourceRejectedLinkedService"], result)

    @builtins.property
    def schema_linked_service(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowSourceSchemaLinkedService"]:
        '''schema_linked_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#schema_linked_service DataFactoryFlowletDataFlow#schema_linked_service}
        '''
        result = self._values.get("schema_linked_service")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSourceSchemaLinkedService"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSourceDataset",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters"},
)
class DataFactoryFlowletDataFlowSourceDataset:
    def __init__(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd4a6feaca5b7894e0268a2968854866a876fdc4558d2fcc221b6d482211eab5)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowSourceDataset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowSourceDatasetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSourceDatasetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16039bd1b2bfaef9252e9dbcecc13b66d9c93a422bc7f91531da79283c8a3ab1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f82f2f8c9ea71475fd8da1634bd7ccf6b569a0bca04eae3ace19437ce29d2d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e772d1a2b3441bd57755e08992e256646c98a17c7c3aea74ef17e12d596be447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowSourceDataset]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSourceDataset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowSourceDataset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce565c61d544a1e8757cf1d3a2fce9911b09d20979abb947322b6c358dcc706d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSourceFlowlet",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "dataset_parameters": "datasetParameters",
        "parameters": "parameters",
    },
)
class DataFactoryFlowletDataFlowSourceFlowlet:
    def __init__(
        self,
        *,
        name: builtins.str,
        dataset_parameters: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param dataset_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset_parameters DataFactoryFlowletDataFlow#dataset_parameters}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068095ebb39a2705742e8f6320bb0a53bd0f0eef7386d1c79051224c34f12422)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dataset_parameters", value=dataset_parameters, expected_type=type_hints["dataset_parameters"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if dataset_parameters is not None:
            self._values["dataset_parameters"] = dataset_parameters
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset_parameters DataFactoryFlowletDataFlow#dataset_parameters}.'''
        result = self._values.get("dataset_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowSourceFlowlet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowSourceFlowletOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSourceFlowletOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__921b7330991980389adff65fe5ea0fb6bdb6750930297ee2f29c640a947ca957)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatasetParameters")
    def reset_dataset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetParameters", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="datasetParametersInput")
    def dataset_parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetParameters")
    def dataset_parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetParameters"))

    @dataset_parameters.setter
    def dataset_parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458468486c561dd2215672ce8c374c1a35a823da3267e67479cfee719485d736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a0c3c621c6226bc32c82e5f33c834f08f7b3cb9f7a05cb1f26f8d4b6c0aadd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ed8137bdb69ce1a124888f68b2998f18fbdc74e3741d3006958de39d6f8b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowSourceFlowlet]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSourceFlowlet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowSourceFlowlet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3214c9f120ac52d5f9888dedd62b52f8a94c6fc73e3d852469d459e9a01b1a0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSourceLinkedService",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters"},
)
class DataFactoryFlowletDataFlowSourceLinkedService:
    def __init__(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5071541bbe88bb0a60caf25a2886136fbcd87de4eb2c96974f62f75a4af63f0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowSourceLinkedService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowSourceLinkedServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSourceLinkedServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__063c66b6e722f81e2d974be75cdc69d90d5d870cf2a470bca4ac66abfff34aca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f153078db66ba75cef6f05882bc3dde3bc60500025871e75e7a0047a6d37e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a6d29d95da16630dacdde8c6943efc7714410ad25735568395267784ed2e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowSourceLinkedService]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSourceLinkedService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowSourceLinkedService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c26de23caa92cc2e403d740efbe07d3fd77cfbeade90e6894119388b6b0507e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryFlowletDataFlowSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81cca39748163098acdc6bfbb91da2487dae8a5d0ccc876fb8ad912c184f5ad8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataFactoryFlowletDataFlowSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f10350d0e85ced19871a266e42276ce22d75578eff10ee4e843768d9d13bba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataFactoryFlowletDataFlowSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825e3c53958dfb60580ba0dd2c1160d112cb15f57049fb3426f2eeeae02faba8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2b90a4bc44478833575dcb34478a263a23a4c3639ba37330c54adff2fe87abf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5da6eb763e795848e950337d497c36f018607bc413eeeb6fdc9c903be7d0c88e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryFlowletDataFlowSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryFlowletDataFlowSource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryFlowletDataFlowSource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572d90e2eff34535550c54229b57752864821a88876f07f9de2cbc947f4cecb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryFlowletDataFlowSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a69a3e8df025e2fe088cab8254a123ff7d9f0f92e237a36727d8ca965f1eeb63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDataset")
    def put_dataset(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowSourceDataset(
            name=name, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putDataset", [value]))

    @jsii.member(jsii_name="putFlowlet")
    def put_flowlet(
        self,
        *,
        name: builtins.str,
        dataset_parameters: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param dataset_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset_parameters DataFactoryFlowletDataFlow#dataset_parameters}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowSourceFlowlet(
            name=name, dataset_parameters=dataset_parameters, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putFlowlet", [value]))

    @jsii.member(jsii_name="putLinkedService")
    def put_linked_service(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowSourceLinkedService(
            name=name, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putLinkedService", [value]))

    @jsii.member(jsii_name="putRejectedLinkedService")
    def put_rejected_linked_service(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowSourceRejectedLinkedService(
            name=name, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putRejectedLinkedService", [value]))

    @jsii.member(jsii_name="putSchemaLinkedService")
    def put_schema_linked_service(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowSourceSchemaLinkedService(
            name=name, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaLinkedService", [value]))

    @jsii.member(jsii_name="resetDataset")
    def reset_dataset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataset", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFlowlet")
    def reset_flowlet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlowlet", []))

    @jsii.member(jsii_name="resetLinkedService")
    def reset_linked_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedService", []))

    @jsii.member(jsii_name="resetRejectedLinkedService")
    def reset_rejected_linked_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRejectedLinkedService", []))

    @jsii.member(jsii_name="resetSchemaLinkedService")
    def reset_schema_linked_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaLinkedService", []))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> DataFactoryFlowletDataFlowSourceDatasetOutputReference:
        return typing.cast(DataFactoryFlowletDataFlowSourceDatasetOutputReference, jsii.get(self, "dataset"))

    @builtins.property
    @jsii.member(jsii_name="flowlet")
    def flowlet(self) -> DataFactoryFlowletDataFlowSourceFlowletOutputReference:
        return typing.cast(DataFactoryFlowletDataFlowSourceFlowletOutputReference, jsii.get(self, "flowlet"))

    @builtins.property
    @jsii.member(jsii_name="linkedService")
    def linked_service(
        self,
    ) -> DataFactoryFlowletDataFlowSourceLinkedServiceOutputReference:
        return typing.cast(DataFactoryFlowletDataFlowSourceLinkedServiceOutputReference, jsii.get(self, "linkedService"))

    @builtins.property
    @jsii.member(jsii_name="rejectedLinkedService")
    def rejected_linked_service(
        self,
    ) -> "DataFactoryFlowletDataFlowSourceRejectedLinkedServiceOutputReference":
        return typing.cast("DataFactoryFlowletDataFlowSourceRejectedLinkedServiceOutputReference", jsii.get(self, "rejectedLinkedService"))

    @builtins.property
    @jsii.member(jsii_name="schemaLinkedService")
    def schema_linked_service(
        self,
    ) -> "DataFactoryFlowletDataFlowSourceSchemaLinkedServiceOutputReference":
        return typing.cast("DataFactoryFlowletDataFlowSourceSchemaLinkedServiceOutputReference", jsii.get(self, "schemaLinkedService"))

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional[DataFactoryFlowletDataFlowSourceDataset]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSourceDataset], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="flowletInput")
    def flowlet_input(self) -> typing.Optional[DataFactoryFlowletDataFlowSourceFlowlet]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSourceFlowlet], jsii.get(self, "flowletInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedServiceInput")
    def linked_service_input(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowSourceLinkedService]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSourceLinkedService], jsii.get(self, "linkedServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="rejectedLinkedServiceInput")
    def rejected_linked_service_input(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowSourceRejectedLinkedService"]:
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSourceRejectedLinkedService"], jsii.get(self, "rejectedLinkedServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaLinkedServiceInput")
    def schema_linked_service_input(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowSourceSchemaLinkedService"]:
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowSourceSchemaLinkedService"], jsii.get(self, "schemaLinkedServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aab095dee56043b00558fdf967e4d4343a69cf4b13bfbad09ee6a4c40cf781ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a32f6b9673f4abf5c15d1b768663686c36027067e6c0fee95ff7fb3e207dccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowSource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowSource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowSource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4639a7c9ea61ca6adcfadd37be9ce23feaf7b54b3322b8d700f87998e392dee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSourceRejectedLinkedService",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters"},
)
class DataFactoryFlowletDataFlowSourceRejectedLinkedService:
    def __init__(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a86a6c370ffd9c81f0fce81f2b669eec3031f725d250655fee1f0b230c9c036)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowSourceRejectedLinkedService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowSourceRejectedLinkedServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSourceRejectedLinkedServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__178d7bbb0130a599b9d008d0db8ec32d415f3e16750417dba3e47a4da7fd744a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d97a7611df39358d6d3733cdaff0490ef9607003112ce9887dafa4e0b245f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b717c638a1ab53a298b19e78bddb25ec2705a52851adb8ddae47860f3f1b89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowSourceRejectedLinkedService]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSourceRejectedLinkedService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowSourceRejectedLinkedService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975670c915e56a295b4ffdd776702edef43aa39579dcbc28bcf9ab7c2eabeafd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSourceSchemaLinkedService",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters"},
)
class DataFactoryFlowletDataFlowSourceSchemaLinkedService:
    def __init__(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762a6256eefb515f7665f236fe9d336c2d67e1fa78fc6e61f9e8e2d22f94ffec)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowSourceSchemaLinkedService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowSourceSchemaLinkedServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowSourceSchemaLinkedServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e51e748861c2e07443d5fa1773d31085e93b664428f931c5e52d316f4db73aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b6312e61744a39ac565444a4ad18e27189d8d1ae03f3feef7bc9f0cfc529e6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186a55c8de4a4e6686909abd96b2b66f8b27d6452b339280c4c10b01b5543eb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowSourceSchemaLinkedService]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowSourceSchemaLinkedService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowSourceSchemaLinkedService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77b1717b75568fc4478e258593de366e8a8e2a8068aaaa6d93d5b8f9cc6ace6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DataFactoryFlowletDataFlowTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#create DataFactoryFlowletDataFlow#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#delete DataFactoryFlowletDataFlow#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#read DataFactoryFlowletDataFlow#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#update DataFactoryFlowletDataFlow#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70999c6d097e6e893dc8c2c0721bd6e04ef2f3475ddc5691ce6cd84c2fc87ed6)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#create DataFactoryFlowletDataFlow#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#delete DataFactoryFlowletDataFlow#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#read DataFactoryFlowletDataFlow#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#update DataFactoryFlowletDataFlow#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a197e37bf524dc907362e1baa0dc64cdd8f36cfa9d198de046eb7cb31f9dd6ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0beeb5d923a7efde3ee866c74b3895265f11b92043b838f1cb4e8a65042a87ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f884bf508d4244a2abaf2ea1c1e9b5651c55ac6d0e789c84494fe2eac9d615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86fc133503619adaa6d559f5e5236e2990f3285d3de6677c1746c80f29d114f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4ec81e9708f75b0e78e79deb033bb68e55e27b71705e36188827056120470d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e77c819acd094acbc62158c1e6cf0bc33520376002dc39cf72117dc3a828e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowTransformation",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "dataset": "dataset",
        "description": "description",
        "flowlet": "flowlet",
        "linked_service": "linkedService",
    },
)
class DataFactoryFlowletDataFlowTransformation:
    def __init__(
        self,
        *,
        name: builtins.str,
        dataset: typing.Optional[typing.Union["DataFactoryFlowletDataFlowTransformationDataset", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        flowlet: typing.Optional[typing.Union["DataFactoryFlowletDataFlowTransformationFlowlet", typing.Dict[builtins.str, typing.Any]]] = None,
        linked_service: typing.Optional[typing.Union["DataFactoryFlowletDataFlowTransformationLinkedService", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param dataset: dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset DataFactoryFlowletDataFlow#dataset}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#description DataFactoryFlowletDataFlow#description}.
        :param flowlet: flowlet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#flowlet DataFactoryFlowletDataFlow#flowlet}
        :param linked_service: linked_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#linked_service DataFactoryFlowletDataFlow#linked_service}
        '''
        if isinstance(dataset, dict):
            dataset = DataFactoryFlowletDataFlowTransformationDataset(**dataset)
        if isinstance(flowlet, dict):
            flowlet = DataFactoryFlowletDataFlowTransformationFlowlet(**flowlet)
        if isinstance(linked_service, dict):
            linked_service = DataFactoryFlowletDataFlowTransformationLinkedService(**linked_service)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1602fc746849a14d4b7b79f6552ddd9a8c6243649d2a63a76e17ff66f2c38812)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument flowlet", value=flowlet, expected_type=type_hints["flowlet"])
            check_type(argname="argument linked_service", value=linked_service, expected_type=type_hints["linked_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if dataset is not None:
            self._values["dataset"] = dataset
        if description is not None:
            self._values["description"] = description
        if flowlet is not None:
            self._values["flowlet"] = flowlet
        if linked_service is not None:
            self._values["linked_service"] = linked_service

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowTransformationDataset"]:
        '''dataset block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset DataFactoryFlowletDataFlow#dataset}
        '''
        result = self._values.get("dataset")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowTransformationDataset"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#description DataFactoryFlowletDataFlow#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flowlet(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowTransformationFlowlet"]:
        '''flowlet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#flowlet DataFactoryFlowletDataFlow#flowlet}
        '''
        result = self._values.get("flowlet")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowTransformationFlowlet"], result)

    @builtins.property
    def linked_service(
        self,
    ) -> typing.Optional["DataFactoryFlowletDataFlowTransformationLinkedService"]:
        '''linked_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#linked_service DataFactoryFlowletDataFlow#linked_service}
        '''
        result = self._values.get("linked_service")
        return typing.cast(typing.Optional["DataFactoryFlowletDataFlowTransformationLinkedService"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowTransformation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowTransformationDataset",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters"},
)
class DataFactoryFlowletDataFlowTransformationDataset:
    def __init__(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54fe491468fd0d5afc794f390024760a4c6f077e0bcb49248a4289bfdcbea61a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowTransformationDataset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowTransformationDatasetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowTransformationDatasetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b4f727884f4997257e1132d93bc5aafbfef2b26e8fdf7ecdd7f596840809010)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755aa400756120ae0b2385d94cab95fe39485b99cfe379ab821a9af5fe8e93db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75e6b43124bfde288f783d382afebd40356cf78b583a17c6b595109b33de6f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowTransformationDataset]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowTransformationDataset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowTransformationDataset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54df76a188e6d55e69c8862f1fef7b7b6ac6f58aec9db3578cf17ced147d23ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowTransformationFlowlet",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "dataset_parameters": "datasetParameters",
        "parameters": "parameters",
    },
)
class DataFactoryFlowletDataFlowTransformationFlowlet:
    def __init__(
        self,
        *,
        name: builtins.str,
        dataset_parameters: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param dataset_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset_parameters DataFactoryFlowletDataFlow#dataset_parameters}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f856052ef34942ac1ed9f2bd3c53bcf60972f5cede99a38cc876335fe4939159)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dataset_parameters", value=dataset_parameters, expected_type=type_hints["dataset_parameters"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if dataset_parameters is not None:
            self._values["dataset_parameters"] = dataset_parameters
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_parameters(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset_parameters DataFactoryFlowletDataFlow#dataset_parameters}.'''
        result = self._values.get("dataset_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowTransformationFlowlet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowTransformationFlowletOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowTransformationFlowletOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a524dc92ac01f49b9dee8653ad4fa072a70d597176204f5a631d81b731dff48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatasetParameters")
    def reset_dataset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetParameters", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="datasetParametersInput")
    def dataset_parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetParameters")
    def dataset_parameters(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetParameters"))

    @dataset_parameters.setter
    def dataset_parameters(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b918037d1f2ddc61efcb5acb4d76eb434ccd09383193198016b47cbb5aebf0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7416ff1e78765ae96950edf4e3ae9f3e1223e6f52d3f5f4839506f08beed934c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095ca66716c05284df456589d7d4b9101c1afd793db03d5ccf619399691d07a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowTransformationFlowlet]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowTransformationFlowlet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowTransformationFlowlet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21797e5e0a8b416ce773ad6bb7c46a1763baab9a108377f796dd2beabbb13195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowTransformationLinkedService",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters"},
)
class DataFactoryFlowletDataFlowTransformationLinkedService:
    def __init__(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf8f68f6038fe19a1de4ae737fb893a10b179c42274ef1022ecd20ed20af096)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryFlowletDataFlowTransformationLinkedService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryFlowletDataFlowTransformationLinkedServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowTransformationLinkedServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5868af091a291f0067e4e754abb2ee8c5883c2f87e1590f3872973002543bb40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90a1970e1ae37e029199fd92bf3c865ce06d7a63918c26c1c2ce6ce43d95304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9df975af7cc30d2c29735efca1e7913242d1b658e20a9e5c210d58c18f8f47b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowTransformationLinkedService]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowTransformationLinkedService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryFlowletDataFlowTransformationLinkedService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5caf8f0cf4322c81162d3b470754a734e8e9803adb32affa20d857a0e7cb7d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryFlowletDataFlowTransformationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowTransformationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d75b8ed4dd74bf6a59868d4dd7ba8d41924911c8a32a819ca7ed77369b269c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataFactoryFlowletDataFlowTransformationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f7bc995799797ace7de638199e4df2d5ed644eeeeac108cac9586ec74c9db6b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataFactoryFlowletDataFlowTransformationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae96325b6946ed1388e21beb4d27cf7843b758ede4d31d082bdd25f9e76a656)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbcd0535177628605cf582df7986e0c995a78161d02593bfe834808bdc716a33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15988e4bef2afff4c753b655d658f696ed0cc1f7b41daef9f77746fe21f74b92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryFlowletDataFlowTransformation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryFlowletDataFlowTransformation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryFlowletDataFlowTransformation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5091e09ad85e2e22a482384a2ed76df80d08d7f69a660840e1c17528b46b1819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataFactoryFlowletDataFlowTransformationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryFlowletDataFlow.DataFactoryFlowletDataFlowTransformationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ebd12b2eb682aec902755a392df892dbd07ac9af99d00b955a95b964948cb1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDataset")
    def put_dataset(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowTransformationDataset(
            name=name, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putDataset", [value]))

    @jsii.member(jsii_name="putFlowlet")
    def put_flowlet(
        self,
        *,
        name: builtins.str,
        dataset_parameters: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param dataset_parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#dataset_parameters DataFactoryFlowletDataFlow#dataset_parameters}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowTransformationFlowlet(
            name=name, dataset_parameters=dataset_parameters, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putFlowlet", [value]))

    @jsii.member(jsii_name="putLinkedService")
    def put_linked_service(
        self,
        *,
        name: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#name DataFactoryFlowletDataFlow#name}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_flowlet_data_flow#parameters DataFactoryFlowletDataFlow#parameters}.
        '''
        value = DataFactoryFlowletDataFlowTransformationLinkedService(
            name=name, parameters=parameters
        )

        return typing.cast(None, jsii.invoke(self, "putLinkedService", [value]))

    @jsii.member(jsii_name="resetDataset")
    def reset_dataset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataset", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFlowlet")
    def reset_flowlet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFlowlet", []))

    @jsii.member(jsii_name="resetLinkedService")
    def reset_linked_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedService", []))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> DataFactoryFlowletDataFlowTransformationDatasetOutputReference:
        return typing.cast(DataFactoryFlowletDataFlowTransformationDatasetOutputReference, jsii.get(self, "dataset"))

    @builtins.property
    @jsii.member(jsii_name="flowlet")
    def flowlet(self) -> DataFactoryFlowletDataFlowTransformationFlowletOutputReference:
        return typing.cast(DataFactoryFlowletDataFlowTransformationFlowletOutputReference, jsii.get(self, "flowlet"))

    @builtins.property
    @jsii.member(jsii_name="linkedService")
    def linked_service(
        self,
    ) -> DataFactoryFlowletDataFlowTransformationLinkedServiceOutputReference:
        return typing.cast(DataFactoryFlowletDataFlowTransformationLinkedServiceOutputReference, jsii.get(self, "linkedService"))

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowTransformationDataset]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowTransformationDataset], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="flowletInput")
    def flowlet_input(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowTransformationFlowlet]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowTransformationFlowlet], jsii.get(self, "flowletInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedServiceInput")
    def linked_service_input(
        self,
    ) -> typing.Optional[DataFactoryFlowletDataFlowTransformationLinkedService]:
        return typing.cast(typing.Optional[DataFactoryFlowletDataFlowTransformationLinkedService], jsii.get(self, "linkedServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce917401a8c4277a2505232303c9986e2c7e63cb9f678b80fbe23af8ecc3c21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58505a42430049f4ef518403d7cebdfbb8c42daa86cccc14907069e94dbf97d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowTransformation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowTransformation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowTransformation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca2bf8ad3c3a73e03376044683a9dc45b8cc962eb735d694a0b622fb7a36ae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataFactoryFlowletDataFlow",
    "DataFactoryFlowletDataFlowConfig",
    "DataFactoryFlowletDataFlowSink",
    "DataFactoryFlowletDataFlowSinkDataset",
    "DataFactoryFlowletDataFlowSinkDatasetOutputReference",
    "DataFactoryFlowletDataFlowSinkFlowlet",
    "DataFactoryFlowletDataFlowSinkFlowletOutputReference",
    "DataFactoryFlowletDataFlowSinkLinkedService",
    "DataFactoryFlowletDataFlowSinkLinkedServiceOutputReference",
    "DataFactoryFlowletDataFlowSinkList",
    "DataFactoryFlowletDataFlowSinkOutputReference",
    "DataFactoryFlowletDataFlowSinkRejectedLinkedService",
    "DataFactoryFlowletDataFlowSinkRejectedLinkedServiceOutputReference",
    "DataFactoryFlowletDataFlowSinkSchemaLinkedService",
    "DataFactoryFlowletDataFlowSinkSchemaLinkedServiceOutputReference",
    "DataFactoryFlowletDataFlowSource",
    "DataFactoryFlowletDataFlowSourceDataset",
    "DataFactoryFlowletDataFlowSourceDatasetOutputReference",
    "DataFactoryFlowletDataFlowSourceFlowlet",
    "DataFactoryFlowletDataFlowSourceFlowletOutputReference",
    "DataFactoryFlowletDataFlowSourceLinkedService",
    "DataFactoryFlowletDataFlowSourceLinkedServiceOutputReference",
    "DataFactoryFlowletDataFlowSourceList",
    "DataFactoryFlowletDataFlowSourceOutputReference",
    "DataFactoryFlowletDataFlowSourceRejectedLinkedService",
    "DataFactoryFlowletDataFlowSourceRejectedLinkedServiceOutputReference",
    "DataFactoryFlowletDataFlowSourceSchemaLinkedService",
    "DataFactoryFlowletDataFlowSourceSchemaLinkedServiceOutputReference",
    "DataFactoryFlowletDataFlowTimeouts",
    "DataFactoryFlowletDataFlowTimeoutsOutputReference",
    "DataFactoryFlowletDataFlowTransformation",
    "DataFactoryFlowletDataFlowTransformationDataset",
    "DataFactoryFlowletDataFlowTransformationDatasetOutputReference",
    "DataFactoryFlowletDataFlowTransformationFlowlet",
    "DataFactoryFlowletDataFlowTransformationFlowletOutputReference",
    "DataFactoryFlowletDataFlowTransformationLinkedService",
    "DataFactoryFlowletDataFlowTransformationLinkedServiceOutputReference",
    "DataFactoryFlowletDataFlowTransformationList",
    "DataFactoryFlowletDataFlowTransformationOutputReference",
]

publication.publish()

def _typecheckingstub__58d72bdbfbb75606cd3efe64dc18da8e2b2cdea19c0d18ed7e177dc86478c6fc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_factory_id: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    folder: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
    script_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
    sink: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryFlowletDataFlowSink, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryFlowletDataFlowSource, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryFlowletDataFlowTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transformation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryFlowletDataFlowTransformation, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__30f4f0ae116e1fbf4f32ee897d3145ba51c85be2a94c59174cedc3f3ce57a563(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d3208efe972ae4202c001c9c482ef42a2160cfb943516a4c12135cb6a324f6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryFlowletDataFlowSink, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb23bd95d0252d6280d0d60094db245046662c514aebced0a6c2b998dd524f20(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryFlowletDataFlowSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ea9e12603a31750ede9779ec0f97d50e6e27f8f086786f8191bfcadabfd476(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryFlowletDataFlowTransformation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__768a944bb414a0fc8c95800e95fc1416c206aeab5549d62e77778a98b782b460(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b192326516e5fe422a2dbb64ae73a38330970493ffee31297c81ebd98dd87d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956e12ab44b9539a69a9a10e57f3d68151bdff9f9a02ce3b8eeab8e7307cc02d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04289a93b7a05ba276ce3ded5c65af1529863bd6e79b97573bdc3c7dc244bb0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f987c430edb7815c4e19f45d2ecda409a56a3c04fc02537e92d37b70d2291f62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b57edb42d2db5af73d411a58da096726f4a09d18be8575206d52a206538ecbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d92e057157991f33e8dbfc7519a1631794646717d0e6a66d1b533b0e1aebd87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313e91a9d41cf33b39b2f74825aca2c9544fc3cf49e0ad913f292d6f947bd243(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2a6b3e92e1364c65c39217aaf055cb2363ce8499648b73fa21f883a6b6492c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_factory_id: builtins.str,
    name: builtins.str,
    annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    folder: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
    script_lines: typing.Optional[typing.Sequence[builtins.str]] = None,
    sink: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryFlowletDataFlowSink, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryFlowletDataFlowSource, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryFlowletDataFlowTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transformation: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataFactoryFlowletDataFlowTransformation, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75bad8be205ec8d501358a58070dbc70014b6509275e3b0723c71b1239c0a38(
    *,
    name: builtins.str,
    dataset: typing.Optional[typing.Union[DataFactoryFlowletDataFlowSinkDataset, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    flowlet: typing.Optional[typing.Union[DataFactoryFlowletDataFlowSinkFlowlet, typing.Dict[builtins.str, typing.Any]]] = None,
    linked_service: typing.Optional[typing.Union[DataFactoryFlowletDataFlowSinkLinkedService, typing.Dict[builtins.str, typing.Any]]] = None,
    rejected_linked_service: typing.Optional[typing.Union[DataFactoryFlowletDataFlowSinkRejectedLinkedService, typing.Dict[builtins.str, typing.Any]]] = None,
    schema_linked_service: typing.Optional[typing.Union[DataFactoryFlowletDataFlowSinkSchemaLinkedService, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d0a98caf28529d0a690cbe37bd10c65c896436226952617b1fa4ed08b5dae1(
    *,
    name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba25b9aa57c5e559ffcfb79cf802eccd9b9b6f77c6bc5593da5a2a24eaa9d3a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51529b371918ebf8798f02e14b46555c16323beee8f73672f648d8067ea06908(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712ecb357692e7c0ab92db826357df38e704fae79702d3842c90e7346b6f9ca9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a0c142a196f9f3e242a47229ddd99547ca4e3b11084ec0656d0c36f54b7ea4(
    value: typing.Optional[DataFactoryFlowletDataFlowSinkDataset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2589d3dad67df502c2f93e0793073f3e2f2eb1a6fc212b114f4048e4860fc51(
    *,
    name: builtins.str,
    dataset_parameters: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180f150a00560296de6d14ca6cd8a67317e4e9efc62f2c82a1dc16898dee3bfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8666fe5fc9c390539dd219b2d04364ff2f1a5312ea717a6b9a9967698f709cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625b047a35ff7219da0fde4a5e534e94d81d8ea5a3ee352b24957ac305a78928(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73262d81fdcbe854d682a636a2729a73adad96284e127741ee6cbb6ff1758526(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61451e6636566250727ff074ac8b796410f2e2696f0cfeec93b5dd59078d3e6(
    value: typing.Optional[DataFactoryFlowletDataFlowSinkFlowlet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4faba067de4bd5546862cc2e7fac9a94515c166a068370d2ba1aeb7014f02dc(
    *,
    name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae326bbfa7e2663bafcc12e45e6109b18f004361dca16928ce94f01060aa37af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5821051c6a36f682b334bbf53e2b70dbdc15f34c9520c89a02e5a856a607bb1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__896cae44c564c58f12f4aff23b017069a7f91ff67323683cd8d3ea5c5ab87c98(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f39646ee3d7f4de9f140efb5c4dcc30af0c99c8576905199d10cd0472e59b6(
    value: typing.Optional[DataFactoryFlowletDataFlowSinkLinkedService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6c56491f285a4c1fdf950bedb293d7163e4322a682e755a51381e997892c17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace3de93043e281b02df75b82895a266d12409239eea9d5e65f68fee2168d1f2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940836e9dfac79980c3d37cb828b18de98848793de3c59d6ec8b7b16d6a27e3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5a48d32ea9099b2478afac3aa2626eba8bdeb8255dc9064f1085ef019f5875(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4107c1011ae46b71ac86fb45062bba976d60f542e5363a3354ee2e60fb79be7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4e4ff4f3415d0cfc8ed9aecb41823b36b0d37abc50bc5ea3189dacb87f7535(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryFlowletDataFlowSink]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fe490fbf77bf50b537c25d5789d4cf9291d978ce38cf122bc88405aa3d3bee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682e0d062712a22c392bd48493a987b20c408d2d3092375aa4089005126e42f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d56f791a94f8f8d3bb005627c0d389c29b549707e97072c20e4f1080129773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877b247a2d605ca95c1fc6aa52eaa93b4d988a8fb2a79554f09f5e746f9f2815(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowSink]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9131372e2f502e32ac34ac890f28e85113a927bb2d04a1be336fef0d78a3167(
    *,
    name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17802501c9915fcbef6ce46d0b55758aa4993e893f195c43a6d2f617d78215e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528d05bb4b14902d8042fc6bdb738d6f50dcd3eabf6f70641ba5b8345aa59dc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3449630512131e2fef155e7cdce3973e4775a4797c1079076f60090b0d96ada(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ba3cdae1440a49ca38cf32d6a6cb008edfb3f2e987e9ab409735297b76d3a3(
    value: typing.Optional[DataFactoryFlowletDataFlowSinkRejectedLinkedService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5790bf7110a8d031f6624859e03ba4d0f2f4a7625b357b170b8431839661a9(
    *,
    name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5836c3bc5844c3e4c44d7c29182129fb1378a039e9b783a848b290ffb3c31b14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b073ed8bd8113cd4c3019d6b231b7e140bed7488db3c5a09e95eba1bc8d7d58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3460f37b023edf81d95842681917779db476553d70a9c3a56f70e3fc894fb3ed(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9c513d5d7d36f5693589581b08e2d6ac533094082070bdb5477b32ebde70c9(
    value: typing.Optional[DataFactoryFlowletDataFlowSinkSchemaLinkedService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97ff011f6a6b6a4d811367f7c917ae375dcb7725df7e960ce6b2853afb80f4e(
    *,
    name: builtins.str,
    dataset: typing.Optional[typing.Union[DataFactoryFlowletDataFlowSourceDataset, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    flowlet: typing.Optional[typing.Union[DataFactoryFlowletDataFlowSourceFlowlet, typing.Dict[builtins.str, typing.Any]]] = None,
    linked_service: typing.Optional[typing.Union[DataFactoryFlowletDataFlowSourceLinkedService, typing.Dict[builtins.str, typing.Any]]] = None,
    rejected_linked_service: typing.Optional[typing.Union[DataFactoryFlowletDataFlowSourceRejectedLinkedService, typing.Dict[builtins.str, typing.Any]]] = None,
    schema_linked_service: typing.Optional[typing.Union[DataFactoryFlowletDataFlowSourceSchemaLinkedService, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4a6feaca5b7894e0268a2968854866a876fdc4558d2fcc221b6d482211eab5(
    *,
    name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16039bd1b2bfaef9252e9dbcecc13b66d9c93a422bc7f91531da79283c8a3ab1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f82f2f8c9ea71475fd8da1634bd7ccf6b569a0bca04eae3ace19437ce29d2d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e772d1a2b3441bd57755e08992e256646c98a17c7c3aea74ef17e12d596be447(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce565c61d544a1e8757cf1d3a2fce9911b09d20979abb947322b6c358dcc706d(
    value: typing.Optional[DataFactoryFlowletDataFlowSourceDataset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068095ebb39a2705742e8f6320bb0a53bd0f0eef7386d1c79051224c34f12422(
    *,
    name: builtins.str,
    dataset_parameters: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921b7330991980389adff65fe5ea0fb6bdb6750930297ee2f29c640a947ca957(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458468486c561dd2215672ce8c374c1a35a823da3267e67479cfee719485d736(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a0c3c621c6226bc32c82e5f33c834f08f7b3cb9f7a05cb1f26f8d4b6c0aadd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ed8137bdb69ce1a124888f68b2998f18fbdc74e3741d3006958de39d6f8b64(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3214c9f120ac52d5f9888dedd62b52f8a94c6fc73e3d852469d459e9a01b1a0c(
    value: typing.Optional[DataFactoryFlowletDataFlowSourceFlowlet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5071541bbe88bb0a60caf25a2886136fbcd87de4eb2c96974f62f75a4af63f0(
    *,
    name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063c66b6e722f81e2d974be75cdc69d90d5d870cf2a470bca4ac66abfff34aca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f153078db66ba75cef6f05882bc3dde3bc60500025871e75e7a0047a6d37e77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a6d29d95da16630dacdde8c6943efc7714410ad25735568395267784ed2e28(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26de23caa92cc2e403d740efbe07d3fd77cfbeade90e6894119388b6b0507e7(
    value: typing.Optional[DataFactoryFlowletDataFlowSourceLinkedService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81cca39748163098acdc6bfbb91da2487dae8a5d0ccc876fb8ad912c184f5ad8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f10350d0e85ced19871a266e42276ce22d75578eff10ee4e843768d9d13bba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825e3c53958dfb60580ba0dd2c1160d112cb15f57049fb3426f2eeeae02faba8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b90a4bc44478833575dcb34478a263a23a4c3639ba37330c54adff2fe87abf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da6eb763e795848e950337d497c36f018607bc413eeeb6fdc9c903be7d0c88e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572d90e2eff34535550c54229b57752864821a88876f07f9de2cbc947f4cecb3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryFlowletDataFlowSource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69a3e8df025e2fe088cab8254a123ff7d9f0f92e237a36727d8ca965f1eeb63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab095dee56043b00558fdf967e4d4343a69cf4b13bfbad09ee6a4c40cf781ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a32f6b9673f4abf5c15d1b768663686c36027067e6c0fee95ff7fb3e207dccb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4639a7c9ea61ca6adcfadd37be9ce23feaf7b54b3322b8d700f87998e392dee6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowSource]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a86a6c370ffd9c81f0fce81f2b669eec3031f725d250655fee1f0b230c9c036(
    *,
    name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178d7bbb0130a599b9d008d0db8ec32d415f3e16750417dba3e47a4da7fd744a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d97a7611df39358d6d3733cdaff0490ef9607003112ce9887dafa4e0b245f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b717c638a1ab53a298b19e78bddb25ec2705a52851adb8ddae47860f3f1b89(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975670c915e56a295b4ffdd776702edef43aa39579dcbc28bcf9ab7c2eabeafd(
    value: typing.Optional[DataFactoryFlowletDataFlowSourceRejectedLinkedService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762a6256eefb515f7665f236fe9d336c2d67e1fa78fc6e61f9e8e2d22f94ffec(
    *,
    name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e51e748861c2e07443d5fa1773d31085e93b664428f931c5e52d316f4db73aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6312e61744a39ac565444a4ad18e27189d8d1ae03f3feef7bc9f0cfc529e6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186a55c8de4a4e6686909abd96b2b66f8b27d6452b339280c4c10b01b5543eb3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77b1717b75568fc4478e258593de366e8a8e2a8068aaaa6d93d5b8f9cc6ace6(
    value: typing.Optional[DataFactoryFlowletDataFlowSourceSchemaLinkedService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70999c6d097e6e893dc8c2c0721bd6e04ef2f3475ddc5691ce6cd84c2fc87ed6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a197e37bf524dc907362e1baa0dc64cdd8f36cfa9d198de046eb7cb31f9dd6ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0beeb5d923a7efde3ee866c74b3895265f11b92043b838f1cb4e8a65042a87ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f884bf508d4244a2abaf2ea1c1e9b5651c55ac6d0e789c84494fe2eac9d615(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86fc133503619adaa6d559f5e5236e2990f3285d3de6677c1746c80f29d114f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4ec81e9708f75b0e78e79deb033bb68e55e27b71705e36188827056120470d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e77c819acd094acbc62158c1e6cf0bc33520376002dc39cf72117dc3a828e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1602fc746849a14d4b7b79f6552ddd9a8c6243649d2a63a76e17ff66f2c38812(
    *,
    name: builtins.str,
    dataset: typing.Optional[typing.Union[DataFactoryFlowletDataFlowTransformationDataset, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    flowlet: typing.Optional[typing.Union[DataFactoryFlowletDataFlowTransformationFlowlet, typing.Dict[builtins.str, typing.Any]]] = None,
    linked_service: typing.Optional[typing.Union[DataFactoryFlowletDataFlowTransformationLinkedService, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fe491468fd0d5afc794f390024760a4c6f077e0bcb49248a4289bfdcbea61a(
    *,
    name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4f727884f4997257e1132d93bc5aafbfef2b26e8fdf7ecdd7f596840809010(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755aa400756120ae0b2385d94cab95fe39485b99cfe379ab821a9af5fe8e93db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75e6b43124bfde288f783d382afebd40356cf78b583a17c6b595109b33de6f5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54df76a188e6d55e69c8862f1fef7b7b6ac6f58aec9db3578cf17ced147d23ef(
    value: typing.Optional[DataFactoryFlowletDataFlowTransformationDataset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f856052ef34942ac1ed9f2bd3c53bcf60972f5cede99a38cc876335fe4939159(
    *,
    name: builtins.str,
    dataset_parameters: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a524dc92ac01f49b9dee8653ad4fa072a70d597176204f5a631d81b731dff48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b918037d1f2ddc61efcb5acb4d76eb434ccd09383193198016b47cbb5aebf0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7416ff1e78765ae96950edf4e3ae9f3e1223e6f52d3f5f4839506f08beed934c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095ca66716c05284df456589d7d4b9101c1afd793db03d5ccf619399691d07a2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21797e5e0a8b416ce773ad6bb7c46a1763baab9a108377f796dd2beabbb13195(
    value: typing.Optional[DataFactoryFlowletDataFlowTransformationFlowlet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf8f68f6038fe19a1de4ae737fb893a10b179c42274ef1022ecd20ed20af096(
    *,
    name: builtins.str,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5868af091a291f0067e4e754abb2ee8c5883c2f87e1590f3872973002543bb40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90a1970e1ae37e029199fd92bf3c865ce06d7a63918c26c1c2ce6ce43d95304(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9df975af7cc30d2c29735efca1e7913242d1b658e20a9e5c210d58c18f8f47b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5caf8f0cf4322c81162d3b470754a734e8e9803adb32affa20d857a0e7cb7d6a(
    value: typing.Optional[DataFactoryFlowletDataFlowTransformationLinkedService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d75b8ed4dd74bf6a59868d4dd7ba8d41924911c8a32a819ca7ed77369b269c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7bc995799797ace7de638199e4df2d5ed644eeeeac108cac9586ec74c9db6b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae96325b6946ed1388e21beb4d27cf7843b758ede4d31d082bdd25f9e76a656(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbcd0535177628605cf582df7986e0c995a78161d02593bfe834808bdc716a33(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15988e4bef2afff4c753b655d658f696ed0cc1f7b41daef9f77746fe21f74b92(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5091e09ad85e2e22a482384a2ed76df80d08d7f69a660840e1c17528b46b1819(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataFactoryFlowletDataFlowTransformation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ebd12b2eb682aec902755a392df892dbd07ac9af99d00b955a95b964948cb1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce917401a8c4277a2505232303c9986e2c7e63cb9f678b80fbe23af8ecc3c21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58505a42430049f4ef518403d7cebdfbb8c42daa86cccc14907069e94dbf97d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca2bf8ad3c3a73e03376044683a9dc45b8cc962eb735d694a0b622fb7a36ae3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryFlowletDataFlowTransformation]],
) -> None:
    """Type checking stubs"""
    pass
