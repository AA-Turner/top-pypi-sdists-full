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

import constructs as _constructs_77d1e7e8
from .. import (
    Component as _Component_2b0ad27f,
    GroupRunnerOptions as _GroupRunnerOptions_148c59c1,
    Project as _Project_57d89203,
    ReleasableCommits as _ReleasableCommits_d481ce10,
    Task as _Task_9fa875b6,
)
from ..github.workflows import (
    Job as _Job_20ffcf45,
    JobPermissions as _JobPermissions_3b5b53dc,
    JobStep as _JobStep_c3287c05,
    Tools as _Tools_75b93a2a,
)


@jsii.data_type(
    jsii_type="projen.release.BranchOptions",
    jsii_struct_bases=[],
    name_mapping={
        "major_version": "majorVersion",
        "min_major_version": "minMajorVersion",
        "minor_version": "minorVersion",
        "npm_dist_tag": "npmDistTag",
        "prerelease": "prerelease",
        "tag_prefix": "tagPrefix",
        "workflow_name": "workflowName",
    },
)
class BranchOptions:
    def __init__(
        self,
        *,
        major_version: jsii.Number,
        min_major_version: typing.Optional[jsii.Number] = None,
        minor_version: typing.Optional[jsii.Number] = None,
        npm_dist_tag: typing.Optional[builtins.str] = None,
        prerelease: typing.Optional[builtins.str] = None,
        tag_prefix: typing.Optional[builtins.str] = None,
        workflow_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for a release branch.

        :param major_version: (experimental) The major versions released from this branch.
        :param min_major_version: (experimental) The minimum major version to release.
        :param minor_version: (experimental) The minor versions released from this branch.
        :param npm_dist_tag: (experimental) The npm distribution tag to use for this branch. Default: "latest"
        :param prerelease: (experimental) Bump the version as a pre-release tag. Default: - normal releases
        :param tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: - no prefix
        :param workflow_name: (experimental) The name of the release workflow. Default: "release-BRANCH"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f62eb98000deee3820f046309b2262c5063c0cb9581232fd1a44731f86986d7)
            check_type(argname="argument major_version", value=major_version, expected_type=type_hints["major_version"])
            check_type(argname="argument min_major_version", value=min_major_version, expected_type=type_hints["min_major_version"])
            check_type(argname="argument minor_version", value=minor_version, expected_type=type_hints["minor_version"])
            check_type(argname="argument npm_dist_tag", value=npm_dist_tag, expected_type=type_hints["npm_dist_tag"])
            check_type(argname="argument prerelease", value=prerelease, expected_type=type_hints["prerelease"])
            check_type(argname="argument tag_prefix", value=tag_prefix, expected_type=type_hints["tag_prefix"])
            check_type(argname="argument workflow_name", value=workflow_name, expected_type=type_hints["workflow_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "major_version": major_version,
        }
        if min_major_version is not None:
            self._values["min_major_version"] = min_major_version
        if minor_version is not None:
            self._values["minor_version"] = minor_version
        if npm_dist_tag is not None:
            self._values["npm_dist_tag"] = npm_dist_tag
        if prerelease is not None:
            self._values["prerelease"] = prerelease
        if tag_prefix is not None:
            self._values["tag_prefix"] = tag_prefix
        if workflow_name is not None:
            self._values["workflow_name"] = workflow_name

    @builtins.property
    def major_version(self) -> jsii.Number:
        '''(experimental) The major versions released from this branch.

        :stability: experimental
        '''
        result = self._values.get("major_version")
        assert result is not None, "Required property 'major_version' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum major version to release.

        :stability: experimental
        '''
        result = self._values.get("min_major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minor_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minor versions released from this branch.

        :stability: experimental
        '''
        result = self._values.get("minor_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def npm_dist_tag(self) -> typing.Optional[builtins.str]:
        '''(experimental) The npm distribution tag to use for this branch.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("npm_dist_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prerelease(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bump the version as a pre-release tag.

        :default: - normal releases

        :stability: experimental
        '''
        result = self._values.get("prerelease")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers.

        Note: this prefix is used to detect the latest tagged version
        when bumping, so if you change this on a project with an existing version
        history, you may need to manually tag your latest release
        with the new prefix.

        :default: - no prefix

        :stability: experimental
        '''
        result = self._values.get("tag_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the release workflow.

        :default: "release-BRANCH"

        :stability: experimental
        '''
        result = self._values.get("workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.release.CodeArtifactAuthProvider")
class CodeArtifactAuthProvider(enum.Enum):
    '''(experimental) Options for authorizing requests to a AWS CodeArtifact npm repository.

    :stability: experimental
    '''

    ACCESS_AND_SECRET_KEY_PAIR = "ACCESS_AND_SECRET_KEY_PAIR"
    '''(experimental) Fixed credentials provided via Github secrets.

    :stability: experimental
    '''
    GITHUB_OIDC = "GITHUB_OIDC"
    '''(experimental) Ephemeral credentials provided via Github's OIDC integration with an IAM role.

    See:
    https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html
    https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.release.CodeArtifactOptions",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id_secret": "accessKeyIdSecret",
        "auth_provider": "authProvider",
        "role_to_assume": "roleToAssume",
        "secret_access_key_secret": "secretAccessKeySecret",
    },
)
class CodeArtifactOptions:
    def __init__(
        self,
        *,
        access_key_id_secret: typing.Optional[builtins.str] = None,
        auth_provider: typing.Optional[CodeArtifactAuthProvider] = None,
        role_to_assume: typing.Optional[builtins.str] = None,
        secret_access_key_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for publishing packages to AWS CodeArtifact.

        :param access_key_id_secret: (experimental) GitHub secret which contains the AWS access key ID to use when publishing packages to AWS CodeArtifact. This property must be specified only when publishing to AWS CodeArtifact (``npmRegistryUrl`` contains AWS CodeArtifact URL). Default: - When the ``authProvider`` value is set to ``CodeArtifactAuthProvider.ACCESS_AND_SECRET_KEY_PAIR``, the default is "AWS_ACCESS_KEY_ID". For ``CodeArtifactAuthProvider.GITHUB_OIDC``, this value must be left undefined.
        :param auth_provider: (experimental) Provider to use for authorizing requests to AWS CodeArtifact. Default: CodeArtifactAuthProvider.ACCESS_AND_SECRET_KEY_PAIR
        :param role_to_assume: (experimental) ARN of AWS role to be assumed prior to get authorization token from AWS CodeArtifact This property must be specified only when publishing to AWS CodeArtifact (``registry`` contains AWS CodeArtifact URL). When using the ``CodeArtifactAuthProvider.GITHUB_OIDC`` auth provider, this value must be defined. Default: undefined
        :param secret_access_key_secret: (experimental) GitHub secret which contains the AWS secret access key to use when publishing packages to AWS CodeArtifact. This property must be specified only when publishing to AWS CodeArtifact (``npmRegistryUrl`` contains AWS CodeArtifact URL). Default: - When the ``authProvider`` value is set to ``CodeArtifactAuthProvider.ACCESS_AND_SECRET_KEY_PAIR``, the default is "AWS_SECRET_ACCESS_KEY". For ``CodeArtifactAuthProvider.GITHUB_OIDC``, this value must be left undefined.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a328fe64db40633fedae889a7376e6885e1983f57d171d4f4ef85af668fafdb)
            check_type(argname="argument access_key_id_secret", value=access_key_id_secret, expected_type=type_hints["access_key_id_secret"])
            check_type(argname="argument auth_provider", value=auth_provider, expected_type=type_hints["auth_provider"])
            check_type(argname="argument role_to_assume", value=role_to_assume, expected_type=type_hints["role_to_assume"])
            check_type(argname="argument secret_access_key_secret", value=secret_access_key_secret, expected_type=type_hints["secret_access_key_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key_id_secret is not None:
            self._values["access_key_id_secret"] = access_key_id_secret
        if auth_provider is not None:
            self._values["auth_provider"] = auth_provider
        if role_to_assume is not None:
            self._values["role_to_assume"] = role_to_assume
        if secret_access_key_secret is not None:
            self._values["secret_access_key_secret"] = secret_access_key_secret

    @builtins.property
    def access_key_id_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the AWS access key ID to use when publishing packages to AWS CodeArtifact.

        This property must be specified only when publishing to AWS CodeArtifact (``npmRegistryUrl`` contains AWS CodeArtifact URL).

        :default:

        - When the ``authProvider`` value is set to
        ``CodeArtifactAuthProvider.ACCESS_AND_SECRET_KEY_PAIR``, the default is
        "AWS_ACCESS_KEY_ID". For ``CodeArtifactAuthProvider.GITHUB_OIDC``, this
        value must be left undefined.

        :stability: experimental
        '''
        result = self._values.get("access_key_id_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_provider(self) -> typing.Optional[CodeArtifactAuthProvider]:
        '''(experimental) Provider to use for authorizing requests to AWS CodeArtifact.

        :default: CodeArtifactAuthProvider.ACCESS_AND_SECRET_KEY_PAIR

        :stability: experimental
        '''
        result = self._values.get("auth_provider")
        return typing.cast(typing.Optional[CodeArtifactAuthProvider], result)

    @builtins.property
    def role_to_assume(self) -> typing.Optional[builtins.str]:
        '''(experimental) ARN of AWS role to be assumed prior to get authorization token from AWS CodeArtifact This property must be specified only when publishing to AWS CodeArtifact (``registry`` contains AWS CodeArtifact URL).

        When using the ``CodeArtifactAuthProvider.GITHUB_OIDC`` auth provider, this value must be defined.

        :default: undefined

        :stability: experimental
        '''
        result = self._values.get("role_to_assume")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_access_key_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the AWS secret access key to use when publishing packages to AWS CodeArtifact.

        This property must be specified only when publishing to AWS CodeArtifact (``npmRegistryUrl`` contains AWS CodeArtifact URL).

        :default:

        - When the ``authProvider`` value is set to
        ``CodeArtifactAuthProvider.ACCESS_AND_SECRET_KEY_PAIR``, the default is
        "AWS_SECRET_ACCESS_KEY". For ``CodeArtifactAuthProvider.GITHUB_OIDC``, this
        value must be left undefined.

        :stability: experimental
        '''
        result = self._values.get("secret_access_key_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeArtifactOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.CommonPublishOptions",
    jsii_struct_bases=[],
    name_mapping={
        "post_publish_steps": "postPublishSteps",
        "pre_publish_steps": "prePublishSteps",
        "publish_tools": "publishTools",
    },
)
class CommonPublishOptions:
    def __init__(
        self,
        *,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Common publishing options.

        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed

        :stability: experimental
        '''
        if isinstance(publish_tools, dict):
            publish_tools = _Tools_75b93a2a(**publish_tools)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9603f09b67279d5ef3dc921367168d873983210161b1d6382c369d0b9ec13b0a)
            check_type(argname="argument post_publish_steps", value=post_publish_steps, expected_type=type_hints["post_publish_steps"])
            check_type(argname="argument pre_publish_steps", value=pre_publish_steps, expected_type=type_hints["pre_publish_steps"])
            check_type(argname="argument publish_tools", value=publish_tools, expected_type=type_hints["publish_tools"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_publish_steps is not None:
            self._values["post_publish_steps"] = post_publish_steps
        if pre_publish_steps is not None:
            self._values["pre_publish_steps"] = pre_publish_steps
        if publish_tools is not None:
            self._values["publish_tools"] = publish_tools

    @builtins.property
    def post_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after executing the publishing command.

        These can be used
        to add/update the release artifacts ot any other tasks needed.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("post_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def pre_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed.

        These steps are executed after ``dist/`` has been populated with the build
        output.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("pre_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def publish_tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Additional tools to install in the publishing job.

        :default: - no additional tools are installed

        :stability: experimental
        '''
        result = self._values.get("publish_tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonPublishOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.ContinuousReleaseOptions",
    jsii_struct_bases=[],
    name_mapping={"paths": "paths"},
)
class ContinuousReleaseOptions:
    def __init__(
        self,
        *,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param paths: (experimental) Paths for which pushes should trigger a release.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b36779f92c5190c3ac9d8a636a537bfe6ebc844a55942ee5dfc0a9656d6192)
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if paths is not None:
            self._values["paths"] = paths

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Paths for which pushes should trigger a release.

        :stability: experimental
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContinuousReleaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.GitHubReleasesPublishOptions",
    jsii_struct_bases=[CommonPublishOptions],
    name_mapping={
        "post_publish_steps": "postPublishSteps",
        "pre_publish_steps": "prePublishSteps",
        "publish_tools": "publishTools",
        "changelog_file": "changelogFile",
        "release_tag_file": "releaseTagFile",
        "version_file": "versionFile",
    },
)
class GitHubReleasesPublishOptions(CommonPublishOptions):
    def __init__(
        self,
        *,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
        changelog_file: builtins.str,
        release_tag_file: builtins.str,
        version_file: builtins.str,
    ) -> None:
        '''(experimental) Publishing options for GitHub releases.

        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed
        :param changelog_file: (experimental) The location of an .md file (relative to ``dist/``) that includes the changelog for the release.
        :param release_tag_file: (experimental) The location of a text file (relative to ``dist/``) that contains the release tag.
        :param version_file: (experimental) The location of a text file (relative to ``dist/``) that contains the version number.

        :stability: experimental
        '''
        if isinstance(publish_tools, dict):
            publish_tools = _Tools_75b93a2a(**publish_tools)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7008ba35b00dedc375d87db7a317e8f077475b6a4e334303337c92bb77171fb)
            check_type(argname="argument post_publish_steps", value=post_publish_steps, expected_type=type_hints["post_publish_steps"])
            check_type(argname="argument pre_publish_steps", value=pre_publish_steps, expected_type=type_hints["pre_publish_steps"])
            check_type(argname="argument publish_tools", value=publish_tools, expected_type=type_hints["publish_tools"])
            check_type(argname="argument changelog_file", value=changelog_file, expected_type=type_hints["changelog_file"])
            check_type(argname="argument release_tag_file", value=release_tag_file, expected_type=type_hints["release_tag_file"])
            check_type(argname="argument version_file", value=version_file, expected_type=type_hints["version_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "changelog_file": changelog_file,
            "release_tag_file": release_tag_file,
            "version_file": version_file,
        }
        if post_publish_steps is not None:
            self._values["post_publish_steps"] = post_publish_steps
        if pre_publish_steps is not None:
            self._values["pre_publish_steps"] = pre_publish_steps
        if publish_tools is not None:
            self._values["publish_tools"] = publish_tools

    @builtins.property
    def post_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after executing the publishing command.

        These can be used
        to add/update the release artifacts ot any other tasks needed.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("post_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def pre_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed.

        These steps are executed after ``dist/`` has been populated with the build
        output.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("pre_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def publish_tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Additional tools to install in the publishing job.

        :default: - no additional tools are installed

        :stability: experimental
        '''
        result = self._values.get("publish_tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    @builtins.property
    def changelog_file(self) -> builtins.str:
        '''(experimental) The location of an .md file (relative to ``dist/``) that includes the changelog for the release.

        :stability: experimental

        Example::

            changelog.md
        '''
        result = self._values.get("changelog_file")
        assert result is not None, "Required property 'changelog_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def release_tag_file(self) -> builtins.str:
        '''(experimental) The location of a text file (relative to ``dist/``) that contains the release tag.

        :stability: experimental

        Example::

            releasetag.txt
        '''
        result = self._values.get("release_tag_file")
        assert result is not None, "Required property 'release_tag_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_file(self) -> builtins.str:
        '''(experimental) The location of a text file (relative to ``dist/``) that contains the version number.

        :stability: experimental

        Example::

            version.txt
        '''
        result = self._values.get("version_file")
        assert result is not None, "Required property 'version_file' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubReleasesPublishOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.GitPublishOptions",
    jsii_struct_bases=[],
    name_mapping={
        "changelog_file": "changelogFile",
        "release_tag_file": "releaseTagFile",
        "version_file": "versionFile",
        "git_branch": "gitBranch",
        "git_push_command": "gitPushCommand",
        "project_changelog_file": "projectChangelogFile",
    },
)
class GitPublishOptions:
    def __init__(
        self,
        *,
        changelog_file: builtins.str,
        release_tag_file: builtins.str,
        version_file: builtins.str,
        git_branch: typing.Optional[builtins.str] = None,
        git_push_command: typing.Optional[builtins.str] = None,
        project_changelog_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Publishing options for Git releases.

        :param changelog_file: (experimental) The location of an .md file (relative to ``dist/``) that includes the changelog for the release.
        :param release_tag_file: (experimental) The location of a text file (relative to ``dist/``) that contains the release tag.
        :param version_file: (experimental) The location of a text file (relative to ``dist/``) that contains the version number.
        :param git_branch: (experimental) Branch to push to. Default: "main"
        :param git_push_command: (experimental) Override git-push command. Set to an empty string to disable pushing.
        :param project_changelog_file: (experimental) The location of an .md file that includes the project-level changelog.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5537e1435c9eea568279fa140de950e1b7275db307b374195986186386d7704)
            check_type(argname="argument changelog_file", value=changelog_file, expected_type=type_hints["changelog_file"])
            check_type(argname="argument release_tag_file", value=release_tag_file, expected_type=type_hints["release_tag_file"])
            check_type(argname="argument version_file", value=version_file, expected_type=type_hints["version_file"])
            check_type(argname="argument git_branch", value=git_branch, expected_type=type_hints["git_branch"])
            check_type(argname="argument git_push_command", value=git_push_command, expected_type=type_hints["git_push_command"])
            check_type(argname="argument project_changelog_file", value=project_changelog_file, expected_type=type_hints["project_changelog_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "changelog_file": changelog_file,
            "release_tag_file": release_tag_file,
            "version_file": version_file,
        }
        if git_branch is not None:
            self._values["git_branch"] = git_branch
        if git_push_command is not None:
            self._values["git_push_command"] = git_push_command
        if project_changelog_file is not None:
            self._values["project_changelog_file"] = project_changelog_file

    @builtins.property
    def changelog_file(self) -> builtins.str:
        '''(experimental) The location of an .md file (relative to ``dist/``) that includes the changelog for the release.

        :stability: experimental

        Example::

            changelog.md
        '''
        result = self._values.get("changelog_file")
        assert result is not None, "Required property 'changelog_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def release_tag_file(self) -> builtins.str:
        '''(experimental) The location of a text file (relative to ``dist/``) that contains the release tag.

        :stability: experimental

        Example::

            releasetag.txt
        '''
        result = self._values.get("release_tag_file")
        assert result is not None, "Required property 'release_tag_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_file(self) -> builtins.str:
        '''(experimental) The location of a text file (relative to ``dist/``) that contains the version number.

        :stability: experimental

        Example::

            version.txt
        '''
        result = self._values.get("version_file")
        assert result is not None, "Required property 'version_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def git_branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) Branch to push to.

        :default: "main"

        :stability: experimental
        '''
        result = self._values.get("git_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_push_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) Override git-push command.

        Set to an empty string to disable pushing.

        :stability: experimental
        '''
        result = self._values.get("git_push_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_changelog_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) The location of an .md file that includes the project-level changelog.

        :stability: experimental
        '''
        result = self._values.get("project_changelog_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitPublishOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.GoPublishOptions",
    jsii_struct_bases=[CommonPublishOptions],
    name_mapping={
        "post_publish_steps": "postPublishSteps",
        "pre_publish_steps": "prePublishSteps",
        "publish_tools": "publishTools",
        "git_branch": "gitBranch",
        "git_commit_message": "gitCommitMessage",
        "github_deploy_key_secret": "githubDeployKeySecret",
        "github_token_secret": "githubTokenSecret",
        "github_use_ssh": "githubUseSsh",
        "git_user_email": "gitUserEmail",
        "git_user_name": "gitUserName",
    },
)
class GoPublishOptions(CommonPublishOptions):
    def __init__(
        self,
        *,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
        git_branch: typing.Optional[builtins.str] = None,
        git_commit_message: typing.Optional[builtins.str] = None,
        github_deploy_key_secret: typing.Optional[builtins.str] = None,
        github_token_secret: typing.Optional[builtins.str] = None,
        github_use_ssh: typing.Optional[builtins.bool] = None,
        git_user_email: typing.Optional[builtins.str] = None,
        git_user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for Go releases.

        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed
        :param git_branch: (experimental) Branch to push to. Default: "main"
        :param git_commit_message: (experimental) The commit message. Default: "chore(release): $VERSION"
        :param github_deploy_key_secret: (experimental) The name of the secret that includes a GitHub deploy key used to push to the GitHub repository. Ignored if ``githubUseSsh`` is ``false``. Default: "GO_GITHUB_DEPLOY_KEY"
        :param github_token_secret: (experimental) The name of the secret that includes a personal GitHub access token used to push to the GitHub repository. Ignored if ``githubUseSsh`` is ``true``. Default: "GO_GITHUB_TOKEN"
        :param github_use_ssh: (experimental) Use SSH to push to GitHub instead of a personal accses token. Default: false
        :param git_user_email: (experimental) The email to use in the release git commit. Default: "github-actions@github.com"
        :param git_user_name: (experimental) The user name to use for the release git commit. Default: "github-actions"

        :stability: experimental
        '''
        if isinstance(publish_tools, dict):
            publish_tools = _Tools_75b93a2a(**publish_tools)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a5b8a4f17bcea99089b42477d5b778fd3a9066d3d1126736ccf21a9c44bfbc)
            check_type(argname="argument post_publish_steps", value=post_publish_steps, expected_type=type_hints["post_publish_steps"])
            check_type(argname="argument pre_publish_steps", value=pre_publish_steps, expected_type=type_hints["pre_publish_steps"])
            check_type(argname="argument publish_tools", value=publish_tools, expected_type=type_hints["publish_tools"])
            check_type(argname="argument git_branch", value=git_branch, expected_type=type_hints["git_branch"])
            check_type(argname="argument git_commit_message", value=git_commit_message, expected_type=type_hints["git_commit_message"])
            check_type(argname="argument github_deploy_key_secret", value=github_deploy_key_secret, expected_type=type_hints["github_deploy_key_secret"])
            check_type(argname="argument github_token_secret", value=github_token_secret, expected_type=type_hints["github_token_secret"])
            check_type(argname="argument github_use_ssh", value=github_use_ssh, expected_type=type_hints["github_use_ssh"])
            check_type(argname="argument git_user_email", value=git_user_email, expected_type=type_hints["git_user_email"])
            check_type(argname="argument git_user_name", value=git_user_name, expected_type=type_hints["git_user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_publish_steps is not None:
            self._values["post_publish_steps"] = post_publish_steps
        if pre_publish_steps is not None:
            self._values["pre_publish_steps"] = pre_publish_steps
        if publish_tools is not None:
            self._values["publish_tools"] = publish_tools
        if git_branch is not None:
            self._values["git_branch"] = git_branch
        if git_commit_message is not None:
            self._values["git_commit_message"] = git_commit_message
        if github_deploy_key_secret is not None:
            self._values["github_deploy_key_secret"] = github_deploy_key_secret
        if github_token_secret is not None:
            self._values["github_token_secret"] = github_token_secret
        if github_use_ssh is not None:
            self._values["github_use_ssh"] = github_use_ssh
        if git_user_email is not None:
            self._values["git_user_email"] = git_user_email
        if git_user_name is not None:
            self._values["git_user_name"] = git_user_name

    @builtins.property
    def post_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after executing the publishing command.

        These can be used
        to add/update the release artifacts ot any other tasks needed.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("post_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def pre_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed.

        These steps are executed after ``dist/`` has been populated with the build
        output.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("pre_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def publish_tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Additional tools to install in the publishing job.

        :default: - no additional tools are installed

        :stability: experimental
        '''
        result = self._values.get("publish_tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    @builtins.property
    def git_branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) Branch to push to.

        :default: "main"

        :stability: experimental
        '''
        result = self._values.get("git_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_commit_message(self) -> typing.Optional[builtins.str]:
        '''(experimental) The commit message.

        :default: "chore(release): $VERSION"

        :stability: experimental
        '''
        result = self._values.get("git_commit_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_deploy_key_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the secret that includes a GitHub deploy key used to push to the GitHub repository.

        Ignored if ``githubUseSsh`` is ``false``.

        :default: "GO_GITHUB_DEPLOY_KEY"

        :stability: experimental
        '''
        result = self._values.get("github_deploy_key_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the secret that includes a personal GitHub access token used to push to the GitHub repository.

        Ignored if ``githubUseSsh`` is ``true``.

        :default: "GO_GITHUB_TOKEN"

        :stability: experimental
        '''
        result = self._values.get("github_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_use_ssh(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use SSH to push to GitHub instead of a personal accses token.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("github_use_ssh")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def git_user_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) The email to use in the release git commit.

        :default: "github-actions@github.com"

        :stability: experimental
        '''
        result = self._values.get("git_user_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_user_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user name to use for the release git commit.

        :default: "github-actions"

        :stability: experimental
        '''
        result = self._values.get("git_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoPublishOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.JsiiReleaseGo",
    jsii_struct_bases=[GoPublishOptions],
    name_mapping={
        "post_publish_steps": "postPublishSteps",
        "pre_publish_steps": "prePublishSteps",
        "publish_tools": "publishTools",
        "git_branch": "gitBranch",
        "git_commit_message": "gitCommitMessage",
        "github_deploy_key_secret": "githubDeployKeySecret",
        "github_token_secret": "githubTokenSecret",
        "github_use_ssh": "githubUseSsh",
        "git_user_email": "gitUserEmail",
        "git_user_name": "gitUserName",
    },
)
class JsiiReleaseGo(GoPublishOptions):
    def __init__(
        self,
        *,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
        git_branch: typing.Optional[builtins.str] = None,
        git_commit_message: typing.Optional[builtins.str] = None,
        github_deploy_key_secret: typing.Optional[builtins.str] = None,
        github_token_secret: typing.Optional[builtins.str] = None,
        github_use_ssh: typing.Optional[builtins.bool] = None,
        git_user_email: typing.Optional[builtins.str] = None,
        git_user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed
        :param git_branch: (experimental) Branch to push to. Default: "main"
        :param git_commit_message: (experimental) The commit message. Default: "chore(release): $VERSION"
        :param github_deploy_key_secret: (experimental) The name of the secret that includes a GitHub deploy key used to push to the GitHub repository. Ignored if ``githubUseSsh`` is ``false``. Default: "GO_GITHUB_DEPLOY_KEY"
        :param github_token_secret: (experimental) The name of the secret that includes a personal GitHub access token used to push to the GitHub repository. Ignored if ``githubUseSsh`` is ``true``. Default: "GO_GITHUB_TOKEN"
        :param github_use_ssh: (experimental) Use SSH to push to GitHub instead of a personal accses token. Default: false
        :param git_user_email: (experimental) The email to use in the release git commit. Default: "github-actions@github.com"
        :param git_user_name: (experimental) The user name to use for the release git commit. Default: "github-actions"

        :deprecated: Use ``GoPublishOptions`` instead.

        :stability: deprecated
        '''
        if isinstance(publish_tools, dict):
            publish_tools = _Tools_75b93a2a(**publish_tools)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44bae65cd3313afa37ada6dbaab99141ff7744458e985bc9c53faa021220e167)
            check_type(argname="argument post_publish_steps", value=post_publish_steps, expected_type=type_hints["post_publish_steps"])
            check_type(argname="argument pre_publish_steps", value=pre_publish_steps, expected_type=type_hints["pre_publish_steps"])
            check_type(argname="argument publish_tools", value=publish_tools, expected_type=type_hints["publish_tools"])
            check_type(argname="argument git_branch", value=git_branch, expected_type=type_hints["git_branch"])
            check_type(argname="argument git_commit_message", value=git_commit_message, expected_type=type_hints["git_commit_message"])
            check_type(argname="argument github_deploy_key_secret", value=github_deploy_key_secret, expected_type=type_hints["github_deploy_key_secret"])
            check_type(argname="argument github_token_secret", value=github_token_secret, expected_type=type_hints["github_token_secret"])
            check_type(argname="argument github_use_ssh", value=github_use_ssh, expected_type=type_hints["github_use_ssh"])
            check_type(argname="argument git_user_email", value=git_user_email, expected_type=type_hints["git_user_email"])
            check_type(argname="argument git_user_name", value=git_user_name, expected_type=type_hints["git_user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_publish_steps is not None:
            self._values["post_publish_steps"] = post_publish_steps
        if pre_publish_steps is not None:
            self._values["pre_publish_steps"] = pre_publish_steps
        if publish_tools is not None:
            self._values["publish_tools"] = publish_tools
        if git_branch is not None:
            self._values["git_branch"] = git_branch
        if git_commit_message is not None:
            self._values["git_commit_message"] = git_commit_message
        if github_deploy_key_secret is not None:
            self._values["github_deploy_key_secret"] = github_deploy_key_secret
        if github_token_secret is not None:
            self._values["github_token_secret"] = github_token_secret
        if github_use_ssh is not None:
            self._values["github_use_ssh"] = github_use_ssh
        if git_user_email is not None:
            self._values["git_user_email"] = git_user_email
        if git_user_name is not None:
            self._values["git_user_name"] = git_user_name

    @builtins.property
    def post_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after executing the publishing command.

        These can be used
        to add/update the release artifacts ot any other tasks needed.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("post_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def pre_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed.

        These steps are executed after ``dist/`` has been populated with the build
        output.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("pre_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def publish_tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Additional tools to install in the publishing job.

        :default: - no additional tools are installed

        :stability: experimental
        '''
        result = self._values.get("publish_tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    @builtins.property
    def git_branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) Branch to push to.

        :default: "main"

        :stability: experimental
        '''
        result = self._values.get("git_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_commit_message(self) -> typing.Optional[builtins.str]:
        '''(experimental) The commit message.

        :default: "chore(release): $VERSION"

        :stability: experimental
        '''
        result = self._values.get("git_commit_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_deploy_key_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the secret that includes a GitHub deploy key used to push to the GitHub repository.

        Ignored if ``githubUseSsh`` is ``false``.

        :default: "GO_GITHUB_DEPLOY_KEY"

        :stability: experimental
        '''
        result = self._values.get("github_deploy_key_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the secret that includes a personal GitHub access token used to push to the GitHub repository.

        Ignored if ``githubUseSsh`` is ``true``.

        :default: "GO_GITHUB_TOKEN"

        :stability: experimental
        '''
        result = self._values.get("github_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_use_ssh(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use SSH to push to GitHub instead of a personal accses token.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("github_use_ssh")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def git_user_email(self) -> typing.Optional[builtins.str]:
        '''(experimental) The email to use in the release git commit.

        :default: "github-actions@github.com"

        :stability: experimental
        '''
        result = self._values.get("git_user_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_user_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user name to use for the release git commit.

        :default: "github-actions"

        :stability: experimental
        '''
        result = self._values.get("git_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsiiReleaseGo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.ManualReleaseOptions",
    jsii_struct_bases=[],
    name_mapping={
        "changelog": "changelog",
        "changelog_path": "changelogPath",
        "git_push_command": "gitPushCommand",
    },
)
class ManualReleaseOptions:
    def __init__(
        self,
        *,
        changelog: typing.Optional[builtins.bool] = None,
        changelog_path: typing.Optional[builtins.str] = None,
        git_push_command: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param changelog: (experimental) Maintain a project-level changelog. Default: true
        :param changelog_path: (experimental) Project-level changelog file path. Ignored if ``changelog`` is false. Default: 'CHANGELOG.md'
        :param git_push_command: (experimental) Override git-push command. Set to an empty string to disable pushing.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2492d83058b766179e85fd785d08928e38b53ce70b0f2dc9a1c5edccb668b930)
            check_type(argname="argument changelog", value=changelog, expected_type=type_hints["changelog"])
            check_type(argname="argument changelog_path", value=changelog_path, expected_type=type_hints["changelog_path"])
            check_type(argname="argument git_push_command", value=git_push_command, expected_type=type_hints["git_push_command"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if changelog is not None:
            self._values["changelog"] = changelog
        if changelog_path is not None:
            self._values["changelog_path"] = changelog_path
        if git_push_command is not None:
            self._values["git_push_command"] = git_push_command

    @builtins.property
    def changelog(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Maintain a project-level changelog.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("changelog")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def changelog_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Project-level changelog file path.

        Ignored if ``changelog`` is false.

        :default: 'CHANGELOG.md'

        :stability: experimental
        '''
        result = self._values.get("changelog_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_push_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) Override git-push command.

        Set to an empty string to disable pushing.

        :stability: experimental
        '''
        result = self._values.get("git_push_command")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManualReleaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.MavenPublishOptions",
    jsii_struct_bases=[CommonPublishOptions],
    name_mapping={
        "post_publish_steps": "postPublishSteps",
        "pre_publish_steps": "prePublishSteps",
        "publish_tools": "publishTools",
        "maven_endpoint": "mavenEndpoint",
        "maven_gpg_private_key_passphrase": "mavenGpgPrivateKeyPassphrase",
        "maven_gpg_private_key_secret": "mavenGpgPrivateKeySecret",
        "maven_password": "mavenPassword",
        "maven_repository_url": "mavenRepositoryUrl",
        "maven_server_id": "mavenServerId",
        "maven_staging_profile_id": "mavenStagingProfileId",
        "maven_username": "mavenUsername",
    },
)
class MavenPublishOptions(CommonPublishOptions):
    def __init__(
        self,
        *,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
        maven_endpoint: typing.Optional[builtins.str] = None,
        maven_gpg_private_key_passphrase: typing.Optional[builtins.str] = None,
        maven_gpg_private_key_secret: typing.Optional[builtins.str] = None,
        maven_password: typing.Optional[builtins.str] = None,
        maven_repository_url: typing.Optional[builtins.str] = None,
        maven_server_id: typing.Optional[builtins.str] = None,
        maven_staging_profile_id: typing.Optional[builtins.str] = None,
        maven_username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for Maven releases.

        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed
        :param maven_endpoint: (experimental) URL of Nexus repository. if not set, defaults to https://oss.sonatype.org Default: "https://oss.sonatype.org"
        :param maven_gpg_private_key_passphrase: (experimental) GitHub secret name which contains the GPG private key or file that includes it. This is used to sign your Maven packages. See instructions. Default: "MAVEN_GPG_PRIVATE_KEY_PASSPHRASE" or not set when using GitHub Packages
        :param maven_gpg_private_key_secret: (experimental) GitHub secret name which contains the GPG private key or file that includes it. This is used to sign your Maven packages. See instructions. Default: "MAVEN_GPG_PRIVATE_KEY" or not set when using GitHub Packages
        :param maven_password: (experimental) GitHub secret name which contains the Password for maven repository. For Maven Central, you will need to Create JIRA account and then request a new project (see links). Default: "MAVEN_PASSWORD" or "GITHUB_TOKEN" when using GitHub Packages
        :param maven_repository_url: (experimental) Deployment repository when not deploying to Maven Central. Default: - not set
        :param maven_server_id: (experimental) Used in maven settings for credential lookup (e.g. use github when publishing to GitHub). Default: "ossrh" (Maven Central) or "github" when using GitHub Packages
        :param maven_staging_profile_id: (experimental) GitHub secret name which contains the Maven Central (sonatype) staging profile ID (e.g. 68a05363083174). Staging profile ID can be found in the URL of the "Releases" staging profile under "Staging Profiles" in https://oss.sonatype.org (e.g. https://oss.sonatype.org/#stagingProfiles;11a33451234521). Default: "MAVEN_STAGING_PROFILE_ID" or not set when using GitHub Packages
        :param maven_username: (experimental) GitHub secret name which contains the Username for maven repository. For Maven Central, you will need to Create JIRA account and then request a new project (see links). Default: "MAVEN_USERNAME" or the GitHub Actor when using GitHub Packages

        :stability: experimental
        '''
        if isinstance(publish_tools, dict):
            publish_tools = _Tools_75b93a2a(**publish_tools)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da2d55bfa47dd9e6869b7f55b573dea54539ab2e9b833766e4140d6d4c4c3d7e)
            check_type(argname="argument post_publish_steps", value=post_publish_steps, expected_type=type_hints["post_publish_steps"])
            check_type(argname="argument pre_publish_steps", value=pre_publish_steps, expected_type=type_hints["pre_publish_steps"])
            check_type(argname="argument publish_tools", value=publish_tools, expected_type=type_hints["publish_tools"])
            check_type(argname="argument maven_endpoint", value=maven_endpoint, expected_type=type_hints["maven_endpoint"])
            check_type(argname="argument maven_gpg_private_key_passphrase", value=maven_gpg_private_key_passphrase, expected_type=type_hints["maven_gpg_private_key_passphrase"])
            check_type(argname="argument maven_gpg_private_key_secret", value=maven_gpg_private_key_secret, expected_type=type_hints["maven_gpg_private_key_secret"])
            check_type(argname="argument maven_password", value=maven_password, expected_type=type_hints["maven_password"])
            check_type(argname="argument maven_repository_url", value=maven_repository_url, expected_type=type_hints["maven_repository_url"])
            check_type(argname="argument maven_server_id", value=maven_server_id, expected_type=type_hints["maven_server_id"])
            check_type(argname="argument maven_staging_profile_id", value=maven_staging_profile_id, expected_type=type_hints["maven_staging_profile_id"])
            check_type(argname="argument maven_username", value=maven_username, expected_type=type_hints["maven_username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_publish_steps is not None:
            self._values["post_publish_steps"] = post_publish_steps
        if pre_publish_steps is not None:
            self._values["pre_publish_steps"] = pre_publish_steps
        if publish_tools is not None:
            self._values["publish_tools"] = publish_tools
        if maven_endpoint is not None:
            self._values["maven_endpoint"] = maven_endpoint
        if maven_gpg_private_key_passphrase is not None:
            self._values["maven_gpg_private_key_passphrase"] = maven_gpg_private_key_passphrase
        if maven_gpg_private_key_secret is not None:
            self._values["maven_gpg_private_key_secret"] = maven_gpg_private_key_secret
        if maven_password is not None:
            self._values["maven_password"] = maven_password
        if maven_repository_url is not None:
            self._values["maven_repository_url"] = maven_repository_url
        if maven_server_id is not None:
            self._values["maven_server_id"] = maven_server_id
        if maven_staging_profile_id is not None:
            self._values["maven_staging_profile_id"] = maven_staging_profile_id
        if maven_username is not None:
            self._values["maven_username"] = maven_username

    @builtins.property
    def post_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after executing the publishing command.

        These can be used
        to add/update the release artifacts ot any other tasks needed.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("post_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def pre_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed.

        These steps are executed after ``dist/`` has been populated with the build
        output.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("pre_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def publish_tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Additional tools to install in the publishing job.

        :default: - no additional tools are installed

        :stability: experimental
        '''
        result = self._values.get("publish_tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    @builtins.property
    def maven_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) URL of Nexus repository.

        if not set, defaults to https://oss.sonatype.org

        :default: "https://oss.sonatype.org"

        :stability: experimental
        '''
        result = self._values.get("maven_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_gpg_private_key_passphrase(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret name which contains the GPG private key or file that includes it.

        This is used to sign your Maven packages. See instructions.

        :default: "MAVEN_GPG_PRIVATE_KEY_PASSPHRASE" or not set when using GitHub Packages

        :see: https://github.com/aws/publib#maven
        :stability: experimental
        '''
        result = self._values.get("maven_gpg_private_key_passphrase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_gpg_private_key_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret name which contains the GPG private key or file that includes it.

        This is used to sign your Maven
        packages. See instructions.

        :default: "MAVEN_GPG_PRIVATE_KEY" or not set when using GitHub Packages

        :see: https://github.com/aws/publib#maven
        :stability: experimental
        '''
        result = self._values.get("maven_gpg_private_key_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_password(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret name which contains the Password for maven repository.

        For Maven Central, you will need to Create JIRA account and then request a
        new project (see links).

        :default: "MAVEN_PASSWORD" or "GITHUB_TOKEN" when using GitHub Packages

        :see: https://issues.sonatype.org/secure/CreateIssue.jspa?issuetype=21&pid=10134
        :stability: experimental
        '''
        result = self._values.get("maven_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_repository_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Deployment repository when not deploying to Maven Central.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("maven_repository_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_server_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Used in maven settings for credential lookup (e.g. use github when publishing to GitHub).

        :default: "ossrh" (Maven Central) or "github" when using GitHub Packages

        :stability: experimental
        '''
        result = self._values.get("maven_server_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_staging_profile_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret name which contains the Maven Central (sonatype) staging profile ID (e.g. 68a05363083174). Staging profile ID can be found in the URL of the "Releases" staging profile under "Staging Profiles" in https://oss.sonatype.org (e.g. https://oss.sonatype.org/#stagingProfiles;11a33451234521).

        :default: "MAVEN_STAGING_PROFILE_ID" or not set when using GitHub Packages

        :stability: experimental
        '''
        result = self._values.get("maven_staging_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_username(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret name which contains the Username for maven repository.

        For Maven Central, you will need to Create JIRA account and then request a
        new project (see links).

        :default: "MAVEN_USERNAME" or the GitHub Actor when using GitHub Packages

        :see: https://issues.sonatype.org/secure/CreateIssue.jspa?issuetype=21&pid=10134
        :stability: experimental
        '''
        result = self._values.get("maven_username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MavenPublishOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.NpmPublishOptions",
    jsii_struct_bases=[CommonPublishOptions],
    name_mapping={
        "post_publish_steps": "postPublishSteps",
        "pre_publish_steps": "prePublishSteps",
        "publish_tools": "publishTools",
        "code_artifact_options": "codeArtifactOptions",
        "dist_tag": "distTag",
        "npm_provenance": "npmProvenance",
        "npm_token_secret": "npmTokenSecret",
        "registry": "registry",
    },
)
class NpmPublishOptions(CommonPublishOptions):
    def __init__(
        self,
        *,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
        code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        dist_tag: typing.Optional[builtins.str] = None,
        npm_provenance: typing.Optional[builtins.bool] = None,
        npm_token_secret: typing.Optional[builtins.str] = None,
        registry: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for npm release.

        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed
        :param code_artifact_options: (experimental) Options for publishing npm package to AWS CodeArtifact. Default: - undefined
        :param dist_tag: (deprecated) Tags can be used to provide an alias instead of version numbers. For example, a project might choose to have multiple streams of development and use a different tag for each stream, e.g., stable, beta, dev, canary. By default, the ``latest`` tag is used by npm to identify the current version of a package, and ``npm install <pkg>`` (without any ``@<version>`` or ``@<tag>`` specifier) installs the latest tag. Typically, projects only use the ``latest`` tag for stable release versions, and use other tags for unstable versions such as prereleases. The ``next`` tag is used by some projects to identify the upcoming version. Default: "latest"
        :param npm_provenance: (experimental) Should provenance statements be generated when package is published. Note that this component is using ``publib`` to publish packages, which is using npm internally and supports provenance statements independently of the package manager used. Default: - undefined
        :param npm_token_secret: (experimental) GitHub secret which contains the NPM token to use when publishing packages. Default: - "NPM_TOKEN" or "GITHUB_TOKEN" if ``registry`` is set to ``npm.pkg.github.com``.
        :param registry: (experimental) The domain name of the npm package registry. To publish to GitHub Packages, set this value to ``"npm.pkg.github.com"``. In this if ``npmTokenSecret`` is not specified, it will default to ``GITHUB_TOKEN`` which means that you will be able to publish to the repository's package store. In this case, make sure ``repositoryUrl`` is correctly defined. Default: "registry.npmjs.org"

        :stability: experimental
        '''
        if isinstance(publish_tools, dict):
            publish_tools = _Tools_75b93a2a(**publish_tools)
        if isinstance(code_artifact_options, dict):
            code_artifact_options = CodeArtifactOptions(**code_artifact_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458289050585e6e895f9ee709ee4e102166b0f71e3c8b2a0617efa2d24e990fb)
            check_type(argname="argument post_publish_steps", value=post_publish_steps, expected_type=type_hints["post_publish_steps"])
            check_type(argname="argument pre_publish_steps", value=pre_publish_steps, expected_type=type_hints["pre_publish_steps"])
            check_type(argname="argument publish_tools", value=publish_tools, expected_type=type_hints["publish_tools"])
            check_type(argname="argument code_artifact_options", value=code_artifact_options, expected_type=type_hints["code_artifact_options"])
            check_type(argname="argument dist_tag", value=dist_tag, expected_type=type_hints["dist_tag"])
            check_type(argname="argument npm_provenance", value=npm_provenance, expected_type=type_hints["npm_provenance"])
            check_type(argname="argument npm_token_secret", value=npm_token_secret, expected_type=type_hints["npm_token_secret"])
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_publish_steps is not None:
            self._values["post_publish_steps"] = post_publish_steps
        if pre_publish_steps is not None:
            self._values["pre_publish_steps"] = pre_publish_steps
        if publish_tools is not None:
            self._values["publish_tools"] = publish_tools
        if code_artifact_options is not None:
            self._values["code_artifact_options"] = code_artifact_options
        if dist_tag is not None:
            self._values["dist_tag"] = dist_tag
        if npm_provenance is not None:
            self._values["npm_provenance"] = npm_provenance
        if npm_token_secret is not None:
            self._values["npm_token_secret"] = npm_token_secret
        if registry is not None:
            self._values["registry"] = registry

    @builtins.property
    def post_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after executing the publishing command.

        These can be used
        to add/update the release artifacts ot any other tasks needed.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("post_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def pre_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed.

        These steps are executed after ``dist/`` has been populated with the build
        output.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("pre_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def publish_tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Additional tools to install in the publishing job.

        :default: - no additional tools are installed

        :stability: experimental
        '''
        result = self._values.get("publish_tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    @builtins.property
    def code_artifact_options(self) -> typing.Optional[CodeArtifactOptions]:
        '''(experimental) Options for publishing npm package to AWS CodeArtifact.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("code_artifact_options")
        return typing.cast(typing.Optional[CodeArtifactOptions], result)

    @builtins.property
    def dist_tag(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Tags can be used to provide an alias instead of version numbers.

        For example, a project might choose to have multiple streams of development
        and use a different tag for each stream, e.g., stable, beta, dev, canary.

        By default, the ``latest`` tag is used by npm to identify the current version
        of a package, and ``npm install <pkg>`` (without any ``@<version>`` or ``@<tag>``
        specifier) installs the latest tag. Typically, projects only use the
        ``latest`` tag for stable release versions, and use other tags for unstable
        versions such as prereleases.

        The ``next`` tag is used by some projects to identify the upcoming version.

        :default: "latest"

        :deprecated: Use ``npmDistTag`` for each release branch instead.

        :stability: deprecated
        '''
        result = self._values.get("dist_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_provenance(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should provenance statements be generated when package is published.

        Note that this component is using ``publib`` to publish packages,
        which is using npm internally and supports provenance statements independently of the package manager used.

        :default: - undefined

        :see: https://docs.npmjs.com/generating-provenance-statements
        :stability: experimental
        '''
        result = self._values.get("npm_provenance")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def npm_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the NPM token to use when publishing packages.

        :default: - "NPM_TOKEN" or "GITHUB_TOKEN" if ``registry`` is set to ``npm.pkg.github.com``.

        :stability: experimental
        '''
        result = self._values.get("npm_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry(self) -> typing.Optional[builtins.str]:
        '''(experimental) The domain name of the npm package registry.

        To publish to GitHub Packages, set this value to ``"npm.pkg.github.com"``. In
        this if ``npmTokenSecret`` is not specified, it will default to
        ``GITHUB_TOKEN`` which means that you will be able to publish to the
        repository's package store. In this case, make sure ``repositoryUrl`` is
        correctly defined.

        :default: "registry.npmjs.org"

        :stability: experimental

        Example::

            "npm.pkg.github.com"
        '''
        result = self._values.get("registry")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NpmPublishOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.NugetPublishOptions",
    jsii_struct_bases=[CommonPublishOptions],
    name_mapping={
        "post_publish_steps": "postPublishSteps",
        "pre_publish_steps": "prePublishSteps",
        "publish_tools": "publishTools",
        "nuget_api_key_secret": "nugetApiKeySecret",
        "nuget_server": "nugetServer",
    },
)
class NugetPublishOptions(CommonPublishOptions):
    def __init__(
        self,
        *,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
        nuget_api_key_secret: typing.Optional[builtins.str] = None,
        nuget_server: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for NuGet releases.

        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed
        :param nuget_api_key_secret: (experimental) GitHub secret which contains the API key for NuGet. Default: "NUGET_API_KEY"
        :param nuget_server: (experimental) NuGet Server URL (defaults to nuget.org).

        :stability: experimental
        '''
        if isinstance(publish_tools, dict):
            publish_tools = _Tools_75b93a2a(**publish_tools)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584d4125e43e970396e9062b357de30ef32a6d1b30bd3a0f00fc7db041ea0bec)
            check_type(argname="argument post_publish_steps", value=post_publish_steps, expected_type=type_hints["post_publish_steps"])
            check_type(argname="argument pre_publish_steps", value=pre_publish_steps, expected_type=type_hints["pre_publish_steps"])
            check_type(argname="argument publish_tools", value=publish_tools, expected_type=type_hints["publish_tools"])
            check_type(argname="argument nuget_api_key_secret", value=nuget_api_key_secret, expected_type=type_hints["nuget_api_key_secret"])
            check_type(argname="argument nuget_server", value=nuget_server, expected_type=type_hints["nuget_server"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_publish_steps is not None:
            self._values["post_publish_steps"] = post_publish_steps
        if pre_publish_steps is not None:
            self._values["pre_publish_steps"] = pre_publish_steps
        if publish_tools is not None:
            self._values["publish_tools"] = publish_tools
        if nuget_api_key_secret is not None:
            self._values["nuget_api_key_secret"] = nuget_api_key_secret
        if nuget_server is not None:
            self._values["nuget_server"] = nuget_server

    @builtins.property
    def post_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after executing the publishing command.

        These can be used
        to add/update the release artifacts ot any other tasks needed.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("post_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def pre_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed.

        These steps are executed after ``dist/`` has been populated with the build
        output.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("pre_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def publish_tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Additional tools to install in the publishing job.

        :default: - no additional tools are installed

        :stability: experimental
        '''
        result = self._values.get("publish_tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    @builtins.property
    def nuget_api_key_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the API key for NuGet.

        :default: "NUGET_API_KEY"

        :stability: experimental
        '''
        result = self._values.get("nuget_api_key_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nuget_server(self) -> typing.Optional[builtins.str]:
        '''(experimental) NuGet Server URL (defaults to nuget.org).

        :stability: experimental
        '''
        result = self._values.get("nuget_server")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NugetPublishOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Publisher(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.release.Publisher",
):
    '''(experimental) Implements GitHub jobs for publishing modules to package managers.

    Under the hood, it uses https://github.com/aws/publib

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        *,
        artifact_name: builtins.str,
        build_job_id: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        dry_run: typing.Optional[builtins.bool] = None,
        failure_issue: typing.Optional[builtins.bool] = None,
        failure_issue_label: typing.Optional[builtins.str] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        publib_version: typing.Optional[builtins.str] = None,
        publish_tasks: typing.Optional[builtins.bool] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param project: -
        :param artifact_name: (experimental) The name of the artifact to download (e.g. ``dist``). The artifact is expected to include a subdirectory for each release target: ``go`` (GitHub), ``dotnet`` (NuGet), ``java`` (Maven), ``js`` (npm), ``python`` (PyPI).
        :param build_job_id: (experimental) The job ID that produces the build artifacts. All publish jobs will take a dependency on this job.
        :param condition: (experimental) A GitHub workflow expression used as a condition for publishers. Default: - no condition
        :param dry_run: (experimental) Do not actually publish, only print the commands that would be executed instead. Useful if you wish to block all publishing from a single option.
        :param failure_issue: (experimental) Create an issue when a publish task fails. Default: false
        :param failure_issue_label: (experimental) The label to apply to the issue marking failed publish tasks. Only applies if ``failureIssue`` is true. Default: "failed-release"
        :param jsii_release_version: 
        :param publib_version: (experimental) Version requirement for ``publib``. Default: "latest"
        :param publish_tasks: (experimental) Define publishing tasks that can be executed manually as well as workflows. Normally, publishing only happens within automated workflows. Enable this in order to create a publishing task for each publishing activity. Default: false
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_node_version: (experimental) Node version to setup in GitHub workflows if any node-based CLI utilities are needed. For example ``publib``, the CLI projen uses to publish releases, is an npm library. Default: lts/*
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee2fd880a34190cc3f39bd885d4276ff656803edbfe41e03f405df373cf1886)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        options = PublisherOptions(
            artifact_name=artifact_name,
            build_job_id=build_job_id,
            condition=condition,
            dry_run=dry_run,
            failure_issue=failure_issue,
            failure_issue_label=failure_issue_label,
            jsii_release_version=jsii_release_version,
            publib_version=publib_version,
            publish_tasks=publish_tasks,
            workflow_container_image=workflow_container_image,
            workflow_node_version=workflow_node_version,
            workflow_runs_on=workflow_runs_on,
            workflow_runs_on_group=workflow_runs_on_group,
        )

        jsii.create(self.__class__, self, [project, options])

    @jsii.member(jsii_name="addGitHubPostPublishingSteps")
    def add_git_hub_post_publishing_steps(self, *steps: _JobStep_c3287c05) -> None:
        '''(experimental) Adds post publishing steps for the GitHub release job.

        :param steps: The steps.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc29acfacedcf962e3aef9229c52a0b3f87bcc40c48ec3ef2bb7b9aff15cdf4)
            check_type(argname="argument steps", value=steps, expected_type=typing.Tuple[type_hints["steps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addGitHubPostPublishingSteps", [*steps]))

    @jsii.member(jsii_name="addGitHubPrePublishingSteps")
    def add_git_hub_pre_publishing_steps(self, *steps: _JobStep_c3287c05) -> None:
        '''(experimental) Adds pre publishing steps for the GitHub release job.

        :param steps: The steps.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92bbbd5b910dba917f337b84006ddf331f055b5c222b506b0599fb0a9ed444e5)
            check_type(argname="argument steps", value=steps, expected_type=typing.Tuple[type_hints["steps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addGitHubPrePublishingSteps", [*steps]))

    @jsii.member(jsii_name="publishToGit")
    def publish_to_git(
        self,
        *,
        changelog_file: builtins.str,
        release_tag_file: builtins.str,
        version_file: builtins.str,
        git_branch: typing.Optional[builtins.str] = None,
        git_push_command: typing.Optional[builtins.str] = None,
        project_changelog_file: typing.Optional[builtins.str] = None,
    ) -> _Task_9fa875b6:
        '''(experimental) Publish to git.

        This includes generating a project-level changelog and release tags.

        :param changelog_file: (experimental) The location of an .md file (relative to ``dist/``) that includes the changelog for the release.
        :param release_tag_file: (experimental) The location of a text file (relative to ``dist/``) that contains the release tag.
        :param version_file: (experimental) The location of a text file (relative to ``dist/``) that contains the version number.
        :param git_branch: (experimental) Branch to push to. Default: "main"
        :param git_push_command: (experimental) Override git-push command. Set to an empty string to disable pushing.
        :param project_changelog_file: (experimental) The location of an .md file that includes the project-level changelog.

        :stability: experimental
        '''
        options = GitPublishOptions(
            changelog_file=changelog_file,
            release_tag_file=release_tag_file,
            version_file=version_file,
            git_branch=git_branch,
            git_push_command=git_push_command,
            project_changelog_file=project_changelog_file,
        )

        return typing.cast(_Task_9fa875b6, jsii.invoke(self, "publishToGit", [options]))

    @jsii.member(jsii_name="publishToGitHubReleases")
    def publish_to_git_hub_releases(
        self,
        *,
        changelog_file: builtins.str,
        release_tag_file: builtins.str,
        version_file: builtins.str,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Creates a GitHub Release.

        :param changelog_file: (experimental) The location of an .md file (relative to ``dist/``) that includes the changelog for the release.
        :param release_tag_file: (experimental) The location of a text file (relative to ``dist/``) that contains the release tag.
        :param version_file: (experimental) The location of a text file (relative to ``dist/``) that contains the version number.
        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed

        :stability: experimental
        '''
        options = GitHubReleasesPublishOptions(
            changelog_file=changelog_file,
            release_tag_file=release_tag_file,
            version_file=version_file,
            post_publish_steps=post_publish_steps,
            pre_publish_steps=pre_publish_steps,
            publish_tools=publish_tools,
        )

        return typing.cast(None, jsii.invoke(self, "publishToGitHubReleases", [options]))

    @jsii.member(jsii_name="publishToGo")
    def publish_to_go(
        self,
        *,
        git_branch: typing.Optional[builtins.str] = None,
        git_commit_message: typing.Optional[builtins.str] = None,
        github_deploy_key_secret: typing.Optional[builtins.str] = None,
        github_token_secret: typing.Optional[builtins.str] = None,
        github_use_ssh: typing.Optional[builtins.bool] = None,
        git_user_email: typing.Optional[builtins.str] = None,
        git_user_name: typing.Optional[builtins.str] = None,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Adds a go publishing job.

        :param git_branch: (experimental) Branch to push to. Default: "main"
        :param git_commit_message: (experimental) The commit message. Default: "chore(release): $VERSION"
        :param github_deploy_key_secret: (experimental) The name of the secret that includes a GitHub deploy key used to push to the GitHub repository. Ignored if ``githubUseSsh`` is ``false``. Default: "GO_GITHUB_DEPLOY_KEY"
        :param github_token_secret: (experimental) The name of the secret that includes a personal GitHub access token used to push to the GitHub repository. Ignored if ``githubUseSsh`` is ``true``. Default: "GO_GITHUB_TOKEN"
        :param github_use_ssh: (experimental) Use SSH to push to GitHub instead of a personal accses token. Default: false
        :param git_user_email: (experimental) The email to use in the release git commit. Default: "github-actions@github.com"
        :param git_user_name: (experimental) The user name to use for the release git commit. Default: "github-actions"
        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed

        :stability: experimental
        '''
        options = GoPublishOptions(
            git_branch=git_branch,
            git_commit_message=git_commit_message,
            github_deploy_key_secret=github_deploy_key_secret,
            github_token_secret=github_token_secret,
            github_use_ssh=github_use_ssh,
            git_user_email=git_user_email,
            git_user_name=git_user_name,
            post_publish_steps=post_publish_steps,
            pre_publish_steps=pre_publish_steps,
            publish_tools=publish_tools,
        )

        return typing.cast(None, jsii.invoke(self, "publishToGo", [options]))

    @jsii.member(jsii_name="publishToMaven")
    def publish_to_maven(
        self,
        *,
        maven_endpoint: typing.Optional[builtins.str] = None,
        maven_gpg_private_key_passphrase: typing.Optional[builtins.str] = None,
        maven_gpg_private_key_secret: typing.Optional[builtins.str] = None,
        maven_password: typing.Optional[builtins.str] = None,
        maven_repository_url: typing.Optional[builtins.str] = None,
        maven_server_id: typing.Optional[builtins.str] = None,
        maven_staging_profile_id: typing.Optional[builtins.str] = None,
        maven_username: typing.Optional[builtins.str] = None,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Publishes artifacts from ``java/**`` to Maven.

        :param maven_endpoint: (experimental) URL of Nexus repository. if not set, defaults to https://oss.sonatype.org Default: "https://oss.sonatype.org"
        :param maven_gpg_private_key_passphrase: (experimental) GitHub secret name which contains the GPG private key or file that includes it. This is used to sign your Maven packages. See instructions. Default: "MAVEN_GPG_PRIVATE_KEY_PASSPHRASE" or not set when using GitHub Packages
        :param maven_gpg_private_key_secret: (experimental) GitHub secret name which contains the GPG private key or file that includes it. This is used to sign your Maven packages. See instructions. Default: "MAVEN_GPG_PRIVATE_KEY" or not set when using GitHub Packages
        :param maven_password: (experimental) GitHub secret name which contains the Password for maven repository. For Maven Central, you will need to Create JIRA account and then request a new project (see links). Default: "MAVEN_PASSWORD" or "GITHUB_TOKEN" when using GitHub Packages
        :param maven_repository_url: (experimental) Deployment repository when not deploying to Maven Central. Default: - not set
        :param maven_server_id: (experimental) Used in maven settings for credential lookup (e.g. use github when publishing to GitHub). Default: "ossrh" (Maven Central) or "github" when using GitHub Packages
        :param maven_staging_profile_id: (experimental) GitHub secret name which contains the Maven Central (sonatype) staging profile ID (e.g. 68a05363083174). Staging profile ID can be found in the URL of the "Releases" staging profile under "Staging Profiles" in https://oss.sonatype.org (e.g. https://oss.sonatype.org/#stagingProfiles;11a33451234521). Default: "MAVEN_STAGING_PROFILE_ID" or not set when using GitHub Packages
        :param maven_username: (experimental) GitHub secret name which contains the Username for maven repository. For Maven Central, you will need to Create JIRA account and then request a new project (see links). Default: "MAVEN_USERNAME" or the GitHub Actor when using GitHub Packages
        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed

        :stability: experimental
        '''
        options = MavenPublishOptions(
            maven_endpoint=maven_endpoint,
            maven_gpg_private_key_passphrase=maven_gpg_private_key_passphrase,
            maven_gpg_private_key_secret=maven_gpg_private_key_secret,
            maven_password=maven_password,
            maven_repository_url=maven_repository_url,
            maven_server_id=maven_server_id,
            maven_staging_profile_id=maven_staging_profile_id,
            maven_username=maven_username,
            post_publish_steps=post_publish_steps,
            pre_publish_steps=pre_publish_steps,
            publish_tools=publish_tools,
        )

        return typing.cast(None, jsii.invoke(self, "publishToMaven", [options]))

    @jsii.member(jsii_name="publishToNpm")
    def publish_to_npm(
        self,
        *,
        code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        dist_tag: typing.Optional[builtins.str] = None,
        npm_provenance: typing.Optional[builtins.bool] = None,
        npm_token_secret: typing.Optional[builtins.str] = None,
        registry: typing.Optional[builtins.str] = None,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Publishes artifacts from ``js/**`` to npm.

        :param code_artifact_options: (experimental) Options for publishing npm package to AWS CodeArtifact. Default: - undefined
        :param dist_tag: (deprecated) Tags can be used to provide an alias instead of version numbers. For example, a project might choose to have multiple streams of development and use a different tag for each stream, e.g., stable, beta, dev, canary. By default, the ``latest`` tag is used by npm to identify the current version of a package, and ``npm install <pkg>`` (without any ``@<version>`` or ``@<tag>`` specifier) installs the latest tag. Typically, projects only use the ``latest`` tag for stable release versions, and use other tags for unstable versions such as prereleases. The ``next`` tag is used by some projects to identify the upcoming version. Default: "latest"
        :param npm_provenance: (experimental) Should provenance statements be generated when package is published. Note that this component is using ``publib`` to publish packages, which is using npm internally and supports provenance statements independently of the package manager used. Default: - undefined
        :param npm_token_secret: (experimental) GitHub secret which contains the NPM token to use when publishing packages. Default: - "NPM_TOKEN" or "GITHUB_TOKEN" if ``registry`` is set to ``npm.pkg.github.com``.
        :param registry: (experimental) The domain name of the npm package registry. To publish to GitHub Packages, set this value to ``"npm.pkg.github.com"``. In this if ``npmTokenSecret`` is not specified, it will default to ``GITHUB_TOKEN`` which means that you will be able to publish to the repository's package store. In this case, make sure ``repositoryUrl`` is correctly defined. Default: "registry.npmjs.org"
        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed

        :stability: experimental
        '''
        options = NpmPublishOptions(
            code_artifact_options=code_artifact_options,
            dist_tag=dist_tag,
            npm_provenance=npm_provenance,
            npm_token_secret=npm_token_secret,
            registry=registry,
            post_publish_steps=post_publish_steps,
            pre_publish_steps=pre_publish_steps,
            publish_tools=publish_tools,
        )

        return typing.cast(None, jsii.invoke(self, "publishToNpm", [options]))

    @jsii.member(jsii_name="publishToNuget")
    def publish_to_nuget(
        self,
        *,
        nuget_api_key_secret: typing.Optional[builtins.str] = None,
        nuget_server: typing.Optional[builtins.str] = None,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Publishes artifacts from ``dotnet/**`` to NuGet Gallery.

        :param nuget_api_key_secret: (experimental) GitHub secret which contains the API key for NuGet. Default: "NUGET_API_KEY"
        :param nuget_server: (experimental) NuGet Server URL (defaults to nuget.org).
        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed

        :stability: experimental
        '''
        options = NugetPublishOptions(
            nuget_api_key_secret=nuget_api_key_secret,
            nuget_server=nuget_server,
            post_publish_steps=post_publish_steps,
            pre_publish_steps=pre_publish_steps,
            publish_tools=publish_tools,
        )

        return typing.cast(None, jsii.invoke(self, "publishToNuget", [options]))

    @jsii.member(jsii_name="publishToPyPi")
    def publish_to_py_pi(
        self,
        *,
        code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        twine_password_secret: typing.Optional[builtins.str] = None,
        twine_registry_url: typing.Optional[builtins.str] = None,
        twine_username_secret: typing.Optional[builtins.str] = None,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Publishes wheel artifacts from ``python`` to PyPI.

        :param code_artifact_options: (experimental) Options for publishing to AWS CodeArtifact. Default: - undefined
        :param twine_password_secret: (experimental) The GitHub secret which contains PyPI password. Default: "TWINE_PASSWORD"
        :param twine_registry_url: (experimental) The registry url to use when releasing packages. Default: - twine default
        :param twine_username_secret: (experimental) The GitHub secret which contains PyPI user name. Default: "TWINE_USERNAME"
        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed

        :stability: experimental
        '''
        options = PyPiPublishOptions(
            code_artifact_options=code_artifact_options,
            twine_password_secret=twine_password_secret,
            twine_registry_url=twine_registry_url,
            twine_username_secret=twine_username_secret,
            post_publish_steps=post_publish_steps,
            pre_publish_steps=pre_publish_steps,
            publish_tools=publish_tools,
        )

        return typing.cast(None, jsii.invoke(self, "publishToPyPi", [options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PUBLISH_GIT_TASK_NAME")
    def PUBLISH_GIT_TASK_NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PUBLISH_GIT_TASK_NAME"))

    @builtins.property
    @jsii.member(jsii_name="artifactName")
    def artifact_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "artifactName"))

    @builtins.property
    @jsii.member(jsii_name="buildJobId")
    def build_job_id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "buildJobId"))

    @builtins.property
    @jsii.member(jsii_name="jsiiReleaseVersion")
    def jsii_release_version(self) -> builtins.str:
        '''
        :deprecated: use ``publibVersion``

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "jsiiReleaseVersion"))

    @builtins.property
    @jsii.member(jsii_name="publibVersion")
    def publib_version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "publibVersion"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "condition"))


@jsii.data_type(
    jsii_type="projen.release.PublisherOptions",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_name": "artifactName",
        "build_job_id": "buildJobId",
        "condition": "condition",
        "dry_run": "dryRun",
        "failure_issue": "failureIssue",
        "failure_issue_label": "failureIssueLabel",
        "jsii_release_version": "jsiiReleaseVersion",
        "publib_version": "publibVersion",
        "publish_tasks": "publishTasks",
        "workflow_container_image": "workflowContainerImage",
        "workflow_node_version": "workflowNodeVersion",
        "workflow_runs_on": "workflowRunsOn",
        "workflow_runs_on_group": "workflowRunsOnGroup",
    },
)
class PublisherOptions:
    def __init__(
        self,
        *,
        artifact_name: builtins.str,
        build_job_id: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        dry_run: typing.Optional[builtins.bool] = None,
        failure_issue: typing.Optional[builtins.bool] = None,
        failure_issue_label: typing.Optional[builtins.str] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        publib_version: typing.Optional[builtins.str] = None,
        publish_tasks: typing.Optional[builtins.bool] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``Publisher``.

        :param artifact_name: (experimental) The name of the artifact to download (e.g. ``dist``). The artifact is expected to include a subdirectory for each release target: ``go`` (GitHub), ``dotnet`` (NuGet), ``java`` (Maven), ``js`` (npm), ``python`` (PyPI).
        :param build_job_id: (experimental) The job ID that produces the build artifacts. All publish jobs will take a dependency on this job.
        :param condition: (experimental) A GitHub workflow expression used as a condition for publishers. Default: - no condition
        :param dry_run: (experimental) Do not actually publish, only print the commands that would be executed instead. Useful if you wish to block all publishing from a single option.
        :param failure_issue: (experimental) Create an issue when a publish task fails. Default: false
        :param failure_issue_label: (experimental) The label to apply to the issue marking failed publish tasks. Only applies if ``failureIssue`` is true. Default: "failed-release"
        :param jsii_release_version: 
        :param publib_version: (experimental) Version requirement for ``publib``. Default: "latest"
        :param publish_tasks: (experimental) Define publishing tasks that can be executed manually as well as workflows. Normally, publishing only happens within automated workflows. Enable this in order to create a publishing task for each publishing activity. Default: false
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_node_version: (experimental) Node version to setup in GitHub workflows if any node-based CLI utilities are needed. For example ``publib``, the CLI projen uses to publish releases, is an npm library. Default: lts/*
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.

        :stability: experimental
        '''
        if isinstance(workflow_runs_on_group, dict):
            workflow_runs_on_group = _GroupRunnerOptions_148c59c1(**workflow_runs_on_group)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e430972b008e5968049196f964ee9dfa036c68b2195f125119bc2629263e791)
            check_type(argname="argument artifact_name", value=artifact_name, expected_type=type_hints["artifact_name"])
            check_type(argname="argument build_job_id", value=build_job_id, expected_type=type_hints["build_job_id"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument dry_run", value=dry_run, expected_type=type_hints["dry_run"])
            check_type(argname="argument failure_issue", value=failure_issue, expected_type=type_hints["failure_issue"])
            check_type(argname="argument failure_issue_label", value=failure_issue_label, expected_type=type_hints["failure_issue_label"])
            check_type(argname="argument jsii_release_version", value=jsii_release_version, expected_type=type_hints["jsii_release_version"])
            check_type(argname="argument publib_version", value=publib_version, expected_type=type_hints["publib_version"])
            check_type(argname="argument publish_tasks", value=publish_tasks, expected_type=type_hints["publish_tasks"])
            check_type(argname="argument workflow_container_image", value=workflow_container_image, expected_type=type_hints["workflow_container_image"])
            check_type(argname="argument workflow_node_version", value=workflow_node_version, expected_type=type_hints["workflow_node_version"])
            check_type(argname="argument workflow_runs_on", value=workflow_runs_on, expected_type=type_hints["workflow_runs_on"])
            check_type(argname="argument workflow_runs_on_group", value=workflow_runs_on_group, expected_type=type_hints["workflow_runs_on_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_name": artifact_name,
            "build_job_id": build_job_id,
        }
        if condition is not None:
            self._values["condition"] = condition
        if dry_run is not None:
            self._values["dry_run"] = dry_run
        if failure_issue is not None:
            self._values["failure_issue"] = failure_issue
        if failure_issue_label is not None:
            self._values["failure_issue_label"] = failure_issue_label
        if jsii_release_version is not None:
            self._values["jsii_release_version"] = jsii_release_version
        if publib_version is not None:
            self._values["publib_version"] = publib_version
        if publish_tasks is not None:
            self._values["publish_tasks"] = publish_tasks
        if workflow_container_image is not None:
            self._values["workflow_container_image"] = workflow_container_image
        if workflow_node_version is not None:
            self._values["workflow_node_version"] = workflow_node_version
        if workflow_runs_on is not None:
            self._values["workflow_runs_on"] = workflow_runs_on
        if workflow_runs_on_group is not None:
            self._values["workflow_runs_on_group"] = workflow_runs_on_group

    @builtins.property
    def artifact_name(self) -> builtins.str:
        '''(experimental) The name of the artifact to download (e.g. ``dist``).

        The artifact is expected to include a subdirectory for each release target:
        ``go`` (GitHub), ``dotnet`` (NuGet), ``java`` (Maven), ``js`` (npm), ``python``
        (PyPI).

        :see: https://github.com/aws/publib
        :stability: experimental
        '''
        result = self._values.get("artifact_name")
        assert result is not None, "Required property 'artifact_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_job_id(self) -> builtins.str:
        '''(experimental) The job ID that produces the build artifacts.

        All publish jobs will take a dependency on this job.

        :stability: experimental
        '''
        result = self._values.get("build_job_id")
        assert result is not None, "Required property 'build_job_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) A GitHub workflow expression used as a condition for publishers.

        :default: - no condition

        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dry_run(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not actually publish, only print the commands that would be executed instead.

        Useful if you wish to block all publishing from a single option.

        :stability: experimental
        '''
        result = self._values.get("dry_run")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def failure_issue(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Create an issue when a publish task fails.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("failure_issue")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def failure_issue_label(self) -> typing.Optional[builtins.str]:
        '''(experimental) The label to apply to the issue marking failed publish tasks.

        Only applies if ``failureIssue`` is true.

        :default: "failed-release"

        :stability: experimental
        '''
        result = self._values.get("failure_issue_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsii_release_version(self) -> typing.Optional[builtins.str]:
        '''
        :deprecated: use ``publibVersion`` instead

        :stability: deprecated
        '''
        result = self._values.get("jsii_release_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publib_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version requirement for ``publib``.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("publib_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_tasks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define publishing tasks that can be executed manually as well as workflows.

        Normally, publishing only happens within automated workflows. Enable this
        in order to create a publishing task for each publishing activity.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_tasks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def workflow_container_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Container image to use for GitHub workflows.

        :default: - default image

        :stability: experimental
        '''
        result = self._values.get("workflow_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Node version to setup in GitHub workflows if any node-based CLI utilities are needed.

        For example ``publib``, the CLI projen uses to publish releases,
        is an npm library.

        :default: lts/*

        :stability: experimental
        '''
        result = self._values.get("workflow_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_runs_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Github Runner selection labels.

        :default: ["ubuntu-latest"]

        :stability: experimental
        :description: Defines a target Runner by labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def workflow_runs_on_group(self) -> typing.Optional[_GroupRunnerOptions_148c59c1]:
        '''(experimental) Github Runner Group selection options.

        :stability: experimental
        :description: Defines a target Runner Group by name and/or labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on_group")
        return typing.cast(typing.Optional[_GroupRunnerOptions_148c59c1], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PublisherOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.PyPiPublishOptions",
    jsii_struct_bases=[CommonPublishOptions],
    name_mapping={
        "post_publish_steps": "postPublishSteps",
        "pre_publish_steps": "prePublishSteps",
        "publish_tools": "publishTools",
        "code_artifact_options": "codeArtifactOptions",
        "twine_password_secret": "twinePasswordSecret",
        "twine_registry_url": "twineRegistryUrl",
        "twine_username_secret": "twineUsernameSecret",
    },
)
class PyPiPublishOptions(CommonPublishOptions):
    def __init__(
        self,
        *,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
        code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        twine_password_secret: typing.Optional[builtins.str] = None,
        twine_registry_url: typing.Optional[builtins.str] = None,
        twine_username_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for PyPI release.

        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed
        :param code_artifact_options: (experimental) Options for publishing to AWS CodeArtifact. Default: - undefined
        :param twine_password_secret: (experimental) The GitHub secret which contains PyPI password. Default: "TWINE_PASSWORD"
        :param twine_registry_url: (experimental) The registry url to use when releasing packages. Default: - twine default
        :param twine_username_secret: (experimental) The GitHub secret which contains PyPI user name. Default: "TWINE_USERNAME"

        :stability: experimental
        '''
        if isinstance(publish_tools, dict):
            publish_tools = _Tools_75b93a2a(**publish_tools)
        if isinstance(code_artifact_options, dict):
            code_artifact_options = CodeArtifactOptions(**code_artifact_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90cd44def59be822b686bcd759d7f0a910b9936ca8acc0ef3e69cda5ddc21d2)
            check_type(argname="argument post_publish_steps", value=post_publish_steps, expected_type=type_hints["post_publish_steps"])
            check_type(argname="argument pre_publish_steps", value=pre_publish_steps, expected_type=type_hints["pre_publish_steps"])
            check_type(argname="argument publish_tools", value=publish_tools, expected_type=type_hints["publish_tools"])
            check_type(argname="argument code_artifact_options", value=code_artifact_options, expected_type=type_hints["code_artifact_options"])
            check_type(argname="argument twine_password_secret", value=twine_password_secret, expected_type=type_hints["twine_password_secret"])
            check_type(argname="argument twine_registry_url", value=twine_registry_url, expected_type=type_hints["twine_registry_url"])
            check_type(argname="argument twine_username_secret", value=twine_username_secret, expected_type=type_hints["twine_username_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_publish_steps is not None:
            self._values["post_publish_steps"] = post_publish_steps
        if pre_publish_steps is not None:
            self._values["pre_publish_steps"] = pre_publish_steps
        if publish_tools is not None:
            self._values["publish_tools"] = publish_tools
        if code_artifact_options is not None:
            self._values["code_artifact_options"] = code_artifact_options
        if twine_password_secret is not None:
            self._values["twine_password_secret"] = twine_password_secret
        if twine_registry_url is not None:
            self._values["twine_registry_url"] = twine_registry_url
        if twine_username_secret is not None:
            self._values["twine_username_secret"] = twine_username_secret

    @builtins.property
    def post_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after executing the publishing command.

        These can be used
        to add/update the release artifacts ot any other tasks needed.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("post_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def pre_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed.

        These steps are executed after ``dist/`` has been populated with the build
        output.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("pre_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def publish_tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Additional tools to install in the publishing job.

        :default: - no additional tools are installed

        :stability: experimental
        '''
        result = self._values.get("publish_tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    @builtins.property
    def code_artifact_options(self) -> typing.Optional[CodeArtifactOptions]:
        '''(experimental) Options for publishing to AWS CodeArtifact.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("code_artifact_options")
        return typing.cast(typing.Optional[CodeArtifactOptions], result)

    @builtins.property
    def twine_password_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub secret which contains PyPI password.

        :default: "TWINE_PASSWORD"

        :stability: experimental
        '''
        result = self._values.get("twine_password_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twine_registry_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The registry url to use when releasing packages.

        :default: - twine default

        :stability: experimental
        '''
        result = self._values.get("twine_registry_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twine_username_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub secret which contains PyPI user name.

        :default: "TWINE_USERNAME"

        :stability: experimental
        '''
        result = self._values.get("twine_username_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PyPiPublishOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Release(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.release.Release",
):
    '''(experimental) Manages releases (currently through GitHub workflows).

    By default, no branches are released. To add branches, call ``addBranch()``.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        *,
        artifacts_directory: builtins.str,
        branch: builtins.str,
        task: _Task_9fa875b6,
        version_file: builtins.str,
        github_release: typing.Optional[builtins.bool] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_permissions: typing.Optional[typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]]] = None,
        bump_package: typing.Optional[builtins.str] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        major_version: typing.Optional[jsii.Number] = None,
        min_major_version: typing.Optional[jsii.Number] = None,
        next_version_command: typing.Optional[builtins.str] = None,
        npm_dist_tag: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        publish_dry_run: typing.Optional[builtins.bool] = None,
        publish_tasks: typing.Optional[builtins.bool] = None,
        releasable_commits: typing.Optional[_ReleasableCommits_d481ce10] = None,
        release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        release_every_commit: typing.Optional[builtins.bool] = None,
        release_failure_issue: typing.Optional[builtins.bool] = None,
        release_failure_issue_label: typing.Optional[builtins.str] = None,
        release_schedule: typing.Optional[builtins.str] = None,
        release_tag_prefix: typing.Optional[builtins.str] = None,
        release_trigger: typing.Optional["ReleaseTrigger"] = None,
        release_workflow_name: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: should be part of the project the Release belongs to.
        :param artifacts_directory: (experimental) A directory which will contain build artifacts. Default: "dist"
        :param branch: (experimental) The default branch name to release from. Use ``majorVersion`` to restrict this branch to only publish releases with a specific major version. You can add additional branches using ``addBranch()``.
        :param task: (experimental) The task to execute in order to create the release artifacts. Artifacts are expected to reside under ``artifactsDirectory`` (defaults to ``dist/``) once build is complete.
        :param version_file: (experimental) A name of a .json file to set the ``version`` field in after a bump.
        :param github_release: (experimental) Create a GitHub release for each release. Default: true
        :param workflow_node_version: (experimental) Node version to setup in GitHub workflows if any node-based CLI utilities are needed. For example ``publib``, the CLI projen uses to publish releases, is an npm library. Default: "lts/*""
        :param workflow_permissions: (experimental) Permissions granted to the release workflow job. Default: ``{ contents: JobPermission.WRITE }``
        :param bump_package: (experimental) The ``commit-and-tag-version`` compatible package used to bump the package version, as a dependency string. This can be any compatible package version, including the deprecated ``standard-version@9``. Default: - A recent version of "commit-and-tag-version"
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param major_version: (experimental) Major version to release from the default branch. If this is specified, we bump the latest version of this major version line. If not specified, we bump the global latest version. Default: - Major version is not enforced.
        :param min_major_version: (experimental) Minimal Major version to release. This can be useful to set to 1, as breaking changes before the 1.x major release are not incrementing the major version number. Can not be set together with ``majorVersion``. Default: - No minimum version is being enforced
        :param next_version_command: (experimental) A shell command to control the next version to release. If present, this shell command will be run before the bump is executed, and it determines what version to release. It will be executed in the following environment: - Working directory: the project directory. - ``$VERSION``: the current version. Looks like ``1.2.3``. - ``$LATEST_TAG``: the most recent tag. Looks like ``prefix-v1.2.3``, or may be unset. - ``$SUGGESTED_BUMP``: the suggested bump action based on commits. One of ``major|minor|patch|none``. The command should print one of the following to ``stdout``: - Nothing: the next version number will be determined based on commit history. - ``x.y.z``: the next version number will be ``x.y.z``. - ``major|minor|patch``: the next version number will be the current version number with the indicated component bumped. This setting cannot be specified together with ``minMajorVersion``; the invoked script can be used to achieve the effects of ``minMajorVersion``. Default: - The next version will be determined based on the commit history and project settings.
        :param npm_dist_tag: (experimental) The npmDistTag to use when publishing from the default branch. To set the npm dist-tag for release branches, set the ``npmDistTag`` property for each branch. Default: "latest"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param publish_dry_run: (experimental) Instead of actually publishing to package managers, just print the publishing command. Default: false
        :param publish_tasks: (experimental) Define publishing tasks that can be executed manually as well as workflows. Normally, publishing only happens within automated workflows. Enable this in order to create a publishing task for each publishing activity. Default: false
        :param releasable_commits: (experimental) Find commits that should be considered releasable Used to decide if a release is required. Default: ReleasableCommits.everyCommit()
        :param release_branches: (experimental) Defines additional release branches. A workflow will be created for each release branch which will publish releases from commits in this branch. Each release branch *must* be assigned a major version number which is used to enforce that versions published from that branch always use that major version. If multiple branches are used, the ``majorVersion`` field must also be provided for the default branch. Default: - no additional branches are used for release. you can use ``addBranch()`` to add additional branches.
        :param release_every_commit: (deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``. Default: true
        :param release_failure_issue: (experimental) Create a github issue on every failed publishing task. Default: false
        :param release_failure_issue_label: (experimental) The label to apply to issues indicating publish failures. Only applies if ``releaseFailureIssue`` is true. Default: "failed-release"
        :param release_schedule: (deprecated) CRON schedule to trigger new releases. Default: - no scheduled releases
        :param release_tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: "v"
        :param release_trigger: (experimental) The release trigger to use. Default: - Continuous releases (``ReleaseTrigger.continuous()``)
        :param release_workflow_name: (experimental) The name of the default release workflow. Default: "release"
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param versionrc_options: (experimental) Custom configuration used when creating changelog with commit-and-tag-version package. Given values either append to default configuration or overwrite values in it. Default: - standard configuration applicable for GitHub repositories
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b447ecb34d36869391ee159467e6c78b74da704722d4c6a517e05bbae9016464)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = ReleaseOptions(
            artifacts_directory=artifacts_directory,
            branch=branch,
            task=task,
            version_file=version_file,
            github_release=github_release,
            workflow_node_version=workflow_node_version,
            workflow_permissions=workflow_permissions,
            bump_package=bump_package,
            jsii_release_version=jsii_release_version,
            major_version=major_version,
            min_major_version=min_major_version,
            next_version_command=next_version_command,
            npm_dist_tag=npm_dist_tag,
            post_build_steps=post_build_steps,
            prerelease=prerelease,
            publish_dry_run=publish_dry_run,
            publish_tasks=publish_tasks,
            releasable_commits=releasable_commits,
            release_branches=release_branches,
            release_every_commit=release_every_commit,
            release_failure_issue=release_failure_issue,
            release_failure_issue_label=release_failure_issue_label,
            release_schedule=release_schedule,
            release_tag_prefix=release_tag_prefix,
            release_trigger=release_trigger,
            release_workflow_name=release_workflow_name,
            release_workflow_setup_steps=release_workflow_setup_steps,
            versionrc_options=versionrc_options,
            workflow_container_image=workflow_container_image,
            workflow_runs_on=workflow_runs_on,
            workflow_runs_on_group=workflow_runs_on_group,
        )

        jsii.create(self.__class__, self, [scope, options])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, project: _Project_57d89203) -> typing.Optional["Release"]:
        '''(experimental) Returns the ``Release`` component of a project or ``undefined`` if the project does not have a Release component.

        :param project: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a92183b4ef9afc7a5f36329d0935bbbd7767d95d760424a1478dedd4c089e82)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        return typing.cast(typing.Optional["Release"], jsii.sinvoke(cls, "of", [project]))

    @jsii.member(jsii_name="addBranch")
    def add_branch(
        self,
        branch: builtins.str,
        *,
        major_version: jsii.Number,
        min_major_version: typing.Optional[jsii.Number] = None,
        minor_version: typing.Optional[jsii.Number] = None,
        npm_dist_tag: typing.Optional[builtins.str] = None,
        prerelease: typing.Optional[builtins.str] = None,
        tag_prefix: typing.Optional[builtins.str] = None,
        workflow_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Adds a release branch.

        It is a git branch from which releases are published. If a project has more than one release
        branch, we require that ``majorVersion`` is also specified for the primary branch in order to
        ensure branches always release the correct version.

        :param branch: The branch to monitor (e.g. ``main``, ``v2.x``).
        :param major_version: (experimental) The major versions released from this branch.
        :param min_major_version: (experimental) The minimum major version to release.
        :param minor_version: (experimental) The minor versions released from this branch.
        :param npm_dist_tag: (experimental) The npm distribution tag to use for this branch. Default: "latest"
        :param prerelease: (experimental) Bump the version as a pre-release tag. Default: - normal releases
        :param tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: - no prefix
        :param workflow_name: (experimental) The name of the release workflow. Default: "release-BRANCH"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f66d9106b15a88644bb5efb62c4d4d18bb7c7b73bb22b904010a8a603f1ec7)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        options = BranchOptions(
            major_version=major_version,
            min_major_version=min_major_version,
            minor_version=minor_version,
            npm_dist_tag=npm_dist_tag,
            prerelease=prerelease,
            tag_prefix=tag_prefix,
            workflow_name=workflow_name,
        )

        return typing.cast(None, jsii.invoke(self, "addBranch", [branch, options]))

    @jsii.member(jsii_name="addJobs")
    def add_jobs(
        self,
        jobs: typing.Mapping[builtins.str, typing.Union[_Job_20ffcf45, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''(experimental) Adds jobs to all release workflows.

        :param jobs: The jobs to add (name => job).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8df2839c98abec4e8a1e84ad0fc953b4051cdf361a30544804281bc912901e2)
            check_type(argname="argument jobs", value=jobs, expected_type=type_hints["jobs"])
        return typing.cast(None, jsii.invoke(self, "addJobs", [jobs]))

    @jsii.member(jsii_name="preSynthesize")
    def pre_synthesize(self) -> None:
        '''(experimental) Called before synthesis.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "preSynthesize", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ANTI_TAMPER_CMD")
    def ANTI_TAMPER_CMD(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ANTI_TAMPER_CMD"))

    @builtins.property
    @jsii.member(jsii_name="artifactsDirectory")
    def artifacts_directory(self) -> builtins.str:
        '''(experimental) Location of build artifacts.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "artifactsDirectory"))

    @builtins.property
    @jsii.member(jsii_name="branches")
    def branches(self) -> typing.List[builtins.str]:
        '''(experimental) Retrieve all release branch names.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "branches"))

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> Publisher:
        '''(experimental) Package publisher.

        :stability: experimental
        '''
        return typing.cast(Publisher, jsii.get(self, "publisher"))


@jsii.data_type(
    jsii_type="projen.release.ReleaseProjectOptions",
    jsii_struct_bases=[],
    name_mapping={
        "bump_package": "bumpPackage",
        "jsii_release_version": "jsiiReleaseVersion",
        "major_version": "majorVersion",
        "min_major_version": "minMajorVersion",
        "next_version_command": "nextVersionCommand",
        "npm_dist_tag": "npmDistTag",
        "post_build_steps": "postBuildSteps",
        "prerelease": "prerelease",
        "publish_dry_run": "publishDryRun",
        "publish_tasks": "publishTasks",
        "releasable_commits": "releasableCommits",
        "release_branches": "releaseBranches",
        "release_every_commit": "releaseEveryCommit",
        "release_failure_issue": "releaseFailureIssue",
        "release_failure_issue_label": "releaseFailureIssueLabel",
        "release_schedule": "releaseSchedule",
        "release_tag_prefix": "releaseTagPrefix",
        "release_trigger": "releaseTrigger",
        "release_workflow_name": "releaseWorkflowName",
        "release_workflow_setup_steps": "releaseWorkflowSetupSteps",
        "versionrc_options": "versionrcOptions",
        "workflow_container_image": "workflowContainerImage",
        "workflow_runs_on": "workflowRunsOn",
        "workflow_runs_on_group": "workflowRunsOnGroup",
    },
)
class ReleaseProjectOptions:
    def __init__(
        self,
        *,
        bump_package: typing.Optional[builtins.str] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        major_version: typing.Optional[jsii.Number] = None,
        min_major_version: typing.Optional[jsii.Number] = None,
        next_version_command: typing.Optional[builtins.str] = None,
        npm_dist_tag: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        publish_dry_run: typing.Optional[builtins.bool] = None,
        publish_tasks: typing.Optional[builtins.bool] = None,
        releasable_commits: typing.Optional[_ReleasableCommits_d481ce10] = None,
        release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        release_every_commit: typing.Optional[builtins.bool] = None,
        release_failure_issue: typing.Optional[builtins.bool] = None,
        release_failure_issue_label: typing.Optional[builtins.str] = None,
        release_schedule: typing.Optional[builtins.str] = None,
        release_tag_prefix: typing.Optional[builtins.str] = None,
        release_trigger: typing.Optional["ReleaseTrigger"] = None,
        release_workflow_name: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Project options for release.

        :param bump_package: (experimental) The ``commit-and-tag-version`` compatible package used to bump the package version, as a dependency string. This can be any compatible package version, including the deprecated ``standard-version@9``. Default: - A recent version of "commit-and-tag-version"
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param major_version: (experimental) Major version to release from the default branch. If this is specified, we bump the latest version of this major version line. If not specified, we bump the global latest version. Default: - Major version is not enforced.
        :param min_major_version: (experimental) Minimal Major version to release. This can be useful to set to 1, as breaking changes before the 1.x major release are not incrementing the major version number. Can not be set together with ``majorVersion``. Default: - No minimum version is being enforced
        :param next_version_command: (experimental) A shell command to control the next version to release. If present, this shell command will be run before the bump is executed, and it determines what version to release. It will be executed in the following environment: - Working directory: the project directory. - ``$VERSION``: the current version. Looks like ``1.2.3``. - ``$LATEST_TAG``: the most recent tag. Looks like ``prefix-v1.2.3``, or may be unset. - ``$SUGGESTED_BUMP``: the suggested bump action based on commits. One of ``major|minor|patch|none``. The command should print one of the following to ``stdout``: - Nothing: the next version number will be determined based on commit history. - ``x.y.z``: the next version number will be ``x.y.z``. - ``major|minor|patch``: the next version number will be the current version number with the indicated component bumped. This setting cannot be specified together with ``minMajorVersion``; the invoked script can be used to achieve the effects of ``minMajorVersion``. Default: - The next version will be determined based on the commit history and project settings.
        :param npm_dist_tag: (experimental) The npmDistTag to use when publishing from the default branch. To set the npm dist-tag for release branches, set the ``npmDistTag`` property for each branch. Default: "latest"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param publish_dry_run: (experimental) Instead of actually publishing to package managers, just print the publishing command. Default: false
        :param publish_tasks: (experimental) Define publishing tasks that can be executed manually as well as workflows. Normally, publishing only happens within automated workflows. Enable this in order to create a publishing task for each publishing activity. Default: false
        :param releasable_commits: (experimental) Find commits that should be considered releasable Used to decide if a release is required. Default: ReleasableCommits.everyCommit()
        :param release_branches: (experimental) Defines additional release branches. A workflow will be created for each release branch which will publish releases from commits in this branch. Each release branch *must* be assigned a major version number which is used to enforce that versions published from that branch always use that major version. If multiple branches are used, the ``majorVersion`` field must also be provided for the default branch. Default: - no additional branches are used for release. you can use ``addBranch()`` to add additional branches.
        :param release_every_commit: (deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``. Default: true
        :param release_failure_issue: (experimental) Create a github issue on every failed publishing task. Default: false
        :param release_failure_issue_label: (experimental) The label to apply to issues indicating publish failures. Only applies if ``releaseFailureIssue`` is true. Default: "failed-release"
        :param release_schedule: (deprecated) CRON schedule to trigger new releases. Default: - no scheduled releases
        :param release_tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: "v"
        :param release_trigger: (experimental) The release trigger to use. Default: - Continuous releases (``ReleaseTrigger.continuous()``)
        :param release_workflow_name: (experimental) The name of the default release workflow. Default: "release"
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param versionrc_options: (experimental) Custom configuration used when creating changelog with commit-and-tag-version package. Given values either append to default configuration or overwrite values in it. Default: - standard configuration applicable for GitHub repositories
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.

        :stability: experimental
        '''
        if isinstance(workflow_runs_on_group, dict):
            workflow_runs_on_group = _GroupRunnerOptions_148c59c1(**workflow_runs_on_group)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc5e99254de9f29d2ac3b86e193164816e1ed36e491e602128e7d16fb86aa377)
            check_type(argname="argument bump_package", value=bump_package, expected_type=type_hints["bump_package"])
            check_type(argname="argument jsii_release_version", value=jsii_release_version, expected_type=type_hints["jsii_release_version"])
            check_type(argname="argument major_version", value=major_version, expected_type=type_hints["major_version"])
            check_type(argname="argument min_major_version", value=min_major_version, expected_type=type_hints["min_major_version"])
            check_type(argname="argument next_version_command", value=next_version_command, expected_type=type_hints["next_version_command"])
            check_type(argname="argument npm_dist_tag", value=npm_dist_tag, expected_type=type_hints["npm_dist_tag"])
            check_type(argname="argument post_build_steps", value=post_build_steps, expected_type=type_hints["post_build_steps"])
            check_type(argname="argument prerelease", value=prerelease, expected_type=type_hints["prerelease"])
            check_type(argname="argument publish_dry_run", value=publish_dry_run, expected_type=type_hints["publish_dry_run"])
            check_type(argname="argument publish_tasks", value=publish_tasks, expected_type=type_hints["publish_tasks"])
            check_type(argname="argument releasable_commits", value=releasable_commits, expected_type=type_hints["releasable_commits"])
            check_type(argname="argument release_branches", value=release_branches, expected_type=type_hints["release_branches"])
            check_type(argname="argument release_every_commit", value=release_every_commit, expected_type=type_hints["release_every_commit"])
            check_type(argname="argument release_failure_issue", value=release_failure_issue, expected_type=type_hints["release_failure_issue"])
            check_type(argname="argument release_failure_issue_label", value=release_failure_issue_label, expected_type=type_hints["release_failure_issue_label"])
            check_type(argname="argument release_schedule", value=release_schedule, expected_type=type_hints["release_schedule"])
            check_type(argname="argument release_tag_prefix", value=release_tag_prefix, expected_type=type_hints["release_tag_prefix"])
            check_type(argname="argument release_trigger", value=release_trigger, expected_type=type_hints["release_trigger"])
            check_type(argname="argument release_workflow_name", value=release_workflow_name, expected_type=type_hints["release_workflow_name"])
            check_type(argname="argument release_workflow_setup_steps", value=release_workflow_setup_steps, expected_type=type_hints["release_workflow_setup_steps"])
            check_type(argname="argument versionrc_options", value=versionrc_options, expected_type=type_hints["versionrc_options"])
            check_type(argname="argument workflow_container_image", value=workflow_container_image, expected_type=type_hints["workflow_container_image"])
            check_type(argname="argument workflow_runs_on", value=workflow_runs_on, expected_type=type_hints["workflow_runs_on"])
            check_type(argname="argument workflow_runs_on_group", value=workflow_runs_on_group, expected_type=type_hints["workflow_runs_on_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bump_package is not None:
            self._values["bump_package"] = bump_package
        if jsii_release_version is not None:
            self._values["jsii_release_version"] = jsii_release_version
        if major_version is not None:
            self._values["major_version"] = major_version
        if min_major_version is not None:
            self._values["min_major_version"] = min_major_version
        if next_version_command is not None:
            self._values["next_version_command"] = next_version_command
        if npm_dist_tag is not None:
            self._values["npm_dist_tag"] = npm_dist_tag
        if post_build_steps is not None:
            self._values["post_build_steps"] = post_build_steps
        if prerelease is not None:
            self._values["prerelease"] = prerelease
        if publish_dry_run is not None:
            self._values["publish_dry_run"] = publish_dry_run
        if publish_tasks is not None:
            self._values["publish_tasks"] = publish_tasks
        if releasable_commits is not None:
            self._values["releasable_commits"] = releasable_commits
        if release_branches is not None:
            self._values["release_branches"] = release_branches
        if release_every_commit is not None:
            self._values["release_every_commit"] = release_every_commit
        if release_failure_issue is not None:
            self._values["release_failure_issue"] = release_failure_issue
        if release_failure_issue_label is not None:
            self._values["release_failure_issue_label"] = release_failure_issue_label
        if release_schedule is not None:
            self._values["release_schedule"] = release_schedule
        if release_tag_prefix is not None:
            self._values["release_tag_prefix"] = release_tag_prefix
        if release_trigger is not None:
            self._values["release_trigger"] = release_trigger
        if release_workflow_name is not None:
            self._values["release_workflow_name"] = release_workflow_name
        if release_workflow_setup_steps is not None:
            self._values["release_workflow_setup_steps"] = release_workflow_setup_steps
        if versionrc_options is not None:
            self._values["versionrc_options"] = versionrc_options
        if workflow_container_image is not None:
            self._values["workflow_container_image"] = workflow_container_image
        if workflow_runs_on is not None:
            self._values["workflow_runs_on"] = workflow_runs_on
        if workflow_runs_on_group is not None:
            self._values["workflow_runs_on_group"] = workflow_runs_on_group

    @builtins.property
    def bump_package(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ``commit-and-tag-version`` compatible package used to bump the package version, as a dependency string.

        This can be any compatible package version, including the deprecated ``standard-version@9``.

        :default: - A recent version of "commit-and-tag-version"

        :stability: experimental
        '''
        result = self._values.get("bump_package")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsii_release_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version requirement of ``publib`` which is used to publish modules to npm.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("jsii_release_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Major version to release from the default branch.

        If this is specified, we bump the latest version of this major version line.
        If not specified, we bump the global latest version.

        :default: - Major version is not enforced.

        :stability: experimental
        '''
        result = self._values.get("major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Minimal Major version to release.

        This can be useful to set to 1, as breaking changes before the 1.x major
        release are not incrementing the major version number.

        Can not be set together with ``majorVersion``.

        :default: - No minimum version is being enforced

        :stability: experimental
        '''
        result = self._values.get("min_major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def next_version_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) A shell command to control the next version to release.

        If present, this shell command will be run before the bump is executed, and
        it determines what version to release. It will be executed in the following
        environment:

        - Working directory: the project directory.
        - ``$VERSION``: the current version. Looks like ``1.2.3``.
        - ``$LATEST_TAG``: the most recent tag. Looks like ``prefix-v1.2.3``, or may be unset.
        - ``$SUGGESTED_BUMP``: the suggested bump action based on commits. One of ``major|minor|patch|none``.

        The command should print one of the following to ``stdout``:

        - Nothing: the next version number will be determined based on commit history.
        - ``x.y.z``: the next version number will be ``x.y.z``.
        - ``major|minor|patch``: the next version number will be the current version number
          with the indicated component bumped.

        This setting cannot be specified together with ``minMajorVersion``; the invoked
        script can be used to achieve the effects of ``minMajorVersion``.

        :default: - The next version will be determined based on the commit history and project settings.

        :stability: experimental
        '''
        result = self._values.get("next_version_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_dist_tag(self) -> typing.Optional[builtins.str]:
        '''(experimental) The npmDistTag to use when publishing from the default branch.

        To set the npm dist-tag for release branches, set the ``npmDistTag`` property
        for each branch.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("npm_dist_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_build_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after build as part of the release workflow.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("post_build_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def prerelease(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre").

        :default: - normal semantic versions

        :stability: experimental
        '''
        result = self._values.get("prerelease")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_dry_run(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Instead of actually publishing to package managers, just print the publishing command.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_dry_run")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def publish_tasks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define publishing tasks that can be executed manually as well as workflows.

        Normally, publishing only happens within automated workflows. Enable this
        in order to create a publishing task for each publishing activity.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_tasks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def releasable_commits(self) -> typing.Optional[_ReleasableCommits_d481ce10]:
        '''(experimental) Find commits that should be considered releasable Used to decide if a release is required.

        :default: ReleasableCommits.everyCommit()

        :stability: experimental
        '''
        result = self._values.get("releasable_commits")
        return typing.cast(typing.Optional[_ReleasableCommits_d481ce10], result)

    @builtins.property
    def release_branches(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, BranchOptions]]:
        '''(experimental) Defines additional release branches.

        A workflow will be created for each
        release branch which will publish releases from commits in this branch.
        Each release branch *must* be assigned a major version number which is used
        to enforce that versions published from that branch always use that major
        version. If multiple branches are used, the ``majorVersion`` field must also
        be provided for the default branch.

        :default:

        - no additional branches are used for release. you can use
        ``addBranch()`` to add additional branches.

        :stability: experimental
        '''
        result = self._values.get("release_branches")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, BranchOptions]], result)

    @builtins.property
    def release_every_commit(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``.

        :default: true

        :deprecated: Use ``releaseTrigger: ReleaseTrigger.continuous()`` instead

        :stability: deprecated
        '''
        result = self._values.get("release_every_commit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_failure_issue(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Create a github issue on every failed publishing task.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("release_failure_issue")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_failure_issue_label(self) -> typing.Optional[builtins.str]:
        '''(experimental) The label to apply to issues indicating publish failures.

        Only applies if ``releaseFailureIssue`` is true.

        :default: "failed-release"

        :stability: experimental
        '''
        result = self._values.get("release_failure_issue_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_schedule(self) -> typing.Optional[builtins.str]:
        '''(deprecated) CRON schedule to trigger new releases.

        :default: - no scheduled releases

        :deprecated: Use ``releaseTrigger: ReleaseTrigger.scheduled()`` instead

        :stability: deprecated
        '''
        result = self._values.get("release_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_tag_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers.

        Note: this prefix is used to detect the latest tagged version
        when bumping, so if you change this on a project with an existing version
        history, you may need to manually tag your latest release
        with the new prefix.

        :default: "v"

        :stability: experimental
        '''
        result = self._values.get("release_tag_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_trigger(self) -> typing.Optional["ReleaseTrigger"]:
        '''(experimental) The release trigger to use.

        :default: - Continuous releases (``ReleaseTrigger.continuous()``)

        :stability: experimental
        '''
        result = self._values.get("release_trigger")
        return typing.cast(typing.Optional["ReleaseTrigger"], result)

    @builtins.property
    def release_workflow_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the default release workflow.

        :default: "release"

        :stability: experimental
        '''
        result = self._values.get("release_workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_workflow_setup_steps(
        self,
    ) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) A set of workflow steps to execute in order to setup the workflow container.

        :stability: experimental
        '''
        result = self._values.get("release_workflow_setup_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def versionrc_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Custom configuration used when creating changelog with commit-and-tag-version package.

        Given values either append to default configuration or overwrite values in it.

        :default: - standard configuration applicable for GitHub repositories

        :stability: experimental
        '''
        result = self._values.get("versionrc_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workflow_container_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Container image to use for GitHub workflows.

        :default: - default image

        :stability: experimental
        '''
        result = self._values.get("workflow_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_runs_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Github Runner selection labels.

        :default: ["ubuntu-latest"]

        :stability: experimental
        :description: Defines a target Runner by labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def workflow_runs_on_group(self) -> typing.Optional[_GroupRunnerOptions_148c59c1]:
        '''(experimental) Github Runner Group selection options.

        :stability: experimental
        :description: Defines a target Runner Group by name and/or labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on_group")
        return typing.cast(typing.Optional[_GroupRunnerOptions_148c59c1], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReleaseTrigger(
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.release.ReleaseTrigger",
):
    '''(experimental) Used to manage release strategies.

    This includes release
    and release artifact automation

    :stability: experimental
    '''

    @jsii.member(jsii_name="continuous")
    @builtins.classmethod
    def continuous(
        cls,
        *,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> "ReleaseTrigger":
        '''(experimental) Creates a continuous release trigger.

        Automated releases will occur on every commit.

        :param paths: (experimental) Paths for which pushes should trigger a release.

        :stability: experimental
        '''
        options = ContinuousReleaseOptions(paths=paths)

        return typing.cast("ReleaseTrigger", jsii.sinvoke(cls, "continuous", [options]))

    @jsii.member(jsii_name="manual")
    @builtins.classmethod
    def manual(
        cls,
        *,
        changelog: typing.Optional[builtins.bool] = None,
        changelog_path: typing.Optional[builtins.str] = None,
        git_push_command: typing.Optional[builtins.str] = None,
    ) -> "ReleaseTrigger":
        '''(experimental) Creates a manual release trigger.

        Use this option if you want totally manual releases.

        This will give you a release task that, in addition to the normal
        release activities will trigger a ``publish:git`` task. This task will
        handle project-level changelog management, release tagging, and pushing
        these artifacts to origin.

        The command used for pushing can be customised by specifying
        ``gitPushCommand``. Set to an empty string to disable pushing entirely.

        Simply run ``yarn release`` to trigger a manual release.

        :param changelog: (experimental) Maintain a project-level changelog. Default: true
        :param changelog_path: (experimental) Project-level changelog file path. Ignored if ``changelog`` is false. Default: 'CHANGELOG.md'
        :param git_push_command: (experimental) Override git-push command. Set to an empty string to disable pushing.

        :stability: experimental
        '''
        options = ManualReleaseOptions(
            changelog=changelog,
            changelog_path=changelog_path,
            git_push_command=git_push_command,
        )

        return typing.cast("ReleaseTrigger", jsii.sinvoke(cls, "manual", [options]))

    @jsii.member(jsii_name="scheduled")
    @builtins.classmethod
    def scheduled(cls, *, schedule: builtins.str) -> "ReleaseTrigger":
        '''(experimental) Creates a scheduled release trigger.

        Automated releases will occur based on the provided cron schedule.

        :param schedule: (experimental) Cron schedule for releases. Only defined if this is a scheduled release.

        :stability: experimental
        '''
        options = ScheduledReleaseOptions(schedule=schedule)

        return typing.cast("ReleaseTrigger", jsii.sinvoke(cls, "scheduled", [options]))

    @jsii.member(jsii_name="workflowDispatch")
    @builtins.classmethod
    def workflow_dispatch(cls) -> "ReleaseTrigger":
        '''(experimental) The release can only be triggered using the GitHub UI.

        :stability: experimental
        '''
        return typing.cast("ReleaseTrigger", jsii.sinvoke(cls, "workflowDispatch", []))

    @builtins.property
    @jsii.member(jsii_name="isContinuous")
    def is_continuous(self) -> builtins.bool:
        '''(experimental) Whether or not this is a continuous release.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isContinuous"))

    @builtins.property
    @jsii.member(jsii_name="isManual")
    def is_manual(self) -> builtins.bool:
        '''(experimental) Whether or not this is a release trigger with a manual task run in a working copy.

        If the ``ReleaseTrigger`` is a GitHub-only manual task, this will return ``false``.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isManual"))

    @builtins.property
    @jsii.member(jsii_name="changelogPath")
    def changelog_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Project-level changelog file path.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "changelogPath"))

    @builtins.property
    @jsii.member(jsii_name="gitPushCommand")
    def git_push_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) Override git-push command used when releasing manually.

        Set to an empty string to disable pushing.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gitPushCommand"))

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Paths for which pushes will trigger a release when ``isContinuous`` is ``true``.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "paths"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.Optional[builtins.str]:
        '''(experimental) Cron schedule for releases.

        Only defined if this is a scheduled release.

        :stability: experimental

        Example::

            '0 17 * * *' - every day at 5 pm
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schedule"))


@jsii.data_type(
    jsii_type="projen.release.ScheduledReleaseOptions",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule"},
)
class ScheduledReleaseOptions:
    def __init__(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: (experimental) Cron schedule for releases. Only defined if this is a scheduled release.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__629cc7488dbd6e87168962d964694e088625a8e208d09e45c120eac7e4963baa)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
        }

    @builtins.property
    def schedule(self) -> builtins.str:
        '''(experimental) Cron schedule for releases.

        Only defined if this is a scheduled release.

        :stability: experimental

        Example::

            '0 17 * * *' - every day at 5 pm
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledReleaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.JsiiReleaseMaven",
    jsii_struct_bases=[MavenPublishOptions],
    name_mapping={
        "post_publish_steps": "postPublishSteps",
        "pre_publish_steps": "prePublishSteps",
        "publish_tools": "publishTools",
        "maven_endpoint": "mavenEndpoint",
        "maven_gpg_private_key_passphrase": "mavenGpgPrivateKeyPassphrase",
        "maven_gpg_private_key_secret": "mavenGpgPrivateKeySecret",
        "maven_password": "mavenPassword",
        "maven_repository_url": "mavenRepositoryUrl",
        "maven_server_id": "mavenServerId",
        "maven_staging_profile_id": "mavenStagingProfileId",
        "maven_username": "mavenUsername",
    },
)
class JsiiReleaseMaven(MavenPublishOptions):
    def __init__(
        self,
        *,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
        maven_endpoint: typing.Optional[builtins.str] = None,
        maven_gpg_private_key_passphrase: typing.Optional[builtins.str] = None,
        maven_gpg_private_key_secret: typing.Optional[builtins.str] = None,
        maven_password: typing.Optional[builtins.str] = None,
        maven_repository_url: typing.Optional[builtins.str] = None,
        maven_server_id: typing.Optional[builtins.str] = None,
        maven_staging_profile_id: typing.Optional[builtins.str] = None,
        maven_username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed
        :param maven_endpoint: (experimental) URL of Nexus repository. if not set, defaults to https://oss.sonatype.org Default: "https://oss.sonatype.org"
        :param maven_gpg_private_key_passphrase: (experimental) GitHub secret name which contains the GPG private key or file that includes it. This is used to sign your Maven packages. See instructions. Default: "MAVEN_GPG_PRIVATE_KEY_PASSPHRASE" or not set when using GitHub Packages
        :param maven_gpg_private_key_secret: (experimental) GitHub secret name which contains the GPG private key or file that includes it. This is used to sign your Maven packages. See instructions. Default: "MAVEN_GPG_PRIVATE_KEY" or not set when using GitHub Packages
        :param maven_password: (experimental) GitHub secret name which contains the Password for maven repository. For Maven Central, you will need to Create JIRA account and then request a new project (see links). Default: "MAVEN_PASSWORD" or "GITHUB_TOKEN" when using GitHub Packages
        :param maven_repository_url: (experimental) Deployment repository when not deploying to Maven Central. Default: - not set
        :param maven_server_id: (experimental) Used in maven settings for credential lookup (e.g. use github when publishing to GitHub). Default: "ossrh" (Maven Central) or "github" when using GitHub Packages
        :param maven_staging_profile_id: (experimental) GitHub secret name which contains the Maven Central (sonatype) staging profile ID (e.g. 68a05363083174). Staging profile ID can be found in the URL of the "Releases" staging profile under "Staging Profiles" in https://oss.sonatype.org (e.g. https://oss.sonatype.org/#stagingProfiles;11a33451234521). Default: "MAVEN_STAGING_PROFILE_ID" or not set when using GitHub Packages
        :param maven_username: (experimental) GitHub secret name which contains the Username for maven repository. For Maven Central, you will need to Create JIRA account and then request a new project (see links). Default: "MAVEN_USERNAME" or the GitHub Actor when using GitHub Packages

        :deprecated: Use ``MavenPublishOptions`` instead.

        :stability: deprecated
        '''
        if isinstance(publish_tools, dict):
            publish_tools = _Tools_75b93a2a(**publish_tools)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370b478ebba8352e12c41a67b57d5954055dba8a6ceae59144e72607fdc6df41)
            check_type(argname="argument post_publish_steps", value=post_publish_steps, expected_type=type_hints["post_publish_steps"])
            check_type(argname="argument pre_publish_steps", value=pre_publish_steps, expected_type=type_hints["pre_publish_steps"])
            check_type(argname="argument publish_tools", value=publish_tools, expected_type=type_hints["publish_tools"])
            check_type(argname="argument maven_endpoint", value=maven_endpoint, expected_type=type_hints["maven_endpoint"])
            check_type(argname="argument maven_gpg_private_key_passphrase", value=maven_gpg_private_key_passphrase, expected_type=type_hints["maven_gpg_private_key_passphrase"])
            check_type(argname="argument maven_gpg_private_key_secret", value=maven_gpg_private_key_secret, expected_type=type_hints["maven_gpg_private_key_secret"])
            check_type(argname="argument maven_password", value=maven_password, expected_type=type_hints["maven_password"])
            check_type(argname="argument maven_repository_url", value=maven_repository_url, expected_type=type_hints["maven_repository_url"])
            check_type(argname="argument maven_server_id", value=maven_server_id, expected_type=type_hints["maven_server_id"])
            check_type(argname="argument maven_staging_profile_id", value=maven_staging_profile_id, expected_type=type_hints["maven_staging_profile_id"])
            check_type(argname="argument maven_username", value=maven_username, expected_type=type_hints["maven_username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_publish_steps is not None:
            self._values["post_publish_steps"] = post_publish_steps
        if pre_publish_steps is not None:
            self._values["pre_publish_steps"] = pre_publish_steps
        if publish_tools is not None:
            self._values["publish_tools"] = publish_tools
        if maven_endpoint is not None:
            self._values["maven_endpoint"] = maven_endpoint
        if maven_gpg_private_key_passphrase is not None:
            self._values["maven_gpg_private_key_passphrase"] = maven_gpg_private_key_passphrase
        if maven_gpg_private_key_secret is not None:
            self._values["maven_gpg_private_key_secret"] = maven_gpg_private_key_secret
        if maven_password is not None:
            self._values["maven_password"] = maven_password
        if maven_repository_url is not None:
            self._values["maven_repository_url"] = maven_repository_url
        if maven_server_id is not None:
            self._values["maven_server_id"] = maven_server_id
        if maven_staging_profile_id is not None:
            self._values["maven_staging_profile_id"] = maven_staging_profile_id
        if maven_username is not None:
            self._values["maven_username"] = maven_username

    @builtins.property
    def post_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after executing the publishing command.

        These can be used
        to add/update the release artifacts ot any other tasks needed.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("post_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def pre_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed.

        These steps are executed after ``dist/`` has been populated with the build
        output.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("pre_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def publish_tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Additional tools to install in the publishing job.

        :default: - no additional tools are installed

        :stability: experimental
        '''
        result = self._values.get("publish_tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    @builtins.property
    def maven_endpoint(self) -> typing.Optional[builtins.str]:
        '''(experimental) URL of Nexus repository.

        if not set, defaults to https://oss.sonatype.org

        :default: "https://oss.sonatype.org"

        :stability: experimental
        '''
        result = self._values.get("maven_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_gpg_private_key_passphrase(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret name which contains the GPG private key or file that includes it.

        This is used to sign your Maven packages. See instructions.

        :default: "MAVEN_GPG_PRIVATE_KEY_PASSPHRASE" or not set when using GitHub Packages

        :see: https://github.com/aws/publib#maven
        :stability: experimental
        '''
        result = self._values.get("maven_gpg_private_key_passphrase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_gpg_private_key_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret name which contains the GPG private key or file that includes it.

        This is used to sign your Maven
        packages. See instructions.

        :default: "MAVEN_GPG_PRIVATE_KEY" or not set when using GitHub Packages

        :see: https://github.com/aws/publib#maven
        :stability: experimental
        '''
        result = self._values.get("maven_gpg_private_key_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_password(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret name which contains the Password for maven repository.

        For Maven Central, you will need to Create JIRA account and then request a
        new project (see links).

        :default: "MAVEN_PASSWORD" or "GITHUB_TOKEN" when using GitHub Packages

        :see: https://issues.sonatype.org/secure/CreateIssue.jspa?issuetype=21&pid=10134
        :stability: experimental
        '''
        result = self._values.get("maven_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_repository_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Deployment repository when not deploying to Maven Central.

        :default: - not set

        :stability: experimental
        '''
        result = self._values.get("maven_repository_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_server_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Used in maven settings for credential lookup (e.g. use github when publishing to GitHub).

        :default: "ossrh" (Maven Central) or "github" when using GitHub Packages

        :stability: experimental
        '''
        result = self._values.get("maven_server_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_staging_profile_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret name which contains the Maven Central (sonatype) staging profile ID (e.g. 68a05363083174). Staging profile ID can be found in the URL of the "Releases" staging profile under "Staging Profiles" in https://oss.sonatype.org (e.g. https://oss.sonatype.org/#stagingProfiles;11a33451234521).

        :default: "MAVEN_STAGING_PROFILE_ID" or not set when using GitHub Packages

        :stability: experimental
        '''
        result = self._values.get("maven_staging_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_username(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret name which contains the Username for maven repository.

        For Maven Central, you will need to Create JIRA account and then request a
        new project (see links).

        :default: "MAVEN_USERNAME" or the GitHub Actor when using GitHub Packages

        :see: https://issues.sonatype.org/secure/CreateIssue.jspa?issuetype=21&pid=10134
        :stability: experimental
        '''
        result = self._values.get("maven_username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsiiReleaseMaven(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.JsiiReleaseNpm",
    jsii_struct_bases=[NpmPublishOptions],
    name_mapping={
        "post_publish_steps": "postPublishSteps",
        "pre_publish_steps": "prePublishSteps",
        "publish_tools": "publishTools",
        "code_artifact_options": "codeArtifactOptions",
        "dist_tag": "distTag",
        "npm_provenance": "npmProvenance",
        "npm_token_secret": "npmTokenSecret",
        "registry": "registry",
    },
)
class JsiiReleaseNpm(NpmPublishOptions):
    def __init__(
        self,
        *,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
        code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        dist_tag: typing.Optional[builtins.str] = None,
        npm_provenance: typing.Optional[builtins.bool] = None,
        npm_token_secret: typing.Optional[builtins.str] = None,
        registry: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed
        :param code_artifact_options: (experimental) Options for publishing npm package to AWS CodeArtifact. Default: - undefined
        :param dist_tag: (deprecated) Tags can be used to provide an alias instead of version numbers. For example, a project might choose to have multiple streams of development and use a different tag for each stream, e.g., stable, beta, dev, canary. By default, the ``latest`` tag is used by npm to identify the current version of a package, and ``npm install <pkg>`` (without any ``@<version>`` or ``@<tag>`` specifier) installs the latest tag. Typically, projects only use the ``latest`` tag for stable release versions, and use other tags for unstable versions such as prereleases. The ``next`` tag is used by some projects to identify the upcoming version. Default: "latest"
        :param npm_provenance: (experimental) Should provenance statements be generated when package is published. Note that this component is using ``publib`` to publish packages, which is using npm internally and supports provenance statements independently of the package manager used. Default: - undefined
        :param npm_token_secret: (experimental) GitHub secret which contains the NPM token to use when publishing packages. Default: - "NPM_TOKEN" or "GITHUB_TOKEN" if ``registry`` is set to ``npm.pkg.github.com``.
        :param registry: (experimental) The domain name of the npm package registry. To publish to GitHub Packages, set this value to ``"npm.pkg.github.com"``. In this if ``npmTokenSecret`` is not specified, it will default to ``GITHUB_TOKEN`` which means that you will be able to publish to the repository's package store. In this case, make sure ``repositoryUrl`` is correctly defined. Default: "registry.npmjs.org"

        :deprecated: Use ``NpmPublishOptions`` instead.

        :stability: deprecated
        '''
        if isinstance(publish_tools, dict):
            publish_tools = _Tools_75b93a2a(**publish_tools)
        if isinstance(code_artifact_options, dict):
            code_artifact_options = CodeArtifactOptions(**code_artifact_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34680d3cf9e2cc6374987796717402a524a0bb377e9172f0707da67450b3239)
            check_type(argname="argument post_publish_steps", value=post_publish_steps, expected_type=type_hints["post_publish_steps"])
            check_type(argname="argument pre_publish_steps", value=pre_publish_steps, expected_type=type_hints["pre_publish_steps"])
            check_type(argname="argument publish_tools", value=publish_tools, expected_type=type_hints["publish_tools"])
            check_type(argname="argument code_artifact_options", value=code_artifact_options, expected_type=type_hints["code_artifact_options"])
            check_type(argname="argument dist_tag", value=dist_tag, expected_type=type_hints["dist_tag"])
            check_type(argname="argument npm_provenance", value=npm_provenance, expected_type=type_hints["npm_provenance"])
            check_type(argname="argument npm_token_secret", value=npm_token_secret, expected_type=type_hints["npm_token_secret"])
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_publish_steps is not None:
            self._values["post_publish_steps"] = post_publish_steps
        if pre_publish_steps is not None:
            self._values["pre_publish_steps"] = pre_publish_steps
        if publish_tools is not None:
            self._values["publish_tools"] = publish_tools
        if code_artifact_options is not None:
            self._values["code_artifact_options"] = code_artifact_options
        if dist_tag is not None:
            self._values["dist_tag"] = dist_tag
        if npm_provenance is not None:
            self._values["npm_provenance"] = npm_provenance
        if npm_token_secret is not None:
            self._values["npm_token_secret"] = npm_token_secret
        if registry is not None:
            self._values["registry"] = registry

    @builtins.property
    def post_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after executing the publishing command.

        These can be used
        to add/update the release artifacts ot any other tasks needed.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("post_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def pre_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed.

        These steps are executed after ``dist/`` has been populated with the build
        output.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("pre_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def publish_tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Additional tools to install in the publishing job.

        :default: - no additional tools are installed

        :stability: experimental
        '''
        result = self._values.get("publish_tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    @builtins.property
    def code_artifact_options(self) -> typing.Optional[CodeArtifactOptions]:
        '''(experimental) Options for publishing npm package to AWS CodeArtifact.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("code_artifact_options")
        return typing.cast(typing.Optional[CodeArtifactOptions], result)

    @builtins.property
    def dist_tag(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Tags can be used to provide an alias instead of version numbers.

        For example, a project might choose to have multiple streams of development
        and use a different tag for each stream, e.g., stable, beta, dev, canary.

        By default, the ``latest`` tag is used by npm to identify the current version
        of a package, and ``npm install <pkg>`` (without any ``@<version>`` or ``@<tag>``
        specifier) installs the latest tag. Typically, projects only use the
        ``latest`` tag for stable release versions, and use other tags for unstable
        versions such as prereleases.

        The ``next`` tag is used by some projects to identify the upcoming version.

        :default: "latest"

        :deprecated: Use ``npmDistTag`` for each release branch instead.

        :stability: deprecated
        '''
        result = self._values.get("dist_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_provenance(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Should provenance statements be generated when package is published.

        Note that this component is using ``publib`` to publish packages,
        which is using npm internally and supports provenance statements independently of the package manager used.

        :default: - undefined

        :see: https://docs.npmjs.com/generating-provenance-statements
        :stability: experimental
        '''
        result = self._values.get("npm_provenance")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def npm_token_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the NPM token to use when publishing packages.

        :default: - "NPM_TOKEN" or "GITHUB_TOKEN" if ``registry`` is set to ``npm.pkg.github.com``.

        :stability: experimental
        '''
        result = self._values.get("npm_token_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry(self) -> typing.Optional[builtins.str]:
        '''(experimental) The domain name of the npm package registry.

        To publish to GitHub Packages, set this value to ``"npm.pkg.github.com"``. In
        this if ``npmTokenSecret`` is not specified, it will default to
        ``GITHUB_TOKEN`` which means that you will be able to publish to the
        repository's package store. In this case, make sure ``repositoryUrl`` is
        correctly defined.

        :default: "registry.npmjs.org"

        :stability: experimental

        Example::

            "npm.pkg.github.com"
        '''
        result = self._values.get("registry")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsiiReleaseNpm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.JsiiReleaseNuget",
    jsii_struct_bases=[NugetPublishOptions],
    name_mapping={
        "post_publish_steps": "postPublishSteps",
        "pre_publish_steps": "prePublishSteps",
        "publish_tools": "publishTools",
        "nuget_api_key_secret": "nugetApiKeySecret",
        "nuget_server": "nugetServer",
    },
)
class JsiiReleaseNuget(NugetPublishOptions):
    def __init__(
        self,
        *,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
        nuget_api_key_secret: typing.Optional[builtins.str] = None,
        nuget_server: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed
        :param nuget_api_key_secret: (experimental) GitHub secret which contains the API key for NuGet. Default: "NUGET_API_KEY"
        :param nuget_server: (experimental) NuGet Server URL (defaults to nuget.org).

        :deprecated: Use ``NugetPublishOptions`` instead.

        :stability: deprecated
        '''
        if isinstance(publish_tools, dict):
            publish_tools = _Tools_75b93a2a(**publish_tools)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14abe6d299c2354a8f22a08788f088aafaa8acf2b85b20f297416346274a9b96)
            check_type(argname="argument post_publish_steps", value=post_publish_steps, expected_type=type_hints["post_publish_steps"])
            check_type(argname="argument pre_publish_steps", value=pre_publish_steps, expected_type=type_hints["pre_publish_steps"])
            check_type(argname="argument publish_tools", value=publish_tools, expected_type=type_hints["publish_tools"])
            check_type(argname="argument nuget_api_key_secret", value=nuget_api_key_secret, expected_type=type_hints["nuget_api_key_secret"])
            check_type(argname="argument nuget_server", value=nuget_server, expected_type=type_hints["nuget_server"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_publish_steps is not None:
            self._values["post_publish_steps"] = post_publish_steps
        if pre_publish_steps is not None:
            self._values["pre_publish_steps"] = pre_publish_steps
        if publish_tools is not None:
            self._values["publish_tools"] = publish_tools
        if nuget_api_key_secret is not None:
            self._values["nuget_api_key_secret"] = nuget_api_key_secret
        if nuget_server is not None:
            self._values["nuget_server"] = nuget_server

    @builtins.property
    def post_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after executing the publishing command.

        These can be used
        to add/update the release artifacts ot any other tasks needed.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("post_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def pre_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed.

        These steps are executed after ``dist/`` has been populated with the build
        output.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("pre_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def publish_tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Additional tools to install in the publishing job.

        :default: - no additional tools are installed

        :stability: experimental
        '''
        result = self._values.get("publish_tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    @builtins.property
    def nuget_api_key_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) GitHub secret which contains the API key for NuGet.

        :default: "NUGET_API_KEY"

        :stability: experimental
        '''
        result = self._values.get("nuget_api_key_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nuget_server(self) -> typing.Optional[builtins.str]:
        '''(experimental) NuGet Server URL (defaults to nuget.org).

        :stability: experimental
        '''
        result = self._values.get("nuget_server")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsiiReleaseNuget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.JsiiReleasePyPi",
    jsii_struct_bases=[PyPiPublishOptions],
    name_mapping={
        "post_publish_steps": "postPublishSteps",
        "pre_publish_steps": "prePublishSteps",
        "publish_tools": "publishTools",
        "code_artifact_options": "codeArtifactOptions",
        "twine_password_secret": "twinePasswordSecret",
        "twine_registry_url": "twineRegistryUrl",
        "twine_username_secret": "twineUsernameSecret",
    },
)
class JsiiReleasePyPi(PyPiPublishOptions):
    def __init__(
        self,
        *,
        post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
        code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        twine_password_secret: typing.Optional[builtins.str] = None,
        twine_registry_url: typing.Optional[builtins.str] = None,
        twine_username_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param post_publish_steps: (experimental) Steps to execute after executing the publishing command. These can be used to add/update the release artifacts ot any other tasks needed. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.
        :param pre_publish_steps: (experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed. These steps are executed after ``dist/`` has been populated with the build output. Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.
        :param publish_tools: (experimental) Additional tools to install in the publishing job. Default: - no additional tools are installed
        :param code_artifact_options: (experimental) Options for publishing to AWS CodeArtifact. Default: - undefined
        :param twine_password_secret: (experimental) The GitHub secret which contains PyPI password. Default: "TWINE_PASSWORD"
        :param twine_registry_url: (experimental) The registry url to use when releasing packages. Default: - twine default
        :param twine_username_secret: (experimental) The GitHub secret which contains PyPI user name. Default: "TWINE_USERNAME"

        :deprecated: Use ``PyPiPublishOptions`` instead.

        :stability: deprecated
        '''
        if isinstance(publish_tools, dict):
            publish_tools = _Tools_75b93a2a(**publish_tools)
        if isinstance(code_artifact_options, dict):
            code_artifact_options = CodeArtifactOptions(**code_artifact_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa7c01cc40634bf771011bf4e8ddb9e3be28efd1b3f15b5d0768a4e810d37bc)
            check_type(argname="argument post_publish_steps", value=post_publish_steps, expected_type=type_hints["post_publish_steps"])
            check_type(argname="argument pre_publish_steps", value=pre_publish_steps, expected_type=type_hints["pre_publish_steps"])
            check_type(argname="argument publish_tools", value=publish_tools, expected_type=type_hints["publish_tools"])
            check_type(argname="argument code_artifact_options", value=code_artifact_options, expected_type=type_hints["code_artifact_options"])
            check_type(argname="argument twine_password_secret", value=twine_password_secret, expected_type=type_hints["twine_password_secret"])
            check_type(argname="argument twine_registry_url", value=twine_registry_url, expected_type=type_hints["twine_registry_url"])
            check_type(argname="argument twine_username_secret", value=twine_username_secret, expected_type=type_hints["twine_username_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_publish_steps is not None:
            self._values["post_publish_steps"] = post_publish_steps
        if pre_publish_steps is not None:
            self._values["pre_publish_steps"] = pre_publish_steps
        if publish_tools is not None:
            self._values["publish_tools"] = publish_tools
        if code_artifact_options is not None:
            self._values["code_artifact_options"] = code_artifact_options
        if twine_password_secret is not None:
            self._values["twine_password_secret"] = twine_password_secret
        if twine_registry_url is not None:
            self._values["twine_registry_url"] = twine_registry_url
        if twine_username_secret is not None:
            self._values["twine_username_secret"] = twine_username_secret

    @builtins.property
    def post_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after executing the publishing command.

        These can be used
        to add/update the release artifacts ot any other tasks needed.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPostPublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("post_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def pre_publish_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute before executing the publishing command. These can be used to prepare the artifact for publishing if needed.

        These steps are executed after ``dist/`` has been populated with the build
        output.

        Note that when using this in ``publishToGitHubReleases`` this will override steps added via ``addGitHubPrePublishingSteps``.

        :stability: experimental
        '''
        result = self._values.get("pre_publish_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def publish_tools(self) -> typing.Optional[_Tools_75b93a2a]:
        '''(experimental) Additional tools to install in the publishing job.

        :default: - no additional tools are installed

        :stability: experimental
        '''
        result = self._values.get("publish_tools")
        return typing.cast(typing.Optional[_Tools_75b93a2a], result)

    @builtins.property
    def code_artifact_options(self) -> typing.Optional[CodeArtifactOptions]:
        '''(experimental) Options for publishing to AWS CodeArtifact.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("code_artifact_options")
        return typing.cast(typing.Optional[CodeArtifactOptions], result)

    @builtins.property
    def twine_password_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub secret which contains PyPI password.

        :default: "TWINE_PASSWORD"

        :stability: experimental
        '''
        result = self._values.get("twine_password_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twine_registry_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The registry url to use when releasing packages.

        :default: - twine default

        :stability: experimental
        '''
        result = self._values.get("twine_registry_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twine_username_secret(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub secret which contains PyPI user name.

        :default: "TWINE_USERNAME"

        :stability: experimental
        '''
        result = self._values.get("twine_username_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsiiReleasePyPi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.release.ReleaseOptions",
    jsii_struct_bases=[ReleaseProjectOptions],
    name_mapping={
        "bump_package": "bumpPackage",
        "jsii_release_version": "jsiiReleaseVersion",
        "major_version": "majorVersion",
        "min_major_version": "minMajorVersion",
        "next_version_command": "nextVersionCommand",
        "npm_dist_tag": "npmDistTag",
        "post_build_steps": "postBuildSteps",
        "prerelease": "prerelease",
        "publish_dry_run": "publishDryRun",
        "publish_tasks": "publishTasks",
        "releasable_commits": "releasableCommits",
        "release_branches": "releaseBranches",
        "release_every_commit": "releaseEveryCommit",
        "release_failure_issue": "releaseFailureIssue",
        "release_failure_issue_label": "releaseFailureIssueLabel",
        "release_schedule": "releaseSchedule",
        "release_tag_prefix": "releaseTagPrefix",
        "release_trigger": "releaseTrigger",
        "release_workflow_name": "releaseWorkflowName",
        "release_workflow_setup_steps": "releaseWorkflowSetupSteps",
        "versionrc_options": "versionrcOptions",
        "workflow_container_image": "workflowContainerImage",
        "workflow_runs_on": "workflowRunsOn",
        "workflow_runs_on_group": "workflowRunsOnGroup",
        "artifacts_directory": "artifactsDirectory",
        "branch": "branch",
        "task": "task",
        "version_file": "versionFile",
        "github_release": "githubRelease",
        "workflow_node_version": "workflowNodeVersion",
        "workflow_permissions": "workflowPermissions",
    },
)
class ReleaseOptions(ReleaseProjectOptions):
    def __init__(
        self,
        *,
        bump_package: typing.Optional[builtins.str] = None,
        jsii_release_version: typing.Optional[builtins.str] = None,
        major_version: typing.Optional[jsii.Number] = None,
        min_major_version: typing.Optional[jsii.Number] = None,
        next_version_command: typing.Optional[builtins.str] = None,
        npm_dist_tag: typing.Optional[builtins.str] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        prerelease: typing.Optional[builtins.str] = None,
        publish_dry_run: typing.Optional[builtins.bool] = None,
        publish_tasks: typing.Optional[builtins.bool] = None,
        releasable_commits: typing.Optional[_ReleasableCommits_d481ce10] = None,
        release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        release_every_commit: typing.Optional[builtins.bool] = None,
        release_failure_issue: typing.Optional[builtins.bool] = None,
        release_failure_issue_label: typing.Optional[builtins.str] = None,
        release_schedule: typing.Optional[builtins.str] = None,
        release_tag_prefix: typing.Optional[builtins.str] = None,
        release_trigger: typing.Optional[ReleaseTrigger] = None,
        release_workflow_name: typing.Optional[builtins.str] = None,
        release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
        versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        workflow_container_image: typing.Optional[builtins.str] = None,
        workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
        artifacts_directory: builtins.str,
        branch: builtins.str,
        task: _Task_9fa875b6,
        version_file: builtins.str,
        github_release: typing.Optional[builtins.bool] = None,
        workflow_node_version: typing.Optional[builtins.str] = None,
        workflow_permissions: typing.Optional[typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for ``Release``.

        :param bump_package: (experimental) The ``commit-and-tag-version`` compatible package used to bump the package version, as a dependency string. This can be any compatible package version, including the deprecated ``standard-version@9``. Default: - A recent version of "commit-and-tag-version"
        :param jsii_release_version: (experimental) Version requirement of ``publib`` which is used to publish modules to npm. Default: "latest"
        :param major_version: (experimental) Major version to release from the default branch. If this is specified, we bump the latest version of this major version line. If not specified, we bump the global latest version. Default: - Major version is not enforced.
        :param min_major_version: (experimental) Minimal Major version to release. This can be useful to set to 1, as breaking changes before the 1.x major release are not incrementing the major version number. Can not be set together with ``majorVersion``. Default: - No minimum version is being enforced
        :param next_version_command: (experimental) A shell command to control the next version to release. If present, this shell command will be run before the bump is executed, and it determines what version to release. It will be executed in the following environment: - Working directory: the project directory. - ``$VERSION``: the current version. Looks like ``1.2.3``. - ``$LATEST_TAG``: the most recent tag. Looks like ``prefix-v1.2.3``, or may be unset. - ``$SUGGESTED_BUMP``: the suggested bump action based on commits. One of ``major|minor|patch|none``. The command should print one of the following to ``stdout``: - Nothing: the next version number will be determined based on commit history. - ``x.y.z``: the next version number will be ``x.y.z``. - ``major|minor|patch``: the next version number will be the current version number with the indicated component bumped. This setting cannot be specified together with ``minMajorVersion``; the invoked script can be used to achieve the effects of ``minMajorVersion``. Default: - The next version will be determined based on the commit history and project settings.
        :param npm_dist_tag: (experimental) The npmDistTag to use when publishing from the default branch. To set the npm dist-tag for release branches, set the ``npmDistTag`` property for each branch. Default: "latest"
        :param post_build_steps: (experimental) Steps to execute after build as part of the release workflow. Default: []
        :param prerelease: (experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre"). Default: - normal semantic versions
        :param publish_dry_run: (experimental) Instead of actually publishing to package managers, just print the publishing command. Default: false
        :param publish_tasks: (experimental) Define publishing tasks that can be executed manually as well as workflows. Normally, publishing only happens within automated workflows. Enable this in order to create a publishing task for each publishing activity. Default: false
        :param releasable_commits: (experimental) Find commits that should be considered releasable Used to decide if a release is required. Default: ReleasableCommits.everyCommit()
        :param release_branches: (experimental) Defines additional release branches. A workflow will be created for each release branch which will publish releases from commits in this branch. Each release branch *must* be assigned a major version number which is used to enforce that versions published from that branch always use that major version. If multiple branches are used, the ``majorVersion`` field must also be provided for the default branch. Default: - no additional branches are used for release. you can use ``addBranch()`` to add additional branches.
        :param release_every_commit: (deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``. Default: true
        :param release_failure_issue: (experimental) Create a github issue on every failed publishing task. Default: false
        :param release_failure_issue_label: (experimental) The label to apply to issues indicating publish failures. Only applies if ``releaseFailureIssue`` is true. Default: "failed-release"
        :param release_schedule: (deprecated) CRON schedule to trigger new releases. Default: - no scheduled releases
        :param release_tag_prefix: (experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers. Note: this prefix is used to detect the latest tagged version when bumping, so if you change this on a project with an existing version history, you may need to manually tag your latest release with the new prefix. Default: "v"
        :param release_trigger: (experimental) The release trigger to use. Default: - Continuous releases (``ReleaseTrigger.continuous()``)
        :param release_workflow_name: (experimental) The name of the default release workflow. Default: "release"
        :param release_workflow_setup_steps: (experimental) A set of workflow steps to execute in order to setup the workflow container.
        :param versionrc_options: (experimental) Custom configuration used when creating changelog with commit-and-tag-version package. Given values either append to default configuration or overwrite values in it. Default: - standard configuration applicable for GitHub repositories
        :param workflow_container_image: (experimental) Container image to use for GitHub workflows. Default: - default image
        :param workflow_runs_on: (experimental) Github Runner selection labels. Default: ["ubuntu-latest"]
        :param workflow_runs_on_group: (experimental) Github Runner Group selection options.
        :param artifacts_directory: (experimental) A directory which will contain build artifacts. Default: "dist"
        :param branch: (experimental) The default branch name to release from. Use ``majorVersion`` to restrict this branch to only publish releases with a specific major version. You can add additional branches using ``addBranch()``.
        :param task: (experimental) The task to execute in order to create the release artifacts. Artifacts are expected to reside under ``artifactsDirectory`` (defaults to ``dist/``) once build is complete.
        :param version_file: (experimental) A name of a .json file to set the ``version`` field in after a bump.
        :param github_release: (experimental) Create a GitHub release for each release. Default: true
        :param workflow_node_version: (experimental) Node version to setup in GitHub workflows if any node-based CLI utilities are needed. For example ``publib``, the CLI projen uses to publish releases, is an npm library. Default: "lts/*""
        :param workflow_permissions: (experimental) Permissions granted to the release workflow job. Default: ``{ contents: JobPermission.WRITE }``

        :stability: experimental
        '''
        if isinstance(workflow_runs_on_group, dict):
            workflow_runs_on_group = _GroupRunnerOptions_148c59c1(**workflow_runs_on_group)
        if isinstance(workflow_permissions, dict):
            workflow_permissions = _JobPermissions_3b5b53dc(**workflow_permissions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcbb9106f2fe858c4efa7a5934906e63b00b56fa33c47c5f910dac2a904f472)
            check_type(argname="argument bump_package", value=bump_package, expected_type=type_hints["bump_package"])
            check_type(argname="argument jsii_release_version", value=jsii_release_version, expected_type=type_hints["jsii_release_version"])
            check_type(argname="argument major_version", value=major_version, expected_type=type_hints["major_version"])
            check_type(argname="argument min_major_version", value=min_major_version, expected_type=type_hints["min_major_version"])
            check_type(argname="argument next_version_command", value=next_version_command, expected_type=type_hints["next_version_command"])
            check_type(argname="argument npm_dist_tag", value=npm_dist_tag, expected_type=type_hints["npm_dist_tag"])
            check_type(argname="argument post_build_steps", value=post_build_steps, expected_type=type_hints["post_build_steps"])
            check_type(argname="argument prerelease", value=prerelease, expected_type=type_hints["prerelease"])
            check_type(argname="argument publish_dry_run", value=publish_dry_run, expected_type=type_hints["publish_dry_run"])
            check_type(argname="argument publish_tasks", value=publish_tasks, expected_type=type_hints["publish_tasks"])
            check_type(argname="argument releasable_commits", value=releasable_commits, expected_type=type_hints["releasable_commits"])
            check_type(argname="argument release_branches", value=release_branches, expected_type=type_hints["release_branches"])
            check_type(argname="argument release_every_commit", value=release_every_commit, expected_type=type_hints["release_every_commit"])
            check_type(argname="argument release_failure_issue", value=release_failure_issue, expected_type=type_hints["release_failure_issue"])
            check_type(argname="argument release_failure_issue_label", value=release_failure_issue_label, expected_type=type_hints["release_failure_issue_label"])
            check_type(argname="argument release_schedule", value=release_schedule, expected_type=type_hints["release_schedule"])
            check_type(argname="argument release_tag_prefix", value=release_tag_prefix, expected_type=type_hints["release_tag_prefix"])
            check_type(argname="argument release_trigger", value=release_trigger, expected_type=type_hints["release_trigger"])
            check_type(argname="argument release_workflow_name", value=release_workflow_name, expected_type=type_hints["release_workflow_name"])
            check_type(argname="argument release_workflow_setup_steps", value=release_workflow_setup_steps, expected_type=type_hints["release_workflow_setup_steps"])
            check_type(argname="argument versionrc_options", value=versionrc_options, expected_type=type_hints["versionrc_options"])
            check_type(argname="argument workflow_container_image", value=workflow_container_image, expected_type=type_hints["workflow_container_image"])
            check_type(argname="argument workflow_runs_on", value=workflow_runs_on, expected_type=type_hints["workflow_runs_on"])
            check_type(argname="argument workflow_runs_on_group", value=workflow_runs_on_group, expected_type=type_hints["workflow_runs_on_group"])
            check_type(argname="argument artifacts_directory", value=artifacts_directory, expected_type=type_hints["artifacts_directory"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument task", value=task, expected_type=type_hints["task"])
            check_type(argname="argument version_file", value=version_file, expected_type=type_hints["version_file"])
            check_type(argname="argument github_release", value=github_release, expected_type=type_hints["github_release"])
            check_type(argname="argument workflow_node_version", value=workflow_node_version, expected_type=type_hints["workflow_node_version"])
            check_type(argname="argument workflow_permissions", value=workflow_permissions, expected_type=type_hints["workflow_permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifacts_directory": artifacts_directory,
            "branch": branch,
            "task": task,
            "version_file": version_file,
        }
        if bump_package is not None:
            self._values["bump_package"] = bump_package
        if jsii_release_version is not None:
            self._values["jsii_release_version"] = jsii_release_version
        if major_version is not None:
            self._values["major_version"] = major_version
        if min_major_version is not None:
            self._values["min_major_version"] = min_major_version
        if next_version_command is not None:
            self._values["next_version_command"] = next_version_command
        if npm_dist_tag is not None:
            self._values["npm_dist_tag"] = npm_dist_tag
        if post_build_steps is not None:
            self._values["post_build_steps"] = post_build_steps
        if prerelease is not None:
            self._values["prerelease"] = prerelease
        if publish_dry_run is not None:
            self._values["publish_dry_run"] = publish_dry_run
        if publish_tasks is not None:
            self._values["publish_tasks"] = publish_tasks
        if releasable_commits is not None:
            self._values["releasable_commits"] = releasable_commits
        if release_branches is not None:
            self._values["release_branches"] = release_branches
        if release_every_commit is not None:
            self._values["release_every_commit"] = release_every_commit
        if release_failure_issue is not None:
            self._values["release_failure_issue"] = release_failure_issue
        if release_failure_issue_label is not None:
            self._values["release_failure_issue_label"] = release_failure_issue_label
        if release_schedule is not None:
            self._values["release_schedule"] = release_schedule
        if release_tag_prefix is not None:
            self._values["release_tag_prefix"] = release_tag_prefix
        if release_trigger is not None:
            self._values["release_trigger"] = release_trigger
        if release_workflow_name is not None:
            self._values["release_workflow_name"] = release_workflow_name
        if release_workflow_setup_steps is not None:
            self._values["release_workflow_setup_steps"] = release_workflow_setup_steps
        if versionrc_options is not None:
            self._values["versionrc_options"] = versionrc_options
        if workflow_container_image is not None:
            self._values["workflow_container_image"] = workflow_container_image
        if workflow_runs_on is not None:
            self._values["workflow_runs_on"] = workflow_runs_on
        if workflow_runs_on_group is not None:
            self._values["workflow_runs_on_group"] = workflow_runs_on_group
        if github_release is not None:
            self._values["github_release"] = github_release
        if workflow_node_version is not None:
            self._values["workflow_node_version"] = workflow_node_version
        if workflow_permissions is not None:
            self._values["workflow_permissions"] = workflow_permissions

    @builtins.property
    def bump_package(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ``commit-and-tag-version`` compatible package used to bump the package version, as a dependency string.

        This can be any compatible package version, including the deprecated ``standard-version@9``.

        :default: - A recent version of "commit-and-tag-version"

        :stability: experimental
        '''
        result = self._values.get("bump_package")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jsii_release_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Version requirement of ``publib`` which is used to publish modules to npm.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("jsii_release_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Major version to release from the default branch.

        If this is specified, we bump the latest version of this major version line.
        If not specified, we bump the global latest version.

        :default: - Major version is not enforced.

        :stability: experimental
        '''
        result = self._values.get("major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_major_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Minimal Major version to release.

        This can be useful to set to 1, as breaking changes before the 1.x major
        release are not incrementing the major version number.

        Can not be set together with ``majorVersion``.

        :default: - No minimum version is being enforced

        :stability: experimental
        '''
        result = self._values.get("min_major_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def next_version_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) A shell command to control the next version to release.

        If present, this shell command will be run before the bump is executed, and
        it determines what version to release. It will be executed in the following
        environment:

        - Working directory: the project directory.
        - ``$VERSION``: the current version. Looks like ``1.2.3``.
        - ``$LATEST_TAG``: the most recent tag. Looks like ``prefix-v1.2.3``, or may be unset.
        - ``$SUGGESTED_BUMP``: the suggested bump action based on commits. One of ``major|minor|patch|none``.

        The command should print one of the following to ``stdout``:

        - Nothing: the next version number will be determined based on commit history.
        - ``x.y.z``: the next version number will be ``x.y.z``.
        - ``major|minor|patch``: the next version number will be the current version number
          with the indicated component bumped.

        This setting cannot be specified together with ``minMajorVersion``; the invoked
        script can be used to achieve the effects of ``minMajorVersion``.

        :default: - The next version will be determined based on the commit history and project settings.

        :stability: experimental
        '''
        result = self._values.get("next_version_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def npm_dist_tag(self) -> typing.Optional[builtins.str]:
        '''(experimental) The npmDistTag to use when publishing from the default branch.

        To set the npm dist-tag for release branches, set the ``npmDistTag`` property
        for each branch.

        :default: "latest"

        :stability: experimental
        '''
        result = self._values.get("npm_dist_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_build_steps(self) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) Steps to execute after build as part of the release workflow.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("post_build_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def prerelease(self) -> typing.Optional[builtins.str]:
        '''(experimental) Bump versions from the default branch as pre-releases (e.g. "beta", "alpha", "pre").

        :default: - normal semantic versions

        :stability: experimental
        '''
        result = self._values.get("prerelease")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_dry_run(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Instead of actually publishing to package managers, just print the publishing command.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_dry_run")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def publish_tasks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Define publishing tasks that can be executed manually as well as workflows.

        Normally, publishing only happens within automated workflows. Enable this
        in order to create a publishing task for each publishing activity.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("publish_tasks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def releasable_commits(self) -> typing.Optional[_ReleasableCommits_d481ce10]:
        '''(experimental) Find commits that should be considered releasable Used to decide if a release is required.

        :default: ReleasableCommits.everyCommit()

        :stability: experimental
        '''
        result = self._values.get("releasable_commits")
        return typing.cast(typing.Optional[_ReleasableCommits_d481ce10], result)

    @builtins.property
    def release_branches(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, BranchOptions]]:
        '''(experimental) Defines additional release branches.

        A workflow will be created for each
        release branch which will publish releases from commits in this branch.
        Each release branch *must* be assigned a major version number which is used
        to enforce that versions published from that branch always use that major
        version. If multiple branches are used, the ``majorVersion`` field must also
        be provided for the default branch.

        :default:

        - no additional branches are used for release. you can use
        ``addBranch()`` to add additional branches.

        :stability: experimental
        '''
        result = self._values.get("release_branches")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, BranchOptions]], result)

    @builtins.property
    def release_every_commit(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Automatically release new versions every commit to one of branches in ``releaseBranches``.

        :default: true

        :deprecated: Use ``releaseTrigger: ReleaseTrigger.continuous()`` instead

        :stability: deprecated
        '''
        result = self._values.get("release_every_commit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_failure_issue(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Create a github issue on every failed publishing task.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("release_failure_issue")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def release_failure_issue_label(self) -> typing.Optional[builtins.str]:
        '''(experimental) The label to apply to issues indicating publish failures.

        Only applies if ``releaseFailureIssue`` is true.

        :default: "failed-release"

        :stability: experimental
        '''
        result = self._values.get("release_failure_issue_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_schedule(self) -> typing.Optional[builtins.str]:
        '''(deprecated) CRON schedule to trigger new releases.

        :default: - no scheduled releases

        :deprecated: Use ``releaseTrigger: ReleaseTrigger.scheduled()`` instead

        :stability: deprecated
        '''
        result = self._values.get("release_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_tag_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Automatically add the given prefix to release tags. Useful if you are releasing on multiple branches with overlapping version numbers.

        Note: this prefix is used to detect the latest tagged version
        when bumping, so if you change this on a project with an existing version
        history, you may need to manually tag your latest release
        with the new prefix.

        :default: "v"

        :stability: experimental
        '''
        result = self._values.get("release_tag_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_trigger(self) -> typing.Optional[ReleaseTrigger]:
        '''(experimental) The release trigger to use.

        :default: - Continuous releases (``ReleaseTrigger.continuous()``)

        :stability: experimental
        '''
        result = self._values.get("release_trigger")
        return typing.cast(typing.Optional[ReleaseTrigger], result)

    @builtins.property
    def release_workflow_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the default release workflow.

        :default: "release"

        :stability: experimental
        '''
        result = self._values.get("release_workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_workflow_setup_steps(
        self,
    ) -> typing.Optional[typing.List[_JobStep_c3287c05]]:
        '''(experimental) A set of workflow steps to execute in order to setup the workflow container.

        :stability: experimental
        '''
        result = self._values.get("release_workflow_setup_steps")
        return typing.cast(typing.Optional[typing.List[_JobStep_c3287c05]], result)

    @builtins.property
    def versionrc_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Custom configuration used when creating changelog with commit-and-tag-version package.

        Given values either append to default configuration or overwrite values in it.

        :default: - standard configuration applicable for GitHub repositories

        :stability: experimental
        '''
        result = self._values.get("versionrc_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def workflow_container_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Container image to use for GitHub workflows.

        :default: - default image

        :stability: experimental
        '''
        result = self._values.get("workflow_container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_runs_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Github Runner selection labels.

        :default: ["ubuntu-latest"]

        :stability: experimental
        :description: Defines a target Runner by labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def workflow_runs_on_group(self) -> typing.Optional[_GroupRunnerOptions_148c59c1]:
        '''(experimental) Github Runner Group selection options.

        :stability: experimental
        :description: Defines a target Runner Group by name and/or labels
        :throws: {Error} if both ``runsOn`` and ``runsOnGroup`` are specified
        '''
        result = self._values.get("workflow_runs_on_group")
        return typing.cast(typing.Optional[_GroupRunnerOptions_148c59c1], result)

    @builtins.property
    def artifacts_directory(self) -> builtins.str:
        '''(experimental) A directory which will contain build artifacts.

        :default: "dist"

        :stability: experimental
        '''
        result = self._values.get("artifacts_directory")
        assert result is not None, "Required property 'artifacts_directory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch(self) -> builtins.str:
        '''(experimental) The default branch name to release from.

        Use ``majorVersion`` to restrict this branch to only publish releases with a
        specific major version.

        You can add additional branches using ``addBranch()``.

        :stability: experimental
        '''
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def task(self) -> _Task_9fa875b6:
        '''(experimental) The task to execute in order to create the release artifacts.

        Artifacts are
        expected to reside under ``artifactsDirectory`` (defaults to ``dist/``) once
        build is complete.

        :stability: experimental
        '''
        result = self._values.get("task")
        assert result is not None, "Required property 'task' is missing"
        return typing.cast(_Task_9fa875b6, result)

    @builtins.property
    def version_file(self) -> builtins.str:
        '''(experimental) A name of a .json file to set the ``version`` field in after a bump.

        :stability: experimental

        Example::

            "package.json"
        '''
        result = self._values.get("version_file")
        assert result is not None, "Required property 'version_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def github_release(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Create a GitHub release for each release.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("github_release")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def workflow_node_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) Node version to setup in GitHub workflows if any node-based CLI utilities are needed.

        For example ``publib``, the CLI projen uses to publish releases,
        is an npm library.

        :default: "lts/*""

        :stability: experimental
        '''
        result = self._values.get("workflow_node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_permissions(self) -> typing.Optional[_JobPermissions_3b5b53dc]:
        '''(experimental) Permissions granted to the release workflow job.

        :default: ``{ contents: JobPermission.WRITE }``

        :stability: experimental
        '''
        result = self._values.get("workflow_permissions")
        return typing.cast(typing.Optional[_JobPermissions_3b5b53dc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BranchOptions",
    "CodeArtifactAuthProvider",
    "CodeArtifactOptions",
    "CommonPublishOptions",
    "ContinuousReleaseOptions",
    "GitHubReleasesPublishOptions",
    "GitPublishOptions",
    "GoPublishOptions",
    "JsiiReleaseGo",
    "JsiiReleaseMaven",
    "JsiiReleaseNpm",
    "JsiiReleaseNuget",
    "JsiiReleasePyPi",
    "ManualReleaseOptions",
    "MavenPublishOptions",
    "NpmPublishOptions",
    "NugetPublishOptions",
    "Publisher",
    "PublisherOptions",
    "PyPiPublishOptions",
    "Release",
    "ReleaseOptions",
    "ReleaseProjectOptions",
    "ReleaseTrigger",
    "ScheduledReleaseOptions",
]

publication.publish()

def _typecheckingstub__6f62eb98000deee3820f046309b2262c5063c0cb9581232fd1a44731f86986d7(
    *,
    major_version: jsii.Number,
    min_major_version: typing.Optional[jsii.Number] = None,
    minor_version: typing.Optional[jsii.Number] = None,
    npm_dist_tag: typing.Optional[builtins.str] = None,
    prerelease: typing.Optional[builtins.str] = None,
    tag_prefix: typing.Optional[builtins.str] = None,
    workflow_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a328fe64db40633fedae889a7376e6885e1983f57d171d4f4ef85af668fafdb(
    *,
    access_key_id_secret: typing.Optional[builtins.str] = None,
    auth_provider: typing.Optional[CodeArtifactAuthProvider] = None,
    role_to_assume: typing.Optional[builtins.str] = None,
    secret_access_key_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9603f09b67279d5ef3dc921367168d873983210161b1d6382c369d0b9ec13b0a(
    *,
    post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b36779f92c5190c3ac9d8a636a537bfe6ebc844a55942ee5dfc0a9656d6192(
    *,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7008ba35b00dedc375d87db7a317e8f077475b6a4e334303337c92bb77171fb(
    *,
    post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    changelog_file: builtins.str,
    release_tag_file: builtins.str,
    version_file: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5537e1435c9eea568279fa140de950e1b7275db307b374195986186386d7704(
    *,
    changelog_file: builtins.str,
    release_tag_file: builtins.str,
    version_file: builtins.str,
    git_branch: typing.Optional[builtins.str] = None,
    git_push_command: typing.Optional[builtins.str] = None,
    project_changelog_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a5b8a4f17bcea99089b42477d5b778fd3a9066d3d1126736ccf21a9c44bfbc(
    *,
    post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    git_branch: typing.Optional[builtins.str] = None,
    git_commit_message: typing.Optional[builtins.str] = None,
    github_deploy_key_secret: typing.Optional[builtins.str] = None,
    github_token_secret: typing.Optional[builtins.str] = None,
    github_use_ssh: typing.Optional[builtins.bool] = None,
    git_user_email: typing.Optional[builtins.str] = None,
    git_user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bae65cd3313afa37ada6dbaab99141ff7744458e985bc9c53faa021220e167(
    *,
    post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    git_branch: typing.Optional[builtins.str] = None,
    git_commit_message: typing.Optional[builtins.str] = None,
    github_deploy_key_secret: typing.Optional[builtins.str] = None,
    github_token_secret: typing.Optional[builtins.str] = None,
    github_use_ssh: typing.Optional[builtins.bool] = None,
    git_user_email: typing.Optional[builtins.str] = None,
    git_user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2492d83058b766179e85fd785d08928e38b53ce70b0f2dc9a1c5edccb668b930(
    *,
    changelog: typing.Optional[builtins.bool] = None,
    changelog_path: typing.Optional[builtins.str] = None,
    git_push_command: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2d55bfa47dd9e6869b7f55b573dea54539ab2e9b833766e4140d6d4c4c3d7e(
    *,
    post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    maven_endpoint: typing.Optional[builtins.str] = None,
    maven_gpg_private_key_passphrase: typing.Optional[builtins.str] = None,
    maven_gpg_private_key_secret: typing.Optional[builtins.str] = None,
    maven_password: typing.Optional[builtins.str] = None,
    maven_repository_url: typing.Optional[builtins.str] = None,
    maven_server_id: typing.Optional[builtins.str] = None,
    maven_staging_profile_id: typing.Optional[builtins.str] = None,
    maven_username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458289050585e6e895f9ee709ee4e102166b0f71e3c8b2a0617efa2d24e990fb(
    *,
    post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    dist_tag: typing.Optional[builtins.str] = None,
    npm_provenance: typing.Optional[builtins.bool] = None,
    npm_token_secret: typing.Optional[builtins.str] = None,
    registry: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584d4125e43e970396e9062b357de30ef32a6d1b30bd3a0f00fc7db041ea0bec(
    *,
    post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    nuget_api_key_secret: typing.Optional[builtins.str] = None,
    nuget_server: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee2fd880a34190cc3f39bd885d4276ff656803edbfe41e03f405df373cf1886(
    project: _Project_57d89203,
    *,
    artifact_name: builtins.str,
    build_job_id: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    dry_run: typing.Optional[builtins.bool] = None,
    failure_issue: typing.Optional[builtins.bool] = None,
    failure_issue_label: typing.Optional[builtins.str] = None,
    jsii_release_version: typing.Optional[builtins.str] = None,
    publib_version: typing.Optional[builtins.str] = None,
    publish_tasks: typing.Optional[builtins.bool] = None,
    workflow_container_image: typing.Optional[builtins.str] = None,
    workflow_node_version: typing.Optional[builtins.str] = None,
    workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc29acfacedcf962e3aef9229c52a0b3f87bcc40c48ec3ef2bb7b9aff15cdf4(
    *steps: _JobStep_c3287c05,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92bbbd5b910dba917f337b84006ddf331f055b5c222b506b0599fb0a9ed444e5(
    *steps: _JobStep_c3287c05,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e430972b008e5968049196f964ee9dfa036c68b2195f125119bc2629263e791(
    *,
    artifact_name: builtins.str,
    build_job_id: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    dry_run: typing.Optional[builtins.bool] = None,
    failure_issue: typing.Optional[builtins.bool] = None,
    failure_issue_label: typing.Optional[builtins.str] = None,
    jsii_release_version: typing.Optional[builtins.str] = None,
    publib_version: typing.Optional[builtins.str] = None,
    publish_tasks: typing.Optional[builtins.bool] = None,
    workflow_container_image: typing.Optional[builtins.str] = None,
    workflow_node_version: typing.Optional[builtins.str] = None,
    workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90cd44def59be822b686bcd759d7f0a910b9936ca8acc0ef3e69cda5ddc21d2(
    *,
    post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    twine_password_secret: typing.Optional[builtins.str] = None,
    twine_registry_url: typing.Optional[builtins.str] = None,
    twine_username_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b447ecb34d36869391ee159467e6c78b74da704722d4c6a517e05bbae9016464(
    scope: _constructs_77d1e7e8.IConstruct,
    *,
    artifacts_directory: builtins.str,
    branch: builtins.str,
    task: _Task_9fa875b6,
    version_file: builtins.str,
    github_release: typing.Optional[builtins.bool] = None,
    workflow_node_version: typing.Optional[builtins.str] = None,
    workflow_permissions: typing.Optional[typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]]] = None,
    bump_package: typing.Optional[builtins.str] = None,
    jsii_release_version: typing.Optional[builtins.str] = None,
    major_version: typing.Optional[jsii.Number] = None,
    min_major_version: typing.Optional[jsii.Number] = None,
    next_version_command: typing.Optional[builtins.str] = None,
    npm_dist_tag: typing.Optional[builtins.str] = None,
    post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    prerelease: typing.Optional[builtins.str] = None,
    publish_dry_run: typing.Optional[builtins.bool] = None,
    publish_tasks: typing.Optional[builtins.bool] = None,
    releasable_commits: typing.Optional[_ReleasableCommits_d481ce10] = None,
    release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    release_every_commit: typing.Optional[builtins.bool] = None,
    release_failure_issue: typing.Optional[builtins.bool] = None,
    release_failure_issue_label: typing.Optional[builtins.str] = None,
    release_schedule: typing.Optional[builtins.str] = None,
    release_tag_prefix: typing.Optional[builtins.str] = None,
    release_trigger: typing.Optional[ReleaseTrigger] = None,
    release_workflow_name: typing.Optional[builtins.str] = None,
    release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    workflow_container_image: typing.Optional[builtins.str] = None,
    workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a92183b4ef9afc7a5f36329d0935bbbd7767d95d760424a1478dedd4c089e82(
    project: _Project_57d89203,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f66d9106b15a88644bb5efb62c4d4d18bb7c7b73bb22b904010a8a603f1ec7(
    branch: builtins.str,
    *,
    major_version: jsii.Number,
    min_major_version: typing.Optional[jsii.Number] = None,
    minor_version: typing.Optional[jsii.Number] = None,
    npm_dist_tag: typing.Optional[builtins.str] = None,
    prerelease: typing.Optional[builtins.str] = None,
    tag_prefix: typing.Optional[builtins.str] = None,
    workflow_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8df2839c98abec4e8a1e84ad0fc953b4051cdf361a30544804281bc912901e2(
    jobs: typing.Mapping[builtins.str, typing.Union[_Job_20ffcf45, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5e99254de9f29d2ac3b86e193164816e1ed36e491e602128e7d16fb86aa377(
    *,
    bump_package: typing.Optional[builtins.str] = None,
    jsii_release_version: typing.Optional[builtins.str] = None,
    major_version: typing.Optional[jsii.Number] = None,
    min_major_version: typing.Optional[jsii.Number] = None,
    next_version_command: typing.Optional[builtins.str] = None,
    npm_dist_tag: typing.Optional[builtins.str] = None,
    post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    prerelease: typing.Optional[builtins.str] = None,
    publish_dry_run: typing.Optional[builtins.bool] = None,
    publish_tasks: typing.Optional[builtins.bool] = None,
    releasable_commits: typing.Optional[_ReleasableCommits_d481ce10] = None,
    release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    release_every_commit: typing.Optional[builtins.bool] = None,
    release_failure_issue: typing.Optional[builtins.bool] = None,
    release_failure_issue_label: typing.Optional[builtins.str] = None,
    release_schedule: typing.Optional[builtins.str] = None,
    release_tag_prefix: typing.Optional[builtins.str] = None,
    release_trigger: typing.Optional[ReleaseTrigger] = None,
    release_workflow_name: typing.Optional[builtins.str] = None,
    release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    workflow_container_image: typing.Optional[builtins.str] = None,
    workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629cc7488dbd6e87168962d964694e088625a8e208d09e45c120eac7e4963baa(
    *,
    schedule: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370b478ebba8352e12c41a67b57d5954055dba8a6ceae59144e72607fdc6df41(
    *,
    post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    maven_endpoint: typing.Optional[builtins.str] = None,
    maven_gpg_private_key_passphrase: typing.Optional[builtins.str] = None,
    maven_gpg_private_key_secret: typing.Optional[builtins.str] = None,
    maven_password: typing.Optional[builtins.str] = None,
    maven_repository_url: typing.Optional[builtins.str] = None,
    maven_server_id: typing.Optional[builtins.str] = None,
    maven_staging_profile_id: typing.Optional[builtins.str] = None,
    maven_username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34680d3cf9e2cc6374987796717402a524a0bb377e9172f0707da67450b3239(
    *,
    post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    dist_tag: typing.Optional[builtins.str] = None,
    npm_provenance: typing.Optional[builtins.bool] = None,
    npm_token_secret: typing.Optional[builtins.str] = None,
    registry: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14abe6d299c2354a8f22a08788f088aafaa8acf2b85b20f297416346274a9b96(
    *,
    post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    nuget_api_key_secret: typing.Optional[builtins.str] = None,
    nuget_server: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa7c01cc40634bf771011bf4e8ddb9e3be28efd1b3f15b5d0768a4e810d37bc(
    *,
    post_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_publish_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_tools: typing.Optional[typing.Union[_Tools_75b93a2a, typing.Dict[builtins.str, typing.Any]]] = None,
    code_artifact_options: typing.Optional[typing.Union[CodeArtifactOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    twine_password_secret: typing.Optional[builtins.str] = None,
    twine_registry_url: typing.Optional[builtins.str] = None,
    twine_username_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcbb9106f2fe858c4efa7a5934906e63b00b56fa33c47c5f910dac2a904f472(
    *,
    bump_package: typing.Optional[builtins.str] = None,
    jsii_release_version: typing.Optional[builtins.str] = None,
    major_version: typing.Optional[jsii.Number] = None,
    min_major_version: typing.Optional[jsii.Number] = None,
    next_version_command: typing.Optional[builtins.str] = None,
    npm_dist_tag: typing.Optional[builtins.str] = None,
    post_build_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    prerelease: typing.Optional[builtins.str] = None,
    publish_dry_run: typing.Optional[builtins.bool] = None,
    publish_tasks: typing.Optional[builtins.bool] = None,
    releasable_commits: typing.Optional[_ReleasableCommits_d481ce10] = None,
    release_branches: typing.Optional[typing.Mapping[builtins.str, typing.Union[BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    release_every_commit: typing.Optional[builtins.bool] = None,
    release_failure_issue: typing.Optional[builtins.bool] = None,
    release_failure_issue_label: typing.Optional[builtins.str] = None,
    release_schedule: typing.Optional[builtins.str] = None,
    release_tag_prefix: typing.Optional[builtins.str] = None,
    release_trigger: typing.Optional[ReleaseTrigger] = None,
    release_workflow_name: typing.Optional[builtins.str] = None,
    release_workflow_setup_steps: typing.Optional[typing.Sequence[typing.Union[_JobStep_c3287c05, typing.Dict[builtins.str, typing.Any]]]] = None,
    versionrc_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    workflow_container_image: typing.Optional[builtins.str] = None,
    workflow_runs_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    workflow_runs_on_group: typing.Optional[typing.Union[_GroupRunnerOptions_148c59c1, typing.Dict[builtins.str, typing.Any]]] = None,
    artifacts_directory: builtins.str,
    branch: builtins.str,
    task: _Task_9fa875b6,
    version_file: builtins.str,
    github_release: typing.Optional[builtins.bool] = None,
    workflow_node_version: typing.Optional[builtins.str] = None,
    workflow_permissions: typing.Optional[typing.Union[_JobPermissions_3b5b53dc, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
