r'''
# `github_repository_ruleset`

Refer to the Terraform Registry for docs: [`github_repository_ruleset`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset).
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


class RepositoryRuleset(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRuleset",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset github_repository_ruleset}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enforcement: builtins.str,
        name: builtins.str,
        rules: typing.Union["RepositoryRulesetRules", typing.Dict[builtins.str, typing.Any]],
        target: builtins.str,
        bypass_actors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RepositoryRulesetBypassActors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        conditions: typing.Optional[typing.Union["RepositoryRulesetConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset github_repository_ruleset} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enforcement: Possible values for Enforcement are ``disabled``, ``active``, ``evaluate``. Note: ``evaluate`` is currently only supported for owners of type ``organization``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#enforcement RepositoryRuleset#enforcement}
        :param name: The name of the ruleset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#rules RepositoryRuleset#rules}
        :param target: Possible values are ``branch`` and ``tag``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#target RepositoryRuleset#target}
        :param bypass_actors: bypass_actors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#bypass_actors RepositoryRuleset#bypass_actors}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#conditions RepositoryRuleset#conditions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#id RepositoryRuleset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param repository: Name of the repository to apply rulset to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#repository RepositoryRuleset#repository}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53279645c069276d4082bf54449f7fa421c295085e74152004c5c91574ec4c34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RepositoryRulesetConfig(
            enforcement=enforcement,
            name=name,
            rules=rules,
            target=target,
            bypass_actors=bypass_actors,
            conditions=conditions,
            id=id,
            repository=repository,
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
        '''Generates CDKTF code for importing a RepositoryRuleset resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RepositoryRuleset to import.
        :param import_from_id: The id of the existing RepositoryRuleset that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RepositoryRuleset to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ece29a0777386e19090e4ba8a22f753dae76867973b9c15753a6cc4175eaef7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBypassActors")
    def put_bypass_actors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RepositoryRulesetBypassActors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9b1464e3f8fbb272e52a265cc64decc8f12d456505b46c7780d8df262e8e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBypassActors", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        *,
        ref_name: typing.Union["RepositoryRulesetConditionsRefName", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param ref_name: ref_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#ref_name RepositoryRuleset#ref_name}
        '''
        value = RepositoryRulesetConditions(ref_name=ref_name)

        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        *,
        branch_name_pattern: typing.Optional[typing.Union["RepositoryRulesetRulesBranchNamePattern", typing.Dict[builtins.str, typing.Any]]] = None,
        commit_author_email_pattern: typing.Optional[typing.Union["RepositoryRulesetRulesCommitAuthorEmailPattern", typing.Dict[builtins.str, typing.Any]]] = None,
        commit_message_pattern: typing.Optional[typing.Union["RepositoryRulesetRulesCommitMessagePattern", typing.Dict[builtins.str, typing.Any]]] = None,
        committer_email_pattern: typing.Optional[typing.Union["RepositoryRulesetRulesCommitterEmailPattern", typing.Dict[builtins.str, typing.Any]]] = None,
        creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_queue: typing.Optional[typing.Union["RepositoryRulesetRulesMergeQueue", typing.Dict[builtins.str, typing.Any]]] = None,
        non_fast_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pull_request: typing.Optional[typing.Union["RepositoryRulesetRulesPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        required_code_scanning: typing.Optional[typing.Union["RepositoryRulesetRulesRequiredCodeScanning", typing.Dict[builtins.str, typing.Any]]] = None,
        required_deployments: typing.Optional[typing.Union["RepositoryRulesetRulesRequiredDeployments", typing.Dict[builtins.str, typing.Any]]] = None,
        required_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_signatures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_status_checks: typing.Optional[typing.Union["RepositoryRulesetRulesRequiredStatusChecks", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_name_pattern: typing.Optional[typing.Union["RepositoryRulesetRulesTagNamePattern", typing.Dict[builtins.str, typing.Any]]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        update_allows_fetch_and_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch_name_pattern: branch_name_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#branch_name_pattern RepositoryRuleset#branch_name_pattern}
        :param commit_author_email_pattern: commit_author_email_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#commit_author_email_pattern RepositoryRuleset#commit_author_email_pattern}
        :param commit_message_pattern: commit_message_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#commit_message_pattern RepositoryRuleset#commit_message_pattern}
        :param committer_email_pattern: committer_email_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#committer_email_pattern RepositoryRuleset#committer_email_pattern}
        :param creation: Only allow users with bypass permission to create matching refs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#creation RepositoryRuleset#creation}
        :param deletion: Only allow users with bypass permissions to delete matching refs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#deletion RepositoryRuleset#deletion}
        :param merge_queue: merge_queue block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#merge_queue RepositoryRuleset#merge_queue}
        :param non_fast_forward: Prevent users with push access from force pushing to branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#non_fast_forward RepositoryRuleset#non_fast_forward}
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pull_request RepositoryRuleset#pull_request}
        :param required_code_scanning: required_code_scanning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_code_scanning RepositoryRuleset#required_code_scanning}
        :param required_deployments: required_deployments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_deployments RepositoryRuleset#required_deployments}
        :param required_linear_history: Prevent merge commits from being pushed to matching branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_linear_history RepositoryRuleset#required_linear_history}
        :param required_signatures: Commits pushed to matching branches must have verified signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_signatures RepositoryRuleset#required_signatures}
        :param required_status_checks: required_status_checks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_status_checks RepositoryRuleset#required_status_checks}
        :param tag_name_pattern: tag_name_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#tag_name_pattern RepositoryRuleset#tag_name_pattern}
        :param update: Only allow users with bypass permission to update matching refs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#update RepositoryRuleset#update}
        :param update_allows_fetch_and_merge: Branch can pull changes from its upstream repository. This is only applicable to forked repositories. Requires ``update`` to be set to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#update_allows_fetch_and_merge RepositoryRuleset#update_allows_fetch_and_merge}
        '''
        value = RepositoryRulesetRules(
            branch_name_pattern=branch_name_pattern,
            commit_author_email_pattern=commit_author_email_pattern,
            commit_message_pattern=commit_message_pattern,
            committer_email_pattern=committer_email_pattern,
            creation=creation,
            deletion=deletion,
            merge_queue=merge_queue,
            non_fast_forward=non_fast_forward,
            pull_request=pull_request,
            required_code_scanning=required_code_scanning,
            required_deployments=required_deployments,
            required_linear_history=required_linear_history,
            required_signatures=required_signatures,
            required_status_checks=required_status_checks,
            tag_name_pattern=tag_name_pattern,
            update=update,
            update_allows_fetch_and_merge=update_allows_fetch_and_merge,
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

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

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
    def bypass_actors(self) -> "RepositoryRulesetBypassActorsList":
        return typing.cast("RepositoryRulesetBypassActorsList", jsii.get(self, "bypassActors"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "RepositoryRulesetConditionsOutputReference":
        return typing.cast("RepositoryRulesetConditionsOutputReference", jsii.get(self, "conditions"))

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
    def rules(self) -> "RepositoryRulesetRulesOutputReference":
        return typing.cast("RepositoryRulesetRulesOutputReference", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="rulesetId")
    def ruleset_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rulesetId"))

    @builtins.property
    @jsii.member(jsii_name="bypassActorsInput")
    def bypass_actors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryRulesetBypassActors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryRulesetBypassActors"]]], jsii.get(self, "bypassActorsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(self) -> typing.Optional["RepositoryRulesetConditions"]:
        return typing.cast(typing.Optional["RepositoryRulesetConditions"], jsii.get(self, "conditionsInput"))

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
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(self) -> typing.Optional["RepositoryRulesetRules"]:
        return typing.cast(typing.Optional["RepositoryRulesetRules"], jsii.get(self, "rulesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0834989dfb73b2358a7b9eee89c980500752e5ba7c0fdeec8702e42f2d69b703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75299856d0c32f805d1e71c83ef01ef6e34b075d17fb46be0fe5df0c4981002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b83181f79362ede70bdbfc1563f0d77da4b3d0f2766193c88563418262adf29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2c3e92cc472434bad498398bf30562de5cedc912cc1e8b893ad0747e44dca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb5f15dc9e585f322f093627c09fcdde843532f5547c118353fa8aebf8be2ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetBypassActors",
    jsii_struct_bases=[],
    name_mapping={
        "actor_id": "actorId",
        "actor_type": "actorType",
        "bypass_mode": "bypassMode",
    },
)
class RepositoryRulesetBypassActors:
    def __init__(
        self,
        *,
        actor_id: jsii.Number,
        actor_type: builtins.str,
        bypass_mode: builtins.str,
    ) -> None:
        '''
        :param actor_id: The ID of the actor that can bypass a ruleset. When ``actor_type`` is ``OrganizationAdmin``, this should be set to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#actor_id RepositoryRuleset#actor_id}
        :param actor_type: The type of actor that can bypass a ruleset. Can be one of: ``RepositoryRole``, ``Team``, ``Integration``, ``OrganizationAdmin``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#actor_type RepositoryRuleset#actor_type}
        :param bypass_mode: When the specified actor can bypass the ruleset. pull_request means that an actor can only bypass rules on pull requests. Can be one of: ``always``, ``pull_request``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#bypass_mode RepositoryRuleset#bypass_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b113f8eb65ef947d85bbb9023fc2306f7cd3f8bc22ebdc38135400f20ead774)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#actor_id RepositoryRuleset#actor_id}
        '''
        result = self._values.get("actor_id")
        assert result is not None, "Required property 'actor_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def actor_type(self) -> builtins.str:
        '''The type of actor that can bypass a ruleset. Can be one of: ``RepositoryRole``, ``Team``, ``Integration``, ``OrganizationAdmin``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#actor_type RepositoryRuleset#actor_type}
        '''
        result = self._values.get("actor_type")
        assert result is not None, "Required property 'actor_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bypass_mode(self) -> builtins.str:
        '''When the specified actor can bypass the ruleset.

        pull_request means that an actor can only bypass rules on pull requests. Can be one of: ``always``, ``pull_request``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#bypass_mode RepositoryRuleset#bypass_mode}
        '''
        result = self._values.get("bypass_mode")
        assert result is not None, "Required property 'bypass_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetBypassActors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetBypassActorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetBypassActorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e11bd1677cad3721d805ef05d277463671de5223b127c2f0b6d8aad249b8a746)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RepositoryRulesetBypassActorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0695c61e16c05ecfeb5d0a08b1689a22dbdd0fb191ea3dfc96c17f462cc64dd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RepositoryRulesetBypassActorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0efb674fc34f95350206a942886ac061429b423def93af98205d5f3aac4b24a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9eba553f86eca2b7e86729b7671a9eac76c90f3f4bc3106c3c5de391b5f07d06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18fd3ef470fecf3e81c9dc73af65aee050c39870319f13b472471f24e860af80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetBypassActors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetBypassActors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetBypassActors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c12dc9bc7b8e37b0cf9bc65323fc580fc5e244ab2cbb31d30c475cfe34a4cb79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RepositoryRulesetBypassActorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetBypassActorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a42f0caddbae1a435cb51c4cafe761cf4776d297f9bb68c87d0bdb8ff22de912)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f263ee75bc019cf69b93b46582b0bb71b7f10d24dd9977492e0b948eaa6609b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="actorType")
    def actor_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actorType"))

    @actor_type.setter
    def actor_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b6cdf17f41002323313e65e36225580f2c0d040fe30a1e558b01dcab373dc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bypassMode")
    def bypass_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bypassMode"))

    @bypass_mode.setter
    def bypass_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34d437e2022d5c6f980308865064f12858f6291fce5af342d6dab8d046b05a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bypassMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryRulesetBypassActors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryRulesetBypassActors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryRulesetBypassActors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6e341bcdf7ee408097128baacda62ba5b54ebff03d283c896c486e83499b84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetConditions",
    jsii_struct_bases=[],
    name_mapping={"ref_name": "refName"},
)
class RepositoryRulesetConditions:
    def __init__(
        self,
        *,
        ref_name: typing.Union["RepositoryRulesetConditionsRefName", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param ref_name: ref_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#ref_name RepositoryRuleset#ref_name}
        '''
        if isinstance(ref_name, dict):
            ref_name = RepositoryRulesetConditionsRefName(**ref_name)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b15d442be132dc3099287a32ff3e984f05e9396b93ad69f6d9be0c194daeb698)
            check_type(argname="argument ref_name", value=ref_name, expected_type=type_hints["ref_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ref_name": ref_name,
        }

    @builtins.property
    def ref_name(self) -> "RepositoryRulesetConditionsRefName":
        '''ref_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#ref_name RepositoryRuleset#ref_name}
        '''
        result = self._values.get("ref_name")
        assert result is not None, "Required property 'ref_name' is missing"
        return typing.cast("RepositoryRulesetConditionsRefName", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c2dd1738c775d5258fec2391c0a8a44303428fc3fd9a224d4a7ba4ffeeb0e72)
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
        :param exclude: Array of ref names or patterns to exclude. The condition will not pass if any of these patterns match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#exclude RepositoryRuleset#exclude}
        :param include: Array of ref names or patterns to include. One of these patterns must match for the condition to pass. Also accepts ``~DEFAULT_BRANCH`` to include the default branch or ``~ALL`` to include all branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#include RepositoryRuleset#include}
        '''
        value = RepositoryRulesetConditionsRefName(exclude=exclude, include=include)

        return typing.cast(None, jsii.invoke(self, "putRefName", [value]))

    @builtins.property
    @jsii.member(jsii_name="refName")
    def ref_name(self) -> "RepositoryRulesetConditionsRefNameOutputReference":
        return typing.cast("RepositoryRulesetConditionsRefNameOutputReference", jsii.get(self, "refName"))

    @builtins.property
    @jsii.member(jsii_name="refNameInput")
    def ref_name_input(self) -> typing.Optional["RepositoryRulesetConditionsRefName"]:
        return typing.cast(typing.Optional["RepositoryRulesetConditionsRefName"], jsii.get(self, "refNameInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RepositoryRulesetConditions]:
        return typing.cast(typing.Optional[RepositoryRulesetConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryRulesetConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4358190746360641a38b0106338f0784aeae3383eb30ebd0fdbdd7a37d5ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetConditionsRefName",
    jsii_struct_bases=[],
    name_mapping={"exclude": "exclude", "include": "include"},
)
class RepositoryRulesetConditionsRefName:
    def __init__(
        self,
        *,
        exclude: typing.Sequence[builtins.str],
        include: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param exclude: Array of ref names or patterns to exclude. The condition will not pass if any of these patterns match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#exclude RepositoryRuleset#exclude}
        :param include: Array of ref names or patterns to include. One of these patterns must match for the condition to pass. Also accepts ``~DEFAULT_BRANCH`` to include the default branch or ``~ALL`` to include all branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#include RepositoryRuleset#include}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c4c98adc74312f53208d238205844b70cd80142c1e2b4b2b95d1329cf654c9)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exclude": exclude,
            "include": include,
        }

    @builtins.property
    def exclude(self) -> typing.List[builtins.str]:
        '''Array of ref names or patterns to exclude. The condition will not pass if any of these patterns match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#exclude RepositoryRuleset#exclude}
        '''
        result = self._values.get("exclude")
        assert result is not None, "Required property 'exclude' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def include(self) -> typing.List[builtins.str]:
        '''Array of ref names or patterns to include.

        One of these patterns must match for the condition to pass. Also accepts ``~DEFAULT_BRANCH`` to include the default branch or ``~ALL`` to include all branches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#include RepositoryRuleset#include}
        '''
        result = self._values.get("include")
        assert result is not None, "Required property 'include' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetConditionsRefName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetConditionsRefNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetConditionsRefNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d8289ecf2b395f25af8db19c42adddf6e662561bd1ebac1997232a722eac6a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc2c86789a36029655b2803423bcb19c9fcf670a74240c473ee797e919dd8bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="include")
    def include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "include"))

    @include.setter
    def include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47b481b3bc0ddb2fcfa583604a650a99e4520c5f19665695362e171106da1a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "include", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RepositoryRulesetConditionsRefName]:
        return typing.cast(typing.Optional[RepositoryRulesetConditionsRefName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryRulesetConditionsRefName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0bcd2a38adfd58db6eb83106c457da08f2acde2a46777f85d5af8637a1ac30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetConfig",
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
        "repository": "repository",
    },
)
class RepositoryRulesetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rules: typing.Union["RepositoryRulesetRules", typing.Dict[builtins.str, typing.Any]],
        target: builtins.str,
        bypass_actors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RepositoryRulesetBypassActors, typing.Dict[builtins.str, typing.Any]]]]] = None,
        conditions: typing.Optional[typing.Union[RepositoryRulesetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enforcement: Possible values for Enforcement are ``disabled``, ``active``, ``evaluate``. Note: ``evaluate`` is currently only supported for owners of type ``organization``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#enforcement RepositoryRuleset#enforcement}
        :param name: The name of the ruleset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#rules RepositoryRuleset#rules}
        :param target: Possible values are ``branch`` and ``tag``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#target RepositoryRuleset#target}
        :param bypass_actors: bypass_actors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#bypass_actors RepositoryRuleset#bypass_actors}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#conditions RepositoryRuleset#conditions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#id RepositoryRuleset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param repository: Name of the repository to apply rulset to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#repository RepositoryRuleset#repository}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(rules, dict):
            rules = RepositoryRulesetRules(**rules)
        if isinstance(conditions, dict):
            conditions = RepositoryRulesetConditions(**conditions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd935179a0b5de3525aae4445b5b9f9cf2143c7fc2d8eb5b083f539a21243164)
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
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
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
        if repository is not None:
            self._values["repository"] = repository

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#enforcement RepositoryRuleset#enforcement}
        '''
        result = self._values.get("enforcement")
        assert result is not None, "Required property 'enforcement' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the ruleset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(self) -> "RepositoryRulesetRules":
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#rules RepositoryRuleset#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast("RepositoryRulesetRules", result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Possible values are ``branch`` and ``tag``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#target RepositoryRuleset#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bypass_actors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetBypassActors]]]:
        '''bypass_actors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#bypass_actors RepositoryRuleset#bypass_actors}
        '''
        result = self._values.get("bypass_actors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetBypassActors]]], result)

    @builtins.property
    def conditions(self) -> typing.Optional[RepositoryRulesetConditions]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#conditions RepositoryRuleset#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[RepositoryRulesetConditions], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#id RepositoryRuleset#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''Name of the repository to apply rulset to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#repository RepositoryRuleset#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRules",
    jsii_struct_bases=[],
    name_mapping={
        "branch_name_pattern": "branchNamePattern",
        "commit_author_email_pattern": "commitAuthorEmailPattern",
        "commit_message_pattern": "commitMessagePattern",
        "committer_email_pattern": "committerEmailPattern",
        "creation": "creation",
        "deletion": "deletion",
        "merge_queue": "mergeQueue",
        "non_fast_forward": "nonFastForward",
        "pull_request": "pullRequest",
        "required_code_scanning": "requiredCodeScanning",
        "required_deployments": "requiredDeployments",
        "required_linear_history": "requiredLinearHistory",
        "required_signatures": "requiredSignatures",
        "required_status_checks": "requiredStatusChecks",
        "tag_name_pattern": "tagNamePattern",
        "update": "update",
        "update_allows_fetch_and_merge": "updateAllowsFetchAndMerge",
    },
)
class RepositoryRulesetRules:
    def __init__(
        self,
        *,
        branch_name_pattern: typing.Optional[typing.Union["RepositoryRulesetRulesBranchNamePattern", typing.Dict[builtins.str, typing.Any]]] = None,
        commit_author_email_pattern: typing.Optional[typing.Union["RepositoryRulesetRulesCommitAuthorEmailPattern", typing.Dict[builtins.str, typing.Any]]] = None,
        commit_message_pattern: typing.Optional[typing.Union["RepositoryRulesetRulesCommitMessagePattern", typing.Dict[builtins.str, typing.Any]]] = None,
        committer_email_pattern: typing.Optional[typing.Union["RepositoryRulesetRulesCommitterEmailPattern", typing.Dict[builtins.str, typing.Any]]] = None,
        creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        merge_queue: typing.Optional[typing.Union["RepositoryRulesetRulesMergeQueue", typing.Dict[builtins.str, typing.Any]]] = None,
        non_fast_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pull_request: typing.Optional[typing.Union["RepositoryRulesetRulesPullRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        required_code_scanning: typing.Optional[typing.Union["RepositoryRulesetRulesRequiredCodeScanning", typing.Dict[builtins.str, typing.Any]]] = None,
        required_deployments: typing.Optional[typing.Union["RepositoryRulesetRulesRequiredDeployments", typing.Dict[builtins.str, typing.Any]]] = None,
        required_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_signatures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_status_checks: typing.Optional[typing.Union["RepositoryRulesetRulesRequiredStatusChecks", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_name_pattern: typing.Optional[typing.Union["RepositoryRulesetRulesTagNamePattern", typing.Dict[builtins.str, typing.Any]]] = None,
        update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        update_allows_fetch_and_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param branch_name_pattern: branch_name_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#branch_name_pattern RepositoryRuleset#branch_name_pattern}
        :param commit_author_email_pattern: commit_author_email_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#commit_author_email_pattern RepositoryRuleset#commit_author_email_pattern}
        :param commit_message_pattern: commit_message_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#commit_message_pattern RepositoryRuleset#commit_message_pattern}
        :param committer_email_pattern: committer_email_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#committer_email_pattern RepositoryRuleset#committer_email_pattern}
        :param creation: Only allow users with bypass permission to create matching refs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#creation RepositoryRuleset#creation}
        :param deletion: Only allow users with bypass permissions to delete matching refs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#deletion RepositoryRuleset#deletion}
        :param merge_queue: merge_queue block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#merge_queue RepositoryRuleset#merge_queue}
        :param non_fast_forward: Prevent users with push access from force pushing to branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#non_fast_forward RepositoryRuleset#non_fast_forward}
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pull_request RepositoryRuleset#pull_request}
        :param required_code_scanning: required_code_scanning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_code_scanning RepositoryRuleset#required_code_scanning}
        :param required_deployments: required_deployments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_deployments RepositoryRuleset#required_deployments}
        :param required_linear_history: Prevent merge commits from being pushed to matching branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_linear_history RepositoryRuleset#required_linear_history}
        :param required_signatures: Commits pushed to matching branches must have verified signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_signatures RepositoryRuleset#required_signatures}
        :param required_status_checks: required_status_checks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_status_checks RepositoryRuleset#required_status_checks}
        :param tag_name_pattern: tag_name_pattern block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#tag_name_pattern RepositoryRuleset#tag_name_pattern}
        :param update: Only allow users with bypass permission to update matching refs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#update RepositoryRuleset#update}
        :param update_allows_fetch_and_merge: Branch can pull changes from its upstream repository. This is only applicable to forked repositories. Requires ``update`` to be set to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#update_allows_fetch_and_merge RepositoryRuleset#update_allows_fetch_and_merge}
        '''
        if isinstance(branch_name_pattern, dict):
            branch_name_pattern = RepositoryRulesetRulesBranchNamePattern(**branch_name_pattern)
        if isinstance(commit_author_email_pattern, dict):
            commit_author_email_pattern = RepositoryRulesetRulesCommitAuthorEmailPattern(**commit_author_email_pattern)
        if isinstance(commit_message_pattern, dict):
            commit_message_pattern = RepositoryRulesetRulesCommitMessagePattern(**commit_message_pattern)
        if isinstance(committer_email_pattern, dict):
            committer_email_pattern = RepositoryRulesetRulesCommitterEmailPattern(**committer_email_pattern)
        if isinstance(merge_queue, dict):
            merge_queue = RepositoryRulesetRulesMergeQueue(**merge_queue)
        if isinstance(pull_request, dict):
            pull_request = RepositoryRulesetRulesPullRequest(**pull_request)
        if isinstance(required_code_scanning, dict):
            required_code_scanning = RepositoryRulesetRulesRequiredCodeScanning(**required_code_scanning)
        if isinstance(required_deployments, dict):
            required_deployments = RepositoryRulesetRulesRequiredDeployments(**required_deployments)
        if isinstance(required_status_checks, dict):
            required_status_checks = RepositoryRulesetRulesRequiredStatusChecks(**required_status_checks)
        if isinstance(tag_name_pattern, dict):
            tag_name_pattern = RepositoryRulesetRulesTagNamePattern(**tag_name_pattern)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd5b2598496ce154f58d07f1ccc6b67c083a48a52f2a5e895e5dc19cc81eb5d)
            check_type(argname="argument branch_name_pattern", value=branch_name_pattern, expected_type=type_hints["branch_name_pattern"])
            check_type(argname="argument commit_author_email_pattern", value=commit_author_email_pattern, expected_type=type_hints["commit_author_email_pattern"])
            check_type(argname="argument commit_message_pattern", value=commit_message_pattern, expected_type=type_hints["commit_message_pattern"])
            check_type(argname="argument committer_email_pattern", value=committer_email_pattern, expected_type=type_hints["committer_email_pattern"])
            check_type(argname="argument creation", value=creation, expected_type=type_hints["creation"])
            check_type(argname="argument deletion", value=deletion, expected_type=type_hints["deletion"])
            check_type(argname="argument merge_queue", value=merge_queue, expected_type=type_hints["merge_queue"])
            check_type(argname="argument non_fast_forward", value=non_fast_forward, expected_type=type_hints["non_fast_forward"])
            check_type(argname="argument pull_request", value=pull_request, expected_type=type_hints["pull_request"])
            check_type(argname="argument required_code_scanning", value=required_code_scanning, expected_type=type_hints["required_code_scanning"])
            check_type(argname="argument required_deployments", value=required_deployments, expected_type=type_hints["required_deployments"])
            check_type(argname="argument required_linear_history", value=required_linear_history, expected_type=type_hints["required_linear_history"])
            check_type(argname="argument required_signatures", value=required_signatures, expected_type=type_hints["required_signatures"])
            check_type(argname="argument required_status_checks", value=required_status_checks, expected_type=type_hints["required_status_checks"])
            check_type(argname="argument tag_name_pattern", value=tag_name_pattern, expected_type=type_hints["tag_name_pattern"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
            check_type(argname="argument update_allows_fetch_and_merge", value=update_allows_fetch_and_merge, expected_type=type_hints["update_allows_fetch_and_merge"])
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
        if merge_queue is not None:
            self._values["merge_queue"] = merge_queue
        if non_fast_forward is not None:
            self._values["non_fast_forward"] = non_fast_forward
        if pull_request is not None:
            self._values["pull_request"] = pull_request
        if required_code_scanning is not None:
            self._values["required_code_scanning"] = required_code_scanning
        if required_deployments is not None:
            self._values["required_deployments"] = required_deployments
        if required_linear_history is not None:
            self._values["required_linear_history"] = required_linear_history
        if required_signatures is not None:
            self._values["required_signatures"] = required_signatures
        if required_status_checks is not None:
            self._values["required_status_checks"] = required_status_checks
        if tag_name_pattern is not None:
            self._values["tag_name_pattern"] = tag_name_pattern
        if update is not None:
            self._values["update"] = update
        if update_allows_fetch_and_merge is not None:
            self._values["update_allows_fetch_and_merge"] = update_allows_fetch_and_merge

    @builtins.property
    def branch_name_pattern(
        self,
    ) -> typing.Optional["RepositoryRulesetRulesBranchNamePattern"]:
        '''branch_name_pattern block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#branch_name_pattern RepositoryRuleset#branch_name_pattern}
        '''
        result = self._values.get("branch_name_pattern")
        return typing.cast(typing.Optional["RepositoryRulesetRulesBranchNamePattern"], result)

    @builtins.property
    def commit_author_email_pattern(
        self,
    ) -> typing.Optional["RepositoryRulesetRulesCommitAuthorEmailPattern"]:
        '''commit_author_email_pattern block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#commit_author_email_pattern RepositoryRuleset#commit_author_email_pattern}
        '''
        result = self._values.get("commit_author_email_pattern")
        return typing.cast(typing.Optional["RepositoryRulesetRulesCommitAuthorEmailPattern"], result)

    @builtins.property
    def commit_message_pattern(
        self,
    ) -> typing.Optional["RepositoryRulesetRulesCommitMessagePattern"]:
        '''commit_message_pattern block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#commit_message_pattern RepositoryRuleset#commit_message_pattern}
        '''
        result = self._values.get("commit_message_pattern")
        return typing.cast(typing.Optional["RepositoryRulesetRulesCommitMessagePattern"], result)

    @builtins.property
    def committer_email_pattern(
        self,
    ) -> typing.Optional["RepositoryRulesetRulesCommitterEmailPattern"]:
        '''committer_email_pattern block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#committer_email_pattern RepositoryRuleset#committer_email_pattern}
        '''
        result = self._values.get("committer_email_pattern")
        return typing.cast(typing.Optional["RepositoryRulesetRulesCommitterEmailPattern"], result)

    @builtins.property
    def creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only allow users with bypass permission to create matching refs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#creation RepositoryRuleset#creation}
        '''
        result = self._values.get("creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only allow users with bypass permissions to delete matching refs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#deletion RepositoryRuleset#deletion}
        '''
        result = self._values.get("deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def merge_queue(self) -> typing.Optional["RepositoryRulesetRulesMergeQueue"]:
        '''merge_queue block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#merge_queue RepositoryRuleset#merge_queue}
        '''
        result = self._values.get("merge_queue")
        return typing.cast(typing.Optional["RepositoryRulesetRulesMergeQueue"], result)

    @builtins.property
    def non_fast_forward(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent users with push access from force pushing to branches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#non_fast_forward RepositoryRuleset#non_fast_forward}
        '''
        result = self._values.get("non_fast_forward")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pull_request(self) -> typing.Optional["RepositoryRulesetRulesPullRequest"]:
        '''pull_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pull_request RepositoryRuleset#pull_request}
        '''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional["RepositoryRulesetRulesPullRequest"], result)

    @builtins.property
    def required_code_scanning(
        self,
    ) -> typing.Optional["RepositoryRulesetRulesRequiredCodeScanning"]:
        '''required_code_scanning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_code_scanning RepositoryRuleset#required_code_scanning}
        '''
        result = self._values.get("required_code_scanning")
        return typing.cast(typing.Optional["RepositoryRulesetRulesRequiredCodeScanning"], result)

    @builtins.property
    def required_deployments(
        self,
    ) -> typing.Optional["RepositoryRulesetRulesRequiredDeployments"]:
        '''required_deployments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_deployments RepositoryRuleset#required_deployments}
        '''
        result = self._values.get("required_deployments")
        return typing.cast(typing.Optional["RepositoryRulesetRulesRequiredDeployments"], result)

    @builtins.property
    def required_linear_history(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent merge commits from being pushed to matching branches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_linear_history RepositoryRuleset#required_linear_history}
        '''
        result = self._values.get("required_linear_history")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_signatures(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Commits pushed to matching branches must have verified signatures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_signatures RepositoryRuleset#required_signatures}
        '''
        result = self._values.get("required_signatures")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_status_checks(
        self,
    ) -> typing.Optional["RepositoryRulesetRulesRequiredStatusChecks"]:
        '''required_status_checks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_status_checks RepositoryRuleset#required_status_checks}
        '''
        result = self._values.get("required_status_checks")
        return typing.cast(typing.Optional["RepositoryRulesetRulesRequiredStatusChecks"], result)

    @builtins.property
    def tag_name_pattern(
        self,
    ) -> typing.Optional["RepositoryRulesetRulesTagNamePattern"]:
        '''tag_name_pattern block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#tag_name_pattern RepositoryRuleset#tag_name_pattern}
        '''
        result = self._values.get("tag_name_pattern")
        return typing.cast(typing.Optional["RepositoryRulesetRulesTagNamePattern"], result)

    @builtins.property
    def update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Only allow users with bypass permission to update matching refs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#update RepositoryRuleset#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def update_allows_fetch_and_merge(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Branch can pull changes from its upstream repository.

        This is only applicable to forked repositories. Requires ``update`` to be set to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#update_allows_fetch_and_merge RepositoryRuleset#update_allows_fetch_and_merge}
        '''
        result = self._values.get("update_allows_fetch_and_merge")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesBranchNamePattern",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "pattern": "pattern",
        "name": "name",
        "negate": "negate",
    },
)
class RepositoryRulesetRulesBranchNamePattern:
    def __init__(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6feb1dff530932b5e3756f7dcfc468bffd7831f1543acc4b5e4b65b3b1aa2f2d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''The pattern to match with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''How this rule will appear to users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the rule will fail if the pattern matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRulesBranchNamePattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetRulesBranchNamePatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesBranchNamePatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c52f43fa5de3d8a540d313d57e9c5fbd810c61c5aa1b6897522631fa1bfb7c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a960aa76f16e2c14eb85ac87b2228276ea6abef6fc6e4dbf7a9a834b43618381)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88d7dd00eb6a5250db137bae1529f6b39eda42adacbeae4a826574287aa0c2cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d62437c08ccfc99bf14132d75fe618c89bc91bdc4ec3f3c6491aa5c996eba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81e9180c607c771e4e2942ef6cc012a01210ecf9d23a21db4be0a3240e60d43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RepositoryRulesetRulesBranchNamePattern]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesBranchNamePattern], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryRulesetRulesBranchNamePattern],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70fef9a8575523fb58aa506722b08e2375baa74db2861686728eaf1c29214259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesCommitAuthorEmailPattern",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "pattern": "pattern",
        "name": "name",
        "negate": "negate",
    },
)
class RepositoryRulesetRulesCommitAuthorEmailPattern:
    def __init__(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e866ccf8a6ad42901d82b114b73b4848cf5cf2ad07fec0c7623c603e109448)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''The pattern to match with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''How this rule will appear to users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the rule will fail if the pattern matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRulesCommitAuthorEmailPattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetRulesCommitAuthorEmailPatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesCommitAuthorEmailPatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c884e5be92cf0bad6431276edf75ceac89d4ff715216d1f97d9e7197cf48530a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fd5ddcfc312c613c2a8cc73e78c5264f0990c8b093e1d4f81366cb6e7bb2321)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a020393f7fcef1f88fa18a93b69ce1f626fa45de9a55568ddcac0dde1cdafb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603cdcfe47cdb30fc3148a60eecc965f46057d8ab80c0bfb58f8f31d921d40fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c175f2be7076775d20696302cae61e88010554b90db0893c04f4c0e00b8549df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RepositoryRulesetRulesCommitAuthorEmailPattern]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesCommitAuthorEmailPattern], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryRulesetRulesCommitAuthorEmailPattern],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82dc042afbd6e9246ec0ecc01293521b6f34a9e52fd254d4fd55b7b33c55662a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesCommitMessagePattern",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "pattern": "pattern",
        "name": "name",
        "negate": "negate",
    },
)
class RepositoryRulesetRulesCommitMessagePattern:
    def __init__(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691cde6a92b7792c9b04588c4a120b7192ada19c5e0d6572311e0a14d1f22c76)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''The pattern to match with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''How this rule will appear to users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the rule will fail if the pattern matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRulesCommitMessagePattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetRulesCommitMessagePatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesCommitMessagePatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c70425d0aec4e3b2b64368d5b61c497e90f05f2f2c9b9c8cd70bfeb289b659d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a7bcc9e2637624744665576cc9bd6911821598447d764a3a5dceb4b2c9c339d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__980c71c4c8f2eeaf987be0ffce97447a451d11e01124931245a5325085361ff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a8011e973c18ed58edc8edba2c6dba8691929a3b5da61fe76597c79eb92289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390f17568e1fb1368d37b997cb384a6f249b80159e295b88961fa53e9bb27520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RepositoryRulesetRulesCommitMessagePattern]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesCommitMessagePattern], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryRulesetRulesCommitMessagePattern],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__765c9c0733be17aad023eb7c409402f93bff8ff9dab64a50fa14ec9f43f800e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesCommitterEmailPattern",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "pattern": "pattern",
        "name": "name",
        "negate": "negate",
    },
)
class RepositoryRulesetRulesCommitterEmailPattern:
    def __init__(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b7952b3be953684e5186a709819d00dd98fab5560463618879c4bf817eaa640)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''The pattern to match with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''How this rule will appear to users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the rule will fail if the pattern matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRulesCommitterEmailPattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetRulesCommitterEmailPatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesCommitterEmailPatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aae294e47da374b4a09e5953298d0c1cfdb45306c89516527bc2e8a14fecffb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afc2dba7f5fc4797a3e12b2b2b4dd69925e20ea83277b8ef0436557ec6873bc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__718823d2b541802c49e24e4ad7522d7d726b0b1f02584497e143e9a834e6e644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc71e60e3eaeba81e16b2e6352365541624710d7d93e9a9ea074efc06a7cfeab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a326fe456228e9d34e700cae6ee0e3cecb4f8cec5b6ec8ef69066cde3734c384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RepositoryRulesetRulesCommitterEmailPattern]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesCommitterEmailPattern], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryRulesetRulesCommitterEmailPattern],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ce47b0050125ed3e424603b163faadafbb337ec76f2fd809d4d8c54e49369fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesMergeQueue",
    jsii_struct_bases=[],
    name_mapping={
        "check_response_timeout_minutes": "checkResponseTimeoutMinutes",
        "grouping_strategy": "groupingStrategy",
        "max_entries_to_build": "maxEntriesToBuild",
        "max_entries_to_merge": "maxEntriesToMerge",
        "merge_method": "mergeMethod",
        "min_entries_to_merge": "minEntriesToMerge",
        "min_entries_to_merge_wait_minutes": "minEntriesToMergeWaitMinutes",
    },
)
class RepositoryRulesetRulesMergeQueue:
    def __init__(
        self,
        *,
        check_response_timeout_minutes: typing.Optional[jsii.Number] = None,
        grouping_strategy: typing.Optional[builtins.str] = None,
        max_entries_to_build: typing.Optional[jsii.Number] = None,
        max_entries_to_merge: typing.Optional[jsii.Number] = None,
        merge_method: typing.Optional[builtins.str] = None,
        min_entries_to_merge: typing.Optional[jsii.Number] = None,
        min_entries_to_merge_wait_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param check_response_timeout_minutes: Maximum time for a required status check to report a conclusion. After this much time has elapsed, checks that have not reported a conclusion will be assumed to have failed. Defaults to ``60``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#check_response_timeout_minutes RepositoryRuleset#check_response_timeout_minutes}
        :param grouping_strategy: When set to ALLGREEN, the merge commit created by merge queue for each PR in the group must pass all required checks to merge. When set to HEADGREEN, only the commit at the head of the merge group, i.e. the commit containing changes from all of the PRs in the group, must pass its required checks to merge. Can be one of: ALLGREEN, HEADGREEN. Defaults to ``ALLGREEN``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#grouping_strategy RepositoryRuleset#grouping_strategy}
        :param max_entries_to_build: Limit the number of queued pull requests requesting checks and workflow runs at the same time. Defaults to ``5``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#max_entries_to_build RepositoryRuleset#max_entries_to_build}
        :param max_entries_to_merge: The maximum number of PRs that will be merged together in a group. Defaults to ``5``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#max_entries_to_merge RepositoryRuleset#max_entries_to_merge}
        :param merge_method: Method to use when merging changes from queued pull requests. Can be one of: MERGE, SQUASH, REBASE. Defaults to ``MERGE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#merge_method RepositoryRuleset#merge_method}
        :param min_entries_to_merge: The minimum number of PRs that will be merged together in a group. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#min_entries_to_merge RepositoryRuleset#min_entries_to_merge}
        :param min_entries_to_merge_wait_minutes: The time merge queue should wait after the first PR is added to the queue for the minimum group size to be met. After this time has elapsed, the minimum group size will be ignored and a smaller group will be merged. Defaults to ``5``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#min_entries_to_merge_wait_minutes RepositoryRuleset#min_entries_to_merge_wait_minutes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3452775c8f3c793f69f256709e9ddd218d135b4d6fa9c3ca33f61d5df56900d)
            check_type(argname="argument check_response_timeout_minutes", value=check_response_timeout_minutes, expected_type=type_hints["check_response_timeout_minutes"])
            check_type(argname="argument grouping_strategy", value=grouping_strategy, expected_type=type_hints["grouping_strategy"])
            check_type(argname="argument max_entries_to_build", value=max_entries_to_build, expected_type=type_hints["max_entries_to_build"])
            check_type(argname="argument max_entries_to_merge", value=max_entries_to_merge, expected_type=type_hints["max_entries_to_merge"])
            check_type(argname="argument merge_method", value=merge_method, expected_type=type_hints["merge_method"])
            check_type(argname="argument min_entries_to_merge", value=min_entries_to_merge, expected_type=type_hints["min_entries_to_merge"])
            check_type(argname="argument min_entries_to_merge_wait_minutes", value=min_entries_to_merge_wait_minutes, expected_type=type_hints["min_entries_to_merge_wait_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if check_response_timeout_minutes is not None:
            self._values["check_response_timeout_minutes"] = check_response_timeout_minutes
        if grouping_strategy is not None:
            self._values["grouping_strategy"] = grouping_strategy
        if max_entries_to_build is not None:
            self._values["max_entries_to_build"] = max_entries_to_build
        if max_entries_to_merge is not None:
            self._values["max_entries_to_merge"] = max_entries_to_merge
        if merge_method is not None:
            self._values["merge_method"] = merge_method
        if min_entries_to_merge is not None:
            self._values["min_entries_to_merge"] = min_entries_to_merge
        if min_entries_to_merge_wait_minutes is not None:
            self._values["min_entries_to_merge_wait_minutes"] = min_entries_to_merge_wait_minutes

    @builtins.property
    def check_response_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''Maximum time for a required status check to report a conclusion.

        After this much time has elapsed, checks that have not reported a conclusion will be assumed to have failed. Defaults to ``60``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#check_response_timeout_minutes RepositoryRuleset#check_response_timeout_minutes}
        '''
        result = self._values.get("check_response_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grouping_strategy(self) -> typing.Optional[builtins.str]:
        '''When set to ALLGREEN, the merge commit created by merge queue for each PR in the group must pass all required checks to merge.

        When set to HEADGREEN, only the commit at the head of the merge group, i.e. the commit containing changes from all of the PRs in the group, must pass its required checks to merge. Can be one of: ALLGREEN, HEADGREEN. Defaults to ``ALLGREEN``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#grouping_strategy RepositoryRuleset#grouping_strategy}
        '''
        result = self._values.get("grouping_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_entries_to_build(self) -> typing.Optional[jsii.Number]:
        '''Limit the number of queued pull requests requesting checks and workflow runs at the same time. Defaults to ``5``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#max_entries_to_build RepositoryRuleset#max_entries_to_build}
        '''
        result = self._values.get("max_entries_to_build")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_entries_to_merge(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of PRs that will be merged together in a group. Defaults to ``5``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#max_entries_to_merge RepositoryRuleset#max_entries_to_merge}
        '''
        result = self._values.get("max_entries_to_merge")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def merge_method(self) -> typing.Optional[builtins.str]:
        '''Method to use when merging changes from queued pull requests.

        Can be one of: MERGE, SQUASH, REBASE. Defaults to ``MERGE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#merge_method RepositoryRuleset#merge_method}
        '''
        result = self._values.get("merge_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_entries_to_merge(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of PRs that will be merged together in a group. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#min_entries_to_merge RepositoryRuleset#min_entries_to_merge}
        '''
        result = self._values.get("min_entries_to_merge")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_entries_to_merge_wait_minutes(self) -> typing.Optional[jsii.Number]:
        '''The time merge queue should wait after the first PR is added to the queue for the minimum group size to be met.

        After this time has elapsed, the minimum group size will be ignored and a smaller group will be merged. Defaults to ``5``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#min_entries_to_merge_wait_minutes RepositoryRuleset#min_entries_to_merge_wait_minutes}
        '''
        result = self._values.get("min_entries_to_merge_wait_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRulesMergeQueue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetRulesMergeQueueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesMergeQueueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c9c644b11979ad55f2e1a7055360c80abc1a09830eace4fcf231180013069e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCheckResponseTimeoutMinutes")
    def reset_check_response_timeout_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckResponseTimeoutMinutes", []))

    @jsii.member(jsii_name="resetGroupingStrategy")
    def reset_grouping_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupingStrategy", []))

    @jsii.member(jsii_name="resetMaxEntriesToBuild")
    def reset_max_entries_to_build(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxEntriesToBuild", []))

    @jsii.member(jsii_name="resetMaxEntriesToMerge")
    def reset_max_entries_to_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxEntriesToMerge", []))

    @jsii.member(jsii_name="resetMergeMethod")
    def reset_merge_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeMethod", []))

    @jsii.member(jsii_name="resetMinEntriesToMerge")
    def reset_min_entries_to_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinEntriesToMerge", []))

    @jsii.member(jsii_name="resetMinEntriesToMergeWaitMinutes")
    def reset_min_entries_to_merge_wait_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinEntriesToMergeWaitMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="checkResponseTimeoutMinutesInput")
    def check_response_timeout_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "checkResponseTimeoutMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="groupingStrategyInput")
    def grouping_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupingStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxEntriesToBuildInput")
    def max_entries_to_build_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxEntriesToBuildInput"))

    @builtins.property
    @jsii.member(jsii_name="maxEntriesToMergeInput")
    def max_entries_to_merge_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxEntriesToMergeInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeMethodInput")
    def merge_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="minEntriesToMergeInput")
    def min_entries_to_merge_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minEntriesToMergeInput"))

    @builtins.property
    @jsii.member(jsii_name="minEntriesToMergeWaitMinutesInput")
    def min_entries_to_merge_wait_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minEntriesToMergeWaitMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="checkResponseTimeoutMinutes")
    def check_response_timeout_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "checkResponseTimeoutMinutes"))

    @check_response_timeout_minutes.setter
    def check_response_timeout_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d513164ef625790be1588cdd118cf4e03074e9aa4c95ca6981148e5f991430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkResponseTimeoutMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupingStrategy")
    def grouping_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupingStrategy"))

    @grouping_strategy.setter
    def grouping_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b6be7b4fc3f10846d0d3fc332010882142768117719811970f1c22ff5f41a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupingStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxEntriesToBuild")
    def max_entries_to_build(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxEntriesToBuild"))

    @max_entries_to_build.setter
    def max_entries_to_build(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3efb4c8b12c7468d6a06b24f753a8a52fc14f28b881998e4c27aff3768935a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxEntriesToBuild", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxEntriesToMerge")
    def max_entries_to_merge(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxEntriesToMerge"))

    @max_entries_to_merge.setter
    def max_entries_to_merge(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03bfde593c6c118b01c1e35911786a0f2e5de24ab104e3d914c59adc4e56a3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxEntriesToMerge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeMethod")
    def merge_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeMethod"))

    @merge_method.setter
    def merge_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8c2a08ebb2f0f293b27aac437bd5801a359497036e9581f4ff0fb2abd9a4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minEntriesToMerge")
    def min_entries_to_merge(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minEntriesToMerge"))

    @min_entries_to_merge.setter
    def min_entries_to_merge(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2161588d66ae90e38da910d3da58cb6e7992ec876404c953f02fb515abc679d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minEntriesToMerge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minEntriesToMergeWaitMinutes")
    def min_entries_to_merge_wait_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minEntriesToMergeWaitMinutes"))

    @min_entries_to_merge_wait_minutes.setter
    def min_entries_to_merge_wait_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f936119411bf42f5fcb2c06468597126fcd96906493a0da8c027902b75344721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minEntriesToMergeWaitMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RepositoryRulesetRulesMergeQueue]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesMergeQueue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryRulesetRulesMergeQueue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e2bf1ab2cd3698e3a16734c6359a5fbf86fc3a93ccf19844b1ad72988b8d080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RepositoryRulesetRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaad3fed465c8a168ff582804366c27bb0cae761711165cda530d9368c09fbb9)
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
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        value = RepositoryRulesetRulesBranchNamePattern(
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
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        value = RepositoryRulesetRulesCommitAuthorEmailPattern(
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
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        value = RepositoryRulesetRulesCommitMessagePattern(
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
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        value = RepositoryRulesetRulesCommitterEmailPattern(
            operator=operator, pattern=pattern, name=name, negate=negate
        )

        return typing.cast(None, jsii.invoke(self, "putCommitterEmailPattern", [value]))

    @jsii.member(jsii_name="putMergeQueue")
    def put_merge_queue(
        self,
        *,
        check_response_timeout_minutes: typing.Optional[jsii.Number] = None,
        grouping_strategy: typing.Optional[builtins.str] = None,
        max_entries_to_build: typing.Optional[jsii.Number] = None,
        max_entries_to_merge: typing.Optional[jsii.Number] = None,
        merge_method: typing.Optional[builtins.str] = None,
        min_entries_to_merge: typing.Optional[jsii.Number] = None,
        min_entries_to_merge_wait_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param check_response_timeout_minutes: Maximum time for a required status check to report a conclusion. After this much time has elapsed, checks that have not reported a conclusion will be assumed to have failed. Defaults to ``60``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#check_response_timeout_minutes RepositoryRuleset#check_response_timeout_minutes}
        :param grouping_strategy: When set to ALLGREEN, the merge commit created by merge queue for each PR in the group must pass all required checks to merge. When set to HEADGREEN, only the commit at the head of the merge group, i.e. the commit containing changes from all of the PRs in the group, must pass its required checks to merge. Can be one of: ALLGREEN, HEADGREEN. Defaults to ``ALLGREEN``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#grouping_strategy RepositoryRuleset#grouping_strategy}
        :param max_entries_to_build: Limit the number of queued pull requests requesting checks and workflow runs at the same time. Defaults to ``5``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#max_entries_to_build RepositoryRuleset#max_entries_to_build}
        :param max_entries_to_merge: The maximum number of PRs that will be merged together in a group. Defaults to ``5``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#max_entries_to_merge RepositoryRuleset#max_entries_to_merge}
        :param merge_method: Method to use when merging changes from queued pull requests. Can be one of: MERGE, SQUASH, REBASE. Defaults to ``MERGE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#merge_method RepositoryRuleset#merge_method}
        :param min_entries_to_merge: The minimum number of PRs that will be merged together in a group. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#min_entries_to_merge RepositoryRuleset#min_entries_to_merge}
        :param min_entries_to_merge_wait_minutes: The time merge queue should wait after the first PR is added to the queue for the minimum group size to be met. After this time has elapsed, the minimum group size will be ignored and a smaller group will be merged. Defaults to ``5``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#min_entries_to_merge_wait_minutes RepositoryRuleset#min_entries_to_merge_wait_minutes}
        '''
        value = RepositoryRulesetRulesMergeQueue(
            check_response_timeout_minutes=check_response_timeout_minutes,
            grouping_strategy=grouping_strategy,
            max_entries_to_build=max_entries_to_build,
            max_entries_to_merge=max_entries_to_merge,
            merge_method=merge_method,
            min_entries_to_merge=min_entries_to_merge,
            min_entries_to_merge_wait_minutes=min_entries_to_merge_wait_minutes,
        )

        return typing.cast(None, jsii.invoke(self, "putMergeQueue", [value]))

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
        :param dismiss_stale_reviews_on_push: New, reviewable commits pushed will dismiss previous pull request review approvals. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#dismiss_stale_reviews_on_push RepositoryRuleset#dismiss_stale_reviews_on_push}
        :param require_code_owner_review: Require an approving review in pull requests that modify files that have a designated code owner. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#require_code_owner_review RepositoryRuleset#require_code_owner_review}
        :param required_approving_review_count: The number of approving reviews that are required before a pull request can be merged. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_approving_review_count RepositoryRuleset#required_approving_review_count}
        :param required_review_thread_resolution: All conversations on code must be resolved before a pull request can be merged. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_review_thread_resolution RepositoryRuleset#required_review_thread_resolution}
        :param require_last_push_approval: Whether the most recent reviewable push must be approved by someone other than the person who pushed it. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#require_last_push_approval RepositoryRuleset#require_last_push_approval}
        '''
        value = RepositoryRulesetRulesPullRequest(
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
        required_code_scanning_tool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param required_code_scanning_tool: required_code_scanning_tool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_code_scanning_tool RepositoryRuleset#required_code_scanning_tool}
        '''
        value = RepositoryRulesetRulesRequiredCodeScanning(
            required_code_scanning_tool=required_code_scanning_tool
        )

        return typing.cast(None, jsii.invoke(self, "putRequiredCodeScanning", [value]))

    @jsii.member(jsii_name="putRequiredDeployments")
    def put_required_deployments(
        self,
        *,
        required_deployment_environments: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param required_deployment_environments: The environments that must be successfully deployed to before branches can be merged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_deployment_environments RepositoryRuleset#required_deployment_environments}
        '''
        value = RepositoryRulesetRulesRequiredDeployments(
            required_deployment_environments=required_deployment_environments
        )

        return typing.cast(None, jsii.invoke(self, "putRequiredDeployments", [value]))

    @jsii.member(jsii_name="putRequiredStatusChecks")
    def put_required_status_checks(
        self,
        *,
        required_check: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RepositoryRulesetRulesRequiredStatusChecksRequiredCheck", typing.Dict[builtins.str, typing.Any]]]],
        do_not_enforce_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        strict_required_status_checks_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param required_check: required_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_check RepositoryRuleset#required_check}
        :param do_not_enforce_on_create: Allow repositories and branches to be created if a check would otherwise prohibit it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#do_not_enforce_on_create RepositoryRuleset#do_not_enforce_on_create}
        :param strict_required_status_checks_policy: Whether pull requests targeting a matching branch must be tested with the latest code. This setting will not take effect unless at least one status check is enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#strict_required_status_checks_policy RepositoryRuleset#strict_required_status_checks_policy}
        '''
        value = RepositoryRulesetRulesRequiredStatusChecks(
            required_check=required_check,
            do_not_enforce_on_create=do_not_enforce_on_create,
            strict_required_status_checks_policy=strict_required_status_checks_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putRequiredStatusChecks", [value]))

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
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        value = RepositoryRulesetRulesTagNamePattern(
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

    @jsii.member(jsii_name="resetMergeQueue")
    def reset_merge_queue(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeQueue", []))

    @jsii.member(jsii_name="resetNonFastForward")
    def reset_non_fast_forward(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonFastForward", []))

    @jsii.member(jsii_name="resetPullRequest")
    def reset_pull_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullRequest", []))

    @jsii.member(jsii_name="resetRequiredCodeScanning")
    def reset_required_code_scanning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredCodeScanning", []))

    @jsii.member(jsii_name="resetRequiredDeployments")
    def reset_required_deployments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredDeployments", []))

    @jsii.member(jsii_name="resetRequiredLinearHistory")
    def reset_required_linear_history(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredLinearHistory", []))

    @jsii.member(jsii_name="resetRequiredSignatures")
    def reset_required_signatures(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredSignatures", []))

    @jsii.member(jsii_name="resetRequiredStatusChecks")
    def reset_required_status_checks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredStatusChecks", []))

    @jsii.member(jsii_name="resetTagNamePattern")
    def reset_tag_name_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagNamePattern", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @jsii.member(jsii_name="resetUpdateAllowsFetchAndMerge")
    def reset_update_allows_fetch_and_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateAllowsFetchAndMerge", []))

    @builtins.property
    @jsii.member(jsii_name="branchNamePattern")
    def branch_name_pattern(
        self,
    ) -> RepositoryRulesetRulesBranchNamePatternOutputReference:
        return typing.cast(RepositoryRulesetRulesBranchNamePatternOutputReference, jsii.get(self, "branchNamePattern"))

    @builtins.property
    @jsii.member(jsii_name="commitAuthorEmailPattern")
    def commit_author_email_pattern(
        self,
    ) -> RepositoryRulesetRulesCommitAuthorEmailPatternOutputReference:
        return typing.cast(RepositoryRulesetRulesCommitAuthorEmailPatternOutputReference, jsii.get(self, "commitAuthorEmailPattern"))

    @builtins.property
    @jsii.member(jsii_name="commitMessagePattern")
    def commit_message_pattern(
        self,
    ) -> RepositoryRulesetRulesCommitMessagePatternOutputReference:
        return typing.cast(RepositoryRulesetRulesCommitMessagePatternOutputReference, jsii.get(self, "commitMessagePattern"))

    @builtins.property
    @jsii.member(jsii_name="committerEmailPattern")
    def committer_email_pattern(
        self,
    ) -> RepositoryRulesetRulesCommitterEmailPatternOutputReference:
        return typing.cast(RepositoryRulesetRulesCommitterEmailPatternOutputReference, jsii.get(self, "committerEmailPattern"))

    @builtins.property
    @jsii.member(jsii_name="mergeQueue")
    def merge_queue(self) -> RepositoryRulesetRulesMergeQueueOutputReference:
        return typing.cast(RepositoryRulesetRulesMergeQueueOutputReference, jsii.get(self, "mergeQueue"))

    @builtins.property
    @jsii.member(jsii_name="pullRequest")
    def pull_request(self) -> "RepositoryRulesetRulesPullRequestOutputReference":
        return typing.cast("RepositoryRulesetRulesPullRequestOutputReference", jsii.get(self, "pullRequest"))

    @builtins.property
    @jsii.member(jsii_name="requiredCodeScanning")
    def required_code_scanning(
        self,
    ) -> "RepositoryRulesetRulesRequiredCodeScanningOutputReference":
        return typing.cast("RepositoryRulesetRulesRequiredCodeScanningOutputReference", jsii.get(self, "requiredCodeScanning"))

    @builtins.property
    @jsii.member(jsii_name="requiredDeployments")
    def required_deployments(
        self,
    ) -> "RepositoryRulesetRulesRequiredDeploymentsOutputReference":
        return typing.cast("RepositoryRulesetRulesRequiredDeploymentsOutputReference", jsii.get(self, "requiredDeployments"))

    @builtins.property
    @jsii.member(jsii_name="requiredStatusChecks")
    def required_status_checks(
        self,
    ) -> "RepositoryRulesetRulesRequiredStatusChecksOutputReference":
        return typing.cast("RepositoryRulesetRulesRequiredStatusChecksOutputReference", jsii.get(self, "requiredStatusChecks"))

    @builtins.property
    @jsii.member(jsii_name="tagNamePattern")
    def tag_name_pattern(self) -> "RepositoryRulesetRulesTagNamePatternOutputReference":
        return typing.cast("RepositoryRulesetRulesTagNamePatternOutputReference", jsii.get(self, "tagNamePattern"))

    @builtins.property
    @jsii.member(jsii_name="branchNamePatternInput")
    def branch_name_pattern_input(
        self,
    ) -> typing.Optional[RepositoryRulesetRulesBranchNamePattern]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesBranchNamePattern], jsii.get(self, "branchNamePatternInput"))

    @builtins.property
    @jsii.member(jsii_name="commitAuthorEmailPatternInput")
    def commit_author_email_pattern_input(
        self,
    ) -> typing.Optional[RepositoryRulesetRulesCommitAuthorEmailPattern]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesCommitAuthorEmailPattern], jsii.get(self, "commitAuthorEmailPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="commitMessagePatternInput")
    def commit_message_pattern_input(
        self,
    ) -> typing.Optional[RepositoryRulesetRulesCommitMessagePattern]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesCommitMessagePattern], jsii.get(self, "commitMessagePatternInput"))

    @builtins.property
    @jsii.member(jsii_name="committerEmailPatternInput")
    def committer_email_pattern_input(
        self,
    ) -> typing.Optional[RepositoryRulesetRulesCommitterEmailPattern]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesCommitterEmailPattern], jsii.get(self, "committerEmailPatternInput"))

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
    @jsii.member(jsii_name="mergeQueueInput")
    def merge_queue_input(self) -> typing.Optional[RepositoryRulesetRulesMergeQueue]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesMergeQueue], jsii.get(self, "mergeQueueInput"))

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
    ) -> typing.Optional["RepositoryRulesetRulesPullRequest"]:
        return typing.cast(typing.Optional["RepositoryRulesetRulesPullRequest"], jsii.get(self, "pullRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredCodeScanningInput")
    def required_code_scanning_input(
        self,
    ) -> typing.Optional["RepositoryRulesetRulesRequiredCodeScanning"]:
        return typing.cast(typing.Optional["RepositoryRulesetRulesRequiredCodeScanning"], jsii.get(self, "requiredCodeScanningInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredDeploymentsInput")
    def required_deployments_input(
        self,
    ) -> typing.Optional["RepositoryRulesetRulesRequiredDeployments"]:
        return typing.cast(typing.Optional["RepositoryRulesetRulesRequiredDeployments"], jsii.get(self, "requiredDeploymentsInput"))

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
    ) -> typing.Optional["RepositoryRulesetRulesRequiredStatusChecks"]:
        return typing.cast(typing.Optional["RepositoryRulesetRulesRequiredStatusChecks"], jsii.get(self, "requiredStatusChecksInput"))

    @builtins.property
    @jsii.member(jsii_name="tagNamePatternInput")
    def tag_name_pattern_input(
        self,
    ) -> typing.Optional["RepositoryRulesetRulesTagNamePattern"]:
        return typing.cast(typing.Optional["RepositoryRulesetRulesTagNamePattern"], jsii.get(self, "tagNamePatternInput"))

    @builtins.property
    @jsii.member(jsii_name="updateAllowsFetchAndMergeInput")
    def update_allows_fetch_and_merge_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "updateAllowsFetchAndMergeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7951a50bb790fdcc6f8d2d9a838517c6a7d05e738b406b47896e138a3fd3300a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__625cac92597a997432e27bbf2bb125648fe2e80ef5d9abaebdcdc903e97bc6ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a49c23968ce0be87a4a8b69c400e548de766c3cfdf3dbdc75410714ff485c539)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2838d387427341224f2b53f6037c0feb04627d7975379ed88a3edd73e598a2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ac4c400ed2e5676023ea62e32e790b13e10e306f828456685d3b20fc6bd5ab8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0df03bbc5e642720ce02744075507c48b721d4813b4ca91be798d40cdbffb57e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateAllowsFetchAndMerge")
    def update_allows_fetch_and_merge(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "updateAllowsFetchAndMerge"))

    @update_allows_fetch_and_merge.setter
    def update_allows_fetch_and_merge(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e10917b4e489c1662b8fc20e9ebc1ad9e042cfffe39e2e1780de2a53c5c003f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateAllowsFetchAndMerge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RepositoryRulesetRules]:
        return typing.cast(typing.Optional[RepositoryRulesetRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RepositoryRulesetRules]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee6ddaecc3f5dcdc39f491ed1b90c9c1146329c894adda25e098d6ca96691304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesPullRequest",
    jsii_struct_bases=[],
    name_mapping={
        "dismiss_stale_reviews_on_push": "dismissStaleReviewsOnPush",
        "require_code_owner_review": "requireCodeOwnerReview",
        "required_approving_review_count": "requiredApprovingReviewCount",
        "required_review_thread_resolution": "requiredReviewThreadResolution",
        "require_last_push_approval": "requireLastPushApproval",
    },
)
class RepositoryRulesetRulesPullRequest:
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
        :param dismiss_stale_reviews_on_push: New, reviewable commits pushed will dismiss previous pull request review approvals. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#dismiss_stale_reviews_on_push RepositoryRuleset#dismiss_stale_reviews_on_push}
        :param require_code_owner_review: Require an approving review in pull requests that modify files that have a designated code owner. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#require_code_owner_review RepositoryRuleset#require_code_owner_review}
        :param required_approving_review_count: The number of approving reviews that are required before a pull request can be merged. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_approving_review_count RepositoryRuleset#required_approving_review_count}
        :param required_review_thread_resolution: All conversations on code must be resolved before a pull request can be merged. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_review_thread_resolution RepositoryRuleset#required_review_thread_resolution}
        :param require_last_push_approval: Whether the most recent reviewable push must be approved by someone other than the person who pushed it. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#require_last_push_approval RepositoryRuleset#require_last_push_approval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5710d1fd0fd967e50dd4923d121188f4d457d154e37d24fb94bad9a2eb190d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#dismiss_stale_reviews_on_push RepositoryRuleset#dismiss_stale_reviews_on_push}
        '''
        result = self._values.get("dismiss_stale_reviews_on_push")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_code_owner_review(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require an approving review in pull requests that modify files that have a designated code owner. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#require_code_owner_review RepositoryRuleset#require_code_owner_review}
        '''
        result = self._values.get("require_code_owner_review")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_approving_review_count(self) -> typing.Optional[jsii.Number]:
        '''The number of approving reviews that are required before a pull request can be merged. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_approving_review_count RepositoryRuleset#required_approving_review_count}
        '''
        result = self._values.get("required_approving_review_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def required_review_thread_resolution(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''All conversations on code must be resolved before a pull request can be merged. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_review_thread_resolution RepositoryRuleset#required_review_thread_resolution}
        '''
        result = self._values.get("required_review_thread_resolution")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_last_push_approval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the most recent reviewable push must be approved by someone other than the person who pushed it.

        Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#require_last_push_approval RepositoryRuleset#require_last_push_approval}
        '''
        result = self._values.get("require_last_push_approval")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRulesPullRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetRulesPullRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesPullRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10ba1f34c8b7d2a84cbb8484451b4024914906413f15e5c2124823c2c3fffb88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29430e43bc1b48f884cf407b657b801567c1998979eb9e9f913a7564e8b56c83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__399f9f7f23fbfdadb53d8cb431d52cb845675f58cfdcfa105e43be1a4554334a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireCodeOwnerReview", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredApprovingReviewCount")
    def required_approving_review_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requiredApprovingReviewCount"))

    @required_approving_review_count.setter
    def required_approving_review_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c9794d7be7b2ee01b943b12620af3c40816432461344391a26e88229f40260)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1edf9d1a4906ebf62c2b5b9138f48302db062e15a05917f699d938d2cdca6b80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1edf7d8f064b253f2b5b3858caca24c672cb0411b34433cf29e0198cd76aeacf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireLastPushApproval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RepositoryRulesetRulesPullRequest]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesPullRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryRulesetRulesPullRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb4b2b6716776fbc5b106e7009db7f8a9a87a391d7f4824cf6ac56ea83ad29af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesRequiredCodeScanning",
    jsii_struct_bases=[],
    name_mapping={"required_code_scanning_tool": "requiredCodeScanningTool"},
)
class RepositoryRulesetRulesRequiredCodeScanning:
    def __init__(
        self,
        *,
        required_code_scanning_tool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param required_code_scanning_tool: required_code_scanning_tool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_code_scanning_tool RepositoryRuleset#required_code_scanning_tool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1432e98853fa6b5b19fea9e2c395654457ae945c965e546ba902f47d4be85d3b)
            check_type(argname="argument required_code_scanning_tool", value=required_code_scanning_tool, expected_type=type_hints["required_code_scanning_tool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "required_code_scanning_tool": required_code_scanning_tool,
        }

    @builtins.property
    def required_code_scanning_tool(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool"]]:
        '''required_code_scanning_tool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_code_scanning_tool RepositoryRuleset#required_code_scanning_tool}
        '''
        result = self._values.get("required_code_scanning_tool")
        assert result is not None, "Required property 'required_code_scanning_tool' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRulesRequiredCodeScanning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetRulesRequiredCodeScanningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesRequiredCodeScanningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80c91137cce33b6b96ebd883fe4d81c02309716a71ecb44de362f3261db2313a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequiredCodeScanningTool")
    def put_required_code_scanning_tool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb7f2dc2f9288c6d07d6806f5663cd75fd05d4d825b49d4525d50970c9053e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequiredCodeScanningTool", [value]))

    @builtins.property
    @jsii.member(jsii_name="requiredCodeScanningTool")
    def required_code_scanning_tool(
        self,
    ) -> "RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningToolList":
        return typing.cast("RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningToolList", jsii.get(self, "requiredCodeScanningTool"))

    @builtins.property
    @jsii.member(jsii_name="requiredCodeScanningToolInput")
    def required_code_scanning_tool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool"]]], jsii.get(self, "requiredCodeScanningToolInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RepositoryRulesetRulesRequiredCodeScanning]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesRequiredCodeScanning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryRulesetRulesRequiredCodeScanning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3535dca1ba9da895ae8ce6fd84172fee55a5cfc5081f2a64c7d5d707fe5555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool",
    jsii_struct_bases=[],
    name_mapping={
        "alerts_threshold": "alertsThreshold",
        "security_alerts_threshold": "securityAlertsThreshold",
        "tool": "tool",
    },
)
class RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool:
    def __init__(
        self,
        *,
        alerts_threshold: builtins.str,
        security_alerts_threshold: builtins.str,
        tool: builtins.str,
    ) -> None:
        '''
        :param alerts_threshold: The severity level at which code scanning results that raise alerts block a reference update. Can be one of: ``none``, ``errors``, ``errors_and_warnings``, ``all``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#alerts_threshold RepositoryRuleset#alerts_threshold}
        :param security_alerts_threshold: The severity level at which code scanning results that raise security alerts block a reference update. Can be one of: ``none``, ``critical``, ``high_or_higher``, ``medium_or_higher``, ``all``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#security_alerts_threshold RepositoryRuleset#security_alerts_threshold}
        :param tool: The name of a code scanning tool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#tool RepositoryRuleset#tool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddf31c248cb1e451dd84116bc9e9875fa05b80457197d33480397e6eaadca527)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#alerts_threshold RepositoryRuleset#alerts_threshold}
        '''
        result = self._values.get("alerts_threshold")
        assert result is not None, "Required property 'alerts_threshold' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_alerts_threshold(self) -> builtins.str:
        '''The severity level at which code scanning results that raise security alerts block a reference update.

        Can be one of: ``none``, ``critical``, ``high_or_higher``, ``medium_or_higher``, ``all``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#security_alerts_threshold RepositoryRuleset#security_alerts_threshold}
        '''
        result = self._values.get("security_alerts_threshold")
        assert result is not None, "Required property 'security_alerts_threshold' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tool(self) -> builtins.str:
        '''The name of a code scanning tool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#tool RepositoryRuleset#tool}
        '''
        result = self._values.get("tool")
        assert result is not None, "Required property 'tool' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningToolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningToolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecb0e9dc58439e6609ba53b207ed5b5f28eb16bb7b50105e43ac9ed1278d37c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningToolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868a77414f1a28344dd38415611cde272dde7539be36f94d51666b604a4a0906)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningToolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f88ea448e1a8185e535c9157ece4e32352c4fac9a6efd0628c1ca60fe5d74387)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e344a28f71e63b7ac90f4ed7466323acba4589b9af44547ecef9ba07aa1bde14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52bdb700232d9878b1d96bbb6e043bc72818027b658181a9d1778c7221ee811f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f946c2a6fd549d9b9643c948bb5a241b67481005c82448b2b48cd47f252a0ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningToolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningToolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3293ccfe981c952e1b85a9dcb337c95e6c82890f53f6443beba5045c8e6a91f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fabaa957cbf27c18d41d0a81e1e689ff8c0bf56a70ede21892bcb32bf3b5009e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alertsThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityAlertsThreshold")
    def security_alerts_threshold(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityAlertsThreshold"))

    @security_alerts_threshold.setter
    def security_alerts_threshold(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4992eec9fe55564e11033f42701efbf1729be069d70e149bcc52ec23f4525c4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityAlertsThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tool")
    def tool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tool"))

    @tool.setter
    def tool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec49e8a73e4c6607a8ccbcabd95436f543a98480f755f4c95ff65bfc4d16292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd0d7038b0b3fca2a6d2ced2ab39c2102472dd5f3cf55e9b2ff12c40bf87914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesRequiredDeployments",
    jsii_struct_bases=[],
    name_mapping={
        "required_deployment_environments": "requiredDeploymentEnvironments",
    },
)
class RepositoryRulesetRulesRequiredDeployments:
    def __init__(
        self,
        *,
        required_deployment_environments: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param required_deployment_environments: The environments that must be successfully deployed to before branches can be merged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_deployment_environments RepositoryRuleset#required_deployment_environments}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ced12fa2738039b95b9d2609099cf5ab7dc1c0f63a55f09b41d8520aca3793)
            check_type(argname="argument required_deployment_environments", value=required_deployment_environments, expected_type=type_hints["required_deployment_environments"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "required_deployment_environments": required_deployment_environments,
        }

    @builtins.property
    def required_deployment_environments(self) -> typing.List[builtins.str]:
        '''The environments that must be successfully deployed to before branches can be merged.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_deployment_environments RepositoryRuleset#required_deployment_environments}
        '''
        result = self._values.get("required_deployment_environments")
        assert result is not None, "Required property 'required_deployment_environments' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRulesRequiredDeployments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetRulesRequiredDeploymentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesRequiredDeploymentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3928fb0186ffc33362b161d730c94c53391b6d70a71b54a314ab17dc7288115d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="requiredDeploymentEnvironmentsInput")
    def required_deployment_environments_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "requiredDeploymentEnvironmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredDeploymentEnvironments")
    def required_deployment_environments(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requiredDeploymentEnvironments"))

    @required_deployment_environments.setter
    def required_deployment_environments(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9098162894a1c6b398d92f90c60420f140a46ff0e89d427d2e6fb1df855a5eaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredDeploymentEnvironments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RepositoryRulesetRulesRequiredDeployments]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesRequiredDeployments], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryRulesetRulesRequiredDeployments],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d09db2553510261abdab20d9db85860c8d2e4a06516e0c1804769de4fe65866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesRequiredStatusChecks",
    jsii_struct_bases=[],
    name_mapping={
        "required_check": "requiredCheck",
        "do_not_enforce_on_create": "doNotEnforceOnCreate",
        "strict_required_status_checks_policy": "strictRequiredStatusChecksPolicy",
    },
)
class RepositoryRulesetRulesRequiredStatusChecks:
    def __init__(
        self,
        *,
        required_check: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RepositoryRulesetRulesRequiredStatusChecksRequiredCheck", typing.Dict[builtins.str, typing.Any]]]],
        do_not_enforce_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        strict_required_status_checks_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param required_check: required_check block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_check RepositoryRuleset#required_check}
        :param do_not_enforce_on_create: Allow repositories and branches to be created if a check would otherwise prohibit it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#do_not_enforce_on_create RepositoryRuleset#do_not_enforce_on_create}
        :param strict_required_status_checks_policy: Whether pull requests targeting a matching branch must be tested with the latest code. This setting will not take effect unless at least one status check is enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#strict_required_status_checks_policy RepositoryRuleset#strict_required_status_checks_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8e47ed9da4ad257544f947f9a0d6f1f595a975b1fa6fbb91de618ff3bd8bc90)
            check_type(argname="argument required_check", value=required_check, expected_type=type_hints["required_check"])
            check_type(argname="argument do_not_enforce_on_create", value=do_not_enforce_on_create, expected_type=type_hints["do_not_enforce_on_create"])
            check_type(argname="argument strict_required_status_checks_policy", value=strict_required_status_checks_policy, expected_type=type_hints["strict_required_status_checks_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "required_check": required_check,
        }
        if do_not_enforce_on_create is not None:
            self._values["do_not_enforce_on_create"] = do_not_enforce_on_create
        if strict_required_status_checks_policy is not None:
            self._values["strict_required_status_checks_policy"] = strict_required_status_checks_policy

    @builtins.property
    def required_check(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryRulesetRulesRequiredStatusChecksRequiredCheck"]]:
        '''required_check block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#required_check RepositoryRuleset#required_check}
        '''
        result = self._values.get("required_check")
        assert result is not None, "Required property 'required_check' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryRulesetRulesRequiredStatusChecksRequiredCheck"]], result)

    @builtins.property
    def do_not_enforce_on_create(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow repositories and branches to be created if a check would otherwise prohibit it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#do_not_enforce_on_create RepositoryRuleset#do_not_enforce_on_create}
        '''
        result = self._values.get("do_not_enforce_on_create")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def strict_required_status_checks_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether pull requests targeting a matching branch must be tested with the latest code.

        This setting will not take effect unless at least one status check is enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#strict_required_status_checks_policy RepositoryRuleset#strict_required_status_checks_policy}
        '''
        result = self._values.get("strict_required_status_checks_policy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRulesRequiredStatusChecks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetRulesRequiredStatusChecksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesRequiredStatusChecksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19cb1db7c59954973a3d52a70ffb7bbb876cd574f3f3bd871f903eed483ccfa5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRequiredCheck")
    def put_required_check(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RepositoryRulesetRulesRequiredStatusChecksRequiredCheck", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b204cbb91ded9937fa516b331a32f536ca2636797d8780efd46b864e5de33aca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequiredCheck", [value]))

    @jsii.member(jsii_name="resetDoNotEnforceOnCreate")
    def reset_do_not_enforce_on_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDoNotEnforceOnCreate", []))

    @jsii.member(jsii_name="resetStrictRequiredStatusChecksPolicy")
    def reset_strict_required_status_checks_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictRequiredStatusChecksPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="requiredCheck")
    def required_check(
        self,
    ) -> "RepositoryRulesetRulesRequiredStatusChecksRequiredCheckList":
        return typing.cast("RepositoryRulesetRulesRequiredStatusChecksRequiredCheckList", jsii.get(self, "requiredCheck"))

    @builtins.property
    @jsii.member(jsii_name="doNotEnforceOnCreateInput")
    def do_not_enforce_on_create_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "doNotEnforceOnCreateInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredCheckInput")
    def required_check_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryRulesetRulesRequiredStatusChecksRequiredCheck"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryRulesetRulesRequiredStatusChecksRequiredCheck"]]], jsii.get(self, "requiredCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="strictRequiredStatusChecksPolicyInput")
    def strict_required_status_checks_policy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "strictRequiredStatusChecksPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="doNotEnforceOnCreate")
    def do_not_enforce_on_create(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "doNotEnforceOnCreate"))

    @do_not_enforce_on_create.setter
    def do_not_enforce_on_create(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9e156c8b8f93190f94efaaa93c28068c0521e5cbc6a380ca7bc4faeaded583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "doNotEnforceOnCreate", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__5e2a81977d0e1b8a645be0ba904c39b4161078b6476e2170c886eb3c99f3e576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictRequiredStatusChecksPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RepositoryRulesetRulesRequiredStatusChecks]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesRequiredStatusChecks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryRulesetRulesRequiredStatusChecks],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c892b468e43d3775011a2084c4a8f2ce225814d7b3da1e70d2215f81734158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesRequiredStatusChecksRequiredCheck",
    jsii_struct_bases=[],
    name_mapping={"context": "context", "integration_id": "integrationId"},
)
class RepositoryRulesetRulesRequiredStatusChecksRequiredCheck:
    def __init__(
        self,
        *,
        context: builtins.str,
        integration_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param context: The status check context name that must be present on the commit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#context RepositoryRuleset#context}
        :param integration_id: The optional integration ID that this status check must originate from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#integration_id RepositoryRuleset#integration_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7dacbef4f66c4ee0151664295d0cb085b49c39bc9328b15c5f5d7e6a69299e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#context RepositoryRuleset#context}
        '''
        result = self._values.get("context")
        assert result is not None, "Required property 'context' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration_id(self) -> typing.Optional[jsii.Number]:
        '''The optional integration ID that this status check must originate from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#integration_id RepositoryRuleset#integration_id}
        '''
        result = self._values.get("integration_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRulesRequiredStatusChecksRequiredCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetRulesRequiredStatusChecksRequiredCheckList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesRequiredStatusChecksRequiredCheckList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25dd732a73e3eb640ef4634483d330d0eea7a9d1e301f175bbea38492fd0fc2f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RepositoryRulesetRulesRequiredStatusChecksRequiredCheckOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f76898b32f88cda5b0f4dd4ad67a6c88e8e9b8a584fffb430a67886d410f53)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RepositoryRulesetRulesRequiredStatusChecksRequiredCheckOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb92acb5aa01a0c528e0d98345b5ebbe194878199d7c443338eb0c6ad7555563)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fec6ff36ba917c484c46d3ec02a0f8b67982492258690437f4a8e4e439c5a1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c8788f6da0f6c01055241572b8f6c76aad02a4398d866a13c4b96430136cb74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetRulesRequiredStatusChecksRequiredCheck]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetRulesRequiredStatusChecksRequiredCheck]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetRulesRequiredStatusChecksRequiredCheck]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b140870acea44f766be2cf81453c6ee4fcb695c21170f76e0b2b00a0ea0cf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RepositoryRulesetRulesRequiredStatusChecksRequiredCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesRequiredStatusChecksRequiredCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a88637e6bfa6465d7bd022d8a437b19f6ac8adc4da04ac70db45a74279541ca2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99330b0493115f9cdd1187399a71065e76d1df1515c24d7127ef8295683e3461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "integrationId"))

    @integration_id.setter
    def integration_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a1375c6aa433d7a04d3ba3fc9ed371ce9e4e9c5fd5eb53eccaaaa4f671345ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryRulesetRulesRequiredStatusChecksRequiredCheck]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryRulesetRulesRequiredStatusChecksRequiredCheck]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryRulesetRulesRequiredStatusChecksRequiredCheck]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3fcd3b6f53b2e3e0ac7374faa1345d24f3e8a03842a220204655c427a34ae1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesTagNamePattern",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "pattern": "pattern",
        "name": "name",
        "negate": "negate",
    },
)
class RepositoryRulesetRulesTagNamePattern:
    def __init__(
        self,
        *,
        operator: builtins.str,
        pattern: builtins.str,
        name: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param operator: The operator to use for matching. Can be one of: ``starts_with``, ``ends_with``, ``contains``, ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        :param pattern: The pattern to match with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        :param name: How this rule will appear to users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        :param negate: If true, the rule will fail if the pattern matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4191059556fd8d13bb47695ed466610498508dbdd5a6b6dba0d8c07fdb2369)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#operator RepositoryRuleset#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''The pattern to match with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#pattern RepositoryRuleset#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''How this rule will appear to users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#name RepositoryRuleset#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the rule will fail if the pattern matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_ruleset#negate RepositoryRuleset#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRulesetRulesTagNamePattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryRulesetRulesTagNamePatternOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryRuleset.RepositoryRulesetRulesTagNamePatternOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7a7bf30701337a73c5fc03df53f3821216ca461debd2e6cdc2bd2777edf442d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41ba7b62322b69419030c7a98207462e5f658ae7396892669b28459c02d22846)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d78a854c6a9f4800dc2dbacc8cbfbc55dd3580edfc677c680edb8adc1f598e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df415937484f4f58047d42a02a35f417b5b65a95c7df0b5dccd645fe3a70608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc37b62d1d7f0bd7c0f752e6306208bb9aee10065d6c15f6362420656c4c232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RepositoryRulesetRulesTagNamePattern]:
        return typing.cast(typing.Optional[RepositoryRulesetRulesTagNamePattern], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryRulesetRulesTagNamePattern],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__216353ae7b7bb0ff78237f0c709b119877eaa8b01e4096ed1fa5aaf5ed3740e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RepositoryRuleset",
    "RepositoryRulesetBypassActors",
    "RepositoryRulesetBypassActorsList",
    "RepositoryRulesetBypassActorsOutputReference",
    "RepositoryRulesetConditions",
    "RepositoryRulesetConditionsOutputReference",
    "RepositoryRulesetConditionsRefName",
    "RepositoryRulesetConditionsRefNameOutputReference",
    "RepositoryRulesetConfig",
    "RepositoryRulesetRules",
    "RepositoryRulesetRulesBranchNamePattern",
    "RepositoryRulesetRulesBranchNamePatternOutputReference",
    "RepositoryRulesetRulesCommitAuthorEmailPattern",
    "RepositoryRulesetRulesCommitAuthorEmailPatternOutputReference",
    "RepositoryRulesetRulesCommitMessagePattern",
    "RepositoryRulesetRulesCommitMessagePatternOutputReference",
    "RepositoryRulesetRulesCommitterEmailPattern",
    "RepositoryRulesetRulesCommitterEmailPatternOutputReference",
    "RepositoryRulesetRulesMergeQueue",
    "RepositoryRulesetRulesMergeQueueOutputReference",
    "RepositoryRulesetRulesOutputReference",
    "RepositoryRulesetRulesPullRequest",
    "RepositoryRulesetRulesPullRequestOutputReference",
    "RepositoryRulesetRulesRequiredCodeScanning",
    "RepositoryRulesetRulesRequiredCodeScanningOutputReference",
    "RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool",
    "RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningToolList",
    "RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningToolOutputReference",
    "RepositoryRulesetRulesRequiredDeployments",
    "RepositoryRulesetRulesRequiredDeploymentsOutputReference",
    "RepositoryRulesetRulesRequiredStatusChecks",
    "RepositoryRulesetRulesRequiredStatusChecksOutputReference",
    "RepositoryRulesetRulesRequiredStatusChecksRequiredCheck",
    "RepositoryRulesetRulesRequiredStatusChecksRequiredCheckList",
    "RepositoryRulesetRulesRequiredStatusChecksRequiredCheckOutputReference",
    "RepositoryRulesetRulesTagNamePattern",
    "RepositoryRulesetRulesTagNamePatternOutputReference",
]

publication.publish()

def _typecheckingstub__53279645c069276d4082bf54449f7fa421c295085e74152004c5c91574ec4c34(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enforcement: builtins.str,
    name: builtins.str,
    rules: typing.Union[RepositoryRulesetRules, typing.Dict[builtins.str, typing.Any]],
    target: builtins.str,
    bypass_actors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RepositoryRulesetBypassActors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    conditions: typing.Optional[typing.Union[RepositoryRulesetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__4ece29a0777386e19090e4ba8a22f753dae76867973b9c15753a6cc4175eaef7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9b1464e3f8fbb272e52a265cc64decc8f12d456505b46c7780d8df262e8e38(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RepositoryRulesetBypassActors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0834989dfb73b2358a7b9eee89c980500752e5ba7c0fdeec8702e42f2d69b703(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75299856d0c32f805d1e71c83ef01ef6e34b075d17fb46be0fe5df0c4981002(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b83181f79362ede70bdbfc1563f0d77da4b3d0f2766193c88563418262adf29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2c3e92cc472434bad498398bf30562de5cedc912cc1e8b893ad0747e44dca6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb5f15dc9e585f322f093627c09fcdde843532f5547c118353fa8aebf8be2ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b113f8eb65ef947d85bbb9023fc2306f7cd3f8bc22ebdc38135400f20ead774(
    *,
    actor_id: jsii.Number,
    actor_type: builtins.str,
    bypass_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11bd1677cad3721d805ef05d277463671de5223b127c2f0b6d8aad249b8a746(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0695c61e16c05ecfeb5d0a08b1689a22dbdd0fb191ea3dfc96c17f462cc64dd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0efb674fc34f95350206a942886ac061429b423def93af98205d5f3aac4b24a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eba553f86eca2b7e86729b7671a9eac76c90f3f4bc3106c3c5de391b5f07d06(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fd3ef470fecf3e81c9dc73af65aee050c39870319f13b472471f24e860af80(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12dc9bc7b8e37b0cf9bc65323fc580fc5e244ab2cbb31d30c475cfe34a4cb79(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetBypassActors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42f0caddbae1a435cb51c4cafe761cf4776d297f9bb68c87d0bdb8ff22de912(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f263ee75bc019cf69b93b46582b0bb71b7f10d24dd9977492e0b948eaa6609b8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b6cdf17f41002323313e65e36225580f2c0d040fe30a1e558b01dcab373dc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34d437e2022d5c6f980308865064f12858f6291fce5af342d6dab8d046b05a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6e341bcdf7ee408097128baacda62ba5b54ebff03d283c896c486e83499b84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryRulesetBypassActors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15d442be132dc3099287a32ff3e984f05e9396b93ad69f6d9be0c194daeb698(
    *,
    ref_name: typing.Union[RepositoryRulesetConditionsRefName, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2dd1738c775d5258fec2391c0a8a44303428fc3fd9a224d4a7ba4ffeeb0e72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4358190746360641a38b0106338f0784aeae3383eb30ebd0fdbdd7a37d5ae5(
    value: typing.Optional[RepositoryRulesetConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c4c98adc74312f53208d238205844b70cd80142c1e2b4b2b95d1329cf654c9(
    *,
    exclude: typing.Sequence[builtins.str],
    include: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8289ecf2b395f25af8db19c42adddf6e662561bd1ebac1997232a722eac6a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2c86789a36029655b2803423bcb19c9fcf670a74240c473ee797e919dd8bc8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47b481b3bc0ddb2fcfa583604a650a99e4520c5f19665695362e171106da1a7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0bcd2a38adfd58db6eb83106c457da08f2acde2a46777f85d5af8637a1ac30(
    value: typing.Optional[RepositoryRulesetConditionsRefName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd935179a0b5de3525aae4445b5b9f9cf2143c7fc2d8eb5b083f539a21243164(
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
    rules: typing.Union[RepositoryRulesetRules, typing.Dict[builtins.str, typing.Any]],
    target: builtins.str,
    bypass_actors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RepositoryRulesetBypassActors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    conditions: typing.Optional[typing.Union[RepositoryRulesetConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd5b2598496ce154f58d07f1ccc6b67c083a48a52f2a5e895e5dc19cc81eb5d(
    *,
    branch_name_pattern: typing.Optional[typing.Union[RepositoryRulesetRulesBranchNamePattern, typing.Dict[builtins.str, typing.Any]]] = None,
    commit_author_email_pattern: typing.Optional[typing.Union[RepositoryRulesetRulesCommitAuthorEmailPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    commit_message_pattern: typing.Optional[typing.Union[RepositoryRulesetRulesCommitMessagePattern, typing.Dict[builtins.str, typing.Any]]] = None,
    committer_email_pattern: typing.Optional[typing.Union[RepositoryRulesetRulesCommitterEmailPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    merge_queue: typing.Optional[typing.Union[RepositoryRulesetRulesMergeQueue, typing.Dict[builtins.str, typing.Any]]] = None,
    non_fast_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pull_request: typing.Optional[typing.Union[RepositoryRulesetRulesPullRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    required_code_scanning: typing.Optional[typing.Union[RepositoryRulesetRulesRequiredCodeScanning, typing.Dict[builtins.str, typing.Any]]] = None,
    required_deployments: typing.Optional[typing.Union[RepositoryRulesetRulesRequiredDeployments, typing.Dict[builtins.str, typing.Any]]] = None,
    required_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_signatures: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_status_checks: typing.Optional[typing.Union[RepositoryRulesetRulesRequiredStatusChecks, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_name_pattern: typing.Optional[typing.Union[RepositoryRulesetRulesTagNamePattern, typing.Dict[builtins.str, typing.Any]]] = None,
    update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    update_allows_fetch_and_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6feb1dff530932b5e3756f7dcfc468bffd7831f1543acc4b5e4b65b3b1aa2f2d(
    *,
    operator: builtins.str,
    pattern: builtins.str,
    name: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c52f43fa5de3d8a540d313d57e9c5fbd810c61c5aa1b6897522631fa1bfb7c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a960aa76f16e2c14eb85ac87b2228276ea6abef6fc6e4dbf7a9a834b43618381(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d7dd00eb6a5250db137bae1529f6b39eda42adacbeae4a826574287aa0c2cd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d62437c08ccfc99bf14132d75fe618c89bc91bdc4ec3f3c6491aa5c996eba5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81e9180c607c771e4e2942ef6cc012a01210ecf9d23a21db4be0a3240e60d43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70fef9a8575523fb58aa506722b08e2375baa74db2861686728eaf1c29214259(
    value: typing.Optional[RepositoryRulesetRulesBranchNamePattern],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e866ccf8a6ad42901d82b114b73b4848cf5cf2ad07fec0c7623c603e109448(
    *,
    operator: builtins.str,
    pattern: builtins.str,
    name: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c884e5be92cf0bad6431276edf75ceac89d4ff715216d1f97d9e7197cf48530a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd5ddcfc312c613c2a8cc73e78c5264f0990c8b093e1d4f81366cb6e7bb2321(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a020393f7fcef1f88fa18a93b69ce1f626fa45de9a55568ddcac0dde1cdafb5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603cdcfe47cdb30fc3148a60eecc965f46057d8ab80c0bfb58f8f31d921d40fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c175f2be7076775d20696302cae61e88010554b90db0893c04f4c0e00b8549df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82dc042afbd6e9246ec0ecc01293521b6f34a9e52fd254d4fd55b7b33c55662a(
    value: typing.Optional[RepositoryRulesetRulesCommitAuthorEmailPattern],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691cde6a92b7792c9b04588c4a120b7192ada19c5e0d6572311e0a14d1f22c76(
    *,
    operator: builtins.str,
    pattern: builtins.str,
    name: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70425d0aec4e3b2b64368d5b61c497e90f05f2f2c9b9c8cd70bfeb289b659d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7bcc9e2637624744665576cc9bd6911821598447d764a3a5dceb4b2c9c339d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980c71c4c8f2eeaf987be0ffce97447a451d11e01124931245a5325085361ff2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a8011e973c18ed58edc8edba2c6dba8691929a3b5da61fe76597c79eb92289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390f17568e1fb1368d37b997cb384a6f249b80159e295b88961fa53e9bb27520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765c9c0733be17aad023eb7c409402f93bff8ff9dab64a50fa14ec9f43f800e7(
    value: typing.Optional[RepositoryRulesetRulesCommitMessagePattern],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7952b3be953684e5186a709819d00dd98fab5560463618879c4bf817eaa640(
    *,
    operator: builtins.str,
    pattern: builtins.str,
    name: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae294e47da374b4a09e5953298d0c1cfdb45306c89516527bc2e8a14fecffb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc2dba7f5fc4797a3e12b2b2b4dd69925e20ea83277b8ef0436557ec6873bc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718823d2b541802c49e24e4ad7522d7d726b0b1f02584497e143e9a834e6e644(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc71e60e3eaeba81e16b2e6352365541624710d7d93e9a9ea074efc06a7cfeab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a326fe456228e9d34e700cae6ee0e3cecb4f8cec5b6ec8ef69066cde3734c384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce47b0050125ed3e424603b163faadafbb337ec76f2fd809d4d8c54e49369fd(
    value: typing.Optional[RepositoryRulesetRulesCommitterEmailPattern],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3452775c8f3c793f69f256709e9ddd218d135b4d6fa9c3ca33f61d5df56900d(
    *,
    check_response_timeout_minutes: typing.Optional[jsii.Number] = None,
    grouping_strategy: typing.Optional[builtins.str] = None,
    max_entries_to_build: typing.Optional[jsii.Number] = None,
    max_entries_to_merge: typing.Optional[jsii.Number] = None,
    merge_method: typing.Optional[builtins.str] = None,
    min_entries_to_merge: typing.Optional[jsii.Number] = None,
    min_entries_to_merge_wait_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9c644b11979ad55f2e1a7055360c80abc1a09830eace4fcf231180013069e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d513164ef625790be1588cdd118cf4e03074e9aa4c95ca6981148e5f991430(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b6be7b4fc3f10846d0d3fc332010882142768117719811970f1c22ff5f41a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3efb4c8b12c7468d6a06b24f753a8a52fc14f28b881998e4c27aff3768935a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03bfde593c6c118b01c1e35911786a0f2e5de24ab104e3d914c59adc4e56a3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8c2a08ebb2f0f293b27aac437bd5801a359497036e9581f4ff0fb2abd9a4dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2161588d66ae90e38da910d3da58cb6e7992ec876404c953f02fb515abc679d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f936119411bf42f5fcb2c06468597126fcd96906493a0da8c027902b75344721(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2bf1ab2cd3698e3a16734c6359a5fbf86fc3a93ccf19844b1ad72988b8d080(
    value: typing.Optional[RepositoryRulesetRulesMergeQueue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaad3fed465c8a168ff582804366c27bb0cae761711165cda530d9368c09fbb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7951a50bb790fdcc6f8d2d9a838517c6a7d05e738b406b47896e138a3fd3300a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625cac92597a997432e27bbf2bb125648fe2e80ef5d9abaebdcdc903e97bc6ae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49c23968ce0be87a4a8b69c400e548de766c3cfdf3dbdc75410714ff485c539(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2838d387427341224f2b53f6037c0feb04627d7975379ed88a3edd73e598a2e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac4c400ed2e5676023ea62e32e790b13e10e306f828456685d3b20fc6bd5ab8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df03bbc5e642720ce02744075507c48b721d4813b4ca91be798d40cdbffb57e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e10917b4e489c1662b8fc20e9ebc1ad9e042cfffe39e2e1780de2a53c5c003f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6ddaecc3f5dcdc39f491ed1b90c9c1146329c894adda25e098d6ca96691304(
    value: typing.Optional[RepositoryRulesetRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5710d1fd0fd967e50dd4923d121188f4d457d154e37d24fb94bad9a2eb190d(
    *,
    dismiss_stale_reviews_on_push: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_code_owner_review: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_approving_review_count: typing.Optional[jsii.Number] = None,
    required_review_thread_resolution: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_last_push_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ba1f34c8b7d2a84cbb8484451b4024914906413f15e5c2124823c2c3fffb88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29430e43bc1b48f884cf407b657b801567c1998979eb9e9f913a7564e8b56c83(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399f9f7f23fbfdadb53d8cb431d52cb845675f58cfdcfa105e43be1a4554334a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c9794d7be7b2ee01b943b12620af3c40816432461344391a26e88229f40260(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edf9d1a4906ebf62c2b5b9138f48302db062e15a05917f699d938d2cdca6b80(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edf7d8f064b253f2b5b3858caca24c672cb0411b34433cf29e0198cd76aeacf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4b2b6716776fbc5b106e7009db7f8a9a87a391d7f4824cf6ac56ea83ad29af(
    value: typing.Optional[RepositoryRulesetRulesPullRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1432e98853fa6b5b19fea9e2c395654457ae945c965e546ba902f47d4be85d3b(
    *,
    required_code_scanning_tool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c91137cce33b6b96ebd883fe4d81c02309716a71ecb44de362f3261db2313a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb7f2dc2f9288c6d07d6806f5663cd75fd05d4d825b49d4525d50970c9053e1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3535dca1ba9da895ae8ce6fd84172fee55a5cfc5081f2a64c7d5d707fe5555(
    value: typing.Optional[RepositoryRulesetRulesRequiredCodeScanning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf31c248cb1e451dd84116bc9e9875fa05b80457197d33480397e6eaadca527(
    *,
    alerts_threshold: builtins.str,
    security_alerts_threshold: builtins.str,
    tool: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb0e9dc58439e6609ba53b207ed5b5f28eb16bb7b50105e43ac9ed1278d37c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868a77414f1a28344dd38415611cde272dde7539be36f94d51666b604a4a0906(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88ea448e1a8185e535c9157ece4e32352c4fac9a6efd0628c1ca60fe5d74387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e344a28f71e63b7ac90f4ed7466323acba4589b9af44547ecef9ba07aa1bde14(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bdb700232d9878b1d96bbb6e043bc72818027b658181a9d1778c7221ee811f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f946c2a6fd549d9b9643c948bb5a241b67481005c82448b2b48cd47f252a0ee4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3293ccfe981c952e1b85a9dcb337c95e6c82890f53f6443beba5045c8e6a91f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabaa957cbf27c18d41d0a81e1e689ff8c0bf56a70ede21892bcb32bf3b5009e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4992eec9fe55564e11033f42701efbf1729be069d70e149bcc52ec23f4525c4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec49e8a73e4c6607a8ccbcabd95436f543a98480f755f4c95ff65bfc4d16292(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd0d7038b0b3fca2a6d2ced2ab39c2102472dd5f3cf55e9b2ff12c40bf87914(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryRulesetRulesRequiredCodeScanningRequiredCodeScanningTool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ced12fa2738039b95b9d2609099cf5ab7dc1c0f63a55f09b41d8520aca3793(
    *,
    required_deployment_environments: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3928fb0186ffc33362b161d730c94c53391b6d70a71b54a314ab17dc7288115d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9098162894a1c6b398d92f90c60420f140a46ff0e89d427d2e6fb1df855a5eaf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d09db2553510261abdab20d9db85860c8d2e4a06516e0c1804769de4fe65866(
    value: typing.Optional[RepositoryRulesetRulesRequiredDeployments],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e47ed9da4ad257544f947f9a0d6f1f595a975b1fa6fbb91de618ff3bd8bc90(
    *,
    required_check: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RepositoryRulesetRulesRequiredStatusChecksRequiredCheck, typing.Dict[builtins.str, typing.Any]]]],
    do_not_enforce_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    strict_required_status_checks_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19cb1db7c59954973a3d52a70ffb7bbb876cd574f3f3bd871f903eed483ccfa5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b204cbb91ded9937fa516b331a32f536ca2636797d8780efd46b864e5de33aca(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RepositoryRulesetRulesRequiredStatusChecksRequiredCheck, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9e156c8b8f93190f94efaaa93c28068c0521e5cbc6a380ca7bc4faeaded583(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2a81977d0e1b8a645be0ba904c39b4161078b6476e2170c886eb3c99f3e576(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c892b468e43d3775011a2084c4a8f2ce225814d7b3da1e70d2215f81734158(
    value: typing.Optional[RepositoryRulesetRulesRequiredStatusChecks],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7dacbef4f66c4ee0151664295d0cb085b49c39bc9328b15c5f5d7e6a69299e(
    *,
    context: builtins.str,
    integration_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25dd732a73e3eb640ef4634483d330d0eea7a9d1e301f175bbea38492fd0fc2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f76898b32f88cda5b0f4dd4ad67a6c88e8e9b8a584fffb430a67886d410f53(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb92acb5aa01a0c528e0d98345b5ebbe194878199d7c443338eb0c6ad7555563(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fec6ff36ba917c484c46d3ec02a0f8b67982492258690437f4a8e4e439c5a1c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c8788f6da0f6c01055241572b8f6c76aad02a4398d866a13c4b96430136cb74(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b140870acea44f766be2cf81453c6ee4fcb695c21170f76e0b2b00a0ea0cf0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryRulesetRulesRequiredStatusChecksRequiredCheck]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88637e6bfa6465d7bd022d8a437b19f6ac8adc4da04ac70db45a74279541ca2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99330b0493115f9cdd1187399a71065e76d1df1515c24d7127ef8295683e3461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1375c6aa433d7a04d3ba3fc9ed371ce9e4e9c5fd5eb53eccaaaa4f671345ec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fcd3b6f53b2e3e0ac7374faa1345d24f3e8a03842a220204655c427a34ae1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryRulesetRulesRequiredStatusChecksRequiredCheck]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4191059556fd8d13bb47695ed466610498508dbdd5a6b6dba0d8c07fdb2369(
    *,
    operator: builtins.str,
    pattern: builtins.str,
    name: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a7bf30701337a73c5fc03df53f3821216ca461debd2e6cdc2bd2777edf442d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ba7b62322b69419030c7a98207462e5f658ae7396892669b28459c02d22846(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78a854c6a9f4800dc2dbacc8cbfbc55dd3580edfc677c680edb8adc1f598e70(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df415937484f4f58047d42a02a35f417b5b65a95c7df0b5dccd645fe3a70608(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc37b62d1d7f0bd7c0f752e6306208bb9aee10065d6c15f6362420656c4c232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216353ae7b7bb0ff78237f0c709b119877eaa8b01e4096ed1fa5aaf5ed3740e7(
    value: typing.Optional[RepositoryRulesetRulesTagNamePattern],
) -> None:
    """Type checking stubs"""
    pass
