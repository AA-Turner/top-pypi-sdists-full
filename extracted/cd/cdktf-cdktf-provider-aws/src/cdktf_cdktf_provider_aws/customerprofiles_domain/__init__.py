r'''
# `aws_customerprofiles_domain`

Refer to the Terraform Registry for docs: [`aws_customerprofiles_domain`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain).
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


class CustomerprofilesDomain(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomain",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain aws_customerprofiles_domain}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_expiration_days: jsii.Number,
        domain_name: builtins.str,
        dead_letter_queue_url: typing.Optional[builtins.str] = None,
        default_encryption_key: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        matching: typing.Optional[typing.Union["CustomerprofilesDomainMatching", typing.Dict[builtins.str, typing.Any]]] = None,
        rule_based_matching: typing.Optional[typing.Union["CustomerprofilesDomainRuleBasedMatching", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain aws_customerprofiles_domain} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_expiration_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#default_expiration_days CustomerprofilesDomain#default_expiration_days}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#domain_name CustomerprofilesDomain#domain_name}.
        :param dead_letter_queue_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#dead_letter_queue_url CustomerprofilesDomain#dead_letter_queue_url}.
        :param default_encryption_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#default_encryption_key CustomerprofilesDomain#default_encryption_key}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#id CustomerprofilesDomain#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param matching: matching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#matching CustomerprofilesDomain#matching}
        :param rule_based_matching: rule_based_matching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#rule_based_matching CustomerprofilesDomain#rule_based_matching}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#tags CustomerprofilesDomain#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#tags_all CustomerprofilesDomain#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3164d89b8342fd58c32815aa8c98563fd5f007db5985969185441340bcffc6e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CustomerprofilesDomainConfig(
            default_expiration_days=default_expiration_days,
            domain_name=domain_name,
            dead_letter_queue_url=dead_letter_queue_url,
            default_encryption_key=default_encryption_key,
            id=id,
            matching=matching,
            rule_based_matching=rule_based_matching,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a CustomerprofilesDomain resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CustomerprofilesDomain to import.
        :param import_from_id: The id of the existing CustomerprofilesDomain that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CustomerprofilesDomain to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04166869dc2f1caf55008d5f0d8866410141b4b5d936471127e898b09ae4d63d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putMatching")
    def put_matching(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        auto_merging: typing.Optional[typing.Union["CustomerprofilesDomainMatchingAutoMerging", typing.Dict[builtins.str, typing.Any]]] = None,
        exporting_config: typing.Optional[typing.Union["CustomerprofilesDomainMatchingExportingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        job_schedule: typing.Optional[typing.Union["CustomerprofilesDomainMatchingJobSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#enabled CustomerprofilesDomain#enabled}.
        :param auto_merging: auto_merging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#auto_merging CustomerprofilesDomain#auto_merging}
        :param exporting_config: exporting_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#exporting_config CustomerprofilesDomain#exporting_config}
        :param job_schedule: job_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#job_schedule CustomerprofilesDomain#job_schedule}
        '''
        value = CustomerprofilesDomainMatching(
            enabled=enabled,
            auto_merging=auto_merging,
            exporting_config=exporting_config,
            job_schedule=job_schedule,
        )

        return typing.cast(None, jsii.invoke(self, "putMatching", [value]))

    @jsii.member(jsii_name="putRuleBasedMatching")
    def put_rule_based_matching(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        attribute_types_selector: typing.Optional[typing.Union["CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        conflict_resolution: typing.Optional[typing.Union["CustomerprofilesDomainRuleBasedMatchingConflictResolution", typing.Dict[builtins.str, typing.Any]]] = None,
        exporting_config: typing.Optional[typing.Union["CustomerprofilesDomainRuleBasedMatchingExportingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        matching_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomerprofilesDomainRuleBasedMatchingMatchingRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_allowed_rule_level_for_matching: typing.Optional[jsii.Number] = None,
        max_allowed_rule_level_for_merging: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#enabled CustomerprofilesDomain#enabled}.
        :param attribute_types_selector: attribute_types_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#attribute_types_selector CustomerprofilesDomain#attribute_types_selector}
        :param conflict_resolution: conflict_resolution block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#conflict_resolution CustomerprofilesDomain#conflict_resolution}
        :param exporting_config: exporting_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#exporting_config CustomerprofilesDomain#exporting_config}
        :param matching_rules: matching_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#matching_rules CustomerprofilesDomain#matching_rules}
        :param max_allowed_rule_level_for_matching: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#max_allowed_rule_level_for_matching CustomerprofilesDomain#max_allowed_rule_level_for_matching}.
        :param max_allowed_rule_level_for_merging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#max_allowed_rule_level_for_merging CustomerprofilesDomain#max_allowed_rule_level_for_merging}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#status CustomerprofilesDomain#status}.
        '''
        value = CustomerprofilesDomainRuleBasedMatching(
            enabled=enabled,
            attribute_types_selector=attribute_types_selector,
            conflict_resolution=conflict_resolution,
            exporting_config=exporting_config,
            matching_rules=matching_rules,
            max_allowed_rule_level_for_matching=max_allowed_rule_level_for_matching,
            max_allowed_rule_level_for_merging=max_allowed_rule_level_for_merging,
            status=status,
        )

        return typing.cast(None, jsii.invoke(self, "putRuleBasedMatching", [value]))

    @jsii.member(jsii_name="resetDeadLetterQueueUrl")
    def reset_dead_letter_queue_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeadLetterQueueUrl", []))

    @jsii.member(jsii_name="resetDefaultEncryptionKey")
    def reset_default_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultEncryptionKey", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMatching")
    def reset_matching(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatching", []))

    @jsii.member(jsii_name="resetRuleBasedMatching")
    def reset_rule_based_matching(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleBasedMatching", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="matching")
    def matching(self) -> "CustomerprofilesDomainMatchingOutputReference":
        return typing.cast("CustomerprofilesDomainMatchingOutputReference", jsii.get(self, "matching"))

    @builtins.property
    @jsii.member(jsii_name="ruleBasedMatching")
    def rule_based_matching(
        self,
    ) -> "CustomerprofilesDomainRuleBasedMatchingOutputReference":
        return typing.cast("CustomerprofilesDomainRuleBasedMatchingOutputReference", jsii.get(self, "ruleBasedMatching"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueueUrlInput")
    def dead_letter_queue_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deadLetterQueueUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultEncryptionKeyInput")
    def default_encryption_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultExpirationDaysInput")
    def default_expiration_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultExpirationDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingInput")
    def matching_input(self) -> typing.Optional["CustomerprofilesDomainMatching"]:
        return typing.cast(typing.Optional["CustomerprofilesDomainMatching"], jsii.get(self, "matchingInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleBasedMatchingInput")
    def rule_based_matching_input(
        self,
    ) -> typing.Optional["CustomerprofilesDomainRuleBasedMatching"]:
        return typing.cast(typing.Optional["CustomerprofilesDomainRuleBasedMatching"], jsii.get(self, "ruleBasedMatchingInput"))

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
    @jsii.member(jsii_name="deadLetterQueueUrl")
    def dead_letter_queue_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deadLetterQueueUrl"))

    @dead_letter_queue_url.setter
    def dead_letter_queue_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63634b1c9b6522bfdff7d0c63b8622d614f9694ae054be49384af403ce1f8dbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deadLetterQueueUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultEncryptionKey")
    def default_encryption_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultEncryptionKey"))

    @default_encryption_key.setter
    def default_encryption_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25c7d16683832cfc98b91aa56d9bf34bd62971257df4c70bfcdb5f9e0160db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultEncryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultExpirationDays")
    def default_expiration_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultExpirationDays"))

    @default_expiration_days.setter
    def default_expiration_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5503afc3aec7dcc21296c3de3f08d7c92320db35857bff6c33d470512cf35ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultExpirationDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60fadc617c4c7ad5f441582d39dec9bb8b2ff623ff070751cc6cb5a781ef997d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a51d9036e5e389e200e3da5cca394ed56c506bcd96cedc3b03bb1dfe22b2d15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8cc2905b7ec69cb9a8a65a9dd8cdc0afa32b377f2471d52570fc24b89c03063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8c4b2da9551a9e6f91c9e36d55d21bcdf3e6ca75d7b4aa6849ead381056c5fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_expiration_days": "defaultExpirationDays",
        "domain_name": "domainName",
        "dead_letter_queue_url": "deadLetterQueueUrl",
        "default_encryption_key": "defaultEncryptionKey",
        "id": "id",
        "matching": "matching",
        "rule_based_matching": "ruleBasedMatching",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class CustomerprofilesDomainConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_expiration_days: jsii.Number,
        domain_name: builtins.str,
        dead_letter_queue_url: typing.Optional[builtins.str] = None,
        default_encryption_key: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        matching: typing.Optional[typing.Union["CustomerprofilesDomainMatching", typing.Dict[builtins.str, typing.Any]]] = None,
        rule_based_matching: typing.Optional[typing.Union["CustomerprofilesDomainRuleBasedMatching", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_expiration_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#default_expiration_days CustomerprofilesDomain#default_expiration_days}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#domain_name CustomerprofilesDomain#domain_name}.
        :param dead_letter_queue_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#dead_letter_queue_url CustomerprofilesDomain#dead_letter_queue_url}.
        :param default_encryption_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#default_encryption_key CustomerprofilesDomain#default_encryption_key}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#id CustomerprofilesDomain#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param matching: matching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#matching CustomerprofilesDomain#matching}
        :param rule_based_matching: rule_based_matching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#rule_based_matching CustomerprofilesDomain#rule_based_matching}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#tags CustomerprofilesDomain#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#tags_all CustomerprofilesDomain#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(matching, dict):
            matching = CustomerprofilesDomainMatching(**matching)
        if isinstance(rule_based_matching, dict):
            rule_based_matching = CustomerprofilesDomainRuleBasedMatching(**rule_based_matching)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31303aaab3a3c03080857caca20b23e01f22a8a99e0cc0a86b328aea70ed099)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_expiration_days", value=default_expiration_days, expected_type=type_hints["default_expiration_days"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument dead_letter_queue_url", value=dead_letter_queue_url, expected_type=type_hints["dead_letter_queue_url"])
            check_type(argname="argument default_encryption_key", value=default_encryption_key, expected_type=type_hints["default_encryption_key"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument matching", value=matching, expected_type=type_hints["matching"])
            check_type(argname="argument rule_based_matching", value=rule_based_matching, expected_type=type_hints["rule_based_matching"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_expiration_days": default_expiration_days,
            "domain_name": domain_name,
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
        if dead_letter_queue_url is not None:
            self._values["dead_letter_queue_url"] = dead_letter_queue_url
        if default_encryption_key is not None:
            self._values["default_encryption_key"] = default_encryption_key
        if id is not None:
            self._values["id"] = id
        if matching is not None:
            self._values["matching"] = matching
        if rule_based_matching is not None:
            self._values["rule_based_matching"] = rule_based_matching
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def default_expiration_days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#default_expiration_days CustomerprofilesDomain#default_expiration_days}.'''
        result = self._values.get("default_expiration_days")
        assert result is not None, "Required property 'default_expiration_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#domain_name CustomerprofilesDomain#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dead_letter_queue_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#dead_letter_queue_url CustomerprofilesDomain#dead_letter_queue_url}.'''
        result = self._values.get("dead_letter_queue_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_encryption_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#default_encryption_key CustomerprofilesDomain#default_encryption_key}.'''
        result = self._values.get("default_encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#id CustomerprofilesDomain#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def matching(self) -> typing.Optional["CustomerprofilesDomainMatching"]:
        '''matching block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#matching CustomerprofilesDomain#matching}
        '''
        result = self._values.get("matching")
        return typing.cast(typing.Optional["CustomerprofilesDomainMatching"], result)

    @builtins.property
    def rule_based_matching(
        self,
    ) -> typing.Optional["CustomerprofilesDomainRuleBasedMatching"]:
        '''rule_based_matching block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#rule_based_matching CustomerprofilesDomain#rule_based_matching}
        '''
        result = self._values.get("rule_based_matching")
        return typing.cast(typing.Optional["CustomerprofilesDomainRuleBasedMatching"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#tags CustomerprofilesDomain#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#tags_all CustomerprofilesDomain#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatching",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "auto_merging": "autoMerging",
        "exporting_config": "exportingConfig",
        "job_schedule": "jobSchedule",
    },
)
class CustomerprofilesDomainMatching:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        auto_merging: typing.Optional[typing.Union["CustomerprofilesDomainMatchingAutoMerging", typing.Dict[builtins.str, typing.Any]]] = None,
        exporting_config: typing.Optional[typing.Union["CustomerprofilesDomainMatchingExportingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        job_schedule: typing.Optional[typing.Union["CustomerprofilesDomainMatchingJobSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#enabled CustomerprofilesDomain#enabled}.
        :param auto_merging: auto_merging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#auto_merging CustomerprofilesDomain#auto_merging}
        :param exporting_config: exporting_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#exporting_config CustomerprofilesDomain#exporting_config}
        :param job_schedule: job_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#job_schedule CustomerprofilesDomain#job_schedule}
        '''
        if isinstance(auto_merging, dict):
            auto_merging = CustomerprofilesDomainMatchingAutoMerging(**auto_merging)
        if isinstance(exporting_config, dict):
            exporting_config = CustomerprofilesDomainMatchingExportingConfig(**exporting_config)
        if isinstance(job_schedule, dict):
            job_schedule = CustomerprofilesDomainMatchingJobSchedule(**job_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4b3440b176ef78bfcddc8888a0c8e0fbba9dbd3d41243f697e3884c8d2f530)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument auto_merging", value=auto_merging, expected_type=type_hints["auto_merging"])
            check_type(argname="argument exporting_config", value=exporting_config, expected_type=type_hints["exporting_config"])
            check_type(argname="argument job_schedule", value=job_schedule, expected_type=type_hints["job_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if auto_merging is not None:
            self._values["auto_merging"] = auto_merging
        if exporting_config is not None:
            self._values["exporting_config"] = exporting_config
        if job_schedule is not None:
            self._values["job_schedule"] = job_schedule

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#enabled CustomerprofilesDomain#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def auto_merging(
        self,
    ) -> typing.Optional["CustomerprofilesDomainMatchingAutoMerging"]:
        '''auto_merging block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#auto_merging CustomerprofilesDomain#auto_merging}
        '''
        result = self._values.get("auto_merging")
        return typing.cast(typing.Optional["CustomerprofilesDomainMatchingAutoMerging"], result)

    @builtins.property
    def exporting_config(
        self,
    ) -> typing.Optional["CustomerprofilesDomainMatchingExportingConfig"]:
        '''exporting_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#exporting_config CustomerprofilesDomain#exporting_config}
        '''
        result = self._values.get("exporting_config")
        return typing.cast(typing.Optional["CustomerprofilesDomainMatchingExportingConfig"], result)

    @builtins.property
    def job_schedule(
        self,
    ) -> typing.Optional["CustomerprofilesDomainMatchingJobSchedule"]:
        '''job_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#job_schedule CustomerprofilesDomain#job_schedule}
        '''
        result = self._values.get("job_schedule")
        return typing.cast(typing.Optional["CustomerprofilesDomainMatchingJobSchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainMatching(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingAutoMerging",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "conflict_resolution": "conflictResolution",
        "consolidation": "consolidation",
        "min_allowed_confidence_score_for_merging": "minAllowedConfidenceScoreForMerging",
    },
)
class CustomerprofilesDomainMatchingAutoMerging:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        conflict_resolution: typing.Optional[typing.Union["CustomerprofilesDomainMatchingAutoMergingConflictResolution", typing.Dict[builtins.str, typing.Any]]] = None,
        consolidation: typing.Optional[typing.Union["CustomerprofilesDomainMatchingAutoMergingConsolidation", typing.Dict[builtins.str, typing.Any]]] = None,
        min_allowed_confidence_score_for_merging: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#enabled CustomerprofilesDomain#enabled}.
        :param conflict_resolution: conflict_resolution block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#conflict_resolution CustomerprofilesDomain#conflict_resolution}
        :param consolidation: consolidation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#consolidation CustomerprofilesDomain#consolidation}
        :param min_allowed_confidence_score_for_merging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#min_allowed_confidence_score_for_merging CustomerprofilesDomain#min_allowed_confidence_score_for_merging}.
        '''
        if isinstance(conflict_resolution, dict):
            conflict_resolution = CustomerprofilesDomainMatchingAutoMergingConflictResolution(**conflict_resolution)
        if isinstance(consolidation, dict):
            consolidation = CustomerprofilesDomainMatchingAutoMergingConsolidation(**consolidation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b93edf8609f4628a8d1a36c3b33a2a8bc95a87c17218452a5fc2e326caa3c1)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument conflict_resolution", value=conflict_resolution, expected_type=type_hints["conflict_resolution"])
            check_type(argname="argument consolidation", value=consolidation, expected_type=type_hints["consolidation"])
            check_type(argname="argument min_allowed_confidence_score_for_merging", value=min_allowed_confidence_score_for_merging, expected_type=type_hints["min_allowed_confidence_score_for_merging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if conflict_resolution is not None:
            self._values["conflict_resolution"] = conflict_resolution
        if consolidation is not None:
            self._values["consolidation"] = consolidation
        if min_allowed_confidence_score_for_merging is not None:
            self._values["min_allowed_confidence_score_for_merging"] = min_allowed_confidence_score_for_merging

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#enabled CustomerprofilesDomain#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def conflict_resolution(
        self,
    ) -> typing.Optional["CustomerprofilesDomainMatchingAutoMergingConflictResolution"]:
        '''conflict_resolution block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#conflict_resolution CustomerprofilesDomain#conflict_resolution}
        '''
        result = self._values.get("conflict_resolution")
        return typing.cast(typing.Optional["CustomerprofilesDomainMatchingAutoMergingConflictResolution"], result)

    @builtins.property
    def consolidation(
        self,
    ) -> typing.Optional["CustomerprofilesDomainMatchingAutoMergingConsolidation"]:
        '''consolidation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#consolidation CustomerprofilesDomain#consolidation}
        '''
        result = self._values.get("consolidation")
        return typing.cast(typing.Optional["CustomerprofilesDomainMatchingAutoMergingConsolidation"], result)

    @builtins.property
    def min_allowed_confidence_score_for_merging(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#min_allowed_confidence_score_for_merging CustomerprofilesDomain#min_allowed_confidence_score_for_merging}.'''
        result = self._values.get("min_allowed_confidence_score_for_merging")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainMatchingAutoMerging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingAutoMergingConflictResolution",
    jsii_struct_bases=[],
    name_mapping={
        "conflict_resolving_model": "conflictResolvingModel",
        "source_name": "sourceName",
    },
)
class CustomerprofilesDomainMatchingAutoMergingConflictResolution:
    def __init__(
        self,
        *,
        conflict_resolving_model: builtins.str,
        source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conflict_resolving_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#conflict_resolving_model CustomerprofilesDomain#conflict_resolving_model}.
        :param source_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#source_name CustomerprofilesDomain#source_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3242aa776d6761704e6d4f17a2e64e13b1e4331466905c6130e0cd452096cfd0)
            check_type(argname="argument conflict_resolving_model", value=conflict_resolving_model, expected_type=type_hints["conflict_resolving_model"])
            check_type(argname="argument source_name", value=source_name, expected_type=type_hints["source_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "conflict_resolving_model": conflict_resolving_model,
        }
        if source_name is not None:
            self._values["source_name"] = source_name

    @builtins.property
    def conflict_resolving_model(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#conflict_resolving_model CustomerprofilesDomain#conflict_resolving_model}.'''
        result = self._values.get("conflict_resolving_model")
        assert result is not None, "Required property 'conflict_resolving_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#source_name CustomerprofilesDomain#source_name}.'''
        result = self._values.get("source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainMatchingAutoMergingConflictResolution(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesDomainMatchingAutoMergingConflictResolutionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingAutoMergingConflictResolutionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__640b216ffa14d4b28aaaaf44c1d993d2491887f3cc6c4bef6cbcdbe98b61b130)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSourceName")
    def reset_source_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceName", []))

    @builtins.property
    @jsii.member(jsii_name="conflictResolvingModelInput")
    def conflict_resolving_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conflictResolvingModelInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceNameInput")
    def source_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="conflictResolvingModel")
    def conflict_resolving_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conflictResolvingModel"))

    @conflict_resolving_model.setter
    def conflict_resolving_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f24f7feda81d2c3b15586f4551d99ef9f2269c84ba64227f7fd3a113450f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conflictResolvingModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceName")
    def source_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceName"))

    @source_name.setter
    def source_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f75b215b2de76aaab097c4f5e464c8880906630141b5fb94b6a73d304dfd2f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CustomerprofilesDomainMatchingAutoMergingConflictResolution]:
        return typing.cast(typing.Optional[CustomerprofilesDomainMatchingAutoMergingConflictResolution], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesDomainMatchingAutoMergingConflictResolution],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98609e9b3b67982629e4c3d9d2e63fd66c68e8fdab6ca53b759bd69a665cc46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingAutoMergingConsolidation",
    jsii_struct_bases=[],
    name_mapping={"matching_attributes_list": "matchingAttributesList"},
)
class CustomerprofilesDomainMatchingAutoMergingConsolidation:
    def __init__(
        self,
        *,
        matching_attributes_list: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Sequence[builtins.str]]],
    ) -> None:
        '''
        :param matching_attributes_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#matching_attributes_list CustomerprofilesDomain#matching_attributes_list}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4a1719942dd0af2e777d67b09c41858cc34ea2dde8b928a4e4dcb1aeceebd2)
            check_type(argname="argument matching_attributes_list", value=matching_attributes_list, expected_type=type_hints["matching_attributes_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "matching_attributes_list": matching_attributes_list,
        }

    @builtins.property
    def matching_attributes_list(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[builtins.str]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#matching_attributes_list CustomerprofilesDomain#matching_attributes_list}.'''
        result = self._values.get("matching_attributes_list")
        assert result is not None, "Required property 'matching_attributes_list' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainMatchingAutoMergingConsolidation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesDomainMatchingAutoMergingConsolidationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingAutoMergingConsolidationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a789c8946fedad8cd385bc9f776dc14511ecc1efba821202f145041846ca4ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="matchingAttributesListInput")
    def matching_attributes_list_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[builtins.str]]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[builtins.str]]]], jsii.get(self, "matchingAttributesListInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingAttributesList")
    def matching_attributes_list(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[builtins.str]]]:
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[builtins.str]]], jsii.get(self, "matchingAttributesList"))

    @matching_attributes_list.setter
    def matching_attributes_list(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c709347afebb48c691802d6f9a43bbb45441e6fc1316f0dc88fa732134c22441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchingAttributesList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CustomerprofilesDomainMatchingAutoMergingConsolidation]:
        return typing.cast(typing.Optional[CustomerprofilesDomainMatchingAutoMergingConsolidation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesDomainMatchingAutoMergingConsolidation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e55895fc107b63924c965094e9e63ceb9b1b1a9e03cd9f09c0e9b2445b54c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CustomerprofilesDomainMatchingAutoMergingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingAutoMergingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49759ad4f5393e58ca50750d897f0b7964c06d00fbd4e3fb9fbae060cc4463e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConflictResolution")
    def put_conflict_resolution(
        self,
        *,
        conflict_resolving_model: builtins.str,
        source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conflict_resolving_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#conflict_resolving_model CustomerprofilesDomain#conflict_resolving_model}.
        :param source_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#source_name CustomerprofilesDomain#source_name}.
        '''
        value = CustomerprofilesDomainMatchingAutoMergingConflictResolution(
            conflict_resolving_model=conflict_resolving_model, source_name=source_name
        )

        return typing.cast(None, jsii.invoke(self, "putConflictResolution", [value]))

    @jsii.member(jsii_name="putConsolidation")
    def put_consolidation(
        self,
        *,
        matching_attributes_list: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Sequence[builtins.str]]],
    ) -> None:
        '''
        :param matching_attributes_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#matching_attributes_list CustomerprofilesDomain#matching_attributes_list}.
        '''
        value = CustomerprofilesDomainMatchingAutoMergingConsolidation(
            matching_attributes_list=matching_attributes_list
        )

        return typing.cast(None, jsii.invoke(self, "putConsolidation", [value]))

    @jsii.member(jsii_name="resetConflictResolution")
    def reset_conflict_resolution(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConflictResolution", []))

    @jsii.member(jsii_name="resetConsolidation")
    def reset_consolidation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsolidation", []))

    @jsii.member(jsii_name="resetMinAllowedConfidenceScoreForMerging")
    def reset_min_allowed_confidence_score_for_merging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinAllowedConfidenceScoreForMerging", []))

    @builtins.property
    @jsii.member(jsii_name="conflictResolution")
    def conflict_resolution(
        self,
    ) -> CustomerprofilesDomainMatchingAutoMergingConflictResolutionOutputReference:
        return typing.cast(CustomerprofilesDomainMatchingAutoMergingConflictResolutionOutputReference, jsii.get(self, "conflictResolution"))

    @builtins.property
    @jsii.member(jsii_name="consolidation")
    def consolidation(
        self,
    ) -> CustomerprofilesDomainMatchingAutoMergingConsolidationOutputReference:
        return typing.cast(CustomerprofilesDomainMatchingAutoMergingConsolidationOutputReference, jsii.get(self, "consolidation"))

    @builtins.property
    @jsii.member(jsii_name="conflictResolutionInput")
    def conflict_resolution_input(
        self,
    ) -> typing.Optional[CustomerprofilesDomainMatchingAutoMergingConflictResolution]:
        return typing.cast(typing.Optional[CustomerprofilesDomainMatchingAutoMergingConflictResolution], jsii.get(self, "conflictResolutionInput"))

    @builtins.property
    @jsii.member(jsii_name="consolidationInput")
    def consolidation_input(
        self,
    ) -> typing.Optional[CustomerprofilesDomainMatchingAutoMergingConsolidation]:
        return typing.cast(typing.Optional[CustomerprofilesDomainMatchingAutoMergingConsolidation], jsii.get(self, "consolidationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="minAllowedConfidenceScoreForMergingInput")
    def min_allowed_confidence_score_for_merging_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minAllowedConfidenceScoreForMergingInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6c440f05324ee1caeb324c2fdd56c1551399c9adc000e989e871e315cf4190ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minAllowedConfidenceScoreForMerging")
    def min_allowed_confidence_score_for_merging(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minAllowedConfidenceScoreForMerging"))

    @min_allowed_confidence_score_for_merging.setter
    def min_allowed_confidence_score_for_merging(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4d475d24767c40dc530f359a40b78a8f310e34c14c8f66bb22c9a8636ecce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minAllowedConfidenceScoreForMerging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CustomerprofilesDomainMatchingAutoMerging]:
        return typing.cast(typing.Optional[CustomerprofilesDomainMatchingAutoMerging], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesDomainMatchingAutoMerging],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648a3315782bfd81a93fb95c0b0e433758a3669f5083c97e87ed01a2625d0117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingExportingConfig",
    jsii_struct_bases=[],
    name_mapping={"s3_exporting": "s3Exporting"},
)
class CustomerprofilesDomainMatchingExportingConfig:
    def __init__(
        self,
        *,
        s3_exporting: typing.Optional[typing.Union["CustomerprofilesDomainMatchingExportingConfigS3Exporting", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3_exporting: s3_exporting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_exporting CustomerprofilesDomain#s3_exporting}
        '''
        if isinstance(s3_exporting, dict):
            s3_exporting = CustomerprofilesDomainMatchingExportingConfigS3Exporting(**s3_exporting)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f38024e27b2ae9def4c331f002ce9b300fc4298939094eb3206825ef6e252c3)
            check_type(argname="argument s3_exporting", value=s3_exporting, expected_type=type_hints["s3_exporting"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_exporting is not None:
            self._values["s3_exporting"] = s3_exporting

    @builtins.property
    def s3_exporting(
        self,
    ) -> typing.Optional["CustomerprofilesDomainMatchingExportingConfigS3Exporting"]:
        '''s3_exporting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_exporting CustomerprofilesDomain#s3_exporting}
        '''
        result = self._values.get("s3_exporting")
        return typing.cast(typing.Optional["CustomerprofilesDomainMatchingExportingConfigS3Exporting"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainMatchingExportingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesDomainMatchingExportingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingExportingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__414c4f9f6f7eb20d6c79ff2f71cccee63affc1dda1a7e8dc42d644f7c37d208b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3Exporting")
    def put_s3_exporting(
        self,
        *,
        s3_bucket_name: builtins.str,
        s3_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_bucket_name CustomerprofilesDomain#s3_bucket_name}.
        :param s3_key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_key_name CustomerprofilesDomain#s3_key_name}.
        '''
        value = CustomerprofilesDomainMatchingExportingConfigS3Exporting(
            s3_bucket_name=s3_bucket_name, s3_key_name=s3_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putS3Exporting", [value]))

    @jsii.member(jsii_name="resetS3Exporting")
    def reset_s3_exporting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Exporting", []))

    @builtins.property
    @jsii.member(jsii_name="s3Exporting")
    def s3_exporting(
        self,
    ) -> "CustomerprofilesDomainMatchingExportingConfigS3ExportingOutputReference":
        return typing.cast("CustomerprofilesDomainMatchingExportingConfigS3ExportingOutputReference", jsii.get(self, "s3Exporting"))

    @builtins.property
    @jsii.member(jsii_name="s3ExportingInput")
    def s3_exporting_input(
        self,
    ) -> typing.Optional["CustomerprofilesDomainMatchingExportingConfigS3Exporting"]:
        return typing.cast(typing.Optional["CustomerprofilesDomainMatchingExportingConfigS3Exporting"], jsii.get(self, "s3ExportingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CustomerprofilesDomainMatchingExportingConfig]:
        return typing.cast(typing.Optional[CustomerprofilesDomainMatchingExportingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesDomainMatchingExportingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e263dc0a8c247481aa34d33b833137b1248a703c351e8c5b6963930a4afcc058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingExportingConfigS3Exporting",
    jsii_struct_bases=[],
    name_mapping={"s3_bucket_name": "s3BucketName", "s3_key_name": "s3KeyName"},
)
class CustomerprofilesDomainMatchingExportingConfigS3Exporting:
    def __init__(
        self,
        *,
        s3_bucket_name: builtins.str,
        s3_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_bucket_name CustomerprofilesDomain#s3_bucket_name}.
        :param s3_key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_key_name CustomerprofilesDomain#s3_key_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc287237c9f3996a77c264c277575337d947320d1f601bb5f20c0c1ca82d2fb2)
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            check_type(argname="argument s3_key_name", value=s3_key_name, expected_type=type_hints["s3_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_bucket_name": s3_bucket_name,
        }
        if s3_key_name is not None:
            self._values["s3_key_name"] = s3_key_name

    @builtins.property
    def s3_bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_bucket_name CustomerprofilesDomain#s3_bucket_name}.'''
        result = self._values.get("s3_bucket_name")
        assert result is not None, "Required property 's3_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_key_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_key_name CustomerprofilesDomain#s3_key_name}.'''
        result = self._values.get("s3_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainMatchingExportingConfigS3Exporting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesDomainMatchingExportingConfigS3ExportingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingExportingConfigS3ExportingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4b9e85d23c53474e4d1dd464c0aa7a11a78ad32b7a3c83bcec7f3da8918854f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3KeyName")
    def reset_s3_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3KeyName", []))

    @builtins.property
    @jsii.member(jsii_name="s3BucketNameInput")
    def s3_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="s3KeyNameInput")
    def s3_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3KeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketName"))

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2e9afebe649299b7ef8fed37b80ab4b1c2719a66f3fc96db8cb5f92b81047a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3KeyName")
    def s3_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3KeyName"))

    @s3_key_name.setter
    def s3_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b943b14522e82a900e8e84355c0036758bc44680c95128ce4fae562f969ce5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3KeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CustomerprofilesDomainMatchingExportingConfigS3Exporting]:
        return typing.cast(typing.Optional[CustomerprofilesDomainMatchingExportingConfigS3Exporting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesDomainMatchingExportingConfigS3Exporting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b40d4768c3563b51fd5bdcec8d4c44242156146db8a27e38c65fde6ff2eb09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingJobSchedule",
    jsii_struct_bases=[],
    name_mapping={"day_of_the_week": "dayOfTheWeek", "time": "time"},
)
class CustomerprofilesDomainMatchingJobSchedule:
    def __init__(self, *, day_of_the_week: builtins.str, time: builtins.str) -> None:
        '''
        :param day_of_the_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#day_of_the_week CustomerprofilesDomain#day_of_the_week}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#time CustomerprofilesDomain#time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__764e24acc585cb43889fdc73075c5067b440f9613cc27d88ecd55bce8928db3e)
            check_type(argname="argument day_of_the_week", value=day_of_the_week, expected_type=type_hints["day_of_the_week"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_the_week": day_of_the_week,
            "time": time,
        }

    @builtins.property
    def day_of_the_week(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#day_of_the_week CustomerprofilesDomain#day_of_the_week}.'''
        result = self._values.get("day_of_the_week")
        assert result is not None, "Required property 'day_of_the_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#time CustomerprofilesDomain#time}.'''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainMatchingJobSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesDomainMatchingJobScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingJobScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__715d88b7e008f45f7f5b6f59a69fc05e10a184933d3f3dfeba4909b2c801eb1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayOfTheWeekInput")
    def day_of_the_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfTheWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfTheWeek")
    def day_of_the_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfTheWeek"))

    @day_of_the_week.setter
    def day_of_the_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83d36e85ca447ce364a176da970eab90f0ad0ed50b026a28adc3829f3f9b433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfTheWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "time"))

    @time.setter
    def time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6516a6721a13cfac4f35f017a06e763578abfe53da38b2f446aff65a4870b2c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CustomerprofilesDomainMatchingJobSchedule]:
        return typing.cast(typing.Optional[CustomerprofilesDomainMatchingJobSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesDomainMatchingJobSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489dda63aeced89df15c64bf766d8a11d690fc2f9b5ab3cdd9df8dbdc083235c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CustomerprofilesDomainMatchingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainMatchingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58fc3b5dead2d856fe006e3a75e83686bcac6b1acfd708680c2dde4d642e37ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoMerging")
    def put_auto_merging(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        conflict_resolution: typing.Optional[typing.Union[CustomerprofilesDomainMatchingAutoMergingConflictResolution, typing.Dict[builtins.str, typing.Any]]] = None,
        consolidation: typing.Optional[typing.Union[CustomerprofilesDomainMatchingAutoMergingConsolidation, typing.Dict[builtins.str, typing.Any]]] = None,
        min_allowed_confidence_score_for_merging: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#enabled CustomerprofilesDomain#enabled}.
        :param conflict_resolution: conflict_resolution block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#conflict_resolution CustomerprofilesDomain#conflict_resolution}
        :param consolidation: consolidation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#consolidation CustomerprofilesDomain#consolidation}
        :param min_allowed_confidence_score_for_merging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#min_allowed_confidence_score_for_merging CustomerprofilesDomain#min_allowed_confidence_score_for_merging}.
        '''
        value = CustomerprofilesDomainMatchingAutoMerging(
            enabled=enabled,
            conflict_resolution=conflict_resolution,
            consolidation=consolidation,
            min_allowed_confidence_score_for_merging=min_allowed_confidence_score_for_merging,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoMerging", [value]))

    @jsii.member(jsii_name="putExportingConfig")
    def put_exporting_config(
        self,
        *,
        s3_exporting: typing.Optional[typing.Union[CustomerprofilesDomainMatchingExportingConfigS3Exporting, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3_exporting: s3_exporting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_exporting CustomerprofilesDomain#s3_exporting}
        '''
        value = CustomerprofilesDomainMatchingExportingConfig(
            s3_exporting=s3_exporting
        )

        return typing.cast(None, jsii.invoke(self, "putExportingConfig", [value]))

    @jsii.member(jsii_name="putJobSchedule")
    def put_job_schedule(
        self,
        *,
        day_of_the_week: builtins.str,
        time: builtins.str,
    ) -> None:
        '''
        :param day_of_the_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#day_of_the_week CustomerprofilesDomain#day_of_the_week}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#time CustomerprofilesDomain#time}.
        '''
        value = CustomerprofilesDomainMatchingJobSchedule(
            day_of_the_week=day_of_the_week, time=time
        )

        return typing.cast(None, jsii.invoke(self, "putJobSchedule", [value]))

    @jsii.member(jsii_name="resetAutoMerging")
    def reset_auto_merging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoMerging", []))

    @jsii.member(jsii_name="resetExportingConfig")
    def reset_exporting_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportingConfig", []))

    @jsii.member(jsii_name="resetJobSchedule")
    def reset_job_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobSchedule", []))

    @builtins.property
    @jsii.member(jsii_name="autoMerging")
    def auto_merging(self) -> CustomerprofilesDomainMatchingAutoMergingOutputReference:
        return typing.cast(CustomerprofilesDomainMatchingAutoMergingOutputReference, jsii.get(self, "autoMerging"))

    @builtins.property
    @jsii.member(jsii_name="exportingConfig")
    def exporting_config(
        self,
    ) -> CustomerprofilesDomainMatchingExportingConfigOutputReference:
        return typing.cast(CustomerprofilesDomainMatchingExportingConfigOutputReference, jsii.get(self, "exportingConfig"))

    @builtins.property
    @jsii.member(jsii_name="jobSchedule")
    def job_schedule(self) -> CustomerprofilesDomainMatchingJobScheduleOutputReference:
        return typing.cast(CustomerprofilesDomainMatchingJobScheduleOutputReference, jsii.get(self, "jobSchedule"))

    @builtins.property
    @jsii.member(jsii_name="autoMergingInput")
    def auto_merging_input(
        self,
    ) -> typing.Optional[CustomerprofilesDomainMatchingAutoMerging]:
        return typing.cast(typing.Optional[CustomerprofilesDomainMatchingAutoMerging], jsii.get(self, "autoMergingInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="exportingConfigInput")
    def exporting_config_input(
        self,
    ) -> typing.Optional[CustomerprofilesDomainMatchingExportingConfig]:
        return typing.cast(typing.Optional[CustomerprofilesDomainMatchingExportingConfig], jsii.get(self, "exportingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="jobScheduleInput")
    def job_schedule_input(
        self,
    ) -> typing.Optional[CustomerprofilesDomainMatchingJobSchedule]:
        return typing.cast(typing.Optional[CustomerprofilesDomainMatchingJobSchedule], jsii.get(self, "jobScheduleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__216c38b8c2ca4ddeb3bab15fddc911abcecb6535c80ffb3863b340fe22dc7219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CustomerprofilesDomainMatching]:
        return typing.cast(typing.Optional[CustomerprofilesDomainMatching], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesDomainMatching],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49431d568f36e7f7b78827c58f72b78de6a47d414537420b9f154829ab58322f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatching",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "attribute_types_selector": "attributeTypesSelector",
        "conflict_resolution": "conflictResolution",
        "exporting_config": "exportingConfig",
        "matching_rules": "matchingRules",
        "max_allowed_rule_level_for_matching": "maxAllowedRuleLevelForMatching",
        "max_allowed_rule_level_for_merging": "maxAllowedRuleLevelForMerging",
        "status": "status",
    },
)
class CustomerprofilesDomainRuleBasedMatching:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        attribute_types_selector: typing.Optional[typing.Union["CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        conflict_resolution: typing.Optional[typing.Union["CustomerprofilesDomainRuleBasedMatchingConflictResolution", typing.Dict[builtins.str, typing.Any]]] = None,
        exporting_config: typing.Optional[typing.Union["CustomerprofilesDomainRuleBasedMatchingExportingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        matching_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CustomerprofilesDomainRuleBasedMatchingMatchingRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_allowed_rule_level_for_matching: typing.Optional[jsii.Number] = None,
        max_allowed_rule_level_for_merging: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#enabled CustomerprofilesDomain#enabled}.
        :param attribute_types_selector: attribute_types_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#attribute_types_selector CustomerprofilesDomain#attribute_types_selector}
        :param conflict_resolution: conflict_resolution block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#conflict_resolution CustomerprofilesDomain#conflict_resolution}
        :param exporting_config: exporting_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#exporting_config CustomerprofilesDomain#exporting_config}
        :param matching_rules: matching_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#matching_rules CustomerprofilesDomain#matching_rules}
        :param max_allowed_rule_level_for_matching: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#max_allowed_rule_level_for_matching CustomerprofilesDomain#max_allowed_rule_level_for_matching}.
        :param max_allowed_rule_level_for_merging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#max_allowed_rule_level_for_merging CustomerprofilesDomain#max_allowed_rule_level_for_merging}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#status CustomerprofilesDomain#status}.
        '''
        if isinstance(attribute_types_selector, dict):
            attribute_types_selector = CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector(**attribute_types_selector)
        if isinstance(conflict_resolution, dict):
            conflict_resolution = CustomerprofilesDomainRuleBasedMatchingConflictResolution(**conflict_resolution)
        if isinstance(exporting_config, dict):
            exporting_config = CustomerprofilesDomainRuleBasedMatchingExportingConfig(**exporting_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86062e96fbda1bdf9e8564d49781c32204023f2b59c4dd82784d12408d1348c7)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument attribute_types_selector", value=attribute_types_selector, expected_type=type_hints["attribute_types_selector"])
            check_type(argname="argument conflict_resolution", value=conflict_resolution, expected_type=type_hints["conflict_resolution"])
            check_type(argname="argument exporting_config", value=exporting_config, expected_type=type_hints["exporting_config"])
            check_type(argname="argument matching_rules", value=matching_rules, expected_type=type_hints["matching_rules"])
            check_type(argname="argument max_allowed_rule_level_for_matching", value=max_allowed_rule_level_for_matching, expected_type=type_hints["max_allowed_rule_level_for_matching"])
            check_type(argname="argument max_allowed_rule_level_for_merging", value=max_allowed_rule_level_for_merging, expected_type=type_hints["max_allowed_rule_level_for_merging"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if attribute_types_selector is not None:
            self._values["attribute_types_selector"] = attribute_types_selector
        if conflict_resolution is not None:
            self._values["conflict_resolution"] = conflict_resolution
        if exporting_config is not None:
            self._values["exporting_config"] = exporting_config
        if matching_rules is not None:
            self._values["matching_rules"] = matching_rules
        if max_allowed_rule_level_for_matching is not None:
            self._values["max_allowed_rule_level_for_matching"] = max_allowed_rule_level_for_matching
        if max_allowed_rule_level_for_merging is not None:
            self._values["max_allowed_rule_level_for_merging"] = max_allowed_rule_level_for_merging
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#enabled CustomerprofilesDomain#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def attribute_types_selector(
        self,
    ) -> typing.Optional["CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector"]:
        '''attribute_types_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#attribute_types_selector CustomerprofilesDomain#attribute_types_selector}
        '''
        result = self._values.get("attribute_types_selector")
        return typing.cast(typing.Optional["CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector"], result)

    @builtins.property
    def conflict_resolution(
        self,
    ) -> typing.Optional["CustomerprofilesDomainRuleBasedMatchingConflictResolution"]:
        '''conflict_resolution block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#conflict_resolution CustomerprofilesDomain#conflict_resolution}
        '''
        result = self._values.get("conflict_resolution")
        return typing.cast(typing.Optional["CustomerprofilesDomainRuleBasedMatchingConflictResolution"], result)

    @builtins.property
    def exporting_config(
        self,
    ) -> typing.Optional["CustomerprofilesDomainRuleBasedMatchingExportingConfig"]:
        '''exporting_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#exporting_config CustomerprofilesDomain#exporting_config}
        '''
        result = self._values.get("exporting_config")
        return typing.cast(typing.Optional["CustomerprofilesDomainRuleBasedMatchingExportingConfig"], result)

    @builtins.property
    def matching_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomerprofilesDomainRuleBasedMatchingMatchingRules"]]]:
        '''matching_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#matching_rules CustomerprofilesDomain#matching_rules}
        '''
        result = self._values.get("matching_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CustomerprofilesDomainRuleBasedMatchingMatchingRules"]]], result)

    @builtins.property
    def max_allowed_rule_level_for_matching(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#max_allowed_rule_level_for_matching CustomerprofilesDomain#max_allowed_rule_level_for_matching}.'''
        result = self._values.get("max_allowed_rule_level_for_matching")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_allowed_rule_level_for_merging(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#max_allowed_rule_level_for_merging CustomerprofilesDomain#max_allowed_rule_level_for_merging}.'''
        result = self._values.get("max_allowed_rule_level_for_merging")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#status CustomerprofilesDomain#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainRuleBasedMatching(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_matching_model": "attributeMatchingModel",
        "address": "address",
        "email_address": "emailAddress",
        "phone_number": "phoneNumber",
    },
)
class CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector:
    def __init__(
        self,
        *,
        attribute_matching_model: builtins.str,
        address: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        phone_number: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param attribute_matching_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#attribute_matching_model CustomerprofilesDomain#attribute_matching_model}.
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#address CustomerprofilesDomain#address}.
        :param email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#email_address CustomerprofilesDomain#email_address}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#phone_number CustomerprofilesDomain#phone_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5133db52b8df22c171606b572b5a72f891382d4207c460f4d0510ded924186ac)
            check_type(argname="argument attribute_matching_model", value=attribute_matching_model, expected_type=type_hints["attribute_matching_model"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attribute_matching_model": attribute_matching_model,
        }
        if address is not None:
            self._values["address"] = address
        if email_address is not None:
            self._values["email_address"] = email_address
        if phone_number is not None:
            self._values["phone_number"] = phone_number

    @builtins.property
    def attribute_matching_model(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#attribute_matching_model CustomerprofilesDomain#attribute_matching_model}.'''
        result = self._values.get("attribute_matching_model")
        assert result is not None, "Required property 'attribute_matching_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#address CustomerprofilesDomain#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email_address(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#email_address CustomerprofilesDomain#email_address}.'''
        result = self._values.get("email_address")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def phone_number(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#phone_number CustomerprofilesDomain#phone_number}.'''
        result = self._values.get("phone_number")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31e83005765c56087bc0cd01fef1159368df4d15c880821925dfffd2060c585d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetEmailAddress")
    def reset_email_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAddress", []))

    @jsii.member(jsii_name="resetPhoneNumber")
    def reset_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoneNumber", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="attributeMatchingModelInput")
    def attribute_matching_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeMatchingModelInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddressInput")
    def email_address_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "address"))

    @address.setter
    def address(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfee1371ef4fc682740ddae334770f0091325405402aa2ad8f2c0a695379365a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="attributeMatchingModel")
    def attribute_matching_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attributeMatchingModel"))

    @attribute_matching_model.setter
    def attribute_matching_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8349552cdcf1cf8122613724c2913396891fb0631f9a3991af6ae937f1ce89b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributeMatchingModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailAddress")
    def email_address(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailAddress"))

    @email_address.setter
    def email_address(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbc8622dd7a8256b549cbe2fdb78df5a4b9b379798f1b11961797b695bcc705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552cdb6be16d1732c5f1cc36b8179a00d0f4840edd41ddedf4125d9b534c478c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector]:
        return typing.cast(typing.Optional[CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec65d41c3862b6cef368a3fde0d92c49e5075d1a05ffedb14321492ac818f770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatchingConflictResolution",
    jsii_struct_bases=[],
    name_mapping={
        "conflict_resolving_model": "conflictResolvingModel",
        "source_name": "sourceName",
    },
)
class CustomerprofilesDomainRuleBasedMatchingConflictResolution:
    def __init__(
        self,
        *,
        conflict_resolving_model: builtins.str,
        source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conflict_resolving_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#conflict_resolving_model CustomerprofilesDomain#conflict_resolving_model}.
        :param source_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#source_name CustomerprofilesDomain#source_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8472b6b4791b9420569e3a8c9a32ea66bd278f39e6b2519971fefa631bdecb5)
            check_type(argname="argument conflict_resolving_model", value=conflict_resolving_model, expected_type=type_hints["conflict_resolving_model"])
            check_type(argname="argument source_name", value=source_name, expected_type=type_hints["source_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "conflict_resolving_model": conflict_resolving_model,
        }
        if source_name is not None:
            self._values["source_name"] = source_name

    @builtins.property
    def conflict_resolving_model(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#conflict_resolving_model CustomerprofilesDomain#conflict_resolving_model}.'''
        result = self._values.get("conflict_resolving_model")
        assert result is not None, "Required property 'conflict_resolving_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#source_name CustomerprofilesDomain#source_name}.'''
        result = self._values.get("source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainRuleBasedMatchingConflictResolution(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesDomainRuleBasedMatchingConflictResolutionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatchingConflictResolutionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__497b34e66560cbc88d16d013935c3911580892ffa69c1ddb78a95dcecace1c9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSourceName")
    def reset_source_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceName", []))

    @builtins.property
    @jsii.member(jsii_name="conflictResolvingModelInput")
    def conflict_resolving_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conflictResolvingModelInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceNameInput")
    def source_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="conflictResolvingModel")
    def conflict_resolving_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conflictResolvingModel"))

    @conflict_resolving_model.setter
    def conflict_resolving_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c1b5bcfe6618dd6855fb3642d4262692d3d98c7bb03fcf355742768b5fec22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conflictResolvingModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceName")
    def source_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceName"))

    @source_name.setter
    def source_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41b0e36fe3a7deef7f6789512b37934202dd8e2c778efaca03931efab8e54b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CustomerprofilesDomainRuleBasedMatchingConflictResolution]:
        return typing.cast(typing.Optional[CustomerprofilesDomainRuleBasedMatchingConflictResolution], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesDomainRuleBasedMatchingConflictResolution],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7970d1b3ae1bc09da1048927c188dfbbebc56fedcc43ca44eeb6b875c9d869f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatchingExportingConfig",
    jsii_struct_bases=[],
    name_mapping={"s3_exporting": "s3Exporting"},
)
class CustomerprofilesDomainRuleBasedMatchingExportingConfig:
    def __init__(
        self,
        *,
        s3_exporting: typing.Optional[typing.Union["CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3_exporting: s3_exporting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_exporting CustomerprofilesDomain#s3_exporting}
        '''
        if isinstance(s3_exporting, dict):
            s3_exporting = CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting(**s3_exporting)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec026e99453d35ba4db980b4a90857f43e4d97b2d4f5842b9aff5655f0e8ffb7)
            check_type(argname="argument s3_exporting", value=s3_exporting, expected_type=type_hints["s3_exporting"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_exporting is not None:
            self._values["s3_exporting"] = s3_exporting

    @builtins.property
    def s3_exporting(
        self,
    ) -> typing.Optional["CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting"]:
        '''s3_exporting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_exporting CustomerprofilesDomain#s3_exporting}
        '''
        result = self._values.get("s3_exporting")
        return typing.cast(typing.Optional["CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainRuleBasedMatchingExportingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesDomainRuleBasedMatchingExportingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatchingExportingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a869681a2680ea9b7cfd307d951440d9791610f54a4179c67d196e32f036069)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3Exporting")
    def put_s3_exporting(
        self,
        *,
        s3_bucket_name: builtins.str,
        s3_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_bucket_name CustomerprofilesDomain#s3_bucket_name}.
        :param s3_key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_key_name CustomerprofilesDomain#s3_key_name}.
        '''
        value = CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting(
            s3_bucket_name=s3_bucket_name, s3_key_name=s3_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putS3Exporting", [value]))

    @jsii.member(jsii_name="resetS3Exporting")
    def reset_s3_exporting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Exporting", []))

    @builtins.property
    @jsii.member(jsii_name="s3Exporting")
    def s3_exporting(
        self,
    ) -> "CustomerprofilesDomainRuleBasedMatchingExportingConfigS3ExportingOutputReference":
        return typing.cast("CustomerprofilesDomainRuleBasedMatchingExportingConfigS3ExportingOutputReference", jsii.get(self, "s3Exporting"))

    @builtins.property
    @jsii.member(jsii_name="s3ExportingInput")
    def s3_exporting_input(
        self,
    ) -> typing.Optional["CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting"]:
        return typing.cast(typing.Optional["CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting"], jsii.get(self, "s3ExportingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CustomerprofilesDomainRuleBasedMatchingExportingConfig]:
        return typing.cast(typing.Optional[CustomerprofilesDomainRuleBasedMatchingExportingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesDomainRuleBasedMatchingExportingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9794fb95b8f5408047cff0bba35a0589b5b9167e02e0e4bc33aa068a31ef18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting",
    jsii_struct_bases=[],
    name_mapping={"s3_bucket_name": "s3BucketName", "s3_key_name": "s3KeyName"},
)
class CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting:
    def __init__(
        self,
        *,
        s3_bucket_name: builtins.str,
        s3_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_bucket_name CustomerprofilesDomain#s3_bucket_name}.
        :param s3_key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_key_name CustomerprofilesDomain#s3_key_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bba76a1ce680a48b1eeb637181a6441e268c007207652e86018bb2ae7282775)
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            check_type(argname="argument s3_key_name", value=s3_key_name, expected_type=type_hints["s3_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_bucket_name": s3_bucket_name,
        }
        if s3_key_name is not None:
            self._values["s3_key_name"] = s3_key_name

    @builtins.property
    def s3_bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_bucket_name CustomerprofilesDomain#s3_bucket_name}.'''
        result = self._values.get("s3_bucket_name")
        assert result is not None, "Required property 's3_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_key_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_key_name CustomerprofilesDomain#s3_key_name}.'''
        result = self._values.get("s3_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesDomainRuleBasedMatchingExportingConfigS3ExportingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatchingExportingConfigS3ExportingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c7e0247204c962cd2ca33a4845beb570279c78a9e60805fae9754d26029fb46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3KeyName")
    def reset_s3_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3KeyName", []))

    @builtins.property
    @jsii.member(jsii_name="s3BucketNameInput")
    def s3_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="s3KeyNameInput")
    def s3_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3KeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketName"))

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59088aa5dcce068ea3e2cea4ded5271b2eab50de6badb65a3fcae857e0285c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3KeyName")
    def s3_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3KeyName"))

    @s3_key_name.setter
    def s3_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62cb82789493b328b6cf1ea6bc42cb57222f7451edc35c0186cbf98e52c9dade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3KeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting]:
        return typing.cast(typing.Optional[CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9537f035795926306db92c271cde65a018c003156a5898dd9d6ae8102b42f4d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatchingMatchingRules",
    jsii_struct_bases=[],
    name_mapping={"rule": "rule"},
)
class CustomerprofilesDomainRuleBasedMatchingMatchingRules:
    def __init__(self, *, rule: typing.Sequence[builtins.str]) -> None:
        '''
        :param rule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#rule CustomerprofilesDomain#rule}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a8b2e4f55b70cc8120dcce4ca3fbf9d9a10b9d9b372ed627a1937d231fe276)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule": rule,
        }

    @builtins.property
    def rule(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#rule CustomerprofilesDomain#rule}.'''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerprofilesDomainRuleBasedMatchingMatchingRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomerprofilesDomainRuleBasedMatchingMatchingRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatchingMatchingRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__626e3dd7d19183086b55cf6816d88c76da0f32815edba4235dee92f190b7d046)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CustomerprofilesDomainRuleBasedMatchingMatchingRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e52fab5eee873b5611a6c08cd3efc3ae0a9b171c3204c3d3d63f6b557c2a7a80)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CustomerprofilesDomainRuleBasedMatchingMatchingRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd6a81f4007ca7c01d57e9bd93da148fddb3b631903f22c0d2dbc268cb3db99d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8602d58803598b8659c967b462cd4d8650a323a69783b8bcc005d560d8f9754)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa1f0542c4f42d566b88a5d8e587e9c9cda94b9a162599aef52abd19d8f549c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomerprofilesDomainRuleBasedMatchingMatchingRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomerprofilesDomainRuleBasedMatchingMatchingRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomerprofilesDomainRuleBasedMatchingMatchingRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2109975351f9cbd9598e150590a8e17ccc1dca7d419fb3f8cf5b7db6945bde8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CustomerprofilesDomainRuleBasedMatchingMatchingRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatchingMatchingRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63285d939190dc66714c8f8b0ca646bbdbb94633f80ddc30abc5b6e9198884ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rule"))

    @rule.setter
    def rule(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4186ae2e6ec59f938de76654771fafd26740e6604b1948423a755d3994edfb6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomerprofilesDomainRuleBasedMatchingMatchingRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomerprofilesDomainRuleBasedMatchingMatchingRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomerprofilesDomainRuleBasedMatchingMatchingRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c460188c773f06c0c2324aa0492fe4176e35c8dbdf74c1c68b215c4e97834c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CustomerprofilesDomainRuleBasedMatchingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.customerprofilesDomain.CustomerprofilesDomainRuleBasedMatchingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fb715fcc94188ce5b7d1ceb475b4aed614c460cdda481845496d5abcf8f0935)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAttributeTypesSelector")
    def put_attribute_types_selector(
        self,
        *,
        attribute_matching_model: builtins.str,
        address: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        phone_number: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param attribute_matching_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#attribute_matching_model CustomerprofilesDomain#attribute_matching_model}.
        :param address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#address CustomerprofilesDomain#address}.
        :param email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#email_address CustomerprofilesDomain#email_address}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#phone_number CustomerprofilesDomain#phone_number}.
        '''
        value = CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector(
            attribute_matching_model=attribute_matching_model,
            address=address,
            email_address=email_address,
            phone_number=phone_number,
        )

        return typing.cast(None, jsii.invoke(self, "putAttributeTypesSelector", [value]))

    @jsii.member(jsii_name="putConflictResolution")
    def put_conflict_resolution(
        self,
        *,
        conflict_resolving_model: builtins.str,
        source_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conflict_resolving_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#conflict_resolving_model CustomerprofilesDomain#conflict_resolving_model}.
        :param source_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#source_name CustomerprofilesDomain#source_name}.
        '''
        value = CustomerprofilesDomainRuleBasedMatchingConflictResolution(
            conflict_resolving_model=conflict_resolving_model, source_name=source_name
        )

        return typing.cast(None, jsii.invoke(self, "putConflictResolution", [value]))

    @jsii.member(jsii_name="putExportingConfig")
    def put_exporting_config(
        self,
        *,
        s3_exporting: typing.Optional[typing.Union[CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3_exporting: s3_exporting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/customerprofiles_domain#s3_exporting CustomerprofilesDomain#s3_exporting}
        '''
        value = CustomerprofilesDomainRuleBasedMatchingExportingConfig(
            s3_exporting=s3_exporting
        )

        return typing.cast(None, jsii.invoke(self, "putExportingConfig", [value]))

    @jsii.member(jsii_name="putMatchingRules")
    def put_matching_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomerprofilesDomainRuleBasedMatchingMatchingRules, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb413a3f81946578196cd3ec04e34577630a7f877bd66012fb97174cae21bef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatchingRules", [value]))

    @jsii.member(jsii_name="resetAttributeTypesSelector")
    def reset_attribute_types_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttributeTypesSelector", []))

    @jsii.member(jsii_name="resetConflictResolution")
    def reset_conflict_resolution(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConflictResolution", []))

    @jsii.member(jsii_name="resetExportingConfig")
    def reset_exporting_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportingConfig", []))

    @jsii.member(jsii_name="resetMatchingRules")
    def reset_matching_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchingRules", []))

    @jsii.member(jsii_name="resetMaxAllowedRuleLevelForMatching")
    def reset_max_allowed_rule_level_for_matching(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAllowedRuleLevelForMatching", []))

    @jsii.member(jsii_name="resetMaxAllowedRuleLevelForMerging")
    def reset_max_allowed_rule_level_for_merging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAllowedRuleLevelForMerging", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="attributeTypesSelector")
    def attribute_types_selector(
        self,
    ) -> CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelectorOutputReference:
        return typing.cast(CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelectorOutputReference, jsii.get(self, "attributeTypesSelector"))

    @builtins.property
    @jsii.member(jsii_name="conflictResolution")
    def conflict_resolution(
        self,
    ) -> CustomerprofilesDomainRuleBasedMatchingConflictResolutionOutputReference:
        return typing.cast(CustomerprofilesDomainRuleBasedMatchingConflictResolutionOutputReference, jsii.get(self, "conflictResolution"))

    @builtins.property
    @jsii.member(jsii_name="exportingConfig")
    def exporting_config(
        self,
    ) -> CustomerprofilesDomainRuleBasedMatchingExportingConfigOutputReference:
        return typing.cast(CustomerprofilesDomainRuleBasedMatchingExportingConfigOutputReference, jsii.get(self, "exportingConfig"))

    @builtins.property
    @jsii.member(jsii_name="matchingRules")
    def matching_rules(
        self,
    ) -> CustomerprofilesDomainRuleBasedMatchingMatchingRulesList:
        return typing.cast(CustomerprofilesDomainRuleBasedMatchingMatchingRulesList, jsii.get(self, "matchingRules"))

    @builtins.property
    @jsii.member(jsii_name="attributeTypesSelectorInput")
    def attribute_types_selector_input(
        self,
    ) -> typing.Optional[CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector]:
        return typing.cast(typing.Optional[CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector], jsii.get(self, "attributeTypesSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="conflictResolutionInput")
    def conflict_resolution_input(
        self,
    ) -> typing.Optional[CustomerprofilesDomainRuleBasedMatchingConflictResolution]:
        return typing.cast(typing.Optional[CustomerprofilesDomainRuleBasedMatchingConflictResolution], jsii.get(self, "conflictResolutionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="exportingConfigInput")
    def exporting_config_input(
        self,
    ) -> typing.Optional[CustomerprofilesDomainRuleBasedMatchingExportingConfig]:
        return typing.cast(typing.Optional[CustomerprofilesDomainRuleBasedMatchingExportingConfig], jsii.get(self, "exportingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="matchingRulesInput")
    def matching_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomerprofilesDomainRuleBasedMatchingMatchingRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomerprofilesDomainRuleBasedMatchingMatchingRules]]], jsii.get(self, "matchingRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAllowedRuleLevelForMatchingInput")
    def max_allowed_rule_level_for_matching_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAllowedRuleLevelForMatchingInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAllowedRuleLevelForMergingInput")
    def max_allowed_rule_level_for_merging_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAllowedRuleLevelForMergingInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__363940186eeeddb44a2f91ae21b5b57a927cce8a88b7123388041bb198b04642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAllowedRuleLevelForMatching")
    def max_allowed_rule_level_for_matching(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAllowedRuleLevelForMatching"))

    @max_allowed_rule_level_for_matching.setter
    def max_allowed_rule_level_for_matching(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075535287fa9727414f52e0a318cbc0bd14db0fc462bcaaf3239ff20d1ed2036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAllowedRuleLevelForMatching", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAllowedRuleLevelForMerging")
    def max_allowed_rule_level_for_merging(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAllowedRuleLevelForMerging"))

    @max_allowed_rule_level_for_merging.setter
    def max_allowed_rule_level_for_merging(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1ea48b0484c2d062f2045d5f9ab7f8b3eb27fa28b377b6b2b13329e520dc44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAllowedRuleLevelForMerging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3b299791ac0c6c2159c4555ea17acc558f1c0e44cc511988bf787f810820e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CustomerprofilesDomainRuleBasedMatching]:
        return typing.cast(typing.Optional[CustomerprofilesDomainRuleBasedMatching], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CustomerprofilesDomainRuleBasedMatching],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9c37175608f356643722110cc5b952422d07e34f63a58f370421b5f69648a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CustomerprofilesDomain",
    "CustomerprofilesDomainConfig",
    "CustomerprofilesDomainMatching",
    "CustomerprofilesDomainMatchingAutoMerging",
    "CustomerprofilesDomainMatchingAutoMergingConflictResolution",
    "CustomerprofilesDomainMatchingAutoMergingConflictResolutionOutputReference",
    "CustomerprofilesDomainMatchingAutoMergingConsolidation",
    "CustomerprofilesDomainMatchingAutoMergingConsolidationOutputReference",
    "CustomerprofilesDomainMatchingAutoMergingOutputReference",
    "CustomerprofilesDomainMatchingExportingConfig",
    "CustomerprofilesDomainMatchingExportingConfigOutputReference",
    "CustomerprofilesDomainMatchingExportingConfigS3Exporting",
    "CustomerprofilesDomainMatchingExportingConfigS3ExportingOutputReference",
    "CustomerprofilesDomainMatchingJobSchedule",
    "CustomerprofilesDomainMatchingJobScheduleOutputReference",
    "CustomerprofilesDomainMatchingOutputReference",
    "CustomerprofilesDomainRuleBasedMatching",
    "CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector",
    "CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelectorOutputReference",
    "CustomerprofilesDomainRuleBasedMatchingConflictResolution",
    "CustomerprofilesDomainRuleBasedMatchingConflictResolutionOutputReference",
    "CustomerprofilesDomainRuleBasedMatchingExportingConfig",
    "CustomerprofilesDomainRuleBasedMatchingExportingConfigOutputReference",
    "CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting",
    "CustomerprofilesDomainRuleBasedMatchingExportingConfigS3ExportingOutputReference",
    "CustomerprofilesDomainRuleBasedMatchingMatchingRules",
    "CustomerprofilesDomainRuleBasedMatchingMatchingRulesList",
    "CustomerprofilesDomainRuleBasedMatchingMatchingRulesOutputReference",
    "CustomerprofilesDomainRuleBasedMatchingOutputReference",
]

publication.publish()

def _typecheckingstub__3164d89b8342fd58c32815aa8c98563fd5f007db5985969185441340bcffc6e7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_expiration_days: jsii.Number,
    domain_name: builtins.str,
    dead_letter_queue_url: typing.Optional[builtins.str] = None,
    default_encryption_key: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    matching: typing.Optional[typing.Union[CustomerprofilesDomainMatching, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_based_matching: typing.Optional[typing.Union[CustomerprofilesDomainRuleBasedMatching, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__04166869dc2f1caf55008d5f0d8866410141b4b5d936471127e898b09ae4d63d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63634b1c9b6522bfdff7d0c63b8622d614f9694ae054be49384af403ce1f8dbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25c7d16683832cfc98b91aa56d9bf34bd62971257df4c70bfcdb5f9e0160db1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5503afc3aec7dcc21296c3de3f08d7c92320db35857bff6c33d470512cf35ee9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60fadc617c4c7ad5f441582d39dec9bb8b2ff623ff070751cc6cb5a781ef997d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a51d9036e5e389e200e3da5cca394ed56c506bcd96cedc3b03bb1dfe22b2d15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8cc2905b7ec69cb9a8a65a9dd8cdc0afa32b377f2471d52570fc24b89c03063(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c4b2da9551a9e6f91c9e36d55d21bcdf3e6ca75d7b4aa6849ead381056c5fa(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31303aaab3a3c03080857caca20b23e01f22a8a99e0cc0a86b328aea70ed099(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_expiration_days: jsii.Number,
    domain_name: builtins.str,
    dead_letter_queue_url: typing.Optional[builtins.str] = None,
    default_encryption_key: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    matching: typing.Optional[typing.Union[CustomerprofilesDomainMatching, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_based_matching: typing.Optional[typing.Union[CustomerprofilesDomainRuleBasedMatching, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4b3440b176ef78bfcddc8888a0c8e0fbba9dbd3d41243f697e3884c8d2f530(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    auto_merging: typing.Optional[typing.Union[CustomerprofilesDomainMatchingAutoMerging, typing.Dict[builtins.str, typing.Any]]] = None,
    exporting_config: typing.Optional[typing.Union[CustomerprofilesDomainMatchingExportingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    job_schedule: typing.Optional[typing.Union[CustomerprofilesDomainMatchingJobSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b93edf8609f4628a8d1a36c3b33a2a8bc95a87c17218452a5fc2e326caa3c1(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    conflict_resolution: typing.Optional[typing.Union[CustomerprofilesDomainMatchingAutoMergingConflictResolution, typing.Dict[builtins.str, typing.Any]]] = None,
    consolidation: typing.Optional[typing.Union[CustomerprofilesDomainMatchingAutoMergingConsolidation, typing.Dict[builtins.str, typing.Any]]] = None,
    min_allowed_confidence_score_for_merging: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3242aa776d6761704e6d4f17a2e64e13b1e4331466905c6130e0cd452096cfd0(
    *,
    conflict_resolving_model: builtins.str,
    source_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640b216ffa14d4b28aaaaf44c1d993d2491887f3cc6c4bef6cbcdbe98b61b130(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f24f7feda81d2c3b15586f4551d99ef9f2269c84ba64227f7fd3a113450f45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f75b215b2de76aaab097c4f5e464c8880906630141b5fb94b6a73d304dfd2f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98609e9b3b67982629e4c3d9d2e63fd66c68e8fdab6ca53b759bd69a665cc46(
    value: typing.Optional[CustomerprofilesDomainMatchingAutoMergingConflictResolution],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4a1719942dd0af2e777d67b09c41858cc34ea2dde8b928a4e4dcb1aeceebd2(
    *,
    matching_attributes_list: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Sequence[builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a789c8946fedad8cd385bc9f776dc14511ecc1efba821202f145041846ca4ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c709347afebb48c691802d6f9a43bbb45441e6fc1316f0dc88fa732134c22441(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[typing.List[builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e55895fc107b63924c965094e9e63ceb9b1b1a9e03cd9f09c0e9b2445b54c11(
    value: typing.Optional[CustomerprofilesDomainMatchingAutoMergingConsolidation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49759ad4f5393e58ca50750d897f0b7964c06d00fbd4e3fb9fbae060cc4463e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c440f05324ee1caeb324c2fdd56c1551399c9adc000e989e871e315cf4190ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4d475d24767c40dc530f359a40b78a8f310e34c14c8f66bb22c9a8636ecce7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648a3315782bfd81a93fb95c0b0e433758a3669f5083c97e87ed01a2625d0117(
    value: typing.Optional[CustomerprofilesDomainMatchingAutoMerging],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f38024e27b2ae9def4c331f002ce9b300fc4298939094eb3206825ef6e252c3(
    *,
    s3_exporting: typing.Optional[typing.Union[CustomerprofilesDomainMatchingExportingConfigS3Exporting, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414c4f9f6f7eb20d6c79ff2f71cccee63affc1dda1a7e8dc42d644f7c37d208b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e263dc0a8c247481aa34d33b833137b1248a703c351e8c5b6963930a4afcc058(
    value: typing.Optional[CustomerprofilesDomainMatchingExportingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc287237c9f3996a77c264c277575337d947320d1f601bb5f20c0c1ca82d2fb2(
    *,
    s3_bucket_name: builtins.str,
    s3_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b9e85d23c53474e4d1dd464c0aa7a11a78ad32b7a3c83bcec7f3da8918854f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2e9afebe649299b7ef8fed37b80ab4b1c2719a66f3fc96db8cb5f92b81047a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b943b14522e82a900e8e84355c0036758bc44680c95128ce4fae562f969ce5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b40d4768c3563b51fd5bdcec8d4c44242156146db8a27e38c65fde6ff2eb09(
    value: typing.Optional[CustomerprofilesDomainMatchingExportingConfigS3Exporting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764e24acc585cb43889fdc73075c5067b440f9613cc27d88ecd55bce8928db3e(
    *,
    day_of_the_week: builtins.str,
    time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715d88b7e008f45f7f5b6f59a69fc05e10a184933d3f3dfeba4909b2c801eb1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83d36e85ca447ce364a176da970eab90f0ad0ed50b026a28adc3829f3f9b433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6516a6721a13cfac4f35f017a06e763578abfe53da38b2f446aff65a4870b2c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489dda63aeced89df15c64bf766d8a11d690fc2f9b5ab3cdd9df8dbdc083235c(
    value: typing.Optional[CustomerprofilesDomainMatchingJobSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58fc3b5dead2d856fe006e3a75e83686bcac6b1acfd708680c2dde4d642e37ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216c38b8c2ca4ddeb3bab15fddc911abcecb6535c80ffb3863b340fe22dc7219(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49431d568f36e7f7b78827c58f72b78de6a47d414537420b9f154829ab58322f(
    value: typing.Optional[CustomerprofilesDomainMatching],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86062e96fbda1bdf9e8564d49781c32204023f2b59c4dd82784d12408d1348c7(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    attribute_types_selector: typing.Optional[typing.Union[CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    conflict_resolution: typing.Optional[typing.Union[CustomerprofilesDomainRuleBasedMatchingConflictResolution, typing.Dict[builtins.str, typing.Any]]] = None,
    exporting_config: typing.Optional[typing.Union[CustomerprofilesDomainRuleBasedMatchingExportingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    matching_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomerprofilesDomainRuleBasedMatchingMatchingRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_allowed_rule_level_for_matching: typing.Optional[jsii.Number] = None,
    max_allowed_rule_level_for_merging: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5133db52b8df22c171606b572b5a72f891382d4207c460f4d0510ded924186ac(
    *,
    attribute_matching_model: builtins.str,
    address: typing.Optional[typing.Sequence[builtins.str]] = None,
    email_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    phone_number: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e83005765c56087bc0cd01fef1159368df4d15c880821925dfffd2060c585d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfee1371ef4fc682740ddae334770f0091325405402aa2ad8f2c0a695379365a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8349552cdcf1cf8122613724c2913396891fb0631f9a3991af6ae937f1ce89b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbc8622dd7a8256b549cbe2fdb78df5a4b9b379798f1b11961797b695bcc705(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552cdb6be16d1732c5f1cc36b8179a00d0f4840edd41ddedf4125d9b534c478c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec65d41c3862b6cef368a3fde0d92c49e5075d1a05ffedb14321492ac818f770(
    value: typing.Optional[CustomerprofilesDomainRuleBasedMatchingAttributeTypesSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8472b6b4791b9420569e3a8c9a32ea66bd278f39e6b2519971fefa631bdecb5(
    *,
    conflict_resolving_model: builtins.str,
    source_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497b34e66560cbc88d16d013935c3911580892ffa69c1ddb78a95dcecace1c9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c1b5bcfe6618dd6855fb3642d4262692d3d98c7bb03fcf355742768b5fec22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41b0e36fe3a7deef7f6789512b37934202dd8e2c778efaca03931efab8e54b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7970d1b3ae1bc09da1048927c188dfbbebc56fedcc43ca44eeb6b875c9d869f(
    value: typing.Optional[CustomerprofilesDomainRuleBasedMatchingConflictResolution],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec026e99453d35ba4db980b4a90857f43e4d97b2d4f5842b9aff5655f0e8ffb7(
    *,
    s3_exporting: typing.Optional[typing.Union[CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a869681a2680ea9b7cfd307d951440d9791610f54a4179c67d196e32f036069(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9794fb95b8f5408047cff0bba35a0589b5b9167e02e0e4bc33aa068a31ef18(
    value: typing.Optional[CustomerprofilesDomainRuleBasedMatchingExportingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bba76a1ce680a48b1eeb637181a6441e268c007207652e86018bb2ae7282775(
    *,
    s3_bucket_name: builtins.str,
    s3_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7e0247204c962cd2ca33a4845beb570279c78a9e60805fae9754d26029fb46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59088aa5dcce068ea3e2cea4ded5271b2eab50de6badb65a3fcae857e0285c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cb82789493b328b6cf1ea6bc42cb57222f7451edc35c0186cbf98e52c9dade(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9537f035795926306db92c271cde65a018c003156a5898dd9d6ae8102b42f4d7(
    value: typing.Optional[CustomerprofilesDomainRuleBasedMatchingExportingConfigS3Exporting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a8b2e4f55b70cc8120dcce4ca3fbf9d9a10b9d9b372ed627a1937d231fe276(
    *,
    rule: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626e3dd7d19183086b55cf6816d88c76da0f32815edba4235dee92f190b7d046(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e52fab5eee873b5611a6c08cd3efc3ae0a9b171c3204c3d3d63f6b557c2a7a80(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6a81f4007ca7c01d57e9bd93da148fddb3b631903f22c0d2dbc268cb3db99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8602d58803598b8659c967b462cd4d8650a323a69783b8bcc005d560d8f9754(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1f0542c4f42d566b88a5d8e587e9c9cda94b9a162599aef52abd19d8f549c3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2109975351f9cbd9598e150590a8e17ccc1dca7d419fb3f8cf5b7db6945bde8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CustomerprofilesDomainRuleBasedMatchingMatchingRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63285d939190dc66714c8f8b0ca646bbdbb94633f80ddc30abc5b6e9198884ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4186ae2e6ec59f938de76654771fafd26740e6604b1948423a755d3994edfb6d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c460188c773f06c0c2324aa0492fe4176e35c8dbdf74c1c68b215c4e97834c39(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CustomerprofilesDomainRuleBasedMatchingMatchingRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb715fcc94188ce5b7d1ceb475b4aed614c460cdda481845496d5abcf8f0935(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb413a3f81946578196cd3ec04e34577630a7f877bd66012fb97174cae21bef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CustomerprofilesDomainRuleBasedMatchingMatchingRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363940186eeeddb44a2f91ae21b5b57a927cce8a88b7123388041bb198b04642(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075535287fa9727414f52e0a318cbc0bd14db0fc462bcaaf3239ff20d1ed2036(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1ea48b0484c2d062f2045d5f9ab7f8b3eb27fa28b377b6b2b13329e520dc44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3b299791ac0c6c2159c4555ea17acc558f1c0e44cc511988bf787f810820e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9c37175608f356643722110cc5b952422d07e34f63a58f370421b5f69648a4(
    value: typing.Optional[CustomerprofilesDomainRuleBasedMatching],
) -> None:
    """Type checking stubs"""
    pass
