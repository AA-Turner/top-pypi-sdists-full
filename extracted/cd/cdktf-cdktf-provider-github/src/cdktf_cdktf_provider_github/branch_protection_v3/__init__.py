r'''
# `github_branch_protection_v3`

Refer to the Terraform Registry for docs: [`github_branch_protection_v3`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3).
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


class BranchProtectionV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.branchProtectionV3.BranchProtectionV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3 github_branch_protection_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        branch: builtins.str,
        repository: builtins.str,
        enforce_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        require_conversation_resolution: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_pull_request_reviews: typing.Optional[typing.Union["BranchProtectionV3RequiredPullRequestReviews", typing.Dict[builtins.str, typing.Any]]] = None,
        required_status_checks: typing.Optional[typing.Union["BranchProtectionV3RequiredStatusChecks", typing.Dict[builtins.str, typing.Any]]] = None,
        require_signed_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrictions: typing.Optional[typing.Union["BranchProtectionV3Restrictions", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3 github_branch_protection_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param branch: The Git branch to protect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#branch BranchProtectionV3#branch}
        :param repository: The GitHub repository name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#repository BranchProtectionV3#repository}
        :param enforce_admins: Setting this to 'true' enforces status checks for repository administrators. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#enforce_admins BranchProtectionV3#enforce_admins}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#id BranchProtectionV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param require_conversation_resolution: Setting this to 'true' requires all conversations on code must be resolved before a pull request can be merged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#require_conversation_resolution BranchProtectionV3#require_conversation_resolution}
        :param required_pull_request_reviews: required_pull_request_reviews block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#required_pull_request_reviews BranchProtectionV3#required_pull_request_reviews}
        :param required_status_checks: required_status_checks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#required_status_checks BranchProtectionV3#required_status_checks}
        :param require_signed_commits: Setting this to 'true' requires all commits to be signed with GPG. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#require_signed_commits BranchProtectionV3#require_signed_commits}
        :param restrictions: restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#restrictions BranchProtectionV3#restrictions}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__039872cea41507d4e2ed84413e7eb4a02bc02877ab2ea2b02ec7bcb05844a193)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BranchProtectionV3Config(
            branch=branch,
            repository=repository,
            enforce_admins=enforce_admins,
            id=id,
            require_conversation_resolution=require_conversation_resolution,
            required_pull_request_reviews=required_pull_request_reviews,
            required_status_checks=required_status_checks,
            require_signed_commits=require_signed_commits,
            restrictions=restrictions,
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
        '''Generates CDKTF code for importing a BranchProtectionV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BranchProtectionV3 to import.
        :param import_from_id: The id of the existing BranchProtectionV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BranchProtectionV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4335e89d3fa2d2f5b920eff3c8ed984e1358d372976c389f7baa92890213a596)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRequiredPullRequestReviews")
    def put_required_pull_request_reviews(
        self,
        *,
        bypass_pull_request_allowances: typing.Optional[typing.Union["BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances", typing.Dict[builtins.str, typing.Any]]] = None,
        dismissal_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
        dismissal_teams: typing.Optional[typing.Sequence[builtins.str]] = None,
        dismissal_users: typing.Optional[typing.Sequence[builtins.str]] = None,
        dismiss_stale_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_code_owner_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_approving_review_count: typing.Optional[jsii.Number] = None,
        require_last_push_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bypass_pull_request_allowances: bypass_pull_request_allowances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#bypass_pull_request_allowances BranchProtectionV3#bypass_pull_request_allowances}
        :param dismissal_apps: The list of apps slugs with dismissal access. Always use slug of the app, not its name. Each app already has to have access to the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#dismissal_apps BranchProtectionV3#dismissal_apps}
        :param dismissal_teams: The list of team slugs with dismissal access. Always use slug of the team, not its name. Each team already has to have access to the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#dismissal_teams BranchProtectionV3#dismissal_teams}
        :param dismissal_users: The list of user logins with dismissal access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#dismissal_users BranchProtectionV3#dismissal_users}
        :param dismiss_stale_reviews: Dismiss approved reviews automatically when a new commit is pushed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#dismiss_stale_reviews BranchProtectionV3#dismiss_stale_reviews}
        :param include_admins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#include_admins BranchProtectionV3#include_admins}.
        :param require_code_owner_reviews: Require an approved review in pull requests including files with a designated code owner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#require_code_owner_reviews BranchProtectionV3#require_code_owner_reviews}
        :param required_approving_review_count: Require 'x' number of approvals to satisfy branch protection requirements. If this is specified it must be a number between 0-6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#required_approving_review_count BranchProtectionV3#required_approving_review_count}
        :param require_last_push_approval: Require that the most recent push must be approved by someone other than the last pusher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#require_last_push_approval BranchProtectionV3#require_last_push_approval}
        '''
        value = BranchProtectionV3RequiredPullRequestReviews(
            bypass_pull_request_allowances=bypass_pull_request_allowances,
            dismissal_apps=dismissal_apps,
            dismissal_teams=dismissal_teams,
            dismissal_users=dismissal_users,
            dismiss_stale_reviews=dismiss_stale_reviews,
            include_admins=include_admins,
            require_code_owner_reviews=require_code_owner_reviews,
            required_approving_review_count=required_approving_review_count,
            require_last_push_approval=require_last_push_approval,
        )

        return typing.cast(None, jsii.invoke(self, "putRequiredPullRequestReviews", [value]))

    @jsii.member(jsii_name="putRequiredStatusChecks")
    def put_required_status_checks(
        self,
        *,
        checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        contexts: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param checks: The list of status checks to require in order to merge into this branch. No status checks are required by default. Checks should be strings containing the 'context' and 'app_id' like so 'context:app_id' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#checks BranchProtectionV3#checks}
        :param contexts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#contexts BranchProtectionV3#contexts}.
        :param include_admins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#include_admins BranchProtectionV3#include_admins}.
        :param strict: Require branches to be up to date before merging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#strict BranchProtectionV3#strict}
        '''
        value = BranchProtectionV3RequiredStatusChecks(
            checks=checks,
            contexts=contexts,
            include_admins=include_admins,
            strict=strict,
        )

        return typing.cast(None, jsii.invoke(self, "putRequiredStatusChecks", [value]))

    @jsii.member(jsii_name="putRestrictions")
    def put_restrictions(
        self,
        *,
        apps: typing.Optional[typing.Sequence[builtins.str]] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param apps: The list of app slugs with push access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#apps BranchProtectionV3#apps}
        :param teams: The list of team slugs with push access. Always use slug of the team, not its name. Each team already has to have access to the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#teams BranchProtectionV3#teams}
        :param users: The list of user logins with push access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#users BranchProtectionV3#users}
        '''
        value = BranchProtectionV3Restrictions(apps=apps, teams=teams, users=users)

        return typing.cast(None, jsii.invoke(self, "putRestrictions", [value]))

    @jsii.member(jsii_name="resetEnforceAdmins")
    def reset_enforce_admins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceAdmins", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRequireConversationResolution")
    def reset_require_conversation_resolution(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireConversationResolution", []))

    @jsii.member(jsii_name="resetRequiredPullRequestReviews")
    def reset_required_pull_request_reviews(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredPullRequestReviews", []))

    @jsii.member(jsii_name="resetRequiredStatusChecks")
    def reset_required_status_checks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredStatusChecks", []))

    @jsii.member(jsii_name="resetRequireSignedCommits")
    def reset_require_signed_commits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireSignedCommits", []))

    @jsii.member(jsii_name="resetRestrictions")
    def reset_restrictions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictions", []))

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
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="requiredPullRequestReviews")
    def required_pull_request_reviews(
        self,
    ) -> "BranchProtectionV3RequiredPullRequestReviewsOutputReference":
        return typing.cast("BranchProtectionV3RequiredPullRequestReviewsOutputReference", jsii.get(self, "requiredPullRequestReviews"))

    @builtins.property
    @jsii.member(jsii_name="requiredStatusChecks")
    def required_status_checks(
        self,
    ) -> "BranchProtectionV3RequiredStatusChecksOutputReference":
        return typing.cast("BranchProtectionV3RequiredStatusChecksOutputReference", jsii.get(self, "requiredStatusChecks"))

    @builtins.property
    @jsii.member(jsii_name="restrictions")
    def restrictions(self) -> "BranchProtectionV3RestrictionsOutputReference":
        return typing.cast("BranchProtectionV3RestrictionsOutputReference", jsii.get(self, "restrictions"))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceAdminsInput")
    def enforce_admins_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceAdminsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="requireConversationResolutionInput")
    def require_conversation_resolution_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireConversationResolutionInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredPullRequestReviewsInput")
    def required_pull_request_reviews_input(
        self,
    ) -> typing.Optional["BranchProtectionV3RequiredPullRequestReviews"]:
        return typing.cast(typing.Optional["BranchProtectionV3RequiredPullRequestReviews"], jsii.get(self, "requiredPullRequestReviewsInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredStatusChecksInput")
    def required_status_checks_input(
        self,
    ) -> typing.Optional["BranchProtectionV3RequiredStatusChecks"]:
        return typing.cast(typing.Optional["BranchProtectionV3RequiredStatusChecks"], jsii.get(self, "requiredStatusChecksInput"))

    @builtins.property
    @jsii.member(jsii_name="requireSignedCommitsInput")
    def require_signed_commits_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireSignedCommitsInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictionsInput")
    def restrictions_input(self) -> typing.Optional["BranchProtectionV3Restrictions"]:
        return typing.cast(typing.Optional["BranchProtectionV3Restrictions"], jsii.get(self, "restrictionsInput"))

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e941dd9e945a198329d9da6759e18ec10363d6b9c8896e5e837cf321231daf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__b494d0b0ca6c4a53c6537073e8d36dbe2bbeab041bfd28d6bfcd99c2779cd24b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceAdmins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3beae1f84462efbc7ef65dab1e4ce12b19a54bdffef1c3a9381329af1611f387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7675e7bdc0625a49918ff4a52d0119ee6df49362334591e2f2b3ea58bb8efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__5a0e8b67b5cae3bfe1321f1379cd12b1239d80e6202e0bc940da4b1c24c57bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireConversationResolution", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__0bad4d359beb198132d309be58a4160eaa93e8f8dee074b247a5b7870e85a1d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireSignedCommits", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.branchProtectionV3.BranchProtectionV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "branch": "branch",
        "repository": "repository",
        "enforce_admins": "enforceAdmins",
        "id": "id",
        "require_conversation_resolution": "requireConversationResolution",
        "required_pull_request_reviews": "requiredPullRequestReviews",
        "required_status_checks": "requiredStatusChecks",
        "require_signed_commits": "requireSignedCommits",
        "restrictions": "restrictions",
    },
)
class BranchProtectionV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        branch: builtins.str,
        repository: builtins.str,
        enforce_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        require_conversation_resolution: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_pull_request_reviews: typing.Optional[typing.Union["BranchProtectionV3RequiredPullRequestReviews", typing.Dict[builtins.str, typing.Any]]] = None,
        required_status_checks: typing.Optional[typing.Union["BranchProtectionV3RequiredStatusChecks", typing.Dict[builtins.str, typing.Any]]] = None,
        require_signed_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restrictions: typing.Optional[typing.Union["BranchProtectionV3Restrictions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param branch: The Git branch to protect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#branch BranchProtectionV3#branch}
        :param repository: The GitHub repository name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#repository BranchProtectionV3#repository}
        :param enforce_admins: Setting this to 'true' enforces status checks for repository administrators. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#enforce_admins BranchProtectionV3#enforce_admins}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#id BranchProtectionV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param require_conversation_resolution: Setting this to 'true' requires all conversations on code must be resolved before a pull request can be merged. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#require_conversation_resolution BranchProtectionV3#require_conversation_resolution}
        :param required_pull_request_reviews: required_pull_request_reviews block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#required_pull_request_reviews BranchProtectionV3#required_pull_request_reviews}
        :param required_status_checks: required_status_checks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#required_status_checks BranchProtectionV3#required_status_checks}
        :param require_signed_commits: Setting this to 'true' requires all commits to be signed with GPG. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#require_signed_commits BranchProtectionV3#require_signed_commits}
        :param restrictions: restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#restrictions BranchProtectionV3#restrictions}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(required_pull_request_reviews, dict):
            required_pull_request_reviews = BranchProtectionV3RequiredPullRequestReviews(**required_pull_request_reviews)
        if isinstance(required_status_checks, dict):
            required_status_checks = BranchProtectionV3RequiredStatusChecks(**required_status_checks)
        if isinstance(restrictions, dict):
            restrictions = BranchProtectionV3Restrictions(**restrictions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4353ac3c92969fc3a73c59c5750c795123358446de59ae56a6eb272050401cc7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument enforce_admins", value=enforce_admins, expected_type=type_hints["enforce_admins"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument require_conversation_resolution", value=require_conversation_resolution, expected_type=type_hints["require_conversation_resolution"])
            check_type(argname="argument required_pull_request_reviews", value=required_pull_request_reviews, expected_type=type_hints["required_pull_request_reviews"])
            check_type(argname="argument required_status_checks", value=required_status_checks, expected_type=type_hints["required_status_checks"])
            check_type(argname="argument require_signed_commits", value=require_signed_commits, expected_type=type_hints["require_signed_commits"])
            check_type(argname="argument restrictions", value=restrictions, expected_type=type_hints["restrictions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch": branch,
            "repository": repository,
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
        if enforce_admins is not None:
            self._values["enforce_admins"] = enforce_admins
        if id is not None:
            self._values["id"] = id
        if require_conversation_resolution is not None:
            self._values["require_conversation_resolution"] = require_conversation_resolution
        if required_pull_request_reviews is not None:
            self._values["required_pull_request_reviews"] = required_pull_request_reviews
        if required_status_checks is not None:
            self._values["required_status_checks"] = required_status_checks
        if require_signed_commits is not None:
            self._values["require_signed_commits"] = require_signed_commits
        if restrictions is not None:
            self._values["restrictions"] = restrictions

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
    def branch(self) -> builtins.str:
        '''The Git branch to protect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#branch BranchProtectionV3#branch}
        '''
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''The GitHub repository name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#repository BranchProtectionV3#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enforce_admins(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to 'true' enforces status checks for repository administrators.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#enforce_admins BranchProtectionV3#enforce_admins}
        '''
        result = self._values.get("enforce_admins")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#id BranchProtectionV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_conversation_resolution(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to 'true' requires all conversations on code must be resolved before a pull request can be merged.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#require_conversation_resolution BranchProtectionV3#require_conversation_resolution}
        '''
        result = self._values.get("require_conversation_resolution")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_pull_request_reviews(
        self,
    ) -> typing.Optional["BranchProtectionV3RequiredPullRequestReviews"]:
        '''required_pull_request_reviews block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#required_pull_request_reviews BranchProtectionV3#required_pull_request_reviews}
        '''
        result = self._values.get("required_pull_request_reviews")
        return typing.cast(typing.Optional["BranchProtectionV3RequiredPullRequestReviews"], result)

    @builtins.property
    def required_status_checks(
        self,
    ) -> typing.Optional["BranchProtectionV3RequiredStatusChecks"]:
        '''required_status_checks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#required_status_checks BranchProtectionV3#required_status_checks}
        '''
        result = self._values.get("required_status_checks")
        return typing.cast(typing.Optional["BranchProtectionV3RequiredStatusChecks"], result)

    @builtins.property
    def require_signed_commits(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to 'true' requires all commits to be signed with GPG.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#require_signed_commits BranchProtectionV3#require_signed_commits}
        '''
        result = self._values.get("require_signed_commits")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restrictions(self) -> typing.Optional["BranchProtectionV3Restrictions"]:
        '''restrictions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#restrictions BranchProtectionV3#restrictions}
        '''
        result = self._values.get("restrictions")
        return typing.cast(typing.Optional["BranchProtectionV3Restrictions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.branchProtectionV3.BranchProtectionV3RequiredPullRequestReviews",
    jsii_struct_bases=[],
    name_mapping={
        "bypass_pull_request_allowances": "bypassPullRequestAllowances",
        "dismissal_apps": "dismissalApps",
        "dismissal_teams": "dismissalTeams",
        "dismissal_users": "dismissalUsers",
        "dismiss_stale_reviews": "dismissStaleReviews",
        "include_admins": "includeAdmins",
        "require_code_owner_reviews": "requireCodeOwnerReviews",
        "required_approving_review_count": "requiredApprovingReviewCount",
        "require_last_push_approval": "requireLastPushApproval",
    },
)
class BranchProtectionV3RequiredPullRequestReviews:
    def __init__(
        self,
        *,
        bypass_pull_request_allowances: typing.Optional[typing.Union["BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances", typing.Dict[builtins.str, typing.Any]]] = None,
        dismissal_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
        dismissal_teams: typing.Optional[typing.Sequence[builtins.str]] = None,
        dismissal_users: typing.Optional[typing.Sequence[builtins.str]] = None,
        dismiss_stale_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_code_owner_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_approving_review_count: typing.Optional[jsii.Number] = None,
        require_last_push_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bypass_pull_request_allowances: bypass_pull_request_allowances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#bypass_pull_request_allowances BranchProtectionV3#bypass_pull_request_allowances}
        :param dismissal_apps: The list of apps slugs with dismissal access. Always use slug of the app, not its name. Each app already has to have access to the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#dismissal_apps BranchProtectionV3#dismissal_apps}
        :param dismissal_teams: The list of team slugs with dismissal access. Always use slug of the team, not its name. Each team already has to have access to the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#dismissal_teams BranchProtectionV3#dismissal_teams}
        :param dismissal_users: The list of user logins with dismissal access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#dismissal_users BranchProtectionV3#dismissal_users}
        :param dismiss_stale_reviews: Dismiss approved reviews automatically when a new commit is pushed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#dismiss_stale_reviews BranchProtectionV3#dismiss_stale_reviews}
        :param include_admins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#include_admins BranchProtectionV3#include_admins}.
        :param require_code_owner_reviews: Require an approved review in pull requests including files with a designated code owner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#require_code_owner_reviews BranchProtectionV3#require_code_owner_reviews}
        :param required_approving_review_count: Require 'x' number of approvals to satisfy branch protection requirements. If this is specified it must be a number between 0-6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#required_approving_review_count BranchProtectionV3#required_approving_review_count}
        :param require_last_push_approval: Require that the most recent push must be approved by someone other than the last pusher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#require_last_push_approval BranchProtectionV3#require_last_push_approval}
        '''
        if isinstance(bypass_pull_request_allowances, dict):
            bypass_pull_request_allowances = BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances(**bypass_pull_request_allowances)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0131a1558a688179cbe6e7e26f0ae8666bd6693787c1b7811dbea084f3d8c46)
            check_type(argname="argument bypass_pull_request_allowances", value=bypass_pull_request_allowances, expected_type=type_hints["bypass_pull_request_allowances"])
            check_type(argname="argument dismissal_apps", value=dismissal_apps, expected_type=type_hints["dismissal_apps"])
            check_type(argname="argument dismissal_teams", value=dismissal_teams, expected_type=type_hints["dismissal_teams"])
            check_type(argname="argument dismissal_users", value=dismissal_users, expected_type=type_hints["dismissal_users"])
            check_type(argname="argument dismiss_stale_reviews", value=dismiss_stale_reviews, expected_type=type_hints["dismiss_stale_reviews"])
            check_type(argname="argument include_admins", value=include_admins, expected_type=type_hints["include_admins"])
            check_type(argname="argument require_code_owner_reviews", value=require_code_owner_reviews, expected_type=type_hints["require_code_owner_reviews"])
            check_type(argname="argument required_approving_review_count", value=required_approving_review_count, expected_type=type_hints["required_approving_review_count"])
            check_type(argname="argument require_last_push_approval", value=require_last_push_approval, expected_type=type_hints["require_last_push_approval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bypass_pull_request_allowances is not None:
            self._values["bypass_pull_request_allowances"] = bypass_pull_request_allowances
        if dismissal_apps is not None:
            self._values["dismissal_apps"] = dismissal_apps
        if dismissal_teams is not None:
            self._values["dismissal_teams"] = dismissal_teams
        if dismissal_users is not None:
            self._values["dismissal_users"] = dismissal_users
        if dismiss_stale_reviews is not None:
            self._values["dismiss_stale_reviews"] = dismiss_stale_reviews
        if include_admins is not None:
            self._values["include_admins"] = include_admins
        if require_code_owner_reviews is not None:
            self._values["require_code_owner_reviews"] = require_code_owner_reviews
        if required_approving_review_count is not None:
            self._values["required_approving_review_count"] = required_approving_review_count
        if require_last_push_approval is not None:
            self._values["require_last_push_approval"] = require_last_push_approval

    @builtins.property
    def bypass_pull_request_allowances(
        self,
    ) -> typing.Optional["BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances"]:
        '''bypass_pull_request_allowances block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#bypass_pull_request_allowances BranchProtectionV3#bypass_pull_request_allowances}
        '''
        result = self._values.get("bypass_pull_request_allowances")
        return typing.cast(typing.Optional["BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances"], result)

    @builtins.property
    def dismissal_apps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of apps slugs with dismissal access.

        Always use slug of the app, not its name. Each app already has to have access to the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#dismissal_apps BranchProtectionV3#dismissal_apps}
        '''
        result = self._values.get("dismissal_apps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dismissal_teams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of team slugs with dismissal access.

        Always use slug of the team, not its name. Each team already has to have access to the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#dismissal_teams BranchProtectionV3#dismissal_teams}
        '''
        result = self._values.get("dismissal_teams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dismissal_users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of user logins with dismissal access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#dismissal_users BranchProtectionV3#dismissal_users}
        '''
        result = self._values.get("dismissal_users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dismiss_stale_reviews(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Dismiss approved reviews automatically when a new commit is pushed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#dismiss_stale_reviews BranchProtectionV3#dismiss_stale_reviews}
        '''
        result = self._values.get("dismiss_stale_reviews")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_admins(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#include_admins BranchProtectionV3#include_admins}.'''
        result = self._values.get("include_admins")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_code_owner_reviews(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require an approved review in pull requests including files with a designated code owner.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#require_code_owner_reviews BranchProtectionV3#require_code_owner_reviews}
        '''
        result = self._values.get("require_code_owner_reviews")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_approving_review_count(self) -> typing.Optional[jsii.Number]:
        '''Require 'x' number of approvals to satisfy branch protection requirements.

        If this is specified it must be a number between 0-6.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#required_approving_review_count BranchProtectionV3#required_approving_review_count}
        '''
        result = self._values.get("required_approving_review_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def require_last_push_approval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require that the most recent push must be approved by someone other than the last pusher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#require_last_push_approval BranchProtectionV3#require_last_push_approval}
        '''
        result = self._values.get("require_last_push_approval")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionV3RequiredPullRequestReviews(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.branchProtectionV3.BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances",
    jsii_struct_bases=[],
    name_mapping={"apps": "apps", "teams": "teams", "users": "users"},
)
class BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances:
    def __init__(
        self,
        *,
        apps: typing.Optional[typing.Sequence[builtins.str]] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param apps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#apps BranchProtectionV3#apps}.
        :param teams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#teams BranchProtectionV3#teams}.
        :param users: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#users BranchProtectionV3#users}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5ecea5383d2630fd5b9e710a7feaadd0260b85669543880d523e7e7e42ee47e)
            check_type(argname="argument apps", value=apps, expected_type=type_hints["apps"])
            check_type(argname="argument teams", value=teams, expected_type=type_hints["teams"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apps is not None:
            self._values["apps"] = apps
        if teams is not None:
            self._values["teams"] = teams
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def apps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#apps BranchProtectionV3#apps}.'''
        result = self._values.get("apps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def teams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#teams BranchProtectionV3#teams}.'''
        result = self._values.get("teams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#users BranchProtectionV3#users}.'''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowancesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.branchProtectionV3.BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowancesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf0dacc3d20372a0c43d75caaf71d2d32539790197f0fb8c9992c8db57254132)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApps")
    def reset_apps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApps", []))

    @jsii.member(jsii_name="resetTeams")
    def reset_teams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeams", []))

    @jsii.member(jsii_name="resetUsers")
    def reset_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsers", []))

    @builtins.property
    @jsii.member(jsii_name="appsInput")
    def apps_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "appsInput"))

    @builtins.property
    @jsii.member(jsii_name="teamsInput")
    def teams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "teamsInput"))

    @builtins.property
    @jsii.member(jsii_name="usersInput")
    def users_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="apps")
    def apps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apps"))

    @apps.setter
    def apps(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f470ea5dd96d66cbcdd65ad48a20c992739352621bd0697aabf434a273537343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="teams")
    def teams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "teams"))

    @teams.setter
    def teams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1288d76193a05f2f86a708179d5c897c542cc54e9fda18a1f49bd720b8143f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f68c7a5c41c77a41dc6ae2c3ed8d6920d50ebf4a2f125106de21572354ca87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances]:
        return typing.cast(typing.Optional[BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a09110d9a4f755abf615a1ab25e81953ddc2d8eae0733bd68110f460a663004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BranchProtectionV3RequiredPullRequestReviewsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.branchProtectionV3.BranchProtectionV3RequiredPullRequestReviewsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b47ad1dae1d5d9db1192a12f9be99ef629ae6514de3d9420ab9ee92872018b5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBypassPullRequestAllowances")
    def put_bypass_pull_request_allowances(
        self,
        *,
        apps: typing.Optional[typing.Sequence[builtins.str]] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param apps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#apps BranchProtectionV3#apps}.
        :param teams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#teams BranchProtectionV3#teams}.
        :param users: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#users BranchProtectionV3#users}.
        '''
        value = BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances(
            apps=apps, teams=teams, users=users
        )

        return typing.cast(None, jsii.invoke(self, "putBypassPullRequestAllowances", [value]))

    @jsii.member(jsii_name="resetBypassPullRequestAllowances")
    def reset_bypass_pull_request_allowances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBypassPullRequestAllowances", []))

    @jsii.member(jsii_name="resetDismissalApps")
    def reset_dismissal_apps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDismissalApps", []))

    @jsii.member(jsii_name="resetDismissalTeams")
    def reset_dismissal_teams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDismissalTeams", []))

    @jsii.member(jsii_name="resetDismissalUsers")
    def reset_dismissal_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDismissalUsers", []))

    @jsii.member(jsii_name="resetDismissStaleReviews")
    def reset_dismiss_stale_reviews(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDismissStaleReviews", []))

    @jsii.member(jsii_name="resetIncludeAdmins")
    def reset_include_admins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeAdmins", []))

    @jsii.member(jsii_name="resetRequireCodeOwnerReviews")
    def reset_require_code_owner_reviews(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireCodeOwnerReviews", []))

    @jsii.member(jsii_name="resetRequiredApprovingReviewCount")
    def reset_required_approving_review_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredApprovingReviewCount", []))

    @jsii.member(jsii_name="resetRequireLastPushApproval")
    def reset_require_last_push_approval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireLastPushApproval", []))

    @builtins.property
    @jsii.member(jsii_name="bypassPullRequestAllowances")
    def bypass_pull_request_allowances(
        self,
    ) -> BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowancesOutputReference:
        return typing.cast(BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowancesOutputReference, jsii.get(self, "bypassPullRequestAllowances"))

    @builtins.property
    @jsii.member(jsii_name="bypassPullRequestAllowancesInput")
    def bypass_pull_request_allowances_input(
        self,
    ) -> typing.Optional[BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances]:
        return typing.cast(typing.Optional[BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances], jsii.get(self, "bypassPullRequestAllowancesInput"))

    @builtins.property
    @jsii.member(jsii_name="dismissalAppsInput")
    def dismissal_apps_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dismissalAppsInput"))

    @builtins.property
    @jsii.member(jsii_name="dismissalTeamsInput")
    def dismissal_teams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dismissalTeamsInput"))

    @builtins.property
    @jsii.member(jsii_name="dismissalUsersInput")
    def dismissal_users_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dismissalUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="dismissStaleReviewsInput")
    def dismiss_stale_reviews_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dismissStaleReviewsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeAdminsInput")
    def include_admins_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeAdminsInput"))

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
    @jsii.member(jsii_name="dismissalApps")
    def dismissal_apps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dismissalApps"))

    @dismissal_apps.setter
    def dismissal_apps(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32d7555d6cf5bd60eef6bad6eebe044f589e5b89e55c86aa3d97a23df41ed7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dismissalApps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dismissalTeams")
    def dismissal_teams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dismissalTeams"))

    @dismissal_teams.setter
    def dismissal_teams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc09e00bab5a4154508871797d9232b73ba64f895956952a30a2f75cb7acc5c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dismissalTeams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dismissalUsers")
    def dismissal_users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dismissalUsers"))

    @dismissal_users.setter
    def dismissal_users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9558c703f0bf0e9a055bcb3b60c1274f2e643296e1ea60b0d8a71a2430c27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dismissalUsers", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__e203d1d24acc458fa90357e29d4f3315342411e33af2011369a95b0daf0bd697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dismissStaleReviews", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeAdmins")
    def include_admins(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeAdmins"))

    @include_admins.setter
    def include_admins(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89da8c8ce466cc211ece9c79c6cc3a8ca53760699b4f96f8210ccf04b0da577a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeAdmins", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__9dcea4eedac35970551dac106dc17f87f877cab3e32ca1dbef2dfc1eff0e48bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireCodeOwnerReviews", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredApprovingReviewCount")
    def required_approving_review_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "requiredApprovingReviewCount"))

    @required_approving_review_count.setter
    def required_approving_review_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__949a4bb08e2a40457200d7109cf4350174e37c0b66924c6475834e6f5787844a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb5e8ad626c6c54ea7502f52ba4b068ac169544c05a3d9f6d664f45ccd0dc7d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireLastPushApproval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BranchProtectionV3RequiredPullRequestReviews]:
        return typing.cast(typing.Optional[BranchProtectionV3RequiredPullRequestReviews], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BranchProtectionV3RequiredPullRequestReviews],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d51dd46f972e55637847d7519b5a2ce2d88da6c849f2cdb111510ac730a0965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.branchProtectionV3.BranchProtectionV3RequiredStatusChecks",
    jsii_struct_bases=[],
    name_mapping={
        "checks": "checks",
        "contexts": "contexts",
        "include_admins": "includeAdmins",
        "strict": "strict",
    },
)
class BranchProtectionV3RequiredStatusChecks:
    def __init__(
        self,
        *,
        checks: typing.Optional[typing.Sequence[builtins.str]] = None,
        contexts: typing.Optional[typing.Sequence[builtins.str]] = None,
        include_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param checks: The list of status checks to require in order to merge into this branch. No status checks are required by default. Checks should be strings containing the 'context' and 'app_id' like so 'context:app_id' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#checks BranchProtectionV3#checks}
        :param contexts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#contexts BranchProtectionV3#contexts}.
        :param include_admins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#include_admins BranchProtectionV3#include_admins}.
        :param strict: Require branches to be up to date before merging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#strict BranchProtectionV3#strict}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b386f85149f964155cc721dadbd98ff804ad76f7bd116a4643069014140eee72)
            check_type(argname="argument checks", value=checks, expected_type=type_hints["checks"])
            check_type(argname="argument contexts", value=contexts, expected_type=type_hints["contexts"])
            check_type(argname="argument include_admins", value=include_admins, expected_type=type_hints["include_admins"])
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if checks is not None:
            self._values["checks"] = checks
        if contexts is not None:
            self._values["contexts"] = contexts
        if include_admins is not None:
            self._values["include_admins"] = include_admins
        if strict is not None:
            self._values["strict"] = strict

    @builtins.property
    def checks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of status checks to require in order to merge into this branch.

        No status checks are required by default. Checks should be strings containing the 'context' and 'app_id' like so 'context:app_id'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#checks BranchProtectionV3#checks}
        '''
        result = self._values.get("checks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def contexts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#contexts BranchProtectionV3#contexts}.'''
        result = self._values.get("contexts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def include_admins(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#include_admins BranchProtectionV3#include_admins}.'''
        result = self._values.get("include_admins")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def strict(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require branches to be up to date before merging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#strict BranchProtectionV3#strict}
        '''
        result = self._values.get("strict")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionV3RequiredStatusChecks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BranchProtectionV3RequiredStatusChecksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.branchProtectionV3.BranchProtectionV3RequiredStatusChecksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f355c77df2cdd733d0837707ff28e99257d368a3c8df36432be48fec3fc9c65b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChecks")
    def reset_checks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChecks", []))

    @jsii.member(jsii_name="resetContexts")
    def reset_contexts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContexts", []))

    @jsii.member(jsii_name="resetIncludeAdmins")
    def reset_include_admins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeAdmins", []))

    @jsii.member(jsii_name="resetStrict")
    def reset_strict(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrict", []))

    @builtins.property
    @jsii.member(jsii_name="checksInput")
    def checks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "checksInput"))

    @builtins.property
    @jsii.member(jsii_name="contextsInput")
    def contexts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contextsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeAdminsInput")
    def include_admins_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeAdminsInput"))

    @builtins.property
    @jsii.member(jsii_name="strictInput")
    def strict_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "strictInput"))

    @builtins.property
    @jsii.member(jsii_name="checks")
    def checks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "checks"))

    @checks.setter
    def checks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f582f87a0a640a84149029e6e7c8ad56ebedd86e6b4d326dcdce1eb4c16f6dd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contexts")
    def contexts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contexts"))

    @contexts.setter
    def contexts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e3345066e1af9e37205a811e84f55cafbabb59d1ab936f675f30c708f3dbf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contexts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeAdmins")
    def include_admins(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeAdmins"))

    @include_admins.setter
    def include_admins(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff9ff3e32b2c15db79442238a97bccde7a6eecfbe7076f18696fcdb3235f762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeAdmins", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__1da807f0777d5136236ebf7b253d32549e35fce1bc1ed8bb92480b9dd20e30b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strict", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BranchProtectionV3RequiredStatusChecks]:
        return typing.cast(typing.Optional[BranchProtectionV3RequiredStatusChecks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BranchProtectionV3RequiredStatusChecks],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be0a6bed4c20ebfb29cd661e71b9bbdf8a75d254a074c2e06c50fcc8fa4c47c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.branchProtectionV3.BranchProtectionV3Restrictions",
    jsii_struct_bases=[],
    name_mapping={"apps": "apps", "teams": "teams", "users": "users"},
)
class BranchProtectionV3Restrictions:
    def __init__(
        self,
        *,
        apps: typing.Optional[typing.Sequence[builtins.str]] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param apps: The list of app slugs with push access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#apps BranchProtectionV3#apps}
        :param teams: The list of team slugs with push access. Always use slug of the team, not its name. Each team already has to have access to the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#teams BranchProtectionV3#teams}
        :param users: The list of user logins with push access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#users BranchProtectionV3#users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c153460c5b324584f9b44993078b841eb9e4c11cca4ad43890e9717617e8bad)
            check_type(argname="argument apps", value=apps, expected_type=type_hints["apps"])
            check_type(argname="argument teams", value=teams, expected_type=type_hints["teams"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apps is not None:
            self._values["apps"] = apps
        if teams is not None:
            self._values["teams"] = teams
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def apps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of app slugs with push access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#apps BranchProtectionV3#apps}
        '''
        result = self._values.get("apps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def teams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of team slugs with push access.

        Always use slug of the team, not its name. Each team already has to have access to the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#teams BranchProtectionV3#teams}
        '''
        result = self._values.get("teams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of user logins with push access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/branch_protection_v3#users BranchProtectionV3#users}
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProtectionV3Restrictions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BranchProtectionV3RestrictionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.branchProtectionV3.BranchProtectionV3RestrictionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b1f5f98270bce39a2019dc609e767b71126a175c78ea978f9bccb9c4a9fadca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetApps")
    def reset_apps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApps", []))

    @jsii.member(jsii_name="resetTeams")
    def reset_teams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeams", []))

    @jsii.member(jsii_name="resetUsers")
    def reset_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsers", []))

    @builtins.property
    @jsii.member(jsii_name="appsInput")
    def apps_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "appsInput"))

    @builtins.property
    @jsii.member(jsii_name="teamsInput")
    def teams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "teamsInput"))

    @builtins.property
    @jsii.member(jsii_name="usersInput")
    def users_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="apps")
    def apps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apps"))

    @apps.setter
    def apps(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feea3a345898f0b1c2722322961d6ccf0f95ec83842494c7519977c8c7caabcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="teams")
    def teams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "teams"))

    @teams.setter
    def teams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6239f90461e03b8bd86c186c916730936612dc192f8979ffedbed7e27beac1b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a309f88f6a3c0a65a8c445a1e57b226512992a777fb8bd487bea0e94c6b3cb99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BranchProtectionV3Restrictions]:
        return typing.cast(typing.Optional[BranchProtectionV3Restrictions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BranchProtectionV3Restrictions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15db7c8722433c6307eb8511cf05855f6079baae607753388f504d2821aa0ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BranchProtectionV3",
    "BranchProtectionV3Config",
    "BranchProtectionV3RequiredPullRequestReviews",
    "BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances",
    "BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowancesOutputReference",
    "BranchProtectionV3RequiredPullRequestReviewsOutputReference",
    "BranchProtectionV3RequiredStatusChecks",
    "BranchProtectionV3RequiredStatusChecksOutputReference",
    "BranchProtectionV3Restrictions",
    "BranchProtectionV3RestrictionsOutputReference",
]

publication.publish()

def _typecheckingstub__039872cea41507d4e2ed84413e7eb4a02bc02877ab2ea2b02ec7bcb05844a193(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    branch: builtins.str,
    repository: builtins.str,
    enforce_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    require_conversation_resolution: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_pull_request_reviews: typing.Optional[typing.Union[BranchProtectionV3RequiredPullRequestReviews, typing.Dict[builtins.str, typing.Any]]] = None,
    required_status_checks: typing.Optional[typing.Union[BranchProtectionV3RequiredStatusChecks, typing.Dict[builtins.str, typing.Any]]] = None,
    require_signed_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restrictions: typing.Optional[typing.Union[BranchProtectionV3Restrictions, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4335e89d3fa2d2f5b920eff3c8ed984e1358d372976c389f7baa92890213a596(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e941dd9e945a198329d9da6759e18ec10363d6b9c8896e5e837cf321231daf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b494d0b0ca6c4a53c6537073e8d36dbe2bbeab041bfd28d6bfcd99c2779cd24b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3beae1f84462efbc7ef65dab1e4ce12b19a54bdffef1c3a9381329af1611f387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7675e7bdc0625a49918ff4a52d0119ee6df49362334591e2f2b3ea58bb8efc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0e8b67b5cae3bfe1321f1379cd12b1239d80e6202e0bc940da4b1c24c57bd3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bad4d359beb198132d309be58a4160eaa93e8f8dee074b247a5b7870e85a1d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4353ac3c92969fc3a73c59c5750c795123358446de59ae56a6eb272050401cc7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    branch: builtins.str,
    repository: builtins.str,
    enforce_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    require_conversation_resolution: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_pull_request_reviews: typing.Optional[typing.Union[BranchProtectionV3RequiredPullRequestReviews, typing.Dict[builtins.str, typing.Any]]] = None,
    required_status_checks: typing.Optional[typing.Union[BranchProtectionV3RequiredStatusChecks, typing.Dict[builtins.str, typing.Any]]] = None,
    require_signed_commits: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restrictions: typing.Optional[typing.Union[BranchProtectionV3Restrictions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0131a1558a688179cbe6e7e26f0ae8666bd6693787c1b7811dbea084f3d8c46(
    *,
    bypass_pull_request_allowances: typing.Optional[typing.Union[BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances, typing.Dict[builtins.str, typing.Any]]] = None,
    dismissal_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
    dismissal_teams: typing.Optional[typing.Sequence[builtins.str]] = None,
    dismissal_users: typing.Optional[typing.Sequence[builtins.str]] = None,
    dismiss_stale_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_code_owner_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_approving_review_count: typing.Optional[jsii.Number] = None,
    require_last_push_approval: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ecea5383d2630fd5b9e710a7feaadd0260b85669543880d523e7e7e42ee47e(
    *,
    apps: typing.Optional[typing.Sequence[builtins.str]] = None,
    teams: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0dacc3d20372a0c43d75caaf71d2d32539790197f0fb8c9992c8db57254132(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f470ea5dd96d66cbcdd65ad48a20c992739352621bd0697aabf434a273537343(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1288d76193a05f2f86a708179d5c897c542cc54e9fda18a1f49bd720b8143f46(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f68c7a5c41c77a41dc6ae2c3ed8d6920d50ebf4a2f125106de21572354ca87(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a09110d9a4f755abf615a1ab25e81953ddc2d8eae0733bd68110f460a663004(
    value: typing.Optional[BranchProtectionV3RequiredPullRequestReviewsBypassPullRequestAllowances],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47ad1dae1d5d9db1192a12f9be99ef629ae6514de3d9420ab9ee92872018b5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32d7555d6cf5bd60eef6bad6eebe044f589e5b89e55c86aa3d97a23df41ed7b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc09e00bab5a4154508871797d9232b73ba64f895956952a30a2f75cb7acc5c9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9558c703f0bf0e9a055bcb3b60c1274f2e643296e1ea60b0d8a71a2430c27c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e203d1d24acc458fa90357e29d4f3315342411e33af2011369a95b0daf0bd697(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89da8c8ce466cc211ece9c79c6cc3a8ca53760699b4f96f8210ccf04b0da577a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dcea4eedac35970551dac106dc17f87f877cab3e32ca1dbef2dfc1eff0e48bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949a4bb08e2a40457200d7109cf4350174e37c0b66924c6475834e6f5787844a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5e8ad626c6c54ea7502f52ba4b068ac169544c05a3d9f6d664f45ccd0dc7d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d51dd46f972e55637847d7519b5a2ce2d88da6c849f2cdb111510ac730a0965(
    value: typing.Optional[BranchProtectionV3RequiredPullRequestReviews],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b386f85149f964155cc721dadbd98ff804ad76f7bd116a4643069014140eee72(
    *,
    checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    contexts: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    strict: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f355c77df2cdd733d0837707ff28e99257d368a3c8df36432be48fec3fc9c65b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f582f87a0a640a84149029e6e7c8ad56ebedd86e6b4d326dcdce1eb4c16f6dd9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e3345066e1af9e37205a811e84f55cafbabb59d1ab936f675f30c708f3dbf5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff9ff3e32b2c15db79442238a97bccde7a6eecfbe7076f18696fcdb3235f762(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da807f0777d5136236ebf7b253d32549e35fce1bc1ed8bb92480b9dd20e30b8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0a6bed4c20ebfb29cd661e71b9bbdf8a75d254a074c2e06c50fcc8fa4c47c5(
    value: typing.Optional[BranchProtectionV3RequiredStatusChecks],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c153460c5b324584f9b44993078b841eb9e4c11cca4ad43890e9717617e8bad(
    *,
    apps: typing.Optional[typing.Sequence[builtins.str]] = None,
    teams: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1f5f98270bce39a2019dc609e767b71126a175c78ea978f9bccb9c4a9fadca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feea3a345898f0b1c2722322961d6ccf0f95ec83842494c7519977c8c7caabcf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6239f90461e03b8bd86c186c916730936612dc192f8979ffedbed7e27beac1b1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a309f88f6a3c0a65a8c445a1e57b226512992a777fb8bd487bea0e94c6b3cb99(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15db7c8722433c6307eb8511cf05855f6079baae607753388f504d2821aa0ad8(
    value: typing.Optional[BranchProtectionV3Restrictions],
) -> None:
    """Type checking stubs"""
    pass
