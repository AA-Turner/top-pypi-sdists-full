r'''
# `github_organization_ruleset`

Refer to the Terraform Registry for docs: [`github_organization_ruleset`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset).
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


class OrganizationRuleset(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRuleset",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset github_organization_ruleset}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enforcement: builtins.str,
        name: builtins.str,
        rules: typing.Union["OrganizationRulesetRules", typing.Dict[builtins.str, typing.Any]],
        target: builtins.str,
        bypass_actors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrganizationRulesetBypassActors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        conditions: typing.Optional[typing.Union["OrganizationRulesetConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset github_organization_ruleset} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enforcement: Possible values for Enforcement are ``disabled``, ``active``, ``evaluate``. Note: ``evaluate`` is currently only supported for owners of type ``organization``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#enforcement OrganizationRuleset#enforcement}
        :param name: The name of the ruleset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#rules OrganizationRuleset#rules}
        :param target: Possible values are ``branch``, ``tag`` and ``push``. Note: The ``push`` target is in beta and is subject to change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#target OrganizationRuleset#target}
        :param bypass_actors: bypass_actors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#bypass_actors OrganizationRuleset#bypass_actors}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#conditions OrganizationRuleset#conditions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#id OrganizationRuleset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc5fb077bc6be64190681136dabf344a2dab20a78bc92b53f438d5d83786b824)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrganizationRulesetConfig(
            enforcement=enforcement,
            name=name,
            rules=rules,
            target=target,
            bypass_actors=bypass_actors,
            conditions=conditions,
            id=id,
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
        '''Generates CDKTF code for importing a OrganizationRuleset resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OrganizationRuleset to import.
        :param import_from_id: The id of the existing OrganizationRuleset that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OrganizationRuleset to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6ff98de80e6a4a348913e4a55df868d1695bf21970ba26ed6d339d98f81b6d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBypassActors")
    def put_bypass_actors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrganizationRulesetBypassActors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49f373669f4bd68e952a4755336447269c5f7ae8c2bb6589c2af1ff6762175f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBypassActors", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        *,
        ref_name: typing.Union["OrganizationRulesetConditionsRefName", typing.Dict[builtins.str, typing.Any]],
        repository_id: typing.Optional[typing.Sequence[jsii.Number]] = None,
        repository_name: typing.Optional[typing.Union["OrganizationRulesetConditionsRepositoryName", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ref_name: ref_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#ref_name OrganizationRuleset#ref_name}
        :param repository_id: The repository IDs that the ruleset applies to. One of these IDs must match for the condition to pass. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#repository_id OrganizationRuleset#repository_id}
        :param repository_name: repository_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#repository_name OrganizationRuleset#repository_name}
        '''
        value = OrganizationRulesetConditions(
            ref_name=ref_name,
            repository_id=repository_id,
            repository_name=repository_name,
        )

        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        *,
        branch_name_pattern: typing.Optional[typing.Union["OrganizationRulesetRulesBranchNamePattern", typing.Dict[builtins.str, typing.Any]]] = None,
        commit_author_email_pattern: typing.Optional[typing.Union["OrganizationRulesetRulesCommitAuthorEmailPattern", typing.Dict[builtins.str, typing.Any]]] = None,
        commit_message_pattern: typing.Optional[typing.Union["OrganizationRulesetRulesCommitMessagePattern", typing.Dict[builtins.str, typing.Any]]] = None,
        committer_email_pattern: typing.Optional[typing.Union["OrganizationRulesetRulesCommitterEmailPattern", typing.Dict[builtins.str, typing.Any]]] = None,
        creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        non_fast_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pull_request: typing.Optional[typing.Union["OrganizationRulesetRulesPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        required_code_scanning: typing.Optional[typing.Union["OrganizationRulesetRulesRequiredCodeScanning", typing.Dict[builtins.str, typing.Any]]] = None,
        required_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_signatures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_status_checks: typing.Optional[typing.Union["OrganizationRulesetRulesRequiredStatusChecks", typing.Dict[builtins.str, typing.Any]]] = None,
        required_workflows: typing.Optional[typing.Union["OrganizationRulesetRulesRequiredWorkflows", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_name_pattern: typing.Optional[typing.Union["OrganizationRulesetRulesTagNamePattern", typing.Dict[builtins.str, typing.Any]]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch_name_pattern: branch_name_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#branch_name_pattern OrganizationRuleset#branch_name_pattern}
        :param commit_author_email_pattern: commit_author_email_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#commit_author_email_pattern OrganizationRuleset#commit_author_email_pattern}
        :param commit_message_pattern: commit_message_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#commit_message_pattern OrganizationRuleset#commit_message_pattern}
        :param committer_email_pattern: committer_email_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#committer_email_pattern OrganizationRuleset#committer_email_pattern}
        :param creation: Only allow users with bypass permission to create matching refs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#creation OrganizationRuleset#creation}
        :param deletion: Only allow users with bypass permissions to delete matching refs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#deletion OrganizationRuleset#deletion}
        :param non_fast_forward: Prevent users with push access from force pushing to branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#non_fast_forward OrganizationRuleset#non_fast_forward}
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pull_request OrganizationRuleset#pull_request}
        :param required_code_scanning: required_code_scanning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_code_scanning OrganizationRuleset#required_code_scanning}
        :param required_linear_history: Prevent merge commits from being pushed to matching branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_linear_history OrganizationRuleset#required_linear_history}
        :param required_signatures: Commits pushed to matching branches must have verified signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_signatures OrganizationRuleset#required_signatures}
        :param required_status_checks: required_status_checks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_status_checks OrganizationRuleset#required_status_checks}
        :param required_workflows: required_workflows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_workflows OrganizationRuleset#required_workflows}
        :param tag_name_pattern: tag_name_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#tag_name_pattern OrganizationRuleset#tag_name_pattern}
        :param update: Only allow users with bypass permission to update matching refs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#update OrganizationRuleset#update}
        '''
        value = OrganizationRulesetRules(
            branch_name_pattern=branch_name_pattern,
            commit_author_email_pattern=commit_author_email_pattern,
            commit_message_pattern=commit_message_pattern,
            committer_email_pattern=committer_email_pattern,
            creation=creation,
            deletion=deletion,
            non_fast_forward=non_fast_forward,
            pull_request=pull_request,
            required_code_scanning=required_code_scanning,
            required_linear_history=required_linear_history,
            required_signatures=required_signatures,
            required_status_checks=required_status_checks,
            required_workflows=required_workflows,
            tag_name_pattern=tag_name_pattern,
            update=update,
        )

        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetBypassActors")
    def reset_bypass_actors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBypassActors", []))

    @jsii.member(jsii_name="resetConditions")
    def reset_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditions", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="bypassActors")
    def bypass_actors(self) -> "OrganizationRulesetBypassActorsList":
        return typing.cast("OrganizationRulesetBypassActorsList", jsii.get(self, "bypassActors"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "OrganizationRulesetConditionsOutputReference":
        return typing.cast("OrganizationRulesetConditionsOutputReference", jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeId"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "OrganizationRulesetRulesOutputReference":
        return typing.cast("OrganizationRulesetRulesOutputReference", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="rulesetId")
    def ruleset_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rulesetId"))

    @builtins.property
    @jsii.member(jsii_name="bypassActorsInput")
    def bypass_actors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetBypassActors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetBypassActors"]]], jsii.get(self, "bypassActorsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(self) -> typing.Optional["OrganizationRulesetConditions"]:
        return typing.cast(typing.Optional["OrganizationRulesetConditions"], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="enforcementInput")
    def enforcement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforcementInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(self) -> typing.Optional["OrganizationRulesetRules"]:
        return typing.cast(typing.Optional["OrganizationRulesetRules"], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="enforcement")
    def enforcement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforcement"))

    @enforcement.setter
    def enforcement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d3d64a69f5a2a364f13b298244c70541c7fd6490eb393a1b7e3c587ee2f27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37243be924fb15ab18747a8e337050a4cc2da36912c897233f0b69bc2b365a7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e944c9eaf971341521a034c08f59c842f31f8d4b21c480238082dc3e0cf1c40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5260980bd71bca6133344f4e5e5b41b04c33f0c38941fc15a870fe2d5aba2d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetBypassActors",
    jsii_struct_bases=[],
    name_mapping={
        "actor_id": "actorId",
        "actor_type": "actorType",
        "bypass_mode": "bypassMode",
    },
)
class OrganizationRulesetBypassActors:
    def __init__(
        self,
        *,
        actor_id: jsii.Number,
        actor_type: builtins.str,
        bypass_mode: builtins.str,
    ) -> None:
        '''
        :param actor_id: The ID of the actor that can bypass a ruleset. When ``actor_type`` is ``OrganizationAdmin``, this should be set to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#actor_id OrganizationRuleset#actor_id}
        :param actor_type: The type of actor that can bypass a ruleset. Can be one of: ``RepositoryRole``, ``Team``, ``Integration``, ``OrganizationAdmin``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#actor_type OrganizationRuleset#actor_type}
        :param bypass_mode: When the specified actor can bypass the ruleset. pull_request means that an actor can only bypass rules on pull requests. Can be one of: ``always``, ``pull_request``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#bypass_mode OrganizationRuleset#bypass_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171bcb85f36c9e4fc8105474b4c99f6153562a06a88854e69c4bedba915e7579)
            check_type(argname="argument actor_id", value=actor_id, expected_type=type_hints["actor_id"])
            check_type(argname="argument actor_type", value=actor_type, expected_type=type_hints["actor_type"])
            check_type(argname="argument bypass_mode", value=bypass_mode, expected_type=type_hints["bypass_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actor_id": actor_id,
            "actor_type": actor_type,
            "bypass_mode": bypass_mode,
        }

    @builtins.property
    def actor_id(self) -> jsii.Number:
        '''The ID of the actor that can bypass a ruleset.

        When ``actor_type`` is ``OrganizationAdmin``, this should be set to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#actor_id OrganizationRuleset#actor_id}
        '''
        result = self._values.get("actor_id")
        assert result is not None, "Required property 'actor_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def actor_type(self) -> builtins.str:
        '''The type of actor that can bypass a ruleset. Can be one of: ``RepositoryRole``, ``Team``, ``Integration``, ``OrganizationAdmin``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#actor_type OrganizationRuleset#actor_type}
        '''
        result = self._values.get("actor_type")
        assert result is not None, "Required property 'actor_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bypass_mode(self) -> builtins.str:
        '''When the specified actor can bypass the ruleset.

        pull_request means that an actor can only bypass rules on pull requests. Can be one of: ``always``, ``pull_request``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#bypass_mode OrganizationRuleset#bypass_mode}
        '''
        result = self._values.get("bypass_mode")
        assert result is not None, "Required property 'bypass_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetBypassActors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetBypassActorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetBypassActorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69c7f0010cb248f1723fcba91209d0d4c9a95c3d419879043cbcd187ea48cc45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrganizationRulesetBypassActorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b830714aa7b6af5121e18ab3c9676607bb331768adf2f9dcde30d02f3903d50)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrganizationRulesetBypassActorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f03cd90d2658709264994b93fa135988f3c4312ec30cd7975c39ed9475657d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21b32e8eaeefc8047e53199bc68be333daddd7c21780777fd5c6e5d5e9d5a987)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f94c116c445dd2eaa918570dbb614d827c8f773216db4feb262140e8c418d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetBypassActors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetBypassActors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetBypassActors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8185bcdc9b98254e82f9eeb572d57e2c686f1300916551888eec4717651672c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrganizationRulesetBypassActorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetBypassActorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__738a6d7263a7debf64ec3dabd7f56f83b394b4e0bf89b2330016fe178a50bdc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actorIdInput")
    def actor_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "actorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="actorTypeInput")
    def actor_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="bypassModeInput")
    def bypass_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bypassModeInput"))

    @builtins.property
    @jsii.member(jsii_name="actorId")
    def actor_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "actorId"))

    @actor_id.setter
    def actor_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52d44debad1e15a30c957747d930694159b8405b3f4885aece43cdaf86bf689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="actorType")
    def actor_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actorType"))

    @actor_type.setter
    def actor_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8922731231bbcfc8ddc0779a0805c0934ba4b8ee4482a69943a34351a18f750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bypassMode")
    def bypass_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bypassMode"))

    @bypass_mode.setter
    def bypass_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a14542ebb5ca2183a9e61b87d7c7583e92e9c2fd486ccaf21a79064ae70ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bypassMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetBypassActors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetBypassActors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetBypassActors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715d43bb5bbead01193bb6437541b657e9444f112dea47c0a5b6facae6832e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetConditions",
    jsii_struct_bases=[],
    name_mapping={
        "ref_name": "refName",
        "repository_id": "repositoryId",
        "repository_name": "repositoryName",
    },
)
class OrganizationRulesetConditions:
    def __init__(
        self,
        *,
        ref_name: typing.Union["OrganizationRulesetConditionsRefName", typing.Dict[builtins.str, typing.Any]],
        repository_id: typing.Optional[typing.Sequence[jsii.Number]] = None,
        repository_name: typing.Optional[typing.Union["OrganizationRulesetConditionsRepositoryName", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ref_name: ref_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#ref_name OrganizationRuleset#ref_name}
        :param repository_id: The repository IDs that the ruleset applies to. One of these IDs must match for the condition to pass. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#repository_id OrganizationRuleset#repository_id}
        :param repository_name: repository_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#repository_name OrganizationRuleset#repository_name}
        '''
        if isinstance(ref_name, dict):
            ref_name = OrganizationRulesetConditionsRefName(**ref_name)
        if isinstance(repository_name, dict):
            repository_name = OrganizationRulesetConditionsRepositoryName(**repository_name)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c28ea2127e2c083f212de90f5be612f0b955fb6faf6e4c6fd1ac40e4e4be6b)
            check_type(argname="argument ref_name", value=ref_name, expected_type=type_hints["ref_name"])
            check_type(argname="argument repository_id", value=repository_id, expected_type=type_hints["repository_id"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ref_name": ref_name,
        }
        if repository_id is not None:
            self._values["repository_id"] = repository_id
        if repository_name is not None:
            self._values["repository_name"] = repository_name

    @builtins.property
    def ref_name(self) -> "OrganizationRulesetConditionsRefName":
        '''ref_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#ref_name OrganizationRuleset#ref_name}
        '''
        result = self._values.get("ref_name")
        assert result is not None, "Required property 'ref_name' is missing"
        return typing.cast("OrganizationRulesetConditionsRefName", result)

    @builtins.property
    def repository_id(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The repository IDs that the ruleset applies to. One of these IDs must match for the condition to pass.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#repository_id OrganizationRuleset#repository_id}
        '''
        result = self._values.get("repository_id")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def repository_name(
        self,
    ) -> typing.Optional["OrganizationRulesetConditionsRepositoryName"]:
        '''repository_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#repository_name OrganizationRuleset#repository_name}
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional["OrganizationRulesetConditionsRepositoryName"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__615c753c57483beefd58357203599e417d0ca5f1d2e44988bc944be70a53fd0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRefName")
    def put_ref_name(
        self,
        *,
        exclude: typing.Sequence[builtins.str],
        include: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param exclude: Array of ref names or patterns to exclude. The condition will not pass if any of these patterns match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#exclude OrganizationRuleset#exclude}
        :param include: Array of ref names or patterns to include. One of these patterns must match for the condition to pass. Also accepts ``~DEFAULT_BRANCH`` to include the default branch or ``~ALL`` to include all branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#include OrganizationRuleset#include}
        '''
        value = OrganizationRulesetConditionsRefName(exclude=exclude, include=include)

        return typing.cast(None, jsii.invoke(self, "putRefName", [value]))

    @jsii.member(jsii_name="putRepositoryName")
    def put_repository_name(
        self,
        *,
        exclude: typing.Sequence[builtins.str],
        include: typing.Sequence[builtins.str],
        protected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param exclude: Array of repository names or patterns to exclude. The condition will not pass if any of these patterns match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#exclude OrganizationRuleset#exclude}
        :param include: Array of repository names or patterns to include. One of these patterns must match for the condition to pass. Also accepts ``~ALL`` to include all repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#include OrganizationRuleset#include}
        :param protected: Whether renaming of target repositories is prevented. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#protected OrganizationRuleset#protected}
        '''
        value = OrganizationRulesetConditionsRepositoryName(
            exclude=exclude, include=include, protected=protected
        )

        return typing.cast(None, jsii.invoke(self, "putRepositoryName", [value]))

    @jsii.member(jsii_name="resetRepositoryId")
    def reset_repository_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryId", []))

    @jsii.member(jsii_name="resetRepositoryName")
    def reset_repository_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryName", []))

    @builtins.property
    @jsii.member(jsii_name="refName")
    def ref_name(self) -> "OrganizationRulesetConditionsRefNameOutputReference":
        return typing.cast("OrganizationRulesetConditionsRefNameOutputReference", jsii.get(self, "refName"))

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(
        self,
    ) -> "OrganizationRulesetConditionsRepositoryNameOutputReference":
        return typing.cast("OrganizationRulesetConditionsRepositoryNameOutputReference", jsii.get(self, "repositoryName"))

    @builtins.property
    @jsii.member(jsii_name="refNameInput")
    def ref_name_input(self) -> typing.Optional["OrganizationRulesetConditionsRefName"]:
        return typing.cast(typing.Optional["OrganizationRulesetConditionsRefName"], jsii.get(self, "refNameInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryIdInput")
    def repository_id_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "repositoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryNameInput")
    def repository_name_input(
        self,
    ) -> typing.Optional["OrganizationRulesetConditionsRepositoryName"]:
        return typing.cast(typing.Optional["OrganizationRulesetConditionsRepositoryName"], jsii.get(self, "repositoryNameInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryId")
    def repository_id(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "repositoryId"))

    @repository_id.setter
    def repository_id(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f329cf75c2515a8327a8a561e60eb4cf00546e3bd8a75c4855191fba89242a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrganizationRulesetConditions]:
        return typing.cast(typing.Optional[OrganizationRulesetConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationRulesetConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f8aac87b82c996f3cd2bb7a5ca561424c8380116b2efee2e0460f77a3a7b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetConditionsRefName",
    jsii_struct_bases=[],
    name_mapping={"exclude": "exclude", "include": "include"},
)
class OrganizationRulesetConditionsRefName:
    def __init__(
        self,
        *,
        exclude: typing.Sequence[builtins.str],
        include: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param exclude: Array of ref names or patterns to exclude. The condition will not pass if any of these patterns match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#exclude OrganizationRuleset#exclude}
        :param include: Array of ref names or patterns to include. One of these patterns must match for the condition to pass. Also accepts ``~DEFAULT_BRANCH`` to include the default branch or ``~ALL`` to include all branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#include OrganizationRuleset#include}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a47a657e5128740f328c06455c50e0488f40951acc92b9125753d74b266a565)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exclude": exclude,
            "include": include,
        }

    @builtins.property
    def exclude(self) -> typing.List[builtins.str]:
        '''Array of ref names or patterns to exclude. The condition will not pass if any of these patterns match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#exclude OrganizationRuleset#exclude}
        '''
        result = self._values.get("exclude")
        assert result is not None, "Required property 'exclude' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def include(self) -> typing.List[builtins.str]:
        '''Array of ref names or patterns to include.

        One of these patterns must match for the condition to pass. Also accepts ``~DEFAULT_BRANCH`` to include the default branch or ``~ALL`` to include all branches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#include OrganizationRuleset#include}
        '''
        result = self._values.get("include")
        assert result is not None, "Required property 'include' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetConditionsRefName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetConditionsRefNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetConditionsRefNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a51b56b89983bfc4bb977f3f3f6c8a1697841d8c8b0979bc09aac2542bae4e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="excludeInput")
    def exclude_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInput")
    def include_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeInput"))

    @builtins.property
    @jsii.member(jsii_name="exclude")
    def exclude(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclude"))

    @exclude.setter
    def exclude(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e06f03a7be4396cb3a20277609fcb96cdef2b64e7a8544502a9573b518fe49df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "include"))

    @include.setter
    def include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493f67835dab90fa79d583548d05b1158d6d6b5892392471aa8629acaaadbe68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrganizationRulesetConditionsRefName]:
        return typing.cast(typing.Optional[OrganizationRulesetConditionsRefName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationRulesetConditionsRefName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d84f759664f5a5134f2c3d8d8e4e7d28eb3e24ffbc19682fcb1e9d441ebd1a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetConditionsRepositoryName",
    jsii_struct_bases=[],
    name_mapping={
        "exclude": "exclude",
        "include": "include",
        "protected": "protected",
    },
)
class OrganizationRulesetConditionsRepositoryName:
    def __init__(
        self,
        *,
        exclude: typing.Sequence[builtins.str],
        include: typing.Sequence[builtins.str],
        protected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param exclude: Array of repository names or patterns to exclude. The condition will not pass if any of these patterns match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#exclude OrganizationRuleset#exclude}
        :param include: Array of repository names or patterns to include. One of these patterns must match for the condition to pass. Also accepts ``~ALL`` to include all repositories. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#include OrganizationRuleset#include}
        :param protected: Whether renaming of target repositories is prevented. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#protected OrganizationRuleset#protected}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7f5d26c86b9c559386d286b2d09e3f548da9627e7101137a95bc50ea363f16)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            check_type(argname="argument protected", value=protected, expected_type=type_hints["protected"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exclude": exclude,
            "include": include,
        }
        if protected is not None:
            self._values["protected"] = protected

    @builtins.property
    def exclude(self) -> typing.List[builtins.str]:
        '''Array of repository names or patterns to exclude. The condition will not pass if any of these patterns match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#exclude OrganizationRuleset#exclude}
        '''
        result = self._values.get("exclude")
        assert result is not None, "Required property 'exclude' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def include(self) -> typing.List[builtins.str]:
        '''Array of repository names or patterns to include.

        One of these patterns must match for the condition to pass. Also accepts ``~ALL`` to include all repositories.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#include OrganizationRuleset#include}
        '''
        result = self._values.get("include")
        assert result is not None, "Required property 'include' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def protected(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether renaming of target repositories is prevented.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#protected OrganizationRuleset#protected}
        '''
        result = self._values.get("protected")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetConditionsRepositoryName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetConditionsRepositoryNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetConditionsRepositoryNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee985c769e49ab767c1f355fcdd90b767abd2a538e73418cfaf01cf87ca32a64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProtected")
    def reset_protected(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtected", []))

    @builtins.property
    @jsii.member(jsii_name="excludeInput")
    def exclude_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInput")
    def include_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includeInput"))

    @builtins.property
    @jsii.member(jsii_name="protectedInput")
    def protected_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "protectedInput"))

    @builtins.property
    @jsii.member(jsii_name="exclude")
    def exclude(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclude"))

    @exclude.setter
    def exclude(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe28a57b17b48e0b7272fc17454ee7d3e775e07d9e6cd9c76e40912a7afb0313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "include"))

    @include.setter
    def include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93160239ebf0ba2de2a9143bdf2b4f929ccedf216b094cf3ed12df266808dc5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protected")
    def protected(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "protected"))

    @protected.setter
    def protected(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3795973b2d630175361b1b7042bd51e06156c3c710eaa8db06ddb97fcacad6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protected", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrganizationRulesetConditionsRepositoryName]:
        return typing.cast(typing.Optional[OrganizationRulesetConditionsRepositoryName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationRulesetConditionsRepositoryName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08267960101db6648fc9279d42bf1423c1411f4d7faff5c3f545ada823f5850d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "enforcement": "enforcement",
        "name": "name",
        "rules": "rules",
        "target": "target",
        "bypass_actors": "bypassActors",
        "conditions": "conditions",
        "id": "id",
    },
)
class OrganizationRulesetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        enforcement: builtins.str,
        name: builtins.str,
        rules: typing.Union["OrganizationRulesetRules", typing.Dict[builtins.str, typing.Any]],
        target: builtins.str,
        bypass_actors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrganizationRulesetBypassActors, typing.Dict[builtins.str, typing.Any]]]]] = None,
        conditions: typing.Optional[typing.Union[OrganizationRulesetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enforcement: Possible values for Enforcement are ``disabled``, ``active``, ``evaluate``. Note: ``evaluate`` is currently only supported for owners of type ``organization``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#enforcement OrganizationRuleset#enforcement}
        :param name: The name of the ruleset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#rules OrganizationRuleset#rules}
        :param target: Possible values are ``branch``, ``tag`` and ``push``. Note: The ``push`` target is in beta and is subject to change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#target OrganizationRuleset#target}
        :param bypass_actors: bypass_actors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#bypass_actors OrganizationRuleset#bypass_actors}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#conditions OrganizationRuleset#conditions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#id OrganizationRuleset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(rules, dict):
            rules = OrganizationRulesetRules(**rules)
        if isinstance(conditions, dict):
            conditions = OrganizationRulesetConditions(**conditions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d508c17eb6da5e61ecab2ed862f3910d061c23e0dc5bb2f0734a4f232d332bb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enforcement", value=enforcement, expected_type=type_hints["enforcement"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument bypass_actors", value=bypass_actors, expected_type=type_hints["bypass_actors"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enforcement": enforcement,
            "name": name,
            "rules": rules,
            "target": target,
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
        if bypass_actors is not None:
            self._values["bypass_actors"] = bypass_actors
        if conditions is not None:
            self._values["conditions"] = conditions
        if id is not None:
            self._values["id"] = id

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
    def enforcement(self) -> builtins.str:
        '''Possible values for Enforcement are ``disabled``, ``active``, ``evaluate``. Note: ``evaluate`` is currently only supported for owners of type ``organization``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#enforcement OrganizationRuleset#enforcement}
        '''
        result = self._values.get("enforcement")
        assert result is not None, "Required property 'enforcement' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the ruleset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(self) -> "OrganizationRulesetRules":
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#rules OrganizationRuleset#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast("OrganizationRulesetRules", result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Possible values are ``branch``, ``tag`` and ``push``. Note: The ``push`` target is in beta and is subject to change.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#target OrganizationRuleset#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bypass_actors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetBypassActors]]]:
        '''bypass_actors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#bypass_actors OrganizationRuleset#bypass_actors}
        '''
        result = self._values.get("bypass_actors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetBypassActors]]], result)

    @builtins.property
    def conditions(self) -> typing.Optional[OrganizationRulesetConditions]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#conditions OrganizationRuleset#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[OrganizationRulesetConditions], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#id OrganizationRuleset#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRules",
    jsii_struct_bases=[],
    name_mapping={
        "branch_name_pattern": "branchNamePattern",
        "commit_author_email_pattern": "commitAuthorEmailPattern",
        "commit_message_pattern": "commitMessagePattern",
        "committer_email_pattern": "committerEmailPattern",
        "creation": "creation",
        "deletion": "deletion",
        "non_fast_forward": "nonFastForward",
        "pull_request": "pullRequest",
        "required_code_scanning": "requiredCodeScanning",
        "required_linear_history": "requiredLinearHistory",
        "required_signatures": "requiredSignatures",
        "required_status_checks": "requiredStatusChecks",
        "required_workflows": "requiredWorkflows",
        "tag_name_pattern": "tagNamePattern",
        "update": "update",
    },
)
class OrganizationRulesetRules:
    def __init__(
        self,
        *,
        branch_name_pattern: typing.Optional[typing.Union["OrganizationRulesetRulesBranchNamePattern", typing.Dict[builtins.str, typing.Any]]] = None,
        commit_author_email_pattern: typing.Optional[typing.Union["OrganizationRulesetRulesCommitAuthorEmailPattern", typing.Dict[builtins.str, typing.Any]]] = None,
        commit_message_pattern: typing.Optional[typing.Union["OrganizationRulesetRulesCommitMessagePattern", typing.Dict[builtins.str, typing.Any]]] = None,
        committer_email_pattern: typing.Optional[typing.Union["OrganizationRulesetRulesCommitterEmailPattern", typing.Dict[builtins.str, typing.Any]]] = None,
        creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        non_fast_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pull_request: typing.Optional[typing.Union["OrganizationRulesetRulesPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        required_code_scanning: typing.Optional[typing.Union["OrganizationRulesetRulesRequiredCodeScanning", typing.Dict[builtins.str, typing.Any]]] = None,
        required_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_signatures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_status_checks: typing.Optional[typing.Union["OrganizationRulesetRulesRequiredStatusChecks", typing.Dict[builtins.str, typing.Any]]] = None,
        required_workflows: typing.Optional[typing.Union["OrganizationRulesetRulesRequiredWorkflows", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_name_pattern: typing.Optional[typing.Union["OrganizationRulesetRulesTagNamePattern", typing.Dict[builtins.str, typing.Any]]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch_name_pattern: branch_name_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#branch_name_pattern OrganizationRuleset#branch_name_pattern}
        :param commit_author_email_pattern: commit_author_email_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#commit_author_email_pattern OrganizationRuleset#commit_author_email_pattern}
        :param commit_message_pattern: commit_message_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#commit_message_pattern OrganizationRuleset#commit_message_pattern}
        :param committer_email_pattern: committer_email_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#committer_email_pattern OrganizationRuleset#committer_email_pattern}
        :param creation: Only allow users with bypass permission to create matching refs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#creation OrganizationRuleset#creation}
        :param deletion: Only allow users with bypass permissions to delete matching refs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#deletion OrganizationRuleset#deletion}
        :param non_fast_forward: Prevent users with push access from force pushing to branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#non_fast_forward OrganizationRuleset#non_fast_forward}
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pull_request OrganizationRuleset#pull_request}
        :param required_code_scanning: required_code_scanning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_code_scanning OrganizationRuleset#required_code_scanning}
        :param required_linear_history: Prevent merge commits from being pushed to matching branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_linear_history OrganizationRuleset#required_linear_history}
        :param required_signatures: Commits pushed to matching branches must have verified signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_signatures OrganizationRuleset#required_signatures}
        :param required_status_checks: required_status_checks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_status_checks OrganizationRuleset#required_status_checks}
        :param required_workflows: required_workflows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_workflows OrganizationRuleset#required_workflows}
        :param tag_name_pattern: tag_name_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#tag_name_pattern OrganizationRuleset#tag_name_pattern}
        :param update: Only allow users with bypass permission to update matching refs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#update OrganizationRuleset#update}
        '''
        if isinstance(branch_name_pattern, dict):
            branch_name_pattern = OrganizationRulesetRulesBranchNamePattern(**branch_name_pattern)
        if isinstance(commit_author_email_pattern, dict):
            commit_author_email_pattern = OrganizationRulesetRulesCommitAuthorEmailPattern(**commit_author_email_pattern)
        if isinstance(commit_message_pattern, dict):
            commit_message_pattern = OrganizationRulesetRulesCommitMessagePattern(**commit_message_pattern)
        if isinstance(committer_email_pattern, dict):
            committer_email_pattern = OrganizationRulesetRulesCommitterEmailPattern(**committer_email_pattern)
        if isinstance(pull_request, dict):
            pull_request = OrganizationRulesetRulesPullRequest(**pull_request)
        if isinstance(required_code_scanning, dict):
            required_code_scanning = OrganizationRulesetRulesRequiredCodeScanning(**required_code_scanning)
        if isinstance(required_status_checks, dict):
            required_status_checks = OrganizationRulesetRulesRequiredStatusChecks(**required_status_checks)
        if isinstance(required_workflows, dict):
            required_workflows = OrganizationRulesetRulesRequiredWorkflows(**required_workflows)
        if isinstance(tag_name_pattern, dict):
            tag_name_pattern = OrganizationRulesetRulesTagNamePattern(**tag_name_pattern)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a0737e599ea67c04f6e2447a3ace44823d6b435f72c4f6773256687d56c13c)
            check_type(argname="argument branch_name_pattern", value=branch_name_pattern, expected_type=type_hints["branch_name_pattern"])
            check_type(argname="argument commit_author_email_pattern", value=commit_author_email_pattern, expected_type=type_hints["commit_author_email_pattern"])
            check_type(argname="argument commit_message_pattern", value=commit_message_pattern, expected_type=type_hints["commit_message_pattern"])
            check_type(argname="argument committer_email_pattern", value=committer_email_pattern, expected_type=type_hints["committer_email_pattern"])
            check_type(argname="argument creation", value=creation, expected_type=type_hints["creation"])
            check_type(argname="argument deletion", value=deletion, expected_type=type_hints["deletion"])
            check_type(argname="argument non_fast_forward", value=non_fast_forward, expected_type=type_hints["non_fast_forward"])
            check_type(argname="argument pull_request", value=pull_request, expected_type=type_hints["pull_request"])
            check_type(argname="argument required_code_scanning", value=required_code_scanning, expected_type=type_hints["required_code_scanning"])
            check_type(argname="argument required_linear_history", value=required_linear_history, expected_type=type_hints["required_linear_history"])
            check_type(argname="argument required_signatures", value=required_signatures, expected_type=type_hints["required_signatures"])
            check_type(argname="argument required_status_checks", value=required_status_checks, expected_type=type_hints["required_status_checks"])
            check_type(argname="argument required_workflows", value=required_workflows, expected_type=type_hints["required_workflows"])
            check_type(argname="argument tag_name_pattern", value=tag_name_pattern, expected_type=type_hints["tag_name_pattern"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branch_name_pattern is not None:
            self._values["branch_name_pattern"] = branch_name_pattern
        if commit_author_email_pattern is not None:
            self._values["commit_author_email_pattern"] = commit_author_email_pattern
        if commit_message_pattern is not None:
            self._values["commit_message_pattern"] = commit_message_pattern
        if committer_email_pattern is not None:
            self._values["committer_email_pattern"] = committer_email_pattern
        if creation is not None:
            self._values["creation"] = creation
        if deletion is not None:
            self._values["deletion"] = deletion
        if non_fast_forward is not None:
            self._values["non_fast_forward"] = non_fast_forward
        if pull_request is not None:
            self._values["pull_request"] = pull_request
        if required_code_scanning is not None:
            self._values["required_code_scanning"] = required_code_scanning
        if required_linear_history is not None:
            self._values["required_linear_history"] = required_linear_history
        if required_signatures is not None:
            self._values["required_signatures"] = required_signatures
        if required_status_checks is not None:
            self._values["required_status_checks"] = required_status_checks
        if required_workflows is not None:
            self._values["required_workflows"] = required_workflows
        if tag_name_pattern is not None:
            self._values["tag_name_pattern"] = tag_name_pattern
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def branch_name_pattern(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesBranchNamePattern"]:
        '''branch_name_pattern block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#branch_name_pattern OrganizationRuleset#branch_name_pattern}
        '''
        result = self._values.get("branch_name_pattern")
        return typing.cast(typing.Optional["OrganizationRulesetRulesBranchNamePattern"], result)

    @builtins.property
    def commit_author_email_pattern(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesCommitAuthorEmailPattern"]:
        '''commit_author_email_pattern block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#commit_author_email_pattern OrganizationRuleset#commit_author_email_pattern}
        '''
        result = self._values.get("commit_author_email_pattern")
        return typing.cast(typing.Optional["OrganizationRulesetRulesCommitAuthorEmailPattern"], result)

    @builtins.property
    def commit_message_pattern(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesCommitMessagePattern"]:
        '''commit_message_pattern block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#commit_message_pattern OrganizationRuleset#commit_message_pattern}
        '''
        result = self._values.get("commit_message_pattern")
        return typing.cast(typing.Optional["OrganizationRulesetRulesCommitMessagePattern"], result)

    @builtins.property
    def committer_email_pattern(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesCommitterEmailPattern"]:
        '''committer_email_pattern block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#committer_email_pattern OrganizationRuleset#committer_email_pattern}
        '''
        result = self._values.get("committer_email_pattern")
        return typing.cast(typing.Optional["OrganizationRulesetRulesCommitterEmailPattern"], result)

    @builtins.property
    def creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only allow users with bypass permission to create matching refs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#creation OrganizationRuleset#creation}
        '''
        result = self._values.get("creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only allow users with bypass permissions to delete matching refs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#deletion OrganizationRuleset#deletion}
        '''
        result = self._values.get("deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def non_fast_forward(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent users with push access from force pushing to branches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#non_fast_forward OrganizationRuleset#non_fast_forward}
        '''
        result = self._values.get("non_fast_forward")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pull_request(self) -> typing.Optional["OrganizationRulesetRulesPullRequest"]:
        '''pull_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pull_request OrganizationRuleset#pull_request}
        '''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional["OrganizationRulesetRulesPullRequest"], result)

    @builtins.property
    def required_code_scanning(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesRequiredCodeScanning"]:
        '''required_code_scanning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_code_scanning OrganizationRuleset#required_code_scanning}
        '''
        result = self._values.get("required_code_scanning")
        return typing.cast(typing.Optional["OrganizationRulesetRulesRequiredCodeScanning"], result)

    @builtins.property
    def required_linear_history(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent merge commits from being pushed to matching branches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_linear_history OrganizationRuleset#required_linear_history}
        '''
        result = self._values.get("required_linear_history")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_signatures(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Commits pushed to matching branches must have verified signatures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_signatures OrganizationRuleset#required_signatures}
        '''
        result = self._values.get("required_signatures")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_status_checks(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesRequiredStatusChecks"]:
        '''required_status_checks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_status_checks OrganizationRuleset#required_status_checks}
        '''
        result = self._values.get("required_status_checks")
        return typing.cast(typing.Optional["OrganizationRulesetRulesRequiredStatusChecks"], result)

    @builtins.property
    def required_workflows(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesRequiredWorkflows"]:
        '''required_workflows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_workflows OrganizationRuleset#required_workflows}
        '''
        result = self._values.get("required_workflows")
        return typing.cast(typing.Optional["OrganizationRulesetRulesRequiredWorkflows"], result)

    @builtins.property
    def tag_name_pattern(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesTagNamePattern"]:
        '''tag_name_pattern block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#tag_name_pattern OrganizationRuleset#tag_name_pattern}
        '''
        result = self._values.get("tag_name_pattern")
        return typing.cast(typing.Optional["OrganizationRulesetRulesTagNamePattern"], result)

    @builtins.property
    def update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only allow users with bypass permission to update matching refs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#update OrganizationRuleset#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesBranchNamePattern",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "pattern": "pattern",
        "name": "name",
        "negate": "negate",
    },
)
class OrganizationRulesetRulesBranchNamePattern:
    def __init__(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d8617c4ab8159b74c2eac3cbc9edc3a30a7549d307611dea71f210e465f4636)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "pattern": pattern,
        }
        if name is not None:
            self._values["name"] = name
        if negate is not None:
            self._values["negate"] = negate

    @builtins.property
    def operator(self) -> builtins.str:
        '''The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''The pattern to match with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''How this rule will appear to users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the rule will fail if the pattern matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRulesBranchNamePattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetRulesBranchNamePatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesBranchNamePatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__736205d481bdc338f34726bc389f1755697a398597c0ce6cc131ac3c8e690b3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7700db1e87052662ea46011404b8db39512906c7d9b037da7201281c3693bf5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ffee740c3fa39c9a63bd02a8cd2085659f9063f94d7b4fcdb0be05ab25fe18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30a127d903ff08e2bd7cf80933e6a5225a2d8b2a7c0388f6d8d7469af06c32d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86709dc8051d95ddfd2fde814e715885b0e54fec1d3c933144df9f5598efd0a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrganizationRulesetRulesBranchNamePattern]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesBranchNamePattern], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationRulesetRulesBranchNamePattern],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585b95d64112de10439100cf71a3864c8b2f607196f7da86c89cc79db6ea96da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesCommitAuthorEmailPattern",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "pattern": "pattern",
        "name": "name",
        "negate": "negate",
    },
)
class OrganizationRulesetRulesCommitAuthorEmailPattern:
    def __init__(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a8999aab61fe9ccbdff23e5804e0b7bd6247a62f3d2044a9d278f414d237fb8)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "pattern": pattern,
        }
        if name is not None:
            self._values["name"] = name
        if negate is not None:
            self._values["negate"] = negate

    @builtins.property
    def operator(self) -> builtins.str:
        '''The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''The pattern to match with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''How this rule will appear to users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the rule will fail if the pattern matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRulesCommitAuthorEmailPattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetRulesCommitAuthorEmailPatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesCommitAuthorEmailPatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16e2a547267584c203bdb913733b14eab5b232784852ede88ac19822d748d600)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152eaca7db9c704deff2ef1279c9fd0fd5cf7796af687ec29eb3c8fc4eec3eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148bf8c3ba90b15ca184a0952bd017f3bb6a1849f9aa0a14f6d3527e4fc64160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c46169928b76607f63b19a84569e25d5b3e4ce011d1f61f196521a08128fd2dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc3f91c359629c3458b4c7a696d15bd91bcc46d85b9f22ab060969a7e38ab92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrganizationRulesetRulesCommitAuthorEmailPattern]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesCommitAuthorEmailPattern], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationRulesetRulesCommitAuthorEmailPattern],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc94bc247157be6949334ba656ee9d9dd13e15ee871f41c742cb3d86e3086ea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesCommitMessagePattern",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "pattern": "pattern",
        "name": "name",
        "negate": "negate",
    },
)
class OrganizationRulesetRulesCommitMessagePattern:
    def __init__(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc0eca162b0ca4c9f47bb2a7fb627264e2c745e76a4b60bdc83e8520f9b7ad8)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "pattern": pattern,
        }
        if name is not None:
            self._values["name"] = name
        if negate is not None:
            self._values["negate"] = negate

    @builtins.property
    def operator(self) -> builtins.str:
        '''The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''The pattern to match with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''How this rule will appear to users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the rule will fail if the pattern matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRulesCommitMessagePattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetRulesCommitMessagePatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesCommitMessagePatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__760da561ae41501a4a070f405bf5554382e527d8b1d37fadac85602bdf262154)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601f3d0b46409f2abe4e68fa6f9664e4f3c3c8b4cbfc3a067dcfe4c3ff30cb98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebe83db5cdd3aec4bd0ddb378d76c6a96681927795b089d7f1199fdcbbb9319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ebf28d258c77d9ff9fe9de801aa930b713616566dfb5bd66a8462c73e6abca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c60c91a95cea162858b83e13f98337231f78fcfde91bb2a957f4de1e9cee28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrganizationRulesetRulesCommitMessagePattern]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesCommitMessagePattern], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationRulesetRulesCommitMessagePattern],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae8d38f026c6bfa55edf176569005fbe74d3e31d659f6f33deb5f4f5b8c0de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesCommitterEmailPattern",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "pattern": "pattern",
        "name": "name",
        "negate": "negate",
    },
)
class OrganizationRulesetRulesCommitterEmailPattern:
    def __init__(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e19d8418043602d4f6e8b990b0c668f0174df988b6b6edaad841fa209b8fd0)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "pattern": pattern,
        }
        if name is not None:
            self._values["name"] = name
        if negate is not None:
            self._values["negate"] = negate

    @builtins.property
    def operator(self) -> builtins.str:
        '''The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''The pattern to match with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''How this rule will appear to users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the rule will fail if the pattern matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRulesCommitterEmailPattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetRulesCommitterEmailPatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesCommitterEmailPatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc5df2033aea927396f3b15c8e77667e44d00787110483e0a223cad8d69d6b59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4271f5130bfd2b1f48da773eb524b5e9cb7cf70d5e99fd780c325cb16ab6da0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4da9f99b0b993d9ddf986ef5c0738c9683592bad332eb044b9e0a87ec4e2dd8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba27b35c8843f575617a82c71127310e824df77d04fd8257f9e9c450b064143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439f8dce8e417f357842e62e4d8e92d3959cb7d3adeea53a4c2d67953a3ec9a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrganizationRulesetRulesCommitterEmailPattern]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesCommitterEmailPattern], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationRulesetRulesCommitterEmailPattern],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0de0a44c5329a33775b0ee15a4abc3d4b1672ede251f623e5be8560a171e64a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrganizationRulesetRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df401dd5d366ab5be38f72d739e9bac0f560595d732b61f8be1f0e67dd02a997)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBranchNamePattern")
    def put_branch_name_pattern(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        value = OrganizationRulesetRulesBranchNamePattern(
            operator=operator, pattern=pattern, name=name, negate=negate
        )

        return typing.cast(None, jsii.invoke(self, "putBranchNamePattern", [value]))

    @jsii.member(jsii_name="putCommitAuthorEmailPattern")
    def put_commit_author_email_pattern(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        value = OrganizationRulesetRulesCommitAuthorEmailPattern(
            operator=operator, pattern=pattern, name=name, negate=negate
        )

        return typing.cast(None, jsii.invoke(self, "putCommitAuthorEmailPattern", [value]))

    @jsii.member(jsii_name="putCommitMessagePattern")
    def put_commit_message_pattern(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        value = OrganizationRulesetRulesCommitMessagePattern(
            operator=operator, pattern=pattern, name=name, negate=negate
        )

        return typing.cast(None, jsii.invoke(self, "putCommitMessagePattern", [value]))

    @jsii.member(jsii_name="putCommitterEmailPattern")
    def put_committer_email_pattern(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        value = OrganizationRulesetRulesCommitterEmailPattern(
            operator=operator, pattern=pattern, name=name, negate=negate
        )

        return typing.cast(None, jsii.invoke(self, "putCommitterEmailPattern", [value]))

    @jsii.member(jsii_name="putPullRequest")
    def put_pull_request(
        self,
        *,
        dismiss_stale_reviews_on_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_code_owner_review: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_approving_review_count: typing.Optional[jsii.Number] = None,
        required_review_thread_resolution: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_last_push_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dismiss_stale_reviews_on_push: New, reviewable commits pushed will dismiss previous pull request review approvals. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#dismiss_stale_reviews_on_push OrganizationRuleset#dismiss_stale_reviews_on_push}
        :param require_code_owner_review: Require an approving review in pull requests that modify files that have a designated code owner. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#require_code_owner_review OrganizationRuleset#require_code_owner_review}
        :param required_approving_review_count: The number of approving reviews that are required before a pull request can be merged. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_approving_review_count OrganizationRuleset#required_approving_review_count}
        :param required_review_thread_resolution: All conversations on code must be resolved before a pull request can be merged. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_review_thread_resolution OrganizationRuleset#required_review_thread_resolution}
        :param require_last_push_approval: Whether the most recent reviewable push must be approved by someone other than the person who pushed it. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#require_last_push_approval OrganizationRuleset#require_last_push_approval}
        '''
        value = OrganizationRulesetRulesPullRequest(
            dismiss_stale_reviews_on_push=dismiss_stale_reviews_on_push,
            require_code_owner_review=require_code_owner_review,
            required_approving_review_count=required_approving_review_count,
            required_review_thread_resolution=required_review_thread_resolution,
            require_last_push_approval=require_last_push_approval,
        )

        return typing.cast(None, jsii.invoke(self, "putPullRequest", [value]))

    @jsii.member(jsii_name="putRequiredCodeScanning")
    def put_required_code_scanning(
        self,
        *,
        required_code_scanning_tool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param required_code_scanning_tool: required_code_scanning_tool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_code_scanning_tool OrganizationRuleset#required_code_scanning_tool}
        '''
        value = OrganizationRulesetRulesRequiredCodeScanning(
            required_code_scanning_tool=required_code_scanning_tool
        )

        return typing.cast(None, jsii.invoke(self, "putRequiredCodeScanning", [value]))

    @jsii.member(jsii_name="putRequiredStatusChecks")
    def put_required_status_checks(
        self,
        *,
        required_check: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrganizationRulesetRulesRequiredStatusChecksRequiredCheck", typing.Dict[builtins.str, typing.Any]]]],
        strict_required_status_checks_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param required_check: required_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_check OrganizationRuleset#required_check}
        :param strict_required_status_checks_policy: Whether pull requests targeting a matching branch must be tested with the latest code. This setting will not take effect unless at least one status check is enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#strict_required_status_checks_policy OrganizationRuleset#strict_required_status_checks_policy}
        '''
        value = OrganizationRulesetRulesRequiredStatusChecks(
            required_check=required_check,
            strict_required_status_checks_policy=strict_required_status_checks_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putRequiredStatusChecks", [value]))

    @jsii.member(jsii_name="putRequiredWorkflows")
    def put_required_workflows(
        self,
        *,
        required_workflow: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param required_workflow: required_workflow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_workflow OrganizationRuleset#required_workflow}
        '''
        value = OrganizationRulesetRulesRequiredWorkflows(
            required_workflow=required_workflow
        )

        return typing.cast(None, jsii.invoke(self, "putRequiredWorkflows", [value]))

    @jsii.member(jsii_name="putTagNamePattern")
    def put_tag_name_pattern(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        value = OrganizationRulesetRulesTagNamePattern(
            operator=operator, pattern=pattern, name=name, negate=negate
        )

        return typing.cast(None, jsii.invoke(self, "putTagNamePattern", [value]))

    @jsii.member(jsii_name="resetBranchNamePattern")
    def reset_branch_name_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranchNamePattern", []))

    @jsii.member(jsii_name="resetCommitAuthorEmailPattern")
    def reset_commit_author_email_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitAuthorEmailPattern", []))

    @jsii.member(jsii_name="resetCommitMessagePattern")
    def reset_commit_message_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitMessagePattern", []))

    @jsii.member(jsii_name="resetCommitterEmailPattern")
    def reset_committer_email_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitterEmailPattern", []))

    @jsii.member(jsii_name="resetCreation")
    def reset_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreation", []))

    @jsii.member(jsii_name="resetDeletion")
    def reset_deletion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletion", []))

    @jsii.member(jsii_name="resetNonFastForward")
    def reset_non_fast_forward(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonFastForward", []))

    @jsii.member(jsii_name="resetPullRequest")
    def reset_pull_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullRequest", []))

    @jsii.member(jsii_name="resetRequiredCodeScanning")
    def reset_required_code_scanning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredCodeScanning", []))

    @jsii.member(jsii_name="resetRequiredLinearHistory")
    def reset_required_linear_history(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredLinearHistory", []))

    @jsii.member(jsii_name="resetRequiredSignatures")
    def reset_required_signatures(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredSignatures", []))

    @jsii.member(jsii_name="resetRequiredStatusChecks")
    def reset_required_status_checks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredStatusChecks", []))

    @jsii.member(jsii_name="resetRequiredWorkflows")
    def reset_required_workflows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredWorkflows", []))

    @jsii.member(jsii_name="resetTagNamePattern")
    def reset_tag_name_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagNamePattern", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="branchNamePattern")
    def branch_name_pattern(
        self,
    ) -> OrganizationRulesetRulesBranchNamePatternOutputReference:
        return typing.cast(OrganizationRulesetRulesBranchNamePatternOutputReference, jsii.get(self, "branchNamePattern"))

    @builtins.property
    @jsii.member(jsii_name="commitAuthorEmailPattern")
    def commit_author_email_pattern(
        self,
    ) -> OrganizationRulesetRulesCommitAuthorEmailPatternOutputReference:
        return typing.cast(OrganizationRulesetRulesCommitAuthorEmailPatternOutputReference, jsii.get(self, "commitAuthorEmailPattern"))

    @builtins.property
    @jsii.member(jsii_name="commitMessagePattern")
    def commit_message_pattern(
        self,
    ) -> OrganizationRulesetRulesCommitMessagePatternOutputReference:
        return typing.cast(OrganizationRulesetRulesCommitMessagePatternOutputReference, jsii.get(self, "commitMessagePattern"))

    @builtins.property
    @jsii.member(jsii_name="committerEmailPattern")
    def committer_email_pattern(
        self,
    ) -> OrganizationRulesetRulesCommitterEmailPatternOutputReference:
        return typing.cast(OrganizationRulesetRulesCommitterEmailPatternOutputReference, jsii.get(self, "committerEmailPattern"))

    @builtins.property
    @jsii.member(jsii_name="pullRequest")
    def pull_request(self) -> "OrganizationRulesetRulesPullRequestOutputReference":
        return typing.cast("OrganizationRulesetRulesPullRequestOutputReference", jsii.get(self, "pullRequest"))

    @builtins.property
    @jsii.member(jsii_name="requiredCodeScanning")
    def required_code_scanning(
        self,
    ) -> "OrganizationRulesetRulesRequiredCodeScanningOutputReference":
        return typing.cast("OrganizationRulesetRulesRequiredCodeScanningOutputReference", jsii.get(self, "requiredCodeScanning"))

    @builtins.property
    @jsii.member(jsii_name="requiredStatusChecks")
    def required_status_checks(
        self,
    ) -> "OrganizationRulesetRulesRequiredStatusChecksOutputReference":
        return typing.cast("OrganizationRulesetRulesRequiredStatusChecksOutputReference", jsii.get(self, "requiredStatusChecks"))

    @builtins.property
    @jsii.member(jsii_name="requiredWorkflows")
    def required_workflows(
        self,
    ) -> "OrganizationRulesetRulesRequiredWorkflowsOutputReference":
        return typing.cast("OrganizationRulesetRulesRequiredWorkflowsOutputReference", jsii.get(self, "requiredWorkflows"))

    @builtins.property
    @jsii.member(jsii_name="tagNamePattern")
    def tag_name_pattern(
        self,
    ) -> "OrganizationRulesetRulesTagNamePatternOutputReference":
        return typing.cast("OrganizationRulesetRulesTagNamePatternOutputReference", jsii.get(self, "tagNamePattern"))

    @builtins.property
    @jsii.member(jsii_name="branchNamePatternInput")
    def branch_name_pattern_input(
        self,
    ) -> typing.Optional[OrganizationRulesetRulesBranchNamePattern]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesBranchNamePattern], jsii.get(self, "branchNamePatternInput"))

    @builtins.property
    @jsii.member(jsii_name="commitAuthorEmailPatternInput")
    def commit_author_email_pattern_input(
        self,
    ) -> typing.Optional[OrganizationRulesetRulesCommitAuthorEmailPattern]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesCommitAuthorEmailPattern], jsii.get(self, "commitAuthorEmailPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="commitMessagePatternInput")
    def commit_message_pattern_input(
        self,
    ) -> typing.Optional[OrganizationRulesetRulesCommitMessagePattern]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesCommitMessagePattern], jsii.get(self, "commitMessagePatternInput"))

    @builtins.property
    @jsii.member(jsii_name="committerEmailPatternInput")
    def committer_email_pattern_input(
        self,
    ) -> typing.Optional[OrganizationRulesetRulesCommitterEmailPattern]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesCommitterEmailPattern], jsii.get(self, "committerEmailPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="creationInput")
    def creation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "creationInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionInput")
    def deletion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionInput"))

    @builtins.property
    @jsii.member(jsii_name="nonFastForwardInput")
    def non_fast_forward_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nonFastForwardInput"))

    @builtins.property
    @jsii.member(jsii_name="pullRequestInput")
    def pull_request_input(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesPullRequest"]:
        return typing.cast(typing.Optional["OrganizationRulesetRulesPullRequest"], jsii.get(self, "pullRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredCodeScanningInput")
    def required_code_scanning_input(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesRequiredCodeScanning"]:
        return typing.cast(typing.Optional["OrganizationRulesetRulesRequiredCodeScanning"], jsii.get(self, "requiredCodeScanningInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredLinearHistoryInput")
    def required_linear_history_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredLinearHistoryInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredSignaturesInput")
    def required_signatures_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredSignaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredStatusChecksInput")
    def required_status_checks_input(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesRequiredStatusChecks"]:
        return typing.cast(typing.Optional["OrganizationRulesetRulesRequiredStatusChecks"], jsii.get(self, "requiredStatusChecksInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredWorkflowsInput")
    def required_workflows_input(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesRequiredWorkflows"]:
        return typing.cast(typing.Optional["OrganizationRulesetRulesRequiredWorkflows"], jsii.get(self, "requiredWorkflowsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagNamePatternInput")
    def tag_name_pattern_input(
        self,
    ) -> typing.Optional["OrganizationRulesetRulesTagNamePattern"]:
        return typing.cast(typing.Optional["OrganizationRulesetRulesTagNamePattern"], jsii.get(self, "tagNamePatternInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="creation")
    def creation(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "creation"))

    @creation.setter
    def creation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09371a585154552be4005cf0094db635779f9ddef9a605cc46b80b31b147cf37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletion")
    def deletion(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletion"))

    @deletion.setter
    def deletion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c53412334f78e3e0d69594acf166c6761e0281d26352bc72bd7724eaed3a1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nonFastForward")
    def non_fast_forward(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nonFastForward"))

    @non_fast_forward.setter
    def non_fast_forward(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5a842819d0c1206e92d8b20409d2c77b9ffef04aeb27630ddaf140c36d8f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonFastForward", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredLinearHistory")
    def required_linear_history(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requiredLinearHistory"))

    @required_linear_history.setter
    def required_linear_history(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1158af716976767afdd04e159709de05466c86527d88c905a8944be175a2e3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredLinearHistory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredSignatures")
    def required_signatures(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requiredSignatures"))

    @required_signatures.setter
    def required_signatures(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc026c59ce66f9aa9eb7776bb08eb2e32c06d735352c174b27bd67251e6241b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredSignatures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "update"))

    @update.setter
    def update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bce960c939ea61b74ab4061d634a61f2842531a37adcb8fbfcd23d67e15671b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrganizationRulesetRules]:
        return typing.cast(typing.Optional[OrganizationRulesetRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OrganizationRulesetRules]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74df58f635f7f6bfa54572807a67ad25262b7d0e23acf149c57ff9e6302c6897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesPullRequest",
    jsii_struct_bases=[],
    name_mapping={
        "dismiss_stale_reviews_on_push": "dismissStaleReviewsOnPush",
        "require_code_owner_review": "requireCodeOwnerReview",
        "required_approving_review_count": "requiredApprovingReviewCount",
        "required_review_thread_resolution": "requiredReviewThreadResolution",
        "require_last_push_approval": "requireLastPushApproval",
    },
)
class OrganizationRulesetRulesPullRequest:
    def __init__(
        self,
        *,
        dismiss_stale_reviews_on_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_code_owner_review: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_approving_review_count: typing.Optional[jsii.Number] = None,
        required_review_thread_resolution: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_last_push_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dismiss_stale_reviews_on_push: New, reviewable commits pushed will dismiss previous pull request review approvals. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#dismiss_stale_reviews_on_push OrganizationRuleset#dismiss_stale_reviews_on_push}
        :param require_code_owner_review: Require an approving review in pull requests that modify files that have a designated code owner. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#require_code_owner_review OrganizationRuleset#require_code_owner_review}
        :param required_approving_review_count: The number of approving reviews that are required before a pull request can be merged. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_approving_review_count OrganizationRuleset#required_approving_review_count}
        :param required_review_thread_resolution: All conversations on code must be resolved before a pull request can be merged. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_review_thread_resolution OrganizationRuleset#required_review_thread_resolution}
        :param require_last_push_approval: Whether the most recent reviewable push must be approved by someone other than the person who pushed it. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#require_last_push_approval OrganizationRuleset#require_last_push_approval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a6ba266aa0d91b9124cda65218e40e2afd852239f6b33ba8806bbf10d4b854)
            check_type(argname="argument dismiss_stale_reviews_on_push", value=dismiss_stale_reviews_on_push, expected_type=type_hints["dismiss_stale_reviews_on_push"])
            check_type(argname="argument require_code_owner_review", value=require_code_owner_review, expected_type=type_hints["require_code_owner_review"])
            check_type(argname="argument required_approving_review_count", value=required_approving_review_count, expected_type=type_hints["required_approving_review_count"])
            check_type(argname="argument required_review_thread_resolution", value=required_review_thread_resolution, expected_type=type_hints["required_review_thread_resolution"])
            check_type(argname="argument require_last_push_approval", value=require_last_push_approval, expected_type=type_hints["require_last_push_approval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dismiss_stale_reviews_on_push is not None:
            self._values["dismiss_stale_reviews_on_push"] = dismiss_stale_reviews_on_push
        if require_code_owner_review is not None:
            self._values["require_code_owner_review"] = require_code_owner_review
        if required_approving_review_count is not None:
            self._values["required_approving_review_count"] = required_approving_review_count
        if required_review_thread_resolution is not None:
            self._values["required_review_thread_resolution"] = required_review_thread_resolution
        if require_last_push_approval is not None:
            self._values["require_last_push_approval"] = require_last_push_approval

    @builtins.property
    def dismiss_stale_reviews_on_push(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''New, reviewable commits pushed will dismiss previous pull request review approvals. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#dismiss_stale_reviews_on_push OrganizationRuleset#dismiss_stale_reviews_on_push}
        '''
        result = self._values.get("dismiss_stale_reviews_on_push")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_code_owner_review(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require an approving review in pull requests that modify files that have a designated code owner. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#require_code_owner_review OrganizationRuleset#require_code_owner_review}
        '''
        result = self._values.get("require_code_owner_review")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_approving_review_count(self) -> typing.Optional[jsii.Number]:
        '''The number of approving reviews that are required before a pull request can be merged. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_approving_review_count OrganizationRuleset#required_approving_review_count}
        '''
        result = self._values.get("required_approving_review_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def required_review_thread_resolution(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''All conversations on code must be resolved before a pull request can be merged. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_review_thread_resolution OrganizationRuleset#required_review_thread_resolution}
        '''
        result = self._values.get("required_review_thread_resolution")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_last_push_approval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the most recent reviewable push must be approved by someone other than the person who pushed it.

        Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#require_last_push_approval OrganizationRuleset#require_last_push_approval}
        '''
        result = self._values.get("require_last_push_approval")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRulesPullRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetRulesPullRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesPullRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__759c6aea629dae61ec9fd9262226a4e9c84052c21d53348801049e5f4c603516)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDismissStaleReviewsOnPush")
    def reset_dismiss_stale_reviews_on_push(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDismissStaleReviewsOnPush", []))

    @jsii.member(jsii_name="resetRequireCodeOwnerReview")
    def reset_require_code_owner_review(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireCodeOwnerReview", []))

    @jsii.member(jsii_name="resetRequiredApprovingReviewCount")
    def reset_required_approving_review_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredApprovingReviewCount", []))

    @jsii.member(jsii_name="resetRequiredReviewThreadResolution")
    def reset_required_review_thread_resolution(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredReviewThreadResolution", []))

    @jsii.member(jsii_name="resetRequireLastPushApproval")
    def reset_require_last_push_approval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireLastPushApproval", []))

    @builtins.property
    @jsii.member(jsii_name="dismissStaleReviewsOnPushInput")
    def dismiss_stale_reviews_on_push_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dismissStaleReviewsOnPushInput"))

    @builtins.property
    @jsii.member(jsii_name="requireCodeOwnerReviewInput")
    def require_code_owner_review_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireCodeOwnerReviewInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredApprovingReviewCountInput")
    def required_approving_review_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requiredApprovingReviewCountInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredReviewThreadResolutionInput")
    def required_review_thread_resolution_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredReviewThreadResolutionInput"))

    @builtins.property
    @jsii.member(jsii_name="requireLastPushApprovalInput")
    def require_last_push_approval_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireLastPushApprovalInput"))

    @builtins.property
    @jsii.member(jsii_name="dismissStaleReviewsOnPush")
    def dismiss_stale_reviews_on_push(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dismissStaleReviewsOnPush"))

    @dismiss_stale_reviews_on_push.setter
    def dismiss_stale_reviews_on_push(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfa3ff9f7f6411c735b4b1b8596e1dd79efd19ce597b1baaa408e6055d47f705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dismissStaleReviewsOnPush", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireCodeOwnerReview")
    def require_code_owner_review(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireCodeOwnerReview"))

    @require_code_owner_review.setter
    def require_code_owner_review(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__542b2c450bf7732c53334570e1aa1ed99d3b3b7fb3445b5fce1c4b06b05a7902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireCodeOwnerReview", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredApprovingReviewCount")
    def required_approving_review_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requiredApprovingReviewCount"))

    @required_approving_review_count.setter
    def required_approving_review_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54383224410e56b117133418e188844fb5fb96b9136d312a81d302eca3eb5d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredApprovingReviewCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredReviewThreadResolution")
    def required_review_thread_resolution(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requiredReviewThreadResolution"))

    @required_review_thread_resolution.setter
    def required_review_thread_resolution(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3925c50fe6228c5af86dec0f9510c2d1d007e07ab39676a179344b166242d442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredReviewThreadResolution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireLastPushApproval")
    def require_last_push_approval(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireLastPushApproval"))

    @require_last_push_approval.setter
    def require_last_push_approval(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2c2b2b95611f2b3f3bda80a29d8fd6d9bae7c0284928050a565fd1609c08d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireLastPushApproval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrganizationRulesetRulesPullRequest]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesPullRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationRulesetRulesPullRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f16aa43e7037cf299659f8bdbab01b137b4dba2a20ed04c44363af061e316bf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredCodeScanning",
    jsii_struct_bases=[],
    name_mapping={"required_code_scanning_tool": "requiredCodeScanningTool"},
)
class OrganizationRulesetRulesRequiredCodeScanning:
    def __init__(
        self,
        *,
        required_code_scanning_tool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param required_code_scanning_tool: required_code_scanning_tool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_code_scanning_tool OrganizationRuleset#required_code_scanning_tool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137afefcbc77a3a9eeb1c66d5876055da4e8ec66f2f8873eb245f6ad9c7116a4)
            check_type(argname="argument required_code_scanning_tool", value=required_code_scanning_tool, expected_type=type_hints["required_code_scanning_tool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "required_code_scanning_tool": required_code_scanning_tool,
        }

    @builtins.property
    def required_code_scanning_tool(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool"]]:
        '''required_code_scanning_tool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_code_scanning_tool OrganizationRuleset#required_code_scanning_tool}
        '''
        result = self._values.get("required_code_scanning_tool")
        assert result is not None, "Required property 'required_code_scanning_tool' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRulesRequiredCodeScanning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetRulesRequiredCodeScanningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredCodeScanningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83947b35873e58d49ce8d65882705c07efb55b6cdab8353ded06e730bed15cb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequiredCodeScanningTool")
    def put_required_code_scanning_tool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08126bc6152a9a22456ef6769d2c3d27cb022ad78c90939a9f0c0cec69a7f2f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequiredCodeScanningTool", [value]))

    @builtins.property
    @jsii.member(jsii_name="requiredCodeScanningTool")
    def required_code_scanning_tool(
        self,
    ) -> "OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningToolList":
        return typing.cast("OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningToolList", jsii.get(self, "requiredCodeScanningTool"))

    @builtins.property
    @jsii.member(jsii_name="requiredCodeScanningToolInput")
    def required_code_scanning_tool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool"]]], jsii.get(self, "requiredCodeScanningToolInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrganizationRulesetRulesRequiredCodeScanning]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesRequiredCodeScanning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationRulesetRulesRequiredCodeScanning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c782324c0b7d06f1ae979e8e025dbe80f7a5c0fcf46ef78b27091408c9a3cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool",
    jsii_struct_bases=[],
    name_mapping={
        "alerts_threshold": "alertsThreshold",
        "security_alerts_threshold": "securityAlertsThreshold",
        "tool": "tool",
    },
)
class OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool:
    def __init__(
        self,
        *,
        alerts_threshold: builtins.str,
        security_alerts_threshold: builtins.str,
        tool: builtins.str,
    ) -> None:
        '''
        :param alerts_threshold: The severity level at which code scanning results that raise alerts block a reference update. Can be one of: ``none``, ``errors``, ``errors_and_warnings``, ``all``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#alerts_threshold OrganizationRuleset#alerts_threshold}
        :param security_alerts_threshold: The severity level at which code scanning results that raise security alerts block a reference update. Can be one of: ``none``, ``critical``, ``high_or_higher``, ``medium_or_higher``, ``all``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#security_alerts_threshold OrganizationRuleset#security_alerts_threshold}
        :param tool: The name of a code scanning tool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#tool OrganizationRuleset#tool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098e784b8b6711010d07d0b3531ffea618b323c6f7a21a238b5bb281595a79a9)
            check_type(argname="argument alerts_threshold", value=alerts_threshold, expected_type=type_hints["alerts_threshold"])
            check_type(argname="argument security_alerts_threshold", value=security_alerts_threshold, expected_type=type_hints["security_alerts_threshold"])
            check_type(argname="argument tool", value=tool, expected_type=type_hints["tool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alerts_threshold": alerts_threshold,
            "security_alerts_threshold": security_alerts_threshold,
            "tool": tool,
        }

    @builtins.property
    def alerts_threshold(self) -> builtins.str:
        '''The severity level at which code scanning results that raise alerts block a reference update.

        Can be one of: ``none``, ``errors``, ``errors_and_warnings``, ``all``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#alerts_threshold OrganizationRuleset#alerts_threshold}
        '''
        result = self._values.get("alerts_threshold")
        assert result is not None, "Required property 'alerts_threshold' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_alerts_threshold(self) -> builtins.str:
        '''The severity level at which code scanning results that raise security alerts block a reference update.

        Can be one of: ``none``, ``critical``, ``high_or_higher``, ``medium_or_higher``, ``all``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#security_alerts_threshold OrganizationRuleset#security_alerts_threshold}
        '''
        result = self._values.get("security_alerts_threshold")
        assert result is not None, "Required property 'security_alerts_threshold' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tool(self) -> builtins.str:
        '''The name of a code scanning tool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#tool OrganizationRuleset#tool}
        '''
        result = self._values.get("tool")
        assert result is not None, "Required property 'tool' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningToolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningToolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e31c6dcd16855a907c9bd8ba5da14749aadbcfba72c32901930612449a11e817)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningToolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45646f3a7d4dd669d994def02b0291acc76301ef535132e54434b6ad80a5ce9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningToolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f0ce5042b9775b4979b95915505a928a865de0eb5ae96166597973869ddee6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5807a67482ffb117827a8482c9d0387eb57c3d2ef2bbabd9bcec94cc1c6d8cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffa22c114a4127275cb848019fe6dcba7591dd2b29543aac1f3c02ebe65b98e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf6b232c9064508185a38aa2e9ff7e60b9aa5e56df0a6451c2a55e9af2759962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningToolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningToolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e9f352ba8b5cee824f11346fdf4ab1770d914de2357142386e46938baa02e50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="alertsThresholdInput")
    def alerts_threshold_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alertsThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="securityAlertsThresholdInput")
    def security_alerts_threshold_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityAlertsThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="toolInput")
    def tool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "toolInput"))

    @builtins.property
    @jsii.member(jsii_name="alertsThreshold")
    def alerts_threshold(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alertsThreshold"))

    @alerts_threshold.setter
    def alerts_threshold(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8229d6391031ec99446996ed3466debac6cabf0f4947144f64dab87b584196ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alertsThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityAlertsThreshold")
    def security_alerts_threshold(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityAlertsThreshold"))

    @security_alerts_threshold.setter
    def security_alerts_threshold(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d38c4d3befc74da1910582cf69291afc9aadce0636152c12aa7d96240c6002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityAlertsThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tool")
    def tool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tool"))

    @tool.setter
    def tool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2de873b9b50b96de60a9ea943ab486869c4979315ea644b11d32dc4ad9539e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48980e73606cebe758fcecbe4a60bc527b9c2b97d43cb81a09a1e3600949398c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredStatusChecks",
    jsii_struct_bases=[],
    name_mapping={
        "required_check": "requiredCheck",
        "strict_required_status_checks_policy": "strictRequiredStatusChecksPolicy",
    },
)
class OrganizationRulesetRulesRequiredStatusChecks:
    def __init__(
        self,
        *,
        required_check: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrganizationRulesetRulesRequiredStatusChecksRequiredCheck", typing.Dict[builtins.str, typing.Any]]]],
        strict_required_status_checks_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param required_check: required_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_check OrganizationRuleset#required_check}
        :param strict_required_status_checks_policy: Whether pull requests targeting a matching branch must be tested with the latest code. This setting will not take effect unless at least one status check is enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#strict_required_status_checks_policy OrganizationRuleset#strict_required_status_checks_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d7aba486b967ac91630462bc500cc3594fe6997e073249edca39ba70c660fac)
            check_type(argname="argument required_check", value=required_check, expected_type=type_hints["required_check"])
            check_type(argname="argument strict_required_status_checks_policy", value=strict_required_status_checks_policy, expected_type=type_hints["strict_required_status_checks_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "required_check": required_check,
        }
        if strict_required_status_checks_policy is not None:
            self._values["strict_required_status_checks_policy"] = strict_required_status_checks_policy

    @builtins.property
    def required_check(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetRulesRequiredStatusChecksRequiredCheck"]]:
        '''required_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_check OrganizationRuleset#required_check}
        '''
        result = self._values.get("required_check")
        assert result is not None, "Required property 'required_check' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetRulesRequiredStatusChecksRequiredCheck"]], result)

    @builtins.property
    def strict_required_status_checks_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether pull requests targeting a matching branch must be tested with the latest code.

        This setting will not take effect unless at least one status check is enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#strict_required_status_checks_policy OrganizationRuleset#strict_required_status_checks_policy}
        '''
        result = self._values.get("strict_required_status_checks_policy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRulesRequiredStatusChecks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetRulesRequiredStatusChecksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredStatusChecksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dec79e973955c971829a81cf7e5b179a865224d7880b63d9e57f31bd0c40e043)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequiredCheck")
    def put_required_check(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrganizationRulesetRulesRequiredStatusChecksRequiredCheck", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe6b3e4082ec2e1dd31e15c0da63408b38059b4c4cebc8908e0dcbf3f188fc7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequiredCheck", [value]))

    @jsii.member(jsii_name="resetStrictRequiredStatusChecksPolicy")
    def reset_strict_required_status_checks_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictRequiredStatusChecksPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="requiredCheck")
    def required_check(
        self,
    ) -> "OrganizationRulesetRulesRequiredStatusChecksRequiredCheckList":
        return typing.cast("OrganizationRulesetRulesRequiredStatusChecksRequiredCheckList", jsii.get(self, "requiredCheck"))

    @builtins.property
    @jsii.member(jsii_name="requiredCheckInput")
    def required_check_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetRulesRequiredStatusChecksRequiredCheck"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetRulesRequiredStatusChecksRequiredCheck"]]], jsii.get(self, "requiredCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="strictRequiredStatusChecksPolicyInput")
    def strict_required_status_checks_policy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "strictRequiredStatusChecksPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="strictRequiredStatusChecksPolicy")
    def strict_required_status_checks_policy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "strictRequiredStatusChecksPolicy"))

    @strict_required_status_checks_policy.setter
    def strict_required_status_checks_policy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9a98974e9dfc48fb677394c041782456ee4632cadef0664e31684918f9a3b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictRequiredStatusChecksPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrganizationRulesetRulesRequiredStatusChecks]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesRequiredStatusChecks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationRulesetRulesRequiredStatusChecks],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44582a645d53de6a6173fa113f3fe9cadda736ce7c0c5903eb2d0cbc46e0a12c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredStatusChecksRequiredCheck",
    jsii_struct_bases=[],
    name_mapping={"context": "context", "integration_id": "integrationId"},
)
class OrganizationRulesetRulesRequiredStatusChecksRequiredCheck:
    def __init__(
        self,
        *,
        context: builtins.str,
        integration_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param context: The status check context name that must be present on the commit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#context OrganizationRuleset#context}
        :param integration_id: The optional integration ID that this status check must originate from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#integration_id OrganizationRuleset#integration_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d94f346f8e9567da929511dc9dca073b4ed9a7da9da22f3fb043e6f50580771)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument integration_id", value=integration_id, expected_type=type_hints["integration_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "context": context,
        }
        if integration_id is not None:
            self._values["integration_id"] = integration_id

    @builtins.property
    def context(self) -> builtins.str:
        '''The status check context name that must be present on the commit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#context OrganizationRuleset#context}
        '''
        result = self._values.get("context")
        assert result is not None, "Required property 'context' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration_id(self) -> typing.Optional[jsii.Number]:
        '''The optional integration ID that this status check must originate from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#integration_id OrganizationRuleset#integration_id}
        '''
        result = self._values.get("integration_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRulesRequiredStatusChecksRequiredCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetRulesRequiredStatusChecksRequiredCheckList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredStatusChecksRequiredCheckList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53902b388305bb630165a0503389f10ab0bb6c5a6cfb7c4bd167a0e3cc235853)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrganizationRulesetRulesRequiredStatusChecksRequiredCheckOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30def4f9aa057708846c64d27d3eccd853bd8076558e865fc7a200716c02b72)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrganizationRulesetRulesRequiredStatusChecksRequiredCheckOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45576296ff9dde3e39e1919634c13604734efa3a9a3133245316e0775c03d34c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5afba349512f20d4d391d21f0aa1f4c703c7a3f5d0f031fad383ab3b519e4b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf07e7bbd7d7b1b10e07f3949c2b2d4596471d833d908cad04cb6f7d25baa4f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetRulesRequiredStatusChecksRequiredCheck]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetRulesRequiredStatusChecksRequiredCheck]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetRulesRequiredStatusChecksRequiredCheck]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4686bfa9032e2a17332bab2f8a710b22b54e6c4543923d5dac867588b43343ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrganizationRulesetRulesRequiredStatusChecksRequiredCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredStatusChecksRequiredCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc5bbffd61365978116bf14298121a4eedfe8c22e4e589f9dfc7e72b68737ba2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIntegrationId")
    def reset_integration_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegrationId", []))

    @builtins.property
    @jsii.member(jsii_name="contextInput")
    def context_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationIdInput")
    def integration_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "integrationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "context"))

    @context.setter
    def context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a9ce53cd0252099374998912a9f9fb98f5136c486d3de1a69643cf6d97ddd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integrationId"))

    @integration_id.setter
    def integration_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd67dcddd9cdf4ded9828654b36d009a06f7de60e9267a27225aba6fd8d91149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetRulesRequiredStatusChecksRequiredCheck]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetRulesRequiredStatusChecksRequiredCheck]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetRulesRequiredStatusChecksRequiredCheck]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06187fb3ef7077995d74d9a36d7ec427603ae7cb783ebbad4a7d442cac5508ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredWorkflows",
    jsii_struct_bases=[],
    name_mapping={"required_workflow": "requiredWorkflow"},
)
class OrganizationRulesetRulesRequiredWorkflows:
    def __init__(
        self,
        *,
        required_workflow: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param required_workflow: required_workflow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_workflow OrganizationRuleset#required_workflow}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8177f8274d24da26111c13992e3b2f50f50b37e6c84196a6eae32452a835f451)
            check_type(argname="argument required_workflow", value=required_workflow, expected_type=type_hints["required_workflow"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "required_workflow": required_workflow,
        }

    @builtins.property
    def required_workflow(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow"]]:
        '''required_workflow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#required_workflow OrganizationRuleset#required_workflow}
        '''
        result = self._values.get("required_workflow")
        assert result is not None, "Required property 'required_workflow' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRulesRequiredWorkflows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetRulesRequiredWorkflowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredWorkflowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8afa5cb45578471b14aef64438e823973b0257c88b719abbbb3f4de207a5a2cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequiredWorkflow")
    def put_required_workflow(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d0117df476224f0f7837506a93dbf407f61516afd0dc1cca508d7948e5c4856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequiredWorkflow", [value]))

    @builtins.property
    @jsii.member(jsii_name="requiredWorkflow")
    def required_workflow(
        self,
    ) -> "OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflowList":
        return typing.cast("OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflowList", jsii.get(self, "requiredWorkflow"))

    @builtins.property
    @jsii.member(jsii_name="requiredWorkflowInput")
    def required_workflow_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow"]]], jsii.get(self, "requiredWorkflowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OrganizationRulesetRulesRequiredWorkflows]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesRequiredWorkflows], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationRulesetRulesRequiredWorkflows],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491742ed321a8c89aac137899ef3b6a8c25b21b35baafe93111ba85de6d7b512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "repository_id": "repositoryId", "ref": "ref"},
)
class OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow:
    def __init__(
        self,
        *,
        path: builtins.str,
        repository_id: jsii.Number,
        ref: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The path to the workflow YAML definition file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#path OrganizationRuleset#path}
        :param repository_id: The repository in which the workflow is defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#repository_id OrganizationRuleset#repository_id}
        :param ref: The ref (branch or tag) of the workflow file to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#ref OrganizationRuleset#ref}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64e282fde9d11b302f583d2e2408d13c9943d877ec1cbb0e86f947cb543df6f)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument repository_id", value=repository_id, expected_type=type_hints["repository_id"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "repository_id": repository_id,
        }
        if ref is not None:
            self._values["ref"] = ref

    @builtins.property
    def path(self) -> builtins.str:
        '''The path to the workflow YAML definition file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#path OrganizationRuleset#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_id(self) -> jsii.Number:
        '''The repository in which the workflow is defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#repository_id OrganizationRuleset#repository_id}
        '''
        result = self._values.get("repository_id")
        assert result is not None, "Required property 'repository_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''The ref (branch or tag) of the workflow file to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#ref OrganizationRuleset#ref}
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46681f622de1bab4d0736e3a219fe0cdded6097f9fa4425d59a9053f63423bd5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d10d90488861ad45f0b33cb2215dab524abd558cc9eb90d43d7ded10e384a8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b240a113f53fa21ad4cc5bcaa717d69f52ba361da4b104263060435475e5909a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95720852c1e8abdb53b054b2a34adcdc47f44016d93b5193508af5a867559ee4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__736857fc4d49dd72551db98dc1c55b99a2dee96c56668192d9f574d6d1fc2c5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f163657fc9a50ae9b3799c8cd6bed313d3eead2d9013d74855185a3f78cca9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bd6058038dd04fdbebee82124c8a43f640298ebb279bace01f4bababbe58680)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRef")
    def reset_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRef", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="refInput")
    def ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "refInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryIdInput")
    def repository_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "repositoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7508084649af612b90179c1aeab3160f5f5d1ba2be7badd8cc80804307eb286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ref"))

    @ref.setter
    def ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d4a7ca0091adb8576140d4c9e0418a200f6bf1f265115e3d78fb4d4be5886fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ref", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryId")
    def repository_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "repositoryId"))

    @repository_id.setter
    def repository_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52985d6132bf1ab690e3d724b385f0b0e73ec70fe4c79bf3c104dd59be47a1ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f111f3b965016dcd5525d1b003a8c0c87382c55ec60593b3b5932227279ba5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesTagNamePattern",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "pattern": "pattern",
        "name": "name",
        "negate": "negate",
    },
)
class OrganizationRulesetRulesTagNamePattern:
    def __init__(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4eb71538d649a88877084d9d9e014761c05a2c46c77de57e570018d91864159)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "pattern": pattern,
        }
        if name is not None:
            self._values["name"] = name
        if negate is not None:
            self._values["negate"] = negate

    @builtins.property
    def operator(self) -> builtins.str:
        '''The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#operator OrganizationRuleset#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''The pattern to match with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#pattern OrganizationRuleset#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''How this rule will appear to users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#name OrganizationRuleset#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the rule will fail if the pattern matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/organization_ruleset#negate OrganizationRuleset#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRulesetRulesTagNamePattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRulesetRulesTagNamePatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.organizationRuleset.OrganizationRulesetRulesTagNamePatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06d07a2e4e06c4d7dc03547af6ccc3d4344623b67a6714d190104bc679f5bfec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de5a3382a1ee63dc6eed7ef59e382b30ac3a6ecc1fb35663c4b415c7261fa45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b014c5ce40344ab9f325c18c9d7a4e84fd70491c6c4ad5b43dd9aabad41cc638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0268bb04249451b3bb239c09f51130c8a1731d82e6edb9b44d79e9481bf9f7a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62aa4b0f1ae63283ce7e15abf7867e3c8f669923a75043ced524af3c90fe7e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrganizationRulesetRulesTagNamePattern]:
        return typing.cast(typing.Optional[OrganizationRulesetRulesTagNamePattern], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrganizationRulesetRulesTagNamePattern],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6690c48748056c220b9be13169fa9c3965e131bc0f1cb555799e49bb5897a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OrganizationRuleset",
    "OrganizationRulesetBypassActors",
    "OrganizationRulesetBypassActorsList",
    "OrganizationRulesetBypassActorsOutputReference",
    "OrganizationRulesetConditions",
    "OrganizationRulesetConditionsOutputReference",
    "OrganizationRulesetConditionsRefName",
    "OrganizationRulesetConditionsRefNameOutputReference",
    "OrganizationRulesetConditionsRepositoryName",
    "OrganizationRulesetConditionsRepositoryNameOutputReference",
    "OrganizationRulesetConfig",
    "OrganizationRulesetRules",
    "OrganizationRulesetRulesBranchNamePattern",
    "OrganizationRulesetRulesBranchNamePatternOutputReference",
    "OrganizationRulesetRulesCommitAuthorEmailPattern",
    "OrganizationRulesetRulesCommitAuthorEmailPatternOutputReference",
    "OrganizationRulesetRulesCommitMessagePattern",
    "OrganizationRulesetRulesCommitMessagePatternOutputReference",
    "OrganizationRulesetRulesCommitterEmailPattern",
    "OrganizationRulesetRulesCommitterEmailPatternOutputReference",
    "OrganizationRulesetRulesOutputReference",
    "OrganizationRulesetRulesPullRequest",
    "OrganizationRulesetRulesPullRequestOutputReference",
    "OrganizationRulesetRulesRequiredCodeScanning",
    "OrganizationRulesetRulesRequiredCodeScanningOutputReference",
    "OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool",
    "OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningToolList",
    "OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningToolOutputReference",
    "OrganizationRulesetRulesRequiredStatusChecks",
    "OrganizationRulesetRulesRequiredStatusChecksOutputReference",
    "OrganizationRulesetRulesRequiredStatusChecksRequiredCheck",
    "OrganizationRulesetRulesRequiredStatusChecksRequiredCheckList",
    "OrganizationRulesetRulesRequiredStatusChecksRequiredCheckOutputReference",
    "OrganizationRulesetRulesRequiredWorkflows",
    "OrganizationRulesetRulesRequiredWorkflowsOutputReference",
    "OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow",
    "OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflowList",
    "OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflowOutputReference",
    "OrganizationRulesetRulesTagNamePattern",
    "OrganizationRulesetRulesTagNamePatternOutputReference",
]

publication.publish()

def _typecheckingstub__dc5fb077bc6be64190681136dabf344a2dab20a78bc92b53f438d5d83786b824(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enforcement: builtins.str,
    name: builtins.str,
    rules: typing.Union[OrganizationRulesetRules, typing.Dict[builtins.str, typing.Any]],
    target: builtins.str,
    bypass_actors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrganizationRulesetBypassActors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    conditions: typing.Optional[typing.Union[OrganizationRulesetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__1c6ff98de80e6a4a348913e4a55df868d1695bf21970ba26ed6d339d98f81b6d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f373669f4bd68e952a4755336447269c5f7ae8c2bb6589c2af1ff6762175f9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrganizationRulesetBypassActors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d3d64a69f5a2a364f13b298244c70541c7fd6490eb393a1b7e3c587ee2f27c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37243be924fb15ab18747a8e337050a4cc2da36912c897233f0b69bc2b365a7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e944c9eaf971341521a034c08f59c842f31f8d4b21c480238082dc3e0cf1c40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5260980bd71bca6133344f4e5e5b41b04c33f0c38941fc15a870fe2d5aba2d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171bcb85f36c9e4fc8105474b4c99f6153562a06a88854e69c4bedba915e7579(
    *,
    actor_id: jsii.Number,
    actor_type: builtins.str,
    bypass_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c7f0010cb248f1723fcba91209d0d4c9a95c3d419879043cbcd187ea48cc45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b830714aa7b6af5121e18ab3c9676607bb331768adf2f9dcde30d02f3903d50(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f03cd90d2658709264994b93fa135988f3c4312ec30cd7975c39ed9475657d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b32e8eaeefc8047e53199bc68be333daddd7c21780777fd5c6e5d5e9d5a987(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f94c116c445dd2eaa918570dbb614d827c8f773216db4feb262140e8c418d75(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8185bcdc9b98254e82f9eeb572d57e2c686f1300916551888eec4717651672c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetBypassActors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738a6d7263a7debf64ec3dabd7f56f83b394b4e0bf89b2330016fe178a50bdc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52d44debad1e15a30c957747d930694159b8405b3f4885aece43cdaf86bf689(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8922731231bbcfc8ddc0779a0805c0934ba4b8ee4482a69943a34351a18f750(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a14542ebb5ca2183a9e61b87d7c7583e92e9c2fd486ccaf21a79064ae70ac3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715d43bb5bbead01193bb6437541b657e9444f112dea47c0a5b6facae6832e85(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetBypassActors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c28ea2127e2c083f212de90f5be612f0b955fb6faf6e4c6fd1ac40e4e4be6b(
    *,
    ref_name: typing.Union[OrganizationRulesetConditionsRefName, typing.Dict[builtins.str, typing.Any]],
    repository_id: typing.Optional[typing.Sequence[jsii.Number]] = None,
    repository_name: typing.Optional[typing.Union[OrganizationRulesetConditionsRepositoryName, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615c753c57483beefd58357203599e417d0ca5f1d2e44988bc944be70a53fd0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f329cf75c2515a8327a8a561e60eb4cf00546e3bd8a75c4855191fba89242a(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f8aac87b82c996f3cd2bb7a5ca561424c8380116b2efee2e0460f77a3a7b5b(
    value: typing.Optional[OrganizationRulesetConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a47a657e5128740f328c06455c50e0488f40951acc92b9125753d74b266a565(
    *,
    exclude: typing.Sequence[builtins.str],
    include: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a51b56b89983bfc4bb977f3f3f6c8a1697841d8c8b0979bc09aac2542bae4e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06f03a7be4396cb3a20277609fcb96cdef2b64e7a8544502a9573b518fe49df(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493f67835dab90fa79d583548d05b1158d6d6b5892392471aa8629acaaadbe68(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d84f759664f5a5134f2c3d8d8e4e7d28eb3e24ffbc19682fcb1e9d441ebd1a4(
    value: typing.Optional[OrganizationRulesetConditionsRefName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7f5d26c86b9c559386d286b2d09e3f548da9627e7101137a95bc50ea363f16(
    *,
    exclude: typing.Sequence[builtins.str],
    include: typing.Sequence[builtins.str],
    protected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee985c769e49ab767c1f355fcdd90b767abd2a538e73418cfaf01cf87ca32a64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe28a57b17b48e0b7272fc17454ee7d3e775e07d9e6cd9c76e40912a7afb0313(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93160239ebf0ba2de2a9143bdf2b4f929ccedf216b094cf3ed12df266808dc5c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3795973b2d630175361b1b7042bd51e06156c3c710eaa8db06ddb97fcacad6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08267960101db6648fc9279d42bf1423c1411f4d7faff5c3f545ada823f5850d(
    value: typing.Optional[OrganizationRulesetConditionsRepositoryName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d508c17eb6da5e61ecab2ed862f3910d061c23e0dc5bb2f0734a4f232d332bb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enforcement: builtins.str,
    name: builtins.str,
    rules: typing.Union[OrganizationRulesetRules, typing.Dict[builtins.str, typing.Any]],
    target: builtins.str,
    bypass_actors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrganizationRulesetBypassActors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    conditions: typing.Optional[typing.Union[OrganizationRulesetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a0737e599ea67c04f6e2447a3ace44823d6b435f72c4f6773256687d56c13c(
    *,
    branch_name_pattern: typing.Optional[typing.Union[OrganizationRulesetRulesBranchNamePattern, typing.Dict[builtins.str, typing.Any]]] = None,
    commit_author_email_pattern: typing.Optional[typing.Union[OrganizationRulesetRulesCommitAuthorEmailPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    commit_message_pattern: typing.Optional[typing.Union[OrganizationRulesetRulesCommitMessagePattern, typing.Dict[builtins.str, typing.Any]]] = None,
    committer_email_pattern: typing.Optional[typing.Union[OrganizationRulesetRulesCommitterEmailPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    non_fast_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pull_request: typing.Optional[typing.Union[OrganizationRulesetRulesPullRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    required_code_scanning: typing.Optional[typing.Union[OrganizationRulesetRulesRequiredCodeScanning, typing.Dict[builtins.str, typing.Any]]] = None,
    required_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_signatures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_status_checks: typing.Optional[typing.Union[OrganizationRulesetRulesRequiredStatusChecks, typing.Dict[builtins.str, typing.Any]]] = None,
    required_workflows: typing.Optional[typing.Union[OrganizationRulesetRulesRequiredWorkflows, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_name_pattern: typing.Optional[typing.Union[OrganizationRulesetRulesTagNamePattern, typing.Dict[builtins.str, typing.Any]]] = None,
    update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d8617c4ab8159b74c2eac3cbc9edc3a30a7549d307611dea71f210e465f4636(
    *,
    operator: builtins.str,
    pattern: builtins.str,
    name: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736205d481bdc338f34726bc389f1755697a398597c0ce6cc131ac3c8e690b3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7700db1e87052662ea46011404b8db39512906c7d9b037da7201281c3693bf5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ffee740c3fa39c9a63bd02a8cd2085659f9063f94d7b4fcdb0be05ab25fe18(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a127d903ff08e2bd7cf80933e6a5225a2d8b2a7c0388f6d8d7469af06c32d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86709dc8051d95ddfd2fde814e715885b0e54fec1d3c933144df9f5598efd0a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585b95d64112de10439100cf71a3864c8b2f607196f7da86c89cc79db6ea96da(
    value: typing.Optional[OrganizationRulesetRulesBranchNamePattern],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8999aab61fe9ccbdff23e5804e0b7bd6247a62f3d2044a9d278f414d237fb8(
    *,
    operator: builtins.str,
    pattern: builtins.str,
    name: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e2a547267584c203bdb913733b14eab5b232784852ede88ac19822d748d600(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152eaca7db9c704deff2ef1279c9fd0fd5cf7796af687ec29eb3c8fc4eec3eaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148bf8c3ba90b15ca184a0952bd017f3bb6a1849f9aa0a14f6d3527e4fc64160(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46169928b76607f63b19a84569e25d5b3e4ce011d1f61f196521a08128fd2dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc3f91c359629c3458b4c7a696d15bd91bcc46d85b9f22ab060969a7e38ab92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc94bc247157be6949334ba656ee9d9dd13e15ee871f41c742cb3d86e3086ea2(
    value: typing.Optional[OrganizationRulesetRulesCommitAuthorEmailPattern],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc0eca162b0ca4c9f47bb2a7fb627264e2c745e76a4b60bdc83e8520f9b7ad8(
    *,
    operator: builtins.str,
    pattern: builtins.str,
    name: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760da561ae41501a4a070f405bf5554382e527d8b1d37fadac85602bdf262154(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601f3d0b46409f2abe4e68fa6f9664e4f3c3c8b4cbfc3a067dcfe4c3ff30cb98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebe83db5cdd3aec4bd0ddb378d76c6a96681927795b089d7f1199fdcbbb9319(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ebf28d258c77d9ff9fe9de801aa930b713616566dfb5bd66a8462c73e6abca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c60c91a95cea162858b83e13f98337231f78fcfde91bb2a957f4de1e9cee28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae8d38f026c6bfa55edf176569005fbe74d3e31d659f6f33deb5f4f5b8c0de6(
    value: typing.Optional[OrganizationRulesetRulesCommitMessagePattern],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e19d8418043602d4f6e8b990b0c668f0174df988b6b6edaad841fa209b8fd0(
    *,
    operator: builtins.str,
    pattern: builtins.str,
    name: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5df2033aea927396f3b15c8e77667e44d00787110483e0a223cad8d69d6b59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4271f5130bfd2b1f48da773eb524b5e9cb7cf70d5e99fd780c325cb16ab6da0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da9f99b0b993d9ddf986ef5c0738c9683592bad332eb044b9e0a87ec4e2dd8d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba27b35c8843f575617a82c71127310e824df77d04fd8257f9e9c450b064143(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439f8dce8e417f357842e62e4d8e92d3959cb7d3adeea53a4c2d67953a3ec9a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0de0a44c5329a33775b0ee15a4abc3d4b1672ede251f623e5be8560a171e64a(
    value: typing.Optional[OrganizationRulesetRulesCommitterEmailPattern],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df401dd5d366ab5be38f72d739e9bac0f560595d732b61f8be1f0e67dd02a997(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09371a585154552be4005cf0094db635779f9ddef9a605cc46b80b31b147cf37(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c53412334f78e3e0d69594acf166c6761e0281d26352bc72bd7724eaed3a1e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5a842819d0c1206e92d8b20409d2c77b9ffef04aeb27630ddaf140c36d8f62(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1158af716976767afdd04e159709de05466c86527d88c905a8944be175a2e3a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc026c59ce66f9aa9eb7776bb08eb2e32c06d735352c174b27bd67251e6241b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bce960c939ea61b74ab4061d634a61f2842531a37adcb8fbfcd23d67e15671b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74df58f635f7f6bfa54572807a67ad25262b7d0e23acf149c57ff9e6302c6897(
    value: typing.Optional[OrganizationRulesetRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a6ba266aa0d91b9124cda65218e40e2afd852239f6b33ba8806bbf10d4b854(
    *,
    dismiss_stale_reviews_on_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_code_owner_review: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_approving_review_count: typing.Optional[jsii.Number] = None,
    required_review_thread_resolution: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_last_push_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759c6aea629dae61ec9fd9262226a4e9c84052c21d53348801049e5f4c603516(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa3ff9f7f6411c735b4b1b8596e1dd79efd19ce597b1baaa408e6055d47f705(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542b2c450bf7732c53334570e1aa1ed99d3b3b7fb3445b5fce1c4b06b05a7902(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54383224410e56b117133418e188844fb5fb96b9136d312a81d302eca3eb5d80(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3925c50fe6228c5af86dec0f9510c2d1d007e07ab39676a179344b166242d442(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2c2b2b95611f2b3f3bda80a29d8fd6d9bae7c0284928050a565fd1609c08d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16aa43e7037cf299659f8bdbab01b137b4dba2a20ed04c44363af061e316bf8(
    value: typing.Optional[OrganizationRulesetRulesPullRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137afefcbc77a3a9eeb1c66d5876055da4e8ec66f2f8873eb245f6ad9c7116a4(
    *,
    required_code_scanning_tool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83947b35873e58d49ce8d65882705c07efb55b6cdab8353ded06e730bed15cb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08126bc6152a9a22456ef6769d2c3d27cb022ad78c90939a9f0c0cec69a7f2f7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c782324c0b7d06f1ae979e8e025dbe80f7a5c0fcf46ef78b27091408c9a3cb9(
    value: typing.Optional[OrganizationRulesetRulesRequiredCodeScanning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098e784b8b6711010d07d0b3531ffea618b323c6f7a21a238b5bb281595a79a9(
    *,
    alerts_threshold: builtins.str,
    security_alerts_threshold: builtins.str,
    tool: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31c6dcd16855a907c9bd8ba5da14749aadbcfba72c32901930612449a11e817(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45646f3a7d4dd669d994def02b0291acc76301ef535132e54434b6ad80a5ce9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f0ce5042b9775b4979b95915505a928a865de0eb5ae96166597973869ddee6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5807a67482ffb117827a8482c9d0387eb57c3d2ef2bbabd9bcec94cc1c6d8cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa22c114a4127275cb848019fe6dcba7591dd2b29543aac1f3c02ebe65b98e0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf6b232c9064508185a38aa2e9ff7e60b9aa5e56df0a6451c2a55e9af2759962(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9f352ba8b5cee824f11346fdf4ab1770d914de2357142386e46938baa02e50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8229d6391031ec99446996ed3466debac6cabf0f4947144f64dab87b584196ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d38c4d3befc74da1910582cf69291afc9aadce0636152c12aa7d96240c6002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2de873b9b50b96de60a9ea943ab486869c4979315ea644b11d32dc4ad9539e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48980e73606cebe758fcecbe4a60bc527b9c2b97d43cb81a09a1e3600949398c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7aba486b967ac91630462bc500cc3594fe6997e073249edca39ba70c660fac(
    *,
    required_check: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrganizationRulesetRulesRequiredStatusChecksRequiredCheck, typing.Dict[builtins.str, typing.Any]]]],
    strict_required_status_checks_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec79e973955c971829a81cf7e5b179a865224d7880b63d9e57f31bd0c40e043(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6b3e4082ec2e1dd31e15c0da63408b38059b4c4cebc8908e0dcbf3f188fc7c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrganizationRulesetRulesRequiredStatusChecksRequiredCheck, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9a98974e9dfc48fb677394c041782456ee4632cadef0664e31684918f9a3b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44582a645d53de6a6173fa113f3fe9cadda736ce7c0c5903eb2d0cbc46e0a12c(
    value: typing.Optional[OrganizationRulesetRulesRequiredStatusChecks],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d94f346f8e9567da929511dc9dca073b4ed9a7da9da22f3fb043e6f50580771(
    *,
    context: builtins.str,
    integration_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53902b388305bb630165a0503389f10ab0bb6c5a6cfb7c4bd167a0e3cc235853(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30def4f9aa057708846c64d27d3eccd853bd8076558e865fc7a200716c02b72(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45576296ff9dde3e39e1919634c13604734efa3a9a3133245316e0775c03d34c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5afba349512f20d4d391d21f0aa1f4c703c7a3f5d0f031fad383ab3b519e4b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf07e7bbd7d7b1b10e07f3949c2b2d4596471d833d908cad04cb6f7d25baa4f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4686bfa9032e2a17332bab2f8a710b22b54e6c4543923d5dac867588b43343ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetRulesRequiredStatusChecksRequiredCheck]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5bbffd61365978116bf14298121a4eedfe8c22e4e589f9dfc7e72b68737ba2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a9ce53cd0252099374998912a9f9fb98f5136c486d3de1a69643cf6d97ddd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd67dcddd9cdf4ded9828654b36d009a06f7de60e9267a27225aba6fd8d91149(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06187fb3ef7077995d74d9a36d7ec427603ae7cb783ebbad4a7d442cac5508ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetRulesRequiredStatusChecksRequiredCheck]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8177f8274d24da26111c13992e3b2f50f50b37e6c84196a6eae32452a835f451(
    *,
    required_workflow: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8afa5cb45578471b14aef64438e823973b0257c88b719abbbb3f4de207a5a2cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0117df476224f0f7837506a93dbf407f61516afd0dc1cca508d7948e5c4856(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491742ed321a8c89aac137899ef3b6a8c25b21b35baafe93111ba85de6d7b512(
    value: typing.Optional[OrganizationRulesetRulesRequiredWorkflows],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64e282fde9d11b302f583d2e2408d13c9943d877ec1cbb0e86f947cb543df6f(
    *,
    path: builtins.str,
    repository_id: jsii.Number,
    ref: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46681f622de1bab4d0736e3a219fe0cdded6097f9fa4425d59a9053f63423bd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d10d90488861ad45f0b33cb2215dab524abd558cc9eb90d43d7ded10e384a8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b240a113f53fa21ad4cc5bcaa717d69f52ba361da4b104263060435475e5909a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95720852c1e8abdb53b054b2a34adcdc47f44016d93b5193508af5a867559ee4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736857fc4d49dd72551db98dc1c55b99a2dee96c56668192d9f574d6d1fc2c5c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f163657fc9a50ae9b3799c8cd6bed313d3eead2d9013d74855185a3f78cca9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd6058038dd04fdbebee82124c8a43f640298ebb279bace01f4bababbe58680(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7508084649af612b90179c1aeab3160f5f5d1ba2be7badd8cc80804307eb286(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4a7ca0091adb8576140d4c9e0418a200f6bf1f265115e3d78fb4d4be5886fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52985d6132bf1ab690e3d724b385f0b0e73ec70fe4c79bf3c104dd59be47a1ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f111f3b965016dcd5525d1b003a8c0c87382c55ec60593b3b5932227279ba5f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrganizationRulesetRulesRequiredWorkflowsRequiredWorkflow]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4eb71538d649a88877084d9d9e014761c05a2c46c77de57e570018d91864159(
    *,
    operator: builtins.str,
    pattern: builtins.str,
    name: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d07a2e4e06c4d7dc03547af6ccc3d4344623b67a6714d190104bc679f5bfec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de5a3382a1ee63dc6eed7ef59e382b30ac3a6ecc1fb35663c4b415c7261fa45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b014c5ce40344ab9f325c18c9d7a4e84fd70491c6c4ad5b43dd9aabad41cc638(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0268bb04249451b3bb239c09f51130c8a1731d82e6edb9b44d79e9481bf9f7a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62aa4b0f1ae63283ce7e15abf7867e3c8f669923a75043ced524af3c90fe7e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6690c48748056c220b9be13169fa9c3965e131bc0f1cb555799e49bb5897a77(
    value: typing.Optional[OrganizationRulesetRulesTagNamePattern],
) -> None:
    """Type checking stubs"""
    pass
