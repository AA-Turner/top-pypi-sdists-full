r'''
# `azurerm_palo_alto_local_rulestack_rule`

Refer to the Terraform Registry for docs: [`azurerm_palo_alto_local_rulestack_rule`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule).
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


class PaloAltoLocalRulestackRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoLocalRulestackRule.PaloAltoLocalRulestackRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule azurerm_palo_alto_local_rulestack_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        applications: typing.Sequence[builtins.str],
        destination: typing.Union["PaloAltoLocalRulestackRuleDestination", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        priority: jsii.Number,
        rulestack_id: builtins.str,
        source: typing.Union["PaloAltoLocalRulestackRuleSource", typing.Dict[builtins.str, typing.Any]],
        audit_comment: typing.Optional[builtins.str] = None,
        category: typing.Optional[typing.Union["PaloAltoLocalRulestackRuleCategory", typing.Dict[builtins.str, typing.Any]]] = None,
        decryption_rule_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        inspection_certificate_id: typing.Optional[builtins.str] = None,
        logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negate_destination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negate_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protocol: typing.Optional[builtins.str] = None,
        protocol_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PaloAltoLocalRulestackRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule azurerm_palo_alto_local_rulestack_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#action PaloAltoLocalRulestackRule#action}.
        :param applications: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#applications PaloAltoLocalRulestackRule#applications}.
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#destination PaloAltoLocalRulestackRule#destination}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#name PaloAltoLocalRulestackRule#name}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#priority PaloAltoLocalRulestackRule#priority}.
        :param rulestack_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#rulestack_id PaloAltoLocalRulestackRule#rulestack_id}.
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#source PaloAltoLocalRulestackRule#source}
        :param audit_comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#audit_comment PaloAltoLocalRulestackRule#audit_comment}.
        :param category: category block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#category PaloAltoLocalRulestackRule#category}
        :param decryption_rule_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#decryption_rule_type PaloAltoLocalRulestackRule#decryption_rule_type}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#description PaloAltoLocalRulestackRule#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#enabled PaloAltoLocalRulestackRule#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#id PaloAltoLocalRulestackRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspection_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#inspection_certificate_id PaloAltoLocalRulestackRule#inspection_certificate_id}.
        :param logging_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#logging_enabled PaloAltoLocalRulestackRule#logging_enabled}.
        :param negate_destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#negate_destination PaloAltoLocalRulestackRule#negate_destination}.
        :param negate_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#negate_source PaloAltoLocalRulestackRule#negate_source}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#protocol PaloAltoLocalRulestackRule#protocol}.
        :param protocol_ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#protocol_ports PaloAltoLocalRulestackRule#protocol_ports}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#tags PaloAltoLocalRulestackRule#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#timeouts PaloAltoLocalRulestackRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65660c187fc7320c3128770c961ceb4c36f8269ac21d27ff7e8fa7cf974b24bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PaloAltoLocalRulestackRuleConfig(
            action=action,
            applications=applications,
            destination=destination,
            name=name,
            priority=priority,
            rulestack_id=rulestack_id,
            source=source,
            audit_comment=audit_comment,
            category=category,
            decryption_rule_type=decryption_rule_type,
            description=description,
            enabled=enabled,
            id=id,
            inspection_certificate_id=inspection_certificate_id,
            logging_enabled=logging_enabled,
            negate_destination=negate_destination,
            negate_source=negate_source,
            protocol=protocol,
            protocol_ports=protocol_ports,
            tags=tags,
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
        '''Generates CDKTF code for importing a PaloAltoLocalRulestackRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PaloAltoLocalRulestackRule to import.
        :param import_from_id: The id of the existing PaloAltoLocalRulestackRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PaloAltoLocalRulestackRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea2d555420d08c2a9f4473e3b6a8a3537d5bf3e9e7ec163982d04aaa80dd947)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCategory")
    def put_category(
        self,
        *,
        custom_urls: typing.Sequence[builtins.str],
        feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param custom_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#custom_urls PaloAltoLocalRulestackRule#custom_urls}.
        :param feeds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#feeds PaloAltoLocalRulestackRule#feeds}.
        '''
        value = PaloAltoLocalRulestackRuleCategory(
            custom_urls=custom_urls, feeds=feeds
        )

        return typing.cast(None, jsii.invoke(self, "putCategory", [value]))

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        *,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        countries: typing.Optional[typing.Sequence[builtins.str]] = None,
        feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_rulestack_fqdn_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_rulestack_prefix_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#cidrs PaloAltoLocalRulestackRule#cidrs}.
        :param countries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#countries PaloAltoLocalRulestackRule#countries}.
        :param feeds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#feeds PaloAltoLocalRulestackRule#feeds}.
        :param local_rulestack_fqdn_list_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#local_rulestack_fqdn_list_ids PaloAltoLocalRulestackRule#local_rulestack_fqdn_list_ids}.
        :param local_rulestack_prefix_list_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#local_rulestack_prefix_list_ids PaloAltoLocalRulestackRule#local_rulestack_prefix_list_ids}.
        '''
        value = PaloAltoLocalRulestackRuleDestination(
            cidrs=cidrs,
            countries=countries,
            feeds=feeds,
            local_rulestack_fqdn_list_ids=local_rulestack_fqdn_list_ids,
            local_rulestack_prefix_list_ids=local_rulestack_prefix_list_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putDestination", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        countries: typing.Optional[typing.Sequence[builtins.str]] = None,
        feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_rulestack_prefix_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#cidrs PaloAltoLocalRulestackRule#cidrs}.
        :param countries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#countries PaloAltoLocalRulestackRule#countries}.
        :param feeds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#feeds PaloAltoLocalRulestackRule#feeds}.
        :param local_rulestack_prefix_list_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#local_rulestack_prefix_list_ids PaloAltoLocalRulestackRule#local_rulestack_prefix_list_ids}.
        '''
        value = PaloAltoLocalRulestackRuleSource(
            cidrs=cidrs,
            countries=countries,
            feeds=feeds,
            local_rulestack_prefix_list_ids=local_rulestack_prefix_list_ids,
        )

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#create PaloAltoLocalRulestackRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#delete PaloAltoLocalRulestackRule#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#read PaloAltoLocalRulestackRule#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#update PaloAltoLocalRulestackRule#update}.
        '''
        value = PaloAltoLocalRulestackRuleTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAuditComment")
    def reset_audit_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuditComment", []))

    @jsii.member(jsii_name="resetCategory")
    def reset_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategory", []))

    @jsii.member(jsii_name="resetDecryptionRuleType")
    def reset_decryption_rule_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDecryptionRuleType", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInspectionCertificateId")
    def reset_inspection_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectionCertificateId", []))

    @jsii.member(jsii_name="resetLoggingEnabled")
    def reset_logging_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingEnabled", []))

    @jsii.member(jsii_name="resetNegateDestination")
    def reset_negate_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateDestination", []))

    @jsii.member(jsii_name="resetNegateSource")
    def reset_negate_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegateSource", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetProtocolPorts")
    def reset_protocol_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolPorts", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="category")
    def category(self) -> "PaloAltoLocalRulestackRuleCategoryOutputReference":
        return typing.cast("PaloAltoLocalRulestackRuleCategoryOutputReference", jsii.get(self, "category"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> "PaloAltoLocalRulestackRuleDestinationOutputReference":
        return typing.cast("PaloAltoLocalRulestackRuleDestinationOutputReference", jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "PaloAltoLocalRulestackRuleSourceOutputReference":
        return typing.cast("PaloAltoLocalRulestackRuleSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PaloAltoLocalRulestackRuleTimeoutsOutputReference":
        return typing.cast("PaloAltoLocalRulestackRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationsInput")
    def applications_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "applicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="auditCommentInput")
    def audit_comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "auditCommentInput"))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional["PaloAltoLocalRulestackRuleCategory"]:
        return typing.cast(typing.Optional["PaloAltoLocalRulestackRuleCategory"], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="decryptionRuleTypeInput")
    def decryption_rule_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "decryptionRuleTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(
        self,
    ) -> typing.Optional["PaloAltoLocalRulestackRuleDestination"]:
        return typing.cast(typing.Optional["PaloAltoLocalRulestackRuleDestination"], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectionCertificateIdInput")
    def inspection_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inspectionCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingEnabledInput")
    def logging_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "loggingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="negateDestinationInput")
    def negate_destination_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="negateSourceInput")
    def negate_source_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolPortsInput")
    def protocol_ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "protocolPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="rulestackIdInput")
    def rulestack_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rulestackIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["PaloAltoLocalRulestackRuleSource"]:
        return typing.cast(typing.Optional["PaloAltoLocalRulestackRuleSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PaloAltoLocalRulestackRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PaloAltoLocalRulestackRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e7bac436af8748d5c106bb73fb0497a20a66f7bda41084ca4e80cb6753aae5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applications")
    def applications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "applications"))

    @applications.setter
    def applications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd7a703e6c1903d33efeadf97940eef7fb3d302a5e48385488c68ddf7abdca2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="auditComment")
    def audit_comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "auditComment"))

    @audit_comment.setter
    def audit_comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad40c39179e1404e5c63176ac7a016daba9b15f73886a43e93dfde9565a8c375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditComment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="decryptionRuleType")
    def decryption_rule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "decryptionRuleType"))

    @decryption_rule_type.setter
    def decryption_rule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eca07122f07421560de2964ac9e477c1de197a285ed3eccfd4b5a87c0c239796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "decryptionRuleType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f35e79bb6cfe55e6b55e69fb7f2abec7c38e67e9987fbfae090eab500600958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__b8e67aca692597ac92206dd8555b5b20cc73883c1a276a58286da32fe382a46b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ab4a8bc95db334308187e084419e24199f5a2f4c6bb4829dd5381da5e56256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inspectionCertificateId")
    def inspection_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inspectionCertificateId"))

    @inspection_certificate_id.setter
    def inspection_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1120c8460e76472292ff3c8bb346f4e01e3bb530c2da746235d47e3c3300e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectionCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loggingEnabled")
    def logging_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "loggingEnabled"))

    @logging_enabled.setter
    def logging_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094b44f0aaafc5b20511ca28072e648a00e780fe27c1abd8cd59c951093be986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3cc4a076ad5f5f49601fd351e579bbad40f3ff78ae02c3724c9f31696622e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateDestination")
    def negate_destination(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateDestination"))

    @negate_destination.setter
    def negate_destination(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73bb6f5bc5245c7f028d1f62a8f88acb8f025ade06f81ab7a856d95209c21711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateDestination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negateSource")
    def negate_source(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negateSource"))

    @negate_source.setter
    def negate_source(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f68879d831e61d5a711d25cfdae7c439ad9fdf179d8ccf80a40803370e74b4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negateSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd7722c63f120c0168f6cfccd7c9f6383c5bf10ee00e3fa5fa9eff9c8d303df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b94a5d9bcc88c449c8e6cd571a22da9400f08bc3ef6e0ed9553ae88c220d85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocolPorts")
    def protocol_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocolPorts"))

    @protocol_ports.setter
    def protocol_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ae6c599258b3ee3f6bc340f8fab15152e12a504876140ecceca28538c8e277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rulestackId")
    def rulestack_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rulestackId"))

    @rulestack_id.setter
    def rulestack_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d2ca6ce6cff10fc86ded9b38bc83204ff878b47d2d833b029cb82ee49b3c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulestackId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e786a2d286e0ca50f821a7bb1c716768b4752b46061a44910eca093fd5de5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoLocalRulestackRule.PaloAltoLocalRulestackRuleCategory",
    jsii_struct_bases=[],
    name_mapping={"custom_urls": "customUrls", "feeds": "feeds"},
)
class PaloAltoLocalRulestackRuleCategory:
    def __init__(
        self,
        *,
        custom_urls: typing.Sequence[builtins.str],
        feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param custom_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#custom_urls PaloAltoLocalRulestackRule#custom_urls}.
        :param feeds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#feeds PaloAltoLocalRulestackRule#feeds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ec9a20cc71d304caca7af08da42ff95e6190baf7da4c712891463137e1001d)
            check_type(argname="argument custom_urls", value=custom_urls, expected_type=type_hints["custom_urls"])
            check_type(argname="argument feeds", value=feeds, expected_type=type_hints["feeds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_urls": custom_urls,
        }
        if feeds is not None:
            self._values["feeds"] = feeds

    @builtins.property
    def custom_urls(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#custom_urls PaloAltoLocalRulestackRule#custom_urls}.'''
        result = self._values.get("custom_urls")
        assert result is not None, "Required property 'custom_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def feeds(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#feeds PaloAltoLocalRulestackRule#feeds}.'''
        result = self._values.get("feeds")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoLocalRulestackRuleCategory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoLocalRulestackRuleCategoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoLocalRulestackRule.PaloAltoLocalRulestackRuleCategoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc0a8c1564a6f5335d9b7abf91264511fda260751e7b2485599779b5ed2db265)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFeeds")
    def reset_feeds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeeds", []))

    @builtins.property
    @jsii.member(jsii_name="customUrlsInput")
    def custom_urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="feedsInput")
    def feeds_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "feedsInput"))

    @builtins.property
    @jsii.member(jsii_name="customUrls")
    def custom_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customUrls"))

    @custom_urls.setter
    def custom_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8832dded0a59f2d208cf3c8e301b4aa55389855c2152e9f18d964fc06914c310)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="feeds")
    def feeds(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "feeds"))

    @feeds.setter
    def feeds(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b957749820c561b84ffa4edab694c07f8657953bf01bd84e7532ce1a2a0a7d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "feeds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PaloAltoLocalRulestackRuleCategory]:
        return typing.cast(typing.Optional[PaloAltoLocalRulestackRuleCategory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoLocalRulestackRuleCategory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83067d42b5a98d90ce58cad5fc944f1e7083f538df4ebcd1c281962bb0139e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoLocalRulestackRule.PaloAltoLocalRulestackRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action": "action",
        "applications": "applications",
        "destination": "destination",
        "name": "name",
        "priority": "priority",
        "rulestack_id": "rulestackId",
        "source": "source",
        "audit_comment": "auditComment",
        "category": "category",
        "decryption_rule_type": "decryptionRuleType",
        "description": "description",
        "enabled": "enabled",
        "id": "id",
        "inspection_certificate_id": "inspectionCertificateId",
        "logging_enabled": "loggingEnabled",
        "negate_destination": "negateDestination",
        "negate_source": "negateSource",
        "protocol": "protocol",
        "protocol_ports": "protocolPorts",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class PaloAltoLocalRulestackRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action: builtins.str,
        applications: typing.Sequence[builtins.str],
        destination: typing.Union["PaloAltoLocalRulestackRuleDestination", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        priority: jsii.Number,
        rulestack_id: builtins.str,
        source: typing.Union["PaloAltoLocalRulestackRuleSource", typing.Dict[builtins.str, typing.Any]],
        audit_comment: typing.Optional[builtins.str] = None,
        category: typing.Optional[typing.Union[PaloAltoLocalRulestackRuleCategory, typing.Dict[builtins.str, typing.Any]]] = None,
        decryption_rule_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        inspection_certificate_id: typing.Optional[builtins.str] = None,
        logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negate_destination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        negate_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protocol: typing.Optional[builtins.str] = None,
        protocol_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PaloAltoLocalRulestackRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#action PaloAltoLocalRulestackRule#action}.
        :param applications: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#applications PaloAltoLocalRulestackRule#applications}.
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#destination PaloAltoLocalRulestackRule#destination}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#name PaloAltoLocalRulestackRule#name}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#priority PaloAltoLocalRulestackRule#priority}.
        :param rulestack_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#rulestack_id PaloAltoLocalRulestackRule#rulestack_id}.
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#source PaloAltoLocalRulestackRule#source}
        :param audit_comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#audit_comment PaloAltoLocalRulestackRule#audit_comment}.
        :param category: category block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#category PaloAltoLocalRulestackRule#category}
        :param decryption_rule_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#decryption_rule_type PaloAltoLocalRulestackRule#decryption_rule_type}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#description PaloAltoLocalRulestackRule#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#enabled PaloAltoLocalRulestackRule#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#id PaloAltoLocalRulestackRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inspection_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#inspection_certificate_id PaloAltoLocalRulestackRule#inspection_certificate_id}.
        :param logging_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#logging_enabled PaloAltoLocalRulestackRule#logging_enabled}.
        :param negate_destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#negate_destination PaloAltoLocalRulestackRule#negate_destination}.
        :param negate_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#negate_source PaloAltoLocalRulestackRule#negate_source}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#protocol PaloAltoLocalRulestackRule#protocol}.
        :param protocol_ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#protocol_ports PaloAltoLocalRulestackRule#protocol_ports}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#tags PaloAltoLocalRulestackRule#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#timeouts PaloAltoLocalRulestackRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination, dict):
            destination = PaloAltoLocalRulestackRuleDestination(**destination)
        if isinstance(source, dict):
            source = PaloAltoLocalRulestackRuleSource(**source)
        if isinstance(category, dict):
            category = PaloAltoLocalRulestackRuleCategory(**category)
        if isinstance(timeouts, dict):
            timeouts = PaloAltoLocalRulestackRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31badf7dba860abd917cfdec0430e58269d69d526e33666ecea034faddbfd78)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument applications", value=applications, expected_type=type_hints["applications"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument rulestack_id", value=rulestack_id, expected_type=type_hints["rulestack_id"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument audit_comment", value=audit_comment, expected_type=type_hints["audit_comment"])
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument decryption_rule_type", value=decryption_rule_type, expected_type=type_hints["decryption_rule_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inspection_certificate_id", value=inspection_certificate_id, expected_type=type_hints["inspection_certificate_id"])
            check_type(argname="argument logging_enabled", value=logging_enabled, expected_type=type_hints["logging_enabled"])
            check_type(argname="argument negate_destination", value=negate_destination, expected_type=type_hints["negate_destination"])
            check_type(argname="argument negate_source", value=negate_source, expected_type=type_hints["negate_source"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocol_ports", value=protocol_ports, expected_type=type_hints["protocol_ports"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "applications": applications,
            "destination": destination,
            "name": name,
            "priority": priority,
            "rulestack_id": rulestack_id,
            "source": source,
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
        if audit_comment is not None:
            self._values["audit_comment"] = audit_comment
        if category is not None:
            self._values["category"] = category
        if decryption_rule_type is not None:
            self._values["decryption_rule_type"] = decryption_rule_type
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if inspection_certificate_id is not None:
            self._values["inspection_certificate_id"] = inspection_certificate_id
        if logging_enabled is not None:
            self._values["logging_enabled"] = logging_enabled
        if negate_destination is not None:
            self._values["negate_destination"] = negate_destination
        if negate_source is not None:
            self._values["negate_source"] = negate_source
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_ports is not None:
            self._values["protocol_ports"] = protocol_ports
        if tags is not None:
            self._values["tags"] = tags
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
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#action PaloAltoLocalRulestackRule#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def applications(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#applications PaloAltoLocalRulestackRule#applications}.'''
        result = self._values.get("applications")
        assert result is not None, "Required property 'applications' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def destination(self) -> "PaloAltoLocalRulestackRuleDestination":
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#destination PaloAltoLocalRulestackRule#destination}
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("PaloAltoLocalRulestackRuleDestination", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#name PaloAltoLocalRulestackRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#priority PaloAltoLocalRulestackRule#priority}.'''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def rulestack_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#rulestack_id PaloAltoLocalRulestackRule#rulestack_id}.'''
        result = self._values.get("rulestack_id")
        assert result is not None, "Required property 'rulestack_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> "PaloAltoLocalRulestackRuleSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#source PaloAltoLocalRulestackRule#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("PaloAltoLocalRulestackRuleSource", result)

    @builtins.property
    def audit_comment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#audit_comment PaloAltoLocalRulestackRule#audit_comment}.'''
        result = self._values.get("audit_comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def category(self) -> typing.Optional[PaloAltoLocalRulestackRuleCategory]:
        '''category block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#category PaloAltoLocalRulestackRule#category}
        '''
        result = self._values.get("category")
        return typing.cast(typing.Optional[PaloAltoLocalRulestackRuleCategory], result)

    @builtins.property
    def decryption_rule_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#decryption_rule_type PaloAltoLocalRulestackRule#decryption_rule_type}.'''
        result = self._values.get("decryption_rule_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#description PaloAltoLocalRulestackRule#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#enabled PaloAltoLocalRulestackRule#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#id PaloAltoLocalRulestackRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspection_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#inspection_certificate_id PaloAltoLocalRulestackRule#inspection_certificate_id}.'''
        result = self._values.get("inspection_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#logging_enabled PaloAltoLocalRulestackRule#logging_enabled}.'''
        result = self._values.get("logging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def negate_destination(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#negate_destination PaloAltoLocalRulestackRule#negate_destination}.'''
        result = self._values.get("negate_destination")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def negate_source(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#negate_source PaloAltoLocalRulestackRule#negate_source}.'''
        result = self._values.get("negate_source")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#protocol PaloAltoLocalRulestackRule#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#protocol_ports PaloAltoLocalRulestackRule#protocol_ports}.'''
        result = self._values.get("protocol_ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#tags PaloAltoLocalRulestackRule#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PaloAltoLocalRulestackRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#timeouts PaloAltoLocalRulestackRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PaloAltoLocalRulestackRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoLocalRulestackRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoLocalRulestackRule.PaloAltoLocalRulestackRuleDestination",
    jsii_struct_bases=[],
    name_mapping={
        "cidrs": "cidrs",
        "countries": "countries",
        "feeds": "feeds",
        "local_rulestack_fqdn_list_ids": "localRulestackFqdnListIds",
        "local_rulestack_prefix_list_ids": "localRulestackPrefixListIds",
    },
)
class PaloAltoLocalRulestackRuleDestination:
    def __init__(
        self,
        *,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        countries: typing.Optional[typing.Sequence[builtins.str]] = None,
        feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_rulestack_fqdn_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_rulestack_prefix_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#cidrs PaloAltoLocalRulestackRule#cidrs}.
        :param countries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#countries PaloAltoLocalRulestackRule#countries}.
        :param feeds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#feeds PaloAltoLocalRulestackRule#feeds}.
        :param local_rulestack_fqdn_list_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#local_rulestack_fqdn_list_ids PaloAltoLocalRulestackRule#local_rulestack_fqdn_list_ids}.
        :param local_rulestack_prefix_list_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#local_rulestack_prefix_list_ids PaloAltoLocalRulestackRule#local_rulestack_prefix_list_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef06df6445821314bd863eeff00011d55291985f9b90fee34134b36e6dda4d7d)
            check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
            check_type(argname="argument countries", value=countries, expected_type=type_hints["countries"])
            check_type(argname="argument feeds", value=feeds, expected_type=type_hints["feeds"])
            check_type(argname="argument local_rulestack_fqdn_list_ids", value=local_rulestack_fqdn_list_ids, expected_type=type_hints["local_rulestack_fqdn_list_ids"])
            check_type(argname="argument local_rulestack_prefix_list_ids", value=local_rulestack_prefix_list_ids, expected_type=type_hints["local_rulestack_prefix_list_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidrs is not None:
            self._values["cidrs"] = cidrs
        if countries is not None:
            self._values["countries"] = countries
        if feeds is not None:
            self._values["feeds"] = feeds
        if local_rulestack_fqdn_list_ids is not None:
            self._values["local_rulestack_fqdn_list_ids"] = local_rulestack_fqdn_list_ids
        if local_rulestack_prefix_list_ids is not None:
            self._values["local_rulestack_prefix_list_ids"] = local_rulestack_prefix_list_ids

    @builtins.property
    def cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#cidrs PaloAltoLocalRulestackRule#cidrs}.'''
        result = self._values.get("cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def countries(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#countries PaloAltoLocalRulestackRule#countries}.'''
        result = self._values.get("countries")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def feeds(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#feeds PaloAltoLocalRulestackRule#feeds}.'''
        result = self._values.get("feeds")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def local_rulestack_fqdn_list_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#local_rulestack_fqdn_list_ids PaloAltoLocalRulestackRule#local_rulestack_fqdn_list_ids}.'''
        result = self._values.get("local_rulestack_fqdn_list_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def local_rulestack_prefix_list_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#local_rulestack_prefix_list_ids PaloAltoLocalRulestackRule#local_rulestack_prefix_list_ids}.'''
        result = self._values.get("local_rulestack_prefix_list_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoLocalRulestackRuleDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoLocalRulestackRuleDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoLocalRulestackRule.PaloAltoLocalRulestackRuleDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c6b9bc711f8c7547d7395b80eaba428d5bd55f8b112416dcf43ea32d8d0593b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCidrs")
    def reset_cidrs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCidrs", []))

    @jsii.member(jsii_name="resetCountries")
    def reset_countries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountries", []))

    @jsii.member(jsii_name="resetFeeds")
    def reset_feeds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeeds", []))

    @jsii.member(jsii_name="resetLocalRulestackFqdnListIds")
    def reset_local_rulestack_fqdn_list_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalRulestackFqdnListIds", []))

    @jsii.member(jsii_name="resetLocalRulestackPrefixListIds")
    def reset_local_rulestack_prefix_list_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalRulestackPrefixListIds", []))

    @builtins.property
    @jsii.member(jsii_name="cidrsInput")
    def cidrs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cidrsInput"))

    @builtins.property
    @jsii.member(jsii_name="countriesInput")
    def countries_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "countriesInput"))

    @builtins.property
    @jsii.member(jsii_name="feedsInput")
    def feeds_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "feedsInput"))

    @builtins.property
    @jsii.member(jsii_name="localRulestackFqdnListIdsInput")
    def local_rulestack_fqdn_list_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "localRulestackFqdnListIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="localRulestackPrefixListIdsInput")
    def local_rulestack_prefix_list_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "localRulestackPrefixListIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="cidrs")
    def cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cidrs"))

    @cidrs.setter
    def cidrs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20dafe5c33f8d18618409a4b9c1cd663016a4371c53be1bb84905354a41f0f12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidrs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countries")
    def countries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "countries"))

    @countries.setter
    def countries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8713fed7885971392f769e62ff88f6e986d636f750f30ec223d575b2e7bdfe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="feeds")
    def feeds(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "feeds"))

    @feeds.setter
    def feeds(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ece3f5459537948a70975d05dd3720c0d12a3bed64e7722f598aecf999a42fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "feeds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localRulestackFqdnListIds")
    def local_rulestack_fqdn_list_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "localRulestackFqdnListIds"))

    @local_rulestack_fqdn_list_ids.setter
    def local_rulestack_fqdn_list_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb14fdf636f54baf971a9d611ad8ca5d3afa897b2195677d3c174a769c02a8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localRulestackFqdnListIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localRulestackPrefixListIds")
    def local_rulestack_prefix_list_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "localRulestackPrefixListIds"))

    @local_rulestack_prefix_list_ids.setter
    def local_rulestack_prefix_list_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a0e73088a69b5835954b49ec1cd355faf4c3a0adc55b2b3db5895382a39fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localRulestackPrefixListIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PaloAltoLocalRulestackRuleDestination]:
        return typing.cast(typing.Optional[PaloAltoLocalRulestackRuleDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoLocalRulestackRuleDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e736eec5b3d0d4b2649a8d6ff24744762bc2f3e7067338e986bb1fe3295b10d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoLocalRulestackRule.PaloAltoLocalRulestackRuleSource",
    jsii_struct_bases=[],
    name_mapping={
        "cidrs": "cidrs",
        "countries": "countries",
        "feeds": "feeds",
        "local_rulestack_prefix_list_ids": "localRulestackPrefixListIds",
    },
)
class PaloAltoLocalRulestackRuleSource:
    def __init__(
        self,
        *,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        countries: typing.Optional[typing.Sequence[builtins.str]] = None,
        feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
        local_rulestack_prefix_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#cidrs PaloAltoLocalRulestackRule#cidrs}.
        :param countries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#countries PaloAltoLocalRulestackRule#countries}.
        :param feeds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#feeds PaloAltoLocalRulestackRule#feeds}.
        :param local_rulestack_prefix_list_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#local_rulestack_prefix_list_ids PaloAltoLocalRulestackRule#local_rulestack_prefix_list_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff53ef82700ade53168f100a033ce8f3abde1b2aed422236612f7fd27946484c)
            check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
            check_type(argname="argument countries", value=countries, expected_type=type_hints["countries"])
            check_type(argname="argument feeds", value=feeds, expected_type=type_hints["feeds"])
            check_type(argname="argument local_rulestack_prefix_list_ids", value=local_rulestack_prefix_list_ids, expected_type=type_hints["local_rulestack_prefix_list_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidrs is not None:
            self._values["cidrs"] = cidrs
        if countries is not None:
            self._values["countries"] = countries
        if feeds is not None:
            self._values["feeds"] = feeds
        if local_rulestack_prefix_list_ids is not None:
            self._values["local_rulestack_prefix_list_ids"] = local_rulestack_prefix_list_ids

    @builtins.property
    def cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#cidrs PaloAltoLocalRulestackRule#cidrs}.'''
        result = self._values.get("cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def countries(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#countries PaloAltoLocalRulestackRule#countries}.'''
        result = self._values.get("countries")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def feeds(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#feeds PaloAltoLocalRulestackRule#feeds}.'''
        result = self._values.get("feeds")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def local_rulestack_prefix_list_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#local_rulestack_prefix_list_ids PaloAltoLocalRulestackRule#local_rulestack_prefix_list_ids}.'''
        result = self._values.get("local_rulestack_prefix_list_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoLocalRulestackRuleSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoLocalRulestackRuleSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoLocalRulestackRule.PaloAltoLocalRulestackRuleSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1302a2c5aefbd3cbde41f78975e5f8f81f01a898a91568d68a99f48a1a2dd472)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCidrs")
    def reset_cidrs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCidrs", []))

    @jsii.member(jsii_name="resetCountries")
    def reset_countries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountries", []))

    @jsii.member(jsii_name="resetFeeds")
    def reset_feeds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeeds", []))

    @jsii.member(jsii_name="resetLocalRulestackPrefixListIds")
    def reset_local_rulestack_prefix_list_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalRulestackPrefixListIds", []))

    @builtins.property
    @jsii.member(jsii_name="cidrsInput")
    def cidrs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cidrsInput"))

    @builtins.property
    @jsii.member(jsii_name="countriesInput")
    def countries_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "countriesInput"))

    @builtins.property
    @jsii.member(jsii_name="feedsInput")
    def feeds_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "feedsInput"))

    @builtins.property
    @jsii.member(jsii_name="localRulestackPrefixListIdsInput")
    def local_rulestack_prefix_list_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "localRulestackPrefixListIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="cidrs")
    def cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cidrs"))

    @cidrs.setter
    def cidrs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0fb3cd9b51e5733f3afec37ce60e8ed57757b9d3c7f652bf8a15aba3dfcea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidrs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countries")
    def countries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "countries"))

    @countries.setter
    def countries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902286ea5b53020364fa3b8de397a70ffb9f0c0ed46b7949ab89f6ed31b75eb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="feeds")
    def feeds(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "feeds"))

    @feeds.setter
    def feeds(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3334a4e261769dd82a07a3e7f98d8c5361d11f53dd5d60b7755d6456c8729674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "feeds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localRulestackPrefixListIds")
    def local_rulestack_prefix_list_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "localRulestackPrefixListIds"))

    @local_rulestack_prefix_list_ids.setter
    def local_rulestack_prefix_list_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac9b6644d78cb8980a46ef414e73c7121b101c70af3ab4aacd1aaeae994e73dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localRulestackPrefixListIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PaloAltoLocalRulestackRuleSource]:
        return typing.cast(typing.Optional[PaloAltoLocalRulestackRuleSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PaloAltoLocalRulestackRuleSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d2092fc74169fafef23edb53b791e4182aaf6b10bd772261cd73046ae51c38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.paloAltoLocalRulestackRule.PaloAltoLocalRulestackRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class PaloAltoLocalRulestackRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#create PaloAltoLocalRulestackRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#delete PaloAltoLocalRulestackRule#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#read PaloAltoLocalRulestackRule#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#update PaloAltoLocalRulestackRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e1f50bde468c1807555f537723cea625568c63ce91b29173357965c6d37d46)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#create PaloAltoLocalRulestackRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#delete PaloAltoLocalRulestackRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#read PaloAltoLocalRulestackRule#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/palo_alto_local_rulestack_rule#update PaloAltoLocalRulestackRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaloAltoLocalRulestackRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PaloAltoLocalRulestackRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.paloAltoLocalRulestackRule.PaloAltoLocalRulestackRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__997725f61de8f5e6117174dab15e5bcb46e225d32c1848f6948944ebb11fec3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81bc084dff4a9a7a192b49e3583d319b1dfb4be271e58df2082ffdfa205ebc95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02843281576f9995d1a58715c9a0de8c6482334ad65ef1d4def52a4bd9419cdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d36f65bdcc4e8284587ed4871f9c90185869e5f71446461585f7cb8a3f7c97b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6f4a719e627e0f68eaeb50ba37ba44574ea43ec8968af72a53d60e0bfbd5cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoLocalRulestackRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoLocalRulestackRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoLocalRulestackRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__239aa840bbe11bf3971d68ca74a868cc9b82b9d89fa4ce3805521a142de549df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PaloAltoLocalRulestackRule",
    "PaloAltoLocalRulestackRuleCategory",
    "PaloAltoLocalRulestackRuleCategoryOutputReference",
    "PaloAltoLocalRulestackRuleConfig",
    "PaloAltoLocalRulestackRuleDestination",
    "PaloAltoLocalRulestackRuleDestinationOutputReference",
    "PaloAltoLocalRulestackRuleSource",
    "PaloAltoLocalRulestackRuleSourceOutputReference",
    "PaloAltoLocalRulestackRuleTimeouts",
    "PaloAltoLocalRulestackRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__65660c187fc7320c3128770c961ceb4c36f8269ac21d27ff7e8fa7cf974b24bb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    applications: typing.Sequence[builtins.str],
    destination: typing.Union[PaloAltoLocalRulestackRuleDestination, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    priority: jsii.Number,
    rulestack_id: builtins.str,
    source: typing.Union[PaloAltoLocalRulestackRuleSource, typing.Dict[builtins.str, typing.Any]],
    audit_comment: typing.Optional[builtins.str] = None,
    category: typing.Optional[typing.Union[PaloAltoLocalRulestackRuleCategory, typing.Dict[builtins.str, typing.Any]]] = None,
    decryption_rule_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    inspection_certificate_id: typing.Optional[builtins.str] = None,
    logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    negate_destination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    negate_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protocol: typing.Optional[builtins.str] = None,
    protocol_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PaloAltoLocalRulestackRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__fea2d555420d08c2a9f4473e3b6a8a3537d5bf3e9e7ec163982d04aaa80dd947(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7bac436af8748d5c106bb73fb0497a20a66f7bda41084ca4e80cb6753aae5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7a703e6c1903d33efeadf97940eef7fb3d302a5e48385488c68ddf7abdca2b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad40c39179e1404e5c63176ac7a016daba9b15f73886a43e93dfde9565a8c375(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca07122f07421560de2964ac9e477c1de197a285ed3eccfd4b5a87c0c239796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f35e79bb6cfe55e6b55e69fb7f2abec7c38e67e9987fbfae090eab500600958(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e67aca692597ac92206dd8555b5b20cc73883c1a276a58286da32fe382a46b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ab4a8bc95db334308187e084419e24199f5a2f4c6bb4829dd5381da5e56256(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1120c8460e76472292ff3c8bb346f4e01e3bb530c2da746235d47e3c3300e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094b44f0aaafc5b20511ca28072e648a00e780fe27c1abd8cd59c951093be986(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3cc4a076ad5f5f49601fd351e579bbad40f3ff78ae02c3724c9f31696622e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bb6f5bc5245c7f028d1f62a8f88acb8f025ade06f81ab7a856d95209c21711(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f68879d831e61d5a711d25cfdae7c439ad9fdf179d8ccf80a40803370e74b4d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd7722c63f120c0168f6cfccd7c9f6383c5bf10ee00e3fa5fa9eff9c8d303df(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b94a5d9bcc88c449c8e6cd571a22da9400f08bc3ef6e0ed9553ae88c220d85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ae6c599258b3ee3f6bc340f8fab15152e12a504876140ecceca28538c8e277(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d2ca6ce6cff10fc86ded9b38bc83204ff878b47d2d833b029cb82ee49b3c28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e786a2d286e0ca50f821a7bb1c716768b4752b46061a44910eca093fd5de5c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ec9a20cc71d304caca7af08da42ff95e6190baf7da4c712891463137e1001d(
    *,
    custom_urls: typing.Sequence[builtins.str],
    feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0a8c1564a6f5335d9b7abf91264511fda260751e7b2485599779b5ed2db265(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8832dded0a59f2d208cf3c8e301b4aa55389855c2152e9f18d964fc06914c310(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b957749820c561b84ffa4edab694c07f8657953bf01bd84e7532ce1a2a0a7d3e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83067d42b5a98d90ce58cad5fc944f1e7083f538df4ebcd1c281962bb0139e8(
    value: typing.Optional[PaloAltoLocalRulestackRuleCategory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31badf7dba860abd917cfdec0430e58269d69d526e33666ecea034faddbfd78(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: builtins.str,
    applications: typing.Sequence[builtins.str],
    destination: typing.Union[PaloAltoLocalRulestackRuleDestination, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    priority: jsii.Number,
    rulestack_id: builtins.str,
    source: typing.Union[PaloAltoLocalRulestackRuleSource, typing.Dict[builtins.str, typing.Any]],
    audit_comment: typing.Optional[builtins.str] = None,
    category: typing.Optional[typing.Union[PaloAltoLocalRulestackRuleCategory, typing.Dict[builtins.str, typing.Any]]] = None,
    decryption_rule_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    inspection_certificate_id: typing.Optional[builtins.str] = None,
    logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    negate_destination: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    negate_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protocol: typing.Optional[builtins.str] = None,
    protocol_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PaloAltoLocalRulestackRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef06df6445821314bd863eeff00011d55291985f9b90fee34134b36e6dda4d7d(
    *,
    cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    countries: typing.Optional[typing.Sequence[builtins.str]] = None,
    feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_rulestack_fqdn_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_rulestack_prefix_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6b9bc711f8c7547d7395b80eaba428d5bd55f8b112416dcf43ea32d8d0593b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20dafe5c33f8d18618409a4b9c1cd663016a4371c53be1bb84905354a41f0f12(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8713fed7885971392f769e62ff88f6e986d636f750f30ec223d575b2e7bdfe0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ece3f5459537948a70975d05dd3720c0d12a3bed64e7722f598aecf999a42fd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb14fdf636f54baf971a9d611ad8ca5d3afa897b2195677d3c174a769c02a8e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a0e73088a69b5835954b49ec1cd355faf4c3a0adc55b2b3db5895382a39fd3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e736eec5b3d0d4b2649a8d6ff24744762bc2f3e7067338e986bb1fe3295b10d4(
    value: typing.Optional[PaloAltoLocalRulestackRuleDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff53ef82700ade53168f100a033ce8f3abde1b2aed422236612f7fd27946484c(
    *,
    cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    countries: typing.Optional[typing.Sequence[builtins.str]] = None,
    feeds: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_rulestack_prefix_list_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1302a2c5aefbd3cbde41f78975e5f8f81f01a898a91568d68a99f48a1a2dd472(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0fb3cd9b51e5733f3afec37ce60e8ed57757b9d3c7f652bf8a15aba3dfcea1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902286ea5b53020364fa3b8de397a70ffb9f0c0ed46b7949ab89f6ed31b75eb4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3334a4e261769dd82a07a3e7f98d8c5361d11f53dd5d60b7755d6456c8729674(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9b6644d78cb8980a46ef414e73c7121b101c70af3ab4aacd1aaeae994e73dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d2092fc74169fafef23edb53b791e4182aaf6b10bd772261cd73046ae51c38(
    value: typing.Optional[PaloAltoLocalRulestackRuleSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e1f50bde468c1807555f537723cea625568c63ce91b29173357965c6d37d46(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997725f61de8f5e6117174dab15e5bcb46e225d32c1848f6948944ebb11fec3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81bc084dff4a9a7a192b49e3583d319b1dfb4be271e58df2082ffdfa205ebc95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02843281576f9995d1a58715c9a0de8c6482334ad65ef1d4def52a4bd9419cdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d36f65bdcc4e8284587ed4871f9c90185869e5f71446461585f7cb8a3f7c97b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6f4a719e627e0f68eaeb50ba37ba44574ea43ec8968af72a53d60e0bfbd5cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239aa840bbe11bf3971d68ca74a868cc9b82b9d89fa4ce3805521a142de549df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PaloAltoLocalRulestackRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
