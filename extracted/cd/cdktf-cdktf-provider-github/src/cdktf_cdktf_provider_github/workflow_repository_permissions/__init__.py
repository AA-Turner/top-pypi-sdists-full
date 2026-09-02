r'''
# `github_workflow_repository_permissions`

Refer to the Terraform Registry for docs: [`github_workflow_repository_permissions`](https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions).
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


class WorkflowRepositoryPermissions(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.workflowRepositoryPermissions.WorkflowRepositoryPermissions",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions github_workflow_repository_permissions}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        repository: builtins.str,
        can_approve_pull_request_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_workflow_permissions: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions github_workflow_repository_permissions} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param repository: The GitHub repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#repository WorkflowRepositoryPermissions#repository}
        :param can_approve_pull_request_reviews: Whether GitHub Actions can approve pull requests. Enabling this can be a security risk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#can_approve_pull_request_reviews WorkflowRepositoryPermissions#can_approve_pull_request_reviews}
        :param default_workflow_permissions: The default workflow permissions granted to the GITHUB_TOKEN when running workflows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#default_workflow_permissions WorkflowRepositoryPermissions#default_workflow_permissions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#id WorkflowRepositoryPermissions#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15eb48447134b0a9d5d9450dd7203332f690dcebef5af5b2dceae833204e278b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WorkflowRepositoryPermissionsConfig(
            repository=repository,
            can_approve_pull_request_reviews=can_approve_pull_request_reviews,
            default_workflow_permissions=default_workflow_permissions,
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
        '''Generates CDKTF code for importing a WorkflowRepositoryPermissions resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WorkflowRepositoryPermissions to import.
        :param import_from_id: The id of the existing WorkflowRepositoryPermissions that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WorkflowRepositoryPermissions to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f3fc2bcdd8ad6c097105bcd2de79c7fbbfb53a453bd16302d3f959172a454c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCanApprovePullRequestReviews")
    def reset_can_approve_pull_request_reviews(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanApprovePullRequestReviews", []))

    @jsii.member(jsii_name="resetDefaultWorkflowPermissions")
    def reset_default_workflow_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultWorkflowPermissions", []))

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
    @jsii.member(jsii_name="canApprovePullRequestReviewsInput")
    def can_approve_pull_request_reviews_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "canApprovePullRequestReviewsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultWorkflowPermissionsInput")
    def default_workflow_permissions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultWorkflowPermissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="canApprovePullRequestReviews")
    def can_approve_pull_request_reviews(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "canApprovePullRequestReviews"))

    @can_approve_pull_request_reviews.setter
    def can_approve_pull_request_reviews(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34b38cb579dbb329e3e10f134ecd6b86cfdbe212fa46359924ffd226307cc34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canApprovePullRequestReviews", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultWorkflowPermissions")
    def default_workflow_permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultWorkflowPermissions"))

    @default_workflow_permissions.setter
    def default_workflow_permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f52d20c56074592e0239b3384e7c615021865028243ca3cedbba3fd05b384a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultWorkflowPermissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb3aa9a5d1ad21e78b2415729b983302053e55b7bde725b9e964d78afd09f93a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e79fade8ca37e2df5e9d5101c3351ad431193ffa13b274c0eec81c97b98ae069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.workflowRepositoryPermissions.WorkflowRepositoryPermissionsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "repository": "repository",
        "can_approve_pull_request_reviews": "canApprovePullRequestReviews",
        "default_workflow_permissions": "defaultWorkflowPermissions",
        "id": "id",
    },
)
class WorkflowRepositoryPermissionsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        repository: builtins.str,
        can_approve_pull_request_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_workflow_permissions: typing.Optional[builtins.str] = None,
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
        :param repository: The GitHub repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#repository WorkflowRepositoryPermissions#repository}
        :param can_approve_pull_request_reviews: Whether GitHub Actions can approve pull requests. Enabling this can be a security risk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#can_approve_pull_request_reviews WorkflowRepositoryPermissions#can_approve_pull_request_reviews}
        :param default_workflow_permissions: The default workflow permissions granted to the GITHUB_TOKEN when running workflows. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#default_workflow_permissions WorkflowRepositoryPermissions#default_workflow_permissions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#id WorkflowRepositoryPermissions#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b398585087dea24b2613d4ed1b09c126ae7d280d8283cc9b0fec6e944b500543)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument can_approve_pull_request_reviews", value=can_approve_pull_request_reviews, expected_type=type_hints["can_approve_pull_request_reviews"])
            check_type(argname="argument default_workflow_permissions", value=default_workflow_permissions, expected_type=type_hints["default_workflow_permissions"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if can_approve_pull_request_reviews is not None:
            self._values["can_approve_pull_request_reviews"] = can_approve_pull_request_reviews
        if default_workflow_permissions is not None:
            self._values["default_workflow_permissions"] = default_workflow_permissions
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
    def repository(self) -> builtins.str:
        '''The GitHub repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#repository WorkflowRepositoryPermissions#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def can_approve_pull_request_reviews(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether GitHub Actions can approve pull requests. Enabling this can be a security risk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#can_approve_pull_request_reviews WorkflowRepositoryPermissions#can_approve_pull_request_reviews}
        '''
        result = self._values.get("can_approve_pull_request_reviews")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_workflow_permissions(self) -> typing.Optional[builtins.str]:
        '''The default workflow permissions granted to the GITHUB_TOKEN when running workflows.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#default_workflow_permissions WorkflowRepositoryPermissions#default_workflow_permissions}
        '''
        result = self._values.get("default_workflow_permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.9.0/docs/resources/workflow_repository_permissions#id WorkflowRepositoryPermissions#id}.

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
        return "WorkflowRepositoryPermissionsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "WorkflowRepositoryPermissions",
    "WorkflowRepositoryPermissionsConfig",
]

publication.publish()

def _typecheckingstub__15eb48447134b0a9d5d9450dd7203332f690dcebef5af5b2dceae833204e278b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    repository: builtins.str,
    can_approve_pull_request_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_workflow_permissions: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__f4f3fc2bcdd8ad6c097105bcd2de79c7fbbfb53a453bd16302d3f959172a454c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34b38cb579dbb329e3e10f134ecd6b86cfdbe212fa46359924ffd226307cc34(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f52d20c56074592e0239b3384e7c615021865028243ca3cedbba3fd05b384a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3aa9a5d1ad21e78b2415729b983302053e55b7bde725b9e964d78afd09f93a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79fade8ca37e2df5e9d5101c3351ad431193ffa13b274c0eec81c97b98ae069(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b398585087dea24b2613d4ed1b09c126ae7d280d8283cc9b0fec6e944b500543(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    repository: builtins.str,
    can_approve_pull_request_reviews: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_workflow_permissions: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
