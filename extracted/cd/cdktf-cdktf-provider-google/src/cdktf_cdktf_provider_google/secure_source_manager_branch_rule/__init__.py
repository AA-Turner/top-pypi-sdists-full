r'''
# `google_secure_source_manager_branch_rule`

Refer to the Terraform Registry for docs: [`google_secure_source_manager_branch_rule`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule).
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


class SecureSourceManagerBranchRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secureSourceManagerBranchRule.SecureSourceManagerBranchRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule google_secure_source_manager_branch_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        branch_rule_id: builtins.str,
        include_pattern: builtins.str,
        location: builtins.str,
        repository_id: builtins.str,
        allow_stale_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        minimum_approvals_count: typing.Optional[jsii.Number] = None,
        minimum_reviews_count: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        require_comments_resolved: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_pull_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["SecureSourceManagerBranchRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule google_secure_source_manager_branch_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param branch_rule_id: The ID for the BranchRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#branch_rule_id SecureSourceManagerBranchRule#branch_rule_id}
        :param include_pattern: The BranchRule matches branches based on the specified regular expression. Use .* to match all branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#include_pattern SecureSourceManagerBranchRule#include_pattern}
        :param location: The location for the Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#location SecureSourceManagerBranchRule#location}
        :param repository_id: The ID for the Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#repository_id SecureSourceManagerBranchRule#repository_id}
        :param allow_stale_reviews: Determines if allow stale reviews or approvals before merging to the branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#allow_stale_reviews SecureSourceManagerBranchRule#allow_stale_reviews}
        :param disabled: Determines if the branch rule is disabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#disabled SecureSourceManagerBranchRule#disabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#id SecureSourceManagerBranchRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimum_approvals_count: The minimum number of approvals required for the branch rule to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#minimum_approvals_count SecureSourceManagerBranchRule#minimum_approvals_count}
        :param minimum_reviews_count: The minimum number of reviews required for the branch rule to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#minimum_reviews_count SecureSourceManagerBranchRule#minimum_reviews_count}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#project SecureSourceManagerBranchRule#project}.
        :param require_comments_resolved: Determines if require comments resolved before merging to the branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#require_comments_resolved SecureSourceManagerBranchRule#require_comments_resolved}
        :param require_linear_history: Determines if require linear history before merging to the branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#require_linear_history SecureSourceManagerBranchRule#require_linear_history}
        :param require_pull_request: Determines if the branch rule requires a pull request or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#require_pull_request SecureSourceManagerBranchRule#require_pull_request}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#timeouts SecureSourceManagerBranchRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c63b4c2cde0f02843fcd2bce974ac339cba59631717be2387d1f3ca08c5199cd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SecureSourceManagerBranchRuleConfig(
            branch_rule_id=branch_rule_id,
            include_pattern=include_pattern,
            location=location,
            repository_id=repository_id,
            allow_stale_reviews=allow_stale_reviews,
            disabled=disabled,
            id=id,
            minimum_approvals_count=minimum_approvals_count,
            minimum_reviews_count=minimum_reviews_count,
            project=project,
            require_comments_resolved=require_comments_resolved,
            require_linear_history=require_linear_history,
            require_pull_request=require_pull_request,
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
        '''Generates CDKTF code for importing a SecureSourceManagerBranchRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SecureSourceManagerBranchRule to import.
        :param import_from_id: The id of the existing SecureSourceManagerBranchRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SecureSourceManagerBranchRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7def9b516d695fdb11ea1c10bd96bc48a896b0cc37037463ad83d25be96d37ac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#create SecureSourceManagerBranchRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#delete SecureSourceManagerBranchRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#update SecureSourceManagerBranchRule#update}.
        '''
        value = SecureSourceManagerBranchRuleTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAllowStaleReviews")
    def reset_allow_stale_reviews(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowStaleReviews", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinimumApprovalsCount")
    def reset_minimum_approvals_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumApprovalsCount", []))

    @jsii.member(jsii_name="resetMinimumReviewsCount")
    def reset_minimum_reviews_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumReviewsCount", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRequireCommentsResolved")
    def reset_require_comments_resolved(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireCommentsResolved", []))

    @jsii.member(jsii_name="resetRequireLinearHistory")
    def reset_require_linear_history(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireLinearHistory", []))

    @jsii.member(jsii_name="resetRequirePullRequest")
    def reset_require_pull_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequirePullRequest", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SecureSourceManagerBranchRuleTimeoutsOutputReference":
        return typing.cast("SecureSourceManagerBranchRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="allowStaleReviewsInput")
    def allow_stale_reviews_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowStaleReviewsInput"))

    @builtins.property
    @jsii.member(jsii_name="branchRuleIdInput")
    def branch_rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchRuleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includePatternInput")
    def include_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includePatternInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumApprovalsCountInput")
    def minimum_approvals_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumApprovalsCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumReviewsCountInput")
    def minimum_reviews_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumReviewsCountInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryIdInput")
    def repository_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="requireCommentsResolvedInput")
    def require_comments_resolved_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireCommentsResolvedInput"))

    @builtins.property
    @jsii.member(jsii_name="requireLinearHistoryInput")
    def require_linear_history_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireLinearHistoryInput"))

    @builtins.property
    @jsii.member(jsii_name="requirePullRequestInput")
    def require_pull_request_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requirePullRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SecureSourceManagerBranchRuleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SecureSourceManagerBranchRuleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowStaleReviews")
    def allow_stale_reviews(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowStaleReviews"))

    @allow_stale_reviews.setter
    def allow_stale_reviews(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d50f2ecebf314aa31a5e64186893135d3ef0086465da5dd656f9fdc71c1d972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowStaleReviews", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="branchRuleId")
    def branch_rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branchRuleId"))

    @branch_rule_id.setter
    def branch_rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2c74339625ac82b572ae7b9ff13a3545de742b4f32df19cf478f498c2376a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchRuleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6e3dcf54de8e0f67840ded5c033f63a54c5e0ec3bf4d09c1313d781b8aeb0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12127451ab8309030d02e03c26e3404a8e94820a09cbb1c37a527a7657b1de6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includePattern")
    def include_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "includePattern"))

    @include_pattern.setter
    def include_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fedd89b4b633c261a92d5871f55c2ac6cba9816671a2b69e199602869678b658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includePattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af9d0f26ac15e160e1c292b870a05d20636727c36681f2fd25f1537de99c2f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumApprovalsCount")
    def minimum_approvals_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumApprovalsCount"))

    @minimum_approvals_count.setter
    def minimum_approvals_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__875aeae7e289818aa7b5a76860bc1d6ec1cb28a3dabb76422d3ee919fabd0c40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumApprovalsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumReviewsCount")
    def minimum_reviews_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumReviewsCount"))

    @minimum_reviews_count.setter
    def minimum_reviews_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde7344427a0de8227c557a3c854bae28640f27b037e76b68734227c9a464c1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumReviewsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e7d14d94cd9c82124ac037fff8843435e6e5a00a08193291c3fe55d67f18a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryId")
    def repository_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryId"))

    @repository_id.setter
    def repository_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153fdbfabb9622c13b2d928005db818f4571d23f4a83814ae0b3754a039a5b03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireCommentsResolved")
    def require_comments_resolved(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireCommentsResolved"))

    @require_comments_resolved.setter
    def require_comments_resolved(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cbe7c8ca24a0977544f58dc3e40caa4479a0bd6602e2c9b25385da1a25537d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireCommentsResolved", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireLinearHistory")
    def require_linear_history(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireLinearHistory"))

    @require_linear_history.setter
    def require_linear_history(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bff55205c65f4eed212ec949f042f5674c87c3c41c441f6ef5bf92b096d4a595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireLinearHistory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requirePullRequest")
    def require_pull_request(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requirePullRequest"))

    @require_pull_request.setter
    def require_pull_request(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f17639caeef480790b1778029d9890773b230c8a3d687fb5fca81f3037c5cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requirePullRequest", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secureSourceManagerBranchRule.SecureSourceManagerBranchRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "branch_rule_id": "branchRuleId",
        "include_pattern": "includePattern",
        "location": "location",
        "repository_id": "repositoryId",
        "allow_stale_reviews": "allowStaleReviews",
        "disabled": "disabled",
        "id": "id",
        "minimum_approvals_count": "minimumApprovalsCount",
        "minimum_reviews_count": "minimumReviewsCount",
        "project": "project",
        "require_comments_resolved": "requireCommentsResolved",
        "require_linear_history": "requireLinearHistory",
        "require_pull_request": "requirePullRequest",
        "timeouts": "timeouts",
    },
)
class SecureSourceManagerBranchRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        branch_rule_id: builtins.str,
        include_pattern: builtins.str,
        location: builtins.str,
        repository_id: builtins.str,
        allow_stale_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        minimum_approvals_count: typing.Optional[jsii.Number] = None,
        minimum_reviews_count: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        require_comments_resolved: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_pull_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["SecureSourceManagerBranchRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param branch_rule_id: The ID for the BranchRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#branch_rule_id SecureSourceManagerBranchRule#branch_rule_id}
        :param include_pattern: The BranchRule matches branches based on the specified regular expression. Use .* to match all branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#include_pattern SecureSourceManagerBranchRule#include_pattern}
        :param location: The location for the Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#location SecureSourceManagerBranchRule#location}
        :param repository_id: The ID for the Repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#repository_id SecureSourceManagerBranchRule#repository_id}
        :param allow_stale_reviews: Determines if allow stale reviews or approvals before merging to the branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#allow_stale_reviews SecureSourceManagerBranchRule#allow_stale_reviews}
        :param disabled: Determines if the branch rule is disabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#disabled SecureSourceManagerBranchRule#disabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#id SecureSourceManagerBranchRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimum_approvals_count: The minimum number of approvals required for the branch rule to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#minimum_approvals_count SecureSourceManagerBranchRule#minimum_approvals_count}
        :param minimum_reviews_count: The minimum number of reviews required for the branch rule to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#minimum_reviews_count SecureSourceManagerBranchRule#minimum_reviews_count}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#project SecureSourceManagerBranchRule#project}.
        :param require_comments_resolved: Determines if require comments resolved before merging to the branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#require_comments_resolved SecureSourceManagerBranchRule#require_comments_resolved}
        :param require_linear_history: Determines if require linear history before merging to the branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#require_linear_history SecureSourceManagerBranchRule#require_linear_history}
        :param require_pull_request: Determines if the branch rule requires a pull request or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#require_pull_request SecureSourceManagerBranchRule#require_pull_request}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#timeouts SecureSourceManagerBranchRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = SecureSourceManagerBranchRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46d0215399d0914e8eca1b4c0b9b29f5f7f45cc38eacccf160371a07b40fcc3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument branch_rule_id", value=branch_rule_id, expected_type=type_hints["branch_rule_id"])
            check_type(argname="argument include_pattern", value=include_pattern, expected_type=type_hints["include_pattern"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument repository_id", value=repository_id, expected_type=type_hints["repository_id"])
            check_type(argname="argument allow_stale_reviews", value=allow_stale_reviews, expected_type=type_hints["allow_stale_reviews"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument minimum_approvals_count", value=minimum_approvals_count, expected_type=type_hints["minimum_approvals_count"])
            check_type(argname="argument minimum_reviews_count", value=minimum_reviews_count, expected_type=type_hints["minimum_reviews_count"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument require_comments_resolved", value=require_comments_resolved, expected_type=type_hints["require_comments_resolved"])
            check_type(argname="argument require_linear_history", value=require_linear_history, expected_type=type_hints["require_linear_history"])
            check_type(argname="argument require_pull_request", value=require_pull_request, expected_type=type_hints["require_pull_request"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch_rule_id": branch_rule_id,
            "include_pattern": include_pattern,
            "location": location,
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
        if allow_stale_reviews is not None:
            self._values["allow_stale_reviews"] = allow_stale_reviews
        if disabled is not None:
            self._values["disabled"] = disabled
        if id is not None:
            self._values["id"] = id
        if minimum_approvals_count is not None:
            self._values["minimum_approvals_count"] = minimum_approvals_count
        if minimum_reviews_count is not None:
            self._values["minimum_reviews_count"] = minimum_reviews_count
        if project is not None:
            self._values["project"] = project
        if require_comments_resolved is not None:
            self._values["require_comments_resolved"] = require_comments_resolved
        if require_linear_history is not None:
            self._values["require_linear_history"] = require_linear_history
        if require_pull_request is not None:
            self._values["require_pull_request"] = require_pull_request
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
    def branch_rule_id(self) -> builtins.str:
        '''The ID for the BranchRule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#branch_rule_id SecureSourceManagerBranchRule#branch_rule_id}
        '''
        result = self._values.get("branch_rule_id")
        assert result is not None, "Required property 'branch_rule_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_pattern(self) -> builtins.str:
        '''The BranchRule matches branches based on the specified regular expression. Use .* to match all branches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#include_pattern SecureSourceManagerBranchRule#include_pattern}
        '''
        result = self._values.get("include_pattern")
        assert result is not None, "Required property 'include_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the Repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#location SecureSourceManagerBranchRule#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_id(self) -> builtins.str:
        '''The ID for the Repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#repository_id SecureSourceManagerBranchRule#repository_id}
        '''
        result = self._values.get("repository_id")
        assert result is not None, "Required property 'repository_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_stale_reviews(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if allow stale reviews or approvals before merging to the branch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#allow_stale_reviews SecureSourceManagerBranchRule#allow_stale_reviews}
        '''
        result = self._values.get("allow_stale_reviews")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if the branch rule is disabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#disabled SecureSourceManagerBranchRule#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#id SecureSourceManagerBranchRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_approvals_count(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of approvals required for the branch rule to be matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#minimum_approvals_count SecureSourceManagerBranchRule#minimum_approvals_count}
        '''
        result = self._values.get("minimum_approvals_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_reviews_count(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of reviews required for the branch rule to be matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#minimum_reviews_count SecureSourceManagerBranchRule#minimum_reviews_count}
        '''
        result = self._values.get("minimum_reviews_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#project SecureSourceManagerBranchRule#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_comments_resolved(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if require comments resolved before merging to the branch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#require_comments_resolved SecureSourceManagerBranchRule#require_comments_resolved}
        '''
        result = self._values.get("require_comments_resolved")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_linear_history(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if require linear history before merging to the branch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#require_linear_history SecureSourceManagerBranchRule#require_linear_history}
        '''
        result = self._values.get("require_linear_history")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_pull_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines if the branch rule requires a pull request or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#require_pull_request SecureSourceManagerBranchRule#require_pull_request}
        '''
        result = self._values.get("require_pull_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SecureSourceManagerBranchRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#timeouts SecureSourceManagerBranchRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SecureSourceManagerBranchRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecureSourceManagerBranchRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.secureSourceManagerBranchRule.SecureSourceManagerBranchRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class SecureSourceManagerBranchRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#create SecureSourceManagerBranchRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#delete SecureSourceManagerBranchRule#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#update SecureSourceManagerBranchRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9e8f84a4186566ccc0eb4d1f22376ba5ebd9c32729d3a152b44cbee4640317)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#create SecureSourceManagerBranchRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#delete SecureSourceManagerBranchRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/secure_source_manager_branch_rule#update SecureSourceManagerBranchRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecureSourceManagerBranchRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecureSourceManagerBranchRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.secureSourceManagerBranchRule.SecureSourceManagerBranchRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__829ecfa1813e76242f08950a007941a1ad0d814ca6a4233e2c984981eb3793b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a96b90db6214cbef3c84a90e6695a39db3fbaf6fd2a9a44cf4995ebbbe968e03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2cbe0085c1c47024975bebfb509af73c74a0f29016f69db022c27b749eb34c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b914cadc6fa85b0614f18ed828301a9d0340d85cb1e01944a90de37ac69fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecureSourceManagerBranchRuleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecureSourceManagerBranchRuleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecureSourceManagerBranchRuleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6eb6e7498099cf9d3ad0b5faab3f52a3f39669027c8ee9f45640e7fd361cb22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SecureSourceManagerBranchRule",
    "SecureSourceManagerBranchRuleConfig",
    "SecureSourceManagerBranchRuleTimeouts",
    "SecureSourceManagerBranchRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c63b4c2cde0f02843fcd2bce974ac339cba59631717be2387d1f3ca08c5199cd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    branch_rule_id: builtins.str,
    include_pattern: builtins.str,
    location: builtins.str,
    repository_id: builtins.str,
    allow_stale_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    minimum_approvals_count: typing.Optional[jsii.Number] = None,
    minimum_reviews_count: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    require_comments_resolved: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_pull_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[SecureSourceManagerBranchRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7def9b516d695fdb11ea1c10bd96bc48a896b0cc37037463ad83d25be96d37ac(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d50f2ecebf314aa31a5e64186893135d3ef0086465da5dd656f9fdc71c1d972(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2c74339625ac82b572ae7b9ff13a3545de742b4f32df19cf478f498c2376a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6e3dcf54de8e0f67840ded5c033f63a54c5e0ec3bf4d09c1313d781b8aeb0e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12127451ab8309030d02e03c26e3404a8e94820a09cbb1c37a527a7657b1de6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedd89b4b633c261a92d5871f55c2ac6cba9816671a2b69e199602869678b658(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af9d0f26ac15e160e1c292b870a05d20636727c36681f2fd25f1537de99c2f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875aeae7e289818aa7b5a76860bc1d6ec1cb28a3dabb76422d3ee919fabd0c40(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde7344427a0de8227c557a3c854bae28640f27b037e76b68734227c9a464c1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e7d14d94cd9c82124ac037fff8843435e6e5a00a08193291c3fe55d67f18a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153fdbfabb9622c13b2d928005db818f4571d23f4a83814ae0b3754a039a5b03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cbe7c8ca24a0977544f58dc3e40caa4479a0bd6602e2c9b25385da1a25537d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff55205c65f4eed212ec949f042f5674c87c3c41c441f6ef5bf92b096d4a595(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f17639caeef480790b1778029d9890773b230c8a3d687fb5fca81f3037c5cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46d0215399d0914e8eca1b4c0b9b29f5f7f45cc38eacccf160371a07b40fcc3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    branch_rule_id: builtins.str,
    include_pattern: builtins.str,
    location: builtins.str,
    repository_id: builtins.str,
    allow_stale_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    minimum_approvals_count: typing.Optional[jsii.Number] = None,
    minimum_reviews_count: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    require_comments_resolved: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_linear_history: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_pull_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[SecureSourceManagerBranchRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9e8f84a4186566ccc0eb4d1f22376ba5ebd9c32729d3a152b44cbee4640317(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829ecfa1813e76242f08950a007941a1ad0d814ca6a4233e2c984981eb3793b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96b90db6214cbef3c84a90e6695a39db3fbaf6fd2a9a44cf4995ebbbe968e03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2cbe0085c1c47024975bebfb509af73c74a0f29016f69db022c27b749eb34c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b914cadc6fa85b0614f18ed828301a9d0340d85cb1e01944a90de37ac69fed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6eb6e7498099cf9d3ad0b5faab3f52a3f39669027c8ee9f45640e7fd361cb22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecureSourceManagerBranchRuleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
