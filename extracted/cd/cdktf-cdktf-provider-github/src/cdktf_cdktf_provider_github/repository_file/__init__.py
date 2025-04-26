r'''
# `github_repository_file`

Refer to the Terraform Registry for docs: [`github_repository_file`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file).
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


class RepositoryFile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repositoryFile.RepositoryFile",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file github_repository_file}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        content: builtins.str,
        file: builtins.str,
        repository: builtins.str,
        autocreate_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        autocreate_branch_source_branch: typing.Optional[builtins.str] = None,
        autocreate_branch_source_sha: typing.Optional[builtins.str] = None,
        branch: typing.Optional[builtins.str] = None,
        commit_author: typing.Optional[builtins.str] = None,
        commit_email: typing.Optional[builtins.str] = None,
        commit_message: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        overwrite_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file github_repository_file} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param content: The file's content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#content RepositoryFile#content}
        :param file: The file path to manage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#file RepositoryFile#file}
        :param repository: The repository name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#repository RepositoryFile#repository}
        :param autocreate_branch: Automatically create the branch if it could not be found. Subsequent reads if the branch is deleted will occur from 'autocreate_branch_source_branch' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#autocreate_branch RepositoryFile#autocreate_branch}
        :param autocreate_branch_source_branch: The branch name to start from, if 'autocreate_branch' is set. Defaults to 'main'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#autocreate_branch_source_branch RepositoryFile#autocreate_branch_source_branch}
        :param autocreate_branch_source_sha: The commit hash to start from, if 'autocreate_branch' is set. Defaults to the tip of 'autocreate_branch_source_branch'. If provided, 'autocreate_branch_source_branch' is ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#autocreate_branch_source_sha RepositoryFile#autocreate_branch_source_sha}
        :param branch: The branch name, defaults to the repository's default branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#branch RepositoryFile#branch}
        :param commit_author: The commit author name, defaults to the authenticated user's name. GitHub app users may omit author and email information so GitHub can verify commits as the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#commit_author RepositoryFile#commit_author}
        :param commit_email: The commit author email address, defaults to the authenticated user's email address. GitHub app users may omit author and email information so GitHub can verify commits as the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#commit_email RepositoryFile#commit_email}
        :param commit_message: The commit message when creating, updating or deleting the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#commit_message RepositoryFile#commit_message}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#id RepositoryFile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param overwrite_on_create: Enable overwriting existing files, defaults to "false". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#overwrite_on_create RepositoryFile#overwrite_on_create}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99385a60faa331aa269b8f4af81b3f66338b7e501e5e5c7933dcb7fd4e1572a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RepositoryFileConfig(
            content=content,
            file=file,
            repository=repository,
            autocreate_branch=autocreate_branch,
            autocreate_branch_source_branch=autocreate_branch_source_branch,
            autocreate_branch_source_sha=autocreate_branch_source_sha,
            branch=branch,
            commit_author=commit_author,
            commit_email=commit_email,
            commit_message=commit_message,
            id=id,
            overwrite_on_create=overwrite_on_create,
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
        '''Generates CDKTF code for importing a RepositoryFile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RepositoryFile to import.
        :param import_from_id: The id of the existing RepositoryFile that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RepositoryFile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a93b4c5df0e48685550c2262435ccb3034defb6a29afa9d5ea109a5317c9994)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAutocreateBranch")
    def reset_autocreate_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutocreateBranch", []))

    @jsii.member(jsii_name="resetAutocreateBranchSourceBranch")
    def reset_autocreate_branch_source_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutocreateBranchSourceBranch", []))

    @jsii.member(jsii_name="resetAutocreateBranchSourceSha")
    def reset_autocreate_branch_source_sha(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutocreateBranchSourceSha", []))

    @jsii.member(jsii_name="resetBranch")
    def reset_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranch", []))

    @jsii.member(jsii_name="resetCommitAuthor")
    def reset_commit_author(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitAuthor", []))

    @jsii.member(jsii_name="resetCommitEmail")
    def reset_commit_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitEmail", []))

    @jsii.member(jsii_name="resetCommitMessage")
    def reset_commit_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitMessage", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOverwriteOnCreate")
    def reset_overwrite_on_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverwriteOnCreate", []))

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
    @jsii.member(jsii_name="commitSha")
    def commit_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitSha"))

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ref"))

    @builtins.property
    @jsii.member(jsii_name="sha")
    def sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha"))

    @builtins.property
    @jsii.member(jsii_name="autocreateBranchInput")
    def autocreate_branch_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autocreateBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="autocreateBranchSourceBranchInput")
    def autocreate_branch_source_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autocreateBranchSourceBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="autocreateBranchSourceShaInput")
    def autocreate_branch_source_sha_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autocreateBranchSourceShaInput"))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="commitAuthorInput")
    def commit_author_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitAuthorInput"))

    @builtins.property
    @jsii.member(jsii_name="commitEmailInput")
    def commit_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="commitMessageInput")
    def commit_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="overwriteOnCreateInput")
    def overwrite_on_create_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "overwriteOnCreateInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="autocreateBranch")
    def autocreate_branch(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autocreateBranch"))

    @autocreate_branch.setter
    def autocreate_branch(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9cfb18510b2b8580209d5d0c79e550a3b369ba59dea58b5073691712e7cce09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autocreateBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autocreateBranchSourceBranch")
    def autocreate_branch_source_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autocreateBranchSourceBranch"))

    @autocreate_branch_source_branch.setter
    def autocreate_branch_source_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ea6c26da374f4f8738ca28ed445ad3aee378dfde6098299e9f067dff2c0f43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autocreateBranchSourceBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autocreateBranchSourceSha")
    def autocreate_branch_source_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autocreateBranchSourceSha"))

    @autocreate_branch_source_sha.setter
    def autocreate_branch_source_sha(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc04b48777262b4e9954721b7abf9928a2c8eae7091860fe23ea200d53d15b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autocreateBranchSourceSha", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74527a685a5b904732722c4a94939bc7a71a5145f76d0fd97b303fb7b9894510)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitAuthor")
    def commit_author(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitAuthor"))

    @commit_author.setter
    def commit_author(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__313b4759e94ebb43fc98947623346d4d162aac918daeb6c1ca0ddd9ff4ab803b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitAuthor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitEmail")
    def commit_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitEmail"))

    @commit_email.setter
    def commit_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfafbb54593bfc6c250f6b218665e2ed3bfb00979d56fc5bd00b0064922598ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitEmail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="commitMessage")
    def commit_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitMessage"))

    @commit_message.setter
    def commit_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a05e709e42da7c2fffcef55265684472932b03465872bf543c73862798fd55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9947b211b2a9828f9681ce03ba6c200be9360e0d7f098c300eca191bdbd6fbfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "file"))

    @file.setter
    def file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34d3db9984ea3ae96f8f43023880e87ec932539840b5b734836797f03921e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "file", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a970f8152ac2fef77bb51012d433bc3f1c67fa89255b58227f081311bdd6ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overwriteOnCreate")
    def overwrite_on_create(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "overwriteOnCreate"))

    @overwrite_on_create.setter
    def overwrite_on_create(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0c5bb8940d14de6fd8728f1056c1531095cdd91babefc3ac2f5ca5034b7aa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overwriteOnCreate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8341d31ff7e3eb59478d7697857d4ace36735e8a7e2d6b167f005a6a8cefa8b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repositoryFile.RepositoryFileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "content": "content",
        "file": "file",
        "repository": "repository",
        "autocreate_branch": "autocreateBranch",
        "autocreate_branch_source_branch": "autocreateBranchSourceBranch",
        "autocreate_branch_source_sha": "autocreateBranchSourceSha",
        "branch": "branch",
        "commit_author": "commitAuthor",
        "commit_email": "commitEmail",
        "commit_message": "commitMessage",
        "id": "id",
        "overwrite_on_create": "overwriteOnCreate",
    },
)
class RepositoryFileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        content: builtins.str,
        file: builtins.str,
        repository: builtins.str,
        autocreate_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        autocreate_branch_source_branch: typing.Optional[builtins.str] = None,
        autocreate_branch_source_sha: typing.Optional[builtins.str] = None,
        branch: typing.Optional[builtins.str] = None,
        commit_author: typing.Optional[builtins.str] = None,
        commit_email: typing.Optional[builtins.str] = None,
        commit_message: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        overwrite_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param content: The file's content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#content RepositoryFile#content}
        :param file: The file path to manage. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#file RepositoryFile#file}
        :param repository: The repository name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#repository RepositoryFile#repository}
        :param autocreate_branch: Automatically create the branch if it could not be found. Subsequent reads if the branch is deleted will occur from 'autocreate_branch_source_branch' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#autocreate_branch RepositoryFile#autocreate_branch}
        :param autocreate_branch_source_branch: The branch name to start from, if 'autocreate_branch' is set. Defaults to 'main'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#autocreate_branch_source_branch RepositoryFile#autocreate_branch_source_branch}
        :param autocreate_branch_source_sha: The commit hash to start from, if 'autocreate_branch' is set. Defaults to the tip of 'autocreate_branch_source_branch'. If provided, 'autocreate_branch_source_branch' is ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#autocreate_branch_source_sha RepositoryFile#autocreate_branch_source_sha}
        :param branch: The branch name, defaults to the repository's default branch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#branch RepositoryFile#branch}
        :param commit_author: The commit author name, defaults to the authenticated user's name. GitHub app users may omit author and email information so GitHub can verify commits as the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#commit_author RepositoryFile#commit_author}
        :param commit_email: The commit author email address, defaults to the authenticated user's email address. GitHub app users may omit author and email information so GitHub can verify commits as the GitHub App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#commit_email RepositoryFile#commit_email}
        :param commit_message: The commit message when creating, updating or deleting the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#commit_message RepositoryFile#commit_message}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#id RepositoryFile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param overwrite_on_create: Enable overwriting existing files, defaults to "false". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#overwrite_on_create RepositoryFile#overwrite_on_create}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48239e51b8b1baf40608ce7b8eef058b88d6a1230835b4ad2e82770cfa5f18d1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument autocreate_branch", value=autocreate_branch, expected_type=type_hints["autocreate_branch"])
            check_type(argname="argument autocreate_branch_source_branch", value=autocreate_branch_source_branch, expected_type=type_hints["autocreate_branch_source_branch"])
            check_type(argname="argument autocreate_branch_source_sha", value=autocreate_branch_source_sha, expected_type=type_hints["autocreate_branch_source_sha"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument commit_author", value=commit_author, expected_type=type_hints["commit_author"])
            check_type(argname="argument commit_email", value=commit_email, expected_type=type_hints["commit_email"])
            check_type(argname="argument commit_message", value=commit_message, expected_type=type_hints["commit_message"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument overwrite_on_create", value=overwrite_on_create, expected_type=type_hints["overwrite_on_create"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "file": file,
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
        if autocreate_branch is not None:
            self._values["autocreate_branch"] = autocreate_branch
        if autocreate_branch_source_branch is not None:
            self._values["autocreate_branch_source_branch"] = autocreate_branch_source_branch
        if autocreate_branch_source_sha is not None:
            self._values["autocreate_branch_source_sha"] = autocreate_branch_source_sha
        if branch is not None:
            self._values["branch"] = branch
        if commit_author is not None:
            self._values["commit_author"] = commit_author
        if commit_email is not None:
            self._values["commit_email"] = commit_email
        if commit_message is not None:
            self._values["commit_message"] = commit_message
        if id is not None:
            self._values["id"] = id
        if overwrite_on_create is not None:
            self._values["overwrite_on_create"] = overwrite_on_create

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
    def content(self) -> builtins.str:
        '''The file's content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#content RepositoryFile#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file(self) -> builtins.str:
        '''The file path to manage.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#file RepositoryFile#file}
        '''
        result = self._values.get("file")
        assert result is not None, "Required property 'file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''The repository name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#repository RepositoryFile#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autocreate_branch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically create the branch if it could not be found.

        Subsequent reads if the branch is deleted will occur from 'autocreate_branch_source_branch'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#autocreate_branch RepositoryFile#autocreate_branch}
        '''
        result = self._values.get("autocreate_branch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def autocreate_branch_source_branch(self) -> typing.Optional[builtins.str]:
        '''The branch name to start from, if 'autocreate_branch' is set. Defaults to 'main'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#autocreate_branch_source_branch RepositoryFile#autocreate_branch_source_branch}
        '''
        result = self._values.get("autocreate_branch_source_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def autocreate_branch_source_sha(self) -> typing.Optional[builtins.str]:
        '''The commit hash to start from, if 'autocreate_branch' is set.

        Defaults to the tip of 'autocreate_branch_source_branch'. If provided, 'autocreate_branch_source_branch' is ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#autocreate_branch_source_sha RepositoryFile#autocreate_branch_source_sha}
        '''
        result = self._values.get("autocreate_branch_source_sha")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''The branch name, defaults to the repository's default branch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#branch RepositoryFile#branch}
        '''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_author(self) -> typing.Optional[builtins.str]:
        '''The commit author name, defaults to the authenticated user's name.

        GitHub app users may omit author and email information so GitHub can verify commits as the GitHub App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#commit_author RepositoryFile#commit_author}
        '''
        result = self._values.get("commit_author")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_email(self) -> typing.Optional[builtins.str]:
        '''The commit author email address, defaults to the authenticated user's email address.

        GitHub app users may omit author and email information so GitHub can verify commits as the GitHub App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#commit_email RepositoryFile#commit_email}
        '''
        result = self._values.get("commit_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def commit_message(self) -> typing.Optional[builtins.str]:
        '''The commit message when creating, updating or deleting the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#commit_message RepositoryFile#commit_message}
        '''
        result = self._values.get("commit_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#id RepositoryFile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overwrite_on_create(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable overwriting existing files, defaults to "false".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository_file#overwrite_on_create RepositoryFile#overwrite_on_create}
        '''
        result = self._values.get("overwrite_on_create")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryFileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "RepositoryFile",
    "RepositoryFileConfig",
]

publication.publish()

def _typecheckingstub__99385a60faa331aa269b8f4af81b3f66338b7e501e5e5c7933dcb7fd4e1572a5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    content: builtins.str,
    file: builtins.str,
    repository: builtins.str,
    autocreate_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    autocreate_branch_source_branch: typing.Optional[builtins.str] = None,
    autocreate_branch_source_sha: typing.Optional[builtins.str] = None,
    branch: typing.Optional[builtins.str] = None,
    commit_author: typing.Optional[builtins.str] = None,
    commit_email: typing.Optional[builtins.str] = None,
    commit_message: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    overwrite_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__0a93b4c5df0e48685550c2262435ccb3034defb6a29afa9d5ea109a5317c9994(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9cfb18510b2b8580209d5d0c79e550a3b369ba59dea58b5073691712e7cce09(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ea6c26da374f4f8738ca28ed445ad3aee378dfde6098299e9f067dff2c0f43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc04b48777262b4e9954721b7abf9928a2c8eae7091860fe23ea200d53d15b41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74527a685a5b904732722c4a94939bc7a71a5145f76d0fd97b303fb7b9894510(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313b4759e94ebb43fc98947623346d4d162aac918daeb6c1ca0ddd9ff4ab803b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfafbb54593bfc6c250f6b218665e2ed3bfb00979d56fc5bd00b0064922598ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a05e709e42da7c2fffcef55265684472932b03465872bf543c73862798fd55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9947b211b2a9828f9681ce03ba6c200be9360e0d7f098c300eca191bdbd6fbfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34d3db9984ea3ae96f8f43023880e87ec932539840b5b734836797f03921e77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a970f8152ac2fef77bb51012d433bc3f1c67fa89255b58227f081311bdd6ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0c5bb8940d14de6fd8728f1056c1531095cdd91babefc3ac2f5ca5034b7aa2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8341d31ff7e3eb59478d7697857d4ace36735e8a7e2d6b167f005a6a8cefa8b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48239e51b8b1baf40608ce7b8eef058b88d6a1230835b4ad2e82770cfa5f18d1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    content: builtins.str,
    file: builtins.str,
    repository: builtins.str,
    autocreate_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    autocreate_branch_source_branch: typing.Optional[builtins.str] = None,
    autocreate_branch_source_sha: typing.Optional[builtins.str] = None,
    branch: typing.Optional[builtins.str] = None,
    commit_author: typing.Optional[builtins.str] = None,
    commit_email: typing.Optional[builtins.str] = None,
    commit_message: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    overwrite_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
