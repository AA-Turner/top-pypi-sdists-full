r'''
# `aws_accessanalyzer_analyzer`

Refer to the Terraform Registry for docs: [`aws_accessanalyzer_analyzer`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer).
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


class AccessanalyzerAnalyzer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzer",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer aws_accessanalyzer_analyzer}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        analyzer_name: builtins.str,
        configuration: typing.Optional[typing.Union["AccessanalyzerAnalyzerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer aws_accessanalyzer_analyzer} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param analyzer_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#analyzer_name AccessanalyzerAnalyzer#analyzer_name}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#configuration AccessanalyzerAnalyzer#configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#id AccessanalyzerAnalyzer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#region AccessanalyzerAnalyzer#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#tags AccessanalyzerAnalyzer#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#tags_all AccessanalyzerAnalyzer#tags_all}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#type AccessanalyzerAnalyzer#type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6367f3d990e3d4c27e0182a7de91e44b74a4d456fd1f83446e0f157fce93af04)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessanalyzerAnalyzerConfig(
            analyzer_name=analyzer_name,
            configuration=configuration,
            id=id,
            region=region,
            tags=tags,
            tags_all=tags_all,
            type=type,
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
        '''Generates CDKTF code for importing a AccessanalyzerAnalyzer resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessanalyzerAnalyzer to import.
        :param import_from_id: The id of the existing AccessanalyzerAnalyzer that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessanalyzerAnalyzer to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23f310473f23d09087c667c7325e075fe84cdd39bfff8f8f2e5ef14bef0ffe25)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfiguration")
    def put_configuration(
        self,
        *,
        internal_access: typing.Optional[typing.Union["AccessanalyzerAnalyzerConfigurationInternalAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        unused_access: typing.Optional[typing.Union["AccessanalyzerAnalyzerConfigurationUnusedAccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param internal_access: internal_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#internal_access AccessanalyzerAnalyzer#internal_access}
        :param unused_access: unused_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#unused_access AccessanalyzerAnalyzer#unused_access}
        '''
        value = AccessanalyzerAnalyzerConfiguration(
            internal_access=internal_access, unused_access=unused_access
        )

        return typing.cast(None, jsii.invoke(self, "putConfiguration", [value]))

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> "AccessanalyzerAnalyzerConfigurationOutputReference":
        return typing.cast("AccessanalyzerAnalyzerConfigurationOutputReference", jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="analyzerNameInput")
    def analyzer_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "analyzerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(
        self,
    ) -> typing.Optional["AccessanalyzerAnalyzerConfiguration"]:
        return typing.cast(typing.Optional["AccessanalyzerAnalyzerConfiguration"], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="analyzerName")
    def analyzer_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "analyzerName"))

    @analyzer_name.setter
    def analyzer_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c2d54cdbddf07ebb862693ae46888178f7405a808a16c8eb561d99f480d7d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "analyzerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb580d614c09ec5df505b717e62279dfb53c2c84a335676add7bab1f231546c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5b29128b95f0437864fdcba031d685f0f460753fa5485bab8aa427d1abd67f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1489106da4731ce078e8cb1260e11b8caed7b0a2f42becf60bcc666cefb6d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a40d49759e687bd503263d803626d09e922ff6b624d718b4745370221a14da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df092ef4230e9f50676b99d34519028b026f148e0988080a99e206fee7d45e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "analyzer_name": "analyzerName",
        "configuration": "configuration",
        "id": "id",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "type": "type",
    },
)
class AccessanalyzerAnalyzerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        analyzer_name: builtins.str,
        configuration: typing.Optional[typing.Union["AccessanalyzerAnalyzerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param analyzer_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#analyzer_name AccessanalyzerAnalyzer#analyzer_name}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#configuration AccessanalyzerAnalyzer#configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#id AccessanalyzerAnalyzer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#region AccessanalyzerAnalyzer#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#tags AccessanalyzerAnalyzer#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#tags_all AccessanalyzerAnalyzer#tags_all}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#type AccessanalyzerAnalyzer#type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(configuration, dict):
            configuration = AccessanalyzerAnalyzerConfiguration(**configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d92b63429984ba04f72b40d1b14bc95abd1d4449d5f68d2460fe85c57ea7db0a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument analyzer_name", value=analyzer_name, expected_type=type_hints["analyzer_name"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "analyzer_name": analyzer_name,
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
        if configuration is not None:
            self._values["configuration"] = configuration
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if type is not None:
            self._values["type"] = type

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
    def analyzer_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#analyzer_name AccessanalyzerAnalyzer#analyzer_name}.'''
        result = self._values.get("analyzer_name")
        assert result is not None, "Required property 'analyzer_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(self) -> typing.Optional["AccessanalyzerAnalyzerConfiguration"]:
        '''configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#configuration AccessanalyzerAnalyzer#configuration}
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional["AccessanalyzerAnalyzerConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#id AccessanalyzerAnalyzer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#region AccessanalyzerAnalyzer#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#tags AccessanalyzerAnalyzer#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#tags_all AccessanalyzerAnalyzer#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#type AccessanalyzerAnalyzer#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessanalyzerAnalyzerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "internal_access": "internalAccess",
        "unused_access": "unusedAccess",
    },
)
class AccessanalyzerAnalyzerConfiguration:
    def __init__(
        self,
        *,
        internal_access: typing.Optional[typing.Union["AccessanalyzerAnalyzerConfigurationInternalAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        unused_access: typing.Optional[typing.Union["AccessanalyzerAnalyzerConfigurationUnusedAccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param internal_access: internal_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#internal_access AccessanalyzerAnalyzer#internal_access}
        :param unused_access: unused_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#unused_access AccessanalyzerAnalyzer#unused_access}
        '''
        if isinstance(internal_access, dict):
            internal_access = AccessanalyzerAnalyzerConfigurationInternalAccess(**internal_access)
        if isinstance(unused_access, dict):
            unused_access = AccessanalyzerAnalyzerConfigurationUnusedAccess(**unused_access)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f033844b2b3d740c06e4ffa098dc10142e959e3632af5ed852d7dc9d6777bddb)
            check_type(argname="argument internal_access", value=internal_access, expected_type=type_hints["internal_access"])
            check_type(argname="argument unused_access", value=unused_access, expected_type=type_hints["unused_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if internal_access is not None:
            self._values["internal_access"] = internal_access
        if unused_access is not None:
            self._values["unused_access"] = unused_access

    @builtins.property
    def internal_access(
        self,
    ) -> typing.Optional["AccessanalyzerAnalyzerConfigurationInternalAccess"]:
        '''internal_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#internal_access AccessanalyzerAnalyzer#internal_access}
        '''
        result = self._values.get("internal_access")
        return typing.cast(typing.Optional["AccessanalyzerAnalyzerConfigurationInternalAccess"], result)

    @builtins.property
    def unused_access(
        self,
    ) -> typing.Optional["AccessanalyzerAnalyzerConfigurationUnusedAccess"]:
        '''unused_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#unused_access AccessanalyzerAnalyzer#unused_access}
        '''
        result = self._values.get("unused_access")
        return typing.cast(typing.Optional["AccessanalyzerAnalyzerConfigurationUnusedAccess"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessanalyzerAnalyzerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationInternalAccess",
    jsii_struct_bases=[],
    name_mapping={"analysis_rule": "analysisRule"},
)
class AccessanalyzerAnalyzerConfigurationInternalAccess:
    def __init__(
        self,
        *,
        analysis_rule: typing.Optional[typing.Union["AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param analysis_rule: analysis_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#analysis_rule AccessanalyzerAnalyzer#analysis_rule}
        '''
        if isinstance(analysis_rule, dict):
            analysis_rule = AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule(**analysis_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68cb67b68da094e7f41cdf5c9d95ebf5d6d3cece2665cc69d475a292d74c509)
            check_type(argname="argument analysis_rule", value=analysis_rule, expected_type=type_hints["analysis_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if analysis_rule is not None:
            self._values["analysis_rule"] = analysis_rule

    @builtins.property
    def analysis_rule(
        self,
    ) -> typing.Optional["AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule"]:
        '''analysis_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#analysis_rule AccessanalyzerAnalyzer#analysis_rule}
        '''
        result = self._values.get("analysis_rule")
        return typing.cast(typing.Optional["AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessanalyzerAnalyzerConfigurationInternalAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule",
    jsii_struct_bases=[],
    name_mapping={"inclusion": "inclusion"},
)
class AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule:
    def __init__(
        self,
        *,
        inclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param inclusion: inclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#inclusion AccessanalyzerAnalyzer#inclusion}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c67d522a84c35b23f61a1bac5943a4dd7977fd6f42ca6e4c0aec995a86afd2)
            check_type(argname="argument inclusion", value=inclusion, expected_type=type_hints["inclusion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inclusion is not None:
            self._values["inclusion"] = inclusion

    @builtins.property
    def inclusion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion"]]]:
        '''inclusion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#inclusion AccessanalyzerAnalyzer#inclusion}
        '''
        result = self._values.get("inclusion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion",
    jsii_struct_bases=[],
    name_mapping={
        "account_ids": "accountIds",
        "resource_arns": "resourceArns",
        "resource_types": "resourceTypes",
    },
)
class AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion:
    def __init__(
        self,
        *,
        account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param account_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#account_ids AccessanalyzerAnalyzer#account_ids}.
        :param resource_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#resource_arns AccessanalyzerAnalyzer#resource_arns}.
        :param resource_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#resource_types AccessanalyzerAnalyzer#resource_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12bf62c0a53885ea5036a5cbd6da21678b9669c49d5238618766833c426b2ed6)
            check_type(argname="argument account_ids", value=account_ids, expected_type=type_hints["account_ids"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_ids is not None:
            self._values["account_ids"] = account_ids
        if resource_arns is not None:
            self._values["resource_arns"] = resource_arns
        if resource_types is not None:
            self._values["resource_types"] = resource_types

    @builtins.property
    def account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#account_ids AccessanalyzerAnalyzer#account_ids}.'''
        result = self._values.get("account_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#resource_arns AccessanalyzerAnalyzer#resource_arns}.'''
        result = self._values.get("resource_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#resource_types AccessanalyzerAnalyzer#resource_types}.'''
        result = self._values.get("resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4da4aa8b7d00cdbf56ce356767ac270707dea661891ee811467df716d094f76c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c9788f4e696a92a2e6112976b968abd9aeb81cefd5b71708bc557b00e5de48)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef91a012bd2495908eba6701ce92f4760bfd55a34503e611a7d42b2a1f918e25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca9f7d6fd5540643ee18110ea6feb6d94523528a8bfde798e24574d746e2dd7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b3070ef4a6b9a9cb1c83ea4b4ad79c097369b0bec7f850fda054822ea04533b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f86ccd9dc2f528ffe3a9616717117957fbc71a317a5c33e59a613c758d317d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33f9662ea48e55f27fa523c62735ca671131b83f30634a8ad31347173061b2ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountIds")
    def reset_account_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountIds", []))

    @jsii.member(jsii_name="resetResourceArns")
    def reset_resource_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceArns", []))

    @jsii.member(jsii_name="resetResourceTypes")
    def reset_resource_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTypes", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdsInput")
    def account_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accountIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArnsInput")
    def resource_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypesInput")
    def resource_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="accountIds")
    def account_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountIds"))

    @account_ids.setter
    def account_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12b0cd6aeff01aef39d2b905622653519a29341293f5dfe0681afff3f2b5845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceArns")
    def resource_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceArns"))

    @resource_arns.setter
    def resource_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fbf9b4c95df34e748049fd68b5a02d0e27f7d62b4965b0c798e7ec466adfd1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90785c143cb048e3e8d24a27dd37ee6314d3a903ff2976e0a079ec72a897a79a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7c85ccee4e9deaa15f67df347d7f82523237ca3ee77e980bf1cd4328e032d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d5342f4d9b5844b303866aac7e10cbc0306e4d8678d419a01e2fb8d81ca29d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInclusion")
    def put_inclusion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f85fea0b7759178dad51b2d9636f197256045d58cee5bc0a7a63f90bf64d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInclusion", [value]))

    @jsii.member(jsii_name="resetInclusion")
    def reset_inclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInclusion", []))

    @builtins.property
    @jsii.member(jsii_name="inclusion")
    def inclusion(
        self,
    ) -> AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusionList:
        return typing.cast(AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusionList, jsii.get(self, "inclusion"))

    @builtins.property
    @jsii.member(jsii_name="inclusionInput")
    def inclusion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion]]], jsii.get(self, "inclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule]:
        return typing.cast(typing.Optional[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c98c2afe4b5ce2e1f935f262e40a8c1767233db09fce6e377b5b685b6b9252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessanalyzerAnalyzerConfigurationInternalAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationInternalAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fae5eabf1504c2f53891148b242abc189fefd76332fe4ef70ebbf3f1c517a9a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnalysisRule")
    def put_analysis_rule(
        self,
        *,
        inclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param inclusion: inclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#inclusion AccessanalyzerAnalyzer#inclusion}
        '''
        value = AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule(
            inclusion=inclusion
        )

        return typing.cast(None, jsii.invoke(self, "putAnalysisRule", [value]))

    @jsii.member(jsii_name="resetAnalysisRule")
    def reset_analysis_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalysisRule", []))

    @builtins.property
    @jsii.member(jsii_name="analysisRule")
    def analysis_rule(
        self,
    ) -> AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleOutputReference:
        return typing.cast(AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleOutputReference, jsii.get(self, "analysisRule"))

    @builtins.property
    @jsii.member(jsii_name="analysisRuleInput")
    def analysis_rule_input(
        self,
    ) -> typing.Optional[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule]:
        return typing.cast(typing.Optional[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule], jsii.get(self, "analysisRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessanalyzerAnalyzerConfigurationInternalAccess]:
        return typing.cast(typing.Optional[AccessanalyzerAnalyzerConfigurationInternalAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessanalyzerAnalyzerConfigurationInternalAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c2c6274671652697deac6a1492aad0f5e67b93ec5d47bb6ad06c5f434801e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessanalyzerAnalyzerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0b1633d4b48ce112819fa0dc5d917bfbbbf6b1296181e6508382b5725218021)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInternalAccess")
    def put_internal_access(
        self,
        *,
        analysis_rule: typing.Optional[typing.Union[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param analysis_rule: analysis_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#analysis_rule AccessanalyzerAnalyzer#analysis_rule}
        '''
        value = AccessanalyzerAnalyzerConfigurationInternalAccess(
            analysis_rule=analysis_rule
        )

        return typing.cast(None, jsii.invoke(self, "putInternalAccess", [value]))

    @jsii.member(jsii_name="putUnusedAccess")
    def put_unused_access(
        self,
        *,
        analysis_rule: typing.Optional[typing.Union["AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule", typing.Dict[builtins.str, typing.Any]]] = None,
        unused_access_age: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param analysis_rule: analysis_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#analysis_rule AccessanalyzerAnalyzer#analysis_rule}
        :param unused_access_age: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#unused_access_age AccessanalyzerAnalyzer#unused_access_age}.
        '''
        value = AccessanalyzerAnalyzerConfigurationUnusedAccess(
            analysis_rule=analysis_rule, unused_access_age=unused_access_age
        )

        return typing.cast(None, jsii.invoke(self, "putUnusedAccess", [value]))

    @jsii.member(jsii_name="resetInternalAccess")
    def reset_internal_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalAccess", []))

    @jsii.member(jsii_name="resetUnusedAccess")
    def reset_unused_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnusedAccess", []))

    @builtins.property
    @jsii.member(jsii_name="internalAccess")
    def internal_access(
        self,
    ) -> AccessanalyzerAnalyzerConfigurationInternalAccessOutputReference:
        return typing.cast(AccessanalyzerAnalyzerConfigurationInternalAccessOutputReference, jsii.get(self, "internalAccess"))

    @builtins.property
    @jsii.member(jsii_name="unusedAccess")
    def unused_access(
        self,
    ) -> "AccessanalyzerAnalyzerConfigurationUnusedAccessOutputReference":
        return typing.cast("AccessanalyzerAnalyzerConfigurationUnusedAccessOutputReference", jsii.get(self, "unusedAccess"))

    @builtins.property
    @jsii.member(jsii_name="internalAccessInput")
    def internal_access_input(
        self,
    ) -> typing.Optional[AccessanalyzerAnalyzerConfigurationInternalAccess]:
        return typing.cast(typing.Optional[AccessanalyzerAnalyzerConfigurationInternalAccess], jsii.get(self, "internalAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="unusedAccessInput")
    def unused_access_input(
        self,
    ) -> typing.Optional["AccessanalyzerAnalyzerConfigurationUnusedAccess"]:
        return typing.cast(typing.Optional["AccessanalyzerAnalyzerConfigurationUnusedAccess"], jsii.get(self, "unusedAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AccessanalyzerAnalyzerConfiguration]:
        return typing.cast(typing.Optional[AccessanalyzerAnalyzerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessanalyzerAnalyzerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ce9f78df8458a424e135db3cd735ecd6b08abb0e44d687e24c87a90352cc62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationUnusedAccess",
    jsii_struct_bases=[],
    name_mapping={
        "analysis_rule": "analysisRule",
        "unused_access_age": "unusedAccessAge",
    },
)
class AccessanalyzerAnalyzerConfigurationUnusedAccess:
    def __init__(
        self,
        *,
        analysis_rule: typing.Optional[typing.Union["AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule", typing.Dict[builtins.str, typing.Any]]] = None,
        unused_access_age: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param analysis_rule: analysis_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#analysis_rule AccessanalyzerAnalyzer#analysis_rule}
        :param unused_access_age: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#unused_access_age AccessanalyzerAnalyzer#unused_access_age}.
        '''
        if isinstance(analysis_rule, dict):
            analysis_rule = AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule(**analysis_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c7ad702f6824ee3c018d3db7d0654122724f0d9685c76f9d7466226b3f4949)
            check_type(argname="argument analysis_rule", value=analysis_rule, expected_type=type_hints["analysis_rule"])
            check_type(argname="argument unused_access_age", value=unused_access_age, expected_type=type_hints["unused_access_age"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if analysis_rule is not None:
            self._values["analysis_rule"] = analysis_rule
        if unused_access_age is not None:
            self._values["unused_access_age"] = unused_access_age

    @builtins.property
    def analysis_rule(
        self,
    ) -> typing.Optional["AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule"]:
        '''analysis_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#analysis_rule AccessanalyzerAnalyzer#analysis_rule}
        '''
        result = self._values.get("analysis_rule")
        return typing.cast(typing.Optional["AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule"], result)

    @builtins.property
    def unused_access_age(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#unused_access_age AccessanalyzerAnalyzer#unused_access_age}.'''
        result = self._values.get("unused_access_age")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessanalyzerAnalyzerConfigurationUnusedAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule",
    jsii_struct_bases=[],
    name_mapping={"exclusion": "exclusion"},
)
class AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule:
    def __init__(
        self,
        *,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#exclusion AccessanalyzerAnalyzer#exclusion}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46e48bda1d1f79dd5f227261ca466b57a42a66dc9042f7ad9939d129e1d93e7)
            check_type(argname="argument exclusion", value=exclusion, expected_type=type_hints["exclusion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusion is not None:
            self._values["exclusion"] = exclusion

    @builtins.property
    def exclusion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion"]]]:
        '''exclusion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#exclusion AccessanalyzerAnalyzer#exclusion}
        '''
        result = self._values.get("exclusion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion",
    jsii_struct_bases=[],
    name_mapping={"account_ids": "accountIds", "resource_tags": "resourceTags"},
)
class AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion:
    def __init__(
        self,
        *,
        account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Mapping[builtins.str, builtins.str]]]] = None,
    ) -> None:
        '''
        :param account_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#account_ids AccessanalyzerAnalyzer#account_ids}.
        :param resource_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#resource_tags AccessanalyzerAnalyzer#resource_tags}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435f3ee0ebdf2108b0e948b8f43381742e405d928fcefddb11b5acadabf9a45b)
            check_type(argname="argument account_ids", value=account_ids, expected_type=type_hints["account_ids"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_ids is not None:
            self._values["account_ids"] = account_ids
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags

    @builtins.property
    def account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#account_ids AccessanalyzerAnalyzer#account_ids}.'''
        result = self._values.get("account_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.Mapping[builtins.str, builtins.str]]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#resource_tags AccessanalyzerAnalyzer#resource_tags}.'''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.Mapping[builtins.str, builtins.str]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b372488a471555c5eae77c71f6615636eaee8520471a063c2ab954d022a8a688)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a1b4eeb955b70cb4e5ff13803fb1b9a7c885f2d542acd838606cc989ec3f6ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752a8e400e580af42760ee77b24e5d6e435cb6f04f6bdaa3998ccd7c83d28c84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b9341ff901515c68a8c82b890748e6ebd6729eb1e8cbfc8bcc886244dc028e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1efbacd2c9f529c2b36227415e6a5e7708fe495543531433489f8c51555e77d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57f92ed09396751cba7fa258a5edb58705987a82d7e68bc99d516a2b3db0ad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56c566c92388e44bac51eff1be5e84ae98a340806ceaa15a02f3a578b4d9991d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountIds")
    def reset_account_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountIds", []))

    @jsii.member(jsii_name="resetResourceTags")
    def reset_resource_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTags", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdsInput")
    def account_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accountIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagsInput")
    def resource_tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.Mapping[builtins.str, builtins.str]]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.Mapping[builtins.str, builtins.str]]]], jsii.get(self, "resourceTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountIds")
    def account_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "accountIds"))

    @account_ids.setter
    def account_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf0feeca738068b65fc9cd9b9ec36ea26874137e1bd735f57f32a60fef941e20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.Mapping[builtins.str, builtins.str]]]:
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "resourceTags"))

    @resource_tags.setter
    def resource_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663fb4e83cfbd33aa3d207ba112666b4c1e767456e9e15afd130be1e2d240604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a88f9b7f055d5581558cadbde8d4665f8aa1b8dd70712210d705e8eec0f351b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e00f849932a55d93fa5c9a26a33bfffd56058d348ba6f7f2d299977915b835c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusion")
    def put_exclusion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2155ac453c16898d1529aba7ad69143a722b00fb18ac539d7b1efbc79287002d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusion", [value]))

    @jsii.member(jsii_name="resetExclusion")
    def reset_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusion", []))

    @builtins.property
    @jsii.member(jsii_name="exclusion")
    def exclusion(
        self,
    ) -> AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusionList:
        return typing.cast(AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusionList, jsii.get(self, "exclusion"))

    @builtins.property
    @jsii.member(jsii_name="exclusionInput")
    def exclusion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion]]], jsii.get(self, "exclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule]:
        return typing.cast(typing.Optional[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d36cf2dc37a7446a3f8f1710558b19e50d0c84ec924cf25daec6c7d9fe5e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessanalyzerAnalyzerConfigurationUnusedAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.accessanalyzerAnalyzer.AccessanalyzerAnalyzerConfigurationUnusedAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66a4a37d75f02f44c4aaeb263c24b0bfe649e09c7773e89773a4aac338224d03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnalysisRule")
    def put_analysis_rule(
        self,
        *,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/accessanalyzer_analyzer#exclusion AccessanalyzerAnalyzer#exclusion}
        '''
        value = AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule(
            exclusion=exclusion
        )

        return typing.cast(None, jsii.invoke(self, "putAnalysisRule", [value]))

    @jsii.member(jsii_name="resetAnalysisRule")
    def reset_analysis_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalysisRule", []))

    @jsii.member(jsii_name="resetUnusedAccessAge")
    def reset_unused_access_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnusedAccessAge", []))

    @builtins.property
    @jsii.member(jsii_name="analysisRule")
    def analysis_rule(
        self,
    ) -> AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleOutputReference:
        return typing.cast(AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleOutputReference, jsii.get(self, "analysisRule"))

    @builtins.property
    @jsii.member(jsii_name="analysisRuleInput")
    def analysis_rule_input(
        self,
    ) -> typing.Optional[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule]:
        return typing.cast(typing.Optional[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule], jsii.get(self, "analysisRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="unusedAccessAgeInput")
    def unused_access_age_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unusedAccessAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="unusedAccessAge")
    def unused_access_age(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unusedAccessAge"))

    @unused_access_age.setter
    def unused_access_age(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9184918a57ddddf4b35f815b7a2df57fb75c4eda666885b39ec3ad31b97f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unusedAccessAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AccessanalyzerAnalyzerConfigurationUnusedAccess]:
        return typing.cast(typing.Optional[AccessanalyzerAnalyzerConfigurationUnusedAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AccessanalyzerAnalyzerConfigurationUnusedAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b6e0337d461d36f1791d196652c0279d47d32ec64bf5ecbdaa8b432f821a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessanalyzerAnalyzer",
    "AccessanalyzerAnalyzerConfig",
    "AccessanalyzerAnalyzerConfiguration",
    "AccessanalyzerAnalyzerConfigurationInternalAccess",
    "AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule",
    "AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion",
    "AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusionList",
    "AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusionOutputReference",
    "AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleOutputReference",
    "AccessanalyzerAnalyzerConfigurationInternalAccessOutputReference",
    "AccessanalyzerAnalyzerConfigurationOutputReference",
    "AccessanalyzerAnalyzerConfigurationUnusedAccess",
    "AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule",
    "AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion",
    "AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusionList",
    "AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusionOutputReference",
    "AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleOutputReference",
    "AccessanalyzerAnalyzerConfigurationUnusedAccessOutputReference",
]

publication.publish()

def _typecheckingstub__6367f3d990e3d4c27e0182a7de91e44b74a4d456fd1f83446e0f157fce93af04(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    analyzer_name: builtins.str,
    configuration: typing.Optional[typing.Union[AccessanalyzerAnalyzerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__23f310473f23d09087c667c7325e075fe84cdd39bfff8f8f2e5ef14bef0ffe25(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2d54cdbddf07ebb862693ae46888178f7405a808a16c8eb561d99f480d7d6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb580d614c09ec5df505b717e62279dfb53c2c84a335676add7bab1f231546c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5b29128b95f0437864fdcba031d685f0f460753fa5485bab8aa427d1abd67f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1489106da4731ce078e8cb1260e11b8caed7b0a2f42becf60bcc666cefb6d3a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a40d49759e687bd503263d803626d09e922ff6b624d718b4745370221a14da(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df092ef4230e9f50676b99d34519028b026f148e0988080a99e206fee7d45e2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d92b63429984ba04f72b40d1b14bc95abd1d4449d5f68d2460fe85c57ea7db0a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    analyzer_name: builtins.str,
    configuration: typing.Optional[typing.Union[AccessanalyzerAnalyzerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f033844b2b3d740c06e4ffa098dc10142e959e3632af5ed852d7dc9d6777bddb(
    *,
    internal_access: typing.Optional[typing.Union[AccessanalyzerAnalyzerConfigurationInternalAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    unused_access: typing.Optional[typing.Union[AccessanalyzerAnalyzerConfigurationUnusedAccess, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68cb67b68da094e7f41cdf5c9d95ebf5d6d3cece2665cc69d475a292d74c509(
    *,
    analysis_rule: typing.Optional[typing.Union[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c67d522a84c35b23f61a1bac5943a4dd7977fd6f42ca6e4c0aec995a86afd2(
    *,
    inclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12bf62c0a53885ea5036a5cbd6da21678b9669c49d5238618766833c426b2ed6(
    *,
    account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da4aa8b7d00cdbf56ce356767ac270707dea661891ee811467df716d094f76c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c9788f4e696a92a2e6112976b968abd9aeb81cefd5b71708bc557b00e5de48(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef91a012bd2495908eba6701ce92f4760bfd55a34503e611a7d42b2a1f918e25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9f7d6fd5540643ee18110ea6feb6d94523528a8bfde798e24574d746e2dd7a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3070ef4a6b9a9cb1c83ea4b4ad79c097369b0bec7f850fda054822ea04533b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f86ccd9dc2f528ffe3a9616717117957fbc71a317a5c33e59a613c758d317d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f9662ea48e55f27fa523c62735ca671131b83f30634a8ad31347173061b2ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12b0cd6aeff01aef39d2b905622653519a29341293f5dfe0681afff3f2b5845(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbf9b4c95df34e748049fd68b5a02d0e27f7d62b4965b0c798e7ec466adfd1a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90785c143cb048e3e8d24a27dd37ee6314d3a903ff2976e0a079ec72a897a79a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7c85ccee4e9deaa15f67df347d7f82523237ca3ee77e980bf1cd4328e032d6(
    value: typing.Optional[typing.Union[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5342f4d9b5844b303866aac7e10cbc0306e4d8678d419a01e2fb8d81ca29d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f85fea0b7759178dad51b2d9636f197256045d58cee5bc0a7a63f90bf64d23(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRuleInclusion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c98c2afe4b5ce2e1f935f262e40a8c1767233db09fce6e377b5b685b6b9252(
    value: typing.Optional[AccessanalyzerAnalyzerConfigurationInternalAccessAnalysisRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae5eabf1504c2f53891148b242abc189fefd76332fe4ef70ebbf3f1c517a9a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c2c6274671652697deac6a1492aad0f5e67b93ec5d47bb6ad06c5f434801e1(
    value: typing.Optional[AccessanalyzerAnalyzerConfigurationInternalAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b1633d4b48ce112819fa0dc5d917bfbbbf6b1296181e6508382b5725218021(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ce9f78df8458a424e135db3cd735ecd6b08abb0e44d687e24c87a90352cc62(
    value: typing.Optional[AccessanalyzerAnalyzerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c7ad702f6824ee3c018d3db7d0654122724f0d9685c76f9d7466226b3f4949(
    *,
    analysis_rule: typing.Optional[typing.Union[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule, typing.Dict[builtins.str, typing.Any]]] = None,
    unused_access_age: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46e48bda1d1f79dd5f227261ca466b57a42a66dc9042f7ad9939d129e1d93e7(
    *,
    exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435f3ee0ebdf2108b0e948b8f43381742e405d928fcefddb11b5acadabf9a45b(
    *,
    account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Mapping[builtins.str, builtins.str]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b372488a471555c5eae77c71f6615636eaee8520471a063c2ab954d022a8a688(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1b4eeb955b70cb4e5ff13803fb1b9a7c885f2d542acd838606cc989ec3f6ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752a8e400e580af42760ee77b24e5d6e435cb6f04f6bdaa3998ccd7c83d28c84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9341ff901515c68a8c82b890748e6ebd6729eb1e8cbfc8bcc886244dc028e5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efbacd2c9f529c2b36227415e6a5e7708fe495543531433489f8c51555e77d6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57f92ed09396751cba7fa258a5edb58705987a82d7e68bc99d516a2b3db0ad9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c566c92388e44bac51eff1be5e84ae98a340806ceaa15a02f3a578b4d9991d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0feeca738068b65fc9cd9b9ec36ea26874137e1bd735f57f32a60fef941e20(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663fb4e83cfbd33aa3d207ba112666b4c1e767456e9e15afd130be1e2d240604(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a88f9b7f055d5581558cadbde8d4665f8aa1b8dd70712210d705e8eec0f351b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e00f849932a55d93fa5c9a26a33bfffd56058d348ba6f7f2d299977915b835c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2155ac453c16898d1529aba7ad69143a722b00fb18ac539d7b1efbc79287002d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRuleExclusion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d36cf2dc37a7446a3f8f1710558b19e50d0c84ec924cf25daec6c7d9fe5e84(
    value: typing.Optional[AccessanalyzerAnalyzerConfigurationUnusedAccessAnalysisRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a4a37d75f02f44c4aaeb263c24b0bfe649e09c7773e89773a4aac338224d03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9184918a57ddddf4b35f815b7a2df57fb75c4eda666885b39ec3ad31b97f46(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b6e0337d461d36f1791d196652c0279d47d32ec64bf5ecbdaa8b432f821a42(
    value: typing.Optional[AccessanalyzerAnalyzerConfigurationUnusedAccess],
) -> None:
    """Type checking stubs"""
    pass
