r'''
# `datadog_csm_threats_agent_rule`

Refer to the Terraform Registry for docs: [`datadog_csm_threats_agent_rule`](https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule).
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


class CsmThreatsAgentRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.csmThreatsAgentRule.CsmThreatsAgentRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule datadog_csm_threats_agent_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        expression: builtins.str,
        name: builtins.str,
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CsmThreatsAgentRuleActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_id: typing.Optional[builtins.str] = None,
        product_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule datadog_csm_threats_agent_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param expression: The SECL expression of the Agent rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#expression CsmThreatsAgentRule#expression}
        :param name: The name of the Agent rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#name CsmThreatsAgentRule#name}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#actions CsmThreatsAgentRule#actions}
        :param description: A description for the Agent rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#description CsmThreatsAgentRule#description}
        :param enabled: Indicates whether the Agent rule is enabled. Must not be used without policy_id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#enabled CsmThreatsAgentRule#enabled}
        :param policy_id: The ID of the agent policy in which the rule is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#policy_id CsmThreatsAgentRule#policy_id}
        :param product_tags: The list of product tags associated with the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#product_tags CsmThreatsAgentRule#product_tags}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b96ea95987798ebe34b266a659f6ec41f8b098fb9529fe89edec606cc13595a2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = CsmThreatsAgentRuleConfig(
            expression=expression,
            name=name,
            actions=actions,
            description=description,
            enabled=enabled,
            policy_id=policy_id,
            product_tags=product_tags,
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
        '''Generates CDKTF code for importing a CsmThreatsAgentRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CsmThreatsAgentRule to import.
        :param import_from_id: The id of the existing CsmThreatsAgentRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CsmThreatsAgentRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2deccf2359142e2d54b59add4f513f6363bcdee66b08685936a5709b5a74cca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CsmThreatsAgentRuleActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301046d350fa883557dd736657e730b5e8678ff9014b34f062ab31ff37aaa81a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetPolicyId")
    def reset_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyId", []))

    @jsii.member(jsii_name="resetProductTags")
    def reset_product_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProductTags", []))

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
    @jsii.member(jsii_name="actions")
    def actions(self) -> "CsmThreatsAgentRuleActionsList":
        return typing.cast("CsmThreatsAgentRuleActionsList", jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CsmThreatsAgentRuleActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CsmThreatsAgentRuleActions"]]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="productTagsInput")
    def product_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "productTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5fde6cf7444808fdb750098789edb5a2b279ce533877e20f40109af1623b3f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07c621b1540ff48e629990ebd420538fb5c9f841503c36c9fbbd5362fef3b521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30b33b27efb3178492b9e2b9fec2d7cd768ccfe24afe50fca8f81de0567c227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f54374f4783f1c580e4c37aa4ac66656d91b41eaf9dff9fdda2cad635d51dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11a5da0f05ab132930bf8cc33e184b64b5aa6266ade23595677682b5403d20b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="productTags")
    def product_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "productTags"))

    @product_tags.setter
    def product_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3238c468d72fb4e032908fc928fd7746e42601ec069942826239f04698c1a405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "productTags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.csmThreatsAgentRule.CsmThreatsAgentRuleActions",
    jsii_struct_bases=[],
    name_mapping={"hash": "hash", "set": "set"},
)
class CsmThreatsAgentRuleActions:
    def __init__(
        self,
        *,
        hash: typing.Optional[typing.Union["CsmThreatsAgentRuleActionsHash", typing.Dict[builtins.str, typing.Any]]] = None,
        set: typing.Optional[typing.Union["CsmThreatsAgentRuleActionsSet", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param hash: hash block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#hash CsmThreatsAgentRule#hash}
        :param set: set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#set CsmThreatsAgentRule#set}
        '''
        if isinstance(hash, dict):
            hash = CsmThreatsAgentRuleActionsHash(**hash)
        if isinstance(set, dict):
            set = CsmThreatsAgentRuleActionsSet(**set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a9b6c6bf33438f36afd7fbe0567a64caad707a897718d9a0f2858a7f57ca17)
            check_type(argname="argument hash", value=hash, expected_type=type_hints["hash"])
            check_type(argname="argument set", value=set, expected_type=type_hints["set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hash is not None:
            self._values["hash"] = hash
        if set is not None:
            self._values["set"] = set

    @builtins.property
    def hash(self) -> typing.Optional["CsmThreatsAgentRuleActionsHash"]:
        '''hash block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#hash CsmThreatsAgentRule#hash}
        '''
        result = self._values.get("hash")
        return typing.cast(typing.Optional["CsmThreatsAgentRuleActionsHash"], result)

    @builtins.property
    def set(self) -> typing.Optional["CsmThreatsAgentRuleActionsSet"]:
        '''set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#set CsmThreatsAgentRule#set}
        '''
        result = self._values.get("set")
        return typing.cast(typing.Optional["CsmThreatsAgentRuleActionsSet"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsmThreatsAgentRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.csmThreatsAgentRule.CsmThreatsAgentRuleActionsHash",
    jsii_struct_bases=[],
    name_mapping={},
)
class CsmThreatsAgentRuleActionsHash:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsmThreatsAgentRuleActionsHash(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CsmThreatsAgentRuleActionsHashOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.csmThreatsAgentRule.CsmThreatsAgentRuleActionsHashOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de26ff18ed0e6490e9769b97f2684c6e46dff67e9e6858d3a4bf17a1928d53ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActionsHash]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActionsHash]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActionsHash]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1f4ce93146da162e17e16fc897299cfd8798064f60dc60ec3f372e4ea26a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CsmThreatsAgentRuleActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.csmThreatsAgentRule.CsmThreatsAgentRuleActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__917b7434d2c31a602cc76dfab03997c4df7c72d04f3461b8f0e602a3a77c7475)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CsmThreatsAgentRuleActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97421f0bf7a41d12b5c55c6d4674d04286b58f13a6d98879110cdff428f0eda2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CsmThreatsAgentRuleActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a9a6ea26ba463e0cdc857650e7341fc36ed11a2a1219b19ab4e8af81a562588)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7de42408361fae6ee9076bafcf04f6cecec85bb011f2eb8317dcbb437a3d7880)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acf4cca05eef7d52b3d6b9d27ec3d2f6c6edee31be42de55c6b95a583c45884f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsmThreatsAgentRuleActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsmThreatsAgentRuleActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsmThreatsAgentRuleActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a33db390cb4ab15bd473d19b6b3384e5ab15805b0d883722243dd2e6149817f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CsmThreatsAgentRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.csmThreatsAgentRule.CsmThreatsAgentRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e947937c063e209b96592a71b19afcd885104dd905a62ca6e372827a61ba9656)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHash")
    def put_hash(self) -> None:
        value = CsmThreatsAgentRuleActionsHash()

        return typing.cast(None, jsii.invoke(self, "putHash", [value]))

    @jsii.member(jsii_name="putSet")
    def put_set(
        self,
        *,
        name: builtins.str,
        append: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        field: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
        ttl: typing.Optional[jsii.Number] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the set action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#name CsmThreatsAgentRule#name}
        :param append: Whether to append to the set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#append CsmThreatsAgentRule#append}
        :param field: The field to get the value from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#field CsmThreatsAgentRule#field}
        :param scope: The scope of the set action (process, container, cgroup, or empty). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#scope CsmThreatsAgentRule#scope}
        :param size: The maximum size of the set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#size CsmThreatsAgentRule#size}
        :param ttl: The time to live for the set in nanoseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#ttl CsmThreatsAgentRule#ttl}
        :param value: The value to set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#value CsmThreatsAgentRule#value}
        '''
        value_ = CsmThreatsAgentRuleActionsSet(
            name=name,
            append=append,
            field=field,
            scope=scope,
            size=size,
            ttl=ttl,
            value=value,
        )

        return typing.cast(None, jsii.invoke(self, "putSet", [value_]))

    @jsii.member(jsii_name="resetSet")
    def reset_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSet", []))

    @builtins.property
    @jsii.member(jsii_name="hash")
    def hash(self) -> CsmThreatsAgentRuleActionsHashOutputReference:
        return typing.cast(CsmThreatsAgentRuleActionsHashOutputReference, jsii.get(self, "hash"))

    @builtins.property
    @jsii.member(jsii_name="set")
    def set(self) -> "CsmThreatsAgentRuleActionsSetOutputReference":
        return typing.cast("CsmThreatsAgentRuleActionsSetOutputReference", jsii.get(self, "set"))

    @builtins.property
    @jsii.member(jsii_name="hashInput")
    def hash_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActionsHash]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActionsHash]], jsii.get(self, "hashInput"))

    @builtins.property
    @jsii.member(jsii_name="setInput")
    def set_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CsmThreatsAgentRuleActionsSet"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CsmThreatsAgentRuleActionsSet"]], jsii.get(self, "setInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1343771c6264c8443c7e3c1dd8e645f73f87e7792a6368c335aca44ea4451bee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.csmThreatsAgentRule.CsmThreatsAgentRuleActionsSet",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "append": "append",
        "field": "field",
        "scope": "scope",
        "size": "size",
        "ttl": "ttl",
        "value": "value",
    },
)
class CsmThreatsAgentRuleActionsSet:
    def __init__(
        self,
        *,
        name: builtins.str,
        append: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        field: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
        ttl: typing.Optional[jsii.Number] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the set action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#name CsmThreatsAgentRule#name}
        :param append: Whether to append to the set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#append CsmThreatsAgentRule#append}
        :param field: The field to get the value from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#field CsmThreatsAgentRule#field}
        :param scope: The scope of the set action (process, container, cgroup, or empty). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#scope CsmThreatsAgentRule#scope}
        :param size: The maximum size of the set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#size CsmThreatsAgentRule#size}
        :param ttl: The time to live for the set in nanoseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#ttl CsmThreatsAgentRule#ttl}
        :param value: The value to set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#value CsmThreatsAgentRule#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d299fa96976ad086426af365bf7d80e33a6c0000d6cf4c63df9664936989f0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument append", value=append, expected_type=type_hints["append"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if append is not None:
            self._values["append"] = append
        if field is not None:
            self._values["field"] = field
        if scope is not None:
            self._values["scope"] = scope
        if size is not None:
            self._values["size"] = size
        if ttl is not None:
            self._values["ttl"] = ttl
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the set action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#name CsmThreatsAgentRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def append(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to append to the set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#append CsmThreatsAgentRule#append}
        '''
        result = self._values.get("append")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def field(self) -> typing.Optional[builtins.str]:
        '''The field to get the value from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#field CsmThreatsAgentRule#field}
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''The scope of the set action (process, container, cgroup, or empty).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#scope CsmThreatsAgentRule#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''The maximum size of the set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#size CsmThreatsAgentRule#size}
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''The time to live for the set in nanoseconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#ttl CsmThreatsAgentRule#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value to set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#value CsmThreatsAgentRule#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsmThreatsAgentRuleActionsSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CsmThreatsAgentRuleActionsSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.csmThreatsAgentRule.CsmThreatsAgentRuleActionsSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60f020d2a8ed25e948beb0b0bb09cf3c51faae822c051ae92da7d8b7d6cda654)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAppend")
    def reset_append(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppend", []))

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="appendInput")
    def append_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "appendInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="append")
    def append(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "append"))

    @append.setter
    def append(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93cd94d34b2e3c84f3ac73bd9ac4b038fe4a071837c0ae73973efd5359b980cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "append", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56070783ca3e0dd01ae5a856939371ada6160eb6a3f73e97888f846f99871f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0abd15e519da05da51565f94660e1c7c0318a56f7cd6bc6061c2ee87f6f50a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f0dd20e7677d422afa5e666911bd62d64c361d6041721c247352a243069120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab17ffa2888d6bd823aef40133cb870ea986830e78726625d3d20d2334033692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19252961041ee99f71a24ff49833ff18c4af77b03f5c746ad805e9ff447ccc76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6fa1e68c138b688de199bf42076dbcd7196c9f2b8f523c706b24a777043f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActionsSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActionsSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActionsSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db63e3ff2f996bb63af1ee4c816b64bce56f1dc8f7783d3d78279cb65eac7c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.csmThreatsAgentRule.CsmThreatsAgentRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "expression": "expression",
        "name": "name",
        "actions": "actions",
        "description": "description",
        "enabled": "enabled",
        "policy_id": "policyId",
        "product_tags": "productTags",
    },
)
class CsmThreatsAgentRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        expression: builtins.str,
        name: builtins.str,
        actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CsmThreatsAgentRuleActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        policy_id: typing.Optional[builtins.str] = None,
        product_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param expression: The SECL expression of the Agent rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#expression CsmThreatsAgentRule#expression}
        :param name: The name of the Agent rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#name CsmThreatsAgentRule#name}
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#actions CsmThreatsAgentRule#actions}
        :param description: A description for the Agent rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#description CsmThreatsAgentRule#description}
        :param enabled: Indicates whether the Agent rule is enabled. Must not be used without policy_id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#enabled CsmThreatsAgentRule#enabled}
        :param policy_id: The ID of the agent policy in which the rule is saved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#policy_id CsmThreatsAgentRule#policy_id}
        :param product_tags: The list of product tags associated with the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#product_tags CsmThreatsAgentRule#product_tags}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579bfb26f6a8a300ae1e7735ccec346e70b8bd06e57fee0a47521d386411d5ba)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument product_tags", value=product_tags, expected_type=type_hints["product_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
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
        if actions is not None:
            self._values["actions"] = actions
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if policy_id is not None:
            self._values["policy_id"] = policy_id
        if product_tags is not None:
            self._values["product_tags"] = product_tags

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
    def expression(self) -> builtins.str:
        '''The SECL expression of the Agent rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#expression CsmThreatsAgentRule#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Agent rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#name CsmThreatsAgentRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsmThreatsAgentRuleActions]]]:
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#actions CsmThreatsAgentRule#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsmThreatsAgentRuleActions]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the Agent rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#description CsmThreatsAgentRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the Agent rule is enabled. Must not be used without policy_id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#enabled CsmThreatsAgentRule#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def policy_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the agent policy in which the rule is saved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#policy_id CsmThreatsAgentRule#policy_id}
        '''
        result = self._values.get("policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of product tags associated with the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/csm_threats_agent_rule#product_tags CsmThreatsAgentRule#product_tags}
        '''
        result = self._values.get("product_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CsmThreatsAgentRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CsmThreatsAgentRule",
    "CsmThreatsAgentRuleActions",
    "CsmThreatsAgentRuleActionsHash",
    "CsmThreatsAgentRuleActionsHashOutputReference",
    "CsmThreatsAgentRuleActionsList",
    "CsmThreatsAgentRuleActionsOutputReference",
    "CsmThreatsAgentRuleActionsSet",
    "CsmThreatsAgentRuleActionsSetOutputReference",
    "CsmThreatsAgentRuleConfig",
]

publication.publish()

def _typecheckingstub__b96ea95987798ebe34b266a659f6ec41f8b098fb9529fe89edec606cc13595a2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    expression: builtins.str,
    name: builtins.str,
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CsmThreatsAgentRuleActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_id: typing.Optional[builtins.str] = None,
    product_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__c2deccf2359142e2d54b59add4f513f6363bcdee66b08685936a5709b5a74cca(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301046d350fa883557dd736657e730b5e8678ff9014b34f062ab31ff37aaa81a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CsmThreatsAgentRuleActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5fde6cf7444808fdb750098789edb5a2b279ce533877e20f40109af1623b3f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c621b1540ff48e629990ebd420538fb5c9f841503c36c9fbbd5362fef3b521(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30b33b27efb3178492b9e2b9fec2d7cd768ccfe24afe50fca8f81de0567c227(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f54374f4783f1c580e4c37aa4ac66656d91b41eaf9dff9fdda2cad635d51dc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11a5da0f05ab132930bf8cc33e184b64b5aa6266ade23595677682b5403d20b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3238c468d72fb4e032908fc928fd7746e42601ec069942826239f04698c1a405(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a9b6c6bf33438f36afd7fbe0567a64caad707a897718d9a0f2858a7f57ca17(
    *,
    hash: typing.Optional[typing.Union[CsmThreatsAgentRuleActionsHash, typing.Dict[builtins.str, typing.Any]]] = None,
    set: typing.Optional[typing.Union[CsmThreatsAgentRuleActionsSet, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de26ff18ed0e6490e9769b97f2684c6e46dff67e9e6858d3a4bf17a1928d53ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1f4ce93146da162e17e16fc897299cfd8798064f60dc60ec3f372e4ea26a3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActionsHash]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917b7434d2c31a602cc76dfab03997c4df7c72d04f3461b8f0e602a3a77c7475(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97421f0bf7a41d12b5c55c6d4674d04286b58f13a6d98879110cdff428f0eda2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9a6ea26ba463e0cdc857650e7341fc36ed11a2a1219b19ab4e8af81a562588(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de42408361fae6ee9076bafcf04f6cecec85bb011f2eb8317dcbb437a3d7880(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf4cca05eef7d52b3d6b9d27ec3d2f6c6edee31be42de55c6b95a583c45884f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a33db390cb4ab15bd473d19b6b3384e5ab15805b0d883722243dd2e6149817f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CsmThreatsAgentRuleActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e947937c063e209b96592a71b19afcd885104dd905a62ca6e372827a61ba9656(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1343771c6264c8443c7e3c1dd8e645f73f87e7792a6368c335aca44ea4451bee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d299fa96976ad086426af365bf7d80e33a6c0000d6cf4c63df9664936989f0(
    *,
    name: builtins.str,
    append: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    field: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    size: typing.Optional[jsii.Number] = None,
    ttl: typing.Optional[jsii.Number] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f020d2a8ed25e948beb0b0bb09cf3c51faae822c051ae92da7d8b7d6cda654(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cd94d34b2e3c84f3ac73bd9ac4b038fe4a071837c0ae73973efd5359b980cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56070783ca3e0dd01ae5a856939371ada6160eb6a3f73e97888f846f99871f54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0abd15e519da05da51565f94660e1c7c0318a56f7cd6bc6061c2ee87f6f50a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f0dd20e7677d422afa5e666911bd62d64c361d6041721c247352a243069120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab17ffa2888d6bd823aef40133cb870ea986830e78726625d3d20d2334033692(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19252961041ee99f71a24ff49833ff18c4af77b03f5c746ad805e9ff447ccc76(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6fa1e68c138b688de199bf42076dbcd7196c9f2b8f523c706b24a777043f38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db63e3ff2f996bb63af1ee4c816b64bce56f1dc8f7783d3d78279cb65eac7c1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CsmThreatsAgentRuleActionsSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579bfb26f6a8a300ae1e7735ccec346e70b8bd06e57fee0a47521d386411d5ba(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    expression: builtins.str,
    name: builtins.str,
    actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CsmThreatsAgentRuleActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    policy_id: typing.Optional[builtins.str] = None,
    product_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
