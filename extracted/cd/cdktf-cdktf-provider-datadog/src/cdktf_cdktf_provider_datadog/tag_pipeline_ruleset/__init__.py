r'''
# `datadog_tag_pipeline_ruleset`

Refer to the Terraform Registry for docs: [`datadog_tag_pipeline_ruleset`](https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset).
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


class TagPipelineRuleset(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRuleset",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset datadog_tag_pipeline_ruleset}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TagPipelineRulesetRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset datadog_tag_pipeline_ruleset} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the ruleset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#name TagPipelineRuleset#name}
        :param enabled: Whether the ruleset is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#enabled TagPipelineRuleset#enabled}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#rules TagPipelineRuleset#rules}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92f9ba5339b69a3e4905493e75064858bae350eaf456419c20b58025b60da23)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = TagPipelineRulesetConfig(
            name=name,
            enabled=enabled,
            rules=rules,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a TagPipelineRuleset resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TagPipelineRuleset to import.
        :param import_from_id: The id of the existing TagPipelineRuleset that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TagPipelineRuleset to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6c73171c16a25328008ac696004a00b0df806a9773dc7aab74b74780a43928)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TagPipelineRulesetRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c74a71eedd7743c45d85276da9b2c7bd93c2cbee59cb229122cff5ef98784c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="position")
    def position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "position"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "TagPipelineRulesetRulesList":
        return typing.cast("TagPipelineRulesetRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TagPipelineRulesetRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TagPipelineRulesetRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502df55f0c92f531841ea2e64e39427651a9415617117b3fb3f19f98c5e94e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e87ca17b7155a784cbb9d9826f15877ffac3afc7291e65c645c554de9b4812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetConfig",
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
        "enabled": "enabled",
        "rules": "rules",
    },
)
class TagPipelineRulesetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TagPipelineRulesetRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the ruleset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#name TagPipelineRuleset#name}
        :param enabled: Whether the ruleset is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#enabled TagPipelineRuleset#enabled}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#rules TagPipelineRuleset#rules}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c04832b1785b97f2fd63968065ddd9247d0f8ee6ebda4d77f42d00b2c1e9fb8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
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
        if enabled is not None:
            self._values["enabled"] = enabled
        if rules is not None:
            self._values["rules"] = rules

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
        '''The name of the ruleset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#name TagPipelineRuleset#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the ruleset is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#enabled TagPipelineRuleset#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TagPipelineRulesetRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#rules TagPipelineRuleset#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TagPipelineRulesetRules"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TagPipelineRulesetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRules",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "name": "name",
        "mapping": "mapping",
        "query": "query",
        "reference_table": "referenceTable",
    },
)
class TagPipelineRulesetRules:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        mapping: typing.Optional[typing.Union["TagPipelineRulesetRulesMapping", typing.Dict[builtins.str, typing.Any]]] = None,
        query: typing.Optional[typing.Union["TagPipelineRulesetRulesQuery", typing.Dict[builtins.str, typing.Any]]] = None,
        reference_table: typing.Optional[typing.Union["TagPipelineRulesetRulesReferenceTable", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled: Whether the rule is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#enabled TagPipelineRuleset#enabled}
        :param name: The name of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#name TagPipelineRuleset#name}
        :param mapping: mapping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#mapping TagPipelineRuleset#mapping}
        :param query: query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#query TagPipelineRuleset#query}
        :param reference_table: reference_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#reference_table TagPipelineRuleset#reference_table}
        '''
        if isinstance(mapping, dict):
            mapping = TagPipelineRulesetRulesMapping(**mapping)
        if isinstance(query, dict):
            query = TagPipelineRulesetRulesQuery(**query)
        if isinstance(reference_table, dict):
            reference_table = TagPipelineRulesetRulesReferenceTable(**reference_table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a185b032a072e255d5f4506c62a0b02b03650b77b01f62d87fe79b06429775)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument mapping", value=mapping, expected_type=type_hints["mapping"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument reference_table", value=reference_table, expected_type=type_hints["reference_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "name": name,
        }
        if mapping is not None:
            self._values["mapping"] = mapping
        if query is not None:
            self._values["query"] = query
        if reference_table is not None:
            self._values["reference_table"] = reference_table

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the rule is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#enabled TagPipelineRuleset#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#name TagPipelineRuleset#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mapping(self) -> typing.Optional["TagPipelineRulesetRulesMapping"]:
        '''mapping block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#mapping TagPipelineRuleset#mapping}
        '''
        result = self._values.get("mapping")
        return typing.cast(typing.Optional["TagPipelineRulesetRulesMapping"], result)

    @builtins.property
    def query(self) -> typing.Optional["TagPipelineRulesetRulesQuery"]:
        '''query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#query TagPipelineRuleset#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional["TagPipelineRulesetRulesQuery"], result)

    @builtins.property
    def reference_table(
        self,
    ) -> typing.Optional["TagPipelineRulesetRulesReferenceTable"]:
        '''reference_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#reference_table TagPipelineRuleset#reference_table}
        '''
        result = self._values.get("reference_table")
        return typing.cast(typing.Optional["TagPipelineRulesetRulesReferenceTable"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TagPipelineRulesetRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TagPipelineRulesetRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a1e2c38b04eed4f5a9b93a0227ab8945a1f175b07e65007beb58e683369fb9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TagPipelineRulesetRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38fef41f75426dec7c9e3de5bfcf555883b2d5734f0688fe79e9856b4517a25c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TagPipelineRulesetRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14dbe24978bdd79e6521c706d3981f074756ad1a121873e5f89fc8be367c0dc7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75e1b5b6a9ba3c1f67877e81fb54969b010fd32a52a592ddf5b051b21629fbcd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5b76c8fbc797d5adedfd2def77d081969ccf152fca5cc2368c26d5e317e35dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TagPipelineRulesetRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TagPipelineRulesetRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TagPipelineRulesetRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f632c97e3c13d4db26a3e703417a37d984ed072eb13f86d5c16eed34f52d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesMapping",
    jsii_struct_bases=[],
    name_mapping={
        "destination_key": "destinationKey",
        "if_not_exists": "ifNotExists",
        "source_keys": "sourceKeys",
    },
)
class TagPipelineRulesetRulesMapping:
    def __init__(
        self,
        *,
        destination_key: typing.Optional[builtins.str] = None,
        if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param destination_key: The destination key for the mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#destination_key TagPipelineRuleset#destination_key}
        :param if_not_exists: Whether to apply the mapping only if the destination key doesn't exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#if_not_exists TagPipelineRuleset#if_not_exists}
        :param source_keys: The source keys for the mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#source_keys TagPipelineRuleset#source_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6a866a2cca0f239bde876a74efd66af707cb5bfb3f7487270f390b86c8e2fc)
            check_type(argname="argument destination_key", value=destination_key, expected_type=type_hints["destination_key"])
            check_type(argname="argument if_not_exists", value=if_not_exists, expected_type=type_hints["if_not_exists"])
            check_type(argname="argument source_keys", value=source_keys, expected_type=type_hints["source_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_key is not None:
            self._values["destination_key"] = destination_key
        if if_not_exists is not None:
            self._values["if_not_exists"] = if_not_exists
        if source_keys is not None:
            self._values["source_keys"] = source_keys

    @builtins.property
    def destination_key(self) -> typing.Optional[builtins.str]:
        '''The destination key for the mapping.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#destination_key TagPipelineRuleset#destination_key}
        '''
        result = self._values.get("destination_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def if_not_exists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to apply the mapping only if the destination key doesn't exist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#if_not_exists TagPipelineRuleset#if_not_exists}
        '''
        result = self._values.get("if_not_exists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The source keys for the mapping.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#source_keys TagPipelineRuleset#source_keys}
        '''
        result = self._values.get("source_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TagPipelineRulesetRulesMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TagPipelineRulesetRulesMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aee16de0c47109eb84be7ae116e3c46461653143511ff48695d12c4f29cf165a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDestinationKey")
    def reset_destination_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationKey", []))

    @jsii.member(jsii_name="resetIfNotExists")
    def reset_if_not_exists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIfNotExists", []))

    @jsii.member(jsii_name="resetSourceKeys")
    def reset_source_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceKeys", []))

    @builtins.property
    @jsii.member(jsii_name="destinationKeyInput")
    def destination_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="ifNotExistsInput")
    def if_not_exists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ifNotExistsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceKeysInput")
    def source_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationKey")
    def destination_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationKey"))

    @destination_key.setter
    def destination_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad396d17b67e996f524dad60dcbaab5f17a0657468181f2caa737c54ffd1971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ifNotExists")
    def if_not_exists(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ifNotExists"))

    @if_not_exists.setter
    def if_not_exists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e05bc6423eec2a5ca966b40fbde04982ad6c2cdef4412b4340f29ac4bc27e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ifNotExists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceKeys")
    def source_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceKeys"))

    @source_keys.setter
    def source_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0ed7f651f1cbb4d4dab342534b7fb479f8389514e4cd32ccf717a1fc4e40029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesMapping]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesMapping]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesMapping]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079851e7fd37ae539c76d8e13b33bcc3565ca59262433d6ae54dbafd7c4f668f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TagPipelineRulesetRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ef8091d86bc6050eb9a9879acc94fa9d0eef6f159491889664512f1efa7fdd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMapping")
    def put_mapping(
        self,
        *,
        destination_key: typing.Optional[builtins.str] = None,
        if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param destination_key: The destination key for the mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#destination_key TagPipelineRuleset#destination_key}
        :param if_not_exists: Whether to apply the mapping only if the destination key doesn't exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#if_not_exists TagPipelineRuleset#if_not_exists}
        :param source_keys: The source keys for the mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#source_keys TagPipelineRuleset#source_keys}
        '''
        value = TagPipelineRulesetRulesMapping(
            destination_key=destination_key,
            if_not_exists=if_not_exists,
            source_keys=source_keys,
        )

        return typing.cast(None, jsii.invoke(self, "putMapping", [value]))

    @jsii.member(jsii_name="putQuery")
    def put_query(
        self,
        *,
        addition: typing.Optional[typing.Union["TagPipelineRulesetRulesQueryAddition", typing.Dict[builtins.str, typing.Any]]] = None,
        case_insensitivity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param addition: addition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#addition TagPipelineRuleset#addition}
        :param case_insensitivity: Whether the query matching is case insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#case_insensitivity TagPipelineRuleset#case_insensitivity}
        :param if_not_exists: Whether to apply the query only if the key doesn't exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#if_not_exists TagPipelineRuleset#if_not_exists}
        :param query: The query string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#query TagPipelineRuleset#query}
        '''
        value = TagPipelineRulesetRulesQuery(
            addition=addition,
            case_insensitivity=case_insensitivity,
            if_not_exists=if_not_exists,
            query=query,
        )

        return typing.cast(None, jsii.invoke(self, "putQuery", [value]))

    @jsii.member(jsii_name="putReferenceTable")
    def put_reference_table(
        self,
        *,
        case_insensitivity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        field_pairs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TagPipelineRulesetRulesReferenceTableFieldPairs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param case_insensitivity: Whether the reference table lookup is case insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#case_insensitivity TagPipelineRuleset#case_insensitivity}
        :param field_pairs: field_pairs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#field_pairs TagPipelineRuleset#field_pairs}
        :param if_not_exists: Whether to apply the reference table only if the key doesn't exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#if_not_exists TagPipelineRuleset#if_not_exists}
        :param source_keys: The source keys for the reference table lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#source_keys TagPipelineRuleset#source_keys}
        :param table_name: The name of the reference table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#table_name TagPipelineRuleset#table_name}
        '''
        value = TagPipelineRulesetRulesReferenceTable(
            case_insensitivity=case_insensitivity,
            field_pairs=field_pairs,
            if_not_exists=if_not_exists,
            source_keys=source_keys,
            table_name=table_name,
        )

        return typing.cast(None, jsii.invoke(self, "putReferenceTable", [value]))

    @jsii.member(jsii_name="resetMapping")
    def reset_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapping", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @jsii.member(jsii_name="resetReferenceTable")
    def reset_reference_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferenceTable", []))

    @builtins.property
    @jsii.member(jsii_name="mapping")
    def mapping(self) -> TagPipelineRulesetRulesMappingOutputReference:
        return typing.cast(TagPipelineRulesetRulesMappingOutputReference, jsii.get(self, "mapping"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> "TagPipelineRulesetRulesQueryOutputReference":
        return typing.cast("TagPipelineRulesetRulesQueryOutputReference", jsii.get(self, "query"))

    @builtins.property
    @jsii.member(jsii_name="referenceTable")
    def reference_table(self) -> "TagPipelineRulesetRulesReferenceTableOutputReference":
        return typing.cast("TagPipelineRulesetRulesReferenceTableOutputReference", jsii.get(self, "referenceTable"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="mappingInput")
    def mapping_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesMapping]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesMapping]], jsii.get(self, "mappingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TagPipelineRulesetRulesQuery"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TagPipelineRulesetRulesQuery"]], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceTableInput")
    def reference_table_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TagPipelineRulesetRulesReferenceTable"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TagPipelineRulesetRulesReferenceTable"]], jsii.get(self, "referenceTableInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9788061eb18616d4a2e712aa665b0c5ad1877879017806428984a226b9d45e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180428b65d61529354d0ae38053568dac6aa2d1f264b37b60fe5d8d573dd722c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9750722f6c0b8605d105b555fc8f1ee6d7d1117fbdd55f1783516671017eac14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesQuery",
    jsii_struct_bases=[],
    name_mapping={
        "addition": "addition",
        "case_insensitivity": "caseInsensitivity",
        "if_not_exists": "ifNotExists",
        "query": "query",
    },
)
class TagPipelineRulesetRulesQuery:
    def __init__(
        self,
        *,
        addition: typing.Optional[typing.Union["TagPipelineRulesetRulesQueryAddition", typing.Dict[builtins.str, typing.Any]]] = None,
        case_insensitivity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param addition: addition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#addition TagPipelineRuleset#addition}
        :param case_insensitivity: Whether the query matching is case insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#case_insensitivity TagPipelineRuleset#case_insensitivity}
        :param if_not_exists: Whether to apply the query only if the key doesn't exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#if_not_exists TagPipelineRuleset#if_not_exists}
        :param query: The query string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#query TagPipelineRuleset#query}
        '''
        if isinstance(addition, dict):
            addition = TagPipelineRulesetRulesQueryAddition(**addition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f571867be6084a4faa451ee7fb9d0bc3ac21e391ddac4ceb6443dcf17852ff0)
            check_type(argname="argument addition", value=addition, expected_type=type_hints["addition"])
            check_type(argname="argument case_insensitivity", value=case_insensitivity, expected_type=type_hints["case_insensitivity"])
            check_type(argname="argument if_not_exists", value=if_not_exists, expected_type=type_hints["if_not_exists"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if addition is not None:
            self._values["addition"] = addition
        if case_insensitivity is not None:
            self._values["case_insensitivity"] = case_insensitivity
        if if_not_exists is not None:
            self._values["if_not_exists"] = if_not_exists
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def addition(self) -> typing.Optional["TagPipelineRulesetRulesQueryAddition"]:
        '''addition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#addition TagPipelineRuleset#addition}
        '''
        result = self._values.get("addition")
        return typing.cast(typing.Optional["TagPipelineRulesetRulesQueryAddition"], result)

    @builtins.property
    def case_insensitivity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the query matching is case insensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#case_insensitivity TagPipelineRuleset#case_insensitivity}
        '''
        result = self._values.get("case_insensitivity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def if_not_exists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to apply the query only if the key doesn't exist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#if_not_exists TagPipelineRuleset#if_not_exists}
        '''
        result = self._values.get("if_not_exists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''The query string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#query TagPipelineRuleset#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TagPipelineRulesetRulesQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesQueryAddition",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class TagPipelineRulesetRulesQueryAddition:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: The key to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#key TagPipelineRuleset#key}
        :param value: The value to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#value TagPipelineRuleset#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02775fed86635da844e67da8855c6bdda3ac5e7f41e054b8746d2bc71e1b094a)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The key to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#key TagPipelineRuleset#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value to add.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#value TagPipelineRuleset#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TagPipelineRulesetRulesQueryAddition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TagPipelineRulesetRulesQueryAdditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesQueryAdditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1160d02a933873f42c62d69f1480921a8f7131525c84473f04be56aa1cfd9b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9620ed5cc40eb38a48d09cb3b66a4529813bd53911e445694d550b2ffe0a7bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09bffe4cb6d6e23fd4624bae25a728ef6ff9352730e1109d85d0e21716d96cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesQueryAddition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesQueryAddition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesQueryAddition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db65ec48e7e4a420c5d6222dbc288e169fc30d527e8d6b6a1c886c2973f3663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TagPipelineRulesetRulesQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d496e1b7b9b87f0acba344a3e96892d0237844fa2233124abd367f21524a2261)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAddition")
    def put_addition(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: The key to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#key TagPipelineRuleset#key}
        :param value: The value to add. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#value TagPipelineRuleset#value}
        '''
        value_ = TagPipelineRulesetRulesQueryAddition(key=key, value=value)

        return typing.cast(None, jsii.invoke(self, "putAddition", [value_]))

    @jsii.member(jsii_name="resetAddition")
    def reset_addition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddition", []))

    @jsii.member(jsii_name="resetCaseInsensitivity")
    def reset_case_insensitivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaseInsensitivity", []))

    @jsii.member(jsii_name="resetIfNotExists")
    def reset_if_not_exists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIfNotExists", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @builtins.property
    @jsii.member(jsii_name="addition")
    def addition(self) -> TagPipelineRulesetRulesQueryAdditionOutputReference:
        return typing.cast(TagPipelineRulesetRulesQueryAdditionOutputReference, jsii.get(self, "addition"))

    @builtins.property
    @jsii.member(jsii_name="additionInput")
    def addition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesQueryAddition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesQueryAddition]], jsii.get(self, "additionInput"))

    @builtins.property
    @jsii.member(jsii_name="caseInsensitivityInput")
    def case_insensitivity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "caseInsensitivityInput"))

    @builtins.property
    @jsii.member(jsii_name="ifNotExistsInput")
    def if_not_exists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ifNotExistsInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="caseInsensitivity")
    def case_insensitivity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "caseInsensitivity"))

    @case_insensitivity.setter
    def case_insensitivity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5cde3bfa8de3dd71dae8b370e6d547b9127742a77cc8fc58eb8e4864ec5f74f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caseInsensitivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ifNotExists")
    def if_not_exists(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ifNotExists"))

    @if_not_exists.setter
    def if_not_exists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6f8bac2cd2b8c59ff6b02b0f9c0c7db2d15f9d06f840698954d213655fa8ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ifNotExists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb28946ee9a1ab4e17bb68fb0040db6769be393f77bcd1c7bdb759d02233a8a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesQuery]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesQuery]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesQuery]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0fe3ed5cd7e6f1d45b368e7fe1a26a9672f5d1fd8b86937973961226e1cfe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesReferenceTable",
    jsii_struct_bases=[],
    name_mapping={
        "case_insensitivity": "caseInsensitivity",
        "field_pairs": "fieldPairs",
        "if_not_exists": "ifNotExists",
        "source_keys": "sourceKeys",
        "table_name": "tableName",
    },
)
class TagPipelineRulesetRulesReferenceTable:
    def __init__(
        self,
        *,
        case_insensitivity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        field_pairs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TagPipelineRulesetRulesReferenceTableFieldPairs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param case_insensitivity: Whether the reference table lookup is case insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#case_insensitivity TagPipelineRuleset#case_insensitivity}
        :param field_pairs: field_pairs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#field_pairs TagPipelineRuleset#field_pairs}
        :param if_not_exists: Whether to apply the reference table only if the key doesn't exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#if_not_exists TagPipelineRuleset#if_not_exists}
        :param source_keys: The source keys for the reference table lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#source_keys TagPipelineRuleset#source_keys}
        :param table_name: The name of the reference table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#table_name TagPipelineRuleset#table_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd6ed2aeb3e27338c9b16554bda258d12e0ea4080b66c0b579d4233c2ce8bfa)
            check_type(argname="argument case_insensitivity", value=case_insensitivity, expected_type=type_hints["case_insensitivity"])
            check_type(argname="argument field_pairs", value=field_pairs, expected_type=type_hints["field_pairs"])
            check_type(argname="argument if_not_exists", value=if_not_exists, expected_type=type_hints["if_not_exists"])
            check_type(argname="argument source_keys", value=source_keys, expected_type=type_hints["source_keys"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if case_insensitivity is not None:
            self._values["case_insensitivity"] = case_insensitivity
        if field_pairs is not None:
            self._values["field_pairs"] = field_pairs
        if if_not_exists is not None:
            self._values["if_not_exists"] = if_not_exists
        if source_keys is not None:
            self._values["source_keys"] = source_keys
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def case_insensitivity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the reference table lookup is case insensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#case_insensitivity TagPipelineRuleset#case_insensitivity}
        '''
        result = self._values.get("case_insensitivity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def field_pairs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TagPipelineRulesetRulesReferenceTableFieldPairs"]]]:
        '''field_pairs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#field_pairs TagPipelineRuleset#field_pairs}
        '''
        result = self._values.get("field_pairs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TagPipelineRulesetRulesReferenceTableFieldPairs"]]], result)

    @builtins.property
    def if_not_exists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to apply the reference table only if the key doesn't exist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#if_not_exists TagPipelineRuleset#if_not_exists}
        '''
        result = self._values.get("if_not_exists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The source keys for the reference table lookup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#source_keys TagPipelineRuleset#source_keys}
        '''
        result = self._values.get("source_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''The name of the reference table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#table_name TagPipelineRuleset#table_name}
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TagPipelineRulesetRulesReferenceTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesReferenceTableFieldPairs",
    jsii_struct_bases=[],
    name_mapping={"input_column": "inputColumn", "output_key": "outputKey"},
)
class TagPipelineRulesetRulesReferenceTableFieldPairs:
    def __init__(
        self,
        *,
        input_column: typing.Optional[builtins.str] = None,
        output_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input_column: The input column name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#input_column TagPipelineRuleset#input_column}
        :param output_key: The output key name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#output_key TagPipelineRuleset#output_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d5d370e46bb56faa883d3a3972bbacc811737a5633979d75851ad571feaec5)
            check_type(argname="argument input_column", value=input_column, expected_type=type_hints["input_column"])
            check_type(argname="argument output_key", value=output_key, expected_type=type_hints["output_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_column is not None:
            self._values["input_column"] = input_column
        if output_key is not None:
            self._values["output_key"] = output_key

    @builtins.property
    def input_column(self) -> typing.Optional[builtins.str]:
        '''The input column name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#input_column TagPipelineRuleset#input_column}
        '''
        result = self._values.get("input_column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_key(self) -> typing.Optional[builtins.str]:
        '''The output key name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.82.0/docs/resources/tag_pipeline_ruleset#output_key TagPipelineRuleset#output_key}
        '''
        result = self._values.get("output_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TagPipelineRulesetRulesReferenceTableFieldPairs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TagPipelineRulesetRulesReferenceTableFieldPairsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesReferenceTableFieldPairsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03b0a3eec2001050c42c2766c42c1769233b78e144505d7903fde32c9cad7bef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TagPipelineRulesetRulesReferenceTableFieldPairsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e260e1096b4568db9588c76cce9350ab4064821700227d38fc940a9cdcf193)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TagPipelineRulesetRulesReferenceTableFieldPairsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f3b970e5288a2c12b8c38e4b73b3539297d02dd717bf3909546f64eba5dfaf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2701c5b3e55e8e176ebbce794390c553f5f76f0eb5b8eb6a48ab52dadfbb775c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3a1f0d1f7f9b7e753712295ef3d34d919cf9f50ed4eccd68bcec4432726353a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TagPipelineRulesetRulesReferenceTableFieldPairs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TagPipelineRulesetRulesReferenceTableFieldPairs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TagPipelineRulesetRulesReferenceTableFieldPairs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094355a9daad48c732d2c07a7f29b7d120a360c63e8c4eff1a226b2c6b031cfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TagPipelineRulesetRulesReferenceTableFieldPairsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesReferenceTableFieldPairsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a70d0d2478834f8e75175209af1dad712cfabca321005a38284d0ad4f5f1939)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInputColumn")
    def reset_input_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputColumn", []))

    @jsii.member(jsii_name="resetOutputKey")
    def reset_output_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputKey", []))

    @builtins.property
    @jsii.member(jsii_name="inputColumnInput")
    def input_column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputColumnInput"))

    @builtins.property
    @jsii.member(jsii_name="outputKeyInput")
    def output_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="inputColumn")
    def input_column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputColumn"))

    @input_column.setter
    def input_column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2bfc3b08f43d1414e1c9a2e32b59472e57cd9891803fa8f04991b4a8be061cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputColumn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputKey")
    def output_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputKey"))

    @output_key.setter
    def output_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20aa0c46a05a95bed0b234b81d2b1b1736cf2a20d1268aa3dd1d426d3cb82bf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesReferenceTableFieldPairs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesReferenceTableFieldPairs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesReferenceTableFieldPairs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca80c13637efc7c826a68e391de67cf362e95f2396e36113866f6d9e81db67ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TagPipelineRulesetRulesReferenceTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.tagPipelineRuleset.TagPipelineRulesetRulesReferenceTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f206056274526c1f69be6d02ef4316533d53617dac7b6dd5e4e8e2e2f9bce25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFieldPairs")
    def put_field_pairs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TagPipelineRulesetRulesReferenceTableFieldPairs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6e35fcdd6de2eaba8a242686ecb73be3f980740e9c3c94988751d8da5f97b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFieldPairs", [value]))

    @jsii.member(jsii_name="resetCaseInsensitivity")
    def reset_case_insensitivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaseInsensitivity", []))

    @jsii.member(jsii_name="resetFieldPairs")
    def reset_field_pairs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldPairs", []))

    @jsii.member(jsii_name="resetIfNotExists")
    def reset_if_not_exists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIfNotExists", []))

    @jsii.member(jsii_name="resetSourceKeys")
    def reset_source_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceKeys", []))

    @jsii.member(jsii_name="resetTableName")
    def reset_table_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableName", []))

    @builtins.property
    @jsii.member(jsii_name="fieldPairs")
    def field_pairs(self) -> TagPipelineRulesetRulesReferenceTableFieldPairsList:
        return typing.cast(TagPipelineRulesetRulesReferenceTableFieldPairsList, jsii.get(self, "fieldPairs"))

    @builtins.property
    @jsii.member(jsii_name="caseInsensitivityInput")
    def case_insensitivity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "caseInsensitivityInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldPairsInput")
    def field_pairs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TagPipelineRulesetRulesReferenceTableFieldPairs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TagPipelineRulesetRulesReferenceTableFieldPairs]]], jsii.get(self, "fieldPairsInput"))

    @builtins.property
    @jsii.member(jsii_name="ifNotExistsInput")
    def if_not_exists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ifNotExistsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceKeysInput")
    def source_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="caseInsensitivity")
    def case_insensitivity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "caseInsensitivity"))

    @case_insensitivity.setter
    def case_insensitivity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb324323f6996e89b8a62ce428c033d2f6457ab970f9acd0b9cf7e2eb05a1379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caseInsensitivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ifNotExists")
    def if_not_exists(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ifNotExists"))

    @if_not_exists.setter
    def if_not_exists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f788fd74349884cf2f8c2b7b3e3780bd4faffc66a4abbe7e0b882365f2f75095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ifNotExists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceKeys")
    def source_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceKeys"))

    @source_keys.setter
    def source_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf07d931e74670065b4774a764f7c5a61be9cd05761a989f792b7dacc61097f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19da18015ddb5e8df7e4aaebfd1b1ecb231212547f494c5b4da7b3f9a4e218be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesReferenceTable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesReferenceTable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesReferenceTable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad19a1c071484a51cfa1e9040db813eaee1114eba2e4c505a9dab2ba42b3c9da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "TagPipelineRuleset",
    "TagPipelineRulesetConfig",
    "TagPipelineRulesetRules",
    "TagPipelineRulesetRulesList",
    "TagPipelineRulesetRulesMapping",
    "TagPipelineRulesetRulesMappingOutputReference",
    "TagPipelineRulesetRulesOutputReference",
    "TagPipelineRulesetRulesQuery",
    "TagPipelineRulesetRulesQueryAddition",
    "TagPipelineRulesetRulesQueryAdditionOutputReference",
    "TagPipelineRulesetRulesQueryOutputReference",
    "TagPipelineRulesetRulesReferenceTable",
    "TagPipelineRulesetRulesReferenceTableFieldPairs",
    "TagPipelineRulesetRulesReferenceTableFieldPairsList",
    "TagPipelineRulesetRulesReferenceTableFieldPairsOutputReference",
    "TagPipelineRulesetRulesReferenceTableOutputReference",
]

