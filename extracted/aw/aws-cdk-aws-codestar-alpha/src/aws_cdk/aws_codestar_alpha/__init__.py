r'''
# AWS::CodeStar Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## GitHub Repository

To create a new GitHub Repository and commit the assets from S3 bucket into the repository after it is created:

```python
import aws_cdk.aws_codestar_alpha as codestar
import aws_cdk.aws_s3 as s3


codestar.GitHubRepository(self, "GitHubRepo",
    owner="aws",
    repository_name="aws-cdk",
    access_token=SecretValue.secrets_manager("my-github-token",
        json_field="token"
    ),
    contents_bucket=s3.Bucket.from_bucket_name(self, "Bucket", "amzn-s3-demo-bucket"),
    contents_key="import.zip"
)
```

## Update or Delete the GitHubRepository

At this moment, updates to the `GitHubRepository` are not supported and the repository will not be deleted upon the deletion of the CloudFormation stack. You will need to update or delete the GitHub repository manually.
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

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codestar-alpha.GitHubRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "contents_bucket": "contentsBucket",
        "contents_key": "contentsKey",
        "owner": "owner",
        "repository_name": "repositoryName",
        "contents_s3_version": "contentsS3Version",
        "description": "description",
        "enable_issues": "enableIssues",
        "visibility": "visibility",
    },
)
class GitHubRepositoryProps:
    def __init__(
        self,
        *,
        access_token: _aws_cdk_ceddda9d.SecretValue,
        contents_bucket: _aws_cdk_aws_s3_ceddda9d.IBucketRef,
        contents_key: builtins.str,
        owner: builtins.str,
        repository_name: builtins.str,
        contents_s3_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_issues: typing.Optional[builtins.bool] = None,
        visibility: typing.Optional["RepositoryVisibility"] = None,
    ) -> None:
        '''(experimental) Construction properties of ``GitHubRepository``.

        :param access_token: (experimental) The GitHub user's personal access token for the GitHub repository.
        :param contents_bucket: (experimental) The name of the Amazon S3 bucket that contains the ZIP file with the content to be committed to the new repository.
        :param contents_key: (experimental) The S3 object key or file name for the ZIP file.
        :param owner: (experimental) The GitHub user name for the owner of the GitHub repository to be created. If this repository should be owned by a GitHub organization, provide its name
        :param repository_name: (experimental) The name of the repository you want to create in GitHub with AWS CloudFormation stack creation.
        :param contents_s3_version: (experimental) The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket. Default: - not specified
        :param description: (experimental) A comment or description about the new repository. This description is displayed in GitHub after the repository is created. Default: - no description
        :param enable_issues: (experimental) Indicates whether to enable issues for the GitHub repository. You can use GitHub issues to track information and bugs for your repository. Default: true
        :param visibility: (experimental) Indicates whether the GitHub repository is a private repository. If so, you choose who can see and commit to this repository. Default: RepositoryVisibility.PUBLIC

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_codestar_alpha as codestar
            import aws_cdk.aws_s3 as s3
            
            
            codestar.GitHubRepository(self, "GitHubRepo",
                owner="aws",
                repository_name="aws-cdk",
                access_token=SecretValue.secrets_manager("my-github-token",
                    json_field="token"
                ),
                contents_bucket=s3.Bucket.from_bucket_name(self, "Bucket", "amzn-s3-demo-bucket"),
                contents_key="import.zip"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c848afd2b589eccc9fe7fdbeff1681e2af3dab8477fed31f0d8bfb02ca05e0df)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument contents_bucket", value=contents_bucket, expected_type=type_hints["contents_bucket"])
            check_type(argname="argument contents_key", value=contents_key, expected_type=type_hints["contents_key"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument contents_s3_version", value=contents_s3_version, expected_type=type_hints["contents_s3_version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_issues", value=enable_issues, expected_type=type_hints["enable_issues"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_token": access_token,
            "contents_bucket": contents_bucket,
            "contents_key": contents_key,
            "owner": owner,
            "repository_name": repository_name,
        }
        if contents_s3_version is not None:
            self._values["contents_s3_version"] = contents_s3_version
        if description is not None:
            self._values["description"] = description
        if enable_issues is not None:
            self._values["enable_issues"] = enable_issues
        if visibility is not None:
            self._values["visibility"] = visibility

    @builtins.property
    def access_token(self) -> _aws_cdk_ceddda9d.SecretValue:
        '''(experimental) The GitHub user's personal access token for the GitHub repository.

        :stability: experimental
        '''
        result = self._values.get("access_token")
        assert result is not None, "Required property 'access_token' is missing"
        return typing.cast(_aws_cdk_ceddda9d.SecretValue, result)

    @builtins.property
    def contents_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucketRef:
        '''(experimental) The name of the Amazon S3 bucket that contains the ZIP file with the content to be committed to the new repository.

        :stability: experimental
        '''
        result = self._values.get("contents_bucket")
        assert result is not None, "Required property 'contents_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucketRef, result)

    @builtins.property
    def contents_key(self) -> builtins.str:
        '''(experimental) The S3 object key or file name for the ZIP file.

        :stability: experimental
        '''
        result = self._values.get("contents_key")
        assert result is not None, "Required property 'contents_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) The GitHub user name for the owner of the GitHub repository to be created.

        If this
        repository should be owned by a GitHub organization, provide its name

        :stability: experimental
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''(experimental) The name of the repository you want to create in GitHub with AWS CloudFormation stack creation.

        :stability: experimental
        '''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def contents_s3_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket.

        :default: - not specified

        :stability: experimental
        '''
        result = self._values.get("contents_s3_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A comment or description about the new repository.

        This description is displayed in GitHub after the repository
        is created.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_issues(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether to enable issues for the GitHub repository.

        You can use GitHub issues to track information
        and bugs for your repository.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enable_issues")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def visibility(self) -> typing.Optional["RepositoryVisibility"]:
        '''(experimental) Indicates whether the GitHub repository is a private repository.

        If so, you choose who can see and commit to
        this repository.

        :default: RepositoryVisibility.PUBLIC

        :stability: experimental
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional["RepositoryVisibility"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-codestar-alpha.IGitHubRepository")
class IGitHubRepository(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) GitHubRepository resource interface.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        '''(experimental) the repository owner.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="repo")
    def repo(self) -> builtins.str:
        '''(experimental) the repository name.

        :stability: experimental
        '''
        ...


class _IGitHubRepositoryProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) GitHubRepository resource interface.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codestar-alpha.IGitHubRepository"

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        '''(experimental) the repository owner.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="repo")
    def repo(self) -> builtins.str:
        '''(experimental) the repository name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repo"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGitHubRepository).__jsii_proxy_class__ = lambda : _IGitHubRepositoryProxy


@jsii.enum(jsii_type="@aws-cdk/aws-codestar-alpha.RepositoryVisibility")
class RepositoryVisibility(enum.Enum):
    '''(experimental) Visibility of the GitHubRepository.

    :stability: experimental
    '''

    PRIVATE = "PRIVATE"
    '''(experimental) private repository.

    :stability: experimental
    '''
    PUBLIC = "PUBLIC"
    '''(experimental) public repository.

    :stability: experimental
    '''


@jsii.implements(IGitHubRepository)
class GitHubRepository(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codestar-alpha.GitHubRepository",
):
    '''(experimental) The GitHubRepository resource.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codestar_alpha as codestar
        import aws_cdk.aws_s3 as s3
        
        
        codestar.GitHubRepository(self, "GitHubRepo",
            owner="aws",
            repository_name="aws-cdk",
            access_token=SecretValue.secrets_manager("my-github-token",
                json_field="token"
            ),
            contents_bucket=s3.Bucket.from_bucket_name(self, "Bucket", "amzn-s3-demo-bucket"),
            contents_key="import.zip"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_token: _aws_cdk_ceddda9d.SecretValue,
        contents_bucket: _aws_cdk_aws_s3_ceddda9d.IBucketRef,
        contents_key: builtins.str,
        owner: builtins.str,
        repository_name: builtins.str,
        contents_s3_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_issues: typing.Optional[builtins.bool] = None,
        visibility: typing.Optional[RepositoryVisibility] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param access_token: (experimental) The GitHub user's personal access token for the GitHub repository.
        :param contents_bucket: (experimental) The name of the Amazon S3 bucket that contains the ZIP file with the content to be committed to the new repository.
        :param contents_key: (experimental) The S3 object key or file name for the ZIP file.
        :param owner: (experimental) The GitHub user name for the owner of the GitHub repository to be created. If this repository should be owned by a GitHub organization, provide its name
        :param repository_name: (experimental) The name of the repository you want to create in GitHub with AWS CloudFormation stack creation.
        :param contents_s3_version: (experimental) The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket. Default: - not specified
        :param description: (experimental) A comment or description about the new repository. This description is displayed in GitHub after the repository is created. Default: - no description
        :param enable_issues: (experimental) Indicates whether to enable issues for the GitHub repository. You can use GitHub issues to track information and bugs for your repository. Default: true
        :param visibility: (experimental) Indicates whether the GitHub repository is a private repository. If so, you choose who can see and commit to this repository. Default: RepositoryVisibility.PUBLIC

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9532a574e633c6d68e3daa0a175cb9309cb6a09badef5107c2a79a31d721ba10)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubRepositoryProps(
            access_token=access_token,
            contents_bucket=contents_bucket,
            contents_key=contents_key,
            owner=owner,
            repository_name=repository_name,
            contents_s3_version=contents_s3_version,
            description=description,
            enable_issues=enable_issues,
            visibility=visibility,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        '''(experimental) the repository owner.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="repo")
    def repo(self) -> builtins.str:
        '''(experimental) the repository name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repo"))


__all__ = [
    "GitHubRepository",
    "GitHubRepositoryProps",
    "IGitHubRepository",
    "RepositoryVisibility",
]

publication.publish()

def _typecheckingstub__c848afd2b589eccc9fe7fdbeff1681e2af3dab8477fed31f0d8bfb02ca05e0df(
    *,
    access_token: _aws_cdk_ceddda9d.SecretValue,
    contents_bucket: _aws_cdk_aws_s3_ceddda9d.IBucketRef,
    contents_key: builtins.str,
    owner: builtins.str,
    repository_name: builtins.str,
    contents_s3_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_issues: typing.Optional[builtins.bool] = None,
    visibility: typing.Optional[RepositoryVisibility] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9532a574e633c6d68e3daa0a175cb9309cb6a09badef5107c2a79a31d721ba10(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_token: _aws_cdk_ceddda9d.SecretValue,
    contents_bucket: _aws_cdk_aws_s3_ceddda9d.IBucketRef,
    contents_key: builtins.str,
    owner: builtins.str,
    repository_name: builtins.str,
    contents_s3_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_issues: typing.Optional[builtins.bool] = None,
    visibility: typing.Optional[RepositoryVisibility] = None,
) -> None:
    """Type checking stubs"""
    pass
