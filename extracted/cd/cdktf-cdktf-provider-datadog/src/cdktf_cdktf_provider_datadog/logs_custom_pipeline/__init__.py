r'''
# `datadog_logs_custom_pipeline`

Refer to the Terraform Registry for docs: [`datadog_logs_custom_pipeline`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline).
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


class LogsCustomPipeline(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipeline",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline datadog_logs_custom_pipeline}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineFilter", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineProcessor", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline datadog_logs_custom_pipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#filter LogsCustomPipeline#filter}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#description LogsCustomPipeline#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#id LogsCustomPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}.
        :param processor: processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#processor LogsCustomPipeline#processor}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#tags LogsCustomPipeline#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a9b3913c726d8d372347ddf08a1fdbf32dc7eb18b77496d47880af01faa82c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LogsCustomPipelineConfig(
            filter=filter,
            name=name,
            description=description,
            id=id,
            is_enabled=is_enabled,
            processor=processor,
            tags=tags,
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
        '''Generates CDKTF code for importing a LogsCustomPipeline resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LogsCustomPipeline to import.
        :param import_from_id: The id of the existing LogsCustomPipeline that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LogsCustomPipeline to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32593a7b2dcab2495d38fed1a253cecd7c87035f223165be2ff78a1136ceadbf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9336c80022eac99c35b90d7a45c4541ac47129ab00c7a5d77384e5c27032ea06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putProcessor")
    def put_processor(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineProcessor", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e1e6851f44972f4803f496a45ff70f64ddb923a488c854bb7e3d86b2bfbd38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProcessor", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetProcessor")
    def reset_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessor", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="filter")
    def filter(self) -> "LogsCustomPipelineFilterList":
        return typing.cast("LogsCustomPipelineFilterList", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="processor")
    def processor(self) -> "LogsCustomPipelineProcessorList":
        return typing.cast("LogsCustomPipelineProcessorList", jsii.get(self, "processor"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineFilter"]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="processorInput")
    def processor_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessor"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessor"]]], jsii.get(self, "processorInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e9a1d7a47e2fd2066ff5cdad653572f2353c9ae50acc99d3b8ce6237d6f3049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a57f530464eb17cd8e83179c92e7b659ebec277a9905aacb98fe0c9d2b8e587e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c448e71b83e50629d9c26249ae6163b7f080508ce8cd9912769707ad08533fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d20b7063ddbc89e283c35bc63c020b1c2f192672850e7e58acdab258748bef34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a67f261877fcd371bd8b7940697e619ab308aa3bad8916b8c28eff35f927580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "filter": "filter",
        "name": "name",
        "description": "description",
        "id": "id",
        "is_enabled": "isEnabled",
        "processor": "processor",
        "tags": "tags",
    },
)
class LogsCustomPipelineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineFilter", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineProcessor", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#filter LogsCustomPipeline#filter}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#description LogsCustomPipeline#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#id LogsCustomPipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}.
        :param processor: processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#processor LogsCustomPipeline#processor}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#tags LogsCustomPipeline#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3428c8dc0ce3178ecfe4025b9c71eb8766b8f723688d7f1c9e1778bbc91f77)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument processor", value=processor, expected_type=type_hints["processor"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if processor is not None:
            self._values["processor"] = processor
        if tags is not None:
            self._values["tags"] = tags

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
    def filter(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineFilter"]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#filter LogsCustomPipeline#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineFilter"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#description LogsCustomPipeline#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#id LogsCustomPipeline#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}.'''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def processor(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessor"]]]:
        '''processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#processor LogsCustomPipeline#processor}
        '''
        result = self._values.get("processor")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessor"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#tags LogsCustomPipeline#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineFilter",
    jsii_struct_bases=[],
    name_mapping={"query": "query"},
)
class LogsCustomPipelineFilter:
    def __init__(self, *, query: builtins.str) -> None:
        '''
        :param query: Filter criteria of the category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#query LogsCustomPipeline#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06af79ced7a3adb91e320775d3af5ca11ddebc719825d9c7b9fd188322da3e5e)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }

    @builtins.property
    def query(self) -> builtins.str:
        '''Filter criteria of the category.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#query LogsCustomPipeline#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8f0ab753ef76fa0e8246c1b4c0a23c1d66343d1d3b5eda1d6fb2ecb10741a40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LogsCustomPipelineFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5cc44101c02727857495e2440142d46144343d11a5b8ab4d6626a8fcbfa477)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsCustomPipelineFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec8e653654db4cabeed1fb8f6c20bfd81758ef1331128e8cd8e01401b9dc5a45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e54d536ef07138950889512ee81540589a558a7aa59c63e4435dfafb76da3e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f737801a0bcecb3ca215443d68a09ab02931500b119867ad9e8ccdb63f31ec46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb4eb64e1c36bbab6d88112b585e492b8b4e46100d0a7291c2d3fc6588fd87a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__099776583831fa336db4d0a67bd960e73fe17051ebd73d1ecb7d0ae48caedbc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efb965ad11c2b8eb005841101c48ca56fc059863ef0b3ef935e5bf2c881927a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7889e3ef4f334d63752f86dc94196d6bf9e0471e3f811bee5d6804d7dcc930d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "arithmetic_processor": "arithmeticProcessor",
        "attribute_remapper": "attributeRemapper",
        "category_processor": "categoryProcessor",
        "date_remapper": "dateRemapper",
        "geo_ip_parser": "geoIpParser",
        "grok_parser": "grokParser",
        "lookup_processor": "lookupProcessor",
        "message_remapper": "messageRemapper",
        "pipeline": "pipeline",
        "reference_table_lookup_processor": "referenceTableLookupProcessor",
        "service_remapper": "serviceRemapper",
        "span_id_remapper": "spanIdRemapper",
        "status_remapper": "statusRemapper",
        "string_builder_processor": "stringBuilderProcessor",
        "trace_id_remapper": "traceIdRemapper",
        "url_parser": "urlParser",
        "user_agent_parser": "userAgentParser",
    },
)
class LogsCustomPipelineProcessor:
    def __init__(
        self,
        *,
        arithmetic_processor: typing.Optional[typing.Union["LogsCustomPipelineProcessorArithmeticProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        attribute_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorAttributeRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        category_processor: typing.Optional[typing.Union["LogsCustomPipelineProcessorCategoryProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        date_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorDateRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        geo_ip_parser: typing.Optional[typing.Union["LogsCustomPipelineProcessorGeoIpParser", typing.Dict[builtins.str, typing.Any]]] = None,
        grok_parser: typing.Optional[typing.Union["LogsCustomPipelineProcessorGrokParser", typing.Dict[builtins.str, typing.Any]]] = None,
        lookup_processor: typing.Optional[typing.Union["LogsCustomPipelineProcessorLookupProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        message_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorMessageRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        pipeline: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipeline", typing.Dict[builtins.str, typing.Any]]] = None,
        reference_table_lookup_processor: typing.Optional[typing.Union["LogsCustomPipelineProcessorReferenceTableLookupProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        service_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorServiceRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        span_id_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorSpanIdRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        status_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorStatusRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        string_builder_processor: typing.Optional[typing.Union["LogsCustomPipelineProcessorStringBuilderProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        trace_id_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorTraceIdRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        url_parser: typing.Optional[typing.Union["LogsCustomPipelineProcessorUrlParser", typing.Dict[builtins.str, typing.Any]]] = None,
        user_agent_parser: typing.Optional[typing.Union["LogsCustomPipelineProcessorUserAgentParser", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param arithmetic_processor: arithmetic_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#arithmetic_processor LogsCustomPipeline#arithmetic_processor}
        :param attribute_remapper: attribute_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#attribute_remapper LogsCustomPipeline#attribute_remapper}
        :param category_processor: category_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#category_processor LogsCustomPipeline#category_processor}
        :param date_remapper: date_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#date_remapper LogsCustomPipeline#date_remapper}
        :param geo_ip_parser: geo_ip_parser block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#geo_ip_parser LogsCustomPipeline#geo_ip_parser}
        :param grok_parser: grok_parser block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#grok_parser LogsCustomPipeline#grok_parser}
        :param lookup_processor: lookup_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_processor LogsCustomPipeline#lookup_processor}
        :param message_remapper: message_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#message_remapper LogsCustomPipeline#message_remapper}
        :param pipeline: pipeline block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#pipeline LogsCustomPipeline#pipeline}
        :param reference_table_lookup_processor: reference_table_lookup_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#reference_table_lookup_processor LogsCustomPipeline#reference_table_lookup_processor}
        :param service_remapper: service_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#service_remapper LogsCustomPipeline#service_remapper}
        :param span_id_remapper: span_id_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#span_id_remapper LogsCustomPipeline#span_id_remapper}
        :param status_remapper: status_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#status_remapper LogsCustomPipeline#status_remapper}
        :param string_builder_processor: string_builder_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#string_builder_processor LogsCustomPipeline#string_builder_processor}
        :param trace_id_remapper: trace_id_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#trace_id_remapper LogsCustomPipeline#trace_id_remapper}
        :param url_parser: url_parser block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#url_parser LogsCustomPipeline#url_parser}
        :param user_agent_parser: user_agent_parser block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#user_agent_parser LogsCustomPipeline#user_agent_parser}
        '''
        if isinstance(arithmetic_processor, dict):
            arithmetic_processor = LogsCustomPipelineProcessorArithmeticProcessor(**arithmetic_processor)
        if isinstance(attribute_remapper, dict):
            attribute_remapper = LogsCustomPipelineProcessorAttributeRemapper(**attribute_remapper)
        if isinstance(category_processor, dict):
            category_processor = LogsCustomPipelineProcessorCategoryProcessor(**category_processor)
        if isinstance(date_remapper, dict):
            date_remapper = LogsCustomPipelineProcessorDateRemapper(**date_remapper)
        if isinstance(geo_ip_parser, dict):
            geo_ip_parser = LogsCustomPipelineProcessorGeoIpParser(**geo_ip_parser)
        if isinstance(grok_parser, dict):
            grok_parser = LogsCustomPipelineProcessorGrokParser(**grok_parser)
        if isinstance(lookup_processor, dict):
            lookup_processor = LogsCustomPipelineProcessorLookupProcessor(**lookup_processor)
        if isinstance(message_remapper, dict):
            message_remapper = LogsCustomPipelineProcessorMessageRemapper(**message_remapper)
        if isinstance(pipeline, dict):
            pipeline = LogsCustomPipelineProcessorPipeline(**pipeline)
        if isinstance(reference_table_lookup_processor, dict):
            reference_table_lookup_processor = LogsCustomPipelineProcessorReferenceTableLookupProcessor(**reference_table_lookup_processor)
        if isinstance(service_remapper, dict):
            service_remapper = LogsCustomPipelineProcessorServiceRemapper(**service_remapper)
        if isinstance(span_id_remapper, dict):
            span_id_remapper = LogsCustomPipelineProcessorSpanIdRemapper(**span_id_remapper)
        if isinstance(status_remapper, dict):
            status_remapper = LogsCustomPipelineProcessorStatusRemapper(**status_remapper)
        if isinstance(string_builder_processor, dict):
            string_builder_processor = LogsCustomPipelineProcessorStringBuilderProcessor(**string_builder_processor)
        if isinstance(trace_id_remapper, dict):
            trace_id_remapper = LogsCustomPipelineProcessorTraceIdRemapper(**trace_id_remapper)
        if isinstance(url_parser, dict):
            url_parser = LogsCustomPipelineProcessorUrlParser(**url_parser)
        if isinstance(user_agent_parser, dict):
            user_agent_parser = LogsCustomPipelineProcessorUserAgentParser(**user_agent_parser)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e162331cefb51b80ece54be0131b60a9983fbadcf5793b75e3f0e393ddc41da9)
            check_type(argname="argument arithmetic_processor", value=arithmetic_processor, expected_type=type_hints["arithmetic_processor"])
            check_type(argname="argument attribute_remapper", value=attribute_remapper, expected_type=type_hints["attribute_remapper"])
            check_type(argname="argument category_processor", value=category_processor, expected_type=type_hints["category_processor"])
            check_type(argname="argument date_remapper", value=date_remapper, expected_type=type_hints["date_remapper"])
            check_type(argname="argument geo_ip_parser", value=geo_ip_parser, expected_type=type_hints["geo_ip_parser"])
            check_type(argname="argument grok_parser", value=grok_parser, expected_type=type_hints["grok_parser"])
            check_type(argname="argument lookup_processor", value=lookup_processor, expected_type=type_hints["lookup_processor"])
            check_type(argname="argument message_remapper", value=message_remapper, expected_type=type_hints["message_remapper"])
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
            check_type(argname="argument reference_table_lookup_processor", value=reference_table_lookup_processor, expected_type=type_hints["reference_table_lookup_processor"])
            check_type(argname="argument service_remapper", value=service_remapper, expected_type=type_hints["service_remapper"])
            check_type(argname="argument span_id_remapper", value=span_id_remapper, expected_type=type_hints["span_id_remapper"])
            check_type(argname="argument status_remapper", value=status_remapper, expected_type=type_hints["status_remapper"])
            check_type(argname="argument string_builder_processor", value=string_builder_processor, expected_type=type_hints["string_builder_processor"])
            check_type(argname="argument trace_id_remapper", value=trace_id_remapper, expected_type=type_hints["trace_id_remapper"])
            check_type(argname="argument url_parser", value=url_parser, expected_type=type_hints["url_parser"])
            check_type(argname="argument user_agent_parser", value=user_agent_parser, expected_type=type_hints["user_agent_parser"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arithmetic_processor is not None:
            self._values["arithmetic_processor"] = arithmetic_processor
        if attribute_remapper is not None:
            self._values["attribute_remapper"] = attribute_remapper
        if category_processor is not None:
            self._values["category_processor"] = category_processor
        if date_remapper is not None:
            self._values["date_remapper"] = date_remapper
        if geo_ip_parser is not None:
            self._values["geo_ip_parser"] = geo_ip_parser
        if grok_parser is not None:
            self._values["grok_parser"] = grok_parser
        if lookup_processor is not None:
            self._values["lookup_processor"] = lookup_processor
        if message_remapper is not None:
            self._values["message_remapper"] = message_remapper
        if pipeline is not None:
            self._values["pipeline"] = pipeline
        if reference_table_lookup_processor is not None:
            self._values["reference_table_lookup_processor"] = reference_table_lookup_processor
        if service_remapper is not None:
            self._values["service_remapper"] = service_remapper
        if span_id_remapper is not None:
            self._values["span_id_remapper"] = span_id_remapper
        if status_remapper is not None:
            self._values["status_remapper"] = status_remapper
        if string_builder_processor is not None:
            self._values["string_builder_processor"] = string_builder_processor
        if trace_id_remapper is not None:
            self._values["trace_id_remapper"] = trace_id_remapper
        if url_parser is not None:
            self._values["url_parser"] = url_parser
        if user_agent_parser is not None:
            self._values["user_agent_parser"] = user_agent_parser

    @builtins.property
    def arithmetic_processor(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorArithmeticProcessor"]:
        '''arithmetic_processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#arithmetic_processor LogsCustomPipeline#arithmetic_processor}
        '''
        result = self._values.get("arithmetic_processor")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorArithmeticProcessor"], result)

    @builtins.property
    def attribute_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorAttributeRemapper"]:
        '''attribute_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#attribute_remapper LogsCustomPipeline#attribute_remapper}
        '''
        result = self._values.get("attribute_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorAttributeRemapper"], result)

    @builtins.property
    def category_processor(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorCategoryProcessor"]:
        '''category_processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#category_processor LogsCustomPipeline#category_processor}
        '''
        result = self._values.get("category_processor")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorCategoryProcessor"], result)

    @builtins.property
    def date_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorDateRemapper"]:
        '''date_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#date_remapper LogsCustomPipeline#date_remapper}
        '''
        result = self._values.get("date_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorDateRemapper"], result)

    @builtins.property
    def geo_ip_parser(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorGeoIpParser"]:
        '''geo_ip_parser block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#geo_ip_parser LogsCustomPipeline#geo_ip_parser}
        '''
        result = self._values.get("geo_ip_parser")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorGeoIpParser"], result)

    @builtins.property
    def grok_parser(self) -> typing.Optional["LogsCustomPipelineProcessorGrokParser"]:
        '''grok_parser block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#grok_parser LogsCustomPipeline#grok_parser}
        '''
        result = self._values.get("grok_parser")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorGrokParser"], result)

    @builtins.property
    def lookup_processor(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorLookupProcessor"]:
        '''lookup_processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_processor LogsCustomPipeline#lookup_processor}
        '''
        result = self._values.get("lookup_processor")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorLookupProcessor"], result)

    @builtins.property
    def message_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorMessageRemapper"]:
        '''message_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#message_remapper LogsCustomPipeline#message_remapper}
        '''
        result = self._values.get("message_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorMessageRemapper"], result)

    @builtins.property
    def pipeline(self) -> typing.Optional["LogsCustomPipelineProcessorPipeline"]:
        '''pipeline block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#pipeline LogsCustomPipeline#pipeline}
        '''
        result = self._values.get("pipeline")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipeline"], result)

    @builtins.property
    def reference_table_lookup_processor(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorReferenceTableLookupProcessor"]:
        '''reference_table_lookup_processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#reference_table_lookup_processor LogsCustomPipeline#reference_table_lookup_processor}
        '''
        result = self._values.get("reference_table_lookup_processor")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorReferenceTableLookupProcessor"], result)

    @builtins.property
    def service_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorServiceRemapper"]:
        '''service_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#service_remapper LogsCustomPipeline#service_remapper}
        '''
        result = self._values.get("service_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorServiceRemapper"], result)

    @builtins.property
    def span_id_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorSpanIdRemapper"]:
        '''span_id_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#span_id_remapper LogsCustomPipeline#span_id_remapper}
        '''
        result = self._values.get("span_id_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorSpanIdRemapper"], result)

    @builtins.property
    def status_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorStatusRemapper"]:
        '''status_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#status_remapper LogsCustomPipeline#status_remapper}
        '''
        result = self._values.get("status_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorStatusRemapper"], result)

    @builtins.property
    def string_builder_processor(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorStringBuilderProcessor"]:
        '''string_builder_processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#string_builder_processor LogsCustomPipeline#string_builder_processor}
        '''
        result = self._values.get("string_builder_processor")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorStringBuilderProcessor"], result)

    @builtins.property
    def trace_id_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorTraceIdRemapper"]:
        '''trace_id_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#trace_id_remapper LogsCustomPipeline#trace_id_remapper}
        '''
        result = self._values.get("trace_id_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorTraceIdRemapper"], result)

    @builtins.property
    def url_parser(self) -> typing.Optional["LogsCustomPipelineProcessorUrlParser"]:
        '''url_parser block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#url_parser LogsCustomPipeline#url_parser}
        '''
        result = self._values.get("url_parser")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorUrlParser"], result)

    @builtins.property
    def user_agent_parser(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorUserAgentParser"]:
        '''user_agent_parser block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#user_agent_parser LogsCustomPipeline#user_agent_parser}
        '''
        result = self._values.get("user_agent_parser")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorUserAgentParser"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorArithmeticProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "target": "target",
        "is_enabled": "isEnabled",
        "is_replace_missing": "isReplaceMissing",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorArithmeticProcessor:
    def __init__(
        self,
        *,
        expression: builtins.str,
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_replace_missing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Arithmetic operation between one or more log attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#expression LogsCustomPipeline#expression}
        :param target: Name of the attribute that contains the result of the arithmetic operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: Boolean value to enable your pipeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param is_replace_missing: If true, it replaces all missing attributes of expression by 0, false skips the operation if an attribute is missing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_replace_missing LogsCustomPipeline#is_replace_missing}
        :param name: Your pipeline name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__165dfccd3ae85989f1d521f57b75d845a867d1a4f22b807f94d1aaea275be552)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument is_replace_missing", value=is_replace_missing, expected_type=type_hints["is_replace_missing"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
            "target": target,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if is_replace_missing is not None:
            self._values["is_replace_missing"] = is_replace_missing
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def expression(self) -> builtins.str:
        '''Arithmetic operation between one or more log attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#expression LogsCustomPipeline#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the attribute that contains the result of the arithmetic operation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean value to enable your pipeline.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_replace_missing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, it replaces all missing attributes of expression by 0, false skips the operation if an attribute is missing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_replace_missing LogsCustomPipeline#is_replace_missing}
        '''
        result = self._values.get("is_replace_missing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Your pipeline name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorArithmeticProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorArithmeticProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorArithmeticProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05d9797a3396bf3e9d3c32d4fdff7d343cccc4c759763a4e243591121ef0db43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetIsReplaceMissing")
    def reset_is_replace_missing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsReplaceMissing", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isReplaceMissingInput")
    def is_replace_missing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isReplaceMissingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e363508fde9ffeb98f691af5e61f1ba73ad2ddb03563d77e62e59d16525f9a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ef3d3da873b0a439249303437e91c62fb4b3c2b80aec8d008e9682cc4b7e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isReplaceMissing")
    def is_replace_missing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isReplaceMissing"))

    @is_replace_missing.setter
    def is_replace_missing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d80b6a691c0611a21df1055eec7adc7a7c69e745d465c2c8c683c584aa6ddba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isReplaceMissing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e1f30706d4b772c31610d43fb5386a95f7d77510f08d7f6b7d2def5a9b256c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc60c9d7103e274bb4f0a83c6d514e7f657b6894bb7f666db6f527e5d74fda8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorArithmeticProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorArithmeticProcessor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorArithmeticProcessor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8764a111b3a5d832e4295bafe2f18b8191becbc06a8b6f960c1a07ecfe49f8cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorAttributeRemapper",
    jsii_struct_bases=[],
    name_mapping={
        "sources": "sources",
        "source_type": "sourceType",
        "target": "target",
        "target_type": "targetType",
        "is_enabled": "isEnabled",
        "name": "name",
        "override_on_conflict": "overrideOnConflict",
        "preserve_source": "preserveSource",
        "target_format": "targetFormat",
    },
)
class LogsCustomPipelineProcessorAttributeRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        source_type: builtins.str,
        target: builtins.str,
        target_type: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        override_on_conflict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preserve_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes or tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param source_type: Defines where the sources are from (log ``attribute`` or ``tag``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source_type LogsCustomPipeline#source_type}
        :param target: Final attribute or tag name to remap the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param target_type: Defines if the target is a log ``attribute`` or ``tag``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target_type LogsCustomPipeline#target_type}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        :param override_on_conflict: Override the target element if already set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#override_on_conflict LogsCustomPipeline#override_on_conflict}
        :param preserve_source: Remove or preserve the remapped source element. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#preserve_source LogsCustomPipeline#preserve_source}
        :param target_format: If the ``target_type`` of the remapper is ``attribute``, try to cast the value to a new specific type. If the cast is not possible, the original type is kept. ``string``, ``integer``, or ``double`` are the possible types. If the ``target_type`` is ``tag``, this parameter may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target_format LogsCustomPipeline#target_format}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3d422d5f6fed40ee0387e1dd3994e0e679e0706bd384bd358d46ba7f62c099)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument override_on_conflict", value=override_on_conflict, expected_type=type_hints["override_on_conflict"])
            check_type(argname="argument preserve_source", value=preserve_source, expected_type=type_hints["preserve_source"])
            check_type(argname="argument target_format", value=target_format, expected_type=type_hints["target_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
            "source_type": source_type,
            "target": target,
            "target_type": target_type,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name
        if override_on_conflict is not None:
            self._values["override_on_conflict"] = override_on_conflict
        if preserve_source is not None:
            self._values["preserve_source"] = preserve_source
        if target_format is not None:
            self._values["target_format"] = target_format

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes or tags.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def source_type(self) -> builtins.str:
        '''Defines where the sources are from (log ``attribute`` or ``tag``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source_type LogsCustomPipeline#source_type}
        '''
        result = self._values.get("source_type")
        assert result is not None, "Required property 'source_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Final attribute or tag name to remap the sources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_type(self) -> builtins.str:
        '''Defines if the target is a log ``attribute`` or ``tag``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target_type LogsCustomPipeline#target_type}
        '''
        result = self._values.get("target_type")
        assert result is not None, "Required property 'target_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def override_on_conflict(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Override the target element if already set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#override_on_conflict LogsCustomPipeline#override_on_conflict}
        '''
        result = self._values.get("override_on_conflict")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def preserve_source(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Remove or preserve the remapped source element.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#preserve_source LogsCustomPipeline#preserve_source}
        '''
        result = self._values.get("preserve_source")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def target_format(self) -> typing.Optional[builtins.str]:
        '''If the ``target_type`` of the remapper is ``attribute``, try to cast the value to a new specific type.

        If the cast is not possible, the original type is kept. ``string``, ``integer``, or ``double`` are the possible types. If the ``target_type`` is ``tag``, this parameter may not be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target_format LogsCustomPipeline#target_format}
        '''
        result = self._values.get("target_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorAttributeRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorAttributeRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorAttributeRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a070498120d900f4a0e1e876b6328834ce066ee7e2cef9699ebb3f7c1b380e9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOverrideOnConflict")
    def reset_override_on_conflict(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideOnConflict", []))

    @jsii.member(jsii_name="resetPreserveSource")
    def reset_preserve_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreserveSource", []))

    @jsii.member(jsii_name="resetTargetFormat")
    def reset_target_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetFormat", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideOnConflictInput")
    def override_on_conflict_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideOnConflictInput"))

    @builtins.property
    @jsii.member(jsii_name="preserveSourceInput")
    def preserve_source_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preserveSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTypeInput")
    def source_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetFormatInput")
    def target_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetTypeInput")
    def target_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e0b337fc3d2a34e0ea36f5bc6f43cda6358b6e5f0213bb7c00a282834bc8ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b6b55f4a42d076bb52639e003b9e0e2c330e3005df2107ab7fca2223ed9f4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overrideOnConflict")
    def override_on_conflict(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overrideOnConflict"))

    @override_on_conflict.setter
    def override_on_conflict(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7179e886b2a4212c745d02dfb10e7b9bfbf004a919c5845d535073258aa40104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideOnConflict", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preserveSource")
    def preserve_source(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preserveSource"))

    @preserve_source.setter
    def preserve_source(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac2161cfa27696ec8fe12ba45818c0fa3767617e30c98f201f3b6d8ac1dadcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f9cb0c5d0e1eb1339a913a646fc7a123f0aab8c9813d014de5e683eb549602)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @source_type.setter
    def source_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64ffbf0753f1b58a50dd5ba1366fc77a3071e88fabd1214834f09b96268389e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934954cd6a3a53003d1079a6b98e24c89792d69209d13b6f6be53cb1c0a2d920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetFormat")
    def target_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetFormat"))

    @target_format.setter
    def target_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94b125d6d060826fc5fe44801833f5b5b6447f71aab7be18bcd4f156581a060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetType"))

    @target_type.setter
    def target_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a390fe672d6b6187e45767ea0b044d704abffb1150f83e5e394a185803e3d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorAttributeRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorAttributeRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorAttributeRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30a3323c99fdb7d2d1e78a5e6e381c842e3bf825d7d59299f692da394c3dfaa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorCategoryProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "target": "target",
        "is_enabled": "isEnabled",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorCategoryProcessor:
    def __init__(
        self,
        *,
        category: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineProcessorCategoryProcessorCategory", typing.Dict[builtins.str, typing.Any]]]],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: category block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#category LogsCustomPipeline#category}
        :param target: Name of the target attribute whose value is defined by the matching category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d020454179d0e702232498c0fb091e398e76a34782b1418abf4a7269ebea3d3b)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
            "target": target,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def category(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessorCategoryProcessorCategory"]]:
        '''category block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#category LogsCustomPipeline#category}
        '''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessorCategoryProcessorCategory"]], result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the target attribute whose value is defined by the matching category.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the category.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorCategoryProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorCategoryProcessorCategory",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter", "name": "name"},
)
class LogsCustomPipelineProcessorCategoryProcessorCategory:
    def __init__(
        self,
        *,
        filter: typing.Union["LogsCustomPipelineProcessorCategoryProcessorCategoryFilter", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#filter LogsCustomPipeline#filter}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}.
        '''
        if isinstance(filter, dict):
            filter = LogsCustomPipelineProcessorCategoryProcessorCategoryFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7e1329af950c282610449115196a444c0c9855ae09fad4918548fc8b396241)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
            "name": name,
        }

    @builtins.property
    def filter(self) -> "LogsCustomPipelineProcessorCategoryProcessorCategoryFilter":
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#filter LogsCustomPipeline#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast("LogsCustomPipelineProcessorCategoryProcessorCategoryFilter", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorCategoryProcessorCategory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorCategoryProcessorCategoryFilter",
    jsii_struct_bases=[],
    name_mapping={"query": "query"},
)
class LogsCustomPipelineProcessorCategoryProcessorCategoryFilter:
    def __init__(self, *, query: builtins.str) -> None:
        '''
        :param query: Filter criteria of the category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#query LogsCustomPipeline#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69b771f248ac613e79dadc9d0b68cc45648b85fc7b1ea8aeaf7c7cf2e4ee334)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }

    @builtins.property
    def query(self) -> builtins.str:
        '''Filter criteria of the category.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#query LogsCustomPipeline#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorCategoryProcessorCategoryFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorCategoryProcessorCategoryFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorCategoryProcessorCategoryFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d692e6103183fd28bcf3912a6f7389af61824912f03e5946c5c8ef88293950d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa42c9d39d6e2316d2a74b8e087df11a1e955cad0990151bf64c850034678e8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorCategoryProcessorCategoryFilter]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorCategoryProcessorCategoryFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorCategoryProcessorCategoryFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88798d6e39d745b915fce8ef2686070024481b3d7a9d716637e2f9116749d5fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorCategoryProcessorCategoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorCategoryProcessorCategoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e822add5e45f4bef35b648616980fe8b0bdf0b0b959be69c51ffffb54e58d2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogsCustomPipelineProcessorCategoryProcessorCategoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb15500654dc374f631d5a6b9e06f46c1e50f5f2c36475f43a8da8a78ba8a644)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsCustomPipelineProcessorCategoryProcessorCategoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3262ae0df39ed7a53eb726b36f21dbda86623da6222ccdea7efadfb44674a168)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b70ea27382ff1985b248d617e576bdaa9341f7c65d1fdca06361812904febaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1647216bf932d1eb569809c2908c93d84fc0b156da5a0161df42c4231ba7f859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorCategoryProcessorCategory]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorCategoryProcessorCategory]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorCategoryProcessorCategory]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ea6cb952750a3e8dccadedacc0f85813fba7de6dea8f76a7269d5da5c4f9a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorCategoryProcessorCategoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorCategoryProcessorCategoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91b0702bd187b80342b6f5e6036dc5c179faefddfc4b4f2c57afe44f58381d87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFilter")
    def put_filter(self, *, query: builtins.str) -> None:
        '''
        :param query: Filter criteria of the category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#query LogsCustomPipeline#query}
        '''
        value = LogsCustomPipelineProcessorCategoryProcessorCategoryFilter(query=query)

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(
        self,
    ) -> LogsCustomPipelineProcessorCategoryProcessorCategoryFilterOutputReference:
        return typing.cast(LogsCustomPipelineProcessorCategoryProcessorCategoryFilterOutputReference, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorCategoryProcessorCategoryFilter]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorCategoryProcessorCategoryFilter], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94b1263b576abe2ce40f13c559e0b3192f50252cf18a5982d2c1c0d29b716497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorCategoryProcessorCategory]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorCategoryProcessorCategory]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorCategoryProcessorCategory]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a65dd7bf75ce80f4df7ac2fe5e4cdd0e3531871a33720117dbb971b463d0cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorCategoryProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorCategoryProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec7f8a23c5afbaf16952c86edf4b552f0d57ecb027e6213f15d90eb4571c8d0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCategory")
    def put_category(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorCategoryProcessorCategory, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c887431da5e945c3df6036be47fbab1b8d8f0ef0dde9176c5e2c49352bf60e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCategory", [value]))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> LogsCustomPipelineProcessorCategoryProcessorCategoryList:
        return typing.cast(LogsCustomPipelineProcessorCategoryProcessorCategoryList, jsii.get(self, "category"))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorCategoryProcessorCategory]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorCategoryProcessorCategory]]], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a662358d429aeded4a587dc4022f09286bfa2dd5a552ceb071a5caeea3270ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e2672b9b3cb324de42c3e87c3e1da2f32faf5b3a245624ac19362ea7d6590a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9815ede4230c572ee01c99de9340a3398235e7520a7590547b90ace08514d435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorCategoryProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorCategoryProcessor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorCategoryProcessor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00a54eaf6adba95744703204a96ac4cf4cf77812b902ddb7ecfdfe3beabee27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorDateRemapper",
    jsii_struct_bases=[],
    name_mapping={"sources": "sources", "is_enabled": "isEnabled", "name": "name"},
)
class LogsCustomPipelineProcessorDateRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b6df76e438ef90b0e20dfa2851fdc5cdf1025815d7cc47b0473fbd428573ed)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorDateRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorDateRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorDateRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98c63044ff0c20b642980c28f513f07a2a798c0a7daea2f9662c515eefd9347a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8775c5b9268424e72d85e8496355eba2c81f4f3e7d4d21c1c425fad127819c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8667b7fb1cb22a5037433d78af772578d22cb58eedb484d1c2d7a264a6a1b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__626c0eb72b89340523a1e5254fc564b4e48e31ffb54aae10cb67a79435a5893d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorDateRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorDateRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorDateRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1291d4e75340add33012bb1eab04270eeb74636647a157eb867c62ec12fcc568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorGeoIpParser",
    jsii_struct_bases=[],
    name_mapping={
        "sources": "sources",
        "target": "target",
        "is_enabled": "isEnabled",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorGeoIpParser:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param target: Name of the parent attribute that contains all the extracted details from the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5876c2864b1a1109c3e39053fe1450681dc744c291d4fa0b2cbd12231caa5f7)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
            "target": target,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the parent attribute that contains all the extracted details from the sources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorGeoIpParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorGeoIpParserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorGeoIpParserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad6fc8938263665763e769fad56c032080ca7fc4c942f7ef3804322fce617160)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae16154b0231ed4d12e00a635072c00e2435a683ab8b0e58e01f7c6deb97165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9233e83ab9841e0746828b78e770a2a4850f960389efce895d5874aad8c4ba01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6c4d5aa7b4447e1684b83719fee8e8ac87a184b590eaa3cfd753437c5df2289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f17bce88a357c74f56c08643f2e374a0790408b0c7fdfb7c0ef785de4ae483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogsCustomPipelineProcessorGeoIpParser]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorGeoIpParser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorGeoIpParser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b518f5e38d97f19af58189a59a90935eb240a72b1a2e7016352f01786577b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorGrokParser",
    jsii_struct_bases=[],
    name_mapping={
        "grok": "grok",
        "source": "source",
        "is_enabled": "isEnabled",
        "name": "name",
        "samples": "samples",
    },
)
class LogsCustomPipelineProcessorGrokParser:
    def __init__(
        self,
        *,
        grok: typing.Union["LogsCustomPipelineProcessorGrokParserGrok", typing.Dict[builtins.str, typing.Any]],
        source: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        samples: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param grok: grok block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#grok LogsCustomPipeline#grok}
        :param source: Name of the log attribute to parse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        :param samples: List of sample logs for this parser. It can save up to 5 samples. Each sample takes up to 5000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#samples LogsCustomPipeline#samples}
        '''
        if isinstance(grok, dict):
            grok = LogsCustomPipelineProcessorGrokParserGrok(**grok)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d345af20518336969f6d0e754f1cf620b57815300996a51e7d870f8b9c21dea6)
            check_type(argname="argument grok", value=grok, expected_type=type_hints["grok"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument samples", value=samples, expected_type=type_hints["samples"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "grok": grok,
            "source": source,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name
        if samples is not None:
            self._values["samples"] = samples

    @builtins.property
    def grok(self) -> "LogsCustomPipelineProcessorGrokParserGrok":
        '''grok block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#grok LogsCustomPipeline#grok}
        '''
        result = self._values.get("grok")
        assert result is not None, "Required property 'grok' is missing"
        return typing.cast("LogsCustomPipelineProcessorGrokParserGrok", result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Name of the log attribute to parse.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def samples(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of sample logs for this parser.

        It can save up to 5 samples. Each sample takes up to 5000 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#samples LogsCustomPipeline#samples}
        '''
        result = self._values.get("samples")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorGrokParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorGrokParserGrok",
    jsii_struct_bases=[],
    name_mapping={"match_rules": "matchRules", "support_rules": "supportRules"},
)
class LogsCustomPipelineProcessorGrokParserGrok:
    def __init__(
        self,
        *,
        match_rules: builtins.str,
        support_rules: builtins.str,
    ) -> None:
        '''
        :param match_rules: Match rules for your grok parser. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#match_rules LogsCustomPipeline#match_rules}
        :param support_rules: Support rules for your grok parser. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#support_rules LogsCustomPipeline#support_rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21a08abaf2a6cbf76e5e0ed1dcff20792a6ea0c7cae6cd9358348db85641b804)
            check_type(argname="argument match_rules", value=match_rules, expected_type=type_hints["match_rules"])
            check_type(argname="argument support_rules", value=support_rules, expected_type=type_hints["support_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_rules": match_rules,
            "support_rules": support_rules,
        }

    @builtins.property
    def match_rules(self) -> builtins.str:
        '''Match rules for your grok parser.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#match_rules LogsCustomPipeline#match_rules}
        '''
        result = self._values.get("match_rules")
        assert result is not None, "Required property 'match_rules' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def support_rules(self) -> builtins.str:
        '''Support rules for your grok parser.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#support_rules LogsCustomPipeline#support_rules}
        '''
        result = self._values.get("support_rules")
        assert result is not None, "Required property 'support_rules' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorGrokParserGrok(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorGrokParserGrokOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorGrokParserGrokOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19d27c2ad36831e510788b04e0e0db467e327ee44ab2671caf6352d5fd005af9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="matchRulesInput")
    def match_rules_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="supportRulesInput")
    def support_rules_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="matchRules")
    def match_rules(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchRules"))

    @match_rules.setter
    def match_rules(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405e1da29d5471136e0108b61534cd43146ac0e5378fa18e44ed5f7454bc755f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportRules")
    def support_rules(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportRules"))

    @support_rules.setter
    def support_rules(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8b7f404ed5c213a9057134bcb87b4d134656c5ce7ee9ab35590588ee4b7083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorGrokParserGrok]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorGrokParserGrok], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorGrokParserGrok],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec88b97a1a58aec7ffe9828c9432ef3ad26dc213191a667f03bfc45b1420416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorGrokParserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorGrokParserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85a7780a9f46b1e92b487a0ff78b8d2b4f59f9898580fd0de07d376e90313f79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrok")
    def put_grok(
        self,
        *,
        match_rules: builtins.str,
        support_rules: builtins.str,
    ) -> None:
        '''
        :param match_rules: Match rules for your grok parser. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#match_rules LogsCustomPipeline#match_rules}
        :param support_rules: Support rules for your grok parser. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#support_rules LogsCustomPipeline#support_rules}
        '''
        value = LogsCustomPipelineProcessorGrokParserGrok(
            match_rules=match_rules, support_rules=support_rules
        )

        return typing.cast(None, jsii.invoke(self, "putGrok", [value]))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSamples")
    def reset_samples(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamples", []))

    @builtins.property
    @jsii.member(jsii_name="grok")
    def grok(self) -> LogsCustomPipelineProcessorGrokParserGrokOutputReference:
        return typing.cast(LogsCustomPipelineProcessorGrokParserGrokOutputReference, jsii.get(self, "grok"))

    @builtins.property
    @jsii.member(jsii_name="grokInput")
    def grok_input(self) -> typing.Optional[LogsCustomPipelineProcessorGrokParserGrok]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorGrokParserGrok], jsii.get(self, "grokInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="samplesInput")
    def samples_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "samplesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c8ec329219a9e1bd1776f8aa2d9642613634308b49880ed3fdf079a446bc82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96e838514d2895dccf71c9f2745c3e510b5e42b7c39b3eabb9d0180ebc2ca27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samples")
    def samples(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "samples"))

    @samples.setter
    def samples(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dac23b16addc6d8334ef0999bcff61e24c66f4afad4c9ccad009c110d788a51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samples", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ac060afe6361667d2eb92505165c772be8c9369c90b7dce3a0bb6aacad4e1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogsCustomPipelineProcessorGrokParser]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorGrokParser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorGrokParser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e19868df886c42fc7da6a77398f765176a97ef511e81e11be1bb13cd8eed24d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9c3f31f1607ec4e4c7211a540aad07d1b5b426644c8c3101f42aaa91c37f611)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LogsCustomPipelineProcessorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c0a26409fab740d17f9cffe1cb17d591fe0e179622020097918ba6a857b6141)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsCustomPipelineProcessorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78331358886a3ddf5567d76f9116ba8baf7bcf8fda341cdef485178df985fa3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a7997e6681e8d33737d46f6d3cabd33b4ab3b9fb5db24dfc5f0e8ebd0cf8e82)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcdb13fdc1022ae6fdd5b2bac099920d32733eab5947647b6f172f8355618c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessor]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessor]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessor]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa940b186cb7e012c6d13893fa6b2dfbd9ad3d88768ded1edb57c715a8fafbf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorLookupProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "lookup_table": "lookupTable",
        "source": "source",
        "target": "target",
        "default_lookup": "defaultLookup",
        "is_enabled": "isEnabled",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorLookupProcessor:
    def __init__(
        self,
        *,
        lookup_table: typing.Sequence[builtins.str],
        source: builtins.str,
        target: builtins.str,
        default_lookup: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lookup_table: List of entries of the lookup table using ``key,value`` format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_table LogsCustomPipeline#lookup_table}
        :param source: Name of the source attribute used to do the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        :param target: Name of the attribute that contains the result of the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param default_lookup: Default lookup value to use if there is no entry in the lookup table for the value of the source attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#default_lookup LogsCustomPipeline#default_lookup}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c4305e56ee1b323e4b08be1a73f63b90af7a45c702b03ab87278aa01bcf83d)
            check_type(argname="argument lookup_table", value=lookup_table, expected_type=type_hints["lookup_table"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument default_lookup", value=default_lookup, expected_type=type_hints["default_lookup"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lookup_table": lookup_table,
            "source": source,
            "target": target,
        }
        if default_lookup is not None:
            self._values["default_lookup"] = default_lookup
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def lookup_table(self) -> typing.List[builtins.str]:
        '''List of entries of the lookup table using ``key,value`` format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_table LogsCustomPipeline#lookup_table}
        '''
        result = self._values.get("lookup_table")
        assert result is not None, "Required property 'lookup_table' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Name of the source attribute used to do the lookup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the attribute that contains the result of the lookup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_lookup(self) -> typing.Optional[builtins.str]:
        '''Default lookup value to use if there is no entry in the lookup table for the value of the source attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#default_lookup LogsCustomPipeline#default_lookup}
        '''
        result = self._values.get("default_lookup")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorLookupProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorLookupProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorLookupProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__989f901959d9b0417f743e275c935776d4e0e2eb8c61348a6b6003c96fd7272b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultLookup")
    def reset_default_lookup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLookup", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="defaultLookupInput")
    def default_lookup_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultLookupInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="lookupTableInput")
    def lookup_table_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "lookupTableInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLookup")
    def default_lookup(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultLookup"))

    @default_lookup.setter
    def default_lookup(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__074baad2a9096250af85266a8f04d46f2751e72b7c0167e7a12088bea9aea154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLookup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd1f2cc5eb33e4dfa05294eaba285f76635578140918144e1a964d74e6a7d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lookupTable")
    def lookup_table(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "lookupTable"))

    @lookup_table.setter
    def lookup_table(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfb37bd71c0e01cab79c571e9d323c3dea09eb69aed11bb3003965cf3d5adae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lookupTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61f00076db9a13743c0a743a8381f302cd607d430ad15863c1a16bf8949cfb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f177e4f6ba4cdfb4423e11266f8c6b74ea35df915ca23aac7888b4abb51375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436142d7fae39dce4cab6d4fe975399b6179b345c3a4da38084430c5d9c8ecbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorLookupProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorLookupProcessor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorLookupProcessor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608ffbc8b6dc0b145a3b0d9dd6176222edfa06b3f6d7c585244afcb91f119803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorMessageRemapper",
    jsii_struct_bases=[],
    name_mapping={"sources": "sources", "is_enabled": "isEnabled", "name": "name"},
)
class LogsCustomPipelineProcessorMessageRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ca14cc207841035e09e338e44cdd9270515b65ee52b5063928d2892e79136c)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorMessageRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorMessageRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorMessageRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77e888c9a07dd8fdc997cebe1efe0498c8b85a6e1968cccfbf68390cdfe744b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca0b6fbe4ea3eb634aa7398db62dda4c1960365d2494608847220f2ebde60cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dbc7e10b43b1a9bac7d470aab3ced3efa35f89981a1cb70e0cbb314fc71151d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70c5963132c01dc79aec276317d63afdc8da66d102bd5c85651002ac1f12c37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorMessageRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorMessageRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorMessageRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d96ef5fa4e978e8dd98d29f0ced8200a58a808961fa6dae125277cf479bfcfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c0c8c66d32b4a8cd59b61a5b5f470a7b6f6c84809aad4f9137bcdf08f822dda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putArithmeticProcessor")
    def put_arithmetic_processor(
        self,
        *,
        expression: builtins.str,
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_replace_missing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Arithmetic operation between one or more log attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#expression LogsCustomPipeline#expression}
        :param target: Name of the attribute that contains the result of the arithmetic operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: Boolean value to enable your pipeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param is_replace_missing: If true, it replaces all missing attributes of expression by 0, false skips the operation if an attribute is missing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_replace_missing LogsCustomPipeline#is_replace_missing}
        :param name: Your pipeline name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorArithmeticProcessor(
            expression=expression,
            target=target,
            is_enabled=is_enabled,
            is_replace_missing=is_replace_missing,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putArithmeticProcessor", [value]))

    @jsii.member(jsii_name="putAttributeRemapper")
    def put_attribute_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        source_type: builtins.str,
        target: builtins.str,
        target_type: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        override_on_conflict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preserve_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes or tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param source_type: Defines where the sources are from (log ``attribute`` or ``tag``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source_type LogsCustomPipeline#source_type}
        :param target: Final attribute or tag name to remap the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param target_type: Defines if the target is a log ``attribute`` or ``tag``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target_type LogsCustomPipeline#target_type}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        :param override_on_conflict: Override the target element if already set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#override_on_conflict LogsCustomPipeline#override_on_conflict}
        :param preserve_source: Remove or preserve the remapped source element. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#preserve_source LogsCustomPipeline#preserve_source}
        :param target_format: If the ``target_type`` of the remapper is ``attribute``, try to cast the value to a new specific type. If the cast is not possible, the original type is kept. ``string``, ``integer``, or ``double`` are the possible types. If the ``target_type`` is ``tag``, this parameter may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target_format LogsCustomPipeline#target_format}
        '''
        value = LogsCustomPipelineProcessorAttributeRemapper(
            sources=sources,
            source_type=source_type,
            target=target,
            target_type=target_type,
            is_enabled=is_enabled,
            name=name,
            override_on_conflict=override_on_conflict,
            preserve_source=preserve_source,
            target_format=target_format,
        )

        return typing.cast(None, jsii.invoke(self, "putAttributeRemapper", [value]))

    @jsii.member(jsii_name="putCategoryProcessor")
    def put_category_processor(
        self,
        *,
        category: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorCategoryProcessorCategory, typing.Dict[builtins.str, typing.Any]]]],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: category block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#category LogsCustomPipeline#category}
        :param target: Name of the target attribute whose value is defined by the matching category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorCategoryProcessor(
            category=category, target=target, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putCategoryProcessor", [value]))

    @jsii.member(jsii_name="putDateRemapper")
    def put_date_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorDateRemapper(
            sources=sources, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putDateRemapper", [value]))

    @jsii.member(jsii_name="putGeoIpParser")
    def put_geo_ip_parser(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param target: Name of the parent attribute that contains all the extracted details from the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorGeoIpParser(
            sources=sources, target=target, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putGeoIpParser", [value]))

    @jsii.member(jsii_name="putGrokParser")
    def put_grok_parser(
        self,
        *,
        grok: typing.Union[LogsCustomPipelineProcessorGrokParserGrok, typing.Dict[builtins.str, typing.Any]],
        source: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        samples: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param grok: grok block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#grok LogsCustomPipeline#grok}
        :param source: Name of the log attribute to parse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        :param samples: List of sample logs for this parser. It can save up to 5 samples. Each sample takes up to 5000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#samples LogsCustomPipeline#samples}
        '''
        value = LogsCustomPipelineProcessorGrokParser(
            grok=grok, source=source, is_enabled=is_enabled, name=name, samples=samples
        )

        return typing.cast(None, jsii.invoke(self, "putGrokParser", [value]))

    @jsii.member(jsii_name="putLookupProcessor")
    def put_lookup_processor(
        self,
        *,
        lookup_table: typing.Sequence[builtins.str],
        source: builtins.str,
        target: builtins.str,
        default_lookup: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lookup_table: List of entries of the lookup table using ``key,value`` format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_table LogsCustomPipeline#lookup_table}
        :param source: Name of the source attribute used to do the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        :param target: Name of the attribute that contains the result of the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param default_lookup: Default lookup value to use if there is no entry in the lookup table for the value of the source attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#default_lookup LogsCustomPipeline#default_lookup}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorLookupProcessor(
            lookup_table=lookup_table,
            source=source,
            target=target,
            default_lookup=default_lookup,
            is_enabled=is_enabled,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putLookupProcessor", [value]))

    @jsii.member(jsii_name="putMessageRemapper")
    def put_message_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorMessageRemapper(
            sources=sources, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putMessageRemapper", [value]))

    @jsii.member(jsii_name="putPipeline")
    def put_pipeline(
        self,
        *,
        filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineProcessorPipelineFilter", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineProcessorPipelineProcessor", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#filter LogsCustomPipeline#filter}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#description LogsCustomPipeline#description}.
        :param is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}.
        :param processor: processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#processor LogsCustomPipeline#processor}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#tags LogsCustomPipeline#tags}.
        '''
        value = LogsCustomPipelineProcessorPipeline(
            filter=filter,
            name=name,
            description=description,
            is_enabled=is_enabled,
            processor=processor,
            tags=tags,
        )

        return typing.cast(None, jsii.invoke(self, "putPipeline", [value]))

    @jsii.member(jsii_name="putReferenceTableLookupProcessor")
    def put_reference_table_lookup_processor(
        self,
        *,
        lookup_enrichment_table: builtins.str,
        source: builtins.str,
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lookup_enrichment_table: Name of the Reference Table for the source attribute and their associated target attribute values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_enrichment_table LogsCustomPipeline#lookup_enrichment_table}
        :param source: Name of the source attribute used to do the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        :param target: Name of the attribute that contains the result of the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorReferenceTableLookupProcessor(
            lookup_enrichment_table=lookup_enrichment_table,
            source=source,
            target=target,
            is_enabled=is_enabled,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putReferenceTableLookupProcessor", [value]))

    @jsii.member(jsii_name="putServiceRemapper")
    def put_service_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorServiceRemapper(
            sources=sources, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putServiceRemapper", [value]))

    @jsii.member(jsii_name="putSpanIdRemapper")
    def put_span_id_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorSpanIdRemapper(
            sources=sources, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putSpanIdRemapper", [value]))

    @jsii.member(jsii_name="putStatusRemapper")
    def put_status_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorStatusRemapper(
            sources=sources, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putStatusRemapper", [value]))

    @jsii.member(jsii_name="putStringBuilderProcessor")
    def put_string_builder_processor(
        self,
        *,
        target: builtins.str,
        template: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_replace_missing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: The name of the attribute that contains the result of the template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param template: The formula with one or more attributes and raw text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#template LogsCustomPipeline#template}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param is_replace_missing: If it replaces all missing attributes of template by an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_replace_missing LogsCustomPipeline#is_replace_missing}
        :param name: The name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorStringBuilderProcessor(
            target=target,
            template=template,
            is_enabled=is_enabled,
            is_replace_missing=is_replace_missing,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putStringBuilderProcessor", [value]))

    @jsii.member(jsii_name="putTraceIdRemapper")
    def put_trace_id_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorTraceIdRemapper(
            sources=sources, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putTraceIdRemapper", [value]))

    @jsii.member(jsii_name="putUrlParser")
    def put_url_parser(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        normalize_ending_slashes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param target: Name of the parent attribute that contains all the extracted details from the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        :param normalize_ending_slashes: Normalize the ending slashes or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#normalize_ending_slashes LogsCustomPipeline#normalize_ending_slashes}
        '''
        value = LogsCustomPipelineProcessorUrlParser(
            sources=sources,
            target=target,
            is_enabled=is_enabled,
            name=name,
            normalize_ending_slashes=normalize_ending_slashes,
        )

        return typing.cast(None, jsii.invoke(self, "putUrlParser", [value]))

    @jsii.member(jsii_name="putUserAgentParser")
    def put_user_agent_parser(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_encoded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param target: Name of the parent attribute that contains all the extracted details from the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param is_encoded: If the source attribute is URL encoded or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_encoded LogsCustomPipeline#is_encoded}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorUserAgentParser(
            sources=sources,
            target=target,
            is_enabled=is_enabled,
            is_encoded=is_encoded,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putUserAgentParser", [value]))

    @jsii.member(jsii_name="resetArithmeticProcessor")
    def reset_arithmetic_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArithmeticProcessor", []))

    @jsii.member(jsii_name="resetAttributeRemapper")
    def reset_attribute_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeRemapper", []))

    @jsii.member(jsii_name="resetCategoryProcessor")
    def reset_category_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategoryProcessor", []))

    @jsii.member(jsii_name="resetDateRemapper")
    def reset_date_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateRemapper", []))

    @jsii.member(jsii_name="resetGeoIpParser")
    def reset_geo_ip_parser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoIpParser", []))

    @jsii.member(jsii_name="resetGrokParser")
    def reset_grok_parser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrokParser", []))

    @jsii.member(jsii_name="resetLookupProcessor")
    def reset_lookup_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLookupProcessor", []))

    @jsii.member(jsii_name="resetMessageRemapper")
    def reset_message_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageRemapper", []))

    @jsii.member(jsii_name="resetPipeline")
    def reset_pipeline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPipeline", []))

    @jsii.member(jsii_name="resetReferenceTableLookupProcessor")
    def reset_reference_table_lookup_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferenceTableLookupProcessor", []))

    @jsii.member(jsii_name="resetServiceRemapper")
    def reset_service_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceRemapper", []))

    @jsii.member(jsii_name="resetSpanIdRemapper")
    def reset_span_id_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpanIdRemapper", []))

    @jsii.member(jsii_name="resetStatusRemapper")
    def reset_status_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusRemapper", []))

    @jsii.member(jsii_name="resetStringBuilderProcessor")
    def reset_string_builder_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringBuilderProcessor", []))

    @jsii.member(jsii_name="resetTraceIdRemapper")
    def reset_trace_id_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTraceIdRemapper", []))

    @jsii.member(jsii_name="resetUrlParser")
    def reset_url_parser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlParser", []))

    @jsii.member(jsii_name="resetUserAgentParser")
    def reset_user_agent_parser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAgentParser", []))

    @builtins.property
    @jsii.member(jsii_name="arithmeticProcessor")
    def arithmetic_processor(
        self,
    ) -> LogsCustomPipelineProcessorArithmeticProcessorOutputReference:
        return typing.cast(LogsCustomPipelineProcessorArithmeticProcessorOutputReference, jsii.get(self, "arithmeticProcessor"))

    @builtins.property
    @jsii.member(jsii_name="attributeRemapper")
    def attribute_remapper(
        self,
    ) -> LogsCustomPipelineProcessorAttributeRemapperOutputReference:
        return typing.cast(LogsCustomPipelineProcessorAttributeRemapperOutputReference, jsii.get(self, "attributeRemapper"))

    @builtins.property
    @jsii.member(jsii_name="categoryProcessor")
    def category_processor(
        self,
    ) -> LogsCustomPipelineProcessorCategoryProcessorOutputReference:
        return typing.cast(LogsCustomPipelineProcessorCategoryProcessorOutputReference, jsii.get(self, "categoryProcessor"))

    @builtins.property
    @jsii.member(jsii_name="dateRemapper")
    def date_remapper(self) -> LogsCustomPipelineProcessorDateRemapperOutputReference:
        return typing.cast(LogsCustomPipelineProcessorDateRemapperOutputReference, jsii.get(self, "dateRemapper"))

    @builtins.property
    @jsii.member(jsii_name="geoIpParser")
    def geo_ip_parser(self) -> LogsCustomPipelineProcessorGeoIpParserOutputReference:
        return typing.cast(LogsCustomPipelineProcessorGeoIpParserOutputReference, jsii.get(self, "geoIpParser"))

    @builtins.property
    @jsii.member(jsii_name="grokParser")
    def grok_parser(self) -> LogsCustomPipelineProcessorGrokParserOutputReference:
        return typing.cast(LogsCustomPipelineProcessorGrokParserOutputReference, jsii.get(self, "grokParser"))

    @builtins.property
    @jsii.member(jsii_name="lookupProcessor")
    def lookup_processor(
        self,
    ) -> LogsCustomPipelineProcessorLookupProcessorOutputReference:
        return typing.cast(LogsCustomPipelineProcessorLookupProcessorOutputReference, jsii.get(self, "lookupProcessor"))

    @builtins.property
    @jsii.member(jsii_name="messageRemapper")
    def message_remapper(
        self,
    ) -> LogsCustomPipelineProcessorMessageRemapperOutputReference:
        return typing.cast(LogsCustomPipelineProcessorMessageRemapperOutputReference, jsii.get(self, "messageRemapper"))

    @builtins.property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> "LogsCustomPipelineProcessorPipelineOutputReference":
        return typing.cast("LogsCustomPipelineProcessorPipelineOutputReference", jsii.get(self, "pipeline"))

    @builtins.property
    @jsii.member(jsii_name="referenceTableLookupProcessor")
    def reference_table_lookup_processor(
        self,
    ) -> "LogsCustomPipelineProcessorReferenceTableLookupProcessorOutputReference":
        return typing.cast("LogsCustomPipelineProcessorReferenceTableLookupProcessorOutputReference", jsii.get(self, "referenceTableLookupProcessor"))

    @builtins.property
    @jsii.member(jsii_name="serviceRemapper")
    def service_remapper(
        self,
    ) -> "LogsCustomPipelineProcessorServiceRemapperOutputReference":
        return typing.cast("LogsCustomPipelineProcessorServiceRemapperOutputReference", jsii.get(self, "serviceRemapper"))

    @builtins.property
    @jsii.member(jsii_name="spanIdRemapper")
    def span_id_remapper(
        self,
    ) -> "LogsCustomPipelineProcessorSpanIdRemapperOutputReference":
        return typing.cast("LogsCustomPipelineProcessorSpanIdRemapperOutputReference", jsii.get(self, "spanIdRemapper"))

    @builtins.property
    @jsii.member(jsii_name="statusRemapper")
    def status_remapper(
        self,
    ) -> "LogsCustomPipelineProcessorStatusRemapperOutputReference":
        return typing.cast("LogsCustomPipelineProcessorStatusRemapperOutputReference", jsii.get(self, "statusRemapper"))

    @builtins.property
    @jsii.member(jsii_name="stringBuilderProcessor")
    def string_builder_processor(
        self,
    ) -> "LogsCustomPipelineProcessorStringBuilderProcessorOutputReference":
        return typing.cast("LogsCustomPipelineProcessorStringBuilderProcessorOutputReference", jsii.get(self, "stringBuilderProcessor"))

    @builtins.property
    @jsii.member(jsii_name="traceIdRemapper")
    def trace_id_remapper(
        self,
    ) -> "LogsCustomPipelineProcessorTraceIdRemapperOutputReference":
        return typing.cast("LogsCustomPipelineProcessorTraceIdRemapperOutputReference", jsii.get(self, "traceIdRemapper"))

    @builtins.property
    @jsii.member(jsii_name="urlParser")
    def url_parser(self) -> "LogsCustomPipelineProcessorUrlParserOutputReference":
        return typing.cast("LogsCustomPipelineProcessorUrlParserOutputReference", jsii.get(self, "urlParser"))

    @builtins.property
    @jsii.member(jsii_name="userAgentParser")
    def user_agent_parser(
        self,
    ) -> "LogsCustomPipelineProcessorUserAgentParserOutputReference":
        return typing.cast("LogsCustomPipelineProcessorUserAgentParserOutputReference", jsii.get(self, "userAgentParser"))

    @builtins.property
    @jsii.member(jsii_name="arithmeticProcessorInput")
    def arithmetic_processor_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorArithmeticProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorArithmeticProcessor], jsii.get(self, "arithmeticProcessorInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeRemapperInput")
    def attribute_remapper_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorAttributeRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorAttributeRemapper], jsii.get(self, "attributeRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="categoryProcessorInput")
    def category_processor_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorCategoryProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorCategoryProcessor], jsii.get(self, "categoryProcessorInput"))

    @builtins.property
    @jsii.member(jsii_name="dateRemapperInput")
    def date_remapper_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorDateRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorDateRemapper], jsii.get(self, "dateRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="geoIpParserInput")
    def geo_ip_parser_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorGeoIpParser]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorGeoIpParser], jsii.get(self, "geoIpParserInput"))

    @builtins.property
    @jsii.member(jsii_name="grokParserInput")
    def grok_parser_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorGrokParser]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorGrokParser], jsii.get(self, "grokParserInput"))

    @builtins.property
    @jsii.member(jsii_name="lookupProcessorInput")
    def lookup_processor_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorLookupProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorLookupProcessor], jsii.get(self, "lookupProcessorInput"))

    @builtins.property
    @jsii.member(jsii_name="messageRemapperInput")
    def message_remapper_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorMessageRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorMessageRemapper], jsii.get(self, "messageRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="pipelineInput")
    def pipeline_input(self) -> typing.Optional["LogsCustomPipelineProcessorPipeline"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipeline"], jsii.get(self, "pipelineInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceTableLookupProcessorInput")
    def reference_table_lookup_processor_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorReferenceTableLookupProcessor"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorReferenceTableLookupProcessor"], jsii.get(self, "referenceTableLookupProcessorInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRemapperInput")
    def service_remapper_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorServiceRemapper"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorServiceRemapper"], jsii.get(self, "serviceRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="spanIdRemapperInput")
    def span_id_remapper_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorSpanIdRemapper"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorSpanIdRemapper"], jsii.get(self, "spanIdRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="statusRemapperInput")
    def status_remapper_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorStatusRemapper"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorStatusRemapper"], jsii.get(self, "statusRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="stringBuilderProcessorInput")
    def string_builder_processor_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorStringBuilderProcessor"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorStringBuilderProcessor"], jsii.get(self, "stringBuilderProcessorInput"))

    @builtins.property
    @jsii.member(jsii_name="traceIdRemapperInput")
    def trace_id_remapper_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorTraceIdRemapper"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorTraceIdRemapper"], jsii.get(self, "traceIdRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="urlParserInput")
    def url_parser_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorUrlParser"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorUrlParser"], jsii.get(self, "urlParserInput"))

    @builtins.property
    @jsii.member(jsii_name="userAgentParserInput")
    def user_agent_parser_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorUserAgentParser"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorUserAgentParser"], jsii.get(self, "userAgentParserInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessor]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessor]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessor]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbfcce8ba77a44cc6bed0938e9873daa5c2f3e0a3a9c84a79d9ebc6de1d98176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipeline",
    jsii_struct_bases=[],
    name_mapping={
        "filter": "filter",
        "name": "name",
        "description": "description",
        "is_enabled": "isEnabled",
        "processor": "processor",
        "tags": "tags",
    },
)
class LogsCustomPipelineProcessorPipeline:
    def __init__(
        self,
        *,
        filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineProcessorPipelineFilter", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        processor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineProcessorPipelineProcessor", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#filter LogsCustomPipeline#filter}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#description LogsCustomPipeline#description}.
        :param is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}.
        :param processor: processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#processor LogsCustomPipeline#processor}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#tags LogsCustomPipeline#tags}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93cae1451052ba984a3062d0fbeac97ee702dacb11ef0e0d66379fd6266737e3)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument processor", value=processor, expected_type=type_hints["processor"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if processor is not None:
            self._values["processor"] = processor
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def filter(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessorPipelineFilter"]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#filter LogsCustomPipeline#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessorPipelineFilter"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#description LogsCustomPipeline#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}.'''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def processor(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessorPipelineProcessor"]]]:
        '''processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#processor LogsCustomPipeline#processor}
        '''
        result = self._values.get("processor")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessorPipelineProcessor"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#tags LogsCustomPipeline#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipeline(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineFilter",
    jsii_struct_bases=[],
    name_mapping={"query": "query"},
)
class LogsCustomPipelineProcessorPipelineFilter:
    def __init__(self, *, query: builtins.str) -> None:
        '''
        :param query: Filter criteria of the category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#query LogsCustomPipeline#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ac592d8c93de938e3b1deba5116a7ba8ba1904d64d0505cfffedf13593eae8)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }

    @builtins.property
    def query(self) -> builtins.str:
        '''Filter criteria of the category.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#query LogsCustomPipeline#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75e1554d898a170ab6a1bca71b376898ac51c4ad7040a358903a7ab41ba0d0de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogsCustomPipelineProcessorPipelineFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1205df598f9f97b8b4748682656fc36cc90ad6426e9dbf3f5be4dc50876f564)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsCustomPipelineProcessorPipelineFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1db1776596a329a7dcf718d45a6f06e2c73dd20a0c2f3b95648dfb314fd88ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfdcb5cdab919f372070cc072d68b3fff1c642e703a4eaf5ef00e3cb2f713d1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__262f62541cfb9512e6230f50c3e46e0b7380688d359154076990a7e5c42d3f83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1263fd7e3d821a625ec73da7e334c95e9b634c2123ac40ff8b0160d9984f9fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorPipelineFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93476001283b32a42c6502bb95ab86b8726404d6aa64057130a159f7d24d6b94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c5e2cb19a2661caaaa2b49ec993c0b2754137d39484c1673b946c66ed175a08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorPipelineFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorPipelineFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorPipelineFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873f19e6bd5dc83f634149cc500b7dfa754a2882c92eb554908994c22d8362bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorPipelineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f38db5f42046c42808b6898039e5e147f48714f4b48cabb056a3bcb337b3366d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorPipelineFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db91895014e1da8ff264065376c4170487e84806626f357ed0e1ba574e88e103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putProcessor")
    def put_processor(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineProcessorPipelineProcessor", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d25ea2a96a07809236e4ecf51a5f96280e462a5a41bce3d1e99054329fb6f766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProcessor", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetProcessor")
    def reset_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessor", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> LogsCustomPipelineProcessorPipelineFilterList:
        return typing.cast(LogsCustomPipelineProcessorPipelineFilterList, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="processor")
    def processor(self) -> "LogsCustomPipelineProcessorPipelineProcessorList":
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorList", jsii.get(self, "processor"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineFilter]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="processorInput")
    def processor_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessorPipelineProcessor"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessorPipelineProcessor"]]], jsii.get(self, "processorInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7806968562473c05d4ffe93a768a3346824d04988202aa61545a92f0982ad8d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d374b7006c3323b9b09fb48ebbbbef157f516a07a983abb6c432e8e241a32bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6567a4a9332609c28ba038d6ac7160a9db29d7ef50aef5e83569354316f60cf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__885d2ba2bf755a7bfe862646caa1bb6c9e9103336f5c79b14196f0614b54926a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogsCustomPipelineProcessorPipeline]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipeline], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipeline],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43017ce50e3363c967e33fb0954a37f52655b63461b5e34b7b39c68afd5ea964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "arithmetic_processor": "arithmeticProcessor",
        "attribute_remapper": "attributeRemapper",
        "category_processor": "categoryProcessor",
        "date_remapper": "dateRemapper",
        "geo_ip_parser": "geoIpParser",
        "grok_parser": "grokParser",
        "lookup_processor": "lookupProcessor",
        "message_remapper": "messageRemapper",
        "reference_table_lookup_processor": "referenceTableLookupProcessor",
        "service_remapper": "serviceRemapper",
        "span_id_remapper": "spanIdRemapper",
        "status_remapper": "statusRemapper",
        "string_builder_processor": "stringBuilderProcessor",
        "trace_id_remapper": "traceIdRemapper",
        "url_parser": "urlParser",
        "user_agent_parser": "userAgentParser",
    },
)
class LogsCustomPipelineProcessorPipelineProcessor:
    def __init__(
        self,
        *,
        arithmetic_processor: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        attribute_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        category_processor: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        date_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorDateRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        geo_ip_parser: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorGeoIpParser", typing.Dict[builtins.str, typing.Any]]] = None,
        grok_parser: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorGrokParser", typing.Dict[builtins.str, typing.Any]]] = None,
        lookup_processor: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorLookupProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        message_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorMessageRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        reference_table_lookup_processor: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        service_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorServiceRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        span_id_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        status_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorStatusRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        string_builder_processor: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor", typing.Dict[builtins.str, typing.Any]]] = None,
        trace_id_remapper: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper", typing.Dict[builtins.str, typing.Any]]] = None,
        url_parser: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorUrlParser", typing.Dict[builtins.str, typing.Any]]] = None,
        user_agent_parser: typing.Optional[typing.Union["LogsCustomPipelineProcessorPipelineProcessorUserAgentParser", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param arithmetic_processor: arithmetic_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#arithmetic_processor LogsCustomPipeline#arithmetic_processor}
        :param attribute_remapper: attribute_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#attribute_remapper LogsCustomPipeline#attribute_remapper}
        :param category_processor: category_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#category_processor LogsCustomPipeline#category_processor}
        :param date_remapper: date_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#date_remapper LogsCustomPipeline#date_remapper}
        :param geo_ip_parser: geo_ip_parser block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#geo_ip_parser LogsCustomPipeline#geo_ip_parser}
        :param grok_parser: grok_parser block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#grok_parser LogsCustomPipeline#grok_parser}
        :param lookup_processor: lookup_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_processor LogsCustomPipeline#lookup_processor}
        :param message_remapper: message_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#message_remapper LogsCustomPipeline#message_remapper}
        :param reference_table_lookup_processor: reference_table_lookup_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#reference_table_lookup_processor LogsCustomPipeline#reference_table_lookup_processor}
        :param service_remapper: service_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#service_remapper LogsCustomPipeline#service_remapper}
        :param span_id_remapper: span_id_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#span_id_remapper LogsCustomPipeline#span_id_remapper}
        :param status_remapper: status_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#status_remapper LogsCustomPipeline#status_remapper}
        :param string_builder_processor: string_builder_processor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#string_builder_processor LogsCustomPipeline#string_builder_processor}
        :param trace_id_remapper: trace_id_remapper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#trace_id_remapper LogsCustomPipeline#trace_id_remapper}
        :param url_parser: url_parser block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#url_parser LogsCustomPipeline#url_parser}
        :param user_agent_parser: user_agent_parser block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#user_agent_parser LogsCustomPipeline#user_agent_parser}
        '''
        if isinstance(arithmetic_processor, dict):
            arithmetic_processor = LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor(**arithmetic_processor)
        if isinstance(attribute_remapper, dict):
            attribute_remapper = LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper(**attribute_remapper)
        if isinstance(category_processor, dict):
            category_processor = LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor(**category_processor)
        if isinstance(date_remapper, dict):
            date_remapper = LogsCustomPipelineProcessorPipelineProcessorDateRemapper(**date_remapper)
        if isinstance(geo_ip_parser, dict):
            geo_ip_parser = LogsCustomPipelineProcessorPipelineProcessorGeoIpParser(**geo_ip_parser)
        if isinstance(grok_parser, dict):
            grok_parser = LogsCustomPipelineProcessorPipelineProcessorGrokParser(**grok_parser)
        if isinstance(lookup_processor, dict):
            lookup_processor = LogsCustomPipelineProcessorPipelineProcessorLookupProcessor(**lookup_processor)
        if isinstance(message_remapper, dict):
            message_remapper = LogsCustomPipelineProcessorPipelineProcessorMessageRemapper(**message_remapper)
        if isinstance(reference_table_lookup_processor, dict):
            reference_table_lookup_processor = LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor(**reference_table_lookup_processor)
        if isinstance(service_remapper, dict):
            service_remapper = LogsCustomPipelineProcessorPipelineProcessorServiceRemapper(**service_remapper)
        if isinstance(span_id_remapper, dict):
            span_id_remapper = LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper(**span_id_remapper)
        if isinstance(status_remapper, dict):
            status_remapper = LogsCustomPipelineProcessorPipelineProcessorStatusRemapper(**status_remapper)
        if isinstance(string_builder_processor, dict):
            string_builder_processor = LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor(**string_builder_processor)
        if isinstance(trace_id_remapper, dict):
            trace_id_remapper = LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper(**trace_id_remapper)
        if isinstance(url_parser, dict):
            url_parser = LogsCustomPipelineProcessorPipelineProcessorUrlParser(**url_parser)
        if isinstance(user_agent_parser, dict):
            user_agent_parser = LogsCustomPipelineProcessorPipelineProcessorUserAgentParser(**user_agent_parser)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83117c88869ce2b934fd70d40a5887b1c9741b8b57c0121d1e8adffc857e1e6)
            check_type(argname="argument arithmetic_processor", value=arithmetic_processor, expected_type=type_hints["arithmetic_processor"])
            check_type(argname="argument attribute_remapper", value=attribute_remapper, expected_type=type_hints["attribute_remapper"])
            check_type(argname="argument category_processor", value=category_processor, expected_type=type_hints["category_processor"])
            check_type(argname="argument date_remapper", value=date_remapper, expected_type=type_hints["date_remapper"])
            check_type(argname="argument geo_ip_parser", value=geo_ip_parser, expected_type=type_hints["geo_ip_parser"])
            check_type(argname="argument grok_parser", value=grok_parser, expected_type=type_hints["grok_parser"])
            check_type(argname="argument lookup_processor", value=lookup_processor, expected_type=type_hints["lookup_processor"])
            check_type(argname="argument message_remapper", value=message_remapper, expected_type=type_hints["message_remapper"])
            check_type(argname="argument reference_table_lookup_processor", value=reference_table_lookup_processor, expected_type=type_hints["reference_table_lookup_processor"])
            check_type(argname="argument service_remapper", value=service_remapper, expected_type=type_hints["service_remapper"])
            check_type(argname="argument span_id_remapper", value=span_id_remapper, expected_type=type_hints["span_id_remapper"])
            check_type(argname="argument status_remapper", value=status_remapper, expected_type=type_hints["status_remapper"])
            check_type(argname="argument string_builder_processor", value=string_builder_processor, expected_type=type_hints["string_builder_processor"])
            check_type(argname="argument trace_id_remapper", value=trace_id_remapper, expected_type=type_hints["trace_id_remapper"])
            check_type(argname="argument url_parser", value=url_parser, expected_type=type_hints["url_parser"])
            check_type(argname="argument user_agent_parser", value=user_agent_parser, expected_type=type_hints["user_agent_parser"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arithmetic_processor is not None:
            self._values["arithmetic_processor"] = arithmetic_processor
        if attribute_remapper is not None:
            self._values["attribute_remapper"] = attribute_remapper
        if category_processor is not None:
            self._values["category_processor"] = category_processor
        if date_remapper is not None:
            self._values["date_remapper"] = date_remapper
        if geo_ip_parser is not None:
            self._values["geo_ip_parser"] = geo_ip_parser
        if grok_parser is not None:
            self._values["grok_parser"] = grok_parser
        if lookup_processor is not None:
            self._values["lookup_processor"] = lookup_processor
        if message_remapper is not None:
            self._values["message_remapper"] = message_remapper
        if reference_table_lookup_processor is not None:
            self._values["reference_table_lookup_processor"] = reference_table_lookup_processor
        if service_remapper is not None:
            self._values["service_remapper"] = service_remapper
        if span_id_remapper is not None:
            self._values["span_id_remapper"] = span_id_remapper
        if status_remapper is not None:
            self._values["status_remapper"] = status_remapper
        if string_builder_processor is not None:
            self._values["string_builder_processor"] = string_builder_processor
        if trace_id_remapper is not None:
            self._values["trace_id_remapper"] = trace_id_remapper
        if url_parser is not None:
            self._values["url_parser"] = url_parser
        if user_agent_parser is not None:
            self._values["user_agent_parser"] = user_agent_parser

    @builtins.property
    def arithmetic_processor(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor"]:
        '''arithmetic_processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#arithmetic_processor LogsCustomPipeline#arithmetic_processor}
        '''
        result = self._values.get("arithmetic_processor")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor"], result)

    @builtins.property
    def attribute_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper"]:
        '''attribute_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#attribute_remapper LogsCustomPipeline#attribute_remapper}
        '''
        result = self._values.get("attribute_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper"], result)

    @builtins.property
    def category_processor(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor"]:
        '''category_processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#category_processor LogsCustomPipeline#category_processor}
        '''
        result = self._values.get("category_processor")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor"], result)

    @builtins.property
    def date_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorDateRemapper"]:
        '''date_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#date_remapper LogsCustomPipeline#date_remapper}
        '''
        result = self._values.get("date_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorDateRemapper"], result)

    @builtins.property
    def geo_ip_parser(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorGeoIpParser"]:
        '''geo_ip_parser block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#geo_ip_parser LogsCustomPipeline#geo_ip_parser}
        '''
        result = self._values.get("geo_ip_parser")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorGeoIpParser"], result)

    @builtins.property
    def grok_parser(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorGrokParser"]:
        '''grok_parser block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#grok_parser LogsCustomPipeline#grok_parser}
        '''
        result = self._values.get("grok_parser")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorGrokParser"], result)

    @builtins.property
    def lookup_processor(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorLookupProcessor"]:
        '''lookup_processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_processor LogsCustomPipeline#lookup_processor}
        '''
        result = self._values.get("lookup_processor")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorLookupProcessor"], result)

    @builtins.property
    def message_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorMessageRemapper"]:
        '''message_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#message_remapper LogsCustomPipeline#message_remapper}
        '''
        result = self._values.get("message_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorMessageRemapper"], result)

    @builtins.property
    def reference_table_lookup_processor(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor"]:
        '''reference_table_lookup_processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#reference_table_lookup_processor LogsCustomPipeline#reference_table_lookup_processor}
        '''
        result = self._values.get("reference_table_lookup_processor")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor"], result)

    @builtins.property
    def service_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorServiceRemapper"]:
        '''service_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#service_remapper LogsCustomPipeline#service_remapper}
        '''
        result = self._values.get("service_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorServiceRemapper"], result)

    @builtins.property
    def span_id_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper"]:
        '''span_id_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#span_id_remapper LogsCustomPipeline#span_id_remapper}
        '''
        result = self._values.get("span_id_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper"], result)

    @builtins.property
    def status_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorStatusRemapper"]:
        '''status_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#status_remapper LogsCustomPipeline#status_remapper}
        '''
        result = self._values.get("status_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorStatusRemapper"], result)

    @builtins.property
    def string_builder_processor(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor"]:
        '''string_builder_processor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#string_builder_processor LogsCustomPipeline#string_builder_processor}
        '''
        result = self._values.get("string_builder_processor")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor"], result)

    @builtins.property
    def trace_id_remapper(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper"]:
        '''trace_id_remapper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#trace_id_remapper LogsCustomPipeline#trace_id_remapper}
        '''
        result = self._values.get("trace_id_remapper")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper"], result)

    @builtins.property
    def url_parser(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorUrlParser"]:
        '''url_parser block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#url_parser LogsCustomPipeline#url_parser}
        '''
        result = self._values.get("url_parser")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorUrlParser"], result)

    @builtins.property
    def user_agent_parser(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorUserAgentParser"]:
        '''user_agent_parser block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#user_agent_parser LogsCustomPipeline#user_agent_parser}
        '''
        result = self._values.get("user_agent_parser")
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorUserAgentParser"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "expression": "expression",
        "target": "target",
        "is_enabled": "isEnabled",
        "is_replace_missing": "isReplaceMissing",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor:
    def __init__(
        self,
        *,
        expression: builtins.str,
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_replace_missing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Arithmetic operation between one or more log attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#expression LogsCustomPipeline#expression}
        :param target: Name of the attribute that contains the result of the arithmetic operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: Boolean value to enable your pipeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param is_replace_missing: If true, it replaces all missing attributes of expression by 0, false skips the operation if an attribute is missing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_replace_missing LogsCustomPipeline#is_replace_missing}
        :param name: Your pipeline name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6472717b34fe07b99b374305a50cc0a4b561c162542c565e3653c0a4e5840c7)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument is_replace_missing", value=is_replace_missing, expected_type=type_hints["is_replace_missing"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
            "target": target,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if is_replace_missing is not None:
            self._values["is_replace_missing"] = is_replace_missing
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def expression(self) -> builtins.str:
        '''Arithmetic operation between one or more log attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#expression LogsCustomPipeline#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the attribute that contains the result of the arithmetic operation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean value to enable your pipeline.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_replace_missing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, it replaces all missing attributes of expression by 0, false skips the operation if an attribute is missing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_replace_missing LogsCustomPipeline#is_replace_missing}
        '''
        result = self._values.get("is_replace_missing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Your pipeline name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f283ecb20b5a149937f868c7f2f375034a4bc0c24fcac52b8543fe9df8ba010d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetIsReplaceMissing")
    def reset_is_replace_missing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsReplaceMissing", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isReplaceMissingInput")
    def is_replace_missing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isReplaceMissingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7eb6bbf476a698e8f021905fc46b58b4485fce133dbe61f2d38e21f7cefaca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8357ed3d28ad8122166261d37ba94008ff0a74b716afdf7b25828adb68c65b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isReplaceMissing")
    def is_replace_missing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isReplaceMissing"))

    @is_replace_missing.setter
    def is_replace_missing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f49edd1949b4d82e3d8e9749e32da84f06cdfa957903f0468daa01b61dcc1ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isReplaceMissing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da29c41c99a85b4884ca7ebc8f2aaa017bca1cd40ac207fa022d72a0483253d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a40b3e07dfdef04cad1318d6109a6d90b441911f758ae220630f10c07d6d51c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21a444dbd31a0c39912d9adf00d6030a297929a85fb012e64947381586743a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper",
    jsii_struct_bases=[],
    name_mapping={
        "sources": "sources",
        "source_type": "sourceType",
        "target": "target",
        "target_type": "targetType",
        "is_enabled": "isEnabled",
        "name": "name",
        "override_on_conflict": "overrideOnConflict",
        "preserve_source": "preserveSource",
        "target_format": "targetFormat",
    },
)
class LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        source_type: builtins.str,
        target: builtins.str,
        target_type: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        override_on_conflict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preserve_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes or tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param source_type: Defines where the sources are from (log ``attribute`` or ``tag``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source_type LogsCustomPipeline#source_type}
        :param target: Final attribute or tag name to remap the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param target_type: Defines if the target is a log ``attribute`` or ``tag``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target_type LogsCustomPipeline#target_type}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        :param override_on_conflict: Override the target element if already set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#override_on_conflict LogsCustomPipeline#override_on_conflict}
        :param preserve_source: Remove or preserve the remapped source element. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#preserve_source LogsCustomPipeline#preserve_source}
        :param target_format: If the ``target_type`` of the remapper is ``attribute``, try to cast the value to a new specific type. If the cast is not possible, the original type is kept. ``string``, ``integer``, or ``double`` are the possible types. If the ``target_type`` is ``tag``, this parameter may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target_format LogsCustomPipeline#target_format}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d539d2cbacbac8393e4c539481675119eaaaf6e04b0ff8a92ba4db6b783e1d)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument override_on_conflict", value=override_on_conflict, expected_type=type_hints["override_on_conflict"])
            check_type(argname="argument preserve_source", value=preserve_source, expected_type=type_hints["preserve_source"])
            check_type(argname="argument target_format", value=target_format, expected_type=type_hints["target_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
            "source_type": source_type,
            "target": target,
            "target_type": target_type,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name
        if override_on_conflict is not None:
            self._values["override_on_conflict"] = override_on_conflict
        if preserve_source is not None:
            self._values["preserve_source"] = preserve_source
        if target_format is not None:
            self._values["target_format"] = target_format

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes or tags.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def source_type(self) -> builtins.str:
        '''Defines where the sources are from (log ``attribute`` or ``tag``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source_type LogsCustomPipeline#source_type}
        '''
        result = self._values.get("source_type")
        assert result is not None, "Required property 'source_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Final attribute or tag name to remap the sources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_type(self) -> builtins.str:
        '''Defines if the target is a log ``attribute`` or ``tag``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target_type LogsCustomPipeline#target_type}
        '''
        result = self._values.get("target_type")
        assert result is not None, "Required property 'target_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def override_on_conflict(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Override the target element if already set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#override_on_conflict LogsCustomPipeline#override_on_conflict}
        '''
        result = self._values.get("override_on_conflict")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def preserve_source(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Remove or preserve the remapped source element.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#preserve_source LogsCustomPipeline#preserve_source}
        '''
        result = self._values.get("preserve_source")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def target_format(self) -> typing.Optional[builtins.str]:
        '''If the ``target_type`` of the remapper is ``attribute``, try to cast the value to a new specific type.

        If the cast is not possible, the original type is kept. ``string``, ``integer``, or ``double`` are the possible types. If the ``target_type`` is ``tag``, this parameter may not be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target_format LogsCustomPipeline#target_format}
        '''
        result = self._values.get("target_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorAttributeRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorAttributeRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7fb7f22bb8eb4c62ecc57660f085b8691183cbfe7092360f1a2fd5adcf45cff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOverrideOnConflict")
    def reset_override_on_conflict(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideOnConflict", []))

    @jsii.member(jsii_name="resetPreserveSource")
    def reset_preserve_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreserveSource", []))

    @jsii.member(jsii_name="resetTargetFormat")
    def reset_target_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetFormat", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideOnConflictInput")
    def override_on_conflict_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overrideOnConflictInput"))

    @builtins.property
    @jsii.member(jsii_name="preserveSourceInput")
    def preserve_source_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preserveSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTypeInput")
    def source_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetFormatInput")
    def target_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="targetTypeInput")
    def target_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1c6d8bc29d8cb5802fcb1b502957dc5835312edf572f8f00016a13d9d0c633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c1d715b663f8f421b4e9de10da4800fdc51ba7232e65276e9c829d7a55a5fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overrideOnConflict")
    def override_on_conflict(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overrideOnConflict"))

    @override_on_conflict.setter
    def override_on_conflict(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__535f72703289ed32dd81ed17aef9cb97c83eb9a6357cca5ac4a736b441b7c474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideOnConflict", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preserveSource")
    def preserve_source(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preserveSource"))

    @preserve_source.setter
    def preserve_source(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e1ed42fed49b84c4c63228cfc111974f6c42c8b69a7fc90d29a7ea51e10b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f2c0c008260bcd9300517f447f019f8877fd1f0a1a030af85462e21f5b73e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @source_type.setter
    def source_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07016dff02666040f68fa7137ba902d199188e7a6f8c328a1c61df309113ee78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a2ff35f1fe0187bb888bab69e296aeedfa479ad827e4cff7133562fc90eff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetFormat")
    def target_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetFormat"))

    @target_format.setter
    def target_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f0123a1aba9cf290c62d68cf7e3c20dc7679bb0c52a6e735674625378a5f41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetType"))

    @target_type.setter
    def target_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a6d6263afa101c14ed5cbd46366aab8e5e6c364bbca85cafcdc9fb26349705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ad7f3565fa6745c85275371be031c48e80a81b41796942969110a408e10834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "target": "target",
        "is_enabled": "isEnabled",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor:
    def __init__(
        self,
        *,
        category: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory", typing.Dict[builtins.str, typing.Any]]]],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: category block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#category LogsCustomPipeline#category}
        :param target: Name of the target attribute whose value is defined by the matching category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076fb5080c0ff6d46a7c2eeb2b2621810e1faaeb6376047c608bf0e5296dc6be)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
            "target": target,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def category(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory"]]:
        '''category block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#category LogsCustomPipeline#category}
        '''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory"]], result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the target attribute whose value is defined by the matching category.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the category.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter", "name": "name"},
)
class LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory:
    def __init__(
        self,
        *,
        filter: typing.Union["LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
    ) -> None:
        '''
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#filter LogsCustomPipeline#filter}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}.
        '''
        if isinstance(filter, dict):
            filter = LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc9895323a13f8534f5a6c88677c9a0443752669b5be7e87038cfc163693e44)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
            "name": name,
        }

    @builtins.property
    def filter(
        self,
    ) -> "LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter":
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#filter LogsCustomPipeline#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter",
    jsii_struct_bases=[],
    name_mapping={"query": "query"},
)
class LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter:
    def __init__(self, *, query: builtins.str) -> None:
        '''
        :param query: Filter criteria of the category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#query LogsCustomPipeline#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a13698893fe66fb74b24f8c9e87e033fdb4d9dccbc9f652b65ffa470489fe1c6)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }

    @builtins.property
    def query(self) -> builtins.str:
        '''Filter criteria of the category.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#query LogsCustomPipeline#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f0d61f3b6d5d6cca479922cb795b7e6df31fd63a8497d7c6d3c0fd0fc4fac5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efbb32a204049320393b36db20c0e575d60b8ef87003387544a0c13198c902c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8106f01b8c8752874e951b2033615285c36c848207c157649232a91fa3f53b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__369c5f1a8fb47aeb844b8f644b4562ae697623d3dde9a9e456428f9a481380b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515d5afdbd7591b6bc85c71e871ad305dea29d50a89ed0e976062f18acf8d8a9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063059981a7fa5190a7261aada3e2dfef7da894617a490293cfd85f3d3a6068d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06260f19d8e656d0be030994c7b3b33fa758dc218434e6f2a4d75e0c7943e041)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afa117767a307a6a1b07c71ae43072caff9aaba70f7df7b7ed84ffc79b649071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b5392c5bd341247769499a9e7e53bbcba58afcb82b0223caa23976f41c9bea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0277f76d899ef21cb20df677be604d7213b3675522f1b5ffa51bf64d56282cb0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFilter")
    def put_filter(self, *, query: builtins.str) -> None:
        '''
        :param query: Filter criteria of the category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#query LogsCustomPipeline#query}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter(
            query=query
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(
        self,
    ) -> LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilterOutputReference:
        return typing.cast(LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilterOutputReference, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de7655e0236fd36918269e52d89e0804362e42e2ebb6488b37e6008d9d3a3d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45fa44f491e4caffbeababbaefef61b56a59b8d70b2cd0c7828328f5fb61a819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24a289b3549e1507a208815d78cc55b8ee9a72253af7cf2154ea1e0bf9870158)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCategory")
    def put_category(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8abdd4eb88293c83a19d79c17e85b5551ee7a26d8ab3ad8c8d5e5165b61135e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCategory", [value]))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(
        self,
    ) -> LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryList:
        return typing.cast(LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryList, jsii.get(self, "category"))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory]]], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da14b1e08bc429a23b1a95a27e3f35c0d346e9c928a9d73b250a53f749046f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d531b7c6070d9212f4fc9992da153e37e0b8a33873adda02b794caca028e102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38d87917d2aae60c0fee2440a0ebd8d7e6658c0f2ae3c4e1e2a2cc65c0295649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c9dd10cccc89123b3b3be3b58d9e649ae1f8c6a2d92021fad088715749f53f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorDateRemapper",
    jsii_struct_bases=[],
    name_mapping={"sources": "sources", "is_enabled": "isEnabled", "name": "name"},
)
class LogsCustomPipelineProcessorPipelineProcessorDateRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b2235a8cad9f7a25804166e40896b12ce08dded8f4b0f15dfa7420679d771b)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorDateRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorDateRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorDateRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7acbcbef5e7d12234130a9370e795815b2daa833bd1b6e96b6f17c3d53d6d63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf6ae40962e22c266395fdc994c1eabdeae2ef78f4b4cbc510a5bdaacf06ead1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29a241496e3629db90cf871145655a80daf47b129f1f4a2f1a58b75f3d01327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a64e532bd00b359ed07e2de61aa88bc21d370b5f3606e3303e57f93ddd55476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorDateRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorDateRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorDateRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5151fa562074a4966b25969f273eb3018f91d38b7b7563f7af3cc75cdc265756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorGeoIpParser",
    jsii_struct_bases=[],
    name_mapping={
        "sources": "sources",
        "target": "target",
        "is_enabled": "isEnabled",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorPipelineProcessorGeoIpParser:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param target: Name of the parent attribute that contains all the extracted details from the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4572e6c6018a2575f6a25afb6b9bbe64523eb8c18dbfa8ecd8b25ae6c8bec8d6)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
            "target": target,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the parent attribute that contains all the extracted details from the sources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorGeoIpParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorGeoIpParserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorGeoIpParserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffef0025044d4c253dc10bfa441f16c99e9dafef65c9c9708f3ce41cd2984dc3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13fda2ae4e6e33ca9b76be1d5698eded3dc2e1206078f096acceac48f192a0fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbeaf680d4dc9b3c91754615dd9378f8b5f98d3617c81a67fe8a82a1269eadf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c8026849ae3630db0bb3ec43b70310c5b8e81a46e3ac5eaa15c1a34b209d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e320ba5a46d5cf013d04ec31e3b4815370c4d7bd5e4bfa65efbaa9371b6798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGeoIpParser]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGeoIpParser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGeoIpParser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49f2c8b5fc9dd07175f298f09d43a149d0da5b3f8f7f9a463f3584c8eede11a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorGrokParser",
    jsii_struct_bases=[],
    name_mapping={
        "grok": "grok",
        "source": "source",
        "is_enabled": "isEnabled",
        "name": "name",
        "samples": "samples",
    },
)
class LogsCustomPipelineProcessorPipelineProcessorGrokParser:
    def __init__(
        self,
        *,
        grok: typing.Union["LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok", typing.Dict[builtins.str, typing.Any]],
        source: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        samples: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param grok: grok block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#grok LogsCustomPipeline#grok}
        :param source: Name of the log attribute to parse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        :param samples: List of sample logs for this parser. It can save up to 5 samples. Each sample takes up to 5000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#samples LogsCustomPipeline#samples}
        '''
        if isinstance(grok, dict):
            grok = LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok(**grok)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1ca36764f078570fc9d9d82c08e79eca9c053a3fef8eee47babf3a9519e9ea)
            check_type(argname="argument grok", value=grok, expected_type=type_hints["grok"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument samples", value=samples, expected_type=type_hints["samples"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "grok": grok,
            "source": source,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name
        if samples is not None:
            self._values["samples"] = samples

    @builtins.property
    def grok(self) -> "LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok":
        '''grok block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#grok LogsCustomPipeline#grok}
        '''
        result = self._values.get("grok")
        assert result is not None, "Required property 'grok' is missing"
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok", result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Name of the log attribute to parse.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def samples(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of sample logs for this parser.

        It can save up to 5 samples. Each sample takes up to 5000 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#samples LogsCustomPipeline#samples}
        '''
        result = self._values.get("samples")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorGrokParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok",
    jsii_struct_bases=[],
    name_mapping={"match_rules": "matchRules", "support_rules": "supportRules"},
)
class LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok:
    def __init__(
        self,
        *,
        match_rules: builtins.str,
        support_rules: builtins.str,
    ) -> None:
        '''
        :param match_rules: Match rules for your grok parser. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#match_rules LogsCustomPipeline#match_rules}
        :param support_rules: Support rules for your grok parser. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#support_rules LogsCustomPipeline#support_rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72aed5e4aa7c818bf6d16ff4d6a8bb1861758557a40acb02485665e235f39f6)
            check_type(argname="argument match_rules", value=match_rules, expected_type=type_hints["match_rules"])
            check_type(argname="argument support_rules", value=support_rules, expected_type=type_hints["support_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "match_rules": match_rules,
            "support_rules": support_rules,
        }

    @builtins.property
    def match_rules(self) -> builtins.str:
        '''Match rules for your grok parser.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#match_rules LogsCustomPipeline#match_rules}
        '''
        result = self._values.get("match_rules")
        assert result is not None, "Required property 'match_rules' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def support_rules(self) -> builtins.str:
        '''Support rules for your grok parser.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#support_rules LogsCustomPipeline#support_rules}
        '''
        result = self._values.get("support_rules")
        assert result is not None, "Required property 'support_rules' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorGrokParserGrokOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorGrokParserGrokOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b799c631036253d55bba52a8fd304c3911099bea02a3a522a46640d9a2930db3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="matchRulesInput")
    def match_rules_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="supportRulesInput")
    def support_rules_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="matchRules")
    def match_rules(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchRules"))

    @match_rules.setter
    def match_rules(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e811a3b0687ee44dffa3ea6622f53daefa55052531e29e450010622d4901f5e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportRules")
    def support_rules(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportRules"))

    @support_rules.setter
    def support_rules(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0edf07761236311f708220a6b28ea8d224a6db28b3dbe6f05fe36c4ae67e53aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca421dc9b7636fc178ad5502e27ddebe6b1d776b72f0e79fcca43b5cc897711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorPipelineProcessorGrokParserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorGrokParserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25398f9fa05388573e46e16b87d5729d603f85fbbbfacf3b0cdb6e55c465b593)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrok")
    def put_grok(
        self,
        *,
        match_rules: builtins.str,
        support_rules: builtins.str,
    ) -> None:
        '''
        :param match_rules: Match rules for your grok parser. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#match_rules LogsCustomPipeline#match_rules}
        :param support_rules: Support rules for your grok parser. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#support_rules LogsCustomPipeline#support_rules}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok(
            match_rules=match_rules, support_rules=support_rules
        )

        return typing.cast(None, jsii.invoke(self, "putGrok", [value]))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSamples")
    def reset_samples(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamples", []))

    @builtins.property
    @jsii.member(jsii_name="grok")
    def grok(
        self,
    ) -> LogsCustomPipelineProcessorPipelineProcessorGrokParserGrokOutputReference:
        return typing.cast(LogsCustomPipelineProcessorPipelineProcessorGrokParserGrokOutputReference, jsii.get(self, "grok"))

    @builtins.property
    @jsii.member(jsii_name="grokInput")
    def grok_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok], jsii.get(self, "grokInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="samplesInput")
    def samples_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "samplesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__337386346c5d2ed8899fb819653ee537efea25b006451178dfd18e4643ec2271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff863364e0701e6efe1cf91e39e811b64e378286943d84996811beff549c498e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samples")
    def samples(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "samples"))

    @samples.setter
    def samples(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9af886131d25c8af29e819d0f910143b44bceef9bb7701eedfee23447f9867e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samples", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fa71496f27252092b0f38dfefbcbdd9efdd0cc8a57cb291a8fb50ce017cd6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGrokParser]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGrokParser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGrokParser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb17df5c567b03eeeba82508f2a3b87f0364b3478cddddf4695a138c0a6eec71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorPipelineProcessorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25f21b612c423d6f005236d9e72cba728052ea99d04b117f8046829725b2ef12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LogsCustomPipelineProcessorPipelineProcessorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e598cb0b50c84b301977d65ba7090f9009247bfdc0fefd468281b81d541547ca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c5c49a6bbc122f54f652659b35e23ac10380ae2c229f899e1ad4996077ae5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c27d8e8c94bb2dd16e3ec1e9bc976028b1c1759859cc81d7f40fcbad9c5e8a32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a13eacae46ed4ad05e8edfbf3ec8f788024599645d7dec3811c30f1ec0b61f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineProcessor]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineProcessor]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineProcessor]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28251a1051edea6a981c5a76f79b063aedf358c4e9e258b0ee4fa2a6422fd939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorLookupProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "lookup_table": "lookupTable",
        "source": "source",
        "target": "target",
        "default_lookup": "defaultLookup",
        "is_enabled": "isEnabled",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorPipelineProcessorLookupProcessor:
    def __init__(
        self,
        *,
        lookup_table: typing.Sequence[builtins.str],
        source: builtins.str,
        target: builtins.str,
        default_lookup: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lookup_table: List of entries of the lookup table using ``key,value`` format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_table LogsCustomPipeline#lookup_table}
        :param source: Name of the source attribute used to do the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        :param target: Name of the attribute that contains the result of the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param default_lookup: Default lookup value to use if there is no entry in the lookup table for the value of the source attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#default_lookup LogsCustomPipeline#default_lookup}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3c59f9e021d4bef41e8fc5a3b5cd9fb80953234adac9d21c60730d950c15f2)
            check_type(argname="argument lookup_table", value=lookup_table, expected_type=type_hints["lookup_table"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument default_lookup", value=default_lookup, expected_type=type_hints["default_lookup"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lookup_table": lookup_table,
            "source": source,
            "target": target,
        }
        if default_lookup is not None:
            self._values["default_lookup"] = default_lookup
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def lookup_table(self) -> typing.List[builtins.str]:
        '''List of entries of the lookup table using ``key,value`` format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_table LogsCustomPipeline#lookup_table}
        '''
        result = self._values.get("lookup_table")
        assert result is not None, "Required property 'lookup_table' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Name of the source attribute used to do the lookup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the attribute that contains the result of the lookup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_lookup(self) -> typing.Optional[builtins.str]:
        '''Default lookup value to use if there is no entry in the lookup table for the value of the source attribute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#default_lookup LogsCustomPipeline#default_lookup}
        '''
        result = self._values.get("default_lookup")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorLookupProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorLookupProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorLookupProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb5309819c5caff36fbc41283f6a86ef60b7dfae0e9cc6fa50d7544d8dcf8d1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultLookup")
    def reset_default_lookup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLookup", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="defaultLookupInput")
    def default_lookup_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultLookupInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="lookupTableInput")
    def lookup_table_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "lookupTableInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLookup")
    def default_lookup(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultLookup"))

    @default_lookup.setter
    def default_lookup(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96c25102e33dfb9fb11023bf081fb5b149cebcafb14da75824ec699e8c40362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLookup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c50c2981af53936b3a79dc6d8ea733b5bba8ecf95e7caba8753f6fee019395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lookupTable")
    def lookup_table(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "lookupTable"))

    @lookup_table.setter
    def lookup_table(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ea0e35e6132f539013ae274d98ddd5e7ccddf5db8d8011f5c558f39d048261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lookupTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d92abde71087c09dcd185ff2e16218b9a7f1731fe016f88bf9f0c76c2bcdb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4396fb92870d3bfdae1a6cea8df8b50c2b2fd838deb480c738eaf0f5f25ba5c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cebf218507c082e847820b2ad012935895fad5c2d5a95ce010d847b5a228015b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorLookupProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorLookupProcessor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorLookupProcessor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5954ec0d5fd1ee0f77cfab6b6226479a600f251263c4db91ea0f0cffaf41b460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorMessageRemapper",
    jsii_struct_bases=[],
    name_mapping={"sources": "sources", "is_enabled": "isEnabled", "name": "name"},
)
class LogsCustomPipelineProcessorPipelineProcessorMessageRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4270b6ad21cf9cb28787964fd4bebca907b8e65f52997e484a894458a58158a)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorMessageRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorMessageRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorMessageRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26a9b1eee95ea57aee6363a12989cc08d32fe436eacb16bd056846a12d554576)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc5312521dd1858b4a299f39bd8beaf2aaf88c06a0a6b3d6e852201962369e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a987e91eea81218c73a076b5e3db9aa93716d543fdca33c6442d5ae305380a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1242a9b97128abd020c03e76be3d03f95f67a2aa3557dd50f4aa66aac1086f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorMessageRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorMessageRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorMessageRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01ca0721cddaa0ac57201375f9965a7b319cd70a4b82233e78b782c164ca297)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LogsCustomPipelineProcessorPipelineProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f7aab94433fc9bb5ce47b7f0b07b6aa544a847a14cb50cd054eadfb2317f84a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putArithmeticProcessor")
    def put_arithmetic_processor(
        self,
        *,
        expression: builtins.str,
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_replace_missing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expression: Arithmetic operation between one or more log attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#expression LogsCustomPipeline#expression}
        :param target: Name of the attribute that contains the result of the arithmetic operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: Boolean value to enable your pipeline. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param is_replace_missing: If true, it replaces all missing attributes of expression by 0, false skips the operation if an attribute is missing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_replace_missing LogsCustomPipeline#is_replace_missing}
        :param name: Your pipeline name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor(
            expression=expression,
            target=target,
            is_enabled=is_enabled,
            is_replace_missing=is_replace_missing,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putArithmeticProcessor", [value]))

    @jsii.member(jsii_name="putAttributeRemapper")
    def put_attribute_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        source_type: builtins.str,
        target: builtins.str,
        target_type: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        override_on_conflict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        preserve_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes or tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param source_type: Defines where the sources are from (log ``attribute`` or ``tag``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source_type LogsCustomPipeline#source_type}
        :param target: Final attribute or tag name to remap the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param target_type: Defines if the target is a log ``attribute`` or ``tag``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target_type LogsCustomPipeline#target_type}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        :param override_on_conflict: Override the target element if already set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#override_on_conflict LogsCustomPipeline#override_on_conflict}
        :param preserve_source: Remove or preserve the remapped source element. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#preserve_source LogsCustomPipeline#preserve_source}
        :param target_format: If the ``target_type`` of the remapper is ``attribute``, try to cast the value to a new specific type. If the cast is not possible, the original type is kept. ``string``, ``integer``, or ``double`` are the possible types. If the ``target_type`` is ``tag``, this parameter may not be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target_format LogsCustomPipeline#target_format}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper(
            sources=sources,
            source_type=source_type,
            target=target,
            target_type=target_type,
            is_enabled=is_enabled,
            name=name,
            override_on_conflict=override_on_conflict,
            preserve_source=preserve_source,
            target_format=target_format,
        )

        return typing.cast(None, jsii.invoke(self, "putAttributeRemapper", [value]))

    @jsii.member(jsii_name="putCategoryProcessor")
    def put_category_processor(
        self,
        *,
        category: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory, typing.Dict[builtins.str, typing.Any]]]],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: category block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#category LogsCustomPipeline#category}
        :param target: Name of the target attribute whose value is defined by the matching category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the category. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor(
            category=category, target=target, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putCategoryProcessor", [value]))

    @jsii.member(jsii_name="putDateRemapper")
    def put_date_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorDateRemapper(
            sources=sources, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putDateRemapper", [value]))

    @jsii.member(jsii_name="putGeoIpParser")
    def put_geo_ip_parser(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param target: Name of the parent attribute that contains all the extracted details from the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorGeoIpParser(
            sources=sources, target=target, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putGeoIpParser", [value]))

    @jsii.member(jsii_name="putGrokParser")
    def put_grok_parser(
        self,
        *,
        grok: typing.Union[LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok, typing.Dict[builtins.str, typing.Any]],
        source: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        samples: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param grok: grok block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#grok LogsCustomPipeline#grok}
        :param source: Name of the log attribute to parse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        :param samples: List of sample logs for this parser. It can save up to 5 samples. Each sample takes up to 5000 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#samples LogsCustomPipeline#samples}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorGrokParser(
            grok=grok, source=source, is_enabled=is_enabled, name=name, samples=samples
        )

        return typing.cast(None, jsii.invoke(self, "putGrokParser", [value]))

    @jsii.member(jsii_name="putLookupProcessor")
    def put_lookup_processor(
        self,
        *,
        lookup_table: typing.Sequence[builtins.str],
        source: builtins.str,
        target: builtins.str,
        default_lookup: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lookup_table: List of entries of the lookup table using ``key,value`` format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_table LogsCustomPipeline#lookup_table}
        :param source: Name of the source attribute used to do the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        :param target: Name of the attribute that contains the result of the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param default_lookup: Default lookup value to use if there is no entry in the lookup table for the value of the source attribute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#default_lookup LogsCustomPipeline#default_lookup}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorLookupProcessor(
            lookup_table=lookup_table,
            source=source,
            target=target,
            default_lookup=default_lookup,
            is_enabled=is_enabled,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putLookupProcessor", [value]))

    @jsii.member(jsii_name="putMessageRemapper")
    def put_message_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorMessageRemapper(
            sources=sources, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putMessageRemapper", [value]))

    @jsii.member(jsii_name="putReferenceTableLookupProcessor")
    def put_reference_table_lookup_processor(
        self,
        *,
        lookup_enrichment_table: builtins.str,
        source: builtins.str,
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lookup_enrichment_table: Name of the Reference Table for the source attribute and their associated target attribute values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_enrichment_table LogsCustomPipeline#lookup_enrichment_table}
        :param source: Name of the source attribute used to do the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        :param target: Name of the attribute that contains the result of the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor(
            lookup_enrichment_table=lookup_enrichment_table,
            source=source,
            target=target,
            is_enabled=is_enabled,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putReferenceTableLookupProcessor", [value]))

    @jsii.member(jsii_name="putServiceRemapper")
    def put_service_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorServiceRemapper(
            sources=sources, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putServiceRemapper", [value]))

    @jsii.member(jsii_name="putSpanIdRemapper")
    def put_span_id_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper(
            sources=sources, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putSpanIdRemapper", [value]))

    @jsii.member(jsii_name="putStatusRemapper")
    def put_status_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorStatusRemapper(
            sources=sources, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putStatusRemapper", [value]))

    @jsii.member(jsii_name="putStringBuilderProcessor")
    def put_string_builder_processor(
        self,
        *,
        target: builtins.str,
        template: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_replace_missing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: The name of the attribute that contains the result of the template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param template: The formula with one or more attributes and raw text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#template LogsCustomPipeline#template}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param is_replace_missing: If it replaces all missing attributes of template by an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_replace_missing LogsCustomPipeline#is_replace_missing}
        :param name: The name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor(
            target=target,
            template=template,
            is_enabled=is_enabled,
            is_replace_missing=is_replace_missing,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putStringBuilderProcessor", [value]))

    @jsii.member(jsii_name="putTraceIdRemapper")
    def put_trace_id_remapper(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper(
            sources=sources, is_enabled=is_enabled, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putTraceIdRemapper", [value]))

    @jsii.member(jsii_name="putUrlParser")
    def put_url_parser(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        normalize_ending_slashes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param target: Name of the parent attribute that contains all the extracted details from the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        :param normalize_ending_slashes: Normalize the ending slashes or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#normalize_ending_slashes LogsCustomPipeline#normalize_ending_slashes}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorUrlParser(
            sources=sources,
            target=target,
            is_enabled=is_enabled,
            name=name,
            normalize_ending_slashes=normalize_ending_slashes,
        )

        return typing.cast(None, jsii.invoke(self, "putUrlParser", [value]))

    @jsii.member(jsii_name="putUserAgentParser")
    def put_user_agent_parser(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_encoded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param target: Name of the parent attribute that contains all the extracted details from the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param is_encoded: If the source attribute is URL encoded or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_encoded LogsCustomPipeline#is_encoded}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        value = LogsCustomPipelineProcessorPipelineProcessorUserAgentParser(
            sources=sources,
            target=target,
            is_enabled=is_enabled,
            is_encoded=is_encoded,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putUserAgentParser", [value]))

    @jsii.member(jsii_name="resetArithmeticProcessor")
    def reset_arithmetic_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArithmeticProcessor", []))

    @jsii.member(jsii_name="resetAttributeRemapper")
    def reset_attribute_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeRemapper", []))

    @jsii.member(jsii_name="resetCategoryProcessor")
    def reset_category_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategoryProcessor", []))

    @jsii.member(jsii_name="resetDateRemapper")
    def reset_date_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateRemapper", []))

    @jsii.member(jsii_name="resetGeoIpParser")
    def reset_geo_ip_parser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoIpParser", []))

    @jsii.member(jsii_name="resetGrokParser")
    def reset_grok_parser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrokParser", []))

    @jsii.member(jsii_name="resetLookupProcessor")
    def reset_lookup_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLookupProcessor", []))

    @jsii.member(jsii_name="resetMessageRemapper")
    def reset_message_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageRemapper", []))

    @jsii.member(jsii_name="resetReferenceTableLookupProcessor")
    def reset_reference_table_lookup_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferenceTableLookupProcessor", []))

    @jsii.member(jsii_name="resetServiceRemapper")
    def reset_service_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceRemapper", []))

    @jsii.member(jsii_name="resetSpanIdRemapper")
    def reset_span_id_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpanIdRemapper", []))

    @jsii.member(jsii_name="resetStatusRemapper")
    def reset_status_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusRemapper", []))

    @jsii.member(jsii_name="resetStringBuilderProcessor")
    def reset_string_builder_processor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringBuilderProcessor", []))

    @jsii.member(jsii_name="resetTraceIdRemapper")
    def reset_trace_id_remapper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTraceIdRemapper", []))

    @jsii.member(jsii_name="resetUrlParser")
    def reset_url_parser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlParser", []))

    @jsii.member(jsii_name="resetUserAgentParser")
    def reset_user_agent_parser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAgentParser", []))

    @builtins.property
    @jsii.member(jsii_name="arithmeticProcessor")
    def arithmetic_processor(
        self,
    ) -> LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessorOutputReference:
        return typing.cast(LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessorOutputReference, jsii.get(self, "arithmeticProcessor"))

    @builtins.property
    @jsii.member(jsii_name="attributeRemapper")
    def attribute_remapper(
        self,
    ) -> LogsCustomPipelineProcessorPipelineProcessorAttributeRemapperOutputReference:
        return typing.cast(LogsCustomPipelineProcessorPipelineProcessorAttributeRemapperOutputReference, jsii.get(self, "attributeRemapper"))

    @builtins.property
    @jsii.member(jsii_name="categoryProcessor")
    def category_processor(
        self,
    ) -> LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorOutputReference:
        return typing.cast(LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorOutputReference, jsii.get(self, "categoryProcessor"))

    @builtins.property
    @jsii.member(jsii_name="dateRemapper")
    def date_remapper(
        self,
    ) -> LogsCustomPipelineProcessorPipelineProcessorDateRemapperOutputReference:
        return typing.cast(LogsCustomPipelineProcessorPipelineProcessorDateRemapperOutputReference, jsii.get(self, "dateRemapper"))

    @builtins.property
    @jsii.member(jsii_name="geoIpParser")
    def geo_ip_parser(
        self,
    ) -> LogsCustomPipelineProcessorPipelineProcessorGeoIpParserOutputReference:
        return typing.cast(LogsCustomPipelineProcessorPipelineProcessorGeoIpParserOutputReference, jsii.get(self, "geoIpParser"))

    @builtins.property
    @jsii.member(jsii_name="grokParser")
    def grok_parser(
        self,
    ) -> LogsCustomPipelineProcessorPipelineProcessorGrokParserOutputReference:
        return typing.cast(LogsCustomPipelineProcessorPipelineProcessorGrokParserOutputReference, jsii.get(self, "grokParser"))

    @builtins.property
    @jsii.member(jsii_name="lookupProcessor")
    def lookup_processor(
        self,
    ) -> LogsCustomPipelineProcessorPipelineProcessorLookupProcessorOutputReference:
        return typing.cast(LogsCustomPipelineProcessorPipelineProcessorLookupProcessorOutputReference, jsii.get(self, "lookupProcessor"))

    @builtins.property
    @jsii.member(jsii_name="messageRemapper")
    def message_remapper(
        self,
    ) -> LogsCustomPipelineProcessorPipelineProcessorMessageRemapperOutputReference:
        return typing.cast(LogsCustomPipelineProcessorPipelineProcessorMessageRemapperOutputReference, jsii.get(self, "messageRemapper"))

    @builtins.property
    @jsii.member(jsii_name="referenceTableLookupProcessor")
    def reference_table_lookup_processor(
        self,
    ) -> "LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessorOutputReference":
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessorOutputReference", jsii.get(self, "referenceTableLookupProcessor"))

    @builtins.property
    @jsii.member(jsii_name="serviceRemapper")
    def service_remapper(
        self,
    ) -> "LogsCustomPipelineProcessorPipelineProcessorServiceRemapperOutputReference":
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorServiceRemapperOutputReference", jsii.get(self, "serviceRemapper"))

    @builtins.property
    @jsii.member(jsii_name="spanIdRemapper")
    def span_id_remapper(
        self,
    ) -> "LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapperOutputReference":
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapperOutputReference", jsii.get(self, "spanIdRemapper"))

    @builtins.property
    @jsii.member(jsii_name="statusRemapper")
    def status_remapper(
        self,
    ) -> "LogsCustomPipelineProcessorPipelineProcessorStatusRemapperOutputReference":
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorStatusRemapperOutputReference", jsii.get(self, "statusRemapper"))

    @builtins.property
    @jsii.member(jsii_name="stringBuilderProcessor")
    def string_builder_processor(
        self,
    ) -> "LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessorOutputReference":
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessorOutputReference", jsii.get(self, "stringBuilderProcessor"))

    @builtins.property
    @jsii.member(jsii_name="traceIdRemapper")
    def trace_id_remapper(
        self,
    ) -> "LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapperOutputReference":
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapperOutputReference", jsii.get(self, "traceIdRemapper"))

    @builtins.property
    @jsii.member(jsii_name="urlParser")
    def url_parser(
        self,
    ) -> "LogsCustomPipelineProcessorPipelineProcessorUrlParserOutputReference":
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorUrlParserOutputReference", jsii.get(self, "urlParser"))

    @builtins.property
    @jsii.member(jsii_name="userAgentParser")
    def user_agent_parser(
        self,
    ) -> "LogsCustomPipelineProcessorPipelineProcessorUserAgentParserOutputReference":
        return typing.cast("LogsCustomPipelineProcessorPipelineProcessorUserAgentParserOutputReference", jsii.get(self, "userAgentParser"))

    @builtins.property
    @jsii.member(jsii_name="arithmeticProcessorInput")
    def arithmetic_processor_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor], jsii.get(self, "arithmeticProcessorInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeRemapperInput")
    def attribute_remapper_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper], jsii.get(self, "attributeRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="categoryProcessorInput")
    def category_processor_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor], jsii.get(self, "categoryProcessorInput"))

    @builtins.property
    @jsii.member(jsii_name="dateRemapperInput")
    def date_remapper_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorDateRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorDateRemapper], jsii.get(self, "dateRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="geoIpParserInput")
    def geo_ip_parser_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGeoIpParser]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGeoIpParser], jsii.get(self, "geoIpParserInput"))

    @builtins.property
    @jsii.member(jsii_name="grokParserInput")
    def grok_parser_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGrokParser]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGrokParser], jsii.get(self, "grokParserInput"))

    @builtins.property
    @jsii.member(jsii_name="lookupProcessorInput")
    def lookup_processor_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorLookupProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorLookupProcessor], jsii.get(self, "lookupProcessorInput"))

    @builtins.property
    @jsii.member(jsii_name="messageRemapperInput")
    def message_remapper_input(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorMessageRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorMessageRemapper], jsii.get(self, "messageRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceTableLookupProcessorInput")
    def reference_table_lookup_processor_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor"], jsii.get(self, "referenceTableLookupProcessorInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRemapperInput")
    def service_remapper_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorServiceRemapper"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorServiceRemapper"], jsii.get(self, "serviceRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="spanIdRemapperInput")
    def span_id_remapper_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper"], jsii.get(self, "spanIdRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="statusRemapperInput")
    def status_remapper_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorStatusRemapper"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorStatusRemapper"], jsii.get(self, "statusRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="stringBuilderProcessorInput")
    def string_builder_processor_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor"], jsii.get(self, "stringBuilderProcessorInput"))

    @builtins.property
    @jsii.member(jsii_name="traceIdRemapperInput")
    def trace_id_remapper_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper"], jsii.get(self, "traceIdRemapperInput"))

    @builtins.property
    @jsii.member(jsii_name="urlParserInput")
    def url_parser_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorUrlParser"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorUrlParser"], jsii.get(self, "urlParserInput"))

    @builtins.property
    @jsii.member(jsii_name="userAgentParserInput")
    def user_agent_parser_input(
        self,
    ) -> typing.Optional["LogsCustomPipelineProcessorPipelineProcessorUserAgentParser"]:
        return typing.cast(typing.Optional["LogsCustomPipelineProcessorPipelineProcessorUserAgentParser"], jsii.get(self, "userAgentParserInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorPipelineProcessor]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorPipelineProcessor]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorPipelineProcessor]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a41475250a108a98b6107c10b28ca53d8a321c49139f7745fa05cb8ef8000222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "lookup_enrichment_table": "lookupEnrichmentTable",
        "source": "source",
        "target": "target",
        "is_enabled": "isEnabled",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor:
    def __init__(
        self,
        *,
        lookup_enrichment_table: builtins.str,
        source: builtins.str,
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lookup_enrichment_table: Name of the Reference Table for the source attribute and their associated target attribute values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_enrichment_table LogsCustomPipeline#lookup_enrichment_table}
        :param source: Name of the source attribute used to do the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        :param target: Name of the attribute that contains the result of the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b2a3e3d94c1fe100587b4b785b35062061dc537deb671f578f28b3c62d5ab3)
            check_type(argname="argument lookup_enrichment_table", value=lookup_enrichment_table, expected_type=type_hints["lookup_enrichment_table"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lookup_enrichment_table": lookup_enrichment_table,
            "source": source,
            "target": target,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def lookup_enrichment_table(self) -> builtins.str:
        '''Name of the Reference Table for the source attribute and their associated target attribute values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_enrichment_table LogsCustomPipeline#lookup_enrichment_table}
        '''
        result = self._values.get("lookup_enrichment_table")
        assert result is not None, "Required property 'lookup_enrichment_table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Name of the source attribute used to do the lookup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the attribute that contains the result of the lookup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e498c89cbbb82684dd902f0e8a365ef04457819b1c447554a72542c936f2461)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="lookupEnrichmentTableInput")
    def lookup_enrichment_table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lookupEnrichmentTableInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08600c73465359d979d27e7b0409f93298bb8478f3d9e94aabd2413a44dfd254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lookupEnrichmentTable")
    def lookup_enrichment_table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lookupEnrichmentTable"))

    @lookup_enrichment_table.setter
    def lookup_enrichment_table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48ef46a42695498830f4b5430f3e05702a8827a08d2b3a5935c32b05bcb57ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lookupEnrichmentTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4247c831f1be7922a8d8039c610f0a5c9f56cf2fd8f07963e30481f3bd3332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0071a45ee40a0726c3881962324ae53e1a6eb799305d56f04d14f19106ca43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6125d7e55d265bf33d9a4af0dc42f6ced97e494d4e15823fcd20cd339e00d961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d924809e3f11915542949a5514f53851273f1610defeeb11cd7cfee9b97921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorServiceRemapper",
    jsii_struct_bases=[],
    name_mapping={"sources": "sources", "is_enabled": "isEnabled", "name": "name"},
)
class LogsCustomPipelineProcessorPipelineProcessorServiceRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25be134783ad8859764727cdc99e7c71582e70dca162ffd46f3b8151dbb5b550)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorServiceRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorServiceRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorServiceRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46184a7d3db44c26d2871dadcb577ab8cbc000e156d1902685d4405467dc600f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b9f3ff658bf26822ebedb26549e0d3c10c401ae82582c3b5e815c04491dc24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d69736caaba7030b946436921c1720890e87e6f95ed60882cc76a32f9ab915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9ccf1c279cf395f7b442eb5705fd114140675bcf5f0c56ef1938f3a4ddb6a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorServiceRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorServiceRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorServiceRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98f99cd929f21d1ed8552d103f8ca266076c0424743aebd4640ca9b1e318bae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper",
    jsii_struct_bases=[],
    name_mapping={"sources": "sources", "is_enabled": "isEnabled", "name": "name"},
)
class LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6efef503278ef352103dffa64419a7a2b276cef8de49d3e655f7a5105702f8fe)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30f235cdaf9e0a09887b05eeadf7b1d1f739c6abe8d45cb959862e5c83f2e667)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd98ee54e9cf8e9a76de0c48a416559e5cab1e3a18c324e068e53e721dd2283a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__871caf0647b58a8426c4cb52a9ff76b3e10c172b0b09ed32ee13a9d86c4daa9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f478a9a08d23aeec28245a030e9bd3cc59e9bd114c47760386f86ba06dca405e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db034d82205a48aa6079e497e1f5b12df99c5f0b53b0e57c69d50aedf6b0107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorStatusRemapper",
    jsii_struct_bases=[],
    name_mapping={"sources": "sources", "is_enabled": "isEnabled", "name": "name"},
)
class LogsCustomPipelineProcessorPipelineProcessorStatusRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c0e93b59b82ff448c83d13cd0fa99f07533f4afd2c1177fa81d5e8a48a6fe4)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorStatusRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorStatusRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorStatusRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__026a173a73dfa0bb583883f7212d3b096a9232854c39027c97f8ad5d56ab51b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04845f06b4e5edcde15336684a2172280abf1e90e768c4efc67c85c8cc978cac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea1c8046d14ff4bd4084449c3d4bd396b35298274002dc5cdd735c0af30c469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4703775625873ea1d888e233acbf6cc74017d589225e93006f2a192c211097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorStatusRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorStatusRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorStatusRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9259e6bf9985ba76a6eb1ab55bd97830c9f85b38e4d071125dfad34d42608823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "template": "template",
        "is_enabled": "isEnabled",
        "is_replace_missing": "isReplaceMissing",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor:
    def __init__(
        self,
        *,
        target: builtins.str,
        template: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_replace_missing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: The name of the attribute that contains the result of the template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param template: The formula with one or more attributes and raw text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#template LogsCustomPipeline#template}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param is_replace_missing: If it replaces all missing attributes of template by an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_replace_missing LogsCustomPipeline#is_replace_missing}
        :param name: The name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e66757241bfa12eba6efebc21b0d18f44ea85a311b2fcab40dfe22cf738a70b)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument is_replace_missing", value=is_replace_missing, expected_type=type_hints["is_replace_missing"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
            "template": template,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if is_replace_missing is not None:
            self._values["is_replace_missing"] = is_replace_missing
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def target(self) -> builtins.str:
        '''The name of the attribute that contains the result of the template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template(self) -> builtins.str:
        '''The formula with one or more attributes and raw text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#template LogsCustomPipeline#template}
        '''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_replace_missing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If it replaces all missing attributes of template by an empty string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_replace_missing LogsCustomPipeline#is_replace_missing}
        '''
        result = self._values.get("is_replace_missing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cad9786c21b9c809a3eb6093b928fdd42d437c1faa52cf93336b0a30b3390386)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetIsReplaceMissing")
    def reset_is_replace_missing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsReplaceMissing", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isReplaceMissingInput")
    def is_replace_missing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isReplaceMissingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e771169fd6d80c55c6fabdd366528fb44939ee3bdbf1663f8ccb1425de98ef65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isReplaceMissing")
    def is_replace_missing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isReplaceMissing"))

    @is_replace_missing.setter
    def is_replace_missing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c77fe989fbb8f19469d162931ae06c1b32ae720e5bc9f5c88439fe7a973bc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isReplaceMissing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c35d30ec1231fb4b54405d6bc22cc6869e73791430083399475bab777e34f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c865b92d2782005e264593741228b5f03d04a71323d411fc0288e5ccce71057b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f8761540d58652544fcb7df0d26a76058951b4d08e139cc917ed5f412dd624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abdf7b6a7ad84bae39fa6f65b0e1a3bf15415c2f2da4abc936f3f8145ff4e53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper",
    jsii_struct_bases=[],
    name_mapping={"sources": "sources", "is_enabled": "isEnabled", "name": "name"},
)
class LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c78e26d1da1606a12b23c4a827f94e47662754d0f66525ba416f1aa7d555513)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__103911d48b52089ff840d432573c3c55231a49ff82e0d6db48e03f71c7412110)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5e67ea870c1335823078986ff725243e804ef2e921c857a597c28aa4d7c348)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f88e5e26161b0a612a11c0d907046c2de927ace96cee0fd7ca02bb236b5d1b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69c4d1a1e70d43aab966a834d2116aac507448cee5120055e352fcc8514a698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9139df5006abc42dc07aaa845dd823d8c0497544a6a78c4c25ff558222589d89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorUrlParser",
    jsii_struct_bases=[],
    name_mapping={
        "sources": "sources",
        "target": "target",
        "is_enabled": "isEnabled",
        "name": "name",
        "normalize_ending_slashes": "normalizeEndingSlashes",
    },
)
class LogsCustomPipelineProcessorPipelineProcessorUrlParser:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        normalize_ending_slashes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param target: Name of the parent attribute that contains all the extracted details from the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        :param normalize_ending_slashes: Normalize the ending slashes or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#normalize_ending_slashes LogsCustomPipeline#normalize_ending_slashes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6419e5c307d58be7369139a6efe254a361067d2475e2affe02845b14fc66b29a)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument normalize_ending_slashes", value=normalize_ending_slashes, expected_type=type_hints["normalize_ending_slashes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
            "target": target,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name
        if normalize_ending_slashes is not None:
            self._values["normalize_ending_slashes"] = normalize_ending_slashes

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the parent attribute that contains all the extracted details from the sources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def normalize_ending_slashes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Normalize the ending slashes or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#normalize_ending_slashes LogsCustomPipeline#normalize_ending_slashes}
        '''
        result = self._values.get("normalize_ending_slashes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorUrlParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorUrlParserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorUrlParserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__098890d600e79568f89c443ebad3cc28ea879ddf074f7e6c071c563c71f1a886)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNormalizeEndingSlashes")
    def reset_normalize_ending_slashes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNormalizeEndingSlashes", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="normalizeEndingSlashesInput")
    def normalize_ending_slashes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "normalizeEndingSlashesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532c42800696cc4589d730f8c502756fb1501be07758e660d755f52388b84bc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c039e07245397cf94d70cf96513731f36480b030ed3f58b8e9ecfa574cbc762e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="normalizeEndingSlashes")
    def normalize_ending_slashes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "normalizeEndingSlashes"))

    @normalize_ending_slashes.setter
    def normalize_ending_slashes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb8df0c1af9bcc031f333b8a6e9283bab887c334404ce257bed2b29f989800a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "normalizeEndingSlashes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836b702ecf46f507a2996c9bdb292c9f399da3fb71d72223cabffe006cde25b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9507245a1e54c87c96e1e618ef813c1bc345b8e64063367b957d3580cc603d2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorUrlParser]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorUrlParser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorUrlParser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d474f44a946633f41e3156bf306b82707c46e45b61065d5a6efb5ef73b4e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorUserAgentParser",
    jsii_struct_bases=[],
    name_mapping={
        "sources": "sources",
        "target": "target",
        "is_enabled": "isEnabled",
        "is_encoded": "isEncoded",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorPipelineProcessorUserAgentParser:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_encoded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param target: Name of the parent attribute that contains all the extracted details from the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param is_encoded: If the source attribute is URL encoded or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_encoded LogsCustomPipeline#is_encoded}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29af01b53c238f2d90fd4bc427fca817635ad0c815bd27d96ac35f477e403480)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument is_encoded", value=is_encoded, expected_type=type_hints["is_encoded"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
            "target": target,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if is_encoded is not None:
            self._values["is_encoded"] = is_encoded
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the parent attribute that contains all the extracted details from the sources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_encoded(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the source attribute is URL encoded or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_encoded LogsCustomPipeline#is_encoded}
        '''
        result = self._values.get("is_encoded")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorPipelineProcessorUserAgentParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorPipelineProcessorUserAgentParserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorPipelineProcessorUserAgentParserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61588ad7916c8fac1cf397a751655ca00760f090a9a082fbbdd978d992b9c582)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetIsEncoded")
    def reset_is_encoded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEncoded", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isEncodedInput")
    def is_encoded_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEncodedInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd9ee50ba3b35d857c6f0cdd2945234643c43ea2dfb2dbcb4b65fd5a01deee14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEncoded")
    def is_encoded(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEncoded"))

    @is_encoded.setter
    def is_encoded(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3b7b8af8cdc0951e5f99d0f9d23b41f1dc60736858cb37fe9737c571a7ff50d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEncoded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc781925581e585b997530e60a29ead3c241d445126211c46a8c8058a8c28dda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d561d8cdea8253a7475af9eef6ddc9486deaec54010661d19194b841f2214c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492af60875d2f2f78bdb68f11e5d69652dc07463af6b14e3d018d4b8a88738ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorPipelineProcessorUserAgentParser]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorPipelineProcessorUserAgentParser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorUserAgentParser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e32838e6de8517b67312327ba1e4fac7cd6ea9a6c365689d97c59c27f5b2b4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorReferenceTableLookupProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "lookup_enrichment_table": "lookupEnrichmentTable",
        "source": "source",
        "target": "target",
        "is_enabled": "isEnabled",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorReferenceTableLookupProcessor:
    def __init__(
        self,
        *,
        lookup_enrichment_table: builtins.str,
        source: builtins.str,
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lookup_enrichment_table: Name of the Reference Table for the source attribute and their associated target attribute values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_enrichment_table LogsCustomPipeline#lookup_enrichment_table}
        :param source: Name of the source attribute used to do the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        :param target: Name of the attribute that contains the result of the lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b6cca9d9a9cbe3ad2987247b67e13964bd885c4df00cb74e2610e0cf86b6253)
            check_type(argname="argument lookup_enrichment_table", value=lookup_enrichment_table, expected_type=type_hints["lookup_enrichment_table"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lookup_enrichment_table": lookup_enrichment_table,
            "source": source,
            "target": target,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def lookup_enrichment_table(self) -> builtins.str:
        '''Name of the Reference Table for the source attribute and their associated target attribute values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#lookup_enrichment_table LogsCustomPipeline#lookup_enrichment_table}
        '''
        result = self._values.get("lookup_enrichment_table")
        assert result is not None, "Required property 'lookup_enrichment_table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Name of the source attribute used to do the lookup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#source LogsCustomPipeline#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the attribute that contains the result of the lookup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorReferenceTableLookupProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorReferenceTableLookupProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorReferenceTableLookupProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6d969205695150cdb2eddf6edb7a579c0f7150e74434f3a4f30fbd4cff9ce65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="lookupEnrichmentTableInput")
    def lookup_enrichment_table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lookupEnrichmentTableInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e18f3e6fe3cd57f460af954ea47089ec63c8591d7991f1956256426570223be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lookupEnrichmentTable")
    def lookup_enrichment_table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lookupEnrichmentTable"))

    @lookup_enrichment_table.setter
    def lookup_enrichment_table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cf4555e2c90d337fc4c45ae7f8c628ef363f475a0fbf916929009f0dc4929af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lookupEnrichmentTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c6c9f767dd2a821ffdc861c5b78f3060d291acdb124720bfa1c2664d68ffa82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71efda4cbf19f9256a451f89e41c51d0719751ac99e02677fb347602ef07c686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43dc3761747b9b5f8352390059fa31bc879c7d2a6a739af1d6cc065bc9989416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorReferenceTableLookupProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorReferenceTableLookupProcessor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorReferenceTableLookupProcessor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc19961c4cf615f839b170242c59aecb9056652db4cd518b3a2f4d6ebb59ad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorServiceRemapper",
    jsii_struct_bases=[],
    name_mapping={"sources": "sources", "is_enabled": "isEnabled", "name": "name"},
)
class LogsCustomPipelineProcessorServiceRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54cc4194c29b2a7d94b070a9867a017a3bdc7d0d5b852974151deb6c87e6e26a)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorServiceRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorServiceRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorServiceRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6de88f687dbc073bbc59478c881c2243968b439c06eb9ddb18172ac0ad53ff4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a6144d409e20324020dd22d1990040fa94dc073c1f918db67bd48dfdfe62d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b3d06c63a796724da91acd5fffb3b76c5596af4f1382f69f25b1e4ebf76bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8ccd56577183d8ff685b5450b42a9fe931c1607fb31cfa5d75788bf306eb37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorServiceRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorServiceRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorServiceRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73bda3550f2b5253f9d37f24412efdc13fb15d5eb012191ea0a41fe306951a67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorSpanIdRemapper",
    jsii_struct_bases=[],
    name_mapping={"sources": "sources", "is_enabled": "isEnabled", "name": "name"},
)
class LogsCustomPipelineProcessorSpanIdRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e40b85d0ecb5219a02c9f9c238ae8a2a047348e3517fe0e81a6422fd4a8fc13)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorSpanIdRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorSpanIdRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorSpanIdRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7feb775571aa45fde3f4e55aca13f3db0e36d815efd3a84915390fc21040c83b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d7ef7d50da25d1872b037a3b67698457d8cf47a90a0bc5a56234c97f1f8e717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7813688dee4ecc1046ae017c435adc3646eb8a04a301fe2dfab27e34b42c7cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0e1d3122622c377fb8e3d2a2198b8c8380633210a8c26604a14783ea3628c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorSpanIdRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorSpanIdRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorSpanIdRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d53fda8b7dabf3666b0a3ad9b802f82d020e2629a428a53e07526992967543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorStatusRemapper",
    jsii_struct_bases=[],
    name_mapping={"sources": "sources", "is_enabled": "isEnabled", "name": "name"},
)
class LogsCustomPipelineProcessorStatusRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd012d0ae3574d49fcd6822968eed258a7d636a90e114efb86003c66877a0692)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorStatusRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorStatusRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorStatusRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f98706500b79e9c4f4a88e52fe842fbf824493085526a5103200e7c6d7cb123)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84b59ed9df64b05d0efb7422c621d264c834bc2bca38dc7b8cf829402aa529ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e8958cd38272b7c1ebfe81ac4e3555ff05c554a312ac3ea12354cacff3fd49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5015b67c39ac3ae0c9da08f411e582079e6eafea3ad8cdb62eac5c350ef9bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorStatusRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorStatusRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorStatusRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec7ef8dc19fbb3cb0135050d1e4b459acef677d3b4db1ec96dab4bc63279153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorStringBuilderProcessor",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "template": "template",
        "is_enabled": "isEnabled",
        "is_replace_missing": "isReplaceMissing",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorStringBuilderProcessor:
    def __init__(
        self,
        *,
        target: builtins.str,
        template: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_replace_missing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: The name of the attribute that contains the result of the template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param template: The formula with one or more attributes and raw text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#template LogsCustomPipeline#template}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param is_replace_missing: If it replaces all missing attributes of template by an empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_replace_missing LogsCustomPipeline#is_replace_missing}
        :param name: The name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714aed5a12c145ede8eceb8e65f765b83fbbf3dee8e229aebbb437508a6c44d1)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument is_replace_missing", value=is_replace_missing, expected_type=type_hints["is_replace_missing"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
            "template": template,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if is_replace_missing is not None:
            self._values["is_replace_missing"] = is_replace_missing
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def target(self) -> builtins.str:
        '''The name of the attribute that contains the result of the template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template(self) -> builtins.str:
        '''The formula with one or more attributes and raw text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#template LogsCustomPipeline#template}
        '''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_replace_missing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If it replaces all missing attributes of template by an empty string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_replace_missing LogsCustomPipeline#is_replace_missing}
        '''
        result = self._values.get("is_replace_missing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorStringBuilderProcessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorStringBuilderProcessorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorStringBuilderProcessorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c24b0c00cb7ebe4b23cf6cdab34b31e0f47659ef51b563dcb4e50a65d96df11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetIsReplaceMissing")
    def reset_is_replace_missing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsReplaceMissing", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isReplaceMissingInput")
    def is_replace_missing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isReplaceMissingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aae4abda1740a218d42bb736867f5d9e8e603723fb9d2e5280315851e58563c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isReplaceMissing")
    def is_replace_missing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isReplaceMissing"))

    @is_replace_missing.setter
    def is_replace_missing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325a0acb3d51eec1e1aee1010d84b695331b3ce147a1e482a63ed5b0b1d7422e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isReplaceMissing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fbe13172c78b0261ca24fbc79d797519ab4364e20554cce892db686ccaf940d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df4d19fa5c6aa3d92431482d0ac4d42a841491cf23d9871f57e072b9e928cc6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de28599778071ce041fbd06caf9499633290257b2e9e3b857e0846f3ecf97ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorStringBuilderProcessor]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorStringBuilderProcessor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorStringBuilderProcessor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d67de72f0005d4ff47084ac1ff0a4f83d53c34b6507d04a98709780b9512049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorTraceIdRemapper",
    jsii_struct_bases=[],
    name_mapping={"sources": "sources", "is_enabled": "isEnabled", "name": "name"},
)
class LogsCustomPipelineProcessorTraceIdRemapper:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d858544fd122c10c765f3ab28363fcfc744f7961a33d4e5aaa04e5bc657902)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorTraceIdRemapper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorTraceIdRemapperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorTraceIdRemapperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ceecbad5676b2652ac9f1fafac2262004b0a16976dc2959df25deab24bfe5a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f09a3e45b0c3b18e29dff33ef633e59477e44a6146e68ff23bfcf8bb9d13e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb272769bbdce286c525b5b96a29c6a25bb13e18e67e117fabead6adb2e9af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59aae166aa8769d6f2acfabd8add5edb19b4eb7bb203da5670ca4385a82d312d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorTraceIdRemapper]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorTraceIdRemapper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorTraceIdRemapper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d7173f13d91368c96f10a5613b7da3bcd98c8eb8f149f460e6afbd4afc27fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorUrlParser",
    jsii_struct_bases=[],
    name_mapping={
        "sources": "sources",
        "target": "target",
        "is_enabled": "isEnabled",
        "name": "name",
        "normalize_ending_slashes": "normalizeEndingSlashes",
    },
)
class LogsCustomPipelineProcessorUrlParser:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        normalize_ending_slashes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param target: Name of the parent attribute that contains all the extracted details from the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        :param normalize_ending_slashes: Normalize the ending slashes or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#normalize_ending_slashes LogsCustomPipeline#normalize_ending_slashes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dedbdfed1ec9e22bc841de9f1b61c79daeb26007d92ba84b48a9230752d504b)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument normalize_ending_slashes", value=normalize_ending_slashes, expected_type=type_hints["normalize_ending_slashes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
            "target": target,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name
        if normalize_ending_slashes is not None:
            self._values["normalize_ending_slashes"] = normalize_ending_slashes

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the parent attribute that contains all the extracted details from the sources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def normalize_ending_slashes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Normalize the ending slashes or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#normalize_ending_slashes LogsCustomPipeline#normalize_ending_slashes}
        '''
        result = self._values.get("normalize_ending_slashes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorUrlParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorUrlParserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorUrlParserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44e927b16bd030b74a8407b90b8af0a4bd095394ca5fb594fd0aaa1043418052)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNormalizeEndingSlashes")
    def reset_normalize_ending_slashes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNormalizeEndingSlashes", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="normalizeEndingSlashesInput")
    def normalize_ending_slashes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "normalizeEndingSlashesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__753b3d32ff9dca6ef7b441c7195bd8eb01ddaf70db8a2fc451d0ef3736e5f4f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db23fcce5ec6e6f74df66cb093c67f4f03ce43e745a503d290bf501d6a5a508b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="normalizeEndingSlashes")
    def normalize_ending_slashes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "normalizeEndingSlashes"))

    @normalize_ending_slashes.setter
    def normalize_ending_slashes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d166ab7980829192058cfe9eafcfb9a02313add57fef2c1ddd30dd4eef6085a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "normalizeEndingSlashes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43ded2419d699408409e6af95884f1e49975a2a8b6909ea3755f266e5803fb6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d3a14c540578085b82c9e549c67a8568890474f6e948f36b34c42e6ddde143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LogsCustomPipelineProcessorUrlParser]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorUrlParser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorUrlParser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb20c83c97f619072e7a55f5ccda982208f7d1d168b7607255c008755256d705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorUserAgentParser",
    jsii_struct_bases=[],
    name_mapping={
        "sources": "sources",
        "target": "target",
        "is_enabled": "isEnabled",
        "is_encoded": "isEncoded",
        "name": "name",
    },
)
class LogsCustomPipelineProcessorUserAgentParser:
    def __init__(
        self,
        *,
        sources: typing.Sequence[builtins.str],
        target: builtins.str,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_encoded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param sources: List of source attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        :param target: Name of the parent attribute that contains all the extracted details from the sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        :param is_enabled: If the processor is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        :param is_encoded: If the source attribute is URL encoded or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_encoded LogsCustomPipeline#is_encoded}
        :param name: Name of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be12c75880a81edc3e6dcbde2e33211035b5ea2be57bca8fafef3ff7028726a0)
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument is_encoded", value=is_encoded, expected_type=type_hints["is_encoded"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sources": sources,
            "target": target,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if is_encoded is not None:
            self._values["is_encoded"] = is_encoded
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def sources(self) -> typing.List[builtins.str]:
        '''List of source attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#sources LogsCustomPipeline#sources}
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Name of the parent attribute that contains all the extracted details from the sources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#target LogsCustomPipeline#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the processor is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_enabled LogsCustomPipeline#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_encoded(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the source attribute is URL encoded or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#is_encoded LogsCustomPipeline#is_encoded}
        '''
        result = self._values.get("is_encoded")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/logs_custom_pipeline#name LogsCustomPipeline#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogsCustomPipelineProcessorUserAgentParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LogsCustomPipelineProcessorUserAgentParserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.logsCustomPipeline.LogsCustomPipelineProcessorUserAgentParserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e3eec1b058514e8d3f84be6ff2c86b0da2c2b93a8b2123e1c58ba67bf5848a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetIsEncoded")
    def reset_is_encoded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEncoded", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isEncodedInput")
    def is_encoded_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEncodedInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8be1dd1319bac2a87a27c3b70897d855c391f67b1c9e37e50a978dc44310bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEncoded")
    def is_encoded(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEncoded"))

    @is_encoded.setter
    def is_encoded(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b904c3f2aae66cdaa5d14436708f4bdbc3e6320b5079353606776d006bf1068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEncoded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c5672cb1a5ddaca44cd79e5ccea7b26628cc308e357b8f7d574f6b4507420b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594906e10d6422f9cf7e3bc7a24c7b137443ea6e1e5c800658b4d3cbb48c7f21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__850ec966fed00458737ab022547e333011ad7d612f5de3030d645e497c1cf4bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LogsCustomPipelineProcessorUserAgentParser]:
        return typing.cast(typing.Optional[LogsCustomPipelineProcessorUserAgentParser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LogsCustomPipelineProcessorUserAgentParser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010adc0009bdade3c939abfba6593eff4a4f3639207395231b08f93e09a25015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LogsCustomPipeline",
    "LogsCustomPipelineConfig",
    "LogsCustomPipelineFilter",
    "LogsCustomPipelineFilterList",
    "LogsCustomPipelineFilterOutputReference",
    "LogsCustomPipelineProcessor",
    "LogsCustomPipelineProcessorArithmeticProcessor",
    "LogsCustomPipelineProcessorArithmeticProcessorOutputReference",
    "LogsCustomPipelineProcessorAttributeRemapper",
    "LogsCustomPipelineProcessorAttributeRemapperOutputReference",
    "LogsCustomPipelineProcessorCategoryProcessor",
    "LogsCustomPipelineProcessorCategoryProcessorCategory",
    "LogsCustomPipelineProcessorCategoryProcessorCategoryFilter",
    "LogsCustomPipelineProcessorCategoryProcessorCategoryFilterOutputReference",
    "LogsCustomPipelineProcessorCategoryProcessorCategoryList",
    "LogsCustomPipelineProcessorCategoryProcessorCategoryOutputReference",
    "LogsCustomPipelineProcessorCategoryProcessorOutputReference",
    "LogsCustomPipelineProcessorDateRemapper",
    "LogsCustomPipelineProcessorDateRemapperOutputReference",
    "LogsCustomPipelineProcessorGeoIpParser",
    "LogsCustomPipelineProcessorGeoIpParserOutputReference",
    "LogsCustomPipelineProcessorGrokParser",
    "LogsCustomPipelineProcessorGrokParserGrok",
    "LogsCustomPipelineProcessorGrokParserGrokOutputReference",
    "LogsCustomPipelineProcessorGrokParserOutputReference",
    "LogsCustomPipelineProcessorList",
    "LogsCustomPipelineProcessorLookupProcessor",
    "LogsCustomPipelineProcessorLookupProcessorOutputReference",
    "LogsCustomPipelineProcessorMessageRemapper",
    "LogsCustomPipelineProcessorMessageRemapperOutputReference",
    "LogsCustomPipelineProcessorOutputReference",
    "LogsCustomPipelineProcessorPipeline",
    "LogsCustomPipelineProcessorPipelineFilter",
    "LogsCustomPipelineProcessorPipelineFilterList",
    "LogsCustomPipelineProcessorPipelineFilterOutputReference",
    "LogsCustomPipelineProcessorPipelineOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessor",
    "LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor",
    "LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessorOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper",
    "LogsCustomPipelineProcessorPipelineProcessorAttributeRemapperOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor",
    "LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory",
    "LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter",
    "LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilterOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryList",
    "LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorDateRemapper",
    "LogsCustomPipelineProcessorPipelineProcessorDateRemapperOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorGeoIpParser",
    "LogsCustomPipelineProcessorPipelineProcessorGeoIpParserOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorGrokParser",
    "LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok",
    "LogsCustomPipelineProcessorPipelineProcessorGrokParserGrokOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorGrokParserOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorList",
    "LogsCustomPipelineProcessorPipelineProcessorLookupProcessor",
    "LogsCustomPipelineProcessorPipelineProcessorLookupProcessorOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorMessageRemapper",
    "LogsCustomPipelineProcessorPipelineProcessorMessageRemapperOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor",
    "LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessorOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorServiceRemapper",
    "LogsCustomPipelineProcessorPipelineProcessorServiceRemapperOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper",
    "LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapperOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorStatusRemapper",
    "LogsCustomPipelineProcessorPipelineProcessorStatusRemapperOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor",
    "LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessorOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper",
    "LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapperOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorUrlParser",
    "LogsCustomPipelineProcessorPipelineProcessorUrlParserOutputReference",
    "LogsCustomPipelineProcessorPipelineProcessorUserAgentParser",
    "LogsCustomPipelineProcessorPipelineProcessorUserAgentParserOutputReference",
    "LogsCustomPipelineProcessorReferenceTableLookupProcessor",
    "LogsCustomPipelineProcessorReferenceTableLookupProcessorOutputReference",
    "LogsCustomPipelineProcessorServiceRemapper",
    "LogsCustomPipelineProcessorServiceRemapperOutputReference",
    "LogsCustomPipelineProcessorSpanIdRemapper",
    "LogsCustomPipelineProcessorSpanIdRemapperOutputReference",
    "LogsCustomPipelineProcessorStatusRemapper",
    "LogsCustomPipelineProcessorStatusRemapperOutputReference",
    "LogsCustomPipelineProcessorStringBuilderProcessor",
    "LogsCustomPipelineProcessorStringBuilderProcessorOutputReference",
    "LogsCustomPipelineProcessorTraceIdRemapper",
    "LogsCustomPipelineProcessorTraceIdRemapperOutputReference",
    "LogsCustomPipelineProcessorUrlParser",
    "LogsCustomPipelineProcessorUrlParserOutputReference",
    "LogsCustomPipelineProcessorUserAgentParser",
    "LogsCustomPipelineProcessorUserAgentParserOutputReference",
]

publication.publish()

def _typecheckingstub__22a9b3913c726d8d372347ddf08a1fdbf32dc7eb18b77496d47880af01faa82c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineFilter, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    processor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessor, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__32593a7b2dcab2495d38fed1a253cecd7c87035f223165be2ff78a1136ceadbf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9336c80022eac99c35b90d7a45c4541ac47129ab00c7a5d77384e5c27032ea06(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e1e6851f44972f4803f496a45ff70f64ddb923a488c854bb7e3d86b2bfbd38(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessor, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9a1d7a47e2fd2066ff5cdad653572f2353c9ae50acc99d3b8ce6237d6f3049(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57f530464eb17cd8e83179c92e7b659ebec277a9905aacb98fe0c9d2b8e587e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c448e71b83e50629d9c26249ae6163b7f080508ce8cd9912769707ad08533fc8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20b7063ddbc89e283c35bc63c020b1c2f192672850e7e58acdab258748bef34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a67f261877fcd371bd8b7940697e619ab308aa3bad8916b8c28eff35f927580(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3428c8dc0ce3178ecfe4025b9c71eb8766b8f723688d7f1c9e1778bbc91f77(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineFilter, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    processor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessor, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06af79ced7a3adb91e320775d3af5ca11ddebc719825d9c7b9fd188322da3e5e(
    *,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f0ab753ef76fa0e8246c1b4c0a23c1d66343d1d3b5eda1d6fb2ecb10741a40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5cc44101c02727857495e2440142d46144343d11a5b8ab4d6626a8fcbfa477(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8e653654db4cabeed1fb8f6c20bfd81758ef1331128e8cd8e01401b9dc5a45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e54d536ef07138950889512ee81540589a558a7aa59c63e4435dfafb76da3e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f737801a0bcecb3ca215443d68a09ab02931500b119867ad9e8ccdb63f31ec46(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb4eb64e1c36bbab6d88112b585e492b8b4e46100d0a7291c2d3fc6588fd87a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__099776583831fa336db4d0a67bd960e73fe17051ebd73d1ecb7d0ae48caedbc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efb965ad11c2b8eb005841101c48ca56fc059863ef0b3ef935e5bf2c881927a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7889e3ef4f334d63752f86dc94196d6bf9e0471e3f811bee5d6804d7dcc930d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e162331cefb51b80ece54be0131b60a9983fbadcf5793b75e3f0e393ddc41da9(
    *,
    arithmetic_processor: typing.Optional[typing.Union[LogsCustomPipelineProcessorArithmeticProcessor, typing.Dict[builtins.str, typing.Any]]] = None,
    attribute_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorAttributeRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    category_processor: typing.Optional[typing.Union[LogsCustomPipelineProcessorCategoryProcessor, typing.Dict[builtins.str, typing.Any]]] = None,
    date_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorDateRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    geo_ip_parser: typing.Optional[typing.Union[LogsCustomPipelineProcessorGeoIpParser, typing.Dict[builtins.str, typing.Any]]] = None,
    grok_parser: typing.Optional[typing.Union[LogsCustomPipelineProcessorGrokParser, typing.Dict[builtins.str, typing.Any]]] = None,
    lookup_processor: typing.Optional[typing.Union[LogsCustomPipelineProcessorLookupProcessor, typing.Dict[builtins.str, typing.Any]]] = None,
    message_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorMessageRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    pipeline: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipeline, typing.Dict[builtins.str, typing.Any]]] = None,
    reference_table_lookup_processor: typing.Optional[typing.Union[LogsCustomPipelineProcessorReferenceTableLookupProcessor, typing.Dict[builtins.str, typing.Any]]] = None,
    service_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorServiceRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    span_id_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorSpanIdRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    status_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorStatusRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    string_builder_processor: typing.Optional[typing.Union[LogsCustomPipelineProcessorStringBuilderProcessor, typing.Dict[builtins.str, typing.Any]]] = None,
    trace_id_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorTraceIdRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    url_parser: typing.Optional[typing.Union[LogsCustomPipelineProcessorUrlParser, typing.Dict[builtins.str, typing.Any]]] = None,
    user_agent_parser: typing.Optional[typing.Union[LogsCustomPipelineProcessorUserAgentParser, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165dfccd3ae85989f1d521f57b75d845a867d1a4f22b807f94d1aaea275be552(
    *,
    expression: builtins.str,
    target: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_replace_missing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d9797a3396bf3e9d3c32d4fdff7d343cccc4c759763a4e243591121ef0db43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e363508fde9ffeb98f691af5e61f1ba73ad2ddb03563d77e62e59d16525f9a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ef3d3da873b0a439249303437e91c62fb4b3c2b80aec8d008e9682cc4b7e89(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80b6a691c0611a21df1055eec7adc7a7c69e745d465c2c8c683c584aa6ddba6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e1f30706d4b772c31610d43fb5386a95f7d77510f08d7f6b7d2def5a9b256c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc60c9d7103e274bb4f0a83c6d514e7f657b6894bb7f666db6f527e5d74fda8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8764a111b3a5d832e4295bafe2f18b8191becbc06a8b6f960c1a07ecfe49f8cb(
    value: typing.Optional[LogsCustomPipelineProcessorArithmeticProcessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3d422d5f6fed40ee0387e1dd3994e0e679e0706bd384bd358d46ba7f62c099(
    *,
    sources: typing.Sequence[builtins.str],
    source_type: builtins.str,
    target: builtins.str,
    target_type: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    override_on_conflict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    preserve_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    target_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a070498120d900f4a0e1e876b6328834ce066ee7e2cef9699ebb3f7c1b380e9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e0b337fc3d2a34e0ea36f5bc6f43cda6358b6e5f0213bb7c00a282834bc8ca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b6b55f4a42d076bb52639e003b9e0e2c330e3005df2107ab7fca2223ed9f4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7179e886b2a4212c745d02dfb10e7b9bfbf004a919c5845d535073258aa40104(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac2161cfa27696ec8fe12ba45818c0fa3767617e30c98f201f3b6d8ac1dadcc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f9cb0c5d0e1eb1339a913a646fc7a123f0aab8c9813d014de5e683eb549602(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64ffbf0753f1b58a50dd5ba1366fc77a3071e88fabd1214834f09b96268389e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934954cd6a3a53003d1079a6b98e24c89792d69209d13b6f6be53cb1c0a2d920(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94b125d6d060826fc5fe44801833f5b5b6447f71aab7be18bcd4f156581a060(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a390fe672d6b6187e45767ea0b044d704abffb1150f83e5e394a185803e3d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a3323c99fdb7d2d1e78a5e6e381c842e3bf825d7d59299f692da394c3dfaa7(
    value: typing.Optional[LogsCustomPipelineProcessorAttributeRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d020454179d0e702232498c0fb091e398e76a34782b1418abf4a7269ebea3d3b(
    *,
    category: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorCategoryProcessorCategory, typing.Dict[builtins.str, typing.Any]]]],
    target: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7e1329af950c282610449115196a444c0c9855ae09fad4918548fc8b396241(
    *,
    filter: typing.Union[LogsCustomPipelineProcessorCategoryProcessorCategoryFilter, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69b771f248ac613e79dadc9d0b68cc45648b85fc7b1ea8aeaf7c7cf2e4ee334(
    *,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d692e6103183fd28bcf3912a6f7389af61824912f03e5946c5c8ef88293950d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa42c9d39d6e2316d2a74b8e087df11a1e955cad0990151bf64c850034678e8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88798d6e39d745b915fce8ef2686070024481b3d7a9d716637e2f9116749d5fc(
    value: typing.Optional[LogsCustomPipelineProcessorCategoryProcessorCategoryFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e822add5e45f4bef35b648616980fe8b0bdf0b0b959be69c51ffffb54e58d2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb15500654dc374f631d5a6b9e06f46c1e50f5f2c36475f43a8da8a78ba8a644(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3262ae0df39ed7a53eb726b36f21dbda86623da6222ccdea7efadfb44674a168(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b70ea27382ff1985b248d617e576bdaa9341f7c65d1fdca06361812904febaf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1647216bf932d1eb569809c2908c93d84fc0b156da5a0161df42c4231ba7f859(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ea6cb952750a3e8dccadedacc0f85813fba7de6dea8f76a7269d5da5c4f9a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorCategoryProcessorCategory]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b0702bd187b80342b6f5e6036dc5c179faefddfc4b4f2c57afe44f58381d87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b1263b576abe2ce40f13c559e0b3192f50252cf18a5982d2c1c0d29b716497(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a65dd7bf75ce80f4df7ac2fe5e4cdd0e3531871a33720117dbb971b463d0cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorCategoryProcessorCategory]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7f8a23c5afbaf16952c86edf4b552f0d57ecb027e6213f15d90eb4571c8d0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c887431da5e945c3df6036be47fbab1b8d8f0ef0dde9176c5e2c49352bf60e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorCategoryProcessorCategory, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a662358d429aeded4a587dc4022f09286bfa2dd5a552ceb071a5caeea3270ca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e2672b9b3cb324de42c3e87c3e1da2f32faf5b3a245624ac19362ea7d6590a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9815ede4230c572ee01c99de9340a3398235e7520a7590547b90ace08514d435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00a54eaf6adba95744703204a96ac4cf4cf77812b902ddb7ecfdfe3beabee27(
    value: typing.Optional[LogsCustomPipelineProcessorCategoryProcessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b6df76e438ef90b0e20dfa2851fdc5cdf1025815d7cc47b0473fbd428573ed(
    *,
    sources: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c63044ff0c20b642980c28f513f07a2a798c0a7daea2f9662c515eefd9347a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8775c5b9268424e72d85e8496355eba2c81f4f3e7d4d21c1c425fad127819c8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8667b7fb1cb22a5037433d78af772578d22cb58eedb484d1c2d7a264a6a1b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626c0eb72b89340523a1e5254fc564b4e48e31ffb54aae10cb67a79435a5893d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1291d4e75340add33012bb1eab04270eeb74636647a157eb867c62ec12fcc568(
    value: typing.Optional[LogsCustomPipelineProcessorDateRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5876c2864b1a1109c3e39053fe1450681dc744c291d4fa0b2cbd12231caa5f7(
    *,
    sources: typing.Sequence[builtins.str],
    target: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6fc8938263665763e769fad56c032080ca7fc4c942f7ef3804322fce617160(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae16154b0231ed4d12e00a635072c00e2435a683ab8b0e58e01f7c6deb97165(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9233e83ab9841e0746828b78e770a2a4850f960389efce895d5874aad8c4ba01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c4d5aa7b4447e1684b83719fee8e8ac87a184b590eaa3cfd753437c5df2289(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f17bce88a357c74f56c08643f2e374a0790408b0c7fdfb7c0ef785de4ae483(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b518f5e38d97f19af58189a59a90935eb240a72b1a2e7016352f01786577b91(
    value: typing.Optional[LogsCustomPipelineProcessorGeoIpParser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d345af20518336969f6d0e754f1cf620b57815300996a51e7d870f8b9c21dea6(
    *,
    grok: typing.Union[LogsCustomPipelineProcessorGrokParserGrok, typing.Dict[builtins.str, typing.Any]],
    source: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    samples: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a08abaf2a6cbf76e5e0ed1dcff20792a6ea0c7cae6cd9358348db85641b804(
    *,
    match_rules: builtins.str,
    support_rules: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d27c2ad36831e510788b04e0e0db467e327ee44ab2671caf6352d5fd005af9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405e1da29d5471136e0108b61534cd43146ac0e5378fa18e44ed5f7454bc755f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8b7f404ed5c213a9057134bcb87b4d134656c5ce7ee9ab35590588ee4b7083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec88b97a1a58aec7ffe9828c9432ef3ad26dc213191a667f03bfc45b1420416(
    value: typing.Optional[LogsCustomPipelineProcessorGrokParserGrok],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a7780a9f46b1e92b487a0ff78b8d2b4f59f9898580fd0de07d376e90313f79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c8ec329219a9e1bd1776f8aa2d9642613634308b49880ed3fdf079a446bc82(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96e838514d2895dccf71c9f2745c3e510b5e42b7c39b3eabb9d0180ebc2ca27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dac23b16addc6d8334ef0999bcff61e24c66f4afad4c9ccad009c110d788a51(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ac060afe6361667d2eb92505165c772be8c9369c90b7dce3a0bb6aacad4e1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e19868df886c42fc7da6a77398f765176a97ef511e81e11be1bb13cd8eed24d(
    value: typing.Optional[LogsCustomPipelineProcessorGrokParser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c3f31f1607ec4e4c7211a540aad07d1b5b426644c8c3101f42aaa91c37f611(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0a26409fab740d17f9cffe1cb17d591fe0e179622020097918ba6a857b6141(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78331358886a3ddf5567d76f9116ba8baf7bcf8fda341cdef485178df985fa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7997e6681e8d33737d46f6d3cabd33b4ab3b9fb5db24dfc5f0e8ebd0cf8e82(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcdb13fdc1022ae6fdd5b2bac099920d32733eab5947647b6f172f8355618c3f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa940b186cb7e012c6d13893fa6b2dfbd9ad3d88768ded1edb57c715a8fafbf0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessor]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c4305e56ee1b323e4b08be1a73f63b90af7a45c702b03ab87278aa01bcf83d(
    *,
    lookup_table: typing.Sequence[builtins.str],
    source: builtins.str,
    target: builtins.str,
    default_lookup: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989f901959d9b0417f743e275c935776d4e0e2eb8c61348a6b6003c96fd7272b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074baad2a9096250af85266a8f04d46f2751e72b7c0167e7a12088bea9aea154(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd1f2cc5eb33e4dfa05294eaba285f76635578140918144e1a964d74e6a7d4e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb37bd71c0e01cab79c571e9d323c3dea09eb69aed11bb3003965cf3d5adae9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61f00076db9a13743c0a743a8381f302cd607d430ad15863c1a16bf8949cfb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f177e4f6ba4cdfb4423e11266f8c6b74ea35df915ca23aac7888b4abb51375(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436142d7fae39dce4cab6d4fe975399b6179b345c3a4da38084430c5d9c8ecbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608ffbc8b6dc0b145a3b0d9dd6176222edfa06b3f6d7c585244afcb91f119803(
    value: typing.Optional[LogsCustomPipelineProcessorLookupProcessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ca14cc207841035e09e338e44cdd9270515b65ee52b5063928d2892e79136c(
    *,
    sources: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e888c9a07dd8fdc997cebe1efe0498c8b85a6e1968cccfbf68390cdfe744b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca0b6fbe4ea3eb634aa7398db62dda4c1960365d2494608847220f2ebde60cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dbc7e10b43b1a9bac7d470aab3ced3efa35f89981a1cb70e0cbb314fc71151d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70c5963132c01dc79aec276317d63afdc8da66d102bd5c85651002ac1f12c37(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d96ef5fa4e978e8dd98d29f0ced8200a58a808961fa6dae125277cf479bfcfe(
    value: typing.Optional[LogsCustomPipelineProcessorMessageRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0c8c66d32b4a8cd59b61a5b5f470a7b6f6c84809aad4f9137bcdf08f822dda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfcce8ba77a44cc6bed0938e9873daa5c2f3e0a3a9c84a79d9ebc6de1d98176(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessor]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cae1451052ba984a3062d0fbeac97ee702dacb11ef0e0d66379fd6266737e3(
    *,
    filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorPipelineFilter, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    processor: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorPipelineProcessor, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ac592d8c93de938e3b1deba5116a7ba8ba1904d64d0505cfffedf13593eae8(
    *,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e1554d898a170ab6a1bca71b376898ac51c4ad7040a358903a7ab41ba0d0de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1205df598f9f97b8b4748682656fc36cc90ad6426e9dbf3f5be4dc50876f564(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1db1776596a329a7dcf718d45a6f06e2c73dd20a0c2f3b95648dfb314fd88ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfdcb5cdab919f372070cc072d68b3fff1c642e703a4eaf5ef00e3cb2f713d1f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262f62541cfb9512e6230f50c3e46e0b7380688d359154076990a7e5c42d3f83(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1263fd7e3d821a625ec73da7e334c95e9b634c2123ac40ff8b0160d9984f9fe8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93476001283b32a42c6502bb95ab86b8726404d6aa64057130a159f7d24d6b94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5e2cb19a2661caaaa2b49ec993c0b2754137d39484c1673b946c66ed175a08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873f19e6bd5dc83f634149cc500b7dfa754a2882c92eb554908994c22d8362bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorPipelineFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38db5f42046c42808b6898039e5e147f48714f4b48cabb056a3bcb337b3366d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db91895014e1da8ff264065376c4170487e84806626f357ed0e1ba574e88e103(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorPipelineFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25ea2a96a07809236e4ecf51a5f96280e462a5a41bce3d1e99054329fb6f766(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorPipelineProcessor, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7806968562473c05d4ffe93a768a3346824d04988202aa61545a92f0982ad8d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d374b7006c3323b9b09fb48ebbbbef157f516a07a983abb6c432e8e241a32bb0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6567a4a9332609c28ba038d6ac7160a9db29d7ef50aef5e83569354316f60cf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885d2ba2bf755a7bfe862646caa1bb6c9e9103336f5c79b14196f0614b54926a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43017ce50e3363c967e33fb0954a37f52655b63461b5e34b7b39c68afd5ea964(
    value: typing.Optional[LogsCustomPipelineProcessorPipeline],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83117c88869ce2b934fd70d40a5887b1c9741b8b57c0121d1e8adffc857e1e6(
    *,
    arithmetic_processor: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor, typing.Dict[builtins.str, typing.Any]]] = None,
    attribute_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    category_processor: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor, typing.Dict[builtins.str, typing.Any]]] = None,
    date_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorDateRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    geo_ip_parser: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorGeoIpParser, typing.Dict[builtins.str, typing.Any]]] = None,
    grok_parser: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorGrokParser, typing.Dict[builtins.str, typing.Any]]] = None,
    lookup_processor: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorLookupProcessor, typing.Dict[builtins.str, typing.Any]]] = None,
    message_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorMessageRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    reference_table_lookup_processor: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor, typing.Dict[builtins.str, typing.Any]]] = None,
    service_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorServiceRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    span_id_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    status_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorStatusRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    string_builder_processor: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor, typing.Dict[builtins.str, typing.Any]]] = None,
    trace_id_remapper: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper, typing.Dict[builtins.str, typing.Any]]] = None,
    url_parser: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorUrlParser, typing.Dict[builtins.str, typing.Any]]] = None,
    user_agent_parser: typing.Optional[typing.Union[LogsCustomPipelineProcessorPipelineProcessorUserAgentParser, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6472717b34fe07b99b374305a50cc0a4b561c162542c565e3653c0a4e5840c7(
    *,
    expression: builtins.str,
    target: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_replace_missing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f283ecb20b5a149937f868c7f2f375034a4bc0c24fcac52b8543fe9df8ba010d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7eb6bbf476a698e8f021905fc46b58b4485fce133dbe61f2d38e21f7cefaca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8357ed3d28ad8122166261d37ba94008ff0a74b716afdf7b25828adb68c65b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f49edd1949b4d82e3d8e9749e32da84f06cdfa957903f0468daa01b61dcc1ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da29c41c99a85b4884ca7ebc8f2aaa017bca1cd40ac207fa022d72a0483253d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a40b3e07dfdef04cad1318d6109a6d90b441911f758ae220630f10c07d6d51c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a444dbd31a0c39912d9adf00d6030a297929a85fb012e64947381586743a22(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorArithmeticProcessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d539d2cbacbac8393e4c539481675119eaaaf6e04b0ff8a92ba4db6b783e1d(
    *,
    sources: typing.Sequence[builtins.str],
    source_type: builtins.str,
    target: builtins.str,
    target_type: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    override_on_conflict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    preserve_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    target_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7fb7f22bb8eb4c62ecc57660f085b8691183cbfe7092360f1a2fd5adcf45cff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1c6d8bc29d8cb5802fcb1b502957dc5835312edf572f8f00016a13d9d0c633(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c1d715b663f8f421b4e9de10da4800fdc51ba7232e65276e9c829d7a55a5fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535f72703289ed32dd81ed17aef9cb97c83eb9a6357cca5ac4a736b441b7c474(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e1ed42fed49b84c4c63228cfc111974f6c42c8b69a7fc90d29a7ea51e10b2b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f2c0c008260bcd9300517f447f019f8877fd1f0a1a030af85462e21f5b73e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07016dff02666040f68fa7137ba902d199188e7a6f8c328a1c61df309113ee78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a2ff35f1fe0187bb888bab69e296aeedfa479ad827e4cff7133562fc90eff9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f0123a1aba9cf290c62d68cf7e3c20dc7679bb0c52a6e735674625378a5f41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a6d6263afa101c14ed5cbd46366aab8e5e6c364bbca85cafcdc9fb26349705(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ad7f3565fa6745c85275371be031c48e80a81b41796942969110a408e10834(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorAttributeRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076fb5080c0ff6d46a7c2eeb2b2621810e1faaeb6376047c608bf0e5296dc6be(
    *,
    category: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory, typing.Dict[builtins.str, typing.Any]]]],
    target: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc9895323a13f8534f5a6c88677c9a0443752669b5be7e87038cfc163693e44(
    *,
    filter: typing.Union[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13698893fe66fb74b24f8c9e87e033fdb4d9dccbc9f652b65ffa470489fe1c6(
    *,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0d61f3b6d5d6cca479922cb795b7e6df31fd63a8497d7c6d3c0fd0fc4fac5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbb32a204049320393b36db20c0e575d60b8ef87003387544a0c13198c902c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8106f01b8c8752874e951b2033615285c36c848207c157649232a91fa3f53b9(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategoryFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369c5f1a8fb47aeb844b8f644b4562ae697623d3dde9a9e456428f9a481380b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515d5afdbd7591b6bc85c71e871ad305dea29d50a89ed0e976062f18acf8d8a9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063059981a7fa5190a7261aada3e2dfef7da894617a490293cfd85f3d3a6068d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06260f19d8e656d0be030994c7b3b33fa758dc218434e6f2a4d75e0c7943e041(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa117767a307a6a1b07c71ae43072caff9aaba70f7df7b7ed84ffc79b649071(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b5392c5bd341247769499a9e7e53bbcba58afcb82b0223caa23976f41c9bea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0277f76d899ef21cb20df677be604d7213b3675522f1b5ffa51bf64d56282cb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7655e0236fd36918269e52d89e0804362e42e2ebb6488b37e6008d9d3a3d6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fa44f491e4caffbeababbaefef61b56a59b8d70b2cd0c7828328f5fb61a819(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a289b3549e1507a208815d78cc55b8ee9a72253af7cf2154ea1e0bf9870158(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abdd4eb88293c83a19d79c17e85b5551ee7a26d8ab3ad8c8d5e5165b61135e0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessorCategory, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da14b1e08bc429a23b1a95a27e3f35c0d346e9c928a9d73b250a53f749046f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d531b7c6070d9212f4fc9992da153e37e0b8a33873adda02b794caca028e102(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d87917d2aae60c0fee2440a0ebd8d7e6658c0f2ae3c4e1e2a2cc65c0295649(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c9dd10cccc89123b3b3be3b58d9e649ae1f8c6a2d92021fad088715749f53f(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorCategoryProcessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b2235a8cad9f7a25804166e40896b12ce08dded8f4b0f15dfa7420679d771b(
    *,
    sources: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7acbcbef5e7d12234130a9370e795815b2daa833bd1b6e96b6f17c3d53d6d63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf6ae40962e22c266395fdc994c1eabdeae2ef78f4b4cbc510a5bdaacf06ead1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29a241496e3629db90cf871145655a80daf47b129f1f4a2f1a58b75f3d01327(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a64e532bd00b359ed07e2de61aa88bc21d370b5f3606e3303e57f93ddd55476(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5151fa562074a4966b25969f273eb3018f91d38b7b7563f7af3cc75cdc265756(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorDateRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4572e6c6018a2575f6a25afb6b9bbe64523eb8c18dbfa8ecd8b25ae6c8bec8d6(
    *,
    sources: typing.Sequence[builtins.str],
    target: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffef0025044d4c253dc10bfa441f16c99e9dafef65c9c9708f3ce41cd2984dc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fda2ae4e6e33ca9b76be1d5698eded3dc2e1206078f096acceac48f192a0fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbeaf680d4dc9b3c91754615dd9378f8b5f98d3617c81a67fe8a82a1269eadf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c8026849ae3630db0bb3ec43b70310c5b8e81a46e3ac5eaa15c1a34b209d51(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e320ba5a46d5cf013d04ec31e3b4815370c4d7bd5e4bfa65efbaa9371b6798(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f2c8b5fc9dd07175f298f09d43a149d0da5b3f8f7f9a463f3584c8eede11a4(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGeoIpParser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1ca36764f078570fc9d9d82c08e79eca9c053a3fef8eee47babf3a9519e9ea(
    *,
    grok: typing.Union[LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok, typing.Dict[builtins.str, typing.Any]],
    source: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    samples: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72aed5e4aa7c818bf6d16ff4d6a8bb1861758557a40acb02485665e235f39f6(
    *,
    match_rules: builtins.str,
    support_rules: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b799c631036253d55bba52a8fd304c3911099bea02a3a522a46640d9a2930db3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e811a3b0687ee44dffa3ea6622f53daefa55052531e29e450010622d4901f5e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0edf07761236311f708220a6b28ea8d224a6db28b3dbe6f05fe36c4ae67e53aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca421dc9b7636fc178ad5502e27ddebe6b1d776b72f0e79fcca43b5cc897711(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGrokParserGrok],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25398f9fa05388573e46e16b87d5729d603f85fbbbfacf3b0cdb6e55c465b593(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337386346c5d2ed8899fb819653ee537efea25b006451178dfd18e4643ec2271(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff863364e0701e6efe1cf91e39e811b64e378286943d84996811beff549c498e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9af886131d25c8af29e819d0f910143b44bceef9bb7701eedfee23447f9867e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fa71496f27252092b0f38dfefbcbdd9efdd0cc8a57cb291a8fb50ce017cd6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb17df5c567b03eeeba82508f2a3b87f0364b3478cddddf4695a138c0a6eec71(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorGrokParser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f21b612c423d6f005236d9e72cba728052ea99d04b117f8046829725b2ef12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e598cb0b50c84b301977d65ba7090f9009247bfdc0fefd468281b81d541547ca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c5c49a6bbc122f54f652659b35e23ac10380ae2c229f899e1ad4996077ae5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27d8e8c94bb2dd16e3ec1e9bc976028b1c1759859cc81d7f40fcbad9c5e8a32(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a13eacae46ed4ad05e8edfbf3ec8f788024599645d7dec3811c30f1ec0b61f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28251a1051edea6a981c5a76f79b063aedf358c4e9e258b0ee4fa2a6422fd939(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LogsCustomPipelineProcessorPipelineProcessor]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3c59f9e021d4bef41e8fc5a3b5cd9fb80953234adac9d21c60730d950c15f2(
    *,
    lookup_table: typing.Sequence[builtins.str],
    source: builtins.str,
    target: builtins.str,
    default_lookup: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb5309819c5caff36fbc41283f6a86ef60b7dfae0e9cc6fa50d7544d8dcf8d1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96c25102e33dfb9fb11023bf081fb5b149cebcafb14da75824ec699e8c40362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c50c2981af53936b3a79dc6d8ea733b5bba8ecf95e7caba8753f6fee019395(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ea0e35e6132f539013ae274d98ddd5e7ccddf5db8d8011f5c558f39d048261(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d92abde71087c09dcd185ff2e16218b9a7f1731fe016f88bf9f0c76c2bcdb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4396fb92870d3bfdae1a6cea8df8b50c2b2fd838deb480c738eaf0f5f25ba5c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cebf218507c082e847820b2ad012935895fad5c2d5a95ce010d847b5a228015b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5954ec0d5fd1ee0f77cfab6b6226479a600f251263c4db91ea0f0cffaf41b460(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorLookupProcessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4270b6ad21cf9cb28787964fd4bebca907b8e65f52997e484a894458a58158a(
    *,
    sources: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a9b1eee95ea57aee6363a12989cc08d32fe436eacb16bd056846a12d554576(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc5312521dd1858b4a299f39bd8beaf2aaf88c06a0a6b3d6e852201962369e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a987e91eea81218c73a076b5e3db9aa93716d543fdca33c6442d5ae305380a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1242a9b97128abd020c03e76be3d03f95f67a2aa3557dd50f4aa66aac1086f9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01ca0721cddaa0ac57201375f9965a7b319cd70a4b82233e78b782c164ca297(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorMessageRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7aab94433fc9bb5ce47b7f0b07b6aa544a847a14cb50cd054eadfb2317f84a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41475250a108a98b6107c10b28ca53d8a321c49139f7745fa05cb8ef8000222(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LogsCustomPipelineProcessorPipelineProcessor]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b2a3e3d94c1fe100587b4b785b35062061dc537deb671f578f28b3c62d5ab3(
    *,
    lookup_enrichment_table: builtins.str,
    source: builtins.str,
    target: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e498c89cbbb82684dd902f0e8a365ef04457819b1c447554a72542c936f2461(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08600c73465359d979d27e7b0409f93298bb8478f3d9e94aabd2413a44dfd254(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48ef46a42695498830f4b5430f3e05702a8827a08d2b3a5935c32b05bcb57ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4247c831f1be7922a8d8039c610f0a5c9f56cf2fd8f07963e30481f3bd3332(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0071a45ee40a0726c3881962324ae53e1a6eb799305d56f04d14f19106ca43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6125d7e55d265bf33d9a4af0dc42f6ced97e494d4e15823fcd20cd339e00d961(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d924809e3f11915542949a5514f53851273f1610defeeb11cd7cfee9b97921(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorReferenceTableLookupProcessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25be134783ad8859764727cdc99e7c71582e70dca162ffd46f3b8151dbb5b550(
    *,
    sources: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46184a7d3db44c26d2871dadcb577ab8cbc000e156d1902685d4405467dc600f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b9f3ff658bf26822ebedb26549e0d3c10c401ae82582c3b5e815c04491dc24(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d69736caaba7030b946436921c1720890e87e6f95ed60882cc76a32f9ab915(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9ccf1c279cf395f7b442eb5705fd114140675bcf5f0c56ef1938f3a4ddb6a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98f99cd929f21d1ed8552d103f8ca266076c0424743aebd4640ca9b1e318bae(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorServiceRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efef503278ef352103dffa64419a7a2b276cef8de49d3e655f7a5105702f8fe(
    *,
    sources: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f235cdaf9e0a09887b05eeadf7b1d1f739c6abe8d45cb959862e5c83f2e667(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd98ee54e9cf8e9a76de0c48a416559e5cab1e3a18c324e068e53e721dd2283a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871caf0647b58a8426c4cb52a9ff76b3e10c172b0b09ed32ee13a9d86c4daa9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f478a9a08d23aeec28245a030e9bd3cc59e9bd114c47760386f86ba06dca405e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db034d82205a48aa6079e497e1f5b12df99c5f0b53b0e57c69d50aedf6b0107(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorSpanIdRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c0e93b59b82ff448c83d13cd0fa99f07533f4afd2c1177fa81d5e8a48a6fe4(
    *,
    sources: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026a173a73dfa0bb583883f7212d3b096a9232854c39027c97f8ad5d56ab51b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04845f06b4e5edcde15336684a2172280abf1e90e768c4efc67c85c8cc978cac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea1c8046d14ff4bd4084449c3d4bd396b35298274002dc5cdd735c0af30c469(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4703775625873ea1d888e233acbf6cc74017d589225e93006f2a192c211097(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9259e6bf9985ba76a6eb1ab55bd97830c9f85b38e4d071125dfad34d42608823(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorStatusRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e66757241bfa12eba6efebc21b0d18f44ea85a311b2fcab40dfe22cf738a70b(
    *,
    target: builtins.str,
    template: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_replace_missing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad9786c21b9c809a3eb6093b928fdd42d437c1faa52cf93336b0a30b3390386(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e771169fd6d80c55c6fabdd366528fb44939ee3bdbf1663f8ccb1425de98ef65(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c77fe989fbb8f19469d162931ae06c1b32ae720e5bc9f5c88439fe7a973bc4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c35d30ec1231fb4b54405d6bc22cc6869e73791430083399475bab777e34f1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c865b92d2782005e264593741228b5f03d04a71323d411fc0288e5ccce71057b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f8761540d58652544fcb7df0d26a76058951b4d08e139cc917ed5f412dd624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abdf7b6a7ad84bae39fa6f65b0e1a3bf15415c2f2da4abc936f3f8145ff4e53(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorStringBuilderProcessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c78e26d1da1606a12b23c4a827f94e47662754d0f66525ba416f1aa7d555513(
    *,
    sources: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103911d48b52089ff840d432573c3c55231a49ff82e0d6db48e03f71c7412110(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5e67ea870c1335823078986ff725243e804ef2e921c857a597c28aa4d7c348(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f88e5e26161b0a612a11c0d907046c2de927ace96cee0fd7ca02bb236b5d1b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69c4d1a1e70d43aab966a834d2116aac507448cee5120055e352fcc8514a698(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9139df5006abc42dc07aaa845dd823d8c0497544a6a78c4c25ff558222589d89(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorTraceIdRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6419e5c307d58be7369139a6efe254a361067d2475e2affe02845b14fc66b29a(
    *,
    sources: typing.Sequence[builtins.str],
    target: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    normalize_ending_slashes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098890d600e79568f89c443ebad3cc28ea879ddf074f7e6c071c563c71f1a886(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532c42800696cc4589d730f8c502756fb1501be07758e660d755f52388b84bc4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c039e07245397cf94d70cf96513731f36480b030ed3f58b8e9ecfa574cbc762e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb8df0c1af9bcc031f333b8a6e9283bab887c334404ce257bed2b29f989800a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836b702ecf46f507a2996c9bdb292c9f399da3fb71d72223cabffe006cde25b0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9507245a1e54c87c96e1e618ef813c1bc345b8e64063367b957d3580cc603d2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d474f44a946633f41e3156bf306b82707c46e45b61065d5a6efb5ef73b4e7f(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorUrlParser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29af01b53c238f2d90fd4bc427fca817635ad0c815bd27d96ac35f477e403480(
    *,
    sources: typing.Sequence[builtins.str],
    target: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_encoded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61588ad7916c8fac1cf397a751655ca00760f090a9a082fbbdd978d992b9c582(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd9ee50ba3b35d857c6f0cdd2945234643c43ea2dfb2dbcb4b65fd5a01deee14(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b7b8af8cdc0951e5f99d0f9d23b41f1dc60736858cb37fe9737c571a7ff50d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc781925581e585b997530e60a29ead3c241d445126211c46a8c8058a8c28dda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d561d8cdea8253a7475af9eef6ddc9486deaec54010661d19194b841f2214c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492af60875d2f2f78bdb68f11e5d69652dc07463af6b14e3d018d4b8a88738ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e32838e6de8517b67312327ba1e4fac7cd6ea9a6c365689d97c59c27f5b2b4a(
    value: typing.Optional[LogsCustomPipelineProcessorPipelineProcessorUserAgentParser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6cca9d9a9cbe3ad2987247b67e13964bd885c4df00cb74e2610e0cf86b6253(
    *,
    lookup_enrichment_table: builtins.str,
    source: builtins.str,
    target: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d969205695150cdb2eddf6edb7a579c0f7150e74434f3a4f30fbd4cff9ce65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e18f3e6fe3cd57f460af954ea47089ec63c8591d7991f1956256426570223be(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf4555e2c90d337fc4c45ae7f8c628ef363f475a0fbf916929009f0dc4929af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c6c9f767dd2a821ffdc861c5b78f3060d291acdb124720bfa1c2664d68ffa82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71efda4cbf19f9256a451f89e41c51d0719751ac99e02677fb347602ef07c686(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43dc3761747b9b5f8352390059fa31bc879c7d2a6a739af1d6cc065bc9989416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc19961c4cf615f839b170242c59aecb9056652db4cd518b3a2f4d6ebb59ad9(
    value: typing.Optional[LogsCustomPipelineProcessorReferenceTableLookupProcessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cc4194c29b2a7d94b070a9867a017a3bdc7d0d5b852974151deb6c87e6e26a(
    *,
    sources: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6de88f687dbc073bbc59478c881c2243968b439c06eb9ddb18172ac0ad53ff4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a6144d409e20324020dd22d1990040fa94dc073c1f918db67bd48dfdfe62d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b3d06c63a796724da91acd5fffb3b76c5596af4f1382f69f25b1e4ebf76bc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8ccd56577183d8ff685b5450b42a9fe931c1607fb31cfa5d75788bf306eb37(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bda3550f2b5253f9d37f24412efdc13fb15d5eb012191ea0a41fe306951a67(
    value: typing.Optional[LogsCustomPipelineProcessorServiceRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e40b85d0ecb5219a02c9f9c238ae8a2a047348e3517fe0e81a6422fd4a8fc13(
    *,
    sources: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7feb775571aa45fde3f4e55aca13f3db0e36d815efd3a84915390fc21040c83b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d7ef7d50da25d1872b037a3b67698457d8cf47a90a0bc5a56234c97f1f8e717(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7813688dee4ecc1046ae017c435adc3646eb8a04a301fe2dfab27e34b42c7cb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0e1d3122622c377fb8e3d2a2198b8c8380633210a8c26604a14783ea3628c5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d53fda8b7dabf3666b0a3ad9b802f82d020e2629a428a53e07526992967543(
    value: typing.Optional[LogsCustomPipelineProcessorSpanIdRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd012d0ae3574d49fcd6822968eed258a7d636a90e114efb86003c66877a0692(
    *,
    sources: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f98706500b79e9c4f4a88e52fe842fbf824493085526a5103200e7c6d7cb123(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b59ed9df64b05d0efb7422c621d264c834bc2bca38dc7b8cf829402aa529ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e8958cd38272b7c1ebfe81ac4e3555ff05c554a312ac3ea12354cacff3fd49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5015b67c39ac3ae0c9da08f411e582079e6eafea3ad8cdb62eac5c350ef9bb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec7ef8dc19fbb3cb0135050d1e4b459acef677d3b4db1ec96dab4bc63279153(
    value: typing.Optional[LogsCustomPipelineProcessorStatusRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714aed5a12c145ede8eceb8e65f765b83fbbf3dee8e229aebbb437508a6c44d1(
    *,
    target: builtins.str,
    template: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_replace_missing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c24b0c00cb7ebe4b23cf6cdab34b31e0f47659ef51b563dcb4e50a65d96df11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aae4abda1740a218d42bb736867f5d9e8e603723fb9d2e5280315851e58563c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325a0acb3d51eec1e1aee1010d84b695331b3ce147a1e482a63ed5b0b1d7422e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbe13172c78b0261ca24fbc79d797519ab4364e20554cce892db686ccaf940d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4d19fa5c6aa3d92431482d0ac4d42a841491cf23d9871f57e072b9e928cc6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de28599778071ce041fbd06caf9499633290257b2e9e3b857e0846f3ecf97ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d67de72f0005d4ff47084ac1ff0a4f83d53c34b6507d04a98709780b9512049(
    value: typing.Optional[LogsCustomPipelineProcessorStringBuilderProcessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d858544fd122c10c765f3ab28363fcfc744f7961a33d4e5aaa04e5bc657902(
    *,
    sources: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ceecbad5676b2652ac9f1fafac2262004b0a16976dc2959df25deab24bfe5a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f09a3e45b0c3b18e29dff33ef633e59477e44a6146e68ff23bfcf8bb9d13e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb272769bbdce286c525b5b96a29c6a25bb13e18e67e117fabead6adb2e9af6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59aae166aa8769d6f2acfabd8add5edb19b4eb7bb203da5670ca4385a82d312d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d7173f13d91368c96f10a5613b7da3bcd98c8eb8f149f460e6afbd4afc27fe(
    value: typing.Optional[LogsCustomPipelineProcessorTraceIdRemapper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dedbdfed1ec9e22bc841de9f1b61c79daeb26007d92ba84b48a9230752d504b(
    *,
    sources: typing.Sequence[builtins.str],
    target: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    normalize_ending_slashes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e927b16bd030b74a8407b90b8af0a4bd095394ca5fb594fd0aaa1043418052(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753b3d32ff9dca6ef7b441c7195bd8eb01ddaf70db8a2fc451d0ef3736e5f4f9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db23fcce5ec6e6f74df66cb093c67f4f03ce43e745a503d290bf501d6a5a508b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d166ab7980829192058cfe9eafcfb9a02313add57fef2c1ddd30dd4eef6085a4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ded2419d699408409e6af95884f1e49975a2a8b6909ea3755f266e5803fb6d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d3a14c540578085b82c9e549c67a8568890474f6e948f36b34c42e6ddde143(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb20c83c97f619072e7a55f5ccda982208f7d1d168b7607255c008755256d705(
    value: typing.Optional[LogsCustomPipelineProcessorUrlParser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be12c75880a81edc3e6dcbde2e33211035b5ea2be57bca8fafef3ff7028726a0(
    *,
    sources: typing.Sequence[builtins.str],
    target: builtins.str,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_encoded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3eec1b058514e8d3f84be6ff2c86b0da2c2b93a8b2123e1c58ba67bf5848a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8be1dd1319bac2a87a27c3b70897d855c391f67b1c9e37e50a978dc44310bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b904c3f2aae66cdaa5d14436708f4bdbc3e6320b5079353606776d006bf1068(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c5672cb1a5ddaca44cd79e5ccea7b26628cc308e357b8f7d574f6b4507420b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594906e10d6422f9cf7e3bc7a24c7b137443ea6e1e5c800658b4d3cbb48c7f21(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850ec966fed00458737ab022547e333011ad7d612f5de3030d645e497c1cf4bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010adc0009bdade3c939abfba6593eff4a4f3639207395231b08f93e09a25015(
    value: typing.Optional[LogsCustomPipelineProcessorUserAgentParser],
) -> None:
    """Type checking stubs"""
    pass