publication.publish()

def _typecheckingstub__a92f9ba5339b69a3e4905493e75064858bae350eaf456419c20b58025b60da23(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TagPipelineRulesetRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__0c6c73171c16a25328008ac696004a00b0df806a9773dc7aab74b74780a43928(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c74a71eedd7743c45d85276da9b2c7bd93c2cbee59cb229122cff5ef98784c6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TagPipelineRulesetRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502df55f0c92f531841ea2e64e39427651a9415617117b3fb3f19f98c5e94e75(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e87ca17b7155a784cbb9d9826f15877ffac3afc7291e65c645c554de9b4812(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c04832b1785b97f2fd63968065ddd9247d0f8ee6ebda4d77f42d00b2c1e9fb8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TagPipelineRulesetRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a185b032a072e255d5f4506c62a0b02b03650b77b01f62d87fe79b06429775(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    mapping: typing.Optional[typing.Union[TagPipelineRulesetRulesMapping, typing.Dict[builtins.str, typing.Any]]] = None,
    query: typing.Optional[typing.Union[TagPipelineRulesetRulesQuery, typing.Dict[builtins.str, typing.Any]]] = None,
    reference_table: typing.Optional[typing.Union[TagPipelineRulesetRulesReferenceTable, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1e2c38b04eed4f5a9b93a0227ab8945a1f175b07e65007beb58e683369fb9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38fef41f75426dec7c9e3de5bfcf555883b2d5734f0688fe79e9856b4517a25c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14dbe24978bdd79e6521c706d3981f074756ad1a121873e5f89fc8be367c0dc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e1b5b6a9ba3c1f67877e81fb54969b010fd32a52a592ddf5b051b21629fbcd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b76c8fbc797d5adedfd2def77d081969ccf152fca5cc2368c26d5e317e35dc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f632c97e3c13d4db26a3e703417a37d984ed072eb13f86d5c16eed34f52d9c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TagPipelineRulesetRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6a866a2cca0f239bde876a74efd66af707cb5bfb3f7487270f390b86c8e2fc(
    *,
    destination_key: typing.Optional[builtins.str] = None,
    if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee16de0c47109eb84be7ae116e3c46461653143511ff48695d12c4f29cf165a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad396d17b67e996f524dad60dcbaab5f17a0657468181f2caa737c54ffd1971(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e05bc6423eec2a5ca966b40fbde04982ad6c2cdef4412b4340f29ac4bc27e2d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ed7f651f1cbb4d4dab342534b7fb479f8389514e4cd32ccf717a1fc4e40029(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079851e7fd37ae539c76d8e13b33bcc3565ca59262433d6ae54dbafd7c4f668f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesMapping]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef8091d86bc6050eb9a9879acc94fa9d0eef6f159491889664512f1efa7fdd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9788061eb18616d4a2e712aa665b0c5ad1877879017806428984a226b9d45e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180428b65d61529354d0ae38053568dac6aa2d1f264b37b60fe5d8d573dd722c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9750722f6c0b8605d105b555fc8f1ee6d7d1117fbdd55f1783516671017eac14(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f571867be6084a4faa451ee7fb9d0bc3ac21e391ddac4ceb6443dcf17852ff0(
    *,
    addition: typing.Optional[typing.Union[TagPipelineRulesetRulesQueryAddition, typing.Dict[builtins.str, typing.Any]]] = None,
    case_insensitivity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02775fed86635da844e67da8855c6bdda3ac5e7f41e054b8746d2bc71e1b094a(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1160d02a933873f42c62d69f1480921a8f7131525c84473f04be56aa1cfd9b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9620ed5cc40eb38a48d09cb3b66a4529813bd53911e445694d550b2ffe0a7bed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09bffe4cb6d6e23fd4624bae25a728ef6ff9352730e1109d85d0e21716d96cc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db65ec48e7e4a420c5d6222dbc288e169fc30d527e8d6b6a1c886c2973f3663(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesQueryAddition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d496e1b7b9b87f0acba344a3e96892d0237844fa2233124abd367f21524a2261(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5cde3bfa8de3dd71dae8b370e6d547b9127742a77cc8fc58eb8e4864ec5f74f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6f8bac2cd2b8c59ff6b02b0f9c0c7db2d15f9d06f840698954d213655fa8ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb28946ee9a1ab4e17bb68fb0040db6769be393f77bcd1c7bdb759d02233a8a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0fe3ed5cd7e6f1d45b368e7fe1a26a9672f5d1fd8b86937973961226e1cfe3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesQuery]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd6ed2aeb3e27338c9b16554bda258d12e0ea4080b66c0b579d4233c2ce8bfa(
    *,
    case_insensitivity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    field_pairs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TagPipelineRulesetRulesReferenceTableFieldPairs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d5d370e46bb56faa883d3a3972bbacc811737a5633979d75851ad571feaec5(
    *,
    input_column: typing.Optional[builtins.str] = None,
    output_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b0a3eec2001050c42c2766c42c1769233b78e144505d7903fde32c9cad7bef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e260e1096b4568db9588c76cce9350ab4064821700227d38fc940a9cdcf193(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3b970e5288a2c12b8c38e4b73b3539297d02dd717bf3909546f64eba5dfaf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2701c5b3e55e8e176ebbce794390c553f5f76f0eb5b8eb6a48ab52dadfbb775c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a1f0d1f7f9b7e753712295ef3d34d919cf9f50ed4eccd68bcec4432726353a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094355a9daad48c732d2c07a7f29b7d120a360c63e8c4eff1a226b2c6b031cfb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TagPipelineRulesetRulesReferenceTableFieldPairs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a70d0d2478834f8e75175209af1dad712cfabca321005a38284d0ad4f5f1939(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2bfc3b08f43d1414e1c9a2e32b59472e57cd9891803fa8f04991b4a8be061cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20aa0c46a05a95bed0b234b81d2b1b1736cf2a20d1268aa3dd1d426d3cb82bf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca80c13637efc7c826a68e391de67cf362e95f2396e36113866f6d9e81db67ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesReferenceTableFieldPairs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f206056274526c1f69be6d02ef4316533d53617dac7b6dd5e4e8e2e2f9bce25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6e35fcdd6de2eaba8a242686ecb73be3f980740e9c3c94988751d8da5f97b7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TagPipelineRulesetRulesReferenceTableFieldPairs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb324323f6996e89b8a62ce428c033d2f6457ab970f9acd0b9cf7e2eb05a1379(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f788fd74349884cf2f8c2b7b3e3780bd4faffc66a4abbe7e0b882365f2f75095(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf07d931e74670065b4774a764f7c5a61be9cd05761a989f792b7dacc61097f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19da18015ddb5e8df7e4aaebfd1b1ecb231212547f494c5b4da7b3f9a4e218be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad19a1c071484a51cfa1e9040db813eaee1114eba2e4c505a9dab2ba42b3c9da(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TagPipelineRulesetRulesReferenceTable]],
) -> None:
    """Type checking stubs"""
    pass
