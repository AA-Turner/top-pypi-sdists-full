r'''
# `datadog_sensitive_data_scanner_rule`

Refer to the Terraform Registry for docs: [`datadog_sensitive_data_scanner_rule`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule).
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


class SensitiveDataScannerRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.sensitiveDataScannerRule.SensitiveDataScannerRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule datadog_sensitive_data_scanner_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        group_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        excluded_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        included_keyword_configuration: typing.Optional[typing.Union["SensitiveDataScannerRuleIncludedKeywordConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        pattern: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        standard_pattern_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        text_replacement: typing.Optional[typing.Union["SensitiveDataScannerRuleTextReplacement", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule datadog_sensitive_data_scanner_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param group_id: Id of the scanning group the rule belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#group_id SensitiveDataScannerRule#group_id}
        :param description: Description of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#description SensitiveDataScannerRule#description}
        :param excluded_namespaces: Attributes excluded from the scan. If namespaces is provided, it has to be a sub-path of the namespaces array. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#excluded_namespaces SensitiveDataScannerRule#excluded_namespaces}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#id SensitiveDataScannerRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param included_keyword_configuration: included_keyword_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#included_keyword_configuration SensitiveDataScannerRule#included_keyword_configuration}
        :param is_enabled: Whether or not the rule is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#is_enabled SensitiveDataScannerRule#is_enabled}
        :param name: Name of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#name SensitiveDataScannerRule#name}
        :param namespaces: Attributes included in the scan. If namespaces is empty or missing, all attributes except excluded_namespaces are scanned. If both are missing the whole event is scanned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#namespaces SensitiveDataScannerRule#namespaces}
        :param pattern: Not included if there is a relationship to a standard pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#pattern SensitiveDataScannerRule#pattern}
        :param priority: Priority level of the rule (optional). Used to order sensitive data discovered in the sds summary page. It must be between 1 and 5 (1 being the most important). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#priority SensitiveDataScannerRule#priority}
        :param standard_pattern_id: Id of the standard pattern the rule refers to. If provided, then pattern must not be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#standard_pattern_id SensitiveDataScannerRule#standard_pattern_id}
        :param tags: List of tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#tags SensitiveDataScannerRule#tags}
        :param text_replacement: text_replacement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#text_replacement SensitiveDataScannerRule#text_replacement}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b59a8e9ca37aa4861d3053ff6381230f5a3f9883dbec45b78452807ff6c0eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SensitiveDataScannerRuleConfig(
            group_id=group_id,
            description=description,
            excluded_namespaces=excluded_namespaces,
            id=id,
            included_keyword_configuration=included_keyword_configuration,
            is_enabled=is_enabled,
            name=name,
            namespaces=namespaces,
            pattern=pattern,
            priority=priority,
            standard_pattern_id=standard_pattern_id,
            tags=tags,
            text_replacement=text_replacement,
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
        '''Generates CDKTF code for importing a SensitiveDataScannerRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SensitiveDataScannerRule to import.
        :param import_from_id: The id of the existing SensitiveDataScannerRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SensitiveDataScannerRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61627d7a9ffdd6a0de3bb114766dc156413efd9623841582c7e0da10e928d23)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIncludedKeywordConfiguration")
    def put_included_keyword_configuration(
        self,
        *,
        character_count: jsii.Number,
        keywords: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param character_count: Number of characters before the match to find a keyword validating the match. It must be between 1 and 50 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#character_count SensitiveDataScannerRule#character_count}
        :param keywords: Keyword list that is checked during scanning in order to validate a match. The number of keywords in the list must be lower than or equal to 30. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#keywords SensitiveDataScannerRule#keywords}
        '''
        value = SensitiveDataScannerRuleIncludedKeywordConfiguration(
            character_count=character_count, keywords=keywords
        )

        return typing.cast(None, jsii.invoke(self, "putIncludedKeywordConfiguration", [value]))

    @jsii.member(jsii_name="putTextReplacement")
    def put_text_replacement(
        self,
        *,
        type: builtins.str,
        number_of_chars: typing.Optional[jsii.Number] = None,
        replacement_string: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of the replacement text. None means no replacement. hash means the data will be stubbed. replacement_string means that one can chose a text to replace the data. partial_replacement_from_beginning allows a user to partially replace the data from the beginning, and partial_replacement_from_end on the other hand, allows to replace data from the end. Valid values are ``none``, ``hash``, ``replacement_string``, ``partial_replacement_from_beginning``, ``partial_replacement_from_end``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#type SensitiveDataScannerRule#type}
        :param number_of_chars: Required if type == 'partial_replacement_from_beginning' or 'partial_replacement_from_end'. It must be > 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#number_of_chars SensitiveDataScannerRule#number_of_chars}
        :param replacement_string: Required if type == 'replacement_string'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#replacement_string SensitiveDataScannerRule#replacement_string}
        '''
        value = SensitiveDataScannerRuleTextReplacement(
            type=type,
            number_of_chars=number_of_chars,
            replacement_string=replacement_string,
        )

        return typing.cast(None, jsii.invoke(self, "putTextReplacement", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExcludedNamespaces")
    def reset_excluded_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedNamespaces", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludedKeywordConfiguration")
    def reset_included_keyword_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedKeywordConfiguration", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamespaces")
    def reset_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespaces", []))

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetStandardPatternId")
    def reset_standard_pattern_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStandardPatternId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTextReplacement")
    def reset_text_replacement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTextReplacement", []))

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
    @jsii.member(jsii_name="includedKeywordConfiguration")
    def included_keyword_configuration(
        self,
    ) -> "SensitiveDataScannerRuleIncludedKeywordConfigurationOutputReference":
        return typing.cast("SensitiveDataScannerRuleIncludedKeywordConfigurationOutputReference", jsii.get(self, "includedKeywordConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="textReplacement")
    def text_replacement(
        self,
    ) -> "SensitiveDataScannerRuleTextReplacementOutputReference":
        return typing.cast("SensitiveDataScannerRuleTextReplacementOutputReference", jsii.get(self, "textReplacement"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedNamespacesInput")
    def excluded_namespaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includedKeywordConfigurationInput")
    def included_keyword_configuration_input(
        self,
    ) -> typing.Optional["SensitiveDataScannerRuleIncludedKeywordConfiguration"]:
        return typing.cast(typing.Optional["SensitiveDataScannerRuleIncludedKeywordConfiguration"], jsii.get(self, "includedKeywordConfigurationInput"))

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
    @jsii.member(jsii_name="namespacesInput")
    def namespaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "namespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="standardPatternIdInput")
    def standard_pattern_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "standardPatternIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="textReplacementInput")
    def text_replacement_input(
        self,
    ) -> typing.Optional["SensitiveDataScannerRuleTextReplacement"]:
        return typing.cast(typing.Optional["SensitiveDataScannerRuleTextReplacement"], jsii.get(self, "textReplacementInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338dd0606c279d14880622e3d49720d03a8216a11faae27d8b860768b919e9b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedNamespaces")
    def excluded_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedNamespaces"))

    @excluded_namespaces.setter
    def excluded_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd881f3aba9373406381db0859c871fd4da8c7e250bb24e1fe9b2c53290eb4a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94527bba4707c56474bfecb5a2490255a3a068231f6447e5681350f76eaf799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425b096a730a25a0417788801d7d4fecee760f7e92546806661a9b96c3cb1502)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40ab3cb25f3daaaa6d3c84b493d7a99a1a024b6071ab3657e82cc9431bd9fd5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7659eb229a15b8541d21e9bf3c80d703caf0d6e7b87cf32f9f4467a8d8c4f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespaces")
    def namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "namespaces"))

    @namespaces.setter
    def namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c303028ed99523ca770939f016d11cebd96e9577bb47147a16f0b6d2d35fbec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff0c3c35c668fca73546b53eba5ebb510616ac3faaa47fb994552feeff3bd36f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e0b87365c1f93540f34e2696f52e4e3d2cda4de84f03f236801bd4775abeff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="standardPatternId")
    def standard_pattern_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "standardPatternId"))

    @standard_pattern_id.setter
    def standard_pattern_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87452c45ff713516525fabaabfc749fa28ddd310af13a04a479b9ee2c16344b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standardPatternId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c44bc0182c43d10143cc0d5dde1b0de72b1ca2a05e5414ea2905fd7ba30dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.sensitiveDataScannerRule.SensitiveDataScannerRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "group_id": "groupId",
        "description": "description",
        "excluded_namespaces": "excludedNamespaces",
        "id": "id",
        "included_keyword_configuration": "includedKeywordConfiguration",
        "is_enabled": "isEnabled",
        "name": "name",
        "namespaces": "namespaces",
        "pattern": "pattern",
        "priority": "priority",
        "standard_pattern_id": "standardPatternId",
        "tags": "tags",
        "text_replacement": "textReplacement",
    },
)
class SensitiveDataScannerRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        group_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        excluded_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        included_keyword_configuration: typing.Optional[typing.Union["SensitiveDataScannerRuleIncludedKeywordConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        pattern: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        standard_pattern_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        text_replacement: typing.Optional[typing.Union["SensitiveDataScannerRuleTextReplacement", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param group_id: Id of the scanning group the rule belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#group_id SensitiveDataScannerRule#group_id}
        :param description: Description of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#description SensitiveDataScannerRule#description}
        :param excluded_namespaces: Attributes excluded from the scan. If namespaces is provided, it has to be a sub-path of the namespaces array. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#excluded_namespaces SensitiveDataScannerRule#excluded_namespaces}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#id SensitiveDataScannerRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param included_keyword_configuration: included_keyword_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#included_keyword_configuration SensitiveDataScannerRule#included_keyword_configuration}
        :param is_enabled: Whether or not the rule is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#is_enabled SensitiveDataScannerRule#is_enabled}
        :param name: Name of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#name SensitiveDataScannerRule#name}
        :param namespaces: Attributes included in the scan. If namespaces is empty or missing, all attributes except excluded_namespaces are scanned. If both are missing the whole event is scanned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#namespaces SensitiveDataScannerRule#namespaces}
        :param pattern: Not included if there is a relationship to a standard pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#pattern SensitiveDataScannerRule#pattern}
        :param priority: Priority level of the rule (optional). Used to order sensitive data discovered in the sds summary page. It must be between 1 and 5 (1 being the most important). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#priority SensitiveDataScannerRule#priority}
        :param standard_pattern_id: Id of the standard pattern the rule refers to. If provided, then pattern must not be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#standard_pattern_id SensitiveDataScannerRule#standard_pattern_id}
        :param tags: List of tags. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#tags SensitiveDataScannerRule#tags}
        :param text_replacement: text_replacement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#text_replacement SensitiveDataScannerRule#text_replacement}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(included_keyword_configuration, dict):
            included_keyword_configuration = SensitiveDataScannerRuleIncludedKeywordConfiguration(**included_keyword_configuration)
        if isinstance(text_replacement, dict):
            text_replacement = SensitiveDataScannerRuleTextReplacement(**text_replacement)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd33bf6184e55ef2b5d4723dfce9e7a8a2a4451f6a23621b4f7a11229756f444)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument excluded_namespaces", value=excluded_namespaces, expected_type=type_hints["excluded_namespaces"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument included_keyword_configuration", value=included_keyword_configuration, expected_type=type_hints["included_keyword_configuration"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument standard_pattern_id", value=standard_pattern_id, expected_type=type_hints["standard_pattern_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument text_replacement", value=text_replacement, expected_type=type_hints["text_replacement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_id": group_id,
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
        if excluded_namespaces is not None:
            self._values["excluded_namespaces"] = excluded_namespaces
        if id is not None:
            self._values["id"] = id
        if included_keyword_configuration is not None:
            self._values["included_keyword_configuration"] = included_keyword_configuration
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if name is not None:
            self._values["name"] = name
        if namespaces is not None:
            self._values["namespaces"] = namespaces
        if pattern is not None:
            self._values["pattern"] = pattern
        if priority is not None:
            self._values["priority"] = priority
        if standard_pattern_id is not None:
            self._values["standard_pattern_id"] = standard_pattern_id
        if tags is not None:
            self._values["tags"] = tags
        if text_replacement is not None:
            self._values["text_replacement"] = text_replacement

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
    def group_id(self) -> builtins.str:
        '''Id of the scanning group the rule belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#group_id SensitiveDataScannerRule#group_id}
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#description SensitiveDataScannerRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def excluded_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Attributes excluded from the scan. If namespaces is provided, it has to be a sub-path of the namespaces array.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#excluded_namespaces SensitiveDataScannerRule#excluded_namespaces}
        '''
        result = self._values.get("excluded_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#id SensitiveDataScannerRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def included_keyword_configuration(
        self,
    ) -> typing.Optional["SensitiveDataScannerRuleIncludedKeywordConfiguration"]:
        '''included_keyword_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#included_keyword_configuration SensitiveDataScannerRule#included_keyword_configuration}
        '''
        result = self._values.get("included_keyword_configuration")
        return typing.cast(typing.Optional["SensitiveDataScannerRuleIncludedKeywordConfiguration"], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the rule is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#is_enabled SensitiveDataScannerRule#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#name SensitiveDataScannerRule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Attributes included in the scan.

        If namespaces is empty or missing, all attributes except excluded_namespaces are scanned. If both are missing the whole event is scanned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#namespaces SensitiveDataScannerRule#namespaces}
        '''
        result = self._values.get("namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pattern(self) -> typing.Optional[builtins.str]:
        '''Not included if there is a relationship to a standard pattern.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#pattern SensitiveDataScannerRule#pattern}
        '''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Priority level of the rule (optional).

        Used to order sensitive data discovered in the sds summary page. It must be between 1 and 5 (1 being the most important).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#priority SensitiveDataScannerRule#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def standard_pattern_id(self) -> typing.Optional[builtins.str]:
        '''Id of the standard pattern the rule refers to. If provided, then pattern must not be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#standard_pattern_id SensitiveDataScannerRule#standard_pattern_id}
        '''
        result = self._values.get("standard_pattern_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of tags.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#tags SensitiveDataScannerRule#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def text_replacement(
        self,
    ) -> typing.Optional["SensitiveDataScannerRuleTextReplacement"]:
        '''text_replacement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#text_replacement SensitiveDataScannerRule#text_replacement}
        '''
        result = self._values.get("text_replacement")
        return typing.cast(typing.Optional["SensitiveDataScannerRuleTextReplacement"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SensitiveDataScannerRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.sensitiveDataScannerRule.SensitiveDataScannerRuleIncludedKeywordConfiguration",
    jsii_struct_bases=[],
    name_mapping={"character_count": "characterCount", "keywords": "keywords"},
)
class SensitiveDataScannerRuleIncludedKeywordConfiguration:
    def __init__(
        self,
        *,
        character_count: jsii.Number,
        keywords: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param character_count: Number of characters before the match to find a keyword validating the match. It must be between 1 and 50 (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#character_count SensitiveDataScannerRule#character_count}
        :param keywords: Keyword list that is checked during scanning in order to validate a match. The number of keywords in the list must be lower than or equal to 30. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#keywords SensitiveDataScannerRule#keywords}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a51a6d386a842e115acd9b6533ba502016def404fd7c862b5c18b7771efaa78d)
            check_type(argname="argument character_count", value=character_count, expected_type=type_hints["character_count"])
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "character_count": character_count,
            "keywords": keywords,
        }

    @builtins.property
    def character_count(self) -> jsii.Number:
        '''Number of characters before the match to find a keyword validating the match.

        It must be between 1 and 50 (inclusive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#character_count SensitiveDataScannerRule#character_count}
        '''
        result = self._values.get("character_count")
        assert result is not None, "Required property 'character_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def keywords(self) -> typing.List[builtins.str]:
        '''Keyword list that is checked during scanning in order to validate a match.

        The number of keywords in the list must be lower than or equal to 30.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#keywords SensitiveDataScannerRule#keywords}
        '''
        result = self._values.get("keywords")
        assert result is not None, "Required property 'keywords' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SensitiveDataScannerRuleIncludedKeywordConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SensitiveDataScannerRuleIncludedKeywordConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.sensitiveDataScannerRule.SensitiveDataScannerRuleIncludedKeywordConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d5abf595e7cbbac6fbbdd60ebeb17f5d66523e58225c783cba103a78c8c0f3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="characterCountInput")
    def character_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "characterCountInput"))

    @builtins.property
    @jsii.member(jsii_name="keywordsInput")
    def keywords_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "keywordsInput"))

    @builtins.property
    @jsii.member(jsii_name="characterCount")
    def character_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "characterCount"))

    @character_count.setter
    def character_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e05377cdaf2553bf412109634c6777d170caf55fab16853bae55b7499fe508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "characterCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keywords")
    def keywords(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "keywords"))

    @keywords.setter
    def keywords(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8ee30af8caf6354bfb7b4273c56cd4becc301c9aa1ddc87dccb19d30467d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keywords", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SensitiveDataScannerRuleIncludedKeywordConfiguration]:
        return typing.cast(typing.Optional[SensitiveDataScannerRuleIncludedKeywordConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SensitiveDataScannerRuleIncludedKeywordConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57567ab143c4cad6f94a40cdd84cd9e77abc7559276fe2f00a9ebf0196faf4ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.sensitiveDataScannerRule.SensitiveDataScannerRuleTextReplacement",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "number_of_chars": "numberOfChars",
        "replacement_string": "replacementString",
    },
)
class SensitiveDataScannerRuleTextReplacement:
    def __init__(
        self,
        *,
        type: builtins.str,
        number_of_chars: typing.Optional[jsii.Number] = None,
        replacement_string: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of the replacement text. None means no replacement. hash means the data will be stubbed. replacement_string means that one can chose a text to replace the data. partial_replacement_from_beginning allows a user to partially replace the data from the beginning, and partial_replacement_from_end on the other hand, allows to replace data from the end. Valid values are ``none``, ``hash``, ``replacement_string``, ``partial_replacement_from_beginning``, ``partial_replacement_from_end``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#type SensitiveDataScannerRule#type}
        :param number_of_chars: Required if type == 'partial_replacement_from_beginning' or 'partial_replacement_from_end'. It must be > 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#number_of_chars SensitiveDataScannerRule#number_of_chars}
        :param replacement_string: Required if type == 'replacement_string'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#replacement_string SensitiveDataScannerRule#replacement_string}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37b96a7b75e670855fd80eaf64ea23f8ef52e4825ede9da1bfb81c69f032c6c)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument number_of_chars", value=number_of_chars, expected_type=type_hints["number_of_chars"])
            check_type(argname="argument replacement_string", value=replacement_string, expected_type=type_hints["replacement_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if number_of_chars is not None:
            self._values["number_of_chars"] = number_of_chars
        if replacement_string is not None:
            self._values["replacement_string"] = replacement_string

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of the replacement text.

        None means no replacement. hash means the data will be stubbed. replacement_string means that one can chose a text to replace the data. partial_replacement_from_beginning allows a user to partially replace the data from the beginning, and partial_replacement_from_end on the other hand, allows to replace data from the end. Valid values are ``none``, ``hash``, ``replacement_string``, ``partial_replacement_from_beginning``, ``partial_replacement_from_end``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#type SensitiveDataScannerRule#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def number_of_chars(self) -> typing.Optional[jsii.Number]:
        '''Required if type == 'partial_replacement_from_beginning' or 'partial_replacement_from_end'. It must be > 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#number_of_chars SensitiveDataScannerRule#number_of_chars}
        '''
        result = self._values.get("number_of_chars")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replacement_string(self) -> typing.Optional[builtins.str]:
        '''Required if type == 'replacement_string'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/sensitive_data_scanner_rule#replacement_string SensitiveDataScannerRule#replacement_string}
        '''
        result = self._values.get("replacement_string")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SensitiveDataScannerRuleTextReplacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SensitiveDataScannerRuleTextReplacementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.sensitiveDataScannerRule.SensitiveDataScannerRuleTextReplacementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6781e81ece16c2b723c3bece41b8ed7e3003e3154e846aa51fd800e088b4a894)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNumberOfChars")
    def reset_number_of_chars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberOfChars", []))

    @jsii.member(jsii_name="resetReplacementString")
    def reset_replacement_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplacementString", []))

    @builtins.property
    @jsii.member(jsii_name="numberOfCharsInput")
    def number_of_chars_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfCharsInput"))

    @builtins.property
    @jsii.member(jsii_name="replacementStringInput")
    def replacement_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replacementStringInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfChars")
    def number_of_chars(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfChars"))

    @number_of_chars.setter
    def number_of_chars(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad6e77eaf467727a7fb2e7ecfae8190d2e3769bf9bd6df97db28e9eab397576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfChars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replacementString")
    def replacement_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replacementString"))

    @replacement_string.setter
    def replacement_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b122b68b89d872411eef87665140c8a7c3c0f11b162e7f13b712703e015aeb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replacementString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5820530810d49825e3a84eec446a9838daa1c8a95dd0de4a840899d2a472f2ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SensitiveDataScannerRuleTextReplacement]:
        return typing.cast(typing.Optional[SensitiveDataScannerRuleTextReplacement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SensitiveDataScannerRuleTextReplacement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a7984099d8e367614b791de3d760e3b7f2136044166ad1845643b1691e3b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SensitiveDataScannerRule",
    "SensitiveDataScannerRuleConfig",
    "SensitiveDataScannerRuleIncludedKeywordConfiguration",
    "SensitiveDataScannerRuleIncludedKeywordConfigurationOutputReference",
    "SensitiveDataScannerRuleTextReplacement",
    "SensitiveDataScannerRuleTextReplacementOutputReference",
]

publication.publish()

def _typecheckingstub__74b59a8e9ca37aa4861d3053ff6381230f5a3f9883dbec45b78452807ff6c0eb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    group_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    excluded_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    included_keyword_configuration: typing.Optional[typing.Union[SensitiveDataScannerRuleIncludedKeywordConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    pattern: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    standard_pattern_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    text_replacement: typing.Optional[typing.Union[SensitiveDataScannerRuleTextReplacement, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e61627d7a9ffdd6a0de3bb114766dc156413efd9623841582c7e0da10e928d23(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338dd0606c279d14880622e3d49720d03a8216a11faae27d8b860768b919e9b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd881f3aba9373406381db0859c871fd4da8c7e250bb24e1fe9b2c53290eb4a9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94527bba4707c56474bfecb5a2490255a3a068231f6447e5681350f76eaf799(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425b096a730a25a0417788801d7d4fecee760f7e92546806661a9b96c3cb1502(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ab3cb25f3daaaa6d3c84b493d7a99a1a024b6071ab3657e82cc9431bd9fd5f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7659eb229a15b8541d21e9bf3c80d703caf0d6e7b87cf32f9f4467a8d8c4f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c303028ed99523ca770939f016d11cebd96e9577bb47147a16f0b6d2d35fbec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0c3c35c668fca73546b53eba5ebb510616ac3faaa47fb994552feeff3bd36f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e0b87365c1f93540f34e2696f52e4e3d2cda4de84f03f236801bd4775abeff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87452c45ff713516525fabaabfc749fa28ddd310af13a04a479b9ee2c16344b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c44bc0182c43d10143cc0d5dde1b0de72b1ca2a05e5414ea2905fd7ba30dba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd33bf6184e55ef2b5d4723dfce9e7a8a2a4451f6a23621b4f7a11229756f444(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    excluded_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    included_keyword_configuration: typing.Optional[typing.Union[SensitiveDataScannerRuleIncludedKeywordConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    pattern: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    standard_pattern_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    text_replacement: typing.Optional[typing.Union[SensitiveDataScannerRuleTextReplacement, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51a6d386a842e115acd9b6533ba502016def404fd7c862b5c18b7771efaa78d(
    *,
    character_count: jsii.Number,
    keywords: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5abf595e7cbbac6fbbdd60ebeb17f5d66523e58225c783cba103a78c8c0f3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e05377cdaf2553bf412109634c6777d170caf55fab16853bae55b7499fe508(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8ee30af8caf6354bfb7b4273c56cd4becc301c9aa1ddc87dccb19d30467d5e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57567ab143c4cad6f94a40cdd84cd9e77abc7559276fe2f00a9ebf0196faf4ec(
    value: typing.Optional[SensitiveDataScannerRuleIncludedKeywordConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37b96a7b75e670855fd80eaf64ea23f8ef52e4825ede9da1bfb81c69f032c6c(
    *,
    type: builtins.str,
    number_of_chars: typing.Optional[jsii.Number] = None,
    replacement_string: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6781e81ece16c2b723c3bece41b8ed7e3003e3154e846aa51fd800e088b4a894(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad6e77eaf467727a7fb2e7ecfae8190d2e3769bf9bd6df97db28e9eab397576(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b122b68b89d872411eef87665140c8a7c3c0f11b162e7f13b712703e015aeb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5820530810d49825e3a84eec446a9838daa1c8a95dd0de4a840899d2a472f2ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a7984099d8e367614b791de3d760e3b7f2136044166ad1845643b1691e3b29(
    value: typing.Optional[SensitiveDataScannerRuleTextReplacement],
) -> None:
    """Type checking stubs"""
    pass
