r'''
# `github_repository_environment`

Refer to the Terraform Registry for docs: [`github_repository_environment`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment).
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


class RepositoryEnvironment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryEnvironment.RepositoryEnvironment",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment github_repository_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        environment: builtins.str,
        repository: builtins.str,
        can_admins_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deployment_branch_policy: typing.Optional[typing.Union["RepositoryEnvironmentDeploymentBranchPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        prevent_self_review: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reviewers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RepositoryEnvironmentReviewers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        wait_timer: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment github_repository_environment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param environment: The name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#environment RepositoryEnvironment#environment}
        :param repository: The repository of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#repository RepositoryEnvironment#repository}
        :param can_admins_bypass: Can Admins bypass deployment protections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#can_admins_bypass RepositoryEnvironment#can_admins_bypass}
        :param deployment_branch_policy: deployment_branch_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#deployment_branch_policy RepositoryEnvironment#deployment_branch_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#id RepositoryEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param prevent_self_review: Prevent users from approving workflows runs that they triggered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#prevent_self_review RepositoryEnvironment#prevent_self_review}
        :param reviewers: reviewers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#reviewers RepositoryEnvironment#reviewers}
        :param wait_timer: Amount of time to delay a job after the job is initially triggered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#wait_timer RepositoryEnvironment#wait_timer}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5737aace49e9141dc6a0f45db527f5edbb39e1b6ff1058faadd71fff846fac4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RepositoryEnvironmentConfig(
            environment=environment,
            repository=repository,
            can_admins_bypass=can_admins_bypass,
            deployment_branch_policy=deployment_branch_policy,
            id=id,
            prevent_self_review=prevent_self_review,
            reviewers=reviewers,
            wait_timer=wait_timer,
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
        '''Generates CDKTF code for importing a RepositoryEnvironment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RepositoryEnvironment to import.
        :param import_from_id: The id of the existing RepositoryEnvironment that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RepositoryEnvironment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1768d14cd2b4c65a34eebd63ffd59a876c7afd67055e38a08528d132a0b4bf82)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDeploymentBranchPolicy")
    def put_deployment_branch_policy(
        self,
        *,
        custom_branch_policies: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        protected_branches: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param custom_branch_policies: Whether only branches that match the specified name patterns can deploy to this environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#custom_branch_policies RepositoryEnvironment#custom_branch_policies}
        :param protected_branches: Whether only branches with branch protection rules can deploy to this environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#protected_branches RepositoryEnvironment#protected_branches}
        '''
        value = RepositoryEnvironmentDeploymentBranchPolicy(
            custom_branch_policies=custom_branch_policies,
            protected_branches=protected_branches,
        )

        return typing.cast(None, jsii.invoke(self, "putDeploymentBranchPolicy", [value]))

    @jsii.member(jsii_name="putReviewers")
    def put_reviewers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RepositoryEnvironmentReviewers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975e0c4a1076f4e4b262094b67bd30bd9334538c33d67acbb4728541707b6c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReviewers", [value]))

    @jsii.member(jsii_name="resetCanAdminsBypass")
    def reset_can_admins_bypass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanAdminsBypass", []))

    @jsii.member(jsii_name="resetDeploymentBranchPolicy")
    def reset_deployment_branch_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentBranchPolicy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPreventSelfReview")
    def reset_prevent_self_review(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventSelfReview", []))

    @jsii.member(jsii_name="resetReviewers")
    def reset_reviewers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReviewers", []))

    @jsii.member(jsii_name="resetWaitTimer")
    def reset_wait_timer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitTimer", []))

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
    @jsii.member(jsii_name="deploymentBranchPolicy")
    def deployment_branch_policy(
        self,
    ) -> "RepositoryEnvironmentDeploymentBranchPolicyOutputReference":
        return typing.cast("RepositoryEnvironmentDeploymentBranchPolicyOutputReference", jsii.get(self, "deploymentBranchPolicy"))

    @builtins.property
    @jsii.member(jsii_name="reviewers")
    def reviewers(self) -> "RepositoryEnvironmentReviewersList":
        return typing.cast("RepositoryEnvironmentReviewersList", jsii.get(self, "reviewers"))

    @builtins.property
    @jsii.member(jsii_name="canAdminsBypassInput")
    def can_admins_bypass_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "canAdminsBypassInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentBranchPolicyInput")
    def deployment_branch_policy_input(
        self,
    ) -> typing.Optional["RepositoryEnvironmentDeploymentBranchPolicy"]:
        return typing.cast(typing.Optional["RepositoryEnvironmentDeploymentBranchPolicy"], jsii.get(self, "deploymentBranchPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="preventSelfReviewInput")
    def prevent_self_review_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventSelfReviewInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="reviewersInput")
    def reviewers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryEnvironmentReviewers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryEnvironmentReviewers"]]], jsii.get(self, "reviewersInput"))

    @builtins.property
    @jsii.member(jsii_name="waitTimerInput")
    def wait_timer_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "waitTimerInput"))

    @builtins.property
    @jsii.member(jsii_name="canAdminsBypass")
    def can_admins_bypass(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "canAdminsBypass"))

    @can_admins_bypass.setter
    def can_admins_bypass(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3f535c69bd3c921518c905026c1468e2beb3c2d9b9b8c8394edf65d3f0c7aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canAdminsBypass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73baead669c7aa485bb77f3637a8768ab798ce68730ea45444cacbf1024d74b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea7d4ea870ec6c3732aab6aa9ef20635789d53052d441bb0b2a20faec92ee3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preventSelfReview")
    def prevent_self_review(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preventSelfReview"))

    @prevent_self_review.setter
    def prevent_self_review(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796710dc47275c26152c8e15cbf26eec1885328681591a78fef2517a5afad4cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventSelfReview", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__927f54dc35fc0e7b9c05efd73485a0c7089b02be18bf5505a83c41ed25df5345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitTimer")
    def wait_timer(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "waitTimer"))

    @wait_timer.setter
    def wait_timer(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c57a23fd0823bfee842c8eb9cbbd1759217a56900e2acab9772d956ecae4a3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitTimer", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryEnvironment.RepositoryEnvironmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "environment": "environment",
        "repository": "repository",
        "can_admins_bypass": "canAdminsBypass",
        "deployment_branch_policy": "deploymentBranchPolicy",
        "id": "id",
        "prevent_self_review": "preventSelfReview",
        "reviewers": "reviewers",
        "wait_timer": "waitTimer",
    },
)
class RepositoryEnvironmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        environment: builtins.str,
        repository: builtins.str,
        can_admins_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deployment_branch_policy: typing.Optional[typing.Union["RepositoryEnvironmentDeploymentBranchPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        prevent_self_review: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reviewers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RepositoryEnvironmentReviewers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        wait_timer: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param environment: The name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#environment RepositoryEnvironment#environment}
        :param repository: The repository of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#repository RepositoryEnvironment#repository}
        :param can_admins_bypass: Can Admins bypass deployment protections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#can_admins_bypass RepositoryEnvironment#can_admins_bypass}
        :param deployment_branch_policy: deployment_branch_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#deployment_branch_policy RepositoryEnvironment#deployment_branch_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#id RepositoryEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param prevent_self_review: Prevent users from approving workflows runs that they triggered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#prevent_self_review RepositoryEnvironment#prevent_self_review}
        :param reviewers: reviewers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#reviewers RepositoryEnvironment#reviewers}
        :param wait_timer: Amount of time to delay a job after the job is initially triggered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#wait_timer RepositoryEnvironment#wait_timer}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(deployment_branch_policy, dict):
            deployment_branch_policy = RepositoryEnvironmentDeploymentBranchPolicy(**deployment_branch_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfd6e10cbb17598aa3daff2805d9fae779c3c046c67057d0fc4c1dd4559cd61)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument can_admins_bypass", value=can_admins_bypass, expected_type=type_hints["can_admins_bypass"])
            check_type(argname="argument deployment_branch_policy", value=deployment_branch_policy, expected_type=type_hints["deployment_branch_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument prevent_self_review", value=prevent_self_review, expected_type=type_hints["prevent_self_review"])
            check_type(argname="argument reviewers", value=reviewers, expected_type=type_hints["reviewers"])
            check_type(argname="argument wait_timer", value=wait_timer, expected_type=type_hints["wait_timer"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "environment": environment,
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
        if can_admins_bypass is not None:
            self._values["can_admins_bypass"] = can_admins_bypass
        if deployment_branch_policy is not None:
            self._values["deployment_branch_policy"] = deployment_branch_policy
        if id is not None:
            self._values["id"] = id
        if prevent_self_review is not None:
            self._values["prevent_self_review"] = prevent_self_review
        if reviewers is not None:
            self._values["reviewers"] = reviewers
        if wait_timer is not None:
            self._values["wait_timer"] = wait_timer

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
    def environment(self) -> builtins.str:
        '''The name of the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#environment RepositoryEnvironment#environment}
        '''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''The repository of the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#repository RepositoryEnvironment#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def can_admins_bypass(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Can Admins bypass deployment protections.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#can_admins_bypass RepositoryEnvironment#can_admins_bypass}
        '''
        result = self._values.get("can_admins_bypass")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deployment_branch_policy(
        self,
    ) -> typing.Optional["RepositoryEnvironmentDeploymentBranchPolicy"]:
        '''deployment_branch_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#deployment_branch_policy RepositoryEnvironment#deployment_branch_policy}
        '''
        result = self._values.get("deployment_branch_policy")
        return typing.cast(typing.Optional["RepositoryEnvironmentDeploymentBranchPolicy"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#id RepositoryEnvironment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prevent_self_review(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent users from approving workflows runs that they triggered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#prevent_self_review RepositoryEnvironment#prevent_self_review}
        '''
        result = self._values.get("prevent_self_review")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reviewers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryEnvironmentReviewers"]]]:
        '''reviewers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#reviewers RepositoryEnvironment#reviewers}
        '''
        result = self._values.get("reviewers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RepositoryEnvironmentReviewers"]]], result)

    @builtins.property
    def wait_timer(self) -> typing.Optional[jsii.Number]:
        '''Amount of time to delay a job after the job is initially triggered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#wait_timer RepositoryEnvironment#wait_timer}
        '''
        result = self._values.get("wait_timer")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryEnvironment.RepositoryEnvironmentDeploymentBranchPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "custom_branch_policies": "customBranchPolicies",
        "protected_branches": "protectedBranches",
    },
)
class RepositoryEnvironmentDeploymentBranchPolicy:
    def __init__(
        self,
        *,
        custom_branch_policies: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        protected_branches: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param custom_branch_policies: Whether only branches that match the specified name patterns can deploy to this environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#custom_branch_policies RepositoryEnvironment#custom_branch_policies}
        :param protected_branches: Whether only branches with branch protection rules can deploy to this environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#protected_branches RepositoryEnvironment#protected_branches}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6643e3f1d290825d17c549b8f503830d76419aaa5c3f4d1dc1bbf2a099a369)
            check_type(argname="argument custom_branch_policies", value=custom_branch_policies, expected_type=type_hints["custom_branch_policies"])
            check_type(argname="argument protected_branches", value=protected_branches, expected_type=type_hints["protected_branches"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "custom_branch_policies": custom_branch_policies,
            "protected_branches": protected_branches,
        }

    @builtins.property
    def custom_branch_policies(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether only branches that match the specified name patterns can deploy to this environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#custom_branch_policies RepositoryEnvironment#custom_branch_policies}
        '''
        result = self._values.get("custom_branch_policies")
        assert result is not None, "Required property 'custom_branch_policies' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def protected_branches(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether only branches with branch protection rules can deploy to this environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#protected_branches RepositoryEnvironment#protected_branches}
        '''
        result = self._values.get("protected_branches")
        assert result is not None, "Required property 'protected_branches' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryEnvironmentDeploymentBranchPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryEnvironmentDeploymentBranchPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryEnvironment.RepositoryEnvironmentDeploymentBranchPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98dcd772ef7486066c8c9fb7bb0497d6b7951d6df3002424a170ebd0ec781102)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="customBranchPoliciesInput")
    def custom_branch_policies_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customBranchPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="protectedBranchesInput")
    def protected_branches_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "protectedBranchesInput"))

    @builtins.property
    @jsii.member(jsii_name="customBranchPolicies")
    def custom_branch_policies(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "customBranchPolicies"))

    @custom_branch_policies.setter
    def custom_branch_policies(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5734b8b71e8d67dcdb46a1dabd92bf69a3d27484808db2742fdf2a8d1b5df1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customBranchPolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protectedBranches")
    def protected_branches(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "protectedBranches"))

    @protected_branches.setter
    def protected_branches(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a77bf90ccb0255f47a5f8f31fdc065984df96906e440ecc5372c633a5e661da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectedBranches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RepositoryEnvironmentDeploymentBranchPolicy]:
        return typing.cast(typing.Optional[RepositoryEnvironmentDeploymentBranchPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositoryEnvironmentDeploymentBranchPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee690089ba55aef4a1d547a5902f336d9e2d8fa453b19ee76c9f5ec83bff8bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryEnvironment.RepositoryEnvironmentReviewers",
    jsii_struct_bases=[],
    name_mapping={"teams": "teams", "users": "users"},
)
class RepositoryEnvironmentReviewers:
    def __init__(
        self,
        *,
        teams: typing.Optional[typing.Sequence[jsii.Number]] = None,
        users: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param teams: Up to 6 IDs for teams who may review jobs that reference the environment. Reviewers must have at least read access to the repository. Only one of the required reviewers needs to approve the job for it to proceed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#teams RepositoryEnvironment#teams}
        :param users: Up to 6 IDs for users who may review jobs that reference the environment. Reviewers must have at least read access to the repository. Only one of the required reviewers needs to approve the job for it to proceed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#users RepositoryEnvironment#users}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930a9437428ecdc1f28eaa64e4bfec055aa8c8c86de5ca5a91103d7c082a87f2)
            check_type(argname="argument teams", value=teams, expected_type=type_hints["teams"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if teams is not None:
            self._values["teams"] = teams
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def teams(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Up to 6 IDs for teams who may review jobs that reference the environment.

        Reviewers must have at least read access to the repository. Only one of the required reviewers needs to approve the job for it to proceed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#teams RepositoryEnvironment#teams}
        '''
        result = self._values.get("teams")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Up to 6 IDs for users who may review jobs that reference the environment.

        Reviewers must have at least read access to the repository. Only one of the required reviewers needs to approve the job for it to proceed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_environment#users RepositoryEnvironment#users}
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryEnvironmentReviewers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryEnvironmentReviewersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryEnvironment.RepositoryEnvironmentReviewersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f957907ed4ea943042965038b4f650d1bf94c13c2327aff8059f5d7d4c07ff9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RepositoryEnvironmentReviewersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__440907a3c754152dc743005736042b9ed0e3d9004adda75293880d7e4a368a99)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RepositoryEnvironmentReviewersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f878bca09b1acc32e9e82a5aea2ee2adfe60914d0e872c804f049edbf58292)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdb26928444c6829f6a1e0d8a180835630f8aa7252c545029c33d844cf232b34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bd20076153ff2ffe44458de85abb459cc776498b1484d06d03503f8dad6cced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryEnvironmentReviewers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryEnvironmentReviewers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryEnvironmentReviewers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9347d37107b80e8de9401cfd30562ecb76f9f97b5e310a7e2de406de413058c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RepositoryEnvironmentReviewersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryEnvironment.RepositoryEnvironmentReviewersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2d5da60d9e07919c032d60e9dda949c91dec6c7c99466aec246e66a40e5177a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTeams")
    def reset_teams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeams", []))

    @jsii.member(jsii_name="resetUsers")
    def reset_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsers", []))

    @builtins.property
    @jsii.member(jsii_name="teamsInput")
    def teams_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "teamsInput"))

    @builtins.property
    @jsii.member(jsii_name="usersInput")
    def users_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "usersInput"))

    @builtins.property
    @jsii.member(jsii_name="teams")
    def teams(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "teams"))

    @teams.setter
    def teams(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091a3cf1d7332a65d0c05b51d262d9a46ec896e1071d5a5359f6240c0b4573ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teams", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d7d9cf21d71bb0214a63a4fdc5c6ffd041414def8770d5ab3a0e060a93a55c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryEnvironmentReviewers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryEnvironmentReviewers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryEnvironmentReviewers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ca2132a1ba25aee9db14d24563daa83edaee6c2ab9c6b5facff08b5d440a26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RepositoryEnvironment",
    "RepositoryEnvironmentConfig",
    "RepositoryEnvironmentDeploymentBranchPolicy",
    "RepositoryEnvironmentDeploymentBranchPolicyOutputReference",
    "RepositoryEnvironmentReviewers",
    "RepositoryEnvironmentReviewersList",
    "RepositoryEnvironmentReviewersOutputReference",
]

