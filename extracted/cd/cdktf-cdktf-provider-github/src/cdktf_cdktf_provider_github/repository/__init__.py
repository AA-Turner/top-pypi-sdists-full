r'''
# `github_repository`

Refer to the Terraform Registry for docs: [`github_repository`](https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository).
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


class Repository(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repository.Repository",
):
    '''Represents a {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository github_repository}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        allow_auto_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_merge_commit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_rebase_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_squash_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_update_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        archived: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        archive_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_init: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_branch: typing.Optional[builtins.str] = None,
        delete_branch_on_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        gitignore_template: typing.Optional[builtins.str] = None,
        has_discussions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        has_downloads: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        has_issues: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        has_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        has_wiki: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        homepage_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_vulnerability_alerts_during_read: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_template: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        license_template: typing.Optional[builtins.str] = None,
        merge_commit_message: typing.Optional[builtins.str] = None,
        merge_commit_title: typing.Optional[builtins.str] = None,
        pages: typing.Optional[typing.Union["RepositoryPages", typing.Dict[builtins.str, typing.Any]]] = None,
        private: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_and_analysis: typing.Optional[typing.Union["RepositorySecurityAndAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
        squash_merge_commit_message: typing.Optional[builtins.str] = None,
        squash_merge_commit_title: typing.Optional[builtins.str] = None,
        template: typing.Optional[typing.Union["RepositoryTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        visibility: typing.Optional[builtins.str] = None,
        vulnerability_alerts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        web_commit_signoff_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository github_repository} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#name Repository#name}
        :param allow_auto_merge: Set to 'true' to allow auto-merging pull requests on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_auto_merge Repository#allow_auto_merge}
        :param allow_merge_commit: Set to 'false' to disable merge commits on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_merge_commit Repository#allow_merge_commit}
        :param allow_rebase_merge: Set to 'false' to disable rebase merges on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_rebase_merge Repository#allow_rebase_merge}
        :param allow_squash_merge: Set to 'false' to disable squash merges on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_squash_merge Repository#allow_squash_merge}
        :param allow_update_branch: Set to 'true' to always suggest updating pull request branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_update_branch Repository#allow_update_branch}
        :param archived: Specifies if the repository should be archived. Defaults to 'false'. NOTE Currently, the API does not support unarchiving. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#archived Repository#archived}
        :param archive_on_destroy: Set to 'true' to archive the repository instead of deleting on destroy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#archive_on_destroy Repository#archive_on_destroy}
        :param auto_init: Set to 'true' to produce an initial commit in the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#auto_init Repository#auto_init}
        :param default_branch: Can only be set after initial repository creation, and only if the target branch exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#default_branch Repository#default_branch}
        :param delete_branch_on_merge: Automatically delete head branch after a pull request is merged. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#delete_branch_on_merge Repository#delete_branch_on_merge}
        :param description: A description of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#description Repository#description}
        :param gitignore_template: Use the name of the template without the extension. For example, 'Haskell'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#gitignore_template Repository#gitignore_template}
        :param has_discussions: Set to 'true' to enable GitHub Discussions on the repository. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_discussions Repository#has_discussions}
        :param has_downloads: Set to 'true' to enable the (deprecated) downloads features on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_downloads Repository#has_downloads}
        :param has_issues: Set to 'true' to enable the GitHub Issues features on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_issues Repository#has_issues}
        :param has_projects: Set to 'true' to enable the GitHub Projects features on the repository. Per the GitHub documentation when in an organization that has disabled repository projects it will default to 'false' and will otherwise default to 'true'. If you specify 'true' when it has been disabled it will return an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_projects Repository#has_projects}
        :param has_wiki: Set to 'true' to enable the GitHub Wiki features on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_wiki Repository#has_wiki}
        :param homepage_url: URL of a page describing the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#homepage_url Repository#homepage_url}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#id Repository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_vulnerability_alerts_during_read: Set to true to not call the vulnerability alerts endpoint so the resource can also be used without admin permissions during read. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#ignore_vulnerability_alerts_during_read Repository#ignore_vulnerability_alerts_during_read}
        :param is_template: Set to 'true' to tell GitHub that this is a template repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#is_template Repository#is_template}
        :param license_template: Use the name of the template without the extension. For example, 'mit' or 'mpl-2.0'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#license_template Repository#license_template}
        :param merge_commit_message: Can be 'PR_BODY', 'PR_TITLE', or 'BLANK' for a default merge commit message. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#merge_commit_message Repository#merge_commit_message}
        :param merge_commit_title: Can be 'PR_TITLE' or 'MERGE_MESSAGE' for a default merge commit title. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#merge_commit_title Repository#merge_commit_title}
        :param pages: pages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#pages Repository#pages}
        :param private: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#private Repository#private}.
        :param security_and_analysis: security_and_analysis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#security_and_analysis Repository#security_and_analysis}
        :param squash_merge_commit_message: Can be 'PR_BODY', 'COMMIT_MESSAGES', or 'BLANK' for a default squash merge commit message. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#squash_merge_commit_message Repository#squash_merge_commit_message}
        :param squash_merge_commit_title: Can be 'PR_TITLE' or 'COMMIT_OR_PR_TITLE' for a default squash merge commit title. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#squash_merge_commit_title Repository#squash_merge_commit_title}
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#template Repository#template}
        :param topics: The list of topics of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#topics Repository#topics}
        :param visibility: Can be 'public' or 'private'. If your organization is associated with an enterprise account using GitHub Enterprise Cloud or GitHub Enterprise Server 2.20+, visibility can also be 'internal'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#visibility Repository#visibility}
        :param vulnerability_alerts: Set to 'true' to enable security alerts for vulnerable dependencies. Enabling requires alerts to be enabled on the owner level. (Note for importing: GitHub enables the alerts on public repos but disables them on private repos by default). Note that vulnerability alerts have not been successfully tested on any GitHub Enterprise instance and may be unavailable in those settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#vulnerability_alerts Repository#vulnerability_alerts}
        :param web_commit_signoff_required: Require contributors to sign off on web-based commits. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#web_commit_signoff_required Repository#web_commit_signoff_required}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb2ad3de9416f1cba9636a8de2ff57cade0941e6e3933abbb2c231a3d8dcf74f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RepositoryConfig(
            name=name,
            allow_auto_merge=allow_auto_merge,
            allow_merge_commit=allow_merge_commit,
            allow_rebase_merge=allow_rebase_merge,
            allow_squash_merge=allow_squash_merge,
            allow_update_branch=allow_update_branch,
            archived=archived,
            archive_on_destroy=archive_on_destroy,
            auto_init=auto_init,
            default_branch=default_branch,
            delete_branch_on_merge=delete_branch_on_merge,
            description=description,
            gitignore_template=gitignore_template,
            has_discussions=has_discussions,
            has_downloads=has_downloads,
            has_issues=has_issues,
            has_projects=has_projects,
            has_wiki=has_wiki,
            homepage_url=homepage_url,
            id=id,
            ignore_vulnerability_alerts_during_read=ignore_vulnerability_alerts_during_read,
            is_template=is_template,
            license_template=license_template,
            merge_commit_message=merge_commit_message,
            merge_commit_title=merge_commit_title,
            pages=pages,
            private=private,
            security_and_analysis=security_and_analysis,
            squash_merge_commit_message=squash_merge_commit_message,
            squash_merge_commit_title=squash_merge_commit_title,
            template=template,
            topics=topics,
            visibility=visibility,
            vulnerability_alerts=vulnerability_alerts,
            web_commit_signoff_required=web_commit_signoff_required,
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
        '''Generates CDKTF code for importing a Repository resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Repository to import.
        :param import_from_id: The id of the existing Repository that should be imported. Refer to the {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Repository to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b9384013746d127f245dfc9ec069a828cb2e0ca83b883e8a34dd859548ec8e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPages")
    def put_pages(
        self,
        *,
        build_type: typing.Optional[builtins.str] = None,
        cname: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union["RepositoryPagesSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param build_type: The type the page should be sourced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#build_type Repository#build_type}
        :param cname: The custom domain for the repository. This can only be set after the repository has been created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#cname Repository#cname}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#source Repository#source}
        '''
        value = RepositoryPages(build_type=build_type, cname=cname, source=source)

        return typing.cast(None, jsii.invoke(self, "putPages", [value]))

    @jsii.member(jsii_name="putSecurityAndAnalysis")
    def put_security_and_analysis(
        self,
        *,
        advanced_security: typing.Optional[typing.Union["RepositorySecurityAndAnalysisAdvancedSecurity", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_scanning: typing.Optional[typing.Union["RepositorySecurityAndAnalysisSecretScanning", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_scanning_push_protection: typing.Optional[typing.Union["RepositorySecurityAndAnalysisSecretScanningPushProtection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_security: advanced_security block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#advanced_security Repository#advanced_security}
        :param secret_scanning: secret_scanning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#secret_scanning Repository#secret_scanning}
        :param secret_scanning_push_protection: secret_scanning_push_protection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#secret_scanning_push_protection Repository#secret_scanning_push_protection}
        '''
        value = RepositorySecurityAndAnalysis(
            advanced_security=advanced_security,
            secret_scanning=secret_scanning,
            secret_scanning_push_protection=secret_scanning_push_protection,
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityAndAnalysis", [value]))

    @jsii.member(jsii_name="putTemplate")
    def put_template(
        self,
        *,
        owner: builtins.str,
        repository: builtins.str,
        include_all_branches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param owner: The GitHub organization or user the template repository is owned by. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#owner Repository#owner}
        :param repository: The name of the template repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#repository Repository#repository}
        :param include_all_branches: Whether the new repository should include all the branches from the template repository (defaults to 'false', which includes only the default branch from the template). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#include_all_branches Repository#include_all_branches}
        '''
        value = RepositoryTemplate(
            owner=owner,
            repository=repository,
            include_all_branches=include_all_branches,
        )

        return typing.cast(None, jsii.invoke(self, "putTemplate", [value]))

    @jsii.member(jsii_name="resetAllowAutoMerge")
    def reset_allow_auto_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowAutoMerge", []))

    @jsii.member(jsii_name="resetAllowMergeCommit")
    def reset_allow_merge_commit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowMergeCommit", []))

    @jsii.member(jsii_name="resetAllowRebaseMerge")
    def reset_allow_rebase_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowRebaseMerge", []))

    @jsii.member(jsii_name="resetAllowSquashMerge")
    def reset_allow_squash_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowSquashMerge", []))

    @jsii.member(jsii_name="resetAllowUpdateBranch")
    def reset_allow_update_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowUpdateBranch", []))

    @jsii.member(jsii_name="resetArchived")
    def reset_archived(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchived", []))

    @jsii.member(jsii_name="resetArchiveOnDestroy")
    def reset_archive_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveOnDestroy", []))

    @jsii.member(jsii_name="resetAutoInit")
    def reset_auto_init(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoInit", []))

    @jsii.member(jsii_name="resetDefaultBranch")
    def reset_default_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBranch", []))

    @jsii.member(jsii_name="resetDeleteBranchOnMerge")
    def reset_delete_branch_on_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteBranchOnMerge", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGitignoreTemplate")
    def reset_gitignore_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitignoreTemplate", []))

    @jsii.member(jsii_name="resetHasDiscussions")
    def reset_has_discussions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHasDiscussions", []))

    @jsii.member(jsii_name="resetHasDownloads")
    def reset_has_downloads(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHasDownloads", []))

    @jsii.member(jsii_name="resetHasIssues")
    def reset_has_issues(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHasIssues", []))

    @jsii.member(jsii_name="resetHasProjects")
    def reset_has_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHasProjects", []))

    @jsii.member(jsii_name="resetHasWiki")
    def reset_has_wiki(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHasWiki", []))

    @jsii.member(jsii_name="resetHomepageUrl")
    def reset_homepage_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHomepageUrl", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIgnoreVulnerabilityAlertsDuringRead")
    def reset_ignore_vulnerability_alerts_during_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreVulnerabilityAlertsDuringRead", []))

    @jsii.member(jsii_name="resetIsTemplate")
    def reset_is_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsTemplate", []))

    @jsii.member(jsii_name="resetLicenseTemplate")
    def reset_license_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseTemplate", []))

    @jsii.member(jsii_name="resetMergeCommitMessage")
    def reset_merge_commit_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeCommitMessage", []))

    @jsii.member(jsii_name="resetMergeCommitTitle")
    def reset_merge_commit_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeCommitTitle", []))

    @jsii.member(jsii_name="resetPages")
    def reset_pages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPages", []))

    @jsii.member(jsii_name="resetPrivate")
    def reset_private(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivate", []))

    @jsii.member(jsii_name="resetSecurityAndAnalysis")
    def reset_security_and_analysis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityAndAnalysis", []))

    @jsii.member(jsii_name="resetSquashMergeCommitMessage")
    def reset_squash_merge_commit_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSquashMergeCommitMessage", []))

    @jsii.member(jsii_name="resetSquashMergeCommitTitle")
    def reset_squash_merge_commit_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSquashMergeCommitTitle", []))

    @jsii.member(jsii_name="resetTemplate")
    def reset_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplate", []))

    @jsii.member(jsii_name="resetTopics")
    def reset_topics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopics", []))

    @jsii.member(jsii_name="resetVisibility")
    def reset_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibility", []))

    @jsii.member(jsii_name="resetVulnerabilityAlerts")
    def reset_vulnerability_alerts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVulnerabilityAlerts", []))

    @jsii.member(jsii_name="resetWebCommitSignoffRequired")
    def reset_web_commit_signoff_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebCommitSignoffRequired", []))

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
    @jsii.member(jsii_name="fullName")
    def full_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullName"))

    @builtins.property
    @jsii.member(jsii_name="gitCloneUrl")
    def git_clone_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gitCloneUrl"))

    @builtins.property
    @jsii.member(jsii_name="htmlUrl")
    def html_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "htmlUrl"))

    @builtins.property
    @jsii.member(jsii_name="httpCloneUrl")
    def http_clone_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpCloneUrl"))

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeId"))

    @builtins.property
    @jsii.member(jsii_name="pages")
    def pages(self) -> "RepositoryPagesOutputReference":
        return typing.cast("RepositoryPagesOutputReference", jsii.get(self, "pages"))

    @builtins.property
    @jsii.member(jsii_name="primaryLanguage")
    def primary_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryLanguage"))

    @builtins.property
    @jsii.member(jsii_name="repoId")
    def repo_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "repoId"))

    @builtins.property
    @jsii.member(jsii_name="securityAndAnalysis")
    def security_and_analysis(self) -> "RepositorySecurityAndAnalysisOutputReference":
        return typing.cast("RepositorySecurityAndAnalysisOutputReference", jsii.get(self, "securityAndAnalysis"))

    @builtins.property
    @jsii.member(jsii_name="sshCloneUrl")
    def ssh_clone_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshCloneUrl"))

    @builtins.property
    @jsii.member(jsii_name="svnUrl")
    def svn_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "svnUrl"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> "RepositoryTemplateOutputReference":
        return typing.cast("RepositoryTemplateOutputReference", jsii.get(self, "template"))

    @builtins.property
    @jsii.member(jsii_name="allowAutoMergeInput")
    def allow_auto_merge_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowAutoMergeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowMergeCommitInput")
    def allow_merge_commit_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowMergeCommitInput"))

    @builtins.property
    @jsii.member(jsii_name="allowRebaseMergeInput")
    def allow_rebase_merge_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowRebaseMergeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowSquashMergeInput")
    def allow_squash_merge_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowSquashMergeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowUpdateBranchInput")
    def allow_update_branch_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowUpdateBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="archivedInput")
    def archived_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "archivedInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveOnDestroyInput")
    def archive_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "archiveOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="autoInitInput")
    def auto_init_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoInitInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBranchInput")
    def default_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteBranchOnMergeInput")
    def delete_branch_on_merge_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteBranchOnMergeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="gitignoreTemplateInput")
    def gitignore_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gitignoreTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="hasDiscussionsInput")
    def has_discussions_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hasDiscussionsInput"))

    @builtins.property
    @jsii.member(jsii_name="hasDownloadsInput")
    def has_downloads_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hasDownloadsInput"))

    @builtins.property
    @jsii.member(jsii_name="hasIssuesInput")
    def has_issues_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hasIssuesInput"))

    @builtins.property
    @jsii.member(jsii_name="hasProjectsInput")
    def has_projects_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hasProjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="hasWikiInput")
    def has_wiki_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hasWikiInput"))

    @builtins.property
    @jsii.member(jsii_name="homepageUrlInput")
    def homepage_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "homepageUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreVulnerabilityAlertsDuringReadInput")
    def ignore_vulnerability_alerts_during_read_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreVulnerabilityAlertsDuringReadInput"))

    @builtins.property
    @jsii.member(jsii_name="isTemplateInput")
    def is_template_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseTemplateInput")
    def license_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeCommitMessageInput")
    def merge_commit_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeCommitMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="mergeCommitTitleInput")
    def merge_commit_title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeCommitTitleInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pagesInput")
    def pages_input(self) -> typing.Optional["RepositoryPages"]:
        return typing.cast(typing.Optional["RepositoryPages"], jsii.get(self, "pagesInput"))

    @builtins.property
    @jsii.member(jsii_name="privateInput")
    def private_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privateInput"))

    @builtins.property
    @jsii.member(jsii_name="securityAndAnalysisInput")
    def security_and_analysis_input(
        self,
    ) -> typing.Optional["RepositorySecurityAndAnalysis"]:
        return typing.cast(typing.Optional["RepositorySecurityAndAnalysis"], jsii.get(self, "securityAndAnalysisInput"))

    @builtins.property
    @jsii.member(jsii_name="squashMergeCommitMessageInput")
    def squash_merge_commit_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "squashMergeCommitMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="squashMergeCommitTitleInput")
    def squash_merge_commit_title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "squashMergeCommitTitleInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional["RepositoryTemplate"]:
        return typing.cast(typing.Optional["RepositoryTemplate"], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsInput")
    def topics_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicsInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityAlertsInput")
    def vulnerability_alerts_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vulnerabilityAlertsInput"))

    @builtins.property
    @jsii.member(jsii_name="webCommitSignoffRequiredInput")
    def web_commit_signoff_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "webCommitSignoffRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="allowAutoMerge")
    def allow_auto_merge(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowAutoMerge"))

    @allow_auto_merge.setter
    def allow_auto_merge(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99650853d3a92a01dc4d1ba7ebe37afa1883ed178a9c3561cc5f4bef9478817a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowAutoMerge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowMergeCommit")
    def allow_merge_commit(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowMergeCommit"))

    @allow_merge_commit.setter
    def allow_merge_commit(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878385ab00bb504b191864effd4adbc7284199482526d868d29de2e73fcb9897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowMergeCommit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowRebaseMerge")
    def allow_rebase_merge(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowRebaseMerge"))

    @allow_rebase_merge.setter
    def allow_rebase_merge(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cbc6ba8fd5f229b519fb138ae9c2b7bc2f1082c5d507ea5b1091617e7dbf901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowRebaseMerge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowSquashMerge")
    def allow_squash_merge(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowSquashMerge"))

    @allow_squash_merge.setter
    def allow_squash_merge(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edbd00add63457a11681a24fdcb852c26aa283efdbc2ab5cf8ed54bef2848654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowSquashMerge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowUpdateBranch")
    def allow_update_branch(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowUpdateBranch"))

    @allow_update_branch.setter
    def allow_update_branch(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d355ae4006ec0346d6e92b5687495aad9f9a6cfe8a960b9b282f2af3e585e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowUpdateBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="archived")
    def archived(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "archived"))

    @archived.setter
    def archived(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a89d532297afab3c41aa76a8bda56fb11e2126d1278037bcb7ed2530242275d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archived", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="archiveOnDestroy")
    def archive_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "archiveOnDestroy"))

    @archive_on_destroy.setter
    def archive_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c7ee0d20e92e88b40f8b9723595767af7866619806db9dafc669d3c7b9ab56d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveOnDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoInit")
    def auto_init(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoInit"))

    @auto_init.setter
    def auto_init(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__275631b99f5bcb75ffc2c37f2c85e10daa5a86b3d0f6bfdca4a8e59c6624d269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoInit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultBranch")
    def default_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBranch"))

    @default_branch.setter
    def default_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d82627b8e608cb706f8b0b0103a8905bb4285d838a94121c331dac434c4a219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBranch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deleteBranchOnMerge")
    def delete_branch_on_merge(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteBranchOnMerge"))

    @delete_branch_on_merge.setter
    def delete_branch_on_merge(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beec610fe68b3f8eb741bce1746af85c989da7ecf15d46eb475d1a7c10170589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteBranchOnMerge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153c99bce172791cc817c27471ae8a94be9803c752803e8b701a74253ac2c6be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gitignoreTemplate")
    def gitignore_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gitignoreTemplate"))

    @gitignore_template.setter
    def gitignore_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4dd717dd8ff90d55f5e7888c1fdc8bb62f67304dd40f717abd95e0f380cf1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitignoreTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hasDiscussions")
    def has_discussions(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hasDiscussions"))

    @has_discussions.setter
    def has_discussions(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3cbe7a89f443e870a9b54eb18b1fe46d81fb86c5825d32b22cc49b08d89415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hasDiscussions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hasDownloads")
    def has_downloads(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hasDownloads"))

    @has_downloads.setter
    def has_downloads(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc1226929319f79b0f22258c33baa892c9d17bb7019eb9aa982f99665e0bbf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hasDownloads", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hasIssues")
    def has_issues(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hasIssues"))

    @has_issues.setter
    def has_issues(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aabb803960373150821aca3eaf97fa08c22e6812ea61336756a995ab5a1e7dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hasIssues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hasProjects")
    def has_projects(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hasProjects"))

    @has_projects.setter
    def has_projects(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c0c39eea9b731d7e9e914745d27d02755313b9c43610cc575bf62cef93950ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hasProjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hasWiki")
    def has_wiki(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hasWiki"))

    @has_wiki.setter
    def has_wiki(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa7fbf91c923e683a067537c1c5339a36926e423c76ebaaaf0b44725b148c386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hasWiki", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="homepageUrl")
    def homepage_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "homepageUrl"))

    @homepage_url.setter
    def homepage_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de277fbf8336f5255bf195a3dca3e6edfb9771ec487fcf7c2b0d0350632a34c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homepageUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41276b8a0d8b7a4a1a36c03ff2bbd816265c1ce29adeb5f90d6e8611228e5ecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreVulnerabilityAlertsDuringRead")
    def ignore_vulnerability_alerts_during_read(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreVulnerabilityAlertsDuringRead"))

    @ignore_vulnerability_alerts_during_read.setter
    def ignore_vulnerability_alerts_during_read(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5781ff7c8f90bc3f290b3523a362cba6a48a3e82dfbff33e0901fa002b486ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreVulnerabilityAlertsDuringRead", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isTemplate")
    def is_template(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isTemplate"))

    @is_template.setter
    def is_template(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6adfb6f2116b34e9caa33399adc85a915dd98a46009743011daaf7a5fa72a70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseTemplate")
    def license_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseTemplate"))

    @license_template.setter
    def license_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9325b52990d5d121b4e6cd3eba62311db6ce5d3b0a226178262438fddc53c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeCommitMessage")
    def merge_commit_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeCommitMessage"))

    @merge_commit_message.setter
    def merge_commit_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46aedc6e5bc0dc0882e59ce1476dc2986b3a1eea7523c91b382983457cfd7bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeCommitMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergeCommitTitle")
    def merge_commit_title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeCommitTitle"))

    @merge_commit_title.setter
    def merge_commit_title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81782f66943ec0409028602d22567108cb5a4f5b92b3563ee3fc5065ff945a8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergeCommitTitle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af17b8d6c41d78ca61038e4489fa772bb3dcae53d05bf2bca711f74f8a2afe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="private")
    def private(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "private"))

    @private.setter
    def private(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b533af431d6317a8df4c0177ada9db710591ab677933cac0fc04be740548911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "private", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="squashMergeCommitMessage")
    def squash_merge_commit_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "squashMergeCommitMessage"))

    @squash_merge_commit_message.setter
    def squash_merge_commit_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58a7dbdfb62ba97aa9aea378f59daafc9605a99740b5c98e2b7a4d353e9a2a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "squashMergeCommitMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="squashMergeCommitTitle")
    def squash_merge_commit_title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "squashMergeCommitTitle"))

    @squash_merge_commit_title.setter
    def squash_merge_commit_title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c67e5851228220377c20ba7d4c6d6ba13852722f2b18650798fd75944be9cea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "squashMergeCommitTitle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topics"))

    @topics.setter
    def topics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f10b7b0930ff2a84f10d679fd5ac02b1f54d20920fb1c9e68aa246d87023eed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c015b68426f27974e8b92a324e97a5879348a85bbfd5d9964f02751c273d72b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vulnerabilityAlerts")
    def vulnerability_alerts(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vulnerabilityAlerts"))

    @vulnerability_alerts.setter
    def vulnerability_alerts(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a704b1d2003587d8f066fc9f61a3c126eea7fd1ba6665c26e30277cf8900c93a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vulnerabilityAlerts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webCommitSignoffRequired")
    def web_commit_signoff_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "webCommitSignoffRequired"))

    @web_commit_signoff_required.setter
    def web_commit_signoff_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38da02c3a4879deaddd2346983d744f94976e25f9de34d50826258c911e6a97f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webCommitSignoffRequired", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repository.RepositoryConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "allow_auto_merge": "allowAutoMerge",
        "allow_merge_commit": "allowMergeCommit",
        "allow_rebase_merge": "allowRebaseMerge",
        "allow_squash_merge": "allowSquashMerge",
        "allow_update_branch": "allowUpdateBranch",
        "archived": "archived",
        "archive_on_destroy": "archiveOnDestroy",
        "auto_init": "autoInit",
        "default_branch": "defaultBranch",
        "delete_branch_on_merge": "deleteBranchOnMerge",
        "description": "description",
        "gitignore_template": "gitignoreTemplate",
        "has_discussions": "hasDiscussions",
        "has_downloads": "hasDownloads",
        "has_issues": "hasIssues",
        "has_projects": "hasProjects",
        "has_wiki": "hasWiki",
        "homepage_url": "homepageUrl",
        "id": "id",
        "ignore_vulnerability_alerts_during_read": "ignoreVulnerabilityAlertsDuringRead",
        "is_template": "isTemplate",
        "license_template": "licenseTemplate",
        "merge_commit_message": "mergeCommitMessage",
        "merge_commit_title": "mergeCommitTitle",
        "pages": "pages",
        "private": "private",
        "security_and_analysis": "securityAndAnalysis",
        "squash_merge_commit_message": "squashMergeCommitMessage",
        "squash_merge_commit_title": "squashMergeCommitTitle",
        "template": "template",
        "topics": "topics",
        "visibility": "visibility",
        "vulnerability_alerts": "vulnerabilityAlerts",
        "web_commit_signoff_required": "webCommitSignoffRequired",
    },
)
class RepositoryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        allow_auto_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_merge_commit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_rebase_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_squash_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_update_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        archived: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        archive_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_init: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_branch: typing.Optional[builtins.str] = None,
        delete_branch_on_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        gitignore_template: typing.Optional[builtins.str] = None,
        has_discussions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        has_downloads: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        has_issues: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        has_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        has_wiki: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        homepage_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ignore_vulnerability_alerts_during_read: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_template: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        license_template: typing.Optional[builtins.str] = None,
        merge_commit_message: typing.Optional[builtins.str] = None,
        merge_commit_title: typing.Optional[builtins.str] = None,
        pages: typing.Optional[typing.Union["RepositoryPages", typing.Dict[builtins.str, typing.Any]]] = None,
        private: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        security_and_analysis: typing.Optional[typing.Union["RepositorySecurityAndAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
        squash_merge_commit_message: typing.Optional[builtins.str] = None,
        squash_merge_commit_title: typing.Optional[builtins.str] = None,
        template: typing.Optional[typing.Union["RepositoryTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        visibility: typing.Optional[builtins.str] = None,
        vulnerability_alerts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        web_commit_signoff_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#name Repository#name}
        :param allow_auto_merge: Set to 'true' to allow auto-merging pull requests on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_auto_merge Repository#allow_auto_merge}
        :param allow_merge_commit: Set to 'false' to disable merge commits on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_merge_commit Repository#allow_merge_commit}
        :param allow_rebase_merge: Set to 'false' to disable rebase merges on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_rebase_merge Repository#allow_rebase_merge}
        :param allow_squash_merge: Set to 'false' to disable squash merges on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_squash_merge Repository#allow_squash_merge}
        :param allow_update_branch: Set to 'true' to always suggest updating pull request branches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_update_branch Repository#allow_update_branch}
        :param archived: Specifies if the repository should be archived. Defaults to 'false'. NOTE Currently, the API does not support unarchiving. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#archived Repository#archived}
        :param archive_on_destroy: Set to 'true' to archive the repository instead of deleting on destroy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#archive_on_destroy Repository#archive_on_destroy}
        :param auto_init: Set to 'true' to produce an initial commit in the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#auto_init Repository#auto_init}
        :param default_branch: Can only be set after initial repository creation, and only if the target branch exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#default_branch Repository#default_branch}
        :param delete_branch_on_merge: Automatically delete head branch after a pull request is merged. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#delete_branch_on_merge Repository#delete_branch_on_merge}
        :param description: A description of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#description Repository#description}
        :param gitignore_template: Use the name of the template without the extension. For example, 'Haskell'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#gitignore_template Repository#gitignore_template}
        :param has_discussions: Set to 'true' to enable GitHub Discussions on the repository. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_discussions Repository#has_discussions}
        :param has_downloads: Set to 'true' to enable the (deprecated) downloads features on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_downloads Repository#has_downloads}
        :param has_issues: Set to 'true' to enable the GitHub Issues features on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_issues Repository#has_issues}
        :param has_projects: Set to 'true' to enable the GitHub Projects features on the repository. Per the GitHub documentation when in an organization that has disabled repository projects it will default to 'false' and will otherwise default to 'true'. If you specify 'true' when it has been disabled it will return an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_projects Repository#has_projects}
        :param has_wiki: Set to 'true' to enable the GitHub Wiki features on the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_wiki Repository#has_wiki}
        :param homepage_url: URL of a page describing the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#homepage_url Repository#homepage_url}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#id Repository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ignore_vulnerability_alerts_during_read: Set to true to not call the vulnerability alerts endpoint so the resource can also be used without admin permissions during read. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#ignore_vulnerability_alerts_during_read Repository#ignore_vulnerability_alerts_during_read}
        :param is_template: Set to 'true' to tell GitHub that this is a template repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#is_template Repository#is_template}
        :param license_template: Use the name of the template without the extension. For example, 'mit' or 'mpl-2.0'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#license_template Repository#license_template}
        :param merge_commit_message: Can be 'PR_BODY', 'PR_TITLE', or 'BLANK' for a default merge commit message. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#merge_commit_message Repository#merge_commit_message}
        :param merge_commit_title: Can be 'PR_TITLE' or 'MERGE_MESSAGE' for a default merge commit title. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#merge_commit_title Repository#merge_commit_title}
        :param pages: pages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#pages Repository#pages}
        :param private: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#private Repository#private}.
        :param security_and_analysis: security_and_analysis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#security_and_analysis Repository#security_and_analysis}
        :param squash_merge_commit_message: Can be 'PR_BODY', 'COMMIT_MESSAGES', or 'BLANK' for a default squash merge commit message. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#squash_merge_commit_message Repository#squash_merge_commit_message}
        :param squash_merge_commit_title: Can be 'PR_TITLE' or 'COMMIT_OR_PR_TITLE' for a default squash merge commit title. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#squash_merge_commit_title Repository#squash_merge_commit_title}
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#template Repository#template}
        :param topics: The list of topics of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#topics Repository#topics}
        :param visibility: Can be 'public' or 'private'. If your organization is associated with an enterprise account using GitHub Enterprise Cloud or GitHub Enterprise Server 2.20+, visibility can also be 'internal'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#visibility Repository#visibility}
        :param vulnerability_alerts: Set to 'true' to enable security alerts for vulnerable dependencies. Enabling requires alerts to be enabled on the owner level. (Note for importing: GitHub enables the alerts on public repos but disables them on private repos by default). Note that vulnerability alerts have not been successfully tested on any GitHub Enterprise instance and may be unavailable in those settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#vulnerability_alerts Repository#vulnerability_alerts}
        :param web_commit_signoff_required: Require contributors to sign off on web-based commits. Defaults to 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#web_commit_signoff_required Repository#web_commit_signoff_required}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(pages, dict):
            pages = RepositoryPages(**pages)
        if isinstance(security_and_analysis, dict):
            security_and_analysis = RepositorySecurityAndAnalysis(**security_and_analysis)
        if isinstance(template, dict):
            template = RepositoryTemplate(**template)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf45aa2a2862bb1ed66a9c1c6d0507f4baf01ba5d9eadf92e68c7a4499ed3955)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_auto_merge", value=allow_auto_merge, expected_type=type_hints["allow_auto_merge"])
            check_type(argname="argument allow_merge_commit", value=allow_merge_commit, expected_type=type_hints["allow_merge_commit"])
            check_type(argname="argument allow_rebase_merge", value=allow_rebase_merge, expected_type=type_hints["allow_rebase_merge"])
            check_type(argname="argument allow_squash_merge", value=allow_squash_merge, expected_type=type_hints["allow_squash_merge"])
            check_type(argname="argument allow_update_branch", value=allow_update_branch, expected_type=type_hints["allow_update_branch"])
            check_type(argname="argument archived", value=archived, expected_type=type_hints["archived"])
            check_type(argname="argument archive_on_destroy", value=archive_on_destroy, expected_type=type_hints["archive_on_destroy"])
            check_type(argname="argument auto_init", value=auto_init, expected_type=type_hints["auto_init"])
            check_type(argname="argument default_branch", value=default_branch, expected_type=type_hints["default_branch"])
            check_type(argname="argument delete_branch_on_merge", value=delete_branch_on_merge, expected_type=type_hints["delete_branch_on_merge"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument gitignore_template", value=gitignore_template, expected_type=type_hints["gitignore_template"])
            check_type(argname="argument has_discussions", value=has_discussions, expected_type=type_hints["has_discussions"])
            check_type(argname="argument has_downloads", value=has_downloads, expected_type=type_hints["has_downloads"])
            check_type(argname="argument has_issues", value=has_issues, expected_type=type_hints["has_issues"])
            check_type(argname="argument has_projects", value=has_projects, expected_type=type_hints["has_projects"])
            check_type(argname="argument has_wiki", value=has_wiki, expected_type=type_hints["has_wiki"])
            check_type(argname="argument homepage_url", value=homepage_url, expected_type=type_hints["homepage_url"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ignore_vulnerability_alerts_during_read", value=ignore_vulnerability_alerts_during_read, expected_type=type_hints["ignore_vulnerability_alerts_during_read"])
            check_type(argname="argument is_template", value=is_template, expected_type=type_hints["is_template"])
            check_type(argname="argument license_template", value=license_template, expected_type=type_hints["license_template"])
            check_type(argname="argument merge_commit_message", value=merge_commit_message, expected_type=type_hints["merge_commit_message"])
            check_type(argname="argument merge_commit_title", value=merge_commit_title, expected_type=type_hints["merge_commit_title"])
            check_type(argname="argument pages", value=pages, expected_type=type_hints["pages"])
            check_type(argname="argument private", value=private, expected_type=type_hints["private"])
            check_type(argname="argument security_and_analysis", value=security_and_analysis, expected_type=type_hints["security_and_analysis"])
            check_type(argname="argument squash_merge_commit_message", value=squash_merge_commit_message, expected_type=type_hints["squash_merge_commit_message"])
            check_type(argname="argument squash_merge_commit_title", value=squash_merge_commit_title, expected_type=type_hints["squash_merge_commit_title"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
            check_type(argname="argument vulnerability_alerts", value=vulnerability_alerts, expected_type=type_hints["vulnerability_alerts"])
            check_type(argname="argument web_commit_signoff_required", value=web_commit_signoff_required, expected_type=type_hints["web_commit_signoff_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if allow_auto_merge is not None:
            self._values["allow_auto_merge"] = allow_auto_merge
        if allow_merge_commit is not None:
            self._values["allow_merge_commit"] = allow_merge_commit
        if allow_rebase_merge is not None:
            self._values["allow_rebase_merge"] = allow_rebase_merge
        if allow_squash_merge is not None:
            self._values["allow_squash_merge"] = allow_squash_merge
        if allow_update_branch is not None:
            self._values["allow_update_branch"] = allow_update_branch
        if archived is not None:
            self._values["archived"] = archived
        if archive_on_destroy is not None:
            self._values["archive_on_destroy"] = archive_on_destroy
        if auto_init is not None:
            self._values["auto_init"] = auto_init
        if default_branch is not None:
            self._values["default_branch"] = default_branch
        if delete_branch_on_merge is not None:
            self._values["delete_branch_on_merge"] = delete_branch_on_merge
        if description is not None:
            self._values["description"] = description
        if gitignore_template is not None:
            self._values["gitignore_template"] = gitignore_template
        if has_discussions is not None:
            self._values["has_discussions"] = has_discussions
        if has_downloads is not None:
            self._values["has_downloads"] = has_downloads
        if has_issues is not None:
            self._values["has_issues"] = has_issues
        if has_projects is not None:
            self._values["has_projects"] = has_projects
        if has_wiki is not None:
            self._values["has_wiki"] = has_wiki
        if homepage_url is not None:
            self._values["homepage_url"] = homepage_url
        if id is not None:
            self._values["id"] = id
        if ignore_vulnerability_alerts_during_read is not None:
            self._values["ignore_vulnerability_alerts_during_read"] = ignore_vulnerability_alerts_during_read
        if is_template is not None:
            self._values["is_template"] = is_template
        if license_template is not None:
            self._values["license_template"] = license_template
        if merge_commit_message is not None:
            self._values["merge_commit_message"] = merge_commit_message
        if merge_commit_title is not None:
            self._values["merge_commit_title"] = merge_commit_title
        if pages is not None:
            self._values["pages"] = pages
        if private is not None:
            self._values["private"] = private
        if security_and_analysis is not None:
            self._values["security_and_analysis"] = security_and_analysis
        if squash_merge_commit_message is not None:
            self._values["squash_merge_commit_message"] = squash_merge_commit_message
        if squash_merge_commit_title is not None:
            self._values["squash_merge_commit_title"] = squash_merge_commit_title
        if template is not None:
            self._values["template"] = template
        if topics is not None:
            self._values["topics"] = topics
        if visibility is not None:
            self._values["visibility"] = visibility
        if vulnerability_alerts is not None:
            self._values["vulnerability_alerts"] = vulnerability_alerts
        if web_commit_signoff_required is not None:
            self._values["web_commit_signoff_required"] = web_commit_signoff_required

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
    def name(self) -> builtins.str:
        '''The name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#name Repository#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_auto_merge(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'true' to allow auto-merging pull requests on the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_auto_merge Repository#allow_auto_merge}
        '''
        result = self._values.get("allow_auto_merge")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_merge_commit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'false' to disable merge commits on the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_merge_commit Repository#allow_merge_commit}
        '''
        result = self._values.get("allow_merge_commit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_rebase_merge(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'false' to disable rebase merges on the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_rebase_merge Repository#allow_rebase_merge}
        '''
        result = self._values.get("allow_rebase_merge")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_squash_merge(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'false' to disable squash merges on the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_squash_merge Repository#allow_squash_merge}
        '''
        result = self._values.get("allow_squash_merge")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_update_branch(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'true' to always suggest updating pull request branches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#allow_update_branch Repository#allow_update_branch}
        '''
        result = self._values.get("allow_update_branch")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def archived(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the repository should be archived. Defaults to 'false'. NOTE Currently, the API does not support unarchiving.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#archived Repository#archived}
        '''
        result = self._values.get("archived")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def archive_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'true' to archive the repository instead of deleting on destroy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#archive_on_destroy Repository#archive_on_destroy}
        '''
        result = self._values.get("archive_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_init(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'true' to produce an initial commit in the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#auto_init Repository#auto_init}
        '''
        result = self._values.get("auto_init")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_branch(self) -> typing.Optional[builtins.str]:
        '''Can only be set after initial repository creation, and only if the target branch exists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#default_branch Repository#default_branch}
        '''
        result = self._values.get("default_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_branch_on_merge(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically delete head branch after a pull request is merged. Defaults to 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#delete_branch_on_merge Repository#delete_branch_on_merge}
        '''
        result = self._values.get("delete_branch_on_merge")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#description Repository#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gitignore_template(self) -> typing.Optional[builtins.str]:
        '''Use the name of the template without the extension. For example, 'Haskell'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#gitignore_template Repository#gitignore_template}
        '''
        result = self._values.get("gitignore_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def has_discussions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'true' to enable GitHub Discussions on the repository. Defaults to 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_discussions Repository#has_discussions}
        '''
        result = self._values.get("has_discussions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def has_downloads(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'true' to enable the (deprecated) downloads features on the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_downloads Repository#has_downloads}
        '''
        result = self._values.get("has_downloads")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def has_issues(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'true' to enable the GitHub Issues features on the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_issues Repository#has_issues}
        '''
        result = self._values.get("has_issues")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def has_projects(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'true' to enable the GitHub Projects features on the repository.

        Per the GitHub documentation when in an organization that has disabled repository projects it will default to 'false' and will otherwise default to 'true'. If you specify 'true' when it has been disabled it will return an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_projects Repository#has_projects}
        '''
        result = self._values.get("has_projects")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def has_wiki(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'true' to enable the GitHub Wiki features on the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#has_wiki Repository#has_wiki}
        '''
        result = self._values.get("has_wiki")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def homepage_url(self) -> typing.Optional[builtins.str]:
        '''URL of a page describing the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#homepage_url Repository#homepage_url}
        '''
        result = self._values.get("homepage_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#id Repository#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_vulnerability_alerts_during_read(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to not call the vulnerability alerts endpoint so the resource can also be used without admin permissions during read.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#ignore_vulnerability_alerts_during_read Repository#ignore_vulnerability_alerts_during_read}
        '''
        result = self._values.get("ignore_vulnerability_alerts_during_read")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_template(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'true' to tell GitHub that this is a template repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#is_template Repository#is_template}
        '''
        result = self._values.get("is_template")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def license_template(self) -> typing.Optional[builtins.str]:
        '''Use the name of the template without the extension. For example, 'mit' or 'mpl-2.0'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#license_template Repository#license_template}
        '''
        result = self._values.get("license_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_commit_message(self) -> typing.Optional[builtins.str]:
        '''Can be 'PR_BODY', 'PR_TITLE', or 'BLANK' for a default merge commit message.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#merge_commit_message Repository#merge_commit_message}
        '''
        result = self._values.get("merge_commit_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_commit_title(self) -> typing.Optional[builtins.str]:
        '''Can be 'PR_TITLE' or 'MERGE_MESSAGE' for a default merge commit title.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#merge_commit_title Repository#merge_commit_title}
        '''
        result = self._values.get("merge_commit_title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pages(self) -> typing.Optional["RepositoryPages"]:
        '''pages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#pages Repository#pages}
        '''
        result = self._values.get("pages")
        return typing.cast(typing.Optional["RepositoryPages"], result)

    @builtins.property
    def private(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#private Repository#private}.'''
        result = self._values.get("private")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def security_and_analysis(self) -> typing.Optional["RepositorySecurityAndAnalysis"]:
        '''security_and_analysis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#security_and_analysis Repository#security_and_analysis}
        '''
        result = self._values.get("security_and_analysis")
        return typing.cast(typing.Optional["RepositorySecurityAndAnalysis"], result)

    @builtins.property
    def squash_merge_commit_message(self) -> typing.Optional[builtins.str]:
        '''Can be 'PR_BODY', 'COMMIT_MESSAGES', or 'BLANK' for a default squash merge commit message.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#squash_merge_commit_message Repository#squash_merge_commit_message}
        '''
        result = self._values.get("squash_merge_commit_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def squash_merge_commit_title(self) -> typing.Optional[builtins.str]:
        '''Can be 'PR_TITLE' or 'COMMIT_OR_PR_TITLE' for a default squash merge commit title.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#squash_merge_commit_title Repository#squash_merge_commit_title}
        '''
        result = self._values.get("squash_merge_commit_title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional["RepositoryTemplate"]:
        '''template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#template Repository#template}
        '''
        result = self._values.get("template")
        return typing.cast(typing.Optional["RepositoryTemplate"], result)

    @builtins.property
    def topics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of topics of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#topics Repository#topics}
        '''
        result = self._values.get("topics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''Can be 'public' or 'private'.

        If your organization is associated with an enterprise account using GitHub Enterprise Cloud or GitHub Enterprise Server 2.20+, visibility can also be 'internal'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#visibility Repository#visibility}
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vulnerability_alerts(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to 'true' to enable security alerts for vulnerable dependencies.

        Enabling requires alerts to be enabled on the owner level. (Note for importing: GitHub enables the alerts on public repos but disables them on private repos by default). Note that vulnerability alerts have not been successfully tested on any GitHub Enterprise instance and may be unavailable in those settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#vulnerability_alerts Repository#vulnerability_alerts}
        '''
        result = self._values.get("vulnerability_alerts")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def web_commit_signoff_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require contributors to sign off on web-based commits. Defaults to 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#web_commit_signoff_required Repository#web_commit_signoff_required}
        '''
        result = self._values.get("web_commit_signoff_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repository.RepositoryPages",
    jsii_struct_bases=[],
    name_mapping={"build_type": "buildType", "cname": "cname", "source": "source"},
)
class RepositoryPages:
    def __init__(
        self,
        *,
        build_type: typing.Optional[builtins.str] = None,
        cname: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union["RepositoryPagesSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param build_type: The type the page should be sourced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#build_type Repository#build_type}
        :param cname: The custom domain for the repository. This can only be set after the repository has been created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#cname Repository#cname}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#source Repository#source}
        '''
        if isinstance(source, dict):
            source = RepositoryPagesSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e70954b03ec2fc6d73711de71b671665b05be37af10edbd9dfa22c9f0d3c627)
            check_type(argname="argument build_type", value=build_type, expected_type=type_hints["build_type"])
            check_type(argname="argument cname", value=cname, expected_type=type_hints["cname"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_type is not None:
            self._values["build_type"] = build_type
        if cname is not None:
            self._values["cname"] = cname
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def build_type(self) -> typing.Optional[builtins.str]:
        '''The type the page should be sourced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#build_type Repository#build_type}
        '''
        result = self._values.get("build_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cname(self) -> typing.Optional[builtins.str]:
        '''The custom domain for the repository. This can only be set after the repository has been created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#cname Repository#cname}
        '''
        result = self._values.get("cname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional["RepositoryPagesSource"]:
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#source Repository#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional["RepositoryPagesSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryPages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryPagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repository.RepositoryPagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc39fc85ebe0ca382f6c91c3ce6febc8fbc7aa41c07fc35c1e2f829d0b3a99cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        branch: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: The repository branch used to publish the site's source files. (i.e. 'main' or 'gh-pages'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#branch Repository#branch}
        :param path: The repository directory from which the site publishes (Default: '/'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#path Repository#path}
        '''
        value = RepositoryPagesSource(branch=branch, path=path)

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetBuildType")
    def reset_build_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildType", []))

    @jsii.member(jsii_name="resetCname")
    def reset_cname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCname", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="custom404")
    def custom404(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "custom404"))

    @builtins.property
    @jsii.member(jsii_name="htmlUrl")
    def html_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "htmlUrl"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "RepositoryPagesSourceOutputReference":
        return typing.cast("RepositoryPagesSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="buildTypeInput")
    def build_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="cnameInput")
    def cname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cnameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["RepositoryPagesSource"]:
        return typing.cast(typing.Optional["RepositoryPagesSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="buildType")
    def build_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildType"))

    @build_type.setter
    def build_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c7e022cdb055fb850ebbb53e5d34c3e4c7fa91ef22c037a32e468243bce69c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cname")
    def cname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cname"))

    @cname.setter
    def cname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b3077c649c51a594da8f67f7f248d5f35c24f90b98cf8ca3fd803af57b78c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RepositoryPages]:
        return typing.cast(typing.Optional[RepositoryPages], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RepositoryPages]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8513c8d12ce6adec782376907310e85f82873d4168058dd6095d00c9fb549aca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repository.RepositoryPagesSource",
    jsii_struct_bases=[],
    name_mapping={"branch": "branch", "path": "path"},
)
class RepositoryPagesSource:
    def __init__(
        self,
        *,
        branch: builtins.str,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch: The repository branch used to publish the site's source files. (i.e. 'main' or 'gh-pages'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#branch Repository#branch}
        :param path: The repository directory from which the site publishes (Default: '/'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#path Repository#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5beded292f823133ae8a0115dd9507c0fe069fdbf4fc228ed92e47333d2faf8d)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch": branch,
        }
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def branch(self) -> builtins.str:
        '''The repository branch used to publish the site's source files. (i.e. 'main' or 'gh-pages').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#branch Repository#branch}
        '''
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The repository directory from which the site publishes (Default: '/').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#path Repository#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryPagesSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryPagesSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repository.RepositoryPagesSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__316b98d430444a10a3456d4927de1d098dc30bacf358fdd8627a224324b92bd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee3795175aaf4d9257ed29094619ba68b74a4c914326b2f6c904805fad43d33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5fef149b3940ead876160ca588253e17f7fc181cc11944dd951fd31e6cf84ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RepositoryPagesSource]:
        return typing.cast(typing.Optional[RepositoryPagesSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RepositoryPagesSource]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4345e041b3479f94cdf30bae9c5fb963ca71af30ed7f6197301b7a61b82db754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repository.RepositorySecurityAndAnalysis",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_security": "advancedSecurity",
        "secret_scanning": "secretScanning",
        "secret_scanning_push_protection": "secretScanningPushProtection",
    },
)
class RepositorySecurityAndAnalysis:
    def __init__(
        self,
        *,
        advanced_security: typing.Optional[typing.Union["RepositorySecurityAndAnalysisAdvancedSecurity", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_scanning: typing.Optional[typing.Union["RepositorySecurityAndAnalysisSecretScanning", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_scanning_push_protection: typing.Optional[typing.Union["RepositorySecurityAndAnalysisSecretScanningPushProtection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_security: advanced_security block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#advanced_security Repository#advanced_security}
        :param secret_scanning: secret_scanning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#secret_scanning Repository#secret_scanning}
        :param secret_scanning_push_protection: secret_scanning_push_protection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#secret_scanning_push_protection Repository#secret_scanning_push_protection}
        '''
        if isinstance(advanced_security, dict):
            advanced_security = RepositorySecurityAndAnalysisAdvancedSecurity(**advanced_security)
        if isinstance(secret_scanning, dict):
            secret_scanning = RepositorySecurityAndAnalysisSecretScanning(**secret_scanning)
        if isinstance(secret_scanning_push_protection, dict):
            secret_scanning_push_protection = RepositorySecurityAndAnalysisSecretScanningPushProtection(**secret_scanning_push_protection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2271226c425db0d89da181b9aab44265a6313794e3fd0e05246d55d1d919ac)
            check_type(argname="argument advanced_security", value=advanced_security, expected_type=type_hints["advanced_security"])
            check_type(argname="argument secret_scanning", value=secret_scanning, expected_type=type_hints["secret_scanning"])
            check_type(argname="argument secret_scanning_push_protection", value=secret_scanning_push_protection, expected_type=type_hints["secret_scanning_push_protection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advanced_security is not None:
            self._values["advanced_security"] = advanced_security
        if secret_scanning is not None:
            self._values["secret_scanning"] = secret_scanning
        if secret_scanning_push_protection is not None:
            self._values["secret_scanning_push_protection"] = secret_scanning_push_protection

    @builtins.property
    def advanced_security(
        self,
    ) -> typing.Optional["RepositorySecurityAndAnalysisAdvancedSecurity"]:
        '''advanced_security block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#advanced_security Repository#advanced_security}
        '''
        result = self._values.get("advanced_security")
        return typing.cast(typing.Optional["RepositorySecurityAndAnalysisAdvancedSecurity"], result)

    @builtins.property
    def secret_scanning(
        self,
    ) -> typing.Optional["RepositorySecurityAndAnalysisSecretScanning"]:
        '''secret_scanning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#secret_scanning Repository#secret_scanning}
        '''
        result = self._values.get("secret_scanning")
        return typing.cast(typing.Optional["RepositorySecurityAndAnalysisSecretScanning"], result)

    @builtins.property
    def secret_scanning_push_protection(
        self,
    ) -> typing.Optional["RepositorySecurityAndAnalysisSecretScanningPushProtection"]:
        '''secret_scanning_push_protection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#secret_scanning_push_protection Repository#secret_scanning_push_protection}
        '''
        result = self._values.get("secret_scanning_push_protection")
        return typing.cast(typing.Optional["RepositorySecurityAndAnalysisSecretScanningPushProtection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositorySecurityAndAnalysis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repository.RepositorySecurityAndAnalysisAdvancedSecurity",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class RepositorySecurityAndAnalysisAdvancedSecurity:
    def __init__(self, *, status: builtins.str) -> None:
        '''
        :param status: Set to 'enabled' to enable advanced security features on the repository. Can be 'enabled' or 'disabled'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#status Repository#status}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c060f5659b2b3b99f5dde43e74e6375fb9f6421b37afa59e72e3c81e5837e652)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status": status,
        }

    @builtins.property
    def status(self) -> builtins.str:
        '''Set to 'enabled' to enable advanced security features on the repository. Can be 'enabled' or 'disabled'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#status Repository#status}
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositorySecurityAndAnalysisAdvancedSecurity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositorySecurityAndAnalysisAdvancedSecurityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repository.RepositorySecurityAndAnalysisAdvancedSecurityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a1da9a485ee8e15e77ad3b28d6589c38c5a11c37c29342b9bc32b65fe8b72f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad685c7b3d553e977affe8335a041cbe6f285c1d1e4079ee871f4f571e719a2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RepositorySecurityAndAnalysisAdvancedSecurity]:
        return typing.cast(typing.Optional[RepositorySecurityAndAnalysisAdvancedSecurity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositorySecurityAndAnalysisAdvancedSecurity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1c288f893e52bfca20137ec08671dbc0ddd877d3d3586b059abf74cb9d3946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RepositorySecurityAndAnalysisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repository.RepositorySecurityAndAnalysisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3aaef169e08107d2826b4b45aacfc39c649f876a4ff97927c8f02ff45bedd36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdvancedSecurity")
    def put_advanced_security(self, *, status: builtins.str) -> None:
        '''
        :param status: Set to 'enabled' to enable advanced security features on the repository. Can be 'enabled' or 'disabled'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#status Repository#status}
        '''
        value = RepositorySecurityAndAnalysisAdvancedSecurity(status=status)

        return typing.cast(None, jsii.invoke(self, "putAdvancedSecurity", [value]))

    @jsii.member(jsii_name="putSecretScanning")
    def put_secret_scanning(self, *, status: builtins.str) -> None:
        '''
        :param status: Set to 'enabled' to enable secret scanning on the repository. Can be 'enabled' or 'disabled'. If set to 'enabled', the repository's visibility must be 'public' or 'security_and_analysis[0].advanced_security[0].status' must also be set to 'enabled'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#status Repository#status}
        '''
        value = RepositorySecurityAndAnalysisSecretScanning(status=status)

        return typing.cast(None, jsii.invoke(self, "putSecretScanning", [value]))

    @jsii.member(jsii_name="putSecretScanningPushProtection")
    def put_secret_scanning_push_protection(self, *, status: builtins.str) -> None:
        '''
        :param status: Set to 'enabled' to enable secret scanning push protection on the repository. Can be 'enabled' or 'disabled'. If set to 'enabled', the repository's visibility must be 'public' or 'security_and_analysis[0].advanced_security[0].status' must also be set to 'enabled'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#status Repository#status}
        '''
        value = RepositorySecurityAndAnalysisSecretScanningPushProtection(
            status=status
        )

        return typing.cast(None, jsii.invoke(self, "putSecretScanningPushProtection", [value]))

    @jsii.member(jsii_name="resetAdvancedSecurity")
    def reset_advanced_security(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedSecurity", []))

    @jsii.member(jsii_name="resetSecretScanning")
    def reset_secret_scanning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretScanning", []))

    @jsii.member(jsii_name="resetSecretScanningPushProtection")
    def reset_secret_scanning_push_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretScanningPushProtection", []))

    @builtins.property
    @jsii.member(jsii_name="advancedSecurity")
    def advanced_security(
        self,
    ) -> RepositorySecurityAndAnalysisAdvancedSecurityOutputReference:
        return typing.cast(RepositorySecurityAndAnalysisAdvancedSecurityOutputReference, jsii.get(self, "advancedSecurity"))

    @builtins.property
    @jsii.member(jsii_name="secretScanning")
    def secret_scanning(
        self,
    ) -> "RepositorySecurityAndAnalysisSecretScanningOutputReference":
        return typing.cast("RepositorySecurityAndAnalysisSecretScanningOutputReference", jsii.get(self, "secretScanning"))

    @builtins.property
    @jsii.member(jsii_name="secretScanningPushProtection")
    def secret_scanning_push_protection(
        self,
    ) -> "RepositorySecurityAndAnalysisSecretScanningPushProtectionOutputReference":
        return typing.cast("RepositorySecurityAndAnalysisSecretScanningPushProtectionOutputReference", jsii.get(self, "secretScanningPushProtection"))

    @builtins.property
    @jsii.member(jsii_name="advancedSecurityInput")
    def advanced_security_input(
        self,
    ) -> typing.Optional[RepositorySecurityAndAnalysisAdvancedSecurity]:
        return typing.cast(typing.Optional[RepositorySecurityAndAnalysisAdvancedSecurity], jsii.get(self, "advancedSecurityInput"))

    @builtins.property
    @jsii.member(jsii_name="secretScanningInput")
    def secret_scanning_input(
        self,
    ) -> typing.Optional["RepositorySecurityAndAnalysisSecretScanning"]:
        return typing.cast(typing.Optional["RepositorySecurityAndAnalysisSecretScanning"], jsii.get(self, "secretScanningInput"))

    @builtins.property
    @jsii.member(jsii_name="secretScanningPushProtectionInput")
    def secret_scanning_push_protection_input(
        self,
    ) -> typing.Optional["RepositorySecurityAndAnalysisSecretScanningPushProtection"]:
        return typing.cast(typing.Optional["RepositorySecurityAndAnalysisSecretScanningPushProtection"], jsii.get(self, "secretScanningPushProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RepositorySecurityAndAnalysis]:
        return typing.cast(typing.Optional[RepositorySecurityAndAnalysis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositorySecurityAndAnalysis],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df31ab65b7009a6b82cad2ea5e9794c0effc97ab93deca14f917f7c25fb7756e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repository.RepositorySecurityAndAnalysisSecretScanning",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class RepositorySecurityAndAnalysisSecretScanning:
    def __init__(self, *, status: builtins.str) -> None:
        '''
        :param status: Set to 'enabled' to enable secret scanning on the repository. Can be 'enabled' or 'disabled'. If set to 'enabled', the repository's visibility must be 'public' or 'security_and_analysis[0].advanced_security[0].status' must also be set to 'enabled'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#status Repository#status}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6164211dbb6fd704aed460be387f07b5a588b13bb5802360f1cb4702b588c090)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status": status,
        }

    @builtins.property
    def status(self) -> builtins.str:
        '''Set to 'enabled' to enable secret scanning on the repository.

        Can be 'enabled' or 'disabled'. If set to 'enabled', the repository's visibility must be 'public' or 'security_and_analysis[0].advanced_security[0].status' must also be set to 'enabled'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#status Repository#status}
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositorySecurityAndAnalysisSecretScanning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositorySecurityAndAnalysisSecretScanningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repository.RepositorySecurityAndAnalysisSecretScanningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51c61a1b3e24b29bb5627a29832b303ce518c1e26b1e8279dd3913fea62da4ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791c1dfed45f39da7b241640ea3d01f9e917b5afe448f73afa7370601fa71fa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RepositorySecurityAndAnalysisSecretScanning]:
        return typing.cast(typing.Optional[RepositorySecurityAndAnalysisSecretScanning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositorySecurityAndAnalysisSecretScanning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f03c28050e0b54f4bb1f8e99538edf26948ee1daead74611520521f03728b45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repository.RepositorySecurityAndAnalysisSecretScanningPushProtection",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class RepositorySecurityAndAnalysisSecretScanningPushProtection:
    def __init__(self, *, status: builtins.str) -> None:
        '''
        :param status: Set to 'enabled' to enable secret scanning push protection on the repository. Can be 'enabled' or 'disabled'. If set to 'enabled', the repository's visibility must be 'public' or 'security_and_analysis[0].advanced_security[0].status' must also be set to 'enabled'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#status Repository#status}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2083f15b0562ff12040b1799f97bbd932e55702e421029024331fc7942af64dd)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status": status,
        }

    @builtins.property
    def status(self) -> builtins.str:
        '''Set to 'enabled' to enable secret scanning push protection on the repository.

        Can be 'enabled' or 'disabled'. If set to 'enabled', the repository's visibility must be 'public' or 'security_and_analysis[0].advanced_security[0].status' must also be set to 'enabled'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#status Repository#status}
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositorySecurityAndAnalysisSecretScanningPushProtection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositorySecurityAndAnalysisSecretScanningPushProtectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repository.RepositorySecurityAndAnalysisSecretScanningPushProtectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d157ba43406867df49b7a925d14bddf1aed84ad4a42e220967b9cae1c385f02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eef98dcb428f4e572cc2504d76a0d7a8c3503f232dccdea1ec78e0fdb39680f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[RepositorySecurityAndAnalysisSecretScanningPushProtection]:
        return typing.cast(typing.Optional[RepositorySecurityAndAnalysisSecretScanningPushProtection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[RepositorySecurityAndAnalysisSecretScanningPushProtection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4263c524d3a85aeb56e25964732727aa16cc0bc3b9c5e152f451d90ad87d769c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-github.repository.RepositoryTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "owner": "owner",
        "repository": "repository",
        "include_all_branches": "includeAllBranches",
    },
)
class RepositoryTemplate:
    def __init__(
        self,
        *,
        owner: builtins.str,
        repository: builtins.str,
        include_all_branches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param owner: The GitHub organization or user the template repository is owned by. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#owner Repository#owner}
        :param repository: The name of the template repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#repository Repository#repository}
        :param include_all_branches: Whether the new repository should include all the branches from the template repository (defaults to 'false', which includes only the default branch from the template). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#include_all_branches Repository#include_all_branches}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc62e7345a0e9e923f09ce69faaa43213f8a732c86f9d3dbd62c00a22c04ee1)
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument include_all_branches", value=include_all_branches, expected_type=type_hints["include_all_branches"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "owner": owner,
            "repository": repository,
        }
        if include_all_branches is not None:
            self._values["include_all_branches"] = include_all_branches

    @builtins.property
    def owner(self) -> builtins.str:
        '''The GitHub organization or user the template repository is owned by.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#owner Repository#owner}
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''The name of the template repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#repository Repository#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_all_branches(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the new repository should include all the branches from the template repository (defaults to 'false', which includes only the default branch from the template).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/integrations/github/6.6.0/docs/resources/repository#include_all_branches Repository#include_all_branches}
        '''
        result = self._values.get("include_all_branches")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RepositoryTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-github.repository.RepositoryTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f21abaa3f03ff88ecf69810b2eb33a1b7da79581edecc0f2ef1add2deb0f9b65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeAllBranches")
    def reset_include_all_branches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeAllBranches", []))

    @builtins.property
    @jsii.member(jsii_name="includeAllBranchesInput")
    def include_all_branches_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeAllBranchesInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerInput")
    def owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="includeAllBranches")
    def include_all_branches(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeAllBranches"))

    @include_all_branches.setter
    def include_all_branches(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975360c89abc404aeb04a16ba3afd1b1aaa26d8a098276e031b5971f1343c737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeAllBranches", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f8ecbb952e1f806294852fbf6e7a8aa667a1420cb688d796d251223f9958ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c6af51a941a35e73f6f1c762f0a5e9135566c6d3ad6b39ad8730ca9310c600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RepositoryTemplate]:
        return typing.cast(typing.Optional[RepositoryTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RepositoryTemplate]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88636d4721259dfd00b20d1e0912f71f22cff229ac84c2c58f0d2c6aabb41acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Repository",
    "RepositoryConfig",
    "RepositoryPages",
    "RepositoryPagesOutputReference",
    "RepositoryPagesSource",
    "RepositoryPagesSourceOutputReference",
    "RepositorySecurityAndAnalysis",
    "RepositorySecurityAndAnalysisAdvancedSecurity",
    "RepositorySecurityAndAnalysisAdvancedSecurityOutputReference",
    "RepositorySecurityAndAnalysisOutputReference",
    "RepositorySecurityAndAnalysisSecretScanning",
    "RepositorySecurityAndAnalysisSecretScanningOutputReference",
    "RepositorySecurityAndAnalysisSecretScanningPushProtection",
    "RepositorySecurityAndAnalysisSecretScanningPushProtectionOutputReference",
    "RepositoryTemplate",
    "RepositoryTemplateOutputReference",
]

publication.publish()

def _typecheckingstub__fb2ad3de9416f1cba9636a8de2ff57cade0941e6e3933abbb2c231a3d8dcf74f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    allow_auto_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_merge_commit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_rebase_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_squash_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_update_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    archived: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    archive_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_init: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_branch: typing.Optional[builtins.str] = None,
    delete_branch_on_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    gitignore_template: typing.Optional[builtins.str] = None,
    has_discussions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    has_downloads: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    has_issues: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    has_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    has_wiki: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    homepage_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_vulnerability_alerts_during_read: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_template: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    license_template: typing.Optional[builtins.str] = None,
    merge_commit_message: typing.Optional[builtins.str] = None,
    merge_commit_title: typing.Optional[builtins.str] = None,
    pages: typing.Optional[typing.Union[RepositoryPages, typing.Dict[builtins.str, typing.Any]]] = None,
    private: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_and_analysis: typing.Optional[typing.Union[RepositorySecurityAndAnalysis, typing.Dict[builtins.str, typing.Any]]] = None,
    squash_merge_commit_message: typing.Optional[builtins.str] = None,
    squash_merge_commit_title: typing.Optional[builtins.str] = None,
    template: typing.Optional[typing.Union[RepositoryTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    visibility: typing.Optional[builtins.str] = None,
    vulnerability_alerts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    web_commit_signoff_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__91b9384013746d127f245dfc9ec069a828cb2e0ca83b883e8a34dd859548ec8e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99650853d3a92a01dc4d1ba7ebe37afa1883ed178a9c3561cc5f4bef9478817a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878385ab00bb504b191864effd4adbc7284199482526d868d29de2e73fcb9897(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cbc6ba8fd5f229b519fb138ae9c2b7bc2f1082c5d507ea5b1091617e7dbf901(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edbd00add63457a11681a24fdcb852c26aa283efdbc2ab5cf8ed54bef2848654(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d355ae4006ec0346d6e92b5687495aad9f9a6cfe8a960b9b282f2af3e585e12(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a89d532297afab3c41aa76a8bda56fb11e2126d1278037bcb7ed2530242275d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7ee0d20e92e88b40f8b9723595767af7866619806db9dafc669d3c7b9ab56d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275631b99f5bcb75ffc2c37f2c85e10daa5a86b3d0f6bfdca4a8e59c6624d269(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d82627b8e608cb706f8b0b0103a8905bb4285d838a94121c331dac434c4a219(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beec610fe68b3f8eb741bce1746af85c989da7ecf15d46eb475d1a7c10170589(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153c99bce172791cc817c27471ae8a94be9803c752803e8b701a74253ac2c6be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4dd717dd8ff90d55f5e7888c1fdc8bb62f67304dd40f717abd95e0f380cf1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3cbe7a89f443e870a9b54eb18b1fe46d81fb86c5825d32b22cc49b08d89415(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc1226929319f79b0f22258c33baa892c9d17bb7019eb9aa982f99665e0bbf1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aabb803960373150821aca3eaf97fa08c22e6812ea61336756a995ab5a1e7dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c0c39eea9b731d7e9e914745d27d02755313b9c43610cc575bf62cef93950ae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7fbf91c923e683a067537c1c5339a36926e423c76ebaaaf0b44725b148c386(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de277fbf8336f5255bf195a3dca3e6edfb9771ec487fcf7c2b0d0350632a34c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41276b8a0d8b7a4a1a36c03ff2bbd816265c1ce29adeb5f90d6e8611228e5ecb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5781ff7c8f90bc3f290b3523a362cba6a48a3e82dfbff33e0901fa002b486ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6adfb6f2116b34e9caa33399adc85a915dd98a46009743011daaf7a5fa72a70(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9325b52990d5d121b4e6cd3eba62311db6ce5d3b0a226178262438fddc53c4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46aedc6e5bc0dc0882e59ce1476dc2986b3a1eea7523c91b382983457cfd7bde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81782f66943ec0409028602d22567108cb5a4f5b92b3563ee3fc5065ff945a8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af17b8d6c41d78ca61038e4489fa772bb3dcae53d05bf2bca711f74f8a2afe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b533af431d6317a8df4c0177ada9db710591ab677933cac0fc04be740548911(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58a7dbdfb62ba97aa9aea378f59daafc9605a99740b5c98e2b7a4d353e9a2a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c67e5851228220377c20ba7d4c6d6ba13852722f2b18650798fd75944be9cea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f10b7b0930ff2a84f10d679fd5ac02b1f54d20920fb1c9e68aa246d87023eed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c015b68426f27974e8b92a324e97a5879348a85bbfd5d9964f02751c273d72b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a704b1d2003587d8f066fc9f61a3c126eea7fd1ba6665c26e30277cf8900c93a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38da02c3a4879deaddd2346983d744f94976e25f9de34d50826258c911e6a97f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf45aa2a2862bb1ed66a9c1c6d0507f4baf01ba5d9eadf92e68c7a4499ed3955(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    allow_auto_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_merge_commit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_rebase_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_squash_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_update_branch: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    archived: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    archive_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_init: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_branch: typing.Optional[builtins.str] = None,
    delete_branch_on_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    gitignore_template: typing.Optional[builtins.str] = None,
    has_discussions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    has_downloads: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    has_issues: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    has_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    has_wiki: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    homepage_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ignore_vulnerability_alerts_during_read: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_template: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    license_template: typing.Optional[builtins.str] = None,
    merge_commit_message: typing.Optional[builtins.str] = None,
    merge_commit_title: typing.Optional[builtins.str] = None,
    pages: typing.Optional[typing.Union[RepositoryPages, typing.Dict[builtins.str, typing.Any]]] = None,
    private: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    security_and_analysis: typing.Optional[typing.Union[RepositorySecurityAndAnalysis, typing.Dict[builtins.str, typing.Any]]] = None,
    squash_merge_commit_message: typing.Optional[builtins.str] = None,
    squash_merge_commit_title: typing.Optional[builtins.str] = None,
    template: typing.Optional[typing.Union[RepositoryTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    visibility: typing.Optional[builtins.str] = None,
    vulnerability_alerts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    web_commit_signoff_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e70954b03ec2fc6d73711de71b671665b05be37af10edbd9dfa22c9f0d3c627(
    *,
    build_type: typing.Optional[builtins.str] = None,
    cname: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[RepositoryPagesSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc39fc85ebe0ca382f6c91c3ce6febc8fbc7aa41c07fc35c1e2f829d0b3a99cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c7e022cdb055fb850ebbb53e5d34c3e4c7fa91ef22c037a32e468243bce69c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b3077c649c51a594da8f67f7f248d5f35c24f90b98cf8ca3fd803af57b78c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8513c8d12ce6adec782376907310e85f82873d4168058dd6095d00c9fb549aca(
    value: typing.Optional[RepositoryPages],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5beded292f823133ae8a0115dd9507c0fe069fdbf4fc228ed92e47333d2faf8d(
    *,
    branch: builtins.str,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316b98d430444a10a3456d4927de1d098dc30bacf358fdd8627a224324b92bd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee3795175aaf4d9257ed29094619ba68b74a4c914326b2f6c904805fad43d33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fef149b3940ead876160ca588253e17f7fc181cc11944dd951fd31e6cf84ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4345e041b3479f94cdf30bae9c5fb963ca71af30ed7f6197301b7a61b82db754(
    value: typing.Optional[RepositoryPagesSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2271226c425db0d89da181b9aab44265a6313794e3fd0e05246d55d1d919ac(
    *,
    advanced_security: typing.Optional[typing.Union[RepositorySecurityAndAnalysisAdvancedSecurity, typing.Dict[builtins.str, typing.Any]]] = None,
    secret_scanning: typing.Optional[typing.Union[RepositorySecurityAndAnalysisSecretScanning, typing.Dict[builtins.str, typing.Any]]] = None,
    secret_scanning_push_protection: typing.Optional[typing.Union[RepositorySecurityAndAnalysisSecretScanningPushProtection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c060f5659b2b3b99f5dde43e74e6375fb9f6421b37afa59e72e3c81e5837e652(
    *,
    status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1da9a485ee8e15e77ad3b28d6589c38c5a11c37c29342b9bc32b65fe8b72f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad685c7b3d553e977affe8335a041cbe6f285c1d1e4079ee871f4f571e719a2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1c288f893e52bfca20137ec08671dbc0ddd877d3d3586b059abf74cb9d3946(
    value: typing.Optional[RepositorySecurityAndAnalysisAdvancedSecurity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3aaef169e08107d2826b4b45aacfc39c649f876a4ff97927c8f02ff45bedd36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df31ab65b7009a6b82cad2ea5e9794c0effc97ab93deca14f917f7c25fb7756e(
    value: typing.Optional[RepositorySecurityAndAnalysis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6164211dbb6fd704aed460be387f07b5a588b13bb5802360f1cb4702b588c090(
    *,
    status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c61a1b3e24b29bb5627a29832b303ce518c1e26b1e8279dd3913fea62da4ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791c1dfed45f39da7b241640ea3d01f9e917b5afe448f73afa7370601fa71fa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f03c28050e0b54f4bb1f8e99538edf26948ee1daead74611520521f03728b45(
    value: typing.Optional[RepositorySecurityAndAnalysisSecretScanning],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2083f15b0562ff12040b1799f97bbd932e55702e421029024331fc7942af64dd(
    *,
    status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d157ba43406867df49b7a925d14bddf1aed84ad4a42e220967b9cae1c385f02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eef98dcb428f4e572cc2504d76a0d7a8c3503f232dccdea1ec78e0fdb39680f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4263c524d3a85aeb56e25964732727aa16cc0bc3b9c5e152f451d90ad87d769c(
    value: typing.Optional[RepositorySecurityAndAnalysisSecretScanningPushProtection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc62e7345a0e9e923f09ce69faaa43213f8a732c86f9d3dbd62c00a22c04ee1(
    *,
    owner: builtins.str,
    repository: builtins.str,
    include_all_branches: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21abaa3f03ff88ecf69810b2eb33a1b7da79581edecc0f2ef1add2deb0f9b65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975360c89abc404aeb04a16ba3afd1b1aaa26d8a098276e031b5971f1343c737(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f8ecbb952e1f806294852fbf6e7a8aa667a1420cb688d796d251223f9958ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c6af51a941a35e73f6f1c762f0a5e9135566c6d3ad6b39ad8730ca9310c600(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88636d4721259dfd00b20d1e0912f71f22cff229ac84c2c58f0d2c6aabb41acb(
    value: typing.Optional[RepositoryTemplate],
) -> None:
    """Type checking stubs"""
    pass
