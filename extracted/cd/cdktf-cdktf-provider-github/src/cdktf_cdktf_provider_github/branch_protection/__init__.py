r'''
# `github_branch_protection`

Refer to the Terraform Registry for docs: [`github_branch_protection`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection).
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


class BranchProtection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.branchProtection.BranchProtection",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection github_branch_protection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        pattern: builtins.str,
        repository_id: builtins.str,
        allows_deletions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allows_force_pushes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        force_push_bypassers: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        lock_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_conversation_resolution: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_pull_request_reviews: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionRequiredPullRequestReviews", typing.Dict[builtins.str, typing.Any]]]]] = None,
        required_status_checks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionRequiredStatusChecks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        require_signed_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrict_pushes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionRestrictPushes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection github_branch_protection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param pattern: Identifies the protection rule pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#pattern BranchProtection#pattern}
        :param repository_id: The name or node ID of the repository associated with this branch protection rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#repository_id BranchProtection#repository_id}
        :param allows_deletions: Setting this to 'true' to allow the branch to be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#allows_deletions BranchProtection#allows_deletions}
        :param allows_force_pushes: Setting this to 'true' to allow force pushes on the branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#allows_force_pushes BranchProtection#allows_force_pushes}
        :param enforce_admins: Setting this to 'true' enforces status checks for repository administrators. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#enforce_admins BranchProtection#enforce_admins}
        :param force_push_bypassers: The list of actor Names/IDs that are allowed to bypass force push restrictions. Actor names must either begin with a '/' for users or the organization name followed by a '/' for teams. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#force_push_bypassers BranchProtection#force_push_bypassers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#id BranchProtection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lock_branch: Setting this to 'true' will make the branch read-only and preventing any pushes to it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#lock_branch BranchProtection#lock_branch}
        :param require_conversation_resolution: Setting this to 'true' requires all conversations on code must be resolved before a pull request can be merged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#require_conversation_resolution BranchProtection#require_conversation_resolution}
        :param required_linear_history: Setting this to 'true' enforces a linear commit Git history, which prevents anyone from pushing merge commits to a branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#required_linear_history BranchProtection#required_linear_history}
        :param required_pull_request_reviews: required_pull_request_reviews block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#required_pull_request_reviews BranchProtection#required_pull_request_reviews}
        :param required_status_checks: required_status_checks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#required_status_checks BranchProtection#required_status_checks}
        :param require_signed_commits: Setting this to 'true' requires all commits to be signed with GPG. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#require_signed_commits BranchProtection#require_signed_commits}
        :param restrict_pushes: restrict_pushes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#restrict_pushes BranchProtection#restrict_pushes}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d030729aabe2b9742e66c59c7dd2efaf5c966fdf7fbff191a75dce20978ddcba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BranchProtectionConfig(
            pattern=pattern,
            repository_id=repository_id,
            allows_deletions=allows_deletions,
            allows_force_pushes=allows_force_pushes,
            enforce_admins=enforce_admins,
            force_push_bypassers=force_push_bypassers,
            id=id,
            lock_branch=lock_branch,
            require_conversation_resolution=require_conversation_resolution,
            required_linear_history=required_linear_history,
            required_pull_request_reviews=required_pull_request_reviews,
            required_status_checks=required_status_checks,
            require_signed_commits=require_signed_commits,
            restrict_pushes=restrict_pushes,
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
        '''Generates CDKTF code for importing a BranchProtection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BranchProtection to import.
        :param import_from_id: The id of the existing BranchProtection that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BranchProtection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688ad4c7eb8b61df2a465a6a7d0f1b356a96527c199e421dbf43f59b1c083798)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRequiredPullRequestReviews")
    def put_required_pull_request_reviews(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionRequiredPullRequestReviews", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__215f8fc60141e807184121c08c2c5248f3ff747b03ded518c8a3913b9c064226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequiredPullRequestReviews", [value]))

    @jsii.member(jsii_name="putRequiredStatusChecks")
    def put_required_status_checks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionRequiredStatusChecks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__897df3e4a4af870e61e9b751544eddf16e7a5ab34265a7d70efd5c1b8398e353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequiredStatusChecks", [value]))

    @jsii.member(jsii_name="putRestrictPushes")
    def put_restrict_pushes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionRestrictPushes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2b0f5d5ed637cb67a87ea8f7dabfa21d7ae05df8b7bc0141431b0552caf59d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRestrictPushes", [value]))

    @jsii.member(jsii_name="resetAllowsDeletions")
    def reset_allows_deletions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowsDeletions", []))

    @jsii.member(jsii_name="resetAllowsForcePushes")
    def reset_allows_force_pushes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowsForcePushes", []))

    @jsii.member(jsii_name="resetEnforceAdmins")
    def reset_enforce_admins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceAdmins", []))

    @jsii.member(jsii_name="resetForcePushBypassers")
    def reset_force_push_bypassers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForcePushBypassers", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLockBranch")
    def reset_lock_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockBranch", []))

    @jsii.member(jsii_name="resetRequireConversationResolution")
    def reset_require_conversation_resolution(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireConversationResolution", []))

    @jsii.member(jsii_name="resetRequiredLinearHistory")
    def reset_required_linear_history(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredLinearHistory", []))

    @jsii.member(jsii_name="resetRequiredPullRequestReviews")
    def reset_required_pull_request_reviews(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredPullRequestReviews", []))

    @jsii.member(jsii_name="resetRequiredStatusChecks")
    def reset_required_status_checks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredStatusChecks", []))

    @jsii.member(jsii_name="resetRequireSignedCommits")
    def reset_require_signed_commits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireSignedCommits", []))

    @jsii.member(jsii_name="resetRestrictPushes")
    def reset_restrict_pushes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictPushes", []))

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
    @jsii.member(jsii_name="requiredPullRequestReviews")
    def required_pull_request_reviews(
        self,
    ) -> "BranchProtectionRequiredPullRequestReviewsList":
        return typing.cast("BranchProtectionRequiredPullRequestReviewsList", jsii.get(self, "requiredPullRequestReviews"))

    @builtins.property
    @jsii.member(jsii_name="requiredStatusChecks")
    def required_status_checks(self) -> "BranchProtectionRequiredStatusChecksList":
        return typing.cast("BranchProtectionRequiredStatusChecksList", jsii.get(self, "requiredStatusChecks"))

    @builtins.property
    @jsii.member(jsii_name="restrictPushes")
    def restrict_pushes(self) -> "BranchProtectionRestrictPushesList":
        return typing.cast("BranchProtectionRestrictPushesList", jsii.get(self, "restrictPushes"))

    @builtins.property
    @jsii.member(jsii_name="allowsDeletionsInput")
    def allows_deletions_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowsDeletionsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowsForcePushesInput")
    def allows_force_pushes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowsForcePushesInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceAdminsInput")
    def enforce_admins_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceAdminsInput"))

    @builtins.property
    @jsii.member(jsii_name="forcePushBypassersInput")
    def force_push_bypassers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "forcePushBypassersInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lockBranchInput")
    def lock_branch_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lockBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryIdInput")
    def repository_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="requireConversationResolutionInput")
    def require_conversation_resolution_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireConversationResolutionInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredLinearHistoryInput")
    def required_linear_history_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredLinearHistoryInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredPullRequestReviewsInput")
    def required_pull_request_reviews_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionRequiredPullRequestReviews"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionRequiredPullRequestReviews"]]], jsii.get(self, "requiredPullRequestReviewsInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredStatusChecksInput")
    def required_status_checks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionRequiredStatusChecks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionRequiredStatusChecks"]]], jsii.get(self, "requiredStatusChecksInput"))

    @builtins.property
    @jsii.member(jsii_name="requireSignedCommitsInput")
    def require_signed_commits_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireSignedCommitsInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictPushesInput")
    def restrict_pushes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionRestrictPushes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionRestrictPushes"]]], jsii.get(self, "restrictPushesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowsDeletions")
    def allows_deletions(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowsDeletions"))

    @allows_deletions.setter
    def allows_deletions(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65fe0163448fd87ec39f78e4834a850d6623d7624f52e4aea12ccd55251c6408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowsDeletions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowsForcePushes")
    def allows_force_pushes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowsForcePushes"))

    @allows_force_pushes.setter
    def allows_force_pushes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde810b2214832b91c9acafa71d8b63a44a7ac74c652a641f84fcf5bfb14055b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowsForcePushes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceAdmins")
    def enforce_admins(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforceAdmins"))

    @enforce_admins.setter
    def enforce_admins(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888f903555688d7f04d46e3961d4e27f565d24f76fc0e1bc988e94a5a29bd71e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceAdmins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forcePushBypassers")
    def force_push_bypassers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "forcePushBypassers"))

    @force_push_bypassers.setter
    def force_push_bypassers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca34f16f03b78c05d3b36c659fd9b0157d00dd00678e068206fa0020fe423ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forcePushBypassers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9677fc24ce3b3428ba41f4398be12e27f66467e263735bdcb41f81b0f41db59d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockBranch")
    def lock_branch(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lockBranch"))

    @lock_branch.setter
    def lock_branch(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739dda8d4b160b7f41f929e72f74a34cc870675bb10f99bafe8336f444426886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522c84c0dc23004234717a1f3b7207bc0523c974c0f0aa4fe63840c5b23612c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryId")
    def repository_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryId"))

    @repository_id.setter
    def repository_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3632dc0718a10e4982a44ea99ffc5b6a9f41cd839082dbe7b8d8de6ebef7ce41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireConversationResolution")
    def require_conversation_resolution(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireConversationResolution"))

    @require_conversation_resolution.setter
    def require_conversation_resolution(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1dbde9aacced77a370f5b9e36a2da53f00793fff61aac5a1cd1f9dfed8ac14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireConversationResolution", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__c27a73e258926e2a107b47348a7654cb102000a78a4321121e533d5ee63d864e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredLinearHistory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireSignedCommits")
    def require_signed_commits(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireSignedCommits"))

    @require_signed_commits.setter
    def require_signed_commits(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ade556af6a23200661fd0b06b8f6b6e6657d7b208cca4e8459c45e35134d69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireSignedCommits", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.branchProtection.BranchProtectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "pattern": "pattern",
        "repository_id": "repositoryId",
        "allows_deletions": "allowsDeletions",
        "allows_force_pushes": "allowsForcePushes",
        "enforce_admins": "enforceAdmins",
        "force_push_bypassers": "forcePushBypassers",
        "id": "id",
        "lock_branch": "lockBranch",
        "require_conversation_resolution": "requireConversationResolution",
        "required_linear_history": "requiredLinearHistory",
        "required_pull_request_reviews": "requiredPullRequestReviews",
        "required_status_checks": "requiredStatusChecks",
        "require_signed_commits": "requireSignedCommits",
        "restrict_pushes": "restrictPushes",
    },
)
class BranchProtectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        pattern: builtins.str,
        repository_id: builtins.str,
        allows_deletions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allows_force_pushes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        force_push_bypassers: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        lock_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_conversation_resolution: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_pull_request_reviews: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionRequiredPullRequestReviews", typing.Dict[builtins.str, typing.Any]]]]] = None,
        required_status_checks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionRequiredStatusChecks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        require_signed_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrict_pushes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BranchProtectionRestrictPushes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param pattern: Identifies the protection rule pattern. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#pattern BranchProtection#pattern}
        :param repository_id: The name or node ID of the repository associated with this branch protection rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#repository_id BranchProtection#repository_id}
        :param allows_deletions: Setting this to 'true' to allow the branch to be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#allows_deletions BranchProtection#allows_deletions}
        :param allows_force_pushes: Setting this to 'true' to allow force pushes on the branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#allows_force_pushes BranchProtection#allows_force_pushes}
        :param enforce_admins: Setting this to 'true' enforces status checks for repository administrators. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#enforce_admins BranchProtection#enforce_admins}
        :param force_push_bypassers: The list of actor Names/IDs that are allowed to bypass force push restrictions. Actor names must either begin with a '/' for users or the organization name followed by a '/' for teams. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#force_push_bypassers BranchProtection#force_push_bypassers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#id BranchProtection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lock_branch: Setting this to 'true' will make the branch read-only and preventing any pushes to it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#lock_branch BranchProtection#lock_branch}
        :param require_conversation_resolution: Setting this to 'true' requires all conversations on code must be resolved before a pull request can be merged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#require_conversation_resolution BranchProtection#require_conversation_resolution}
        :param required_linear_history: Setting this to 'true' enforces a linear commit Git history, which prevents anyone from pushing merge commits to a branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#required_linear_history BranchProtection#required_linear_history}
        :param required_pull_request_reviews: required_pull_request_reviews block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#required_pull_request_reviews BranchProtection#required_pull_request_reviews}
        :param required_status_checks: required_status_checks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#required_status_checks BranchProtection#required_status_checks}
        :param require_signed_commits: Setting this to 'true' requires all commits to be signed with GPG. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#require_signed_commits BranchProtection#require_signed_commits}
        :param restrict_pushes: restrict_pushes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#restrict_pushes BranchProtection#restrict_pushes}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f157734353bd3c3b64004c63ef022a11eec58f6b59240b1e11b3b00d868ee9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument repository_id", value=repository_id, expected_type=type_hints["repository_id"])
            check_type(argname="argument allows_deletions", value=allows_deletions, expected_type=type_hints["allows_deletions"])
            check_type(argname="argument allows_force_pushes", value=allows_force_pushes, expected_type=type_hints["allows_force_pushes"])
            check_type(argname="argument enforce_admins", value=enforce_admins, expected_type=type_hints["enforce_admins"])
            check_type(argname="argument force_push_bypassers", value=force_push_bypassers, expected_type=type_hints["force_push_bypassers"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lock_branch", value=lock_branch, expected_type=type_hints["lock_branch"])
            check_type(argname="argument require_conversation_resolution", value=require_conversation_resolution, expected_type=type_hints["require_conversation_resolution"])
            check_type(argname="argument required_linear_history", value=required_linear_history, expected_type=type_hints["required_linear_history"])
            check_type(argname="argument required_pull_request_reviews", value=required_pull_request_reviews, expected_type=type_hints["required_pull_request_reviews"])
            check_type(argname="argument required_status_checks", value=required_status_checks, expected_type=type_hints["required_status_checks"])
            check_type(argname="argument require_signed_commits", value=require_signed_commits, expected_type=type_hints["require_signed_commits"])
            check_type(argname="argument restrict_pushes", value=restrict_pushes, expected_type=type_hints["restrict_pushes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern": pattern,
            "repository_id": repository_id,
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
        if allows_deletions is not None:
            self._values["allows_deletions"] = allows_deletions
        if allows_force_pushes is not None:
            self._values["allows_force_pushes"] = allows_force_pushes
        if enforce_admins is not None:
            self._values["enforce_admins"] = enforce_admins
        if force_push_bypassers is not None:
            self._values["force_push_bypassers"] = force_push_bypassers
        if id is not None:
            self._values["id"] = id
        if lock_branch is not None:
            self._values["lock_branch"] = lock_branch
        if require_conversation_resolution is not None:
            self._values["require_conversation_resolution"] = require_conversation_resolution
        if required_linear_history is not None:
            self._values["required_linear_history"] = required_linear_history
        if required_pull_request_reviews is not None:
            self._values["required_pull_request_reviews"] = required_pull_request_reviews
        if required_status_checks is not None:
            self._values["required_status_checks"] = required_status_checks
        if require_signed_commits is not None:
            self._values["require_signed_commits"] = require_signed_commits
        if restrict_pushes is not None:
            self._values["restrict_pushes"] = restrict_pushes

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
    def pattern(self) -> builtins.str:
        '''Identifies the protection rule pattern.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#pattern BranchProtection#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_id(self) -> builtins.str:
        '''The name or node ID of the repository associated with this branch protection rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#repository_id BranchProtection#repository_id}
        '''
        result = self._values.get("repository_id")
        assert result is not None, "Required property 'repository_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allows_deletions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to 'true' to allow the branch to be deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#allows_deletions BranchProtection#allows_deletions}
        '''
        result = self._values.get("allows_deletions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allows_force_pushes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to 'true' to allow force pushes on the branch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#allows_force_pushes BranchProtection#allows_force_pushes}
        '''
        result = self._values.get("allows_force_pushes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enforce_admins(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to 'true' enforces status checks for repository administrators.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#enforce_admins BranchProtection#enforce_admins}
        '''
        result = self._values.get("enforce_admins")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def force_push_bypassers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of actor Names/IDs that are allowed to bypass force push restrictions.

        Actor names must either begin with a '/' for users or the organization name followed by a '/' for teams.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#force_push_bypassers BranchProtection#force_push_bypassers}
        '''
        result = self._values.get("force_push_bypassers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#id BranchProtection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_branch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to 'true' will make the branch read-only and preventing any pushes to it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#lock_branch BranchProtection#lock_branch}
        '''
        result = self._values.get("lock_branch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_conversation_resolution(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to 'true' requires all conversations on code must be resolved before a pull request can be merged.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#require_conversation_resolution BranchProtection#require_conversation_resolution}
        '''
        result = self._values.get("require_conversation_resolution")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_linear_history(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to 'true' enforces a linear commit Git history, which prevents anyone from pushing merge commits to a branch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#required_linear_history BranchProtection#required_linear_history}
        '''
        result = self._values.get("required_linear_history")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_pull_request_reviews(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionRequiredPullRequestReviews"]]]:
        '''required_pull_request_reviews block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#required_pull_request_reviews BranchProtection#required_pull_request_reviews}
        '''
        result = self._values.get("required_pull_request_reviews")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionRequiredPullRequestReviews"]]], result)

    @builtins.property
    def required_status_checks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionRequiredStatusChecks"]]]:
        '''required_status_checks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#required_status_checks BranchProtection#required_status_checks}
        '''
        result = self._values.get("required_status_checks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionRequiredStatusChecks"]]], result)

    @builtins.property
    def require_signed_commits(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to 'true' requires all commits to be signed with GPG.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#require_signed_commits BranchProtection#require_signed_commits}
        '''
        result = self._values.get("require_signed_commits")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restrict_pushes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionRestrictPushes"]]]:
        '''restrict_pushes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#restrict_pushes BranchProtection#restrict_pushes}
        '''
        result = self._values.get("restrict_pushes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BranchProtectionRestrictPushes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.branchProtection.BranchProtectionRequiredPullRequestReviews",
    jsii_struct_bases=[],
    name_mapping={
        "dismissal_restrictions": "dismissalRestrictions",
        "dismiss_stale_reviews": "dismissStaleReviews",
        "pull_request_bypassers": "pullRequestBypassers",
        "require_code_owner_reviews": "requireCodeOwnerReviews",
        "required_approving_review_count": "requiredApprovingReviewCount",
        "require_last_push_approval": "requireLastPushApproval",
        "restrict_dismissals": "restrictDismissals",
    },
)
class BranchProtectionRequiredPullRequestReviews:
    def __init__(
        self,
        *,
        dismissal_restrictions: typing.Optional[typing.Sequence[builtins.str]] = None,
        dismiss_stale_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pull_request_bypassers: typing.Optional[typing.Sequence[builtins.str]] = None,
        require_code_owner_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_approving_review_count: typing.Optional[jsii.Number] = None,
        require_last_push_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrict_dismissals: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dismissal_restrictions: The list of actor Names/IDs with dismissal access. If not empty, 'restrict_dismissals' is ignored. Actor names must either begin with a '/' for users or the organization name followed by a '/' for teams. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#dismissal_restrictions BranchProtection#dismissal_restrictions}
        :param dismiss_stale_reviews: Dismiss approved reviews automatically when a new commit is pushed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#dismiss_stale_reviews BranchProtection#dismiss_stale_reviews}
        :param pull_request_bypassers: The list of actor Names/IDs that are allowed to bypass pull request requirements. Actor names must either begin with a '/' for users or the organization name followed by a '/' for teams. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#pull_request_bypassers BranchProtection#pull_request_bypassers}
        :param require_code_owner_reviews: Require an approved review in pull requests including files with a designated code owner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#require_code_owner_reviews BranchProtection#require_code_owner_reviews}
        :param required_approving_review_count: Require 'x' number of approvals to satisfy branch protection requirements. If this is specified it must be a number between 0-6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#required_approving_review_count BranchProtection#required_approving_review_count}
        :param require_last_push_approval: Require that The most recent push must be approved by someone other than the last pusher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#require_last_push_approval BranchProtection#require_last_push_approval}
        :param restrict_dismissals: Restrict pull request review dismissals. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#restrict_dismissals BranchProtection#restrict_dismissals}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae3e79bdeea90e37d5a8fb25455b197d6a1e3c0077680a677856ed5ce571c8b)
            check_type(argname="argument dismissal_restrictions", value=dismissal_restrictions, expected_type=type_hints["dismissal_restrictions"])
            check_type(argname="argument dismiss_stale_reviews", value=dismiss_stale_reviews, expected_type=type_hints["dismiss_stale_reviews"])
            check_type(argname="argument pull_request_bypassers", value=pull_request_bypassers, expected_type=type_hints["pull_request_bypassers"])
            check_type(argname="argument require_code_owner_reviews", value=require_code_owner_reviews, expected_type=type_hints["require_code_owner_reviews"])
            check_type(argname="argument required_approving_review_count", value=required_approving_review_count, expected_type=type_hints["required_approving_review_count"])
            check_type(argname="argument require_last_push_approval", value=require_last_push_approval, expected_type=type_hints["require_last_push_approval"])
            check_type(argname="argument restrict_dismissals", value=restrict_dismissals, expected_type=type_hints["restrict_dismissals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dismissal_restrictions is not None:
            self._values["dismissal_restrictions"] = dismissal_restrictions
        if dismiss_stale_reviews is not None:
            self._values["dismiss_stale_reviews"] = dismiss_stale_reviews
        if pull_request_bypassers is not None:
            self._values["pull_request_bypassers"] = pull_request_bypassers
        if require_code_owner_reviews is not None:
            self._values["require_code_owner_reviews"] = require_code_owner_reviews
        if required_approving_review_count is not None:
            self._values["required_approving_review_count"] = required_approving_review_count
        if require_last_push_approval is not None:
            self._values["require_last_push_approval"] = require_last_push_approval
        if restrict_dismissals is not None:
            self._values["restrict_dismissals"] = restrict_dismissals

    @builtins.property
    def dismissal_restrictions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of actor Names/IDs with dismissal access.

        If not empty, 'restrict_dismissals' is ignored. Actor names must either begin with a '/' for users or the organization name followed by a '/' for teams.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#dismissal_restrictions BranchProtection#dismissal_restrictions}
        '''
        result = self._values.get("dismissal_restrictions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dismiss_stale_reviews(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Dismiss approved reviews automatically when a new commit is pushed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#dismiss_stale_reviews BranchProtection#dismiss_stale_reviews}
        '''
        result = self._values.get("dismiss_stale_reviews")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pull_request_bypassers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of actor Names/IDs that are allowed to bypass pull request requirements.

        Actor names must either begin with a '/' for users or the organization name followed by a '/' for teams.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#pull_request_bypassers BranchProtection#pull_request_bypassers}
        '''
        result = self._values.get("pull_request_bypassers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def require_code_owner_reviews(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require an approved review in pull requests including files with a designated code owner.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#require_code_owner_reviews BranchProtection#require_code_owner_reviews}
        '''
        result = self._values.get("require_code_owner_reviews")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_approving_review_count(self) -> typing.Optional[jsii.Number]:
        '''Require 'x' number of approvals to satisfy branch protection requirements.

        If this is specified it must be a number between 0-6.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#required_approving_review_count BranchProtection#required_approving_review_count}
        '''
        result = self._values.get("required_approving_review_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def require_last_push_approval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require that The most recent push must be approved by someone other than the last pusher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#require_last_push_approval BranchProtection#require_last_push_approval}
        '''
        result = self._values.get("require_last_push_approval")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restrict_dismissals(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Restrict pull request review dismissals.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#restrict_dismissals BranchProtection#restrict_dismissals}
        '''
        result = self._values.get("restrict_dismissals")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionRequiredPullRequestReviews(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BranchProtectionRequiredPullRequestReviewsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.branchProtection.BranchProtectionRequiredPullRequestReviewsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78f9a6aae9b77cda69b5383b5e421a2e96847538f137b3149468d49c3a02673f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BranchProtectionRequiredPullRequestReviewsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae0dd3ecce54167e5d26e4d77cdaf8393991f55efbb8134e167686b7aff7c7ae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BranchProtectionRequiredPullRequestReviewsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0148a21e71842d246d96599984f7e4393f1aaa4dfc55300dee01b9bd24bef6ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0df28ff06118259b9bc04ad0b2da47fb8206b0ac47bbf113e5573ee5929d947d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5a5c16a56b9ae378820518a22c67fe1f3257159a38565aa1a311c4d7d8d6e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionRequiredPullRequestReviews]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionRequiredPullRequestReviews]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionRequiredPullRequestReviews]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd293737d35a8af7998fd0976135cb824daf298fd61b346dd0f9f852124bb34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BranchProtectionRequiredPullRequestReviewsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.branchProtection.BranchProtectionRequiredPullRequestReviewsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df6c06f73c632f5f950e5c428b440bcced423fbd754c3bcfefc393337b5be96e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDismissalRestrictions")
    def reset_dismissal_restrictions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDismissalRestrictions", []))

    @jsii.member(jsii_name="resetDismissStaleReviews")
    def reset_dismiss_stale_reviews(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDismissStaleReviews", []))

    @jsii.member(jsii_name="resetPullRequestBypassers")
    def reset_pull_request_bypassers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullRequestBypassers", []))

    @jsii.member(jsii_name="resetRequireCodeOwnerReviews")
    def reset_require_code_owner_reviews(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireCodeOwnerReviews", []))

    @jsii.member(jsii_name="resetRequiredApprovingReviewCount")
    def reset_required_approving_review_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredApprovingReviewCount", []))

    @jsii.member(jsii_name="resetRequireLastPushApproval")
    def reset_require_last_push_approval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireLastPushApproval", []))

    @jsii.member(jsii_name="resetRestrictDismissals")
    def reset_restrict_dismissals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictDismissals", []))

    @builtins.property
    @jsii.member(jsii_name="dismissalRestrictionsInput")
    def dismissal_restrictions_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dismissalRestrictionsInput"))

    @builtins.property
    @jsii.member(jsii_name="dismissStaleReviewsInput")
    def dismiss_stale_reviews_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dismissStaleReviewsInput"))

    @builtins.property
    @jsii.member(jsii_name="pullRequestBypassersInput")
    def pull_request_bypassers_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pullRequestBypassersInput"))

    @builtins.property
    @jsii.member(jsii_name="requireCodeOwnerReviewsInput")
    def require_code_owner_reviews_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireCodeOwnerReviewsInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredApprovingReviewCountInput")
    def required_approving_review_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requiredApprovingReviewCountInput"))

    @builtins.property
    @jsii.member(jsii_name="requireLastPushApprovalInput")
    def require_last_push_approval_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireLastPushApprovalInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictDismissalsInput")
    def restrict_dismissals_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "restrictDismissalsInput"))

    @builtins.property
    @jsii.member(jsii_name="dismissalRestrictions")
    def dismissal_restrictions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dismissalRestrictions"))

    @dismissal_restrictions.setter
    def dismissal_restrictions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e68498d9de1d1b4bdd2d64cbfb9f7778edcf42c93b9881e752734d34b4d562f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dismissalRestrictions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dismissStaleReviews")
    def dismiss_stale_reviews(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dismissStaleReviews"))

    @dismiss_stale_reviews.setter
    def dismiss_stale_reviews(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0533cebca31eed4033a1f9c8e48266087da6584b26111c8a9be7833590d2330a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dismissStaleReviews", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pullRequestBypassers")
    def pull_request_bypassers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pullRequestBypassers"))

    @pull_request_bypassers.setter
    def pull_request_bypassers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98b1ccd954631fb0b6f4784988ef6996826c638f185a89876feb02a0936aa76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullRequestBypassers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireCodeOwnerReviews")
    def require_code_owner_reviews(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireCodeOwnerReviews"))

    @require_code_owner_reviews.setter
    def require_code_owner_reviews(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e3312c9705c1614da802daa06065581f96a657fee44660b780da345f28c29b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireCodeOwnerReviews", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredApprovingReviewCount")
    def required_approving_review_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requiredApprovingReviewCount"))

    @required_approving_review_count.setter
    def required_approving_review_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528efceaf80cf0ac4b616c6af9c9fafa4024ef64e135f49f18dc049bd7834054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredApprovingReviewCount", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__2048b9e3b84aace57685f6d9c14195f92bf56f0a834042fa1833b67c4d1f16f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireLastPushApproval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictDismissals")
    def restrict_dismissals(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "restrictDismissals"))

    @restrict_dismissals.setter
    def restrict_dismissals(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273dcd7ceb9e7e0011aa4d384839813121ec347826f62537539eedbfa78b5ad0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictDismissals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionRequiredPullRequestReviews]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionRequiredPullRequestReviews]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionRequiredPullRequestReviews]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__313ad5f964da21bba4813f2f8bfaeb03e74c7b0b7d940aa4db7ff4a400b05333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.branchProtection.BranchProtectionRequiredStatusChecks",
    jsii_struct_bases=[],
    name_mapping={"contexts": "contexts", "strict": "strict"},
)
class BranchProtectionRequiredStatusChecks:
    def __init__(
        self,
        *,
        contexts: typing.Optional[typing.Sequence[builtins.str]] = None,
        strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param contexts: The list of status checks to require in order to merge into this branch. No status checks are required by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#contexts BranchProtection#contexts}
        :param strict: Require branches to be up to date before merging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#strict BranchProtection#strict}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d90c20efc3d39f8f73e822ebe82b2c6ad70144f8034f76b4ed5cbf9d3f50bb59)
            check_type(argname="argument contexts", value=contexts, expected_type=type_hints["contexts"])
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contexts is not None:
            self._values["contexts"] = contexts
        if strict is not None:
            self._values["strict"] = strict

    @builtins.property
    def contexts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of status checks to require in order to merge into this branch.

        No status checks are required by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#contexts BranchProtection#contexts}
        '''
        result = self._values.get("contexts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def strict(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require branches to be up to date before merging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#strict BranchProtection#strict}
        '''
        result = self._values.get("strict")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionRequiredStatusChecks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BranchProtectionRequiredStatusChecksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.branchProtection.BranchProtectionRequiredStatusChecksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad411799c9218127eff5ab90dfa0049e75136e80c8b9bb956b9bd72263f43008)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BranchProtectionRequiredStatusChecksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__440f78836e0b3b1293eeea561c0ad16a6b7970cba8c2d06520ae0ce6b6934868)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BranchProtectionRequiredStatusChecksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aaa4533c9bea25b784baf775ff94cc12bda5254e659b3ad96a0b58d9f698c41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a022130380905c9cc47fb27d1f67bb2d551c4e5629cea1824b306c4484e960f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__379fcbac66f0b5b103bb7e2dac65cbba95fcdedde988d5af7f77b8381e4032b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionRequiredStatusChecks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionRequiredStatusChecks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionRequiredStatusChecks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a56dbf1da4bc0c0089747fc9d89bdf62f49691d0445d45d58a7e786d5dac48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BranchProtectionRequiredStatusChecksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.branchProtection.BranchProtectionRequiredStatusChecksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d26e2d31cb690f61a6f6a1ed32710bd76959b18aa71d85ec602aa6ca771d8f6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContexts")
    def reset_contexts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContexts", []))

    @jsii.member(jsii_name="resetStrict")
    def reset_strict(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrict", []))

    @builtins.property
    @jsii.member(jsii_name="contextsInput")
    def contexts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contextsInput"))

    @builtins.property
    @jsii.member(jsii_name="strictInput")
    def strict_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "strictInput"))

    @builtins.property
    @jsii.member(jsii_name="contexts")
    def contexts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contexts"))

    @contexts.setter
    def contexts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03d7f437e58a5b41ed4708c350128eba0a2204088f91aeea7c16df56cd5aeeaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contexts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strict")
    def strict(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "strict"))

    @strict.setter
    def strict(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d816b80817866a2ca70e461e2fab20bbb46f41c1e3e20c7e5c4ddd14fbf9c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strict", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionRequiredStatusChecks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionRequiredStatusChecks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionRequiredStatusChecks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae83444c4cdf78a49b2a5592b9257752ff36ace810a2c03efb9451ec8d8c28d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.branchProtection.BranchProtectionRestrictPushes",
    jsii_struct_bases=[],
    name_mapping={
        "blocks_creations": "blocksCreations",
        "push_allowances": "pushAllowances",
    },
)
class BranchProtectionRestrictPushes:
    def __init__(
        self,
        *,
        blocks_creations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        push_allowances: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param blocks_creations: Restrict pushes that create matching branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#blocks_creations BranchProtection#blocks_creations}
        :param push_allowances: The list of actor Names/IDs that may push to the branch. Actor names must either begin with a '/' for users or the organization name followed by a '/' for teams. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#push_allowances BranchProtection#push_allowances}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44889c6999810fd309649f0ae74c5cc83c5b66a17ceea929d16d8ca302adee75)
            check_type(argname="argument blocks_creations", value=blocks_creations, expected_type=type_hints["blocks_creations"])
            check_type(argname="argument push_allowances", value=push_allowances, expected_type=type_hints["push_allowances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if blocks_creations is not None:
            self._values["blocks_creations"] = blocks_creations
        if push_allowances is not None:
            self._values["push_allowances"] = push_allowances

    @builtins.property
    def blocks_creations(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Restrict pushes that create matching branches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#blocks_creations BranchProtection#blocks_creations}
        '''
        result = self._values.get("blocks_creations")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def push_allowances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of actor Names/IDs that may push to the branch.

        Actor names must either begin with a '/' for users or the organization name followed by a '/' for teams.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection#push_allowances BranchProtection#push_allowances}
        '''
        result = self._values.get("push_allowances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionRestrictPushes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BranchProtectionRestrictPushesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.branchProtection.BranchProtectionRestrictPushesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d9fd7ae9fad9b60e9aaf942469b48f2d1123034c1a685e88c321a92fe60708a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BranchProtectionRestrictPushesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f3b19a55ddfcb6527794c1f8c5fe09770c8ef97193427c47f24b47439c0d9d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BranchProtectionRestrictPushesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510f7a72ee9e631b31cf33bbf524adf6ceea9323d334e67496744bd7a3156614)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d81fd8aca6ffd0e574d7c43495a14b2f3932883dfb1a26dda9a3187dbc579fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67256a2003c58d169c8fb480a37e35a9cea66cbc99a69c88c7729d63bd21d14c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionRestrictPushes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionRestrictPushes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionRestrictPushes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179faa773db4dd73c26d8679821d90fa4792ddf068dfaa7c90adadee308a2cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BranchProtectionRestrictPushesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.branchProtection.BranchProtectionRestrictPushesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__567b092a1f474446d2150d2b03c17cdff89051d7686e51d225cea21ba52b5298)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBlocksCreations")
    def reset_blocks_creations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlocksCreations", []))

    @jsii.member(jsii_name="resetPushAllowances")
    def reset_push_allowances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushAllowances", []))

    @builtins.property
    @jsii.member(jsii_name="blocksCreationsInput")
    def blocks_creations_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "blocksCreationsInput"))

    @builtins.property
    @jsii.member(jsii_name="pushAllowancesInput")
    def push_allowances_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pushAllowancesInput"))

    @builtins.property
    @jsii.member(jsii_name="blocksCreations")
    def blocks_creations(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "blocksCreations"))

    @blocks_creations.setter
    def blocks_creations(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336d457667eed709478e5544d7bf317185f4b3184f1243f43896e4b8b2c7bb56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blocksCreations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pushAllowances")
    def push_allowances(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pushAllowances"))

    @push_allowances.setter
    def push_allowances(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58dcf6d538baa9f7c8d5fd51f46e04961b46884f84fe9c1c38a041e8c9505153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushAllowances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionRestrictPushes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionRestrictPushes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionRestrictPushes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f51d44e6b0c76b41a184d4c6c19dfb5da5d9e65f7ce9cff80b80ef1d0eb8b6c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BranchProtection",
    "BranchProtectionConfig",
    "BranchProtectionRequiredPullRequestReviews",
    "BranchProtectionRequiredPullRequestReviewsList",
    "BranchProtectionRequiredPullRequestReviewsOutputReference",
    "BranchProtectionRequiredStatusChecks",
    "BranchProtectionRequiredStatusChecksList",
    "BranchProtectionRequiredStatusChecksOutputReference",
    "BranchProtectionRestrictPushes",
    "BranchProtectionRestrictPushesList",
    "BranchProtectionRestrictPushesOutputReference",
]

publication.publish()

def _typecheckingstub__d030729aabe2b9742e66c59c7dd2efaf5c966fdf7fbff191a75dce20978ddcba(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    pattern: builtins.str,
    repository_id: builtins.str,
    allows_deletions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allows_force_pushes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforce_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    force_push_bypassers: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    lock_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_conversation_resolution: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_pull_request_reviews: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionRequiredPullRequestReviews, typing.Dict[builtins.str, typing.Any]]]]] = None,
    required_status_checks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionRequiredStatusChecks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    require_signed_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restrict_pushes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionRestrictPushes, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__688ad4c7eb8b61df2a465a6a7d0f1b356a96527c199e421dbf43f59b1c083798(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215f8fc60141e807184121c08c2c5248f3ff747b03ded518c8a3913b9c064226(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionRequiredPullRequestReviews, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897df3e4a4af870e61e9b751544eddf16e7a5ab34265a7d70efd5c1b8398e353(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionRequiredStatusChecks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2b0f5d5ed637cb67a87ea8f7dabfa21d7ae05df8b7bc0141431b0552caf59d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionRestrictPushes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65fe0163448fd87ec39f78e4834a850d6623d7624f52e4aea12ccd55251c6408(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde810b2214832b91c9acafa71d8b63a44a7ac74c652a641f84fcf5bfb14055b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888f903555688d7f04d46e3961d4e27f565d24f76fc0e1bc988e94a5a29bd71e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca34f16f03b78c05d3b36c659fd9b0157d00dd00678e068206fa0020fe423ef(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9677fc24ce3b3428ba41f4398be12e27f66467e263735bdcb41f81b0f41db59d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739dda8d4b160b7f41f929e72f74a34cc870675bb10f99bafe8336f444426886(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522c84c0dc23004234717a1f3b7207bc0523c974c0f0aa4fe63840c5b23612c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3632dc0718a10e4982a44ea99ffc5b6a9f41cd839082dbe7b8d8de6ebef7ce41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1dbde9aacced77a370f5b9e36a2da53f00793fff61aac5a1cd1f9dfed8ac14(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27a73e258926e2a107b47348a7654cb102000a78a4321121e533d5ee63d864e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ade556af6a23200661fd0b06b8f6b6e6657d7b208cca4e8459c45e35134d69(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f157734353bd3c3b64004c63ef022a11eec58f6b59240b1e11b3b00d868ee9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pattern: builtins.str,
    repository_id: builtins.str,
    allows_deletions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allows_force_pushes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforce_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    force_push_bypassers: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    lock_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_conversation_resolution: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_pull_request_reviews: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionRequiredPullRequestReviews, typing.Dict[builtins.str, typing.Any]]]]] = None,
    required_status_checks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionRequiredStatusChecks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    require_signed_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restrict_pushes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BranchProtectionRestrictPushes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae3e79bdeea90e37d5a8fb25455b197d6a1e3c0077680a677856ed5ce571c8b(
    *,
    dismissal_restrictions: typing.Optional[typing.Sequence[builtins.str]] = None,
    dismiss_stale_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pull_request_bypassers: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_code_owner_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_approving_review_count: typing.Optional[jsii.Number] = None,
    require_last_push_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restrict_dismissals: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f9a6aae9b77cda69b5383b5e421a2e96847538f137b3149468d49c3a02673f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0dd3ecce54167e5d26e4d77cdaf8393991f55efbb8134e167686b7aff7c7ae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0148a21e71842d246d96599984f7e4393f1aaa4dfc55300dee01b9bd24bef6ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df28ff06118259b9bc04ad0b2da47fb8206b0ac47bbf113e5573ee5929d947d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a5c16a56b9ae378820518a22c67fe1f3257159a38565aa1a311c4d7d8d6e0b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd293737d35a8af7998fd0976135cb824daf298fd61b346dd0f9f852124bb34(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionRequiredPullRequestReviews]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6c06f73c632f5f950e5c428b440bcced423fbd754c3bcfefc393337b5be96e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68498d9de1d1b4bdd2d64cbfb9f7778edcf42c93b9881e752734d34b4d562f9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0533cebca31eed4033a1f9c8e48266087da6584b26111c8a9be7833590d2330a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98b1ccd954631fb0b6f4784988ef6996826c638f185a89876feb02a0936aa76(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e3312c9705c1614da802daa06065581f96a657fee44660b780da345f28c29b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528efceaf80cf0ac4b616c6af9c9fafa4024ef64e135f49f18dc049bd7834054(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2048b9e3b84aace57685f6d9c14195f92bf56f0a834042fa1833b67c4d1f16f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273dcd7ceb9e7e0011aa4d384839813121ec347826f62537539eedbfa78b5ad0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313ad5f964da21bba4813f2f8bfaeb03e74c7b0b7d940aa4db7ff4a400b05333(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionRequiredPullRequestReviews]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90c20efc3d39f8f73e822ebe82b2c6ad70144f8034f76b4ed5cbf9d3f50bb59(
    *,
    contexts: typing.Optional[typing.Sequence[builtins.str]] = None,
    strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad411799c9218127eff5ab90dfa0049e75136e80c8b9bb956b9bd72263f43008(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440f78836e0b3b1293eeea561c0ad16a6b7970cba8c2d06520ae0ce6b6934868(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aaa4533c9bea25b784baf775ff94cc12bda5254e659b3ad96a0b58d9f698c41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a022130380905c9cc47fb27d1f67bb2d551c4e5629cea1824b306c4484e960f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__379fcbac66f0b5b103bb7e2dac65cbba95fcdedde988d5af7f77b8381e4032b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a56dbf1da4bc0c0089747fc9d89bdf62f49691d0445d45d58a7e786d5dac48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionRequiredStatusChecks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26e2d31cb690f61a6f6a1ed32710bd76959b18aa71d85ec602aa6ca771d8f6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d7f437e58a5b41ed4708c350128eba0a2204088f91aeea7c16df56cd5aeeaf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d816b80817866a2ca70e461e2fab20bbb46f41c1e3e20c7e5c4ddd14fbf9c50(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae83444c4cdf78a49b2a5592b9257752ff36ace810a2c03efb9451ec8d8c28d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionRequiredStatusChecks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44889c6999810fd309649f0ae74c5cc83c5b66a17ceea929d16d8ca302adee75(
    *,
    blocks_creations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    push_allowances: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9fd7ae9fad9b60e9aaf942469b48f2d1123034c1a685e88c321a92fe60708a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f3b19a55ddfcb6527794c1f8c5fe09770c8ef97193427c47f24b47439c0d9d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510f7a72ee9e631b31cf33bbf524adf6ceea9323d334e67496744bd7a3156614(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d81fd8aca6ffd0e574d7c43495a14b2f3932883dfb1a26dda9a3187dbc579fb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67256a2003c58d169c8fb480a37e35a9cea66cbc99a69c88c7729d63bd21d14c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179faa773db4dd73c26d8679821d90fa4792ddf068dfaa7c90adadee308a2cee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BranchProtectionRestrictPushes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567b092a1f474446d2150d2b03c17cdff89051d7686e51d225cea21ba52b5298(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336d457667eed709478e5544d7bf317185f4b3184f1243f43896e4b8b2c7bb56(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58dcf6d538baa9f7c8d5fd51f46e04961b46884f84fe9c1c38a041e8c9505153(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51d44e6b0c76b41a184d4c6c19dfb5da5d9e65f7ce9cff80b80ef1d0eb8b6c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BranchProtectionRestrictPushes]],
) -> None:
    """Type checking stubs"""
    pass