publication.publish()

def _typecheckingstub__5737aace49e9141dc6a0f45db527f5edbb39e1b6ff1058faadd71fff846fac4b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    environment: builtins.str,
    repository: builtins.str,
    can_admins_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deployment_branch_policy: typing.Optional[typing.Union[RepositoryEnvironmentDeploymentBranchPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    prevent_self_review: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reviewers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RepositoryEnvironmentReviewers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    wait_timer: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__1768d14cd2b4c65a34eebd63ffd59a876c7afd67055e38a08528d132a0b4bf82(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975e0c4a1076f4e4b262094b67bd30bd9334538c33d67acbb4728541707b6c91(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RepositoryEnvironmentReviewers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3f535c69bd3c921518c905026c1468e2beb3c2d9b9b8c8394edf65d3f0c7aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73baead669c7aa485bb77f3637a8768ab798ce68730ea45444cacbf1024d74b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea7d4ea870ec6c3732aab6aa9ef20635789d53052d441bb0b2a20faec92ee3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796710dc47275c26152c8e15cbf26eec1885328681591a78fef2517a5afad4cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927f54dc35fc0e7b9c05efd73485a0c7089b02be18bf5505a83c41ed25df5345(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c57a23fd0823bfee842c8eb9cbbd1759217a56900e2acab9772d956ecae4a3e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfd6e10cbb17598aa3daff2805d9fae779c3c046c67057d0fc4c1dd4559cd61(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    environment: builtins.str,
    repository: builtins.str,
    can_admins_bypass: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deployment_branch_policy: typing.Optional[typing.Union[RepositoryEnvironmentDeploymentBranchPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    prevent_self_review: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reviewers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RepositoryEnvironmentReviewers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    wait_timer: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6643e3f1d290825d17c549b8f503830d76419aaa5c3f4d1dc1bbf2a099a369(
    *,
    custom_branch_policies: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    protected_branches: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98dcd772ef7486066c8c9fb7bb0497d6b7951d6df3002424a170ebd0ec781102(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5734b8b71e8d67dcdb46a1dabd92bf69a3d27484808db2742fdf2a8d1b5df1c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a77bf90ccb0255f47a5f8f31fdc065984df96906e440ecc5372c633a5e661da(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee690089ba55aef4a1d547a5902f336d9e2d8fa453b19ee76c9f5ec83bff8bb5(
    value: typing.Optional[RepositoryEnvironmentDeploymentBranchPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930a9437428ecdc1f28eaa64e4bfec055aa8c8c86de5ca5a91103d7c082a87f2(
    *,
    teams: typing.Optional[typing.Sequence[jsii.Number]] = None,
    users: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f957907ed4ea943042965038b4f650d1bf94c13c2327aff8059f5d7d4c07ff9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440907a3c754152dc743005736042b9ed0e3d9004adda75293880d7e4a368a99(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f878bca09b1acc32e9e82a5aea2ee2adfe60914d0e872c804f049edbf58292(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb26928444c6829f6a1e0d8a180835630f8aa7252c545029c33d844cf232b34(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd20076153ff2ffe44458de85abb459cc776498b1484d06d03503f8dad6cced(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9347d37107b80e8de9401cfd30562ecb76f9f97b5e310a7e2de406de413058c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RepositoryEnvironmentReviewers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d5da60d9e07919c032d60e9dda949c91dec6c7c99466aec246e66a40e5177a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091a3cf1d7332a65d0c05b51d262d9a46ec896e1071d5a5359f6240c0b4573ca(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d7d9cf21d71bb0214a63a4fdc5c6ffd041414def8770d5ab3a0e060a93a55c(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ca2132a1ba25aee9db14d24563daa83edaee6c2ab9c6b5facff08b5d440a26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RepositoryEnvironmentReviewers]],
) -> None:
    """Type checking stubs"""
    pass
