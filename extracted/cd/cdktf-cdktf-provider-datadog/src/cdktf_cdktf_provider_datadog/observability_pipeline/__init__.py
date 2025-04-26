r'''
# `datadog_observability_pipeline`

Refer to the Terraform Registry for docs: [`datadog_observability_pipeline`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline).
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


class ObservabilityPipeline(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipeline",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline datadog_observability_pipeline}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        config: typing.Optional[typing.Union["ObservabilityPipelineConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline datadog_observability_pipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The pipeline name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#name ObservabilityPipeline#name}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#config ObservabilityPipeline#config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee9d464e582ae9a75da04cd684e5ea244fdbe899fe3071650dd3238886db306)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config_ = ObservabilityPipelineConfig(
            name=name,
            config=config,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ObservabilityPipeline resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ObservabilityPipeline to import.
        :param import_from_id: The id of the existing ObservabilityPipeline that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ObservabilityPipeline to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae63d30a4c57c3e8916b0bb55a37a0fe3c1c3b757f634d9aec4d4709eb51e2ad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        destinations: typing.Optional[typing.Union["ObservabilityPipelineConfigDestinations", typing.Dict[builtins.str, typing.Any]]] = None,
        processors: typing.Optional[typing.Union["ObservabilityPipelineConfigProcessors", typing.Dict[builtins.str, typing.Any]]] = None,
        sources: typing.Optional[typing.Union["ObservabilityPipelineConfigSources", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#destinations ObservabilityPipeline#destinations}
        :param processors: processors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#processors ObservabilityPipeline#processors}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#sources ObservabilityPipeline#sources}
        '''
        value = ObservabilityPipelineConfigA(
            destinations=destinations, processors=processors, sources=sources
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

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
    @jsii.member(jsii_name="config")
    def config(self) -> "ObservabilityPipelineConfigAOutputReference":
        return typing.cast("ObservabilityPipelineConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ObservabilityPipelineConfigA"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ObservabilityPipelineConfigA"]], jsii.get(self, "configInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a0d6e8aebcb558877887e4a1468bf5aaf290dffa6ecf66e6dcf4439bd42041f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "config": "config",
    },
)
class ObservabilityPipelineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        config: typing.Optional[typing.Union["ObservabilityPipelineConfigA", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The pipeline name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#name ObservabilityPipeline#name}
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#config ObservabilityPipeline#config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = ObservabilityPipelineConfigA(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b4c775c68f141781e3ef51e8999fecb62f12088f93e8e34e670cb2d92e51a4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if config is not None:
            self._values["config"] = config

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
    def name(self) -> builtins.str:
        '''The pipeline name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#name ObservabilityPipeline#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> typing.Optional["ObservabilityPipelineConfigA"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#config ObservabilityPipeline#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["ObservabilityPipelineConfigA"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "destinations": "destinations",
        "processors": "processors",
        "sources": "sources",
    },
)
class ObservabilityPipelineConfigA:
    def __init__(
        self,
        *,
        destinations: typing.Optional[typing.Union["ObservabilityPipelineConfigDestinations", typing.Dict[builtins.str, typing.Any]]] = None,
        processors: typing.Optional[typing.Union["ObservabilityPipelineConfigProcessors", typing.Dict[builtins.str, typing.Any]]] = None,
        sources: typing.Optional[typing.Union["ObservabilityPipelineConfigSources", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#destinations ObservabilityPipeline#destinations}
        :param processors: processors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#processors ObservabilityPipeline#processors}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#sources ObservabilityPipeline#sources}
        '''
        if isinstance(destinations, dict):
            destinations = ObservabilityPipelineConfigDestinations(**destinations)
        if isinstance(processors, dict):
            processors = ObservabilityPipelineConfigProcessors(**processors)
        if isinstance(sources, dict):
            sources = ObservabilityPipelineConfigSources(**sources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66e7fb77d4a0ebfd34c20f92abdd7c2d541fe8acfad45ad868ed671d5351f48)
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument processors", value=processors, expected_type=type_hints["processors"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destinations is not None:
            self._values["destinations"] = destinations
        if processors is not None:
            self._values["processors"] = processors
        if sources is not None:
            self._values["sources"] = sources

    @builtins.property
    def destinations(
        self,
    ) -> typing.Optional["ObservabilityPipelineConfigDestinations"]:
        '''destinations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#destinations ObservabilityPipeline#destinations}
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional["ObservabilityPipelineConfigDestinations"], result)

    @builtins.property
    def processors(self) -> typing.Optional["ObservabilityPipelineConfigProcessors"]:
        '''processors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#processors ObservabilityPipeline#processors}
        '''
        result = self._values.get("processors")
        return typing.cast(typing.Optional["ObservabilityPipelineConfigProcessors"], result)

    @builtins.property
    def sources(self) -> typing.Optional["ObservabilityPipelineConfigSources"]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#sources ObservabilityPipeline#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional["ObservabilityPipelineConfigSources"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e50c091225c9c55921a02474d1e20134231e0a986b3c223fd7b8d6fabfc37359)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDestinations")
    def put_destinations(
        self,
        *,
        datadog_logs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigDestinationsDatadogLogs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param datadog_logs: datadog_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#datadog_logs ObservabilityPipeline#datadog_logs}
        '''
        value = ObservabilityPipelineConfigDestinations(datadog_logs=datadog_logs)

        return typing.cast(None, jsii.invoke(self, "putDestinations", [value]))

    @jsii.member(jsii_name="putProcessors")
    def put_processors(
        self,
        *,
        add_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsAddFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parse_json: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsParseJson", typing.Dict[builtins.str, typing.Any]]]]] = None,
        quota: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsQuota", typing.Dict[builtins.str, typing.Any]]]]] = None,
        remove_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsRemoveFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rename_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsRenameFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param add_fields: add_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#add_fields ObservabilityPipeline#add_fields}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#filter ObservabilityPipeline#filter}
        :param parse_json: parse_json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#parse_json ObservabilityPipeline#parse_json}
        :param quota: quota block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#quota ObservabilityPipeline#quota}
        :param remove_fields: remove_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#remove_fields ObservabilityPipeline#remove_fields}
        :param rename_fields: rename_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#rename_fields ObservabilityPipeline#rename_fields}
        '''
        value = ObservabilityPipelineConfigProcessors(
            add_fields=add_fields,
            filter=filter,
            parse_json=parse_json,
            quota=quota,
            remove_fields=remove_fields,
            rename_fields=rename_fields,
        )

        return typing.cast(None, jsii.invoke(self, "putProcessors", [value]))

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        *,
        datadog_agent: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigSourcesDatadogAgent", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kafka: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigSourcesKafka", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param datadog_agent: datadog_agent block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#datadog_agent ObservabilityPipeline#datadog_agent}
        :param kafka: kafka block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#kafka ObservabilityPipeline#kafka}
        '''
        value = ObservabilityPipelineConfigSources(
            datadog_agent=datadog_agent, kafka=kafka
        )

        return typing.cast(None, jsii.invoke(self, "putSources", [value]))

    @jsii.member(jsii_name="resetDestinations")
    def reset_destinations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinations", []))

    @jsii.member(jsii_name="resetProcessors")
    def reset_processors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessors", []))

    @jsii.member(jsii_name="resetSources")
    def reset_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSources", []))

    @builtins.property
    @jsii.member(jsii_name="destinations")
    def destinations(self) -> "ObservabilityPipelineConfigDestinationsOutputReference":
        return typing.cast("ObservabilityPipelineConfigDestinationsOutputReference", jsii.get(self, "destinations"))

    @builtins.property
    @jsii.member(jsii_name="processors")
    def processors(self) -> "ObservabilityPipelineConfigProcessorsOutputReference":
        return typing.cast("ObservabilityPipelineConfigProcessorsOutputReference", jsii.get(self, "processors"))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> "ObservabilityPipelineConfigSourcesOutputReference":
        return typing.cast("ObservabilityPipelineConfigSourcesOutputReference", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="destinationsInput")
    def destinations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ObservabilityPipelineConfigDestinations"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ObservabilityPipelineConfigDestinations"]], jsii.get(self, "destinationsInput"))

    @builtins.property
    @jsii.member(jsii_name="processorsInput")
    def processors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ObservabilityPipelineConfigProcessors"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ObservabilityPipelineConfigProcessors"]], jsii.get(self, "processorsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ObservabilityPipelineConfigSources"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ObservabilityPipelineConfigSources"]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigA]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigA]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigA]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb701a3b55e459a4155b0cbce02ff5a2701688f282605ac8e14cf3599cff4cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigDestinations",
    jsii_struct_bases=[],
    name_mapping={"datadog_logs": "datadogLogs"},
)
class ObservabilityPipelineConfigDestinations:
    def __init__(
        self,
        *,
        datadog_logs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigDestinationsDatadogLogs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param datadog_logs: datadog_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#datadog_logs ObservabilityPipeline#datadog_logs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ade6b9ae46e12b43fc9b2b75670b6fa0834fe8bd3c5a5c300bd8a93f9a303c6)
            check_type(argname="argument datadog_logs", value=datadog_logs, expected_type=type_hints["datadog_logs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if datadog_logs is not None:
            self._values["datadog_logs"] = datadog_logs

    @builtins.property
    def datadog_logs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigDestinationsDatadogLogs"]]]:
        '''datadog_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#datadog_logs ObservabilityPipeline#datadog_logs}
        '''
        result = self._values.get("datadog_logs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigDestinationsDatadogLogs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigDestinations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigDestinationsDatadogLogs",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "inputs": "inputs"},
)
class ObservabilityPipelineConfigDestinationsDatadogLogs:
    def __init__(
        self,
        *,
        id: builtins.str,
        inputs: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param id: The unique ID of the destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inputs: The inputs for the destination. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac7dd044594db6b267b5b808b4b6d3114fd6b446568da2576017b50d75475a7)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "inputs": inputs,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique ID of the destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inputs(self) -> typing.List[builtins.str]:
        '''The inputs for the destination.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        '''
        result = self._values.get("inputs")
        assert result is not None, "Required property 'inputs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigDestinationsDatadogLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigDestinationsDatadogLogsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigDestinationsDatadogLogsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5aabd92b775f32011ac2e7c257e22adbcd8f1cc95689369e1bc39040d06b101)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigDestinationsDatadogLogsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7730a2c775288521ccf5fe9a4bf19fbe0208607b7721f4e02690fdaec0813e71)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigDestinationsDatadogLogsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80e697f29b37aa467228bf645facf5643366f52d772a5b26ab343ce57431a98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b37d312314900c4ee7072fe40ad009230acc902afa1f1c79afe052e78176b518)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02d3ae4b31ed8c50bc5f045efbb15e93a74afe9af5d85caf73e21ef7e8f71195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigDestinationsDatadogLogs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigDestinationsDatadogLogs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigDestinationsDatadogLogs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a7af2a4bc4915faa207bf9d70e66986d25038f3950fde7a83fb1bb05d427c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigDestinationsDatadogLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigDestinationsDatadogLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a59e02a3d3fd3807823df3b953ee8ce8489fc4dd14463c24a91ea8304691f9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2412e932c2485a20cb00476081bb7c21bd62c57159657dbfce7459ae074e7447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputs"))

    @inputs.setter
    def inputs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030a941fbd0ab1862c8f1031d29b9bd12dfc521fbad9065c9db6caa73d110383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigDestinationsDatadogLogs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigDestinationsDatadogLogs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigDestinationsDatadogLogs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d59598cc5cfe643183aead5dba514126bc63c910e89924c6b3bb39969841463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigDestinationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigDestinationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d550d7a34086fead61f237cd33a839da16994ae1ae0a6e1ed11052f0f4a0d72d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDatadogLogs")
    def put_datadog_logs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigDestinationsDatadogLogs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5293fc9e077a0355ad40233c6c1dc7cb838d8410b7c8d36324e07285acd173f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDatadogLogs", [value]))

    @jsii.member(jsii_name="resetDatadogLogs")
    def reset_datadog_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadogLogs", []))

    @builtins.property
    @jsii.member(jsii_name="datadogLogs")
    def datadog_logs(self) -> ObservabilityPipelineConfigDestinationsDatadogLogsList:
        return typing.cast(ObservabilityPipelineConfigDestinationsDatadogLogsList, jsii.get(self, "datadogLogs"))

    @builtins.property
    @jsii.member(jsii_name="datadogLogsInput")
    def datadog_logs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigDestinationsDatadogLogs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigDestinationsDatadogLogs]]], jsii.get(self, "datadogLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigDestinations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigDestinations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigDestinations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea7d9c6e23b6786f3a83833e91aeaf27174d080a81114a4ce9ca569d4ebc754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessors",
    jsii_struct_bases=[],
    name_mapping={
        "add_fields": "addFields",
        "filter": "filter",
        "parse_json": "parseJson",
        "quota": "quota",
        "remove_fields": "removeFields",
        "rename_fields": "renameFields",
    },
)
class ObservabilityPipelineConfigProcessors:
    def __init__(
        self,
        *,
        add_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsAddFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parse_json: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsParseJson", typing.Dict[builtins.str, typing.Any]]]]] = None,
        quota: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsQuota", typing.Dict[builtins.str, typing.Any]]]]] = None,
        remove_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsRemoveFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rename_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsRenameFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param add_fields: add_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#add_fields ObservabilityPipeline#add_fields}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#filter ObservabilityPipeline#filter}
        :param parse_json: parse_json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#parse_json ObservabilityPipeline#parse_json}
        :param quota: quota block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#quota ObservabilityPipeline#quota}
        :param remove_fields: remove_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#remove_fields ObservabilityPipeline#remove_fields}
        :param rename_fields: rename_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#rename_fields ObservabilityPipeline#rename_fields}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70735c7949657318d76c2bf80bfb931c6f4d1dda94d21c87d73dbb72b28bbd6b)
            check_type(argname="argument add_fields", value=add_fields, expected_type=type_hints["add_fields"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument parse_json", value=parse_json, expected_type=type_hints["parse_json"])
            check_type(argname="argument quota", value=quota, expected_type=type_hints["quota"])
            check_type(argname="argument remove_fields", value=remove_fields, expected_type=type_hints["remove_fields"])
            check_type(argname="argument rename_fields", value=rename_fields, expected_type=type_hints["rename_fields"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_fields is not None:
            self._values["add_fields"] = add_fields
        if filter is not None:
            self._values["filter"] = filter
        if parse_json is not None:
            self._values["parse_json"] = parse_json
        if quota is not None:
            self._values["quota"] = quota
        if remove_fields is not None:
            self._values["remove_fields"] = remove_fields
        if rename_fields is not None:
            self._values["rename_fields"] = rename_fields

    @builtins.property
    def add_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsAddFields"]]]:
        '''add_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#add_fields ObservabilityPipeline#add_fields}
        '''
        result = self._values.get("add_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsAddFields"]]], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#filter ObservabilityPipeline#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsFilter"]]], result)

    @builtins.property
    def parse_json(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsParseJson"]]]:
        '''parse_json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#parse_json ObservabilityPipeline#parse_json}
        '''
        result = self._values.get("parse_json")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsParseJson"]]], result)

    @builtins.property
    def quota(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsQuota"]]]:
        '''quota block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#quota ObservabilityPipeline#quota}
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsQuota"]]], result)

    @builtins.property
    def remove_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsRemoveFields"]]]:
        '''remove_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#remove_fields ObservabilityPipeline#remove_fields}
        '''
        result = self._values.get("remove_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsRemoveFields"]]], result)

    @builtins.property
    def rename_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsRenameFields"]]]:
        '''rename_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#rename_fields ObservabilityPipeline#rename_fields}
        '''
        result = self._values.get("rename_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsRenameFields"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsAddFields",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "include": "include",
        "inputs": "inputs",
        "field": "field",
    },
)
class ObservabilityPipelineConfigProcessorsAddFields:
    def __init__(
        self,
        *,
        id: builtins.str,
        include: builtins.str,
        inputs: typing.Sequence[builtins.str],
        field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsAddFieldsField", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param id: The unique ID of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include: A Datadog search query used to determine which logs this processor targets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#include ObservabilityPipeline#include}
        :param inputs: The inputs for the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        :param field: field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#field ObservabilityPipeline#field}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec882221963f5a89d0b572d7a253b5286d8ec1586f34630cd95410af7b450ee7)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "include": include,
            "inputs": inputs,
        }
        if field is not None:
            self._values["field"] = field

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique ID of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include(self) -> builtins.str:
        '''A Datadog search query used to determine which logs this processor targets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#include ObservabilityPipeline#include}
        '''
        result = self._values.get("include")
        assert result is not None, "Required property 'include' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inputs(self) -> typing.List[builtins.str]:
        '''The inputs for the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        '''
        result = self._values.get("inputs")
        assert result is not None, "Required property 'inputs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def field(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsAddFieldsField"]]]:
        '''field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#field ObservabilityPipeline#field}
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsAddFieldsField"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessorsAddFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsAddFieldsField",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ObservabilityPipelineConfigProcessorsAddFieldsField:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: The field name to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#name ObservabilityPipeline#name}
        :param value: The value to assign to the field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#value ObservabilityPipeline#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600686e000790fe141c4b2e9f31a997eeb27c1ae29016a70ee2f9bb024b8882d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The field name to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#name ObservabilityPipeline#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value to assign to the field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#value ObservabilityPipeline#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessorsAddFieldsField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigProcessorsAddFieldsFieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsAddFieldsFieldList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eea22baaaf997f47b530aedbdb77dedece5c3a72b557260a40ee672b085dbc28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigProcessorsAddFieldsFieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8af8989953ec21fd676976bf95d9e788028397c8f782e1924a6de55627963b8b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigProcessorsAddFieldsFieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d470c6b76b96c0a12e91798199cbbd58c2f0083008082465a11bc364f70c538)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d601e471588b54eb7d5fd9a807ea80df35c38138454761e0875915f7a7ed951)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac80d78daf186cc48a98a765b2a8bce657aef83bbd86c96a0775da5e9b1227f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsAddFieldsField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsAddFieldsField]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsAddFieldsField]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a7c6fb9a248d529962220c9358b07a9e6d4cee2d8bed25ef1924ec6012798f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsAddFieldsFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsAddFieldsFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd514257793c6b1417da895b0f3960cbc53716d965040a6f1b2f43db13b3242b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe59f9d6ca21f292188709ecad6e967bbec8bd5acaaa33d75a13d1c63b5342e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e8a64b096d7543c1661c2731d0250a3d55dbf21635c2a5d60ff4051f6b9041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsAddFieldsField]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsAddFieldsField]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsAddFieldsField]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a5fa1e5f244b284592e39dcad7f500a8056889dd3c417ab027b2bc666d0406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsAddFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsAddFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60edc1da79c657453aa92b1f92cc2eff87ff145e5776762148e9f67bee8bf13f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigProcessorsAddFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f7ceea9a9dea68d928de1b7e2a0d636b7629c5b7683e3562cf72ccdbe009e5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigProcessorsAddFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51dd999badbccdc780f30205246acde53a27f6b1bde2e4d049e45de046cea47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b14913bfe9577e3e75d3e0d8b97812b11c367ccf969572673b03d4a4565e583)
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
            type_hints = typing.get_type_hints(_typecheckingstub__988f6a54f1372e9637781146883441b110d24d08a293c54e364e173df88c4331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsAddFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsAddFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsAddFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1d4713ceaa4325fb827c97b9a7166961d169c57489360f6d62a2037ab195c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsAddFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsAddFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1bef632bc294d35ecf2433c72376caf1f46b113f26a6002c09e1e040d790a29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putField")
    def put_field(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsAddFieldsField, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5648689dad52e943941378ef4a3922482cc7f3b03518610c80889c4f7426c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putField", [value]))

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> ObservabilityPipelineConfigProcessorsAddFieldsFieldList:
        return typing.cast(ObservabilityPipelineConfigProcessorsAddFieldsFieldList, jsii.get(self, "field"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsAddFieldsField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsAddFieldsField]]], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInput")
    def include_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includeInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3c89075918f33a6017690f0d2c1ca909bce75d0922263006a84ac311981a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "include"))

    @include.setter
    def include(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6034bbf17ed8f841012253083d02e46ea4f403a8d94dcec03c750d13a8bd9c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputs"))

    @inputs.setter
    def inputs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__525101bf03ade027a8c8f30e3dbc6d9ee24d7b242de2b2ebc5b9b62b482dfc16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsAddFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsAddFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsAddFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225e0a72a38b1fba3ba7d9003ca201aa1cd68557f1f4ba940316ca7e3db107bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsFilter",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "include": "include", "inputs": "inputs"},
)
class ObservabilityPipelineConfigProcessorsFilter:
    def __init__(
        self,
        *,
        id: builtins.str,
        include: builtins.str,
        inputs: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param id: The unique ID of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include: A Datadog search query used to determine which logs should pass through the filter. Logs that match this query continue to downstream components; others are dropped. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#include ObservabilityPipeline#include}
        :param inputs: The inputs for the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716f86525bbefc8f88c9c5a55769316492c07ceaa74dc3e5604319633f7d201c)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "include": include,
            "inputs": inputs,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique ID of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include(self) -> builtins.str:
        '''A Datadog search query used to determine which logs should pass through the filter.

        Logs that match this query continue to downstream components; others are dropped.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#include ObservabilityPipeline#include}
        '''
        result = self._values.get("include")
        assert result is not None, "Required property 'include' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inputs(self) -> typing.List[builtins.str]:
        '''The inputs for the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        '''
        result = self._values.get("inputs")
        assert result is not None, "Required property 'inputs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessorsFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigProcessorsFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9db28dd4ce778ffc826e503a8e66b0031f90f7b4cf48cd70b5b4f52d0ff66fbf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigProcessorsFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b4bbfff82c91127486e710ebbf3e5d4d5c503298bdd19f68bff6bd17adcb05)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigProcessorsFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39456daf4e4ba765690302917a9b431fbb9d1f8525628239c0a416e39a2566ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c661995033e9ea205e773acbb5fde7e024b36d026cd17248a41c7843d972f455)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a92d3b6a3da5d9305233d03fb9903f5e8febc6632b8b841f9ade60919040464a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74836f050c984f7b655f6ed99383d318b077ecd52d90cac73dc4673bf422b608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__311395263aa372cd2af8e732dd71d270beea9a567fdbb6dffc04f6812b3a904f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInput")
    def include_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includeInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92ccadc8b0ba1d94afecef670ae4bf9a3200fea3d9e0fcaaffe4ecc72656fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "include"))

    @include.setter
    def include(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__384aca36e8d40d51391afc2de2a3e314892d01fa53cba446853676b4d43ea5d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputs"))

    @inputs.setter
    def inputs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd7a8a540aab0b721cb730d71ce5fcce57a4ae78fe113ef35a40881a4af7fa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58afd2baecdaf1f17c50b4bb91eabb6951fe6a1c5ce253c1f9c9d1167eef1fd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__764fb59c255712a769848254605538637e8209b6b325b57e12da5b9a8d4b814d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAddFields")
    def put_add_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsAddFields, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56a23f8572a89e7bd546299223f1f31eabe1b85e3402e8b5ece17b92f0676ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAddFields", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935e60a76f6721ec781b276968bbb69fb60c2b0e769132ae156c76e3a1573268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putParseJson")
    def put_parse_json(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsParseJson", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d096df1cf9909294a39860ef7e453666a661a518837a7fb96c879a385e1e237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParseJson", [value]))

    @jsii.member(jsii_name="putQuota")
    def put_quota(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsQuota", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b0583498b83607284e690773effd2df58dda1650e1eb5f64239293bb024d070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQuota", [value]))

    @jsii.member(jsii_name="putRemoveFields")
    def put_remove_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsRemoveFields", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e7d6aa18c55f68ebd5db49bd47461a3e385768fb2f3d6f9533fc49b949eed3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRemoveFields", [value]))

    @jsii.member(jsii_name="putRenameFields")
    def put_rename_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsRenameFields", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d90c98f21d09754878289af3f963b70bfc702a9c246e4e65d55d5f92f1e3367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRenameFields", [value]))

    @jsii.member(jsii_name="resetAddFields")
    def reset_add_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddFields", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetParseJson")
    def reset_parse_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseJson", []))

    @jsii.member(jsii_name="resetQuota")
    def reset_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuota", []))

    @jsii.member(jsii_name="resetRemoveFields")
    def reset_remove_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoveFields", []))

    @jsii.member(jsii_name="resetRenameFields")
    def reset_rename_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenameFields", []))

    @builtins.property
    @jsii.member(jsii_name="addFields")
    def add_fields(self) -> ObservabilityPipelineConfigProcessorsAddFieldsList:
        return typing.cast(ObservabilityPipelineConfigProcessorsAddFieldsList, jsii.get(self, "addFields"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> ObservabilityPipelineConfigProcessorsFilterList:
        return typing.cast(ObservabilityPipelineConfigProcessorsFilterList, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="parseJson")
    def parse_json(self) -> "ObservabilityPipelineConfigProcessorsParseJsonList":
        return typing.cast("ObservabilityPipelineConfigProcessorsParseJsonList", jsii.get(self, "parseJson"))

    @builtins.property
    @jsii.member(jsii_name="quota")
    def quota(self) -> "ObservabilityPipelineConfigProcessorsQuotaList":
        return typing.cast("ObservabilityPipelineConfigProcessorsQuotaList", jsii.get(self, "quota"))

    @builtins.property
    @jsii.member(jsii_name="removeFields")
    def remove_fields(self) -> "ObservabilityPipelineConfigProcessorsRemoveFieldsList":
        return typing.cast("ObservabilityPipelineConfigProcessorsRemoveFieldsList", jsii.get(self, "removeFields"))

    @builtins.property
    @jsii.member(jsii_name="renameFields")
    def rename_fields(self) -> "ObservabilityPipelineConfigProcessorsRenameFieldsList":
        return typing.cast("ObservabilityPipelineConfigProcessorsRenameFieldsList", jsii.get(self, "renameFields"))

    @builtins.property
    @jsii.member(jsii_name="addFieldsInput")
    def add_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsAddFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsAddFields]]], jsii.get(self, "addFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsFilter]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="parseJsonInput")
    def parse_json_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsParseJson"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsParseJson"]]], jsii.get(self, "parseJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="quotaInput")
    def quota_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsQuota"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsQuota"]]], jsii.get(self, "quotaInput"))

    @builtins.property
    @jsii.member(jsii_name="removeFieldsInput")
    def remove_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsRemoveFields"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsRemoveFields"]]], jsii.get(self, "removeFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="renameFieldsInput")
    def rename_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsRenameFields"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsRenameFields"]]], jsii.get(self, "renameFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ab56d0be6405c998d21c9f1f24cb2489c20284c3832f2b2827dcf15544669b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsParseJson",
    jsii_struct_bases=[],
    name_mapping={
        "field": "field",
        "id": "id",
        "include": "include",
        "inputs": "inputs",
    },
)
class ObservabilityPipelineConfigProcessorsParseJson:
    def __init__(
        self,
        *,
        field: builtins.str,
        id: builtins.str,
        include: builtins.str,
        inputs: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param field: The field to parse. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#field ObservabilityPipeline#field}
        :param id: The unique ID of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include: A Datadog search query used to determine which logs this processor targets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#include ObservabilityPipeline#include}
        :param inputs: The inputs for the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b5bc2e45530f50f7e6155fbbd9e717db91020a4adb16ac25236468d4cbe4bf)
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field": field,
            "id": id,
            "include": include,
            "inputs": inputs,
        }

    @builtins.property
    def field(self) -> builtins.str:
        '''The field to parse.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#field ObservabilityPipeline#field}
        '''
        result = self._values.get("field")
        assert result is not None, "Required property 'field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique ID of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include(self) -> builtins.str:
        '''A Datadog search query used to determine which logs this processor targets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#include ObservabilityPipeline#include}
        '''
        result = self._values.get("include")
        assert result is not None, "Required property 'include' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inputs(self) -> typing.List[builtins.str]:
        '''The inputs for the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        '''
        result = self._values.get("inputs")
        assert result is not None, "Required property 'inputs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessorsParseJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigProcessorsParseJsonList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsParseJsonList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__186e719237e98dd9468fc5f3d396555198539835ba69a9c6043a19aafda567cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigProcessorsParseJsonOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f49e661318c65408ace7ab0d86aea4d75ce268204e8d754cdff8f2b982cd40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigProcessorsParseJsonOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf19396bd18249b8d42f2f7fe96056d11fbeb384c6a7ab25ea6790c17c6fcfd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af8982381b59af24b78359d20ab7e621c195d358f513d8dd7cc885c94f8f39bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c959e8b9ec85f404ec9662dcff5bde0a5196de6eb199dc17c3098f094462c89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsParseJson]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsParseJson]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsParseJson]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8326003255892efeb15bfad9892bc9bb2df9811bca845747682d1ad9b493bb9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsParseJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsParseJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc2dc5f3ee617c5cd8eb41fee9899d47e1d20f3166605bd7f4a9571a4641958f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInput")
    def include_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includeInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4749f4d338e8014b81b7da4e9e429bd8cb3f7dae67dcdbc5d186366e08306b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d77213b62a62efbc39d9909a3b941244fd3faf2083807ea4eeb610c52d5d863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "include"))

    @include.setter
    def include(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149aab8c1754e41da61a42bb2c0788e747291caeaec6c4785a1e2353a60b923a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputs"))

    @inputs.setter
    def inputs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a718e93ecc18b14dfbf01826d8253feff99d031b13e3927e46f2ec78322d20d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsParseJson]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsParseJson]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsParseJson]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eef630e85c044ebe4a31feb444c3bc43c6292f05150d01562e8229402d0196d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuota",
    jsii_struct_bases=[],
    name_mapping={
        "drop_events": "dropEvents",
        "id": "id",
        "include": "include",
        "inputs": "inputs",
        "limit": "limit",
        "name": "name",
        "ignore_when_missing_partitions": "ignoreWhenMissingPartitions",
        "overrides": "overrides",
        "partition_fields": "partitionFields",
    },
)
class ObservabilityPipelineConfigProcessorsQuota:
    def __init__(
        self,
        *,
        drop_events: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        id: builtins.str,
        include: builtins.str,
        inputs: typing.Sequence[builtins.str],
        limit: typing.Union["ObservabilityPipelineConfigProcessorsQuotaLimit", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        ignore_when_missing_partitions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsQuotaOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        partition_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param drop_events: Whether to drop events exceeding the limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#drop_events ObservabilityPipeline#drop_events}
        :param id: The unique ID of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include: A Datadog search query used to determine which logs this processor targets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#include ObservabilityPipeline#include}
        :param inputs: The inputs for the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        :param limit: limit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#limit ObservabilityPipeline#limit}
        :param name: The name of the quota. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#name ObservabilityPipeline#name}
        :param ignore_when_missing_partitions: Whether to ignore when partition fields are missing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#ignore_when_missing_partitions ObservabilityPipeline#ignore_when_missing_partitions}
        :param overrides: overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#overrides ObservabilityPipeline#overrides}
        :param partition_fields: List of partition fields. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#partition_fields ObservabilityPipeline#partition_fields}
        '''
        if isinstance(limit, dict):
            limit = ObservabilityPipelineConfigProcessorsQuotaLimit(**limit)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c9aa4b8a81ac275740889575040a3ca73ea4d9de7785542bdccb4245941bb4)
            check_type(argname="argument drop_events", value=drop_events, expected_type=type_hints["drop_events"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ignore_when_missing_partitions", value=ignore_when_missing_partitions, expected_type=type_hints["ignore_when_missing_partitions"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument partition_fields", value=partition_fields, expected_type=type_hints["partition_fields"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "drop_events": drop_events,
            "id": id,
            "include": include,
            "inputs": inputs,
            "limit": limit,
            "name": name,
        }
        if ignore_when_missing_partitions is not None:
            self._values["ignore_when_missing_partitions"] = ignore_when_missing_partitions
        if overrides is not None:
            self._values["overrides"] = overrides
        if partition_fields is not None:
            self._values["partition_fields"] = partition_fields

    @builtins.property
    def drop_events(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether to drop events exceeding the limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#drop_events ObservabilityPipeline#drop_events}
        '''
        result = self._values.get("drop_events")
        assert result is not None, "Required property 'drop_events' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique ID of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include(self) -> builtins.str:
        '''A Datadog search query used to determine which logs this processor targets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#include ObservabilityPipeline#include}
        '''
        result = self._values.get("include")
        assert result is not None, "Required property 'include' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inputs(self) -> typing.List[builtins.str]:
        '''The inputs for the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        '''
        result = self._values.get("inputs")
        assert result is not None, "Required property 'inputs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def limit(self) -> "ObservabilityPipelineConfigProcessorsQuotaLimit":
        '''limit block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#limit ObservabilityPipeline#limit}
        '''
        result = self._values.get("limit")
        assert result is not None, "Required property 'limit' is missing"
        return typing.cast("ObservabilityPipelineConfigProcessorsQuotaLimit", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the quota.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#name ObservabilityPipeline#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ignore_when_missing_partitions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to ignore when partition fields are missing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#ignore_when_missing_partitions ObservabilityPipeline#ignore_when_missing_partitions}
        '''
        result = self._values.get("ignore_when_missing_partitions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsQuotaOverrides"]]]:
        '''overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#overrides ObservabilityPipeline#overrides}
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsQuotaOverrides"]]], result)

    @builtins.property
    def partition_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of partition fields.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#partition_fields ObservabilityPipeline#partition_fields}
        '''
        result = self._values.get("partition_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessorsQuota(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuotaLimit",
    jsii_struct_bases=[],
    name_mapping={"enforce": "enforce", "limit": "limit"},
)
class ObservabilityPipelineConfigProcessorsQuotaLimit:
    def __init__(self, *, enforce: builtins.str, limit: jsii.Number) -> None:
        '''
        :param enforce: Whether to enforce by 'bytes' or 'events'. Valid values are ``bytes``, ``events``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#enforce ObservabilityPipeline#enforce}
        :param limit: The daily quota limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#limit ObservabilityPipeline#limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dee7801dfff0c689049c646a00b943dacfc5f5d1cf0d25fd8171ea137e5a92c)
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enforce": enforce,
            "limit": limit,
        }

    @builtins.property
    def enforce(self) -> builtins.str:
        '''Whether to enforce by 'bytes' or 'events'. Valid values are ``bytes``, ``events``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#enforce ObservabilityPipeline#enforce}
        '''
        result = self._values.get("enforce")
        assert result is not None, "Required property 'enforce' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def limit(self) -> jsii.Number:
        '''The daily quota limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#limit ObservabilityPipeline#limit}
        '''
        result = self._values.get("limit")
        assert result is not None, "Required property 'limit' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessorsQuotaLimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigProcessorsQuotaLimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuotaLimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5b17504720e9a9aba6b5ffd55377336d8f9b8466f35881ccc4ac9fda6026afb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3201f014125c53391931a31ce35962fd6c1c97d90607df04a7bf5e1b6d5af07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e1b1d63df48e410e445e20cb36d291c7d7c7a5dcb335d3b5c6a98e4fcf7e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaLimit]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaLimit]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaLimit]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4621719119831a28bb2aa47948aa5f88f15611b4c7b6ffcffe890911bf41d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsQuotaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuotaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4d17f65ac9ee3ca300af5239532466d9db1d850d671ebbd8e41bda2786ae076)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigProcessorsQuotaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbe2b944137feaace52bf3be20be8798915d780df121c1543eef5dd295f42d7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigProcessorsQuotaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101b1ce1e9839098a07300bc2ce7bebfe5a7240f16e2a00b03622c7edbe96246)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ef6464a2f099cacf91198b45d1b00fad70027cec877c5f4a201aff3090f747f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25d39c88b34c3eb33f39ae01cb2d1a8e363d02b63a27a74417a7c0a177fd4ada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuota]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuota]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuota]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__905c6ef0338a922a29fc2d8a98b25863a9b0a593ab4d189e346f096246539436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsQuotaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuotaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65278396386c1d0e5d0de8ce2458c95887618e89ac7df63fbe77f500bd0f68e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLimit")
    def put_limit(self, *, enforce: builtins.str, limit: jsii.Number) -> None:
        '''
        :param enforce: Whether to enforce by 'bytes' or 'events'. Valid values are ``bytes``, ``events``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#enforce ObservabilityPipeline#enforce}
        :param limit: The daily quota limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#limit ObservabilityPipeline#limit}
        '''
        value = ObservabilityPipelineConfigProcessorsQuotaLimit(
            enforce=enforce, limit=limit
        )

        return typing.cast(None, jsii.invoke(self, "putLimit", [value]))

    @jsii.member(jsii_name="putOverrides")
    def put_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsQuotaOverrides", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaaa55c57f073a063c5b01815a6cef741559309c132ad4b7da6c494f7c5dce2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOverrides", [value]))

    @jsii.member(jsii_name="resetIgnoreWhenMissingPartitions")
    def reset_ignore_when_missing_partitions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreWhenMissingPartitions", []))

    @jsii.member(jsii_name="resetOverrides")
    def reset_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrides", []))

    @jsii.member(jsii_name="resetPartitionFields")
    def reset_partition_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionFields", []))

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> ObservabilityPipelineConfigProcessorsQuotaLimitOutputReference:
        return typing.cast(ObservabilityPipelineConfigProcessorsQuotaLimitOutputReference, jsii.get(self, "limit"))

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(self) -> "ObservabilityPipelineConfigProcessorsQuotaOverridesList":
        return typing.cast("ObservabilityPipelineConfigProcessorsQuotaOverridesList", jsii.get(self, "overrides"))

    @builtins.property
    @jsii.member(jsii_name="dropEventsInput")
    def drop_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreWhenMissingPartitionsInput")
    def ignore_when_missing_partitions_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreWhenMissingPartitionsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInput")
    def include_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includeInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaLimit]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaLimit]], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="overridesInput")
    def overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsQuotaOverrides"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsQuotaOverrides"]]], jsii.get(self, "overridesInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionFieldsInput")
    def partition_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "partitionFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="dropEvents")
    def drop_events(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropEvents"))

    @drop_events.setter
    def drop_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f856a1481decc7a1050ad61befa2c93c277a9f60068ba391e668b0d89127b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b45e3c5574ac8a83d9a1c66a08b80f9a562a79337cb2774c47f198065d4c76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreWhenMissingPartitions")
    def ignore_when_missing_partitions(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreWhenMissingPartitions"))

    @ignore_when_missing_partitions.setter
    def ignore_when_missing_partitions(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f9ac205755d2ae845760a7a14ca154e2cccb2f2a7caaa93b824e9a3332e17b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreWhenMissingPartitions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "include"))

    @include.setter
    def include(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02040b0dc50e72121535dcc166552255db592c14e3180a9e8d1b60721d6aca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputs"))

    @inputs.setter
    def inputs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41936c9125ec0231dc429630f3a9fd556ae9f9ea26b396df6b4b1b5f99a7f81a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7f3582625d30e926c8810d38e4d3581c22ff753ca004764a67d4858f7bfe7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionFields")
    def partition_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "partitionFields"))

    @partition_fields.setter
    def partition_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__671fc1c9f0fad990ce74cf7b33b7d9a0d88f36234713306168c89ed3556c4a2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuota]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuota]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuota]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff3305ed3d6c1803c4760aa51654f59ed5896702f613e86e182df31d8264c4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuotaOverrides",
    jsii_struct_bases=[],
    name_mapping={"limit": "limit", "field": "field"},
)
class ObservabilityPipelineConfigProcessorsQuotaOverrides:
    def __init__(
        self,
        *,
        limit: typing.Union["ObservabilityPipelineConfigProcessorsQuotaOverridesLimit", typing.Dict[builtins.str, typing.Any]],
        field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsQuotaOverridesField", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param limit: limit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#limit ObservabilityPipeline#limit}
        :param field: field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#field ObservabilityPipeline#field}
        '''
        if isinstance(limit, dict):
            limit = ObservabilityPipelineConfigProcessorsQuotaOverridesLimit(**limit)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f355cc996fc24ac0f70943d038cd16164e8776d83c4df7c8490f4b7cfa55dbd)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "limit": limit,
        }
        if field is not None:
            self._values["field"] = field

    @builtins.property
    def limit(self) -> "ObservabilityPipelineConfigProcessorsQuotaOverridesLimit":
        '''limit block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#limit ObservabilityPipeline#limit}
        '''
        result = self._values.get("limit")
        assert result is not None, "Required property 'limit' is missing"
        return typing.cast("ObservabilityPipelineConfigProcessorsQuotaOverridesLimit", result)

    @builtins.property
    def field(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsQuotaOverridesField"]]]:
        '''field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#field ObservabilityPipeline#field}
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsQuotaOverridesField"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessorsQuotaOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuotaOverridesField",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ObservabilityPipelineConfigProcessorsQuotaOverridesField:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: The field name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#name ObservabilityPipeline#name}
        :param value: The field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#value ObservabilityPipeline#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61af1950a287739bfec7ec9421099d1bbc57cdef0e3c27c130c0a7a74fd65445)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The field name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#name ObservabilityPipeline#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#value ObservabilityPipeline#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessorsQuotaOverridesField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigProcessorsQuotaOverridesFieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuotaOverridesFieldList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4f51342eb87a9e4827f8b019528d3f6a8827da5012805de5303ca8cf27f06d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigProcessorsQuotaOverridesFieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27647872608485317446c5739734da21bb451fd11d0329a118bc86cbbb6ebee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigProcessorsQuotaOverridesFieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b30fced8be5916b435880ba13b6ee2cc9c52d016954b3e070bed031a061e5f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a4d81c28d339208b5d5d536fd559e117876d8d1aebbcc0ef0490f8ac7ef0304)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0b8f1938e2b00e9e6a77fc265b4b2c29f9026109383a5465f8fcab02bcf1721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuotaOverridesField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuotaOverridesField]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuotaOverridesField]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054ca0043f4cd4b80791b26e44442a1fcc3e134e48c8c95e6bcd662819e73f57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsQuotaOverridesFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuotaOverridesFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d270a7dbd38bade2e82948257ebe1e533608b04624718e3321fb5899b11f3c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc6cf54d93d2bca2ff30853ff466e3ff2c497c3d060f62411b9347d22b4ccdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c2541a7d9e4166f1c0b10708999ae1cd6b1515be8fe1a29658fd061aece745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverridesField]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverridesField]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverridesField]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c61c388fd54d61cfa357e682b66b11a7ba6da2cfa3b25155bf425aa8106982e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuotaOverridesLimit",
    jsii_struct_bases=[],
    name_mapping={"enforce": "enforce", "limit": "limit"},
)
class ObservabilityPipelineConfigProcessorsQuotaOverridesLimit:
    def __init__(self, *, enforce: builtins.str, limit: jsii.Number) -> None:
        '''
        :param enforce: Whether to enforce by 'bytes' or 'events'. Valid values are ``bytes``, ``events``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#enforce ObservabilityPipeline#enforce}
        :param limit: The daily quota limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#limit ObservabilityPipeline#limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db902c552d2bb6c42a48a64cc7557124218afbe8c1029eed7d25000136534b5a)
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enforce": enforce,
            "limit": limit,
        }

    @builtins.property
    def enforce(self) -> builtins.str:
        '''Whether to enforce by 'bytes' or 'events'. Valid values are ``bytes``, ``events``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#enforce ObservabilityPipeline#enforce}
        '''
        result = self._values.get("enforce")
        assert result is not None, "Required property 'enforce' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def limit(self) -> jsii.Number:
        '''The daily quota limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#limit ObservabilityPipeline#limit}
        '''
        result = self._values.get("limit")
        assert result is not None, "Required property 'limit' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessorsQuotaOverridesLimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigProcessorsQuotaOverridesLimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuotaOverridesLimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdfef76d784d00db4e3119037c0502459a82ec9f52e19e47eb8c27852027cafa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforce"))

    @enforce.setter
    def enforce(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14912c8194113e79c47573f65d75953a679c0a5b7b94988b767dba8676f4ee98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd539f8dd64bf8219e2d64702fbc7c388f087038f6aeb3cd4f65eee181fe64f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverridesLimit]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverridesLimit]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverridesLimit]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6aa3362248080f4f1632035003759e899a175cbd9db87e89553ea9d9af5e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsQuotaOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuotaOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a446a772f8343643efac3f7195c111a4f49d922bd14a05eb5393244f26d68891)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigProcessorsQuotaOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18915bda1c7a71a74d1c81c0a2b97d1a35098b3645be1d155a708e3025de4da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigProcessorsQuotaOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192c5871f4a8dbcb2b8fac1841a041d7035e8222d19564222628518e5fa185d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e6a8a01548a5b26af9de1bb871fbc04b64c4e4e5b52fd4901d4db76b9ee944f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__112cc713991a24aaf2158c6965a522d5710d8ca4f0975cdb363e90a85c6bc3c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuotaOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuotaOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuotaOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1964890f3bd2ad429c73e8406634a886b155ec5f8d594e2dc334ad8786a44925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsQuotaOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsQuotaOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbaf9a09e95886f06779c71b9306242b7a5e36d8dbf6b8ebae10bba60a7d7090)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putField")
    def put_field(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsQuotaOverridesField, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9d68a821dadde6c38c7c1199d162a1e928d08c3a567be15e96fa74284664778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putField", [value]))

    @jsii.member(jsii_name="putLimit")
    def put_limit(self, *, enforce: builtins.str, limit: jsii.Number) -> None:
        '''
        :param enforce: Whether to enforce by 'bytes' or 'events'. Valid values are ``bytes``, ``events``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#enforce ObservabilityPipeline#enforce}
        :param limit: The daily quota limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#limit ObservabilityPipeline#limit}
        '''
        value = ObservabilityPipelineConfigProcessorsQuotaOverridesLimit(
            enforce=enforce, limit=limit
        )

        return typing.cast(None, jsii.invoke(self, "putLimit", [value]))

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> ObservabilityPipelineConfigProcessorsQuotaOverridesFieldList:
        return typing.cast(ObservabilityPipelineConfigProcessorsQuotaOverridesFieldList, jsii.get(self, "field"))

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(
        self,
    ) -> ObservabilityPipelineConfigProcessorsQuotaOverridesLimitOutputReference:
        return typing.cast(ObservabilityPipelineConfigProcessorsQuotaOverridesLimitOutputReference, jsii.get(self, "limit"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuotaOverridesField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuotaOverridesField]]], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverridesLimit]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverridesLimit]], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverrides]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverrides]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverrides]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e37887fc23e3b304e78591dc2f7db64c3a1cde339f54511478bb8385ffca07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsRemoveFields",
    jsii_struct_bases=[],
    name_mapping={
        "fields": "fields",
        "id": "id",
        "include": "include",
        "inputs": "inputs",
    },
)
class ObservabilityPipelineConfigProcessorsRemoveFields:
    def __init__(
        self,
        *,
        fields: typing.Sequence[builtins.str],
        id: builtins.str,
        include: builtins.str,
        inputs: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param fields: List of fields to remove from the events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#fields ObservabilityPipeline#fields}
        :param id: The unique ID of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include: A Datadog search query used to determine which logs this processor targets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#include ObservabilityPipeline#include}
        :param inputs: The inputs for the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ad0615220b708f5abd61c8dab0dd9d0cdfb6e0874ae9521118b49a257692b2)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fields": fields,
            "id": id,
            "include": include,
            "inputs": inputs,
        }

    @builtins.property
    def fields(self) -> typing.List[builtins.str]:
        '''List of fields to remove from the events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#fields ObservabilityPipeline#fields}
        '''
        result = self._values.get("fields")
        assert result is not None, "Required property 'fields' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique ID of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include(self) -> builtins.str:
        '''A Datadog search query used to determine which logs this processor targets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#include ObservabilityPipeline#include}
        '''
        result = self._values.get("include")
        assert result is not None, "Required property 'include' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inputs(self) -> typing.List[builtins.str]:
        '''The inputs for the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        '''
        result = self._values.get("inputs")
        assert result is not None, "Required property 'inputs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessorsRemoveFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigProcessorsRemoveFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsRemoveFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c9c809131c784a41ae29a2d766ebda16c163c0b7feb171eba5c97cc12121766)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigProcessorsRemoveFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9149b01001eb8fe263e4df9315582a9dfcf0df249eeeccf18cee0de5252d23e0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigProcessorsRemoveFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe77409dc99b706a81cbac3d4ed98c698f65156c8efa21af48f75587707bccb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__324126a382f2f00328955a132b1fe2b0c3daf599a4c43162f2ad44e628ed45e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__979329cb1543b875992406ffdd426a21ca8cc88d89455dc877aea05cdcc5af52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRemoveFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRemoveFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRemoveFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3955f8117db0a8794a05752120835d2e9cc2703d70e0992234ca43ef819d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsRemoveFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsRemoveFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a9453a2b8752cb825e8b31f5efd74958ab3ee731e8b7bdb8a3271c0bb457c77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="fieldsInput")
    def fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInput")
    def include_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includeInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fields"))

    @fields.setter
    def fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7fb29adbddcd093bfec79a72d38771fe2434fbd3264564cd3fa4e76d7ca9d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51a0a016fe05a3a01691e1a37dd24e28feb798e1b7a102d82c0e359cd9f4738d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "include"))

    @include.setter
    def include(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcba0db3dd4c734e744e26dc27fa70580933bcf7c6b505c8c932f77b58acbf25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputs"))

    @inputs.setter
    def inputs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d9b0bf65b46fdaa8b15f47d643b1e5366af4f8d44af9bf1683ad9cd45da59ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsRemoveFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsRemoveFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsRemoveFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9c33a4bd1916d0cdab24f0fe988152237f66152841a3f13dfc125795983844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsRenameFields",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "include": "include",
        "inputs": "inputs",
        "field": "field",
    },
)
class ObservabilityPipelineConfigProcessorsRenameFields:
    def __init__(
        self,
        *,
        id: builtins.str,
        include: builtins.str,
        inputs: typing.Sequence[builtins.str],
        field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigProcessorsRenameFieldsField", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param id: The unique ID of the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include: A Datadog search query used to determine which logs this processor targets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#include ObservabilityPipeline#include}
        :param inputs: he inputs for the processor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        :param field: field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#field ObservabilityPipeline#field}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849fb1f97819bfd610bcc90a4fa3cfbf8c464ffe831b9a07fcd7438516b944b1)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "include": include,
            "inputs": inputs,
        }
        if field is not None:
            self._values["field"] = field

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique ID of the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include(self) -> builtins.str:
        '''A Datadog search query used to determine which logs this processor targets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#include ObservabilityPipeline#include}
        '''
        result = self._values.get("include")
        assert result is not None, "Required property 'include' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inputs(self) -> typing.List[builtins.str]:
        '''he inputs for the processor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#inputs ObservabilityPipeline#inputs}
        '''
        result = self._values.get("inputs")
        assert result is not None, "Required property 'inputs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def field(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsRenameFieldsField"]]]:
        '''field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#field ObservabilityPipeline#field}
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigProcessorsRenameFieldsField"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessorsRenameFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsRenameFieldsField",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "preserve_source": "preserveSource",
        "source": "source",
    },
)
class ObservabilityPipelineConfigProcessorsRenameFieldsField:
    def __init__(
        self,
        *,
        destination: builtins.str,
        preserve_source: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        source: builtins.str,
    ) -> None:
        '''
        :param destination: Destination field name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#destination ObservabilityPipeline#destination}
        :param preserve_source: Whether to keep the original field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#preserve_source ObservabilityPipeline#preserve_source}
        :param source: Source field to rename. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#source ObservabilityPipeline#source}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec911e68d925c617fd922cac083783e7833f677602ebb88e4c94bd7456820924)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument preserve_source", value=preserve_source, expected_type=type_hints["preserve_source"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "preserve_source": preserve_source,
            "source": source,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Destination field name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#destination ObservabilityPipeline#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def preserve_source(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether to keep the original field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#preserve_source ObservabilityPipeline#preserve_source}
        '''
        result = self._values.get("preserve_source")
        assert result is not None, "Required property 'preserve_source' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Source field to rename.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#source ObservabilityPipeline#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigProcessorsRenameFieldsField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigProcessorsRenameFieldsFieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsRenameFieldsFieldList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f15a43aca17468511a91f7c39e21032e56e79c6d30dda0e206d7aff61143181c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigProcessorsRenameFieldsFieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431847aad0aefd13c0b38390d4ad971c3560f522579ab98cc3b930d20b3ccf34)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigProcessorsRenameFieldsFieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c4018382829499e17e0992b70b9ccd4008da22fe564b97ddbd12b5c88a5462)
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
            type_hints = typing.get_type_hints(_typecheckingstub__444d0b6aca6078ecfd9bb23385d581289243fd1c04ef7b0b159377f9227c9885)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53d57fb6f2a3439cbfeff088df8fcfa6faed091d21f77060c6f12d6081df94b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRenameFieldsField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRenameFieldsField]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRenameFieldsField]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7984c0f51418aea142e787b5d5b72c7c4d094d389d6463b6c6c3c97b9f061b7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsRenameFieldsFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsRenameFieldsFieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe2bb864112d4f75fb9c5f8d23d1fd4fe94b46d118b72387dcc1aed6ff2a3eed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="preserveSourceInput")
    def preserve_source_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preserveSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11f18a0d13e6d6e72364b0a20d6a92cba117f5804c1b24bb65867bb0d13630f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__c91df38a150972186b05915d4cbd99f279d37fb5d744c53231d3a1ca7350f6f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c4b56ca879139b1345e317a4445b72f804c699f63c6efcd01138988887c2dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsRenameFieldsField]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsRenameFieldsField]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsRenameFieldsField]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85975616e971682b360160bd6e110e9fa12333cb2d27540dfd91b1e0e3184099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsRenameFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsRenameFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6672b12f2f5f04ed1ca63131aea669371ee240d74cd979a337a832c5272a152)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigProcessorsRenameFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d356b9b6ca82fd1bf51bf9ece912c324be80ea8b302a800878dd345707bbd9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigProcessorsRenameFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e39459a1c3d47277662c879c209ffaa31cac044c28ced771478783eb9db5408e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a84fa510e4257af026383cf992cd13cc365488a6b418e348b2c4669614786e2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52d9a68e33e2b04cc594f6a34e998c5c77581d41f87cf072182b48582b42c480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRenameFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRenameFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRenameFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6432e01b8081b3bbea81e403e201b33d00fb9ad2096cdad7d375410ba1f3376b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigProcessorsRenameFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigProcessorsRenameFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45aa7c1efbb0e78d154b976ce58edea1332ca80237a6ea736fcf9a57b9f55de8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putField")
    def put_field(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsRenameFieldsField, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1fe62e2a071ceafd68f4a36aab2f942636673b3cc7e39c430b7b26f564a9021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putField", [value]))

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> ObservabilityPipelineConfigProcessorsRenameFieldsFieldList:
        return typing.cast(ObservabilityPipelineConfigProcessorsRenameFieldsFieldList, jsii.get(self, "field"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRenameFieldsField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRenameFieldsField]]], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInput")
    def include_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includeInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__615f64cb9c2152ec249b81444b6a638c302a8a17016bdba5b2757fe2ba1189b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "include"))

    @include.setter
    def include(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58476176361adeafef7afba54f462ddb1281e79233dbc5ea35f6bb795e9c3053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputs"))

    @inputs.setter
    def inputs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48fbf7f172310e68c602a7aaef870db514d47e0a9eee6401dc6b5a0d843801d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsRenameFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsRenameFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsRenameFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e08dae1e73188f72f20016a6682a8ef48c65d986bccc30f8b0a5a269f0faa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSources",
    jsii_struct_bases=[],
    name_mapping={"datadog_agent": "datadogAgent", "kafka": "kafka"},
)
class ObservabilityPipelineConfigSources:
    def __init__(
        self,
        *,
        datadog_agent: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigSourcesDatadogAgent", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kafka: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigSourcesKafka", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param datadog_agent: datadog_agent block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#datadog_agent ObservabilityPipeline#datadog_agent}
        :param kafka: kafka block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#kafka ObservabilityPipeline#kafka}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49015850ddc7b28aa0df549fd07e8652551f233acd25899cb805b635a0122141)
            check_type(argname="argument datadog_agent", value=datadog_agent, expected_type=type_hints["datadog_agent"])
            check_type(argname="argument kafka", value=kafka, expected_type=type_hints["kafka"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if datadog_agent is not None:
            self._values["datadog_agent"] = datadog_agent
        if kafka is not None:
            self._values["kafka"] = kafka

    @builtins.property
    def datadog_agent(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesDatadogAgent"]]]:
        '''datadog_agent block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#datadog_agent ObservabilityPipeline#datadog_agent}
        '''
        result = self._values.get("datadog_agent")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesDatadogAgent"]]], result)

    @builtins.property
    def kafka(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesKafka"]]]:
        '''kafka block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#kafka ObservabilityPipeline#kafka}
        '''
        result = self._values.get("kafka")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesKafka"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesDatadogAgent",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "tls": "tls"},
)
class ObservabilityPipelineConfigSourcesDatadogAgent:
    def __init__(
        self,
        *,
        id: builtins.str,
        tls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigSourcesDatadogAgentTls", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param id: The unique ID of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tls: tls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#tls ObservabilityPipeline#tls}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40201c60390f36fa192eeac8d0af2513cf89c03af6641e65c0f35add37d87ebe)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if tls is not None:
            self._values["tls"] = tls

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique ID of the source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tls(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesDatadogAgentTls"]]]:
        '''tls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#tls ObservabilityPipeline#tls}
        '''
        result = self._values.get("tls")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesDatadogAgentTls"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigSourcesDatadogAgent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigSourcesDatadogAgentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesDatadogAgentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cb4d298dccfbae1a99f65381f3c298ed79508c6b35c88c90a6c352dff1ac84c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigSourcesDatadogAgentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1445b660cfe5960d6e6a6811c74ecff20a88d14b6ae3430099c92d0b9c4cda9d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigSourcesDatadogAgentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92151ad31d93f6e95c11400ceb4d7370170773ed92b7161676add8d88bd557e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22258c5e1a53822dbda8a82930c51bb5fb3dba2f2b02c77ac988ca5799002a70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dac69d6abd36ca22b48c6b2b504f2f465048bb3ee2e0da90803a74d8a55c0e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesDatadogAgent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesDatadogAgent]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesDatadogAgent]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c3c3cb4e6bc2164419addf08f2f631e5ada486ed221af5dcb3c4ebb0d61cd72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigSourcesDatadogAgentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesDatadogAgentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__405f98baa0b8eba74e390c222687507c5ef0ddb82f7a807a62be6e3de9e3b97a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTls")
    def put_tls(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigSourcesDatadogAgentTls", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3472cd349bb4b455f7b9092de4ccc728740ba932e4ec5dd226c4892997814a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTls", [value]))

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(self) -> "ObservabilityPipelineConfigSourcesDatadogAgentTlsList":
        return typing.cast("ObservabilityPipelineConfigSourcesDatadogAgentTlsList", jsii.get(self, "tls"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesDatadogAgentTls"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesDatadogAgentTls"]]], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5dfb5a7b5ce97d2cfc53b6fc85a61b693bd6dc19eece711917b5723d4554b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesDatadogAgent]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesDatadogAgent]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesDatadogAgent]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b5f01fc2a67116df0634133c082a48b04e533c19090f3c0806f9e442696735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesDatadogAgentTls",
    jsii_struct_bases=[],
    name_mapping={"crt_file": "crtFile", "ca_file": "caFile", "key_file": "keyFile"},
)
class ObservabilityPipelineConfigSourcesDatadogAgentTls:
    def __init__(
        self,
        *,
        crt_file: builtins.str,
        ca_file: typing.Optional[builtins.str] = None,
        key_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param crt_file: Path to the TLS client certificate file used to authenticate the pipeline component with upstream or downstream services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#crt_file ObservabilityPipeline#crt_file}
        :param ca_file: Path to the Certificate Authority (CA) file used to validate the server’s TLS certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#ca_file ObservabilityPipeline#ca_file}
        :param key_file: Path to the private key file associated with the TLS client certificate. Used for mutual TLS authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#key_file ObservabilityPipeline#key_file}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1248ce1386d6f6612f15a5abcbbc84d0bb2700663daff7defe11323c2b3baf)
            check_type(argname="argument crt_file", value=crt_file, expected_type=type_hints["crt_file"])
            check_type(argname="argument ca_file", value=ca_file, expected_type=type_hints["ca_file"])
            check_type(argname="argument key_file", value=key_file, expected_type=type_hints["key_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "crt_file": crt_file,
        }
        if ca_file is not None:
            self._values["ca_file"] = ca_file
        if key_file is not None:
            self._values["key_file"] = key_file

    @builtins.property
    def crt_file(self) -> builtins.str:
        '''Path to the TLS client certificate file used to authenticate the pipeline component with upstream or downstream services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#crt_file ObservabilityPipeline#crt_file}
        '''
        result = self._values.get("crt_file")
        assert result is not None, "Required property 'crt_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ca_file(self) -> typing.Optional[builtins.str]:
        '''Path to the Certificate Authority (CA) file used to validate the server’s TLS certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#ca_file ObservabilityPipeline#ca_file}
        '''
        result = self._values.get("ca_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_file(self) -> typing.Optional[builtins.str]:
        '''Path to the private key file associated with the TLS client certificate. Used for mutual TLS authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#key_file ObservabilityPipeline#key_file}
        '''
        result = self._values.get("key_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigSourcesDatadogAgentTls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigSourcesDatadogAgentTlsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesDatadogAgentTlsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ae58c8e8f8f13ffc6df57a64610764a73a6d72c3e9f2ebc1348da7e37b7f21a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigSourcesDatadogAgentTlsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8cff1f518e63762879af6646e2fb1b3adf821dc38bdd573f9a49e2d1bcf17c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigSourcesDatadogAgentTlsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d669a99413db70fef37bb0df2529ea474fc186ffebc064ef401dd30f657cf7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8264a0bc45c82c15e3db3b6c04fbaee568317402e6446c1ff4fda240bbc0a99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e35f67ce3173ef8f23e21b7ef3d505f4d5d6467a5ad2d259c8a2b01fe8ae5a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesDatadogAgentTls]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesDatadogAgentTls]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesDatadogAgentTls]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca95e738bb4e4331451c9c5e5388b21156b10818f465edecb5adc9c4c38b480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigSourcesDatadogAgentTlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesDatadogAgentTlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecc3e40a7e2dfa553b85abdb00d6d8c8a8f2a76e6bb9eacce5beb39f96147cd1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCaFile")
    def reset_ca_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaFile", []))

    @jsii.member(jsii_name="resetKeyFile")
    def reset_key_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyFile", []))

    @builtins.property
    @jsii.member(jsii_name="caFileInput")
    def ca_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caFileInput"))

    @builtins.property
    @jsii.member(jsii_name="crtFileInput")
    def crt_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crtFileInput"))

    @builtins.property
    @jsii.member(jsii_name="keyFileInput")
    def key_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyFileInput"))

    @builtins.property
    @jsii.member(jsii_name="caFile")
    def ca_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caFile"))

    @ca_file.setter
    def ca_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e28492516ef7eaf0ab27516fdc5c328f418ca63e4424193c8061015d58c9c4ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crtFile")
    def crt_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crtFile"))

    @crt_file.setter
    def crt_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96fc24db2aa2d2b693c1a1a605564a7f5ff08a092fc4e3d30aa9dfe39b45f77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crtFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyFile")
    def key_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyFile"))

    @key_file.setter
    def key_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cfa784008904a2745ef31dcaae41ba3d484c2f272c399c9091c6b896226ae86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesDatadogAgentTls]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesDatadogAgentTls]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesDatadogAgentTls]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b3b6172ee837de4bef4f6409a499b47dc989333cccaee51c0584ba943ab43c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesKafka",
    jsii_struct_bases=[],
    name_mapping={
        "group_id": "groupId",
        "id": "id",
        "sasl": "sasl",
        "topics": "topics",
        "librdkafka_option": "librdkafkaOption",
        "tls": "tls",
    },
)
class ObservabilityPipelineConfigSourcesKafka:
    def __init__(
        self,
        *,
        group_id: builtins.str,
        id: builtins.str,
        sasl: typing.Union["ObservabilityPipelineConfigSourcesKafkaSasl", typing.Dict[builtins.str, typing.Any]],
        topics: typing.Sequence[builtins.str],
        librdkafka_option: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigSourcesKafkaTls", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param group_id: The Kafka consumer group ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#group_id ObservabilityPipeline#group_id}
        :param id: The unique ID of the source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param sasl: sasl block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#sasl ObservabilityPipeline#sasl}
        :param topics: A list of Kafka topic names to subscribe to. The source ingests messages from each topic specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#topics ObservabilityPipeline#topics}
        :param librdkafka_option: librdkafka_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#librdkafka_option ObservabilityPipeline#librdkafka_option}
        :param tls: tls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#tls ObservabilityPipeline#tls}
        '''
        if isinstance(sasl, dict):
            sasl = ObservabilityPipelineConfigSourcesKafkaSasl(**sasl)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0bd79b2cf7c0464e23f9c8e94f48bce0ce006e782fa5311b6373760317e8d27)
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument sasl", value=sasl, expected_type=type_hints["sasl"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
            check_type(argname="argument librdkafka_option", value=librdkafka_option, expected_type=type_hints["librdkafka_option"])
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_id": group_id,
            "id": id,
            "sasl": sasl,
            "topics": topics,
        }
        if librdkafka_option is not None:
            self._values["librdkafka_option"] = librdkafka_option
        if tls is not None:
            self._values["tls"] = tls

    @builtins.property
    def group_id(self) -> builtins.str:
        '''The Kafka consumer group ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#group_id ObservabilityPipeline#group_id}
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique ID of the source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#id ObservabilityPipeline#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sasl(self) -> "ObservabilityPipelineConfigSourcesKafkaSasl":
        '''sasl block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#sasl ObservabilityPipeline#sasl}
        '''
        result = self._values.get("sasl")
        assert result is not None, "Required property 'sasl' is missing"
        return typing.cast("ObservabilityPipelineConfigSourcesKafkaSasl", result)

    @builtins.property
    def topics(self) -> typing.List[builtins.str]:
        '''A list of Kafka topic names to subscribe to. The source ingests messages from each topic specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#topics ObservabilityPipeline#topics}
        '''
        result = self._values.get("topics")
        assert result is not None, "Required property 'topics' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def librdkafka_option(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption"]]]:
        '''librdkafka_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#librdkafka_option ObservabilityPipeline#librdkafka_option}
        '''
        result = self._values.get("librdkafka_option")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption"]]], result)

    @builtins.property
    def tls(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesKafkaTls"]]]:
        '''tls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#tls ObservabilityPipeline#tls}
        '''
        result = self._values.get("tls")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesKafkaTls"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigSourcesKafka(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: The name of the librdkafka option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#name ObservabilityPipeline#name}
        :param value: The value of the librdkafka option. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#value ObservabilityPipeline#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5d0624a80c6c222871d6ebe171e184204118a3006ab0b82d2142b3b692e472)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the librdkafka option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#name ObservabilityPipeline#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value of the librdkafka option.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#value ObservabilityPipeline#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOptionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOptionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__815877146f7eeb8059be1007d48c068cedbf6d686e14e473539c943c97d7449a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOptionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e90ed0f87e8b5272e82305d5464228e6088083a2a4a60062971eed7963f750c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOptionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d5d1eeae8368f66982cb98f462bb6de75c6845e73266cb003d46c3c7d58660)
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
            type_hints = typing.get_type_hints(_typecheckingstub__139ed0e40d7546603ce1debbe13e8e10d74f967ea0630b765466578391c762d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9568500e1b3b049446159d7d2b785919f84e9fc68b528263b5ee54e32ce38c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df9a850b4ee7e351ee8265e5db14f076b67dad75411ee00a2d075cdcad2bbf63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__deb6cf15ad8e2384d1a3a62d175c405052c1fceda6fc565812ac6ff17da9abb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d931536ed43a98a1d09cfddf6699b3c98dd0d9a6cf4741b8c6572a8fd07783c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6513f9dcb7f3b77aa3528e1a027158360e02e185b997dbdb7a164c5b0cd6019e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd31d6ee4bfb4f838ef0fbb863aca389c7a22eaa2ea77bb5027c5fcb746f21ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigSourcesKafkaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesKafkaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1e360c55060f7aad4d70cb3f9f4d9d6b4d376e13a44a89b842beee0c44d3912)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigSourcesKafkaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b199d24e78b213791c133e169c79090ca4a4f2dfe6d8fe53c0ec7e4a3c24e6d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigSourcesKafkaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3216732c27083019e24476f70e8fd1f25323408442320f635402ec59203cc7c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc099ed115eee72db525ca2256d4a145d37e9da7e1a22dd94ebb8ee3577d30cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8416d0b954c5f7cca370f6eab77bf27d5be7e1e1d5b068d6513f284462530798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafka]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafka]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafka]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a094957d0e77752b407fcf2f7822652e81f538f8c36440cba328efc207efb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigSourcesKafkaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesKafkaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5b5b34319f083966581dc59835a0f8cac9bfedd865462f47f492a03a386da30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLibrdkafkaOption")
    def put_librdkafka_option(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6948e6a338aa5a7846330e81694d07385095660a4b6d9924621a5f504cb053d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLibrdkafkaOption", [value]))

    @jsii.member(jsii_name="putSasl")
    def put_sasl(self, *, mechanism: builtins.str) -> None:
        '''
        :param mechanism: SASL mechanism to use (e.g., PLAIN, SCRAM-SHA-256, SCRAM-SHA-512). Valid values are ``PLAIN``, ``SCRAM-SHA-256``, ``SCRAM-SHA-512``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#mechanism ObservabilityPipeline#mechanism}
        '''
        value = ObservabilityPipelineConfigSourcesKafkaSasl(mechanism=mechanism)

        return typing.cast(None, jsii.invoke(self, "putSasl", [value]))

    @jsii.member(jsii_name="putTls")
    def put_tls(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ObservabilityPipelineConfigSourcesKafkaTls", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84426544f54b89792c80cdc659c8013cd3f551704061bd6e4f4b4692fbadae75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTls", [value]))

    @jsii.member(jsii_name="resetLibrdkafkaOption")
    def reset_librdkafka_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLibrdkafkaOption", []))

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

    @builtins.property
    @jsii.member(jsii_name="librdkafkaOption")
    def librdkafka_option(
        self,
    ) -> ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOptionList:
        return typing.cast(ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOptionList, jsii.get(self, "librdkafkaOption"))

    @builtins.property
    @jsii.member(jsii_name="sasl")
    def sasl(self) -> "ObservabilityPipelineConfigSourcesKafkaSaslOutputReference":
        return typing.cast("ObservabilityPipelineConfigSourcesKafkaSaslOutputReference", jsii.get(self, "sasl"))

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(self) -> "ObservabilityPipelineConfigSourcesKafkaTlsList":
        return typing.cast("ObservabilityPipelineConfigSourcesKafkaTlsList", jsii.get(self, "tls"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="librdkafkaOptionInput")
    def librdkafka_option_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption]]], jsii.get(self, "librdkafkaOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="saslInput")
    def sasl_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ObservabilityPipelineConfigSourcesKafkaSasl"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ObservabilityPipelineConfigSourcesKafkaSasl"]], jsii.get(self, "saslInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesKafkaTls"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ObservabilityPipelineConfigSourcesKafkaTls"]]], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsInput")
    def topics_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622359c6ffe3a4b3cdf81953983c0654ce8cf870588bfe923ad91b54dabece41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84892662b215c640845022678839bf4f94e724876627d34cee3513d2ef93095b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topics"))

    @topics.setter
    def topics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dfc515f7cade04b03f03c06623e6542a4066f9716d398c0948c9b6b30b4e1d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafka]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafka]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafka]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a8b183bb4fb95dfbbf0c35f44a7253b1c239e0562e6047b9db48fa1969e7d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesKafkaSasl",
    jsii_struct_bases=[],
    name_mapping={"mechanism": "mechanism"},
)
class ObservabilityPipelineConfigSourcesKafkaSasl:
    def __init__(self, *, mechanism: builtins.str) -> None:
        '''
        :param mechanism: SASL mechanism to use (e.g., PLAIN, SCRAM-SHA-256, SCRAM-SHA-512). Valid values are ``PLAIN``, ``SCRAM-SHA-256``, ``SCRAM-SHA-512``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#mechanism ObservabilityPipeline#mechanism}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6e38ce744df0cb92bf762198c4adc184d3b7f046d504de1c3685045cf9735e)
            check_type(argname="argument mechanism", value=mechanism, expected_type=type_hints["mechanism"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mechanism": mechanism,
        }

    @builtins.property
    def mechanism(self) -> builtins.str:
        '''SASL mechanism to use (e.g., PLAIN, SCRAM-SHA-256, SCRAM-SHA-512). Valid values are ``PLAIN``, ``SCRAM-SHA-256``, ``SCRAM-SHA-512``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#mechanism ObservabilityPipeline#mechanism}
        '''
        result = self._values.get("mechanism")
        assert result is not None, "Required property 'mechanism' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigSourcesKafkaSasl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigSourcesKafkaSaslOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesKafkaSaslOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b878721355138368deecd0a1da77a1aa730833afd1439ef23ce898f8740ff10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="mechanismInput")
    def mechanism_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mechanismInput"))

    @builtins.property
    @jsii.member(jsii_name="mechanism")
    def mechanism(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mechanism"))

    @mechanism.setter
    def mechanism(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bbf0f299715faef85571286f43dca85bf3d454bacbb9d8bea2fe4dd521242cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mechanism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafkaSasl]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafkaSasl]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafkaSasl]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db8d1a12cd7c6f6d25049a627cff5006490281ad1b101949eb8dfb106275111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesKafkaTls",
    jsii_struct_bases=[],
    name_mapping={"crt_file": "crtFile", "ca_file": "caFile", "key_file": "keyFile"},
)
class ObservabilityPipelineConfigSourcesKafkaTls:
    def __init__(
        self,
        *,
        crt_file: builtins.str,
        ca_file: typing.Optional[builtins.str] = None,
        key_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param crt_file: Path to the TLS client certificate file used to authenticate the pipeline component with upstream or downstream services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#crt_file ObservabilityPipeline#crt_file}
        :param ca_file: Path to the Certificate Authority (CA) file used to validate the server’s TLS certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#ca_file ObservabilityPipeline#ca_file}
        :param key_file: Path to the private key file associated with the TLS client certificate. Used for mutual TLS authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#key_file ObservabilityPipeline#key_file}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d6c7bbbd7f2b61906e176457cf1a945c1143eb7863214425d60b683a1c10f5)
            check_type(argname="argument crt_file", value=crt_file, expected_type=type_hints["crt_file"])
            check_type(argname="argument ca_file", value=ca_file, expected_type=type_hints["ca_file"])
            check_type(argname="argument key_file", value=key_file, expected_type=type_hints["key_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "crt_file": crt_file,
        }
        if ca_file is not None:
            self._values["ca_file"] = ca_file
        if key_file is not None:
            self._values["key_file"] = key_file

    @builtins.property
    def crt_file(self) -> builtins.str:
        '''Path to the TLS client certificate file used to authenticate the pipeline component with upstream or downstream services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#crt_file ObservabilityPipeline#crt_file}
        '''
        result = self._values.get("crt_file")
        assert result is not None, "Required property 'crt_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ca_file(self) -> typing.Optional[builtins.str]:
        '''Path to the Certificate Authority (CA) file used to validate the server’s TLS certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#ca_file ObservabilityPipeline#ca_file}
        '''
        result = self._values.get("ca_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_file(self) -> typing.Optional[builtins.str]:
        '''Path to the private key file associated with the TLS client certificate. Used for mutual TLS authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/observability_pipeline#key_file ObservabilityPipeline#key_file}
        '''
        result = self._values.get("key_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObservabilityPipelineConfigSourcesKafkaTls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ObservabilityPipelineConfigSourcesKafkaTlsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesKafkaTlsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bd2f6bf94973b8bf754e6fde5266137bc5ef4f8e886a58c89b32c53166b9439)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ObservabilityPipelineConfigSourcesKafkaTlsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46994fdd0bfd059a60591434c42fd128e261a6d313e98cb4d18ad44e9a49e488)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ObservabilityPipelineConfigSourcesKafkaTlsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3754b0bf21ea547e2d9c12fe8903535a7979b5399ab5356bd85261cbb9ccb3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efc50a7460e88c6b68a5fb079cbcd85c21187eee6d4dfd07294f3b395ef36003)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b12249e783d42af849173573d6a7c3276010bbb808f44db9f33f7d1458325dd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafkaTls]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafkaTls]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafkaTls]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e611b48df1b525d09782b43138bef00326305d09d97a61b477ec2efac54782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigSourcesKafkaTlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesKafkaTlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__000a52ce188d0410331c08333ed1ea695f7bd5d94181007456c5386772c41f83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCaFile")
    def reset_ca_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaFile", []))

    @jsii.member(jsii_name="resetKeyFile")
    def reset_key_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyFile", []))

    @builtins.property
    @jsii.member(jsii_name="caFileInput")
    def ca_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caFileInput"))

    @builtins.property
    @jsii.member(jsii_name="crtFileInput")
    def crt_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crtFileInput"))

    @builtins.property
    @jsii.member(jsii_name="keyFileInput")
    def key_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyFileInput"))

    @builtins.property
    @jsii.member(jsii_name="caFile")
    def ca_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caFile"))

    @ca_file.setter
    def ca_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1020ee2daca202835bb81ae76cb11ab4c7c736dd047dec6ee1c5774188162218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crtFile")
    def crt_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crtFile"))

    @crt_file.setter
    def crt_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9e79803cfd9e8e2b214f874bde22baea57ac0242f3c236b5618cb3fd093385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crtFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyFile")
    def key_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyFile"))

    @key_file.setter
    def key_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04250b0879c2d4d54cf4ad0d3e29d8a6d1f5e45a70a47240abe5cd84d46d4fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafkaTls]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafkaTls]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafkaTls]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce2a5a64b073f774d5aa097a3952fed90604f78b678a80e15d859f530f3ee54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ObservabilityPipelineConfigSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.observabilityPipeline.ObservabilityPipelineConfigSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b48de712acdfad9d5d2f7e9f51bf90cfa89a1103c4dbf1922bfaa8590b7dcce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDatadogAgent")
    def put_datadog_agent(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesDatadogAgent, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1a4612504dc0bc02164c43e0fb103a0984d6fe5dc39443dd949f6cb4e2093d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDatadogAgent", [value]))

    @jsii.member(jsii_name="putKafka")
    def put_kafka(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesKafka, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0afd50a302db25761c4c4735ab30449ba0ba4769957bd601ed8b9bfbae9d6e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKafka", [value]))

    @jsii.member(jsii_name="resetDatadogAgent")
    def reset_datadog_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadogAgent", []))

    @jsii.member(jsii_name="resetKafka")
    def reset_kafka(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKafka", []))

    @builtins.property
    @jsii.member(jsii_name="datadogAgent")
    def datadog_agent(self) -> ObservabilityPipelineConfigSourcesDatadogAgentList:
        return typing.cast(ObservabilityPipelineConfigSourcesDatadogAgentList, jsii.get(self, "datadogAgent"))

    @builtins.property
    @jsii.member(jsii_name="kafka")
    def kafka(self) -> ObservabilityPipelineConfigSourcesKafkaList:
        return typing.cast(ObservabilityPipelineConfigSourcesKafkaList, jsii.get(self, "kafka"))

    @builtins.property
    @jsii.member(jsii_name="datadogAgentInput")
    def datadog_agent_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesDatadogAgent]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesDatadogAgent]]], jsii.get(self, "datadogAgentInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaInput")
    def kafka_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafka]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafka]]], jsii.get(self, "kafkaInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b515a1ba47e4634acb7fe55d0b955434b2dc901b54e5b829571084232f32cbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ObservabilityPipeline",
    "ObservabilityPipelineConfig",
    "ObservabilityPipelineConfigA",
    "ObservabilityPipelineConfigAOutputReference",
    "ObservabilityPipelineConfigDestinations",
    "ObservabilityPipelineConfigDestinationsDatadogLogs",
    "ObservabilityPipelineConfigDestinationsDatadogLogsList",
    "ObservabilityPipelineConfigDestinationsDatadogLogsOutputReference",
    "ObservabilityPipelineConfigDestinationsOutputReference",
    "ObservabilityPipelineConfigProcessors",
    "ObservabilityPipelineConfigProcessorsAddFields",
    "ObservabilityPipelineConfigProcessorsAddFieldsField",
    "ObservabilityPipelineConfigProcessorsAddFieldsFieldList",
    "ObservabilityPipelineConfigProcessorsAddFieldsFieldOutputReference",
    "ObservabilityPipelineConfigProcessorsAddFieldsList",
    "ObservabilityPipelineConfigProcessorsAddFieldsOutputReference",
    "ObservabilityPipelineConfigProcessorsFilter",
    "ObservabilityPipelineConfigProcessorsFilterList",
    "ObservabilityPipelineConfigProcessorsFilterOutputReference",
    "ObservabilityPipelineConfigProcessorsOutputReference",
    "ObservabilityPipelineConfigProcessorsParseJson",
    "ObservabilityPipelineConfigProcessorsParseJsonList",
    "ObservabilityPipelineConfigProcessorsParseJsonOutputReference",
    "ObservabilityPipelineConfigProcessorsQuota",
    "ObservabilityPipelineConfigProcessorsQuotaLimit",
    "ObservabilityPipelineConfigProcessorsQuotaLimitOutputReference",
    "ObservabilityPipelineConfigProcessorsQuotaList",
    "ObservabilityPipelineConfigProcessorsQuotaOutputReference",
    "ObservabilityPipelineConfigProcessorsQuotaOverrides",
    "ObservabilityPipelineConfigProcessorsQuotaOverridesField",
    "ObservabilityPipelineConfigProcessorsQuotaOverridesFieldList",
    "ObservabilityPipelineConfigProcessorsQuotaOverridesFieldOutputReference",
    "ObservabilityPipelineConfigProcessorsQuotaOverridesLimit",
    "ObservabilityPipelineConfigProcessorsQuotaOverridesLimitOutputReference",
    "ObservabilityPipelineConfigProcessorsQuotaOverridesList",
    "ObservabilityPipelineConfigProcessorsQuotaOverridesOutputReference",
    "ObservabilityPipelineConfigProcessorsRemoveFields",
    "ObservabilityPipelineConfigProcessorsRemoveFieldsList",
    "ObservabilityPipelineConfigProcessorsRemoveFieldsOutputReference",
    "ObservabilityPipelineConfigProcessorsRenameFields",
    "ObservabilityPipelineConfigProcessorsRenameFieldsField",
    "ObservabilityPipelineConfigProcessorsRenameFieldsFieldList",
    "ObservabilityPipelineConfigProcessorsRenameFieldsFieldOutputReference",
    "ObservabilityPipelineConfigProcessorsRenameFieldsList",
    "ObservabilityPipelineConfigProcessorsRenameFieldsOutputReference",
    "ObservabilityPipelineConfigSources",
    "ObservabilityPipelineConfigSourcesDatadogAgent",
    "ObservabilityPipelineConfigSourcesDatadogAgentList",
    "ObservabilityPipelineConfigSourcesDatadogAgentOutputReference",
    "ObservabilityPipelineConfigSourcesDatadogAgentTls",
    "ObservabilityPipelineConfigSourcesDatadogAgentTlsList",
    "ObservabilityPipelineConfigSourcesDatadogAgentTlsOutputReference",
    "ObservabilityPipelineConfigSourcesKafka",
    "ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption",
    "ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOptionList",
    "ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOptionOutputReference",
    "ObservabilityPipelineConfigSourcesKafkaList",
    "ObservabilityPipelineConfigSourcesKafkaOutputReference",
    "ObservabilityPipelineConfigSourcesKafkaSasl",
    "ObservabilityPipelineConfigSourcesKafkaSaslOutputReference",
    "ObservabilityPipelineConfigSourcesKafkaTls",
    "ObservabilityPipelineConfigSourcesKafkaTlsList",
    "ObservabilityPipelineConfigSourcesKafkaTlsOutputReference",
    "ObservabilityPipelineConfigSourcesOutputReference",
]

publication.publish()

def _typecheckingstub__2ee9d464e582ae9a75da04cd684e5ea244fdbe899fe3071650dd3238886db306(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    config: typing.Optional[typing.Union[ObservabilityPipelineConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ae63d30a4c57c3e8916b0bb55a37a0fe3c1c3b757f634d9aec4d4709eb51e2ad(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d6e8aebcb558877887e4a1468bf5aaf290dffa6ecf66e6dcf4439bd42041f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b4c775c68f141781e3ef51e8999fecb62f12088f93e8e34e670cb2d92e51a4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    config: typing.Optional[typing.Union[ObservabilityPipelineConfigA, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66e7fb77d4a0ebfd34c20f92abdd7c2d541fe8acfad45ad868ed671d5351f48(
    *,
    destinations: typing.Optional[typing.Union[ObservabilityPipelineConfigDestinations, typing.Dict[builtins.str, typing.Any]]] = None,
    processors: typing.Optional[typing.Union[ObservabilityPipelineConfigProcessors, typing.Dict[builtins.str, typing.Any]]] = None,
    sources: typing.Optional[typing.Union[ObservabilityPipelineConfigSources, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50c091225c9c55921a02474d1e20134231e0a986b3c223fd7b8d6fabfc37359(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb701a3b55e459a4155b0cbce02ff5a2701688f282605ac8e14cf3599cff4cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigA]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ade6b9ae46e12b43fc9b2b75670b6fa0834fe8bd3c5a5c300bd8a93f9a303c6(
    *,
    datadog_logs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigDestinationsDatadogLogs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac7dd044594db6b267b5b808b4b6d3114fd6b446568da2576017b50d75475a7(
    *,
    id: builtins.str,
    inputs: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5aabd92b775f32011ac2e7c257e22adbcd8f1cc95689369e1bc39040d06b101(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7730a2c775288521ccf5fe9a4bf19fbe0208607b7721f4e02690fdaec0813e71(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80e697f29b37aa467228bf645facf5643366f52d772a5b26ab343ce57431a98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37d312314900c4ee7072fe40ad009230acc902afa1f1c79afe052e78176b518(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d3ae4b31ed8c50bc5f045efbb15e93a74afe9af5d85caf73e21ef7e8f71195(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a7af2a4bc4915faa207bf9d70e66986d25038f3950fde7a83fb1bb05d427c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigDestinationsDatadogLogs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a59e02a3d3fd3807823df3b953ee8ce8489fc4dd14463c24a91ea8304691f9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2412e932c2485a20cb00476081bb7c21bd62c57159657dbfce7459ae074e7447(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030a941fbd0ab1862c8f1031d29b9bd12dfc521fbad9065c9db6caa73d110383(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d59598cc5cfe643183aead5dba514126bc63c910e89924c6b3bb39969841463(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigDestinationsDatadogLogs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d550d7a34086fead61f237cd33a839da16994ae1ae0a6e1ed11052f0f4a0d72d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5293fc9e077a0355ad40233c6c1dc7cb838d8410b7c8d36324e07285acd173f7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigDestinationsDatadogLogs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea7d9c6e23b6786f3a83833e91aeaf27174d080a81114a4ce9ca569d4ebc754(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigDestinations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70735c7949657318d76c2bf80bfb931c6f4d1dda94d21c87d73dbb72b28bbd6b(
    *,
    add_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsAddFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parse_json: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsParseJson, typing.Dict[builtins.str, typing.Any]]]]] = None,
    quota: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsQuota, typing.Dict[builtins.str, typing.Any]]]]] = None,
    remove_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsRemoveFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rename_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsRenameFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec882221963f5a89d0b572d7a253b5286d8ec1586f34630cd95410af7b450ee7(
    *,
    id: builtins.str,
    include: builtins.str,
    inputs: typing.Sequence[builtins.str],
    field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsAddFieldsField, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600686e000790fe141c4b2e9f31a997eeb27c1ae29016a70ee2f9bb024b8882d(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea22baaaf997f47b530aedbdb77dedece5c3a72b557260a40ee672b085dbc28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af8989953ec21fd676976bf95d9e788028397c8f782e1924a6de55627963b8b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d470c6b76b96c0a12e91798199cbbd58c2f0083008082465a11bc364f70c538(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d601e471588b54eb7d5fd9a807ea80df35c38138454761e0875915f7a7ed951(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac80d78daf186cc48a98a765b2a8bce657aef83bbd86c96a0775da5e9b1227f5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a7c6fb9a248d529962220c9358b07a9e6d4cee2d8bed25ef1924ec6012798f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsAddFieldsField]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd514257793c6b1417da895b0f3960cbc53716d965040a6f1b2f43db13b3242b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe59f9d6ca21f292188709ecad6e967bbec8bd5acaaa33d75a13d1c63b5342e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e8a64b096d7543c1661c2731d0250a3d55dbf21635c2a5d60ff4051f6b9041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a5fa1e5f244b284592e39dcad7f500a8056889dd3c417ab027b2bc666d0406(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsAddFieldsField]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60edc1da79c657453aa92b1f92cc2eff87ff145e5776762148e9f67bee8bf13f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f7ceea9a9dea68d928de1b7e2a0d636b7629c5b7683e3562cf72ccdbe009e5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51dd999badbccdc780f30205246acde53a27f6b1bde2e4d049e45de046cea47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b14913bfe9577e3e75d3e0d8b97812b11c367ccf969572673b03d4a4565e583(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__988f6a54f1372e9637781146883441b110d24d08a293c54e364e173df88c4331(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d4713ceaa4325fb827c97b9a7166961d169c57489360f6d62a2037ab195c0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsAddFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bef632bc294d35ecf2433c72376caf1f46b113f26a6002c09e1e040d790a29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5648689dad52e943941378ef4a3922482cc7f3b03518610c80889c4f7426c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsAddFieldsField, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3c89075918f33a6017690f0d2c1ca909bce75d0922263006a84ac311981a38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6034bbf17ed8f841012253083d02e46ea4f403a8d94dcec03c750d13a8bd9c8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525101bf03ade027a8c8f30e3dbc6d9ee24d7b242de2b2ebc5b9b62b482dfc16(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225e0a72a38b1fba3ba7d9003ca201aa1cd68557f1f4ba940316ca7e3db107bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsAddFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716f86525bbefc8f88c9c5a55769316492c07ceaa74dc3e5604319633f7d201c(
    *,
    id: builtins.str,
    include: builtins.str,
    inputs: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db28dd4ce778ffc826e503a8e66b0031f90f7b4cf48cd70b5b4f52d0ff66fbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b4bbfff82c91127486e710ebbf3e5d4d5c503298bdd19f68bff6bd17adcb05(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39456daf4e4ba765690302917a9b431fbb9d1f8525628239c0a416e39a2566ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c661995033e9ea205e773acbb5fde7e024b36d026cd17248a41c7843d972f455(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92d3b6a3da5d9305233d03fb9903f5e8febc6632b8b841f9ade60919040464a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74836f050c984f7b655f6ed99383d318b077ecd52d90cac73dc4673bf422b608(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311395263aa372cd2af8e732dd71d270beea9a567fdbb6dffc04f6812b3a904f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92ccadc8b0ba1d94afecef670ae4bf9a3200fea3d9e0fcaaffe4ecc72656fe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__384aca36e8d40d51391afc2de2a3e314892d01fa53cba446853676b4d43ea5d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd7a8a540aab0b721cb730d71ce5fcce57a4ae78fe113ef35a40881a4af7fa9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58afd2baecdaf1f17c50b4bb91eabb6951fe6a1c5ce253c1f9c9d1167eef1fd6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764fb59c255712a769848254605538637e8209b6b325b57e12da5b9a8d4b814d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56a23f8572a89e7bd546299223f1f31eabe1b85e3402e8b5ece17b92f0676ec(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsAddFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__935e60a76f6721ec781b276968bbb69fb60c2b0e769132ae156c76e3a1573268(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d096df1cf9909294a39860ef7e453666a661a518837a7fb96c879a385e1e237(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsParseJson, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0583498b83607284e690773effd2df58dda1650e1eb5f64239293bb024d070(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsQuota, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e7d6aa18c55f68ebd5db49bd47461a3e385768fb2f3d6f9533fc49b949eed3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsRemoveFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d90c98f21d09754878289af3f963b70bfc702a9c246e4e65d55d5f92f1e3367(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsRenameFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ab56d0be6405c998d21c9f1f24cb2489c20284c3832f2b2827dcf15544669b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b5bc2e45530f50f7e6155fbbd9e717db91020a4adb16ac25236468d4cbe4bf(
    *,
    field: builtins.str,
    id: builtins.str,
    include: builtins.str,
    inputs: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186e719237e98dd9468fc5f3d396555198539835ba69a9c6043a19aafda567cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f49e661318c65408ace7ab0d86aea4d75ce268204e8d754cdff8f2b982cd40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf19396bd18249b8d42f2f7fe96056d11fbeb384c6a7ab25ea6790c17c6fcfd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8982381b59af24b78359d20ab7e621c195d358f513d8dd7cc885c94f8f39bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c959e8b9ec85f404ec9662dcff5bde0a5196de6eb199dc17c3098f094462c89b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8326003255892efeb15bfad9892bc9bb2df9811bca845747682d1ad9b493bb9d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsParseJson]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2dc5f3ee617c5cd8eb41fee9899d47e1d20f3166605bd7f4a9571a4641958f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4749f4d338e8014b81b7da4e9e429bd8cb3f7dae67dcdbc5d186366e08306b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d77213b62a62efbc39d9909a3b941244fd3faf2083807ea4eeb610c52d5d863(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149aab8c1754e41da61a42bb2c0788e747291caeaec6c4785a1e2353a60b923a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a718e93ecc18b14dfbf01826d8253feff99d031b13e3927e46f2ec78322d20d4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eef630e85c044ebe4a31feb444c3bc43c6292f05150d01562e8229402d0196d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsParseJson]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c9aa4b8a81ac275740889575040a3ca73ea4d9de7785542bdccb4245941bb4(
    *,
    drop_events: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    id: builtins.str,
    include: builtins.str,
    inputs: typing.Sequence[builtins.str],
    limit: typing.Union[ObservabilityPipelineConfigProcessorsQuotaLimit, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    ignore_when_missing_partitions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsQuotaOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    partition_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dee7801dfff0c689049c646a00b943dacfc5f5d1cf0d25fd8171ea137e5a92c(
    *,
    enforce: builtins.str,
    limit: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b17504720e9a9aba6b5ffd55377336d8f9b8466f35881ccc4ac9fda6026afb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3201f014125c53391931a31ce35962fd6c1c97d90607df04a7bf5e1b6d5af07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e1b1d63df48e410e445e20cb36d291c7d7c7a5dcb335d3b5c6a98e4fcf7e38(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4621719119831a28bb2aa47948aa5f88f15611b4c7b6ffcffe890911bf41d5c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaLimit]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d17f65ac9ee3ca300af5239532466d9db1d850d671ebbd8e41bda2786ae076(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbe2b944137feaace52bf3be20be8798915d780df121c1543eef5dd295f42d7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101b1ce1e9839098a07300bc2ce7bebfe5a7240f16e2a00b03622c7edbe96246(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef6464a2f099cacf91198b45d1b00fad70027cec877c5f4a201aff3090f747f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d39c88b34c3eb33f39ae01cb2d1a8e363d02b63a27a74417a7c0a177fd4ada(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905c6ef0338a922a29fc2d8a98b25863a9b0a593ab4d189e346f096246539436(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuota]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65278396386c1d0e5d0de8ce2458c95887618e89ac7df63fbe77f500bd0f68e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaaa55c57f073a063c5b01815a6cef741559309c132ad4b7da6c494f7c5dce2e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsQuotaOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f856a1481decc7a1050ad61befa2c93c277a9f60068ba391e668b0d89127b4e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b45e3c5574ac8a83d9a1c66a08b80f9a562a79337cb2774c47f198065d4c76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f9ac205755d2ae845760a7a14ca154e2cccb2f2a7caaa93b824e9a3332e17b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02040b0dc50e72121535dcc166552255db592c14e3180a9e8d1b60721d6aca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41936c9125ec0231dc429630f3a9fd556ae9f9ea26b396df6b4b1b5f99a7f81a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7f3582625d30e926c8810d38e4d3581c22ff753ca004764a67d4858f7bfe7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671fc1c9f0fad990ce74cf7b33b7d9a0d88f36234713306168c89ed3556c4a2f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff3305ed3d6c1803c4760aa51654f59ed5896702f613e86e182df31d8264c4b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuota]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f355cc996fc24ac0f70943d038cd16164e8776d83c4df7c8490f4b7cfa55dbd(
    *,
    limit: typing.Union[ObservabilityPipelineConfigProcessorsQuotaOverridesLimit, typing.Dict[builtins.str, typing.Any]],
    field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsQuotaOverridesField, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61af1950a287739bfec7ec9421099d1bbc57cdef0e3c27c130c0a7a74fd65445(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f51342eb87a9e4827f8b019528d3f6a8827da5012805de5303ca8cf27f06d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27647872608485317446c5739734da21bb451fd11d0329a118bc86cbbb6ebee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b30fced8be5916b435880ba13b6ee2cc9c52d016954b3e070bed031a061e5f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4d81c28d339208b5d5d536fd559e117876d8d1aebbcc0ef0490f8ac7ef0304(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b8f1938e2b00e9e6a77fc265b4b2c29f9026109383a5465f8fcab02bcf1721(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054ca0043f4cd4b80791b26e44442a1fcc3e134e48c8c95e6bcd662819e73f57(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuotaOverridesField]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d270a7dbd38bade2e82948257ebe1e533608b04624718e3321fb5899b11f3c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc6cf54d93d2bca2ff30853ff466e3ff2c497c3d060f62411b9347d22b4ccdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c2541a7d9e4166f1c0b10708999ae1cd6b1515be8fe1a29658fd061aece745(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c61c388fd54d61cfa357e682b66b11a7ba6da2cfa3b25155bf425aa8106982e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverridesField]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db902c552d2bb6c42a48a64cc7557124218afbe8c1029eed7d25000136534b5a(
    *,
    enforce: builtins.str,
    limit: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfef76d784d00db4e3119037c0502459a82ec9f52e19e47eb8c27852027cafa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14912c8194113e79c47573f65d75953a679c0a5b7b94988b767dba8676f4ee98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd539f8dd64bf8219e2d64702fbc7c388f087038f6aeb3cd4f65eee181fe64f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6aa3362248080f4f1632035003759e899a175cbd9db87e89553ea9d9af5e75(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverridesLimit]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a446a772f8343643efac3f7195c111a4f49d922bd14a05eb5393244f26d68891(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18915bda1c7a71a74d1c81c0a2b97d1a35098b3645be1d155a708e3025de4da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192c5871f4a8dbcb2b8fac1841a041d7035e8222d19564222628518e5fa185d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6a8a01548a5b26af9de1bb871fbc04b64c4e4e5b52fd4901d4db76b9ee944f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__112cc713991a24aaf2158c6965a522d5710d8ca4f0975cdb363e90a85c6bc3c8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1964890f3bd2ad429c73e8406634a886b155ec5f8d594e2dc334ad8786a44925(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsQuotaOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbaf9a09e95886f06779c71b9306242b7a5e36d8dbf6b8ebae10bba60a7d7090(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d68a821dadde6c38c7c1199d162a1e928d08c3a567be15e96fa74284664778(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsQuotaOverridesField, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e37887fc23e3b304e78591dc2f7db64c3a1cde339f54511478bb8385ffca07a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsQuotaOverrides]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ad0615220b708f5abd61c8dab0dd9d0cdfb6e0874ae9521118b49a257692b2(
    *,
    fields: typing.Sequence[builtins.str],
    id: builtins.str,
    include: builtins.str,
    inputs: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9c809131c784a41ae29a2d766ebda16c163c0b7feb171eba5c97cc12121766(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9149b01001eb8fe263e4df9315582a9dfcf0df249eeeccf18cee0de5252d23e0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe77409dc99b706a81cbac3d4ed98c698f65156c8efa21af48f75587707bccb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324126a382f2f00328955a132b1fe2b0c3daf599a4c43162f2ad44e628ed45e4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979329cb1543b875992406ffdd426a21ca8cc88d89455dc877aea05cdcc5af52(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3955f8117db0a8794a05752120835d2e9cc2703d70e0992234ca43ef819d07(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRemoveFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9453a2b8752cb825e8b31f5efd74958ab3ee731e8b7bdb8a3271c0bb457c77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7fb29adbddcd093bfec79a72d38771fe2434fbd3264564cd3fa4e76d7ca9d1e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a0a016fe05a3a01691e1a37dd24e28feb798e1b7a102d82c0e359cd9f4738d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcba0db3dd4c734e744e26dc27fa70580933bcf7c6b505c8c932f77b58acbf25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d9b0bf65b46fdaa8b15f47d643b1e5366af4f8d44af9bf1683ad9cd45da59ac(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9c33a4bd1916d0cdab24f0fe988152237f66152841a3f13dfc125795983844(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsRemoveFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849fb1f97819bfd610bcc90a4fa3cfbf8c464ffe831b9a07fcd7438516b944b1(
    *,
    id: builtins.str,
    include: builtins.str,
    inputs: typing.Sequence[builtins.str],
    field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsRenameFieldsField, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec911e68d925c617fd922cac083783e7833f677602ebb88e4c94bd7456820924(
    *,
    destination: builtins.str,
    preserve_source: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    source: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f15a43aca17468511a91f7c39e21032e56e79c6d30dda0e206d7aff61143181c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431847aad0aefd13c0b38390d4ad971c3560f522579ab98cc3b930d20b3ccf34(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c4018382829499e17e0992b70b9ccd4008da22fe564b97ddbd12b5c88a5462(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444d0b6aca6078ecfd9bb23385d581289243fd1c04ef7b0b159377f9227c9885(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d57fb6f2a3439cbfeff088df8fcfa6faed091d21f77060c6f12d6081df94b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7984c0f51418aea142e787b5d5b72c7c4d094d389d6463b6c6c3c97b9f061b7a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRenameFieldsField]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2bb864112d4f75fb9c5f8d23d1fd4fe94b46d118b72387dcc1aed6ff2a3eed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11f18a0d13e6d6e72364b0a20d6a92cba117f5804c1b24bb65867bb0d13630f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91df38a150972186b05915d4cbd99f279d37fb5d744c53231d3a1ca7350f6f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c4b56ca879139b1345e317a4445b72f804c699f63c6efcd01138988887c2dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85975616e971682b360160bd6e110e9fa12333cb2d27540dfd91b1e0e3184099(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsRenameFieldsField]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6672b12f2f5f04ed1ca63131aea669371ee240d74cd979a337a832c5272a152(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d356b9b6ca82fd1bf51bf9ece912c324be80ea8b302a800878dd345707bbd9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39459a1c3d47277662c879c209ffaa31cac044c28ced771478783eb9db5408e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84fa510e4257af026383cf992cd13cc365488a6b418e348b2c4669614786e2d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d9a68e33e2b04cc594f6a34e998c5c77581d41f87cf072182b48582b42c480(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6432e01b8081b3bbea81e403e201b33d00fb9ad2096cdad7d375410ba1f3376b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigProcessorsRenameFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45aa7c1efbb0e78d154b976ce58edea1332ca80237a6ea736fcf9a57b9f55de8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fe62e2a071ceafd68f4a36aab2f942636673b3cc7e39c430b7b26f564a9021(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigProcessorsRenameFieldsField, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615f64cb9c2152ec249b81444b6a638c302a8a17016bdba5b2757fe2ba1189b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58476176361adeafef7afba54f462ddb1281e79233dbc5ea35f6bb795e9c3053(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48fbf7f172310e68c602a7aaef870db514d47e0a9eee6401dc6b5a0d843801d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e08dae1e73188f72f20016a6682a8ef48c65d986bccc30f8b0a5a269f0faa4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigProcessorsRenameFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49015850ddc7b28aa0df549fd07e8652551f233acd25899cb805b635a0122141(
    *,
    datadog_agent: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesDatadogAgent, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kafka: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesKafka, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40201c60390f36fa192eeac8d0af2513cf89c03af6641e65c0f35add37d87ebe(
    *,
    id: builtins.str,
    tls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesDatadogAgentTls, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb4d298dccfbae1a99f65381f3c298ed79508c6b35c88c90a6c352dff1ac84c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1445b660cfe5960d6e6a6811c74ecff20a88d14b6ae3430099c92d0b9c4cda9d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92151ad31d93f6e95c11400ceb4d7370170773ed92b7161676add8d88bd557e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22258c5e1a53822dbda8a82930c51bb5fb3dba2f2b02c77ac988ca5799002a70(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac69d6abd36ca22b48c6b2b504f2f465048bb3ee2e0da90803a74d8a55c0e8d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3c3cb4e6bc2164419addf08f2f631e5ada486ed221af5dcb3c4ebb0d61cd72(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesDatadogAgent]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405f98baa0b8eba74e390c222687507c5ef0ddb82f7a807a62be6e3de9e3b97a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3472cd349bb4b455f7b9092de4ccc728740ba932e4ec5dd226c4892997814a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesDatadogAgentTls, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5dfb5a7b5ce97d2cfc53b6fc85a61b693bd6dc19eece711917b5723d4554b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b5f01fc2a67116df0634133c082a48b04e533c19090f3c0806f9e442696735(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesDatadogAgent]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1248ce1386d6f6612f15a5abcbbc84d0bb2700663daff7defe11323c2b3baf(
    *,
    crt_file: builtins.str,
    ca_file: typing.Optional[builtins.str] = None,
    key_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae58c8e8f8f13ffc6df57a64610764a73a6d72c3e9f2ebc1348da7e37b7f21a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8cff1f518e63762879af6646e2fb1b3adf821dc38bdd573f9a49e2d1bcf17c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d669a99413db70fef37bb0df2529ea474fc186ffebc064ef401dd30f657cf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8264a0bc45c82c15e3db3b6c04fbaee568317402e6446c1ff4fda240bbc0a99(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35f67ce3173ef8f23e21b7ef3d505f4d5d6467a5ad2d259c8a2b01fe8ae5a29(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca95e738bb4e4331451c9c5e5388b21156b10818f465edecb5adc9c4c38b480(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesDatadogAgentTls]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc3e40a7e2dfa553b85abdb00d6d8c8a8f2a76e6bb9eacce5beb39f96147cd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e28492516ef7eaf0ab27516fdc5c328f418ca63e4424193c8061015d58c9c4ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96fc24db2aa2d2b693c1a1a605564a7f5ff08a092fc4e3d30aa9dfe39b45f77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cfa784008904a2745ef31dcaae41ba3d484c2f272c399c9091c6b896226ae86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3b6172ee837de4bef4f6409a499b47dc989333cccaee51c0584ba943ab43c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesDatadogAgentTls]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0bd79b2cf7c0464e23f9c8e94f48bce0ce006e782fa5311b6373760317e8d27(
    *,
    group_id: builtins.str,
    id: builtins.str,
    sasl: typing.Union[ObservabilityPipelineConfigSourcesKafkaSasl, typing.Dict[builtins.str, typing.Any]],
    topics: typing.Sequence[builtins.str],
    librdkafka_option: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tls: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesKafkaTls, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5d0624a80c6c222871d6ebe171e184204118a3006ab0b82d2142b3b692e472(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815877146f7eeb8059be1007d48c068cedbf6d686e14e473539c943c97d7449a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e90ed0f87e8b5272e82305d5464228e6088083a2a4a60062971eed7963f750c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d5d1eeae8368f66982cb98f462bb6de75c6845e73266cb003d46c3c7d58660(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139ed0e40d7546603ce1debbe13e8e10d74f967ea0630b765466578391c762d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9568500e1b3b049446159d7d2b785919f84e9fc68b528263b5ee54e32ce38c64(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df9a850b4ee7e351ee8265e5db14f076b67dad75411ee00a2d075cdcad2bbf63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb6cf15ad8e2384d1a3a62d175c405052c1fceda6fc565812ac6ff17da9abb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d931536ed43a98a1d09cfddf6699b3c98dd0d9a6cf4741b8c6572a8fd07783c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6513f9dcb7f3b77aa3528e1a027158360e02e185b997dbdb7a164c5b0cd6019e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd31d6ee4bfb4f838ef0fbb863aca389c7a22eaa2ea77bb5027c5fcb746f21ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e360c55060f7aad4d70cb3f9f4d9d6b4d376e13a44a89b842beee0c44d3912(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b199d24e78b213791c133e169c79090ca4a4f2dfe6d8fe53c0ec7e4a3c24e6d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3216732c27083019e24476f70e8fd1f25323408442320f635402ec59203cc7c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc099ed115eee72db525ca2256d4a145d37e9da7e1a22dd94ebb8ee3577d30cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8416d0b954c5f7cca370f6eab77bf27d5be7e1e1d5b068d6513f284462530798(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a094957d0e77752b407fcf2f7822652e81f538f8c36440cba328efc207efb6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafka]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b5b34319f083966581dc59835a0f8cac9bfedd865462f47f492a03a386da30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6948e6a338aa5a7846330e81694d07385095660a4b6d9924621a5f504cb053d7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesKafkaLibrdkafkaOption, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84426544f54b89792c80cdc659c8013cd3f551704061bd6e4f4b4692fbadae75(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesKafkaTls, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622359c6ffe3a4b3cdf81953983c0654ce8cf870588bfe923ad91b54dabece41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84892662b215c640845022678839bf4f94e724876627d34cee3513d2ef93095b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dfc515f7cade04b03f03c06623e6542a4066f9716d398c0948c9b6b30b4e1d7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8b183bb4fb95dfbbf0c35f44a7253b1c239e0562e6047b9db48fa1969e7d10(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafka]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6e38ce744df0cb92bf762198c4adc184d3b7f046d504de1c3685045cf9735e(
    *,
    mechanism: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b878721355138368deecd0a1da77a1aa730833afd1439ef23ce898f8740ff10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbf0f299715faef85571286f43dca85bf3d454bacbb9d8bea2fe4dd521242cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db8d1a12cd7c6f6d25049a627cff5006490281ad1b101949eb8dfb106275111(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafkaSasl]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d6c7bbbd7f2b61906e176457cf1a945c1143eb7863214425d60b683a1c10f5(
    *,
    crt_file: builtins.str,
    ca_file: typing.Optional[builtins.str] = None,
    key_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd2f6bf94973b8bf754e6fde5266137bc5ef4f8e886a58c89b32c53166b9439(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46994fdd0bfd059a60591434c42fd128e261a6d313e98cb4d18ad44e9a49e488(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3754b0bf21ea547e2d9c12fe8903535a7979b5399ab5356bd85261cbb9ccb3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc50a7460e88c6b68a5fb079cbcd85c21187eee6d4dfd07294f3b395ef36003(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12249e783d42af849173573d6a7c3276010bbb808f44db9f33f7d1458325dd4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e611b48df1b525d09782b43138bef00326305d09d97a61b477ec2efac54782(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ObservabilityPipelineConfigSourcesKafkaTls]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000a52ce188d0410331c08333ed1ea695f7bd5d94181007456c5386772c41f83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1020ee2daca202835bb81ae76cb11ab4c7c736dd047dec6ee1c5774188162218(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9e79803cfd9e8e2b214f874bde22baea57ac0242f3c236b5618cb3fd093385(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04250b0879c2d4d54cf4ad0d3e29d8a6d1f5e45a70a47240abe5cd84d46d4fb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce2a5a64b073f774d5aa097a3952fed90604f78b678a80e15d859f530f3ee54(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSourcesKafkaTls]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b48de712acdfad9d5d2f7e9f51bf90cfa89a1103c4dbf1922bfaa8590b7dcce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1a4612504dc0bc02164c43e0fb103a0984d6fe5dc39443dd949f6cb4e2093d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesDatadogAgent, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0afd50a302db25761c4c4735ab30449ba0ba4769957bd601ed8b9bfbae9d6e63(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ObservabilityPipelineConfigSourcesKafka, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b515a1ba47e4634acb7fe55d0b955434b2dc901b54e5b829571084232f32cbd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ObservabilityPipelineConfigSources]],
) -> None:
    """Type checking stubs"""
    pass
