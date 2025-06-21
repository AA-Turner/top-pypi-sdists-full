r'''
# AWS Amplify Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

The AWS Amplify Console provides a Git-based workflow for deploying and hosting fullstack serverless web applications. A fullstack serverless app consists of a backend built with cloud resources such as GraphQL or REST APIs, file and data storage, and a frontend built with single page application frameworks such as React, Angular, Vue, or Gatsby.

## Setting up an app with branches, custom rules and a domain

To set up an Amplify Console app, define an `App`:

```python
import aws_cdk.aws_codebuild as codebuild


amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    build_spec=codebuild.BuildSpec.from_object_to_yaml({
        # Alternatively add a `amplify.yml` to the repo
        "version": "1.0",
        "frontend": {
            "phases": {
                "pre_build": {
                    "commands": ["yarn"
                    ]
                },
                "build": {
                    "commands": ["yarn build"
                    ]
                }
            },
            "artifacts": {
                "base_directory": "public",
                "files": -"**/*"
            }
        }
    })
)
```

To connect your `App` to GitLab, use the `GitLabSourceCodeProvider`:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitLabSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-gitlab-token")
    )
)
```

To connect your `App` to CodeCommit, use the `CodeCommitSourceCodeProvider`:

```python
import aws_cdk.aws_codecommit as codecommit


repository = codecommit.Repository(self, "Repo",
    repository_name="my-repo"
)

amplify_app = amplify.App(self, "App",
    source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=repository)
)
```

The IAM role associated with the `App` will automatically be granted the permission
to pull the CodeCommit repository.

Add branches:

```python
# amplify_app: amplify.App


main = amplify_app.add_branch("main") # `id` will be used as repo branch name
dev = amplify_app.add_branch("dev",
    performance_mode=True
)
dev.add_environment("STAGE", "dev")
```

Auto build and pull request preview are enabled by default.

Add custom rules for redirection:

```python
from aws_cdk.aws_amplify_alpha import CustomRule

# amplify_app: amplify.App

amplify_app.add_custom_rule(CustomRule(
    source="/docs/specific-filename.html",
    target="/documents/different-filename.html",
    status=amplify.RedirectStatus.TEMPORARY_REDIRECT
))
```

When working with a single page application (SPA), use the
`CustomRule.SINGLE_PAGE_APPLICATION_REDIRECT` to set up a 200
rewrite for all files to `index.html` except for the following
file extensions: css, gif, ico, jpg, js, png, txt, svg, woff,
ttf, map, json, webmanifest.

```python
# my_single_page_app: amplify.App


my_single_page_app.add_custom_rule(amplify.CustomRule.SINGLE_PAGE_APPLICATION_REDIRECT)
```

Add a domain and map sub domains to branches:

```python
# amplify_app: amplify.App
# main: amplify.Branch
# dev: amplify.Branch


domain = amplify_app.add_domain("example.com",
    enable_auto_subdomain=True,  # in case subdomains should be auto registered for branches
    auto_subdomain_creation_patterns=["*", "pr*"]
)
domain.map_root(main) # map main branch to domain root
domain.map_sub_domain(main, "www")
domain.map_sub_domain(dev)
```

To specify a custom certificate for your custom domain use the `customCertificate` property:

```python
# custom_certificate: acm.Certificate
# amplify_app: amplify.App


domain = amplify_app.add_domain("example.com",
    custom_certificate=custom_certificate
)
```

## Restricting access

Password protect the app with basic auth by specifying the `basicAuth` prop.

Use `BasicAuth.fromCredentials` when referencing an existing secret:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    basic_auth=amplify.BasicAuth.from_credentials("username", SecretValue.secrets_manager("my-github-token"))
)
```

Use `BasicAuth.fromGeneratedPassword` to generate a password in Secrets Manager:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    basic_auth=amplify.BasicAuth.from_generated_password("username")
)
```

Basic auth can be added to specific branches:

```python
# amplify_app: amplify.App

amplify_app.add_branch("feature/next",
    basic_auth=amplify.BasicAuth.from_generated_password("username")
)
```

## Automatically creating and deleting branches

Use the `autoBranchCreation` and `autoBranchDeletion` props to control creation/deletion
of branches:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    auto_branch_creation=amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
        patterns=["feature/*", "test/*"]),
    auto_branch_deletion=True
)
```

## Adding custom response headers

Use the `customResponseHeaders` prop to configure custom response headers for an Amplify app:

```python
amplify_app = amplify.App(self, "App",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    custom_response_headers=[amplify.CustomResponseHeader(
        pattern="*.json",
        headers={
            "custom-header-name-1": "custom-header-value-1",
            "custom-header-name-2": "custom-header-value-2"
        }
    ), amplify.CustomResponseHeader(
        pattern="/path/*",
        headers={
            "custom-header-name-1": "custom-header-value-2"
        }
    )
    ]
)
```

If the app uses a monorepo structure, define which appRoot from the build spec the custom response headers should apply to by using the `appRoot` property:

```python
import aws_cdk.aws_codebuild as codebuild


amplify_app = amplify.App(self, "App",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    build_spec=codebuild.BuildSpec.from_object_to_yaml({
        "version": "1.0",
        "applications": [{
            "app_root": "frontend",
            "frontend": {
                "phases": {
                    "pre_build": {
                        "commands": ["npm install"]
                    },
                    "build": {
                        "commands": ["npm run build"]
                    }
                }
            }
        }, {
            "app_root": "backend",
            "backend": {
                "phases": {
                    "pre_build": {
                        "commands": ["npm install"]
                    },
                    "build": {
                        "commands": ["npm run build"]
                    }
                }
            }
        }
        ]
    }),
    custom_response_headers=[amplify.CustomResponseHeader(
        app_root="frontend",
        pattern="*.json",
        headers={
            "custom-header-name-1": "custom-header-value-1",
            "custom-header-name-2": "custom-header-value-2"
        }
    ), amplify.CustomResponseHeader(
        app_root="backend",
        pattern="/path/*",
        headers={
            "custom-header-name-1": "custom-header-value-2"
        }
    )
    ]
)
```

## Configure server side rendering when hosting app

Setting the `platform` field on the Amplify `App` construct can be used to control whether the app will host only static assets or server side rendered assets in addition to static. By default, the value is set to `WEB` (static only), however, server side rendering can be turned on by setting to `WEB_COMPUTE` as follows:

```python
amplify_app = amplify.App(self, "MyApp",
    platform=amplify.Platform.WEB_COMPUTE
)
```

## Compute role

This integration, enables you to assign an IAM role to the Amplify SSR Compute service to allow your server-side rendered (SSR) application to securely access specific AWS resources based on the role's permissions.

For example, you can allow your app's SSR compute functions to securely access other AWS services or resources, such as Amazon Bedrock or an Amazon S3 bucket, based on the permissions defined in the assigned IAM role.

For more information, see [Adding an SSR Compute role to allow access to AWS resources](https://docs.aws.amazon.com/amplify/latest/userguide/amplify-SSR-compute-role.html).

By default, a new role is created when `platform` is `Platform.WEB_COMPUTE` or `Platform.WEB_DYNAMIC`.
If you want to assign an IAM role to the APP, set `compute` to the role:

```python
# compute_role: iam.Role


amplify_app = amplify.App(self, "MyApp",
    platform=amplify.Platform.WEB_COMPUTE,
    compute_role=compute_role
)
```

It is also possible to override the compute role for a specific branch by setting `computeRole` in `Branch`:

```python
# compute_role: iam.Role
# amplify_app: amplify.App


branch = amplify_app.add_branch("dev", compute_role=compute_role)
```

## Cache Config

Amplify uses Amazon CloudFront to manage the caching configuration for your hosted applications. A cache configuration is applied to each app to optimize for the best performance.

Setting the `cacheConfigType` field on the Amplify `App` construct can be used to control cache configuration. By default, the value is set to `AMPLIFY_MANAGED`. If you want to exclude all cookies from the cache key, set `AMPLIFY_MANAGED_NO_COOKIES`.

For more information, see [Managing the cache configuration for an app](https://docs.aws.amazon.com/amplify/latest/userguide/caching.html).

```python
amplify_app = amplify.App(self, "MyApp",
    cache_config_type=amplify.CacheConfigType.AMPLIFY_MANAGED_NO_COOKIES
)
```

## Deploying Assets

`sourceCodeProvider` is optional; when this is not specified the Amplify app can be deployed to using `.zip` packages. The `asset` property can be used to deploy S3 assets to Amplify as part of the CDK:

```python
import aws_cdk.aws_s3_assets as assets

# asset: assets.Asset
# amplify_app: amplify.App

branch = amplify_app.add_branch("dev", asset=asset)
```

## Skew protection for Amplify Deployments

Deployment skew protection is available to Amplify applications to eliminate version skew issues between client and servers in web applications.
When you apply skew protection to an Amplify application, you can ensure that your clients always interact with the correct version of server-side assets, regardless of when a deployment occurs.

For more information, see [Skew protection for Amplify deployments](https://docs.aws.amazon.com/amplify/latest/userguide/skew-protection.html).

To enable skew protection, set the `skewProtection` property to `true`:

```python
# amplify_app: amplify.App

branch = amplify_app.add_branch("dev", skew_protection=True)
```
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
import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_ceddda9d
import aws_cdk.aws_codebuild as _aws_cdk_aws_codebuild_ceddda9d
import aws_cdk.aws_codecommit as _aws_cdk_aws_codecommit_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_s3_assets as _aws_cdk_aws_s3_assets_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.AppProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_name": "appName",
        "auto_branch_creation": "autoBranchCreation",
        "auto_branch_deletion": "autoBranchDeletion",
        "basic_auth": "basicAuth",
        "build_spec": "buildSpec",
        "cache_config_type": "cacheConfigType",
        "compute_role": "computeRole",
        "custom_response_headers": "customResponseHeaders",
        "custom_rules": "customRules",
        "description": "description",
        "environment_variables": "environmentVariables",
        "platform": "platform",
        "role": "role",
        "source_code_provider": "sourceCodeProvider",
    },
)
class AppProps:
    def __init__(
        self,
        *,
        app_name: typing.Optional[builtins.str] = None,
        auto_branch_creation: typing.Optional[typing.Union["AutoBranchCreation", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_branch_deletion: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional["BasicAuth"] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
        cache_config_type: typing.Optional["CacheConfigType"] = None,
        compute_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        custom_response_headers: typing.Optional[typing.Sequence[typing.Union["CustomResponseHeader", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_rules: typing.Optional[typing.Sequence["CustomRule"]] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        platform: typing.Optional["Platform"] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        source_code_provider: typing.Optional["ISourceCodeProvider"] = None,
    ) -> None:
        '''(experimental) Properties for an App.

        :param app_name: (experimental) The name for the application. Default: - a CDK generated name
        :param auto_branch_creation: (experimental) The auto branch creation configuration. Use this to automatically create branches that match a certain pattern. Default: - no auto branch creation
        :param auto_branch_deletion: (experimental) Automatically disconnect a branch in the Amplify Console when you delete a branch from your Git repository. Default: false
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection at an app level to all your branches. Default: - no password protection
        :param build_spec: (experimental) BuildSpec for the application. Alternatively, add a ``amplify.yml`` file to the repository. Default: - no build spec
        :param cache_config_type: (experimental) The type of cache configuration to use for an Amplify app. Default: CacheConfigType.AMPLIFY_MANAGED
        :param compute_role: (experimental) The IAM role for an SSR app. The Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions. Default: undefined - a new role is created when ``platform`` is ``Platform.WEB_COMPUTE`` or ``Platform.WEB_DYNAMIC``, otherwise no compute role
        :param custom_response_headers: (experimental) The custom HTTP response headers for an Amplify app. Default: - no custom response headers
        :param custom_rules: (experimental) Custom rewrite/redirect rules for the application. Default: - no custom rewrite/redirect rules
        :param description: (experimental) A description for the application. Default: - no description
        :param environment_variables: (experimental) Environment variables for the application. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - no environment variables
        :param platform: (experimental) Indicates the hosting platform to use. Set to WEB for static site generated (SSG) apps (i.e. a Create React App or Gatsby) and WEB_COMPUTE for server side rendered (SSR) apps (i.e. NextJS). Default: Platform.WEB
        :param role: (experimental) The IAM service role to associate with the application. The App implements IGrantable. Default: - a new role is created
        :param source_code_provider: (experimental) The source code provider for this application. Default: - not connected to a source code provider

        :stability: experimental
        :exampleMetadata: infused

        Example::

            amplify_app = amplify.App(self, "MyApp",
                source_code_provider=amplify.GitHubSourceCodeProvider(
                    owner="<user>",
                    repository="<repo>",
                    oauth_token=SecretValue.secrets_manager("my-github-token")
                ),
                auto_branch_creation=amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                    patterns=["feature/*", "test/*"]),
                auto_branch_deletion=True
            )
        '''
        if isinstance(auto_branch_creation, dict):
            auto_branch_creation = AutoBranchCreation(**auto_branch_creation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00fae34ad2733a382bf4bd9703c470687ee286b909acac7113a890be0a23b881)
            check_type(argname="argument app_name", value=app_name, expected_type=type_hints["app_name"])
            check_type(argname="argument auto_branch_creation", value=auto_branch_creation, expected_type=type_hints["auto_branch_creation"])
            check_type(argname="argument auto_branch_deletion", value=auto_branch_deletion, expected_type=type_hints["auto_branch_deletion"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument cache_config_type", value=cache_config_type, expected_type=type_hints["cache_config_type"])
            check_type(argname="argument compute_role", value=compute_role, expected_type=type_hints["compute_role"])
            check_type(argname="argument custom_response_headers", value=custom_response_headers, expected_type=type_hints["custom_response_headers"])
            check_type(argname="argument custom_rules", value=custom_rules, expected_type=type_hints["custom_rules"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument source_code_provider", value=source_code_provider, expected_type=type_hints["source_code_provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_name is not None:
            self._values["app_name"] = app_name
        if auto_branch_creation is not None:
            self._values["auto_branch_creation"] = auto_branch_creation
        if auto_branch_deletion is not None:
            self._values["auto_branch_deletion"] = auto_branch_deletion
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if cache_config_type is not None:
            self._values["cache_config_type"] = cache_config_type
        if compute_role is not None:
            self._values["compute_role"] = compute_role
        if custom_response_headers is not None:
            self._values["custom_response_headers"] = custom_response_headers
        if custom_rules is not None:
            self._values["custom_rules"] = custom_rules
        if description is not None:
            self._values["description"] = description
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if platform is not None:
            self._values["platform"] = platform
        if role is not None:
            self._values["role"] = role
        if source_code_provider is not None:
            self._values["source_code_provider"] = source_code_provider

    @builtins.property
    def app_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the application.

        :default: - a CDK generated name

        :stability: experimental
        '''
        result = self._values.get("app_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_branch_creation(self) -> typing.Optional["AutoBranchCreation"]:
        '''(experimental) The auto branch creation configuration.

        Use this to automatically create
        branches that match a certain pattern.

        :default: - no auto branch creation

        :stability: experimental
        '''
        result = self._values.get("auto_branch_creation")
        return typing.cast(typing.Optional["AutoBranchCreation"], result)

    @builtins.property
    def auto_branch_deletion(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically disconnect a branch in the Amplify Console when you delete a branch from your Git repository.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("auto_branch_deletion")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional["BasicAuth"]:
        '''(experimental) The Basic Auth configuration.

        Use this to set password protection at an
        app level to all your branches.

        :default: - no password protection

        :stability: experimental
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional["BasicAuth"], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec]:
        '''(experimental) BuildSpec for the application.

        Alternatively, add a ``amplify.yml``
        file to the repository.

        :default: - no build spec

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
        :stability: experimental
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec], result)

    @builtins.property
    def cache_config_type(self) -> typing.Optional["CacheConfigType"]:
        '''(experimental) The type of cache configuration to use for an Amplify app.

        :default: CacheConfigType.AMPLIFY_MANAGED

        :stability: experimental
        '''
        result = self._values.get("cache_config_type")
        return typing.cast(typing.Optional["CacheConfigType"], result)

    @builtins.property
    def compute_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role for an SSR app.

        The Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions.

        :default: undefined - a new role is created when ``platform`` is ``Platform.WEB_COMPUTE`` or ``Platform.WEB_DYNAMIC``, otherwise no compute role

        :stability: experimental
        '''
        result = self._values.get("compute_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def custom_response_headers(
        self,
    ) -> typing.Optional[typing.List["CustomResponseHeader"]]:
        '''(experimental) The custom HTTP response headers for an Amplify app.

        :default: - no custom response headers

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/custom-headers.html
        :stability: experimental
        '''
        result = self._values.get("custom_response_headers")
        return typing.cast(typing.Optional[typing.List["CustomResponseHeader"]], result)

    @builtins.property
    def custom_rules(self) -> typing.Optional[typing.List["CustomRule"]]:
        '''(experimental) Custom rewrite/redirect rules for the application.

        :default: - no custom rewrite/redirect rules

        :stability: experimental
        '''
        result = self._values.get("custom_rules")
        return typing.cast(typing.Optional[typing.List["CustomRule"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the application.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for the application.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :default: - no environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def platform(self) -> typing.Optional["Platform"]:
        '''(experimental) Indicates the hosting platform to use.

        Set to WEB for static site
        generated (SSG) apps (i.e. a Create React App or Gatsby) and WEB_COMPUTE
        for server side rendered (SSR) apps (i.e. NextJS).

        :default: Platform.WEB

        :stability: experimental
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional["Platform"], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM service role to associate with the application.

        The App
        implements IGrantable.

        :default: - a new role is created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def source_code_provider(self) -> typing.Optional["ISourceCodeProvider"]:
        '''(experimental) The source code provider for this application.

        :default: - not connected to a source code provider

        :stability: experimental
        '''
        result = self._values.get("source_code_provider")
        return typing.cast(typing.Optional["ISourceCodeProvider"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.AutoBranchCreation",
    jsii_struct_bases=[],
    name_mapping={
        "auto_build": "autoBuild",
        "basic_auth": "basicAuth",
        "build_spec": "buildSpec",
        "environment_variables": "environmentVariables",
        "patterns": "patterns",
        "pull_request_environment_name": "pullRequestEnvironmentName",
        "pull_request_preview": "pullRequestPreview",
        "stage": "stage",
    },
)
class AutoBranchCreation:
    def __init__(
        self,
        *,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional["BasicAuth"] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Auto branch creation configuration.

        :param auto_build: (experimental) Whether to enable auto building for the auto created branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the auto created branch. Default: - no password protection
        :param build_spec: (experimental) Build spec for the auto created branch. Default: - application build spec
        :param environment_variables: (experimental) Environment variables for the auto created branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param patterns: (experimental) Automated branch creation glob patterns. Default: - all repository branches
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews of the auto created branch. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the auto created branch. Default: true
        :param stage: (experimental) Stage for the auto created branch. Default: - no stage

        :stability: experimental
        :exampleMetadata: infused

        Example::

            amplify_app = amplify.App(self, "MyApp",
                source_code_provider=amplify.GitHubSourceCodeProvider(
                    owner="<user>",
                    repository="<repo>",
                    oauth_token=SecretValue.secrets_manager("my-github-token")
                ),
                auto_branch_creation=amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                    patterns=["feature/*", "test/*"]),
                auto_branch_deletion=True
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f2af0e4edaf98f48a3180a7128a09045875ec0261dce3f9482c947bcbaae487)
            check_type(argname="argument auto_build", value=auto_build, expected_type=type_hints["auto_build"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument patterns", value=patterns, expected_type=type_hints["patterns"])
            check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
            check_type(argname="argument pull_request_preview", value=pull_request_preview, expected_type=type_hints["pull_request_preview"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_build is not None:
            self._values["auto_build"] = auto_build
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if patterns is not None:
            self._values["patterns"] = patterns
        if pull_request_environment_name is not None:
            self._values["pull_request_environment_name"] = pull_request_environment_name
        if pull_request_preview is not None:
            self._values["pull_request_preview"] = pull_request_preview
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def auto_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable auto building for the auto created branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional["BasicAuth"]:
        '''(experimental) The Basic Auth configuration.

        Use this to set password protection for
        the auto created branch.

        :default: - no password protection

        :stability: experimental
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional["BasicAuth"], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec]:
        '''(experimental) Build spec for the auto created branch.

        :default: - application build spec

        :stability: experimental
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for the auto created branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :default: - application environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Automated branch creation glob patterns.

        :default: - all repository branches

        :stability: experimental
        '''
        result = self._values.get("patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The dedicated backend environment for the pull request previews of the auto created branch.

        :default: - automatically provision a temporary backend

        :stability: experimental
        '''
        result = self._values.get("pull_request_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable pull request preview for the auto created branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_preview")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Stage for the auto created branch.

        :default: - no stage

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoBranchCreation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BasicAuth(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify-alpha.BasicAuth",
):
    '''(experimental) Basic Auth configuration.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            source_code_provider=amplify.GitHubSourceCodeProvider(
                owner="<user>",
                repository="<repo>",
                oauth_token=SecretValue.secrets_manager("my-github-token")
            ),
            basic_auth=amplify.BasicAuth.from_generated_password("username")
        )
    '''

    def __init__(
        self,
        *,
        username: builtins.str,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        password: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    ) -> None:
        '''
        :param username: (experimental) The username.
        :param encryption_key: (experimental) The encryption key to use to encrypt the password when it's generated in Secrets Manager. Default: - default master key
        :param password: (experimental) The password. Default: - A Secrets Manager generated password

        :stability: experimental
        '''
        props = BasicAuthProps(
            username=username, encryption_key=encryption_key, password=password
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="fromCredentials")
    @builtins.classmethod
    def from_credentials(
        cls,
        username: builtins.str,
        password: _aws_cdk_ceddda9d.SecretValue,
    ) -> "BasicAuth":
        '''(experimental) Creates a Basic Auth configuration from a username and a password.

        :param username: The username.
        :param password: The password.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb61d9465b046820e4be734cff063bd1c7fefa32eea9bb8808c12336571c6dc3)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        return typing.cast("BasicAuth", jsii.sinvoke(cls, "fromCredentials", [username, password]))

    @jsii.member(jsii_name="fromGeneratedPassword")
    @builtins.classmethod
    def from_generated_password(
        cls,
        username: builtins.str,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> "BasicAuth":
        '''(experimental) Creates a Basic Auth configuration with a password generated in Secrets Manager.

        :param username: The username.
        :param encryption_key: The encryption key to use to encrypt the password in Secrets Manager.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f366513def1e04612e697b08e7c8224a644a15e7253569d6b718c02c3b943d4)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
        return typing.cast("BasicAuth", jsii.sinvoke(cls, "fromGeneratedPassword", [username, encryption_key]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> "BasicAuthConfig":
        '''(experimental) Binds this Basic Auth configuration to an App.

        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a575491ebde5fe3bfc9e69f32ef44ff1ba5507b5e749645203007fb5fe4214ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("BasicAuthConfig", jsii.invoke(self, "bind", [scope, id]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.BasicAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_basic_auth": "enableBasicAuth",
        "password": "password",
        "username": "username",
    },
)
class BasicAuthConfig:
    def __init__(
        self,
        *,
        enable_basic_auth: builtins.bool,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''(experimental) A Basic Auth configuration.

        :param enable_basic_auth: (experimental) Whether to enable Basic Auth.
        :param password: (experimental) The password.
        :param username: (experimental) The username.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify_alpha as amplify_alpha
            
            basic_auth_config = amplify_alpha.BasicAuthConfig(
                enable_basic_auth=False,
                password="password",
                username="username"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa4e34249a276be45cee21e775f03f7d1e7897d6d161907ebd2793f00e4409a)
            check_type(argname="argument enable_basic_auth", value=enable_basic_auth, expected_type=type_hints["enable_basic_auth"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_basic_auth": enable_basic_auth,
            "password": password,
            "username": username,
        }

    @builtins.property
    def enable_basic_auth(self) -> builtins.bool:
        '''(experimental) Whether to enable Basic Auth.

        :stability: experimental
        '''
        result = self._values.get("enable_basic_auth")
        assert result is not None, "Required property 'enable_basic_auth' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''(experimental) The password.

        :stability: experimental
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.BasicAuthProps",
    jsii_struct_bases=[],
    name_mapping={
        "username": "username",
        "encryption_key": "encryptionKey",
        "password": "password",
    },
)
class BasicAuthProps:
    def __init__(
        self,
        *,
        username: builtins.str,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        password: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    ) -> None:
        '''(experimental) Properties for a BasicAuth.

        :param username: (experimental) The username.
        :param encryption_key: (experimental) The encryption key to use to encrypt the password when it's generated in Secrets Manager. Default: - default master key
        :param password: (experimental) The password. Default: - A Secrets Manager generated password

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify_alpha as amplify_alpha
            import aws_cdk as cdk
            from aws_cdk import aws_kms as kms
            
            # key: kms.Key
            # secret_value: cdk.SecretValue
            
            basic_auth_props = amplify_alpha.BasicAuthProps(
                username="username",
            
                # the properties below are optional
                encryption_key=key,
                password=secret_value
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3809f6d0ef297fe501ad051e76013b357eb7facbc26fe8936330556c35d4dc74)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The encryption key to use to encrypt the password when it's generated in Secrets Manager.

        :default: - default master key

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def password(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''(experimental) The password.

        :default: - A Secrets Manager generated password

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicAuthProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.BranchOptions",
    jsii_struct_bases=[],
    name_mapping={
        "asset": "asset",
        "auto_build": "autoBuild",
        "basic_auth": "basicAuth",
        "branch_name": "branchName",
        "build_spec": "buildSpec",
        "compute_role": "computeRole",
        "description": "description",
        "environment_variables": "environmentVariables",
        "performance_mode": "performanceMode",
        "pull_request_environment_name": "pullRequestEnvironmentName",
        "pull_request_preview": "pullRequestPreview",
        "skew_protection": "skewProtection",
        "stage": "stage",
    },
)
class BranchOptions:
    def __init__(
        self,
        *,
        asset: typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset] = None,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
        compute_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        performance_mode: typing.Optional[builtins.bool] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        skew_protection: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options to add a branch to an application.

        :param asset: (experimental) Asset for deployment. The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's startDeployment API to initiate and deploy a S3 asset onto the App. Default: - no asset
        :param auto_build: (experimental) Whether to enable auto building for the branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: (experimental) The name of the branch. Default: - the construct's id
        :param build_spec: (experimental) BuildSpec for the branch. Default: - no build spec
        :param compute_role: (experimental) The IAM role to assign to a branch of an SSR app. The SSR Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions. This role overrides the app-level compute role. Default: undefined - No specific role for the branch. If the app has a compute role, it will be inherited.
        :param description: (experimental) A description for the branch. Default: - no description
        :param environment_variables: (experimental) Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param performance_mode: (experimental) Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out. Default: false
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the branch. Default: true
        :param skew_protection: (experimental) Specifies whether the skew protection feature is enabled for the branch. Deployment skew protection is available to Amplify applications to eliminate version skew issues between client and servers in web applications. When you apply skew protection to a branch, you can ensure that your clients always interact with the correct version of server-side assets, regardless of when a deployment occurs. Default: None - Default setting is no skew protection.
        :param stage: (experimental) Stage for the branch. Default: - no stage

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # compute_role: iam.Role
            # amplify_app: amplify.App
            
            
            branch = amplify_app.add_branch("dev", compute_role=compute_role)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b000a0021ff86c948a7f1d5b6d9915b3dd9424861178bf3ab8c784feb250caeb)
            check_type(argname="argument asset", value=asset, expected_type=type_hints["asset"])
            check_type(argname="argument auto_build", value=auto_build, expected_type=type_hints["auto_build"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument compute_role", value=compute_role, expected_type=type_hints["compute_role"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument performance_mode", value=performance_mode, expected_type=type_hints["performance_mode"])
            check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
            check_type(argname="argument pull_request_preview", value=pull_request_preview, expected_type=type_hints["pull_request_preview"])
            check_type(argname="argument skew_protection", value=skew_protection, expected_type=type_hints["skew_protection"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset is not None:
            self._values["asset"] = asset
        if auto_build is not None:
            self._values["auto_build"] = auto_build
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if branch_name is not None:
            self._values["branch_name"] = branch_name
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if compute_role is not None:
            self._values["compute_role"] = compute_role
        if description is not None:
            self._values["description"] = description
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if pull_request_environment_name is not None:
            self._values["pull_request_environment_name"] = pull_request_environment_name
        if pull_request_preview is not None:
            self._values["pull_request_preview"] = pull_request_preview
        if skew_protection is not None:
            self._values["skew_protection"] = skew_protection
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def asset(self) -> typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset]:
        '''(experimental) Asset for deployment.

        The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's
        startDeployment API to initiate and deploy a S3 asset onto the App.

        :default: - no asset

        :stability: experimental
        '''
        result = self._values.get("asset")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset], result)

    @builtins.property
    def auto_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable auto building for the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional[BasicAuth]:
        '''(experimental) The Basic Auth configuration.

        Use this to set password protection for
        the branch

        :default: - no password protection

        :stability: experimental
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional[BasicAuth], result)

    @builtins.property
    def branch_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the branch.

        :default: - the construct's id

        :stability: experimental
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec]:
        '''(experimental) BuildSpec for the branch.

        :default: - no build spec

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
        :stability: experimental
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec], result)

    @builtins.property
    def compute_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role to assign to a branch of an SSR app.

        The SSR Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions.

        This role overrides the app-level compute role.

        :default: undefined - No specific role for the branch. If the app has a compute role, it will be inherited.

        :stability: experimental
        '''
        result = self._values.get("compute_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the branch.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for the branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :default: - application environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def performance_mode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge
        for a longer interval. When performance mode is enabled, hosting configuration or code changes
        can take up to 10 minutes to roll out.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("performance_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The dedicated backend environment for the pull request previews.

        :default: - automatically provision a temporary backend

        :stability: experimental
        '''
        result = self._values.get("pull_request_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable pull request preview for the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_preview")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def skew_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the skew protection feature is enabled for the branch.

        Deployment skew protection is available to Amplify applications to eliminate version skew issues
        between client and servers in web applications.
        When you apply skew protection to a branch, you can ensure that your clients always interact
        with the correct version of server-side assets, regardless of when a deployment occurs.

        :default: None - Default setting is no skew protection.

        :stability: experimental
        '''
        result = self._values.get("skew_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Stage for the branch.

        :default: - no stage

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.BranchProps",
    jsii_struct_bases=[BranchOptions],
    name_mapping={
        "asset": "asset",
        "auto_build": "autoBuild",
        "basic_auth": "basicAuth",
        "branch_name": "branchName",
        "build_spec": "buildSpec",
        "compute_role": "computeRole",
        "description": "description",
        "environment_variables": "environmentVariables",
        "performance_mode": "performanceMode",
        "pull_request_environment_name": "pullRequestEnvironmentName",
        "pull_request_preview": "pullRequestPreview",
        "skew_protection": "skewProtection",
        "stage": "stage",
        "app": "app",
    },
)
class BranchProps(BranchOptions):
    def __init__(
        self,
        *,
        asset: typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset] = None,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
        compute_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        performance_mode: typing.Optional[builtins.bool] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        skew_protection: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
        app: "IApp",
    ) -> None:
        '''(experimental) Properties for a Branch.

        :param asset: (experimental) Asset for deployment. The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's startDeployment API to initiate and deploy a S3 asset onto the App. Default: - no asset
        :param auto_build: (experimental) Whether to enable auto building for the branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: (experimental) The name of the branch. Default: - the construct's id
        :param build_spec: (experimental) BuildSpec for the branch. Default: - no build spec
        :param compute_role: (experimental) The IAM role to assign to a branch of an SSR app. The SSR Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions. This role overrides the app-level compute role. Default: undefined - No specific role for the branch. If the app has a compute role, it will be inherited.
        :param description: (experimental) A description for the branch. Default: - no description
        :param environment_variables: (experimental) Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param performance_mode: (experimental) Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out. Default: false
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the branch. Default: true
        :param skew_protection: (experimental) Specifies whether the skew protection feature is enabled for the branch. Deployment skew protection is available to Amplify applications to eliminate version skew issues between client and servers in web applications. When you apply skew protection to a branch, you can ensure that your clients always interact with the correct version of server-side assets, regardless of when a deployment occurs. Default: None - Default setting is no skew protection.
        :param stage: (experimental) Stage for the branch. Default: - no stage
        :param app: (experimental) The application within which the branch must be created.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify_alpha as amplify_alpha
            from aws_cdk import aws_codebuild as codebuild
            from aws_cdk import aws_iam as iam
            from aws_cdk import aws_s3_assets as s3_assets
            
            # app: amplify_alpha.App
            # asset: s3_assets.Asset
            # basic_auth: amplify_alpha.BasicAuth
            # build_spec: codebuild.BuildSpec
            # role: iam.Role
            
            branch_props = amplify_alpha.BranchProps(
                app=app,
            
                # the properties below are optional
                asset=asset,
                auto_build=False,
                basic_auth=basic_auth,
                branch_name="branchName",
                build_spec=build_spec,
                compute_role=role,
                description="description",
                environment_variables={
                    "environment_variables_key": "environmentVariables"
                },
                performance_mode=False,
                pull_request_environment_name="pullRequestEnvironmentName",
                pull_request_preview=False,
                skew_protection=False,
                stage="stage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__529d2fd3c9613ce4eb269675040b4e50e2005444ff5b8d0f0cf4702adf37c2da)
            check_type(argname="argument asset", value=asset, expected_type=type_hints["asset"])
            check_type(argname="argument auto_build", value=auto_build, expected_type=type_hints["auto_build"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument compute_role", value=compute_role, expected_type=type_hints["compute_role"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument performance_mode", value=performance_mode, expected_type=type_hints["performance_mode"])
            check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
            check_type(argname="argument pull_request_preview", value=pull_request_preview, expected_type=type_hints["pull_request_preview"])
            check_type(argname="argument skew_protection", value=skew_protection, expected_type=type_hints["skew_protection"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app": app,
        }
        if asset is not None:
            self._values["asset"] = asset
        if auto_build is not None:
            self._values["auto_build"] = auto_build
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if branch_name is not None:
            self._values["branch_name"] = branch_name
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if compute_role is not None:
            self._values["compute_role"] = compute_role
        if description is not None:
            self._values["description"] = description
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if pull_request_environment_name is not None:
            self._values["pull_request_environment_name"] = pull_request_environment_name
        if pull_request_preview is not None:
            self._values["pull_request_preview"] = pull_request_preview
        if skew_protection is not None:
            self._values["skew_protection"] = skew_protection
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def asset(self) -> typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset]:
        '''(experimental) Asset for deployment.

        The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's
        startDeployment API to initiate and deploy a S3 asset onto the App.

        :default: - no asset

        :stability: experimental
        '''
        result = self._values.get("asset")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset], result)

    @builtins.property
    def auto_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable auto building for the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional[BasicAuth]:
        '''(experimental) The Basic Auth configuration.

        Use this to set password protection for
        the branch

        :default: - no password protection

        :stability: experimental
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional[BasicAuth], result)

    @builtins.property
    def branch_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the branch.

        :default: - the construct's id

        :stability: experimental
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec]:
        '''(experimental) BuildSpec for the branch.

        :default: - no build spec

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
        :stability: experimental
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec], result)

    @builtins.property
    def compute_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role to assign to a branch of an SSR app.

        The SSR Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions.

        This role overrides the app-level compute role.

        :default: undefined - No specific role for the branch. If the app has a compute role, it will be inherited.

        :stability: experimental
        '''
        result = self._values.get("compute_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the branch.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for the branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :default: - application environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def performance_mode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge
        for a longer interval. When performance mode is enabled, hosting configuration or code changes
        can take up to 10 minutes to roll out.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("performance_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The dedicated backend environment for the pull request previews.

        :default: - automatically provision a temporary backend

        :stability: experimental
        '''
        result = self._values.get("pull_request_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable pull request preview for the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_preview")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def skew_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the skew protection feature is enabled for the branch.

        Deployment skew protection is available to Amplify applications to eliminate version skew issues
        between client and servers in web applications.
        When you apply skew protection to a branch, you can ensure that your clients always interact
        with the correct version of server-side assets, regardless of when a deployment occurs.

        :default: None - Default setting is no skew protection.

        :stability: experimental
        '''
        result = self._values.get("skew_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Stage for the branch.

        :default: - no stage

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app(self) -> "IApp":
        '''(experimental) The application within which the branch must be created.

        :stability: experimental
        '''
        result = self._values.get("app")
        assert result is not None, "Required property 'app' is missing"
        return typing.cast("IApp", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-amplify-alpha.CacheConfigType")
class CacheConfigType(enum.Enum):
    '''(experimental) The type of cache configuration to use for an Amplify app.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            cache_config_type=amplify.CacheConfigType.AMPLIFY_MANAGED_NO_COOKIES
        )
    '''

    AMPLIFY_MANAGED = "AMPLIFY_MANAGED"
    '''(experimental) AMPLIFY_MANAGED - Automatically applies an optimized cache configuration for your app based on its platform, routing rules, and rewrite rules.

    :stability: experimental
    '''
    AMPLIFY_MANAGED_NO_COOKIES = "AMPLIFY_MANAGED_NO_COOKIES"
    '''(experimental) AMPLIFY_MANAGED_NO_COOKIES - The same as AMPLIFY_MANAGED, except that it excludes all cookies from the cache key.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.CodeCommitSourceCodeProviderProps",
    jsii_struct_bases=[],
    name_mapping={"repository": "repository"},
)
class CodeCommitSourceCodeProviderProps:
    def __init__(
        self,
        *,
        repository: _aws_cdk_aws_codecommit_ceddda9d.IRepository,
    ) -> None:
        '''(experimental) Properties for a CodeCommit source code provider.

        :param repository: (experimental) The CodeCommit repository.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_codecommit as codecommit
            
            
            repository = codecommit.Repository(self, "Repo",
                repository_name="my-repo"
            )
            
            amplify_app = amplify.App(self, "App",
                source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=repository)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa2a223f4d92f511cf4841627ec77cbadb81380423b16782bcb854435bab9a3c)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
        }

    @builtins.property
    def repository(self) -> _aws_cdk_aws_codecommit_ceddda9d.IRepository:
        '''(experimental) The CodeCommit repository.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(_aws_cdk_aws_codecommit_ceddda9d.IRepository, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeCommitSourceCodeProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.CustomResponseHeader",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "pattern": "pattern", "app_root": "appRoot"},
)
class CustomResponseHeader:
    def __init__(
        self,
        *,
        headers: typing.Mapping[builtins.str, builtins.str],
        pattern: builtins.str,
        app_root: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Custom response header of an Amplify App.

        :param headers: (experimental) The map of custom headers to be applied.
        :param pattern: (experimental) These custom headers will be applied to all URL file paths that match this pattern.
        :param app_root: (experimental) If the app uses a monorepo structure, the appRoot from the build spec to apply the custom headers to. Default: - The appRoot is omitted in the custom headers output.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify_alpha as amplify_alpha
            
            custom_response_header = amplify_alpha.CustomResponseHeader(
                headers={
                    "headers_key": "headers"
                },
                pattern="pattern",
            
                # the properties below are optional
                app_root="appRoot"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c1962999fedf4ca1e171bdd7613e146d33a972f8a3275a1c82cf2d83ee1b3d)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument app_root", value=app_root, expected_type=type_hints["app_root"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "headers": headers,
            "pattern": pattern,
        }
        if app_root is not None:
            self._values["app_root"] = app_root

    @builtins.property
    def headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The map of custom headers to be applied.

        :stability: experimental
        '''
        result = self._values.get("headers")
        assert result is not None, "Required property 'headers' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''(experimental) These custom headers will be applied to all URL file paths that match this pattern.

        :stability: experimental
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_root(self) -> typing.Optional[builtins.str]:
        '''(experimental) If the app uses a monorepo structure, the appRoot from the build spec to apply the custom headers to.

        :default: - The appRoot is omitted in the custom headers output.

        :stability: experimental
        '''
        result = self._values.get("app_root")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomResponseHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomRule(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify-alpha.CustomRule",
):
    '''(experimental) Custom rewrite/redirect rule for an Amplify App.

    :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_amplify_alpha import CustomRule
        
        # amplify_app: amplify.App
        
        amplify_app.add_custom_rule(CustomRule(
            source="/docs/specific-filename.html",
            target="/documents/different-filename.html",
            status=amplify.RedirectStatus.TEMPORARY_REDIRECT
        ))
    '''

    def __init__(
        self,
        *,
        source: builtins.str,
        target: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        status: typing.Optional["RedirectStatus"] = None,
    ) -> None:
        '''
        :param source: (experimental) The source pattern for a URL rewrite or redirect rule.
        :param target: (experimental) The target pattern for a URL rewrite or redirect rule.
        :param condition: (experimental) The condition for a URL rewrite or redirect rule, e.g. country code. Default: - no condition
        :param status: (experimental) The status code for a URL rewrite or redirect rule. Default: PERMANENT_REDIRECT

        :stability: experimental
        '''
        options = CustomRuleOptions(
            source=source, target=target, condition=condition, status=status
        )

        jsii.create(self.__class__, self, [options])

    @jsii.python.classproperty
    @jsii.member(jsii_name="SINGLE_PAGE_APPLICATION_REDIRECT")
    def SINGLE_PAGE_APPLICATION_REDIRECT(cls) -> "CustomRule":
        '''(experimental) Sets up a 200 rewrite for all paths to ``index.html`` except for path containing a file extension.

        :stability: experimental
        '''
        return typing.cast("CustomRule", jsii.sget(cls, "SINGLE_PAGE_APPLICATION_REDIRECT"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''(experimental) The source pattern for a URL rewrite or redirect rule.

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        '''(experimental) The target pattern for a URL rewrite or redirect rule.

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) The condition for a URL rewrite or redirect rule, e.g. country code.

        :default: - no condition

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional["RedirectStatus"]:
        '''(experimental) The status code for a URL rewrite or redirect rule.

        :default: PERMANENT_REDIRECT

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional["RedirectStatus"], jsii.get(self, "status"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.CustomRuleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "target": "target",
        "condition": "condition",
        "status": "status",
    },
)
class CustomRuleOptions:
    def __init__(
        self,
        *,
        source: builtins.str,
        target: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        status: typing.Optional["RedirectStatus"] = None,
    ) -> None:
        '''(experimental) Options for a custom rewrite/redirect rule for an Amplify App.

        :param source: (experimental) The source pattern for a URL rewrite or redirect rule.
        :param target: (experimental) The target pattern for a URL rewrite or redirect rule.
        :param condition: (experimental) The condition for a URL rewrite or redirect rule, e.g. country code. Default: - no condition
        :param status: (experimental) The status code for a URL rewrite or redirect rule. Default: PERMANENT_REDIRECT

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_amplify_alpha import CustomRule
            
            # amplify_app: amplify.App
            
            amplify_app.add_custom_rule(CustomRule(
                source="/docs/specific-filename.html",
                target="/documents/different-filename.html",
                status=amplify.RedirectStatus.TEMPORARY_REDIRECT
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716b401b2530f2ea497b885540df3538442041316ceef4d35cbbdb92fa7c627d)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
            "target": target,
        }
        if condition is not None:
            self._values["condition"] = condition
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def source(self) -> builtins.str:
        '''(experimental) The source pattern for a URL rewrite or redirect rule.

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''(experimental) The target pattern for a URL rewrite or redirect rule.

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) The condition for a URL rewrite or redirect rule, e.g. country code.

        :default: - no condition

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional["RedirectStatus"]:
        '''(experimental) The status code for a URL rewrite or redirect rule.

        :default: PERMANENT_REDIRECT

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["RedirectStatus"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomRuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Domain(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify-alpha.Domain",
):
    '''(experimental) An Amplify Console domain.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # amplify_app: amplify.App
        # main: amplify.Branch
        # dev: amplify.Branch
        
        
        domain = amplify_app.add_domain("example.com",
            enable_auto_subdomain=True,  # in case subdomains should be auto registered for branches
            auto_subdomain_creation_patterns=["*", "pr*"]
        )
        domain.map_root(main) # map main branch to domain root
        domain.map_sub_domain(main, "www")
        domain.map_sub_domain(dev)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app: "IApp",
        auto_sub_domain_iam_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union["SubDomain", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app: (experimental) The application to which the domain must be connected.
        :param auto_sub_domain_iam_role: (experimental) The IAM role with access to Route53 when using enableAutoSubdomain. Default: the IAM role from App.grantPrincipal
        :param auto_subdomain_creation_patterns: (experimental) Branches which should automatically create subdomains. Default: - all repository branches ['*', 'pr*']
        :param custom_certificate: (experimental) The type of SSL/TLS certificate to use for your custom domain. Default: - Amplify uses the default certificate that it provisions and manages for you
        :param domain_name: (experimental) The name of the domain. Default: - the construct's id
        :param enable_auto_subdomain: (experimental) Automatically create subdomains for connected branches. Default: false
        :param sub_domains: (experimental) Subdomains. Default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e333b720149581cace67c91dbe1444026f7810389a4b7e045740c2cc6daec4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DomainProps(
            app=app,
            auto_sub_domain_iam_role=auto_sub_domain_iam_role,
            auto_subdomain_creation_patterns=auto_subdomain_creation_patterns,
            custom_certificate=custom_certificate,
            domain_name=domain_name,
            enable_auto_subdomain=enable_auto_subdomain,
            sub_domains=sub_domains,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="mapRoot")
    def map_root(self, branch: "IBranch") -> "Domain":
        '''(experimental) Maps a branch to the domain root.

        :param branch: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c869e76fd73bca8b756321422ccc73fc84cda2d048155aaa02c2be3ca35b44b)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        return typing.cast("Domain", jsii.invoke(self, "mapRoot", [branch]))

    @jsii.member(jsii_name="mapSubDomain")
    def map_sub_domain(
        self,
        branch: "IBranch",
        prefix: typing.Optional[builtins.str] = None,
    ) -> "Domain":
        '''(experimental) Maps a branch to a sub domain.

        :param branch: The branch.
        :param prefix: The prefix. Use '' to map to the root of the domain. Defaults to branch name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa160eb48a0fec188e680884a7d6535fc2cc3d4e1b98f3dea06a760deb6186c4)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        return typing.cast("Domain", jsii.invoke(self, "mapSubDomain", [branch, prefix]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="certificateRecord")
    def certificate_record(self) -> builtins.str:
        '''(experimental) The DNS Record for certificate verification.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateRecord"))

    @builtins.property
    @jsii.member(jsii_name="domainAutoSubDomainCreationPatterns")
    def domain_auto_sub_domain_creation_patterns(self) -> typing.List[builtins.str]:
        '''(experimental) Branch patterns for the automatically created subdomain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainAutoSubDomainCreationPatterns"))

    @builtins.property
    @jsii.member(jsii_name="domainAutoSubDomainIamRole")
    def domain_auto_sub_domain_iam_role(self) -> builtins.str:
        '''(experimental) The IAM service role for the subdomain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainAutoSubDomainIamRole"))

    @builtins.property
    @jsii.member(jsii_name="domainEnableAutoSubDomain")
    def domain_enable_auto_sub_domain(self) -> _aws_cdk_ceddda9d.IResolvable:
        '''(experimental) Specifies whether the automated creation of subdomains for branches is enabled.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(_aws_cdk_ceddda9d.IResolvable, jsii.get(self, "domainEnableAutoSubDomain"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) The name of the domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="domainStatus")
    def domain_status(self) -> builtins.str:
        '''(experimental) The status of the domain association.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainStatus"))

    @builtins.property
    @jsii.member(jsii_name="statusReason")
    def status_reason(self) -> builtins.str:
        '''(experimental) The reason for the current status of the domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "statusReason"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.DomainOptions",
    jsii_struct_bases=[],
    name_mapping={
        "auto_subdomain_creation_patterns": "autoSubdomainCreationPatterns",
        "custom_certificate": "customCertificate",
        "domain_name": "domainName",
        "enable_auto_subdomain": "enableAutoSubdomain",
        "sub_domains": "subDomains",
    },
)
class DomainOptions:
    def __init__(
        self,
        *,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union["SubDomain", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Options to add a domain to an application.

        :param auto_subdomain_creation_patterns: (experimental) Branches which should automatically create subdomains. Default: - all repository branches ['*', 'pr*']
        :param custom_certificate: (experimental) The type of SSL/TLS certificate to use for your custom domain. Default: - Amplify uses the default certificate that it provisions and manages for you
        :param domain_name: (experimental) The name of the domain. Default: - the construct's id
        :param enable_auto_subdomain: (experimental) Automatically create subdomains for connected branches. Default: false
        :param sub_domains: (experimental) Subdomains. Default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # amplify_app: amplify.App
            # main: amplify.Branch
            # dev: amplify.Branch
            
            
            domain = amplify_app.add_domain("example.com",
                enable_auto_subdomain=True,  # in case subdomains should be auto registered for branches
                auto_subdomain_creation_patterns=["*", "pr*"]
            )
            domain.map_root(main) # map main branch to domain root
            domain.map_sub_domain(main, "www")
            domain.map_sub_domain(dev)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c320927402b9dc876549f614a833ea8c346cc42aadbbe883e3d2646c5dd361ff)
            check_type(argname="argument auto_subdomain_creation_patterns", value=auto_subdomain_creation_patterns, expected_type=type_hints["auto_subdomain_creation_patterns"])
            check_type(argname="argument custom_certificate", value=custom_certificate, expected_type=type_hints["custom_certificate"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument enable_auto_subdomain", value=enable_auto_subdomain, expected_type=type_hints["enable_auto_subdomain"])
            check_type(argname="argument sub_domains", value=sub_domains, expected_type=type_hints["sub_domains"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_subdomain_creation_patterns is not None:
            self._values["auto_subdomain_creation_patterns"] = auto_subdomain_creation_patterns
        if custom_certificate is not None:
            self._values["custom_certificate"] = custom_certificate
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if enable_auto_subdomain is not None:
            self._values["enable_auto_subdomain"] = enable_auto_subdomain
        if sub_domains is not None:
            self._values["sub_domains"] = sub_domains

    @builtins.property
    def auto_subdomain_creation_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Branches which should automatically create subdomains.

        :default: - all repository branches ['*', 'pr*']

        :stability: experimental
        '''
        result = self._values.get("auto_subdomain_creation_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def custom_certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''(experimental) The type of SSL/TLS certificate to use for your custom domain.

        :default: - Amplify uses the default certificate that it provisions and manages for you

        :stability: experimental
        '''
        result = self._values.get("custom_certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the domain.

        :default: - the construct's id

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_subdomain(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically create subdomains for connected branches.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_auto_subdomain")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sub_domains(self) -> typing.Optional[typing.List["SubDomain"]]:
        '''(experimental) Subdomains.

        :default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        '''
        result = self._values.get("sub_domains")
        return typing.cast(typing.Optional[typing.List["SubDomain"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.DomainProps",
    jsii_struct_bases=[DomainOptions],
    name_mapping={
        "auto_subdomain_creation_patterns": "autoSubdomainCreationPatterns",
        "custom_certificate": "customCertificate",
        "domain_name": "domainName",
        "enable_auto_subdomain": "enableAutoSubdomain",
        "sub_domains": "subDomains",
        "app": "app",
        "auto_sub_domain_iam_role": "autoSubDomainIamRole",
    },
)
class DomainProps(DomainOptions):
    def __init__(
        self,
        *,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union["SubDomain", typing.Dict[builtins.str, typing.Any]]]] = None,
        app: "IApp",
        auto_sub_domain_iam_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''(experimental) Properties for a Domain.

        :param auto_subdomain_creation_patterns: (experimental) Branches which should automatically create subdomains. Default: - all repository branches ['*', 'pr*']
        :param custom_certificate: (experimental) The type of SSL/TLS certificate to use for your custom domain. Default: - Amplify uses the default certificate that it provisions and manages for you
        :param domain_name: (experimental) The name of the domain. Default: - the construct's id
        :param enable_auto_subdomain: (experimental) Automatically create subdomains for connected branches. Default: false
        :param sub_domains: (experimental) Subdomains. Default: - use ``addSubDomain()`` to add subdomains
        :param app: (experimental) The application to which the domain must be connected.
        :param auto_sub_domain_iam_role: (experimental) The IAM role with access to Route53 when using enableAutoSubdomain. Default: the IAM role from App.grantPrincipal

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify_alpha as amplify_alpha
            from aws_cdk import aws_certificatemanager as certificatemanager
            from aws_cdk import aws_iam as iam
            
            # app: amplify_alpha.App
            # branch: amplify_alpha.Branch
            # certificate: certificatemanager.Certificate
            # role: iam.Role
            
            domain_props = amplify_alpha.DomainProps(
                app=app,
            
                # the properties below are optional
                auto_subdomain_creation_patterns=["autoSubdomainCreationPatterns"],
                auto_sub_domain_iam_role=role,
                custom_certificate=certificate,
                domain_name="domainName",
                enable_auto_subdomain=False,
                sub_domains=[amplify_alpha.SubDomain(
                    branch=branch,
            
                    # the properties below are optional
                    prefix="prefix"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bcc4553ef04f08c67c00e5ca845c349b18cd93f97e022c79c4b74ef6e4b08c4)
            check_type(argname="argument auto_subdomain_creation_patterns", value=auto_subdomain_creation_patterns, expected_type=type_hints["auto_subdomain_creation_patterns"])
            check_type(argname="argument custom_certificate", value=custom_certificate, expected_type=type_hints["custom_certificate"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument enable_auto_subdomain", value=enable_auto_subdomain, expected_type=type_hints["enable_auto_subdomain"])
            check_type(argname="argument sub_domains", value=sub_domains, expected_type=type_hints["sub_domains"])
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
            check_type(argname="argument auto_sub_domain_iam_role", value=auto_sub_domain_iam_role, expected_type=type_hints["auto_sub_domain_iam_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app": app,
        }
        if auto_subdomain_creation_patterns is not None:
            self._values["auto_subdomain_creation_patterns"] = auto_subdomain_creation_patterns
        if custom_certificate is not None:
            self._values["custom_certificate"] = custom_certificate
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if enable_auto_subdomain is not None:
            self._values["enable_auto_subdomain"] = enable_auto_subdomain
        if sub_domains is not None:
            self._values["sub_domains"] = sub_domains
        if auto_sub_domain_iam_role is not None:
            self._values["auto_sub_domain_iam_role"] = auto_sub_domain_iam_role

    @builtins.property
    def auto_subdomain_creation_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Branches which should automatically create subdomains.

        :default: - all repository branches ['*', 'pr*']

        :stability: experimental
        '''
        result = self._values.get("auto_subdomain_creation_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def custom_certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''(experimental) The type of SSL/TLS certificate to use for your custom domain.

        :default: - Amplify uses the default certificate that it provisions and manages for you

        :stability: experimental
        '''
        result = self._values.get("custom_certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the domain.

        :default: - the construct's id

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_subdomain(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically create subdomains for connected branches.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_auto_subdomain")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sub_domains(self) -> typing.Optional[typing.List["SubDomain"]]:
        '''(experimental) Subdomains.

        :default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        '''
        result = self._values.get("sub_domains")
        return typing.cast(typing.Optional[typing.List["SubDomain"]], result)

    @builtins.property
    def app(self) -> "IApp":
        '''(experimental) The application to which the domain must be connected.

        :stability: experimental
        '''
        result = self._values.get("app")
        assert result is not None, "Required property 'app' is missing"
        return typing.cast("IApp", result)

    @builtins.property
    def auto_sub_domain_iam_role(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role with access to Route53 when using enableAutoSubdomain.

        :default: the IAM role from App.grantPrincipal

        :stability: experimental
        '''
        result = self._values.get("auto_sub_domain_iam_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.GitHubSourceCodeProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "oauth_token": "oauthToken",
        "owner": "owner",
        "repository": "repository",
    },
)
class GitHubSourceCodeProviderProps:
    def __init__(
        self,
        *,
        oauth_token: _aws_cdk_ceddda9d.SecretValue,
        owner: builtins.str,
        repository: builtins.str,
    ) -> None:
        '''(experimental) Properties for a GitHub source code provider.

        :param oauth_token: (experimental) A personal access token with the ``repo`` scope.
        :param owner: (experimental) The user or organization owning the repository.
        :param repository: (experimental) The name of the repository.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            amplify_app = amplify.App(self, "App",
                source_code_provider=amplify.GitHubSourceCodeProvider(
                    owner="<user>",
                    repository="<repo>",
                    oauth_token=SecretValue.secrets_manager("my-github-token")
                ),
                custom_response_headers=[amplify.CustomResponseHeader(
                    pattern="*.json",
                    headers={
                        "custom-header-name-1": "custom-header-value-1",
                        "custom-header-name-2": "custom-header-value-2"
                    }
                ), amplify.CustomResponseHeader(
                    pattern="/path/*",
                    headers={
                        "custom-header-name-1": "custom-header-value-2"
                    }
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a971b7d216fe8bfb4bdd8a433546879b4d66a8bf5db40ad1bec42594688a780b)
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oauth_token": oauth_token,
            "owner": owner,
            "repository": repository,
        }

    @builtins.property
    def oauth_token(self) -> _aws_cdk_ceddda9d.SecretValue:
        '''(experimental) A personal access token with the ``repo`` scope.

        :stability: experimental
        '''
        result = self._values.get("oauth_token")
        assert result is not None, "Required property 'oauth_token' is missing"
        return typing.cast(_aws_cdk_ceddda9d.SecretValue, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) The user or organization owning the repository.

        :stability: experimental
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''(experimental) The name of the repository.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSourceCodeProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.GitLabSourceCodeProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "oauth_token": "oauthToken",
        "owner": "owner",
        "repository": "repository",
    },
)
class GitLabSourceCodeProviderProps:
    def __init__(
        self,
        *,
        oauth_token: _aws_cdk_ceddda9d.SecretValue,
        owner: builtins.str,
        repository: builtins.str,
    ) -> None:
        '''(experimental) Properties for a GitLab source code provider.

        :param oauth_token: (experimental) A personal access token with the ``repo`` scope.
        :param owner: (experimental) The user or organization owning the repository.
        :param repository: (experimental) The name of the repository.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            amplify_app = amplify.App(self, "MyApp",
                source_code_provider=amplify.GitLabSourceCodeProvider(
                    owner="<user>",
                    repository="<repo>",
                    oauth_token=SecretValue.secrets_manager("my-gitlab-token")
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a410ebec7c5d44edc4b31cd124a785c4320c6fc00e5255e7e368cb8c5a23a054)
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oauth_token": oauth_token,
            "owner": owner,
            "repository": repository,
        }

    @builtins.property
    def oauth_token(self) -> _aws_cdk_ceddda9d.SecretValue:
        '''(experimental) A personal access token with the ``repo`` scope.

        :stability: experimental
        '''
        result = self._values.get("oauth_token")
        assert result is not None, "Required property 'oauth_token' is missing"
        return typing.cast(_aws_cdk_ceddda9d.SecretValue, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) The user or organization owning the repository.

        :stability: experimental
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''(experimental) The name of the repository.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitLabSourceCodeProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-amplify-alpha.IApp")
class IApp(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) An Amplify Console application.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''(experimental) The application id.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IAppProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) An Amplify Console application.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-amplify-alpha.IApp"

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''(experimental) The application id.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "appId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApp).__jsii_proxy_class__ = lambda : _IAppProxy


@jsii.interface(jsii_type="@aws-cdk/aws-amplify-alpha.IBranch")
class IBranch(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A branch.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        '''(experimental) The name of the branch.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IBranchProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A branch.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-amplify-alpha.IBranch"

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        '''(experimental) The name of the branch.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "branchName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBranch).__jsii_proxy_class__ = lambda : _IBranchProxy


@jsii.interface(jsii_type="@aws-cdk/aws-amplify-alpha.ISourceCodeProvider")
class ISourceCodeProvider(typing_extensions.Protocol):
    '''(experimental) A source code provider.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(self, app: "App") -> "SourceCodeProviderConfig":
        '''(experimental) Binds the source code provider to an app.

        :param app: The app [disable-awslint:ref-via-interface].

        :stability: experimental
        '''
        ...


class _ISourceCodeProviderProxy:
    '''(experimental) A source code provider.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-amplify-alpha.ISourceCodeProvider"

    @jsii.member(jsii_name="bind")
    def bind(self, app: "App") -> "SourceCodeProviderConfig":
        '''(experimental) Binds the source code provider to an app.

        :param app: The app [disable-awslint:ref-via-interface].

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827844675225f813772a868238ca8ec0955c868d8d638a34104a2a053abc8b6b)
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
        return typing.cast("SourceCodeProviderConfig", jsii.invoke(self, "bind", [app]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISourceCodeProvider).__jsii_proxy_class__ = lambda : _ISourceCodeProviderProxy


@jsii.enum(jsii_type="@aws-cdk/aws-amplify-alpha.Platform")
class Platform(enum.Enum):
    '''(experimental) Available hosting platforms to use on the App.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            platform=amplify.Platform.WEB_COMPUTE
        )
    '''

    WEB = "WEB"
    '''(experimental) WEB - Used to indicate that the app is hosted using only static assets.

    :stability: experimental
    '''
    WEB_COMPUTE = "WEB_COMPUTE"
    '''(experimental) WEB_COMPUTE - Used to indicate the app is hosted using a combination of server side rendered and static assets.

    :stability: experimental
    '''
    WEB_DYNAMIC = "WEB_DYNAMIC"
    '''(experimental) WEB_DYNAMIC - Used to indicate the app is hosted using a fully dynamic architecture, where requests are processed at runtime by backend compute services.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-amplify-alpha.RedirectStatus")
class RedirectStatus(enum.Enum):
    '''(experimental) The status code for a URL rewrite or redirect rule.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_amplify_alpha import CustomRule
        
        # amplify_app: amplify.App
        
        amplify_app.add_custom_rule(CustomRule(
            source="/docs/specific-filename.html",
            target="/documents/different-filename.html",
            status=amplify.RedirectStatus.TEMPORARY_REDIRECT
        ))
    '''

    REWRITE = "REWRITE"
    '''(experimental) Rewrite (200).

    :stability: experimental
    '''
    PERMANENT_REDIRECT = "PERMANENT_REDIRECT"
    '''(experimental) Permanent redirect (301).

    :stability: experimental
    '''
    TEMPORARY_REDIRECT = "TEMPORARY_REDIRECT"
    '''(experimental) Temporary redirect (302).

    :stability: experimental
    '''
    NOT_FOUND = "NOT_FOUND"
    '''(experimental) Not found (404).

    :stability: experimental
    '''
    NOT_FOUND_REWRITE = "NOT_FOUND_REWRITE"
    '''(experimental) Not found rewrite (404).

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.SourceCodeProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "repository": "repository",
        "access_token": "accessToken",
        "oauth_token": "oauthToken",
    },
)
class SourceCodeProviderConfig:
    def __init__(
        self,
        *,
        repository: builtins.str,
        access_token: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        oauth_token: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    ) -> None:
        '''(experimental) Configuration for the source code provider.

        :param repository: (experimental) The repository for the application. Must use the ``HTTPS`` protocol. For example, ``https://github.com/aws/aws-cdk``.
        :param access_token: (experimental) Personal Access token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key. Token is not stored. Either ``accessToken`` or ``oauthToken`` must be specified if ``repository`` is sepcified. Default: - do not use a token
        :param oauth_token: (experimental) OAuth token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key. OAuth token is not stored. Either ``accessToken`` or ``oauthToken`` must be specified if ``repository`` is specified. Default: - do not use a token

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify_alpha as amplify_alpha
            import aws_cdk as cdk
            
            # secret_value: cdk.SecretValue
            
            source_code_provider_config = amplify_alpha.SourceCodeProviderConfig(
                repository="repository",
            
                # the properties below are optional
                access_token=secret_value,
                oauth_token=secret_value
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac2e4799ab05086079fd0209d56fa5d22cdc005ae42195d771cdce9310ea40d)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_token is not None:
            self._values["oauth_token"] = oauth_token

    @builtins.property
    def repository(self) -> builtins.str:
        '''(experimental) The repository for the application. Must use the ``HTTPS`` protocol.

        For example, ``https://github.com/aws/aws-cdk``.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''(experimental) Personal Access token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key.

        Token is not stored.

        Either ``accessToken`` or ``oauthToken`` must be specified if ``repository``
        is sepcified.

        :default: - do not use a token

        :stability: experimental
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def oauth_token(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''(experimental) OAuth token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key.

        OAuth token is not stored.

        Either ``accessToken`` or ``oauthToken`` must be specified if ``repository``
        is specified.

        :default: - do not use a token

        :stability: experimental
        '''
        result = self._values.get("oauth_token")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceCodeProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-amplify-alpha.SubDomain",
    jsii_struct_bases=[],
    name_mapping={"branch": "branch", "prefix": "prefix"},
)
class SubDomain:
    def __init__(
        self,
        *,
        branch: IBranch,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Sub domain settings.

        :param branch: (experimental) The branch.
        :param prefix: (experimental) The prefix. Use '' to map to the root of the domain Default: - the branch name

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_amplify_alpha as amplify_alpha
            
            # branch: amplify_alpha.Branch
            
            sub_domain = amplify_alpha.SubDomain(
                branch=branch,
            
                # the properties below are optional
                prefix="prefix"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6446d0b441d64cdc5587fba11548aaa739970869298a998c56e521c703c189)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch": branch,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def branch(self) -> IBranch:
        '''(experimental) The branch.

        :stability: experimental
        '''
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(IBranch, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The prefix.

        Use '' to map to the root of the domain

        :default: - the branch name

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubDomain(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IApp, _aws_cdk_aws_iam_ceddda9d.IGrantable)
class App(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify-alpha.App",
):
    '''(experimental) An Amplify Console application.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            source_code_provider=amplify.GitHubSourceCodeProvider(
                owner="<user>",
                repository="<repo>",
                oauth_token=SecretValue.secrets_manager("my-github-token")
            ),
            auto_branch_creation=amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                patterns=["feature/*", "test/*"]),
            auto_branch_deletion=True
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app_name: typing.Optional[builtins.str] = None,
        auto_branch_creation: typing.Optional[typing.Union[AutoBranchCreation, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_branch_deletion: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
        cache_config_type: typing.Optional[CacheConfigType] = None,
        compute_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        custom_response_headers: typing.Optional[typing.Sequence[typing.Union[CustomResponseHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_rules: typing.Optional[typing.Sequence[CustomRule]] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        platform: typing.Optional[Platform] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        source_code_provider: typing.Optional[ISourceCodeProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app_name: (experimental) The name for the application. Default: - a CDK generated name
        :param auto_branch_creation: (experimental) The auto branch creation configuration. Use this to automatically create branches that match a certain pattern. Default: - no auto branch creation
        :param auto_branch_deletion: (experimental) Automatically disconnect a branch in the Amplify Console when you delete a branch from your Git repository. Default: false
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection at an app level to all your branches. Default: - no password protection
        :param build_spec: (experimental) BuildSpec for the application. Alternatively, add a ``amplify.yml`` file to the repository. Default: - no build spec
        :param cache_config_type: (experimental) The type of cache configuration to use for an Amplify app. Default: CacheConfigType.AMPLIFY_MANAGED
        :param compute_role: (experimental) The IAM role for an SSR app. The Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions. Default: undefined - a new role is created when ``platform`` is ``Platform.WEB_COMPUTE`` or ``Platform.WEB_DYNAMIC``, otherwise no compute role
        :param custom_response_headers: (experimental) The custom HTTP response headers for an Amplify app. Default: - no custom response headers
        :param custom_rules: (experimental) Custom rewrite/redirect rules for the application. Default: - no custom rewrite/redirect rules
        :param description: (experimental) A description for the application. Default: - no description
        :param environment_variables: (experimental) Environment variables for the application. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - no environment variables
        :param platform: (experimental) Indicates the hosting platform to use. Set to WEB for static site generated (SSG) apps (i.e. a Create React App or Gatsby) and WEB_COMPUTE for server side rendered (SSR) apps (i.e. NextJS). Default: Platform.WEB
        :param role: (experimental) The IAM service role to associate with the application. The App implements IGrantable. Default: - a new role is created
        :param source_code_provider: (experimental) The source code provider for this application. Default: - not connected to a source code provider

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb3fdecad4b351bd290c8a9d65c70964afb63130c3af329024642f751e1c88d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AppProps(
            app_name=app_name,
            auto_branch_creation=auto_branch_creation,
            auto_branch_deletion=auto_branch_deletion,
            basic_auth=basic_auth,
            build_spec=build_spec,
            cache_config_type=cache_config_type,
            compute_role=compute_role,
            custom_response_headers=custom_response_headers,
            custom_rules=custom_rules,
            description=description,
            environment_variables=environment_variables,
            platform=platform,
            role=role,
            source_code_provider=source_code_provider,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAppId")
    @builtins.classmethod
    def from_app_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        app_id: builtins.str,
    ) -> IApp:
        '''(experimental) Import an existing application.

        :param scope: -
        :param id: -
        :param app_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3f336cf0eaa13206e537622709ef647bef74d888dac99cd443461cc4455f954)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
        return typing.cast(IApp, jsii.sinvoke(cls, "fromAppId", [scope, id, app_id]))

    @jsii.member(jsii_name="addAutoBranchEnvironment")
    def add_auto_branch_environment(
        self,
        name: builtins.str,
        value: builtins.str,
    ) -> "App":
        '''(experimental) Adds an environment variable to the auto created branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c4175887e8f0238227347c352129f3e79394976ffce631cfdc2d4a9f0f90bd6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("App", jsii.invoke(self, "addAutoBranchEnvironment", [name, value]))

    @jsii.member(jsii_name="addBranch")
    def add_branch(
        self,
        id: builtins.str,
        *,
        asset: typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset] = None,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
        compute_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        performance_mode: typing.Optional[builtins.bool] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        skew_protection: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> "Branch":
        '''(experimental) Adds a branch to this application.

        :param id: -
        :param asset: (experimental) Asset for deployment. The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's startDeployment API to initiate and deploy a S3 asset onto the App. Default: - no asset
        :param auto_build: (experimental) Whether to enable auto building for the branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: (experimental) The name of the branch. Default: - the construct's id
        :param build_spec: (experimental) BuildSpec for the branch. Default: - no build spec
        :param compute_role: (experimental) The IAM role to assign to a branch of an SSR app. The SSR Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions. This role overrides the app-level compute role. Default: undefined - No specific role for the branch. If the app has a compute role, it will be inherited.
        :param description: (experimental) A description for the branch. Default: - no description
        :param environment_variables: (experimental) Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param performance_mode: (experimental) Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out. Default: false
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the branch. Default: true
        :param skew_protection: (experimental) Specifies whether the skew protection feature is enabled for the branch. Deployment skew protection is available to Amplify applications to eliminate version skew issues between client and servers in web applications. When you apply skew protection to a branch, you can ensure that your clients always interact with the correct version of server-side assets, regardless of when a deployment occurs. Default: None - Default setting is no skew protection.
        :param stage: (experimental) Stage for the branch. Default: - no stage

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2df726a9de1c19f40cb6ef900a079002cd8f15beecdff87621764c6d7dd0531)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = BranchOptions(
            asset=asset,
            auto_build=auto_build,
            basic_auth=basic_auth,
            branch_name=branch_name,
            build_spec=build_spec,
            compute_role=compute_role,
            description=description,
            environment_variables=environment_variables,
            performance_mode=performance_mode,
            pull_request_environment_name=pull_request_environment_name,
            pull_request_preview=pull_request_preview,
            skew_protection=skew_protection,
            stage=stage,
        )

        return typing.cast("Branch", jsii.invoke(self, "addBranch", [id, options]))

    @jsii.member(jsii_name="addCustomRule")
    def add_custom_rule(self, rule: CustomRule) -> "App":
        '''(experimental) Adds a custom rewrite/redirect rule to this application.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6783891a6cd7f3088a3bed2c1715b515a14c667057f4628ec4078468d12da60c)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast("App", jsii.invoke(self, "addCustomRule", [rule]))

    @jsii.member(jsii_name="addDomain")
    def add_domain(
        self,
        id: builtins.str,
        *,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> Domain:
        '''(experimental) Adds a domain to this application.

        :param id: -
        :param auto_subdomain_creation_patterns: (experimental) Branches which should automatically create subdomains. Default: - all repository branches ['*', 'pr*']
        :param custom_certificate: (experimental) The type of SSL/TLS certificate to use for your custom domain. Default: - Amplify uses the default certificate that it provisions and manages for you
        :param domain_name: (experimental) The name of the domain. Default: - the construct's id
        :param enable_auto_subdomain: (experimental) Automatically create subdomains for connected branches. Default: false
        :param sub_domains: (experimental) Subdomains. Default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eded460e79858e0488221a5d3720c49b396d004a89444fee1e0b50398d19393)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = DomainOptions(
            auto_subdomain_creation_patterns=auto_subdomain_creation_patterns,
            custom_certificate=custom_certificate,
            domain_name=domain_name,
            enable_auto_subdomain=enable_auto_subdomain,
            sub_domains=sub_domains,
        )

        return typing.cast(Domain, jsii.invoke(self, "addDomain", [id, options]))

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(self, name: builtins.str, value: builtins.str) -> "App":
        '''(experimental) Adds an environment variable to this application.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a51be2fb6676f14c991e00fb755d16c1ced49655e61e9ae209c7cc236cedc927)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("App", jsii.invoke(self, "addEnvironment", [name, value]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''(experimental) The application id.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @builtins.property
    @jsii.member(jsii_name="appName")
    def app_name(self) -> builtins.str:
        '''(experimental) The name of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "appName"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="defaultDomain")
    def default_domain(self) -> builtins.str:
        '''(experimental) The default domain of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "defaultDomain"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="computeRole")
    def compute_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role for an SSR app.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "computeRole"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> typing.Optional[Platform]:
        '''(experimental) The platform of the app.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[Platform], jsii.get(self, "platform"))


@jsii.implements(IBranch)
class Branch(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify-alpha.Branch",
):
    '''(experimental) An Amplify Console branch.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # compute_role: iam.Role
        # amplify_app: amplify.App
        
        
        branch = amplify_app.add_branch("dev", compute_role=compute_role)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app: IApp,
        asset: typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset] = None,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
        compute_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        performance_mode: typing.Optional[builtins.bool] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        skew_protection: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app: (experimental) The application within which the branch must be created.
        :param asset: (experimental) Asset for deployment. The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's startDeployment API to initiate and deploy a S3 asset onto the App. Default: - no asset
        :param auto_build: (experimental) Whether to enable auto building for the branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: (experimental) The name of the branch. Default: - the construct's id
        :param build_spec: (experimental) BuildSpec for the branch. Default: - no build spec
        :param compute_role: (experimental) The IAM role to assign to a branch of an SSR app. The SSR Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions. This role overrides the app-level compute role. Default: undefined - No specific role for the branch. If the app has a compute role, it will be inherited.
        :param description: (experimental) A description for the branch. Default: - no description
        :param environment_variables: (experimental) Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param performance_mode: (experimental) Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out. Default: false
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the branch. Default: true
        :param skew_protection: (experimental) Specifies whether the skew protection feature is enabled for the branch. Deployment skew protection is available to Amplify applications to eliminate version skew issues between client and servers in web applications. When you apply skew protection to a branch, you can ensure that your clients always interact with the correct version of server-side assets, regardless of when a deployment occurs. Default: None - Default setting is no skew protection.
        :param stage: (experimental) Stage for the branch. Default: - no stage

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d9ca053e5c72ede5db7f548cddd267aa4e3612c2ede03b31b18efcb9826978)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BranchProps(
            app=app,
            asset=asset,
            auto_build=auto_build,
            basic_auth=basic_auth,
            branch_name=branch_name,
            build_spec=build_spec,
            compute_role=compute_role,
            description=description,
            environment_variables=environment_variables,
            performance_mode=performance_mode,
            pull_request_environment_name=pull_request_environment_name,
            pull_request_preview=pull_request_preview,
            skew_protection=skew_protection,
            stage=stage,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromBranchName")
    @builtins.classmethod
    def from_branch_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        branch_name: builtins.str,
    ) -> IBranch:
        '''(experimental) Import an existing branch.

        :param scope: -
        :param id: -
        :param branch_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa5ffbe763f20879178517ee1de040b22dd307df63054ff4d34194b83dc836f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
        return typing.cast(IBranch, jsii.sinvoke(cls, "fromBranchName", [scope, id, branch_name]))

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(self, name: builtins.str, value: builtins.str) -> "Branch":
        '''(experimental) Adds an environment variable to this branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3bb818e563fb94e108a4ac51c6856e0f40137143fc5b1abb03be954bc2d372)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("Branch", jsii.invoke(self, "addEnvironment", [name, value]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the branch.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        '''(experimental) The name of the branch.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "branchName"))


@jsii.implements(ISourceCodeProvider)
class CodeCommitSourceCodeProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify-alpha.CodeCommitSourceCodeProvider",
):
    '''(experimental) CodeCommit source code provider.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codecommit as codecommit
        
        
        repository = codecommit.Repository(self, "Repo",
            repository_name="my-repo"
        )
        
        amplify_app = amplify.App(self, "App",
            source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=repository)
        )
    '''

    def __init__(
        self,
        *,
        repository: _aws_cdk_aws_codecommit_ceddda9d.IRepository,
    ) -> None:
        '''
        :param repository: (experimental) The CodeCommit repository.

        :stability: experimental
        '''
        props = CodeCommitSourceCodeProviderProps(repository=repository)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, app: App) -> SourceCodeProviderConfig:
        '''(experimental) Binds the source code provider to an app.

        :param app: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b2e5a130d115ac93f5dc1c7a49d85af09f80db57b20a2c3aacf0df76ee411f)
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
        return typing.cast(SourceCodeProviderConfig, jsii.invoke(self, "bind", [app]))


@jsii.implements(ISourceCodeProvider)
class GitHubSourceCodeProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify-alpha.GitHubSourceCodeProvider",
):
    '''(experimental) GitHub source code provider.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "App",
            source_code_provider=amplify.GitHubSourceCodeProvider(
                owner="<user>",
                repository="<repo>",
                oauth_token=SecretValue.secrets_manager("my-github-token")
            ),
            custom_response_headers=[amplify.CustomResponseHeader(
                pattern="*.json",
                headers={
                    "custom-header-name-1": "custom-header-value-1",
                    "custom-header-name-2": "custom-header-value-2"
                }
            ), amplify.CustomResponseHeader(
                pattern="/path/*",
                headers={
                    "custom-header-name-1": "custom-header-value-2"
                }
            )
            ]
        )
    '''

    def __init__(
        self,
        *,
        oauth_token: _aws_cdk_ceddda9d.SecretValue,
        owner: builtins.str,
        repository: builtins.str,
    ) -> None:
        '''
        :param oauth_token: (experimental) A personal access token with the ``repo`` scope.
        :param owner: (experimental) The user or organization owning the repository.
        :param repository: (experimental) The name of the repository.

        :stability: experimental
        '''
        props = GitHubSourceCodeProviderProps(
            oauth_token=oauth_token, owner=owner, repository=repository
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _app: App) -> SourceCodeProviderConfig:
        '''(experimental) Binds the source code provider to an app.

        :param _app: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95bb551e0bd0c5908f812aa7521905b367f553a81d84e74c14963deac202e989)
            check_type(argname="argument _app", value=_app, expected_type=type_hints["_app"])
        return typing.cast(SourceCodeProviderConfig, jsii.invoke(self, "bind", [_app]))


@jsii.implements(ISourceCodeProvider)
class GitLabSourceCodeProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-amplify-alpha.GitLabSourceCodeProvider",
):
    '''(experimental) GitLab source code provider.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            source_code_provider=amplify.GitLabSourceCodeProvider(
                owner="<user>",
                repository="<repo>",
                oauth_token=SecretValue.secrets_manager("my-gitlab-token")
            )
        )
    '''

    def __init__(
        self,
        *,
        oauth_token: _aws_cdk_ceddda9d.SecretValue,
        owner: builtins.str,
        repository: builtins.str,
    ) -> None:
        '''
        :param oauth_token: (experimental) A personal access token with the ``repo`` scope.
        :param owner: (experimental) The user or organization owning the repository.
        :param repository: (experimental) The name of the repository.

        :stability: experimental
        '''
        props = GitLabSourceCodeProviderProps(
            oauth_token=oauth_token, owner=owner, repository=repository
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _app: App) -> SourceCodeProviderConfig:
        '''(experimental) Binds the source code provider to an app.

        :param _app: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29dad1f763523380f6a67ed0ae532ec1546e13d4d89b8aa9148ee6c401326b7d)
            check_type(argname="argument _app", value=_app, expected_type=type_hints["_app"])
        return typing.cast(SourceCodeProviderConfig, jsii.invoke(self, "bind", [_app]))


__all__ = [
    "App",
    "AppProps",
    "AutoBranchCreation",
    "BasicAuth",
    "BasicAuthConfig",
    "BasicAuthProps",
    "Branch",
    "BranchOptions",
    "BranchProps",
    "CacheConfigType",
    "CodeCommitSourceCodeProvider",
    "CodeCommitSourceCodeProviderProps",
    "CustomResponseHeader",
    "CustomRule",
    "CustomRuleOptions",
    "Domain",
    "DomainOptions",
    "DomainProps",
    "GitHubSourceCodeProvider",
    "GitHubSourceCodeProviderProps",
    "GitLabSourceCodeProvider",
    "GitLabSourceCodeProviderProps",
    "IApp",
    "IBranch",
    "ISourceCodeProvider",
    "Platform",
    "RedirectStatus",
    "SourceCodeProviderConfig",
    "SubDomain",
]

publication.publish()

def _typecheckingstub__00fae34ad2733a382bf4bd9703c470687ee286b909acac7113a890be0a23b881(
    *,
    app_name: typing.Optional[builtins.str] = None,
    auto_branch_creation: typing.Optional[typing.Union[AutoBranchCreation, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_branch_deletion: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
    cache_config_type: typing.Optional[CacheConfigType] = None,
    compute_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    custom_response_headers: typing.Optional[typing.Sequence[typing.Union[CustomResponseHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_rules: typing.Optional[typing.Sequence[CustomRule]] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    platform: typing.Optional[Platform] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    source_code_provider: typing.Optional[ISourceCodeProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f2af0e4edaf98f48a3180a7128a09045875ec0261dce3f9482c947bcbaae487(
    *,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb61d9465b046820e4be734cff063bd1c7fefa32eea9bb8808c12336571c6dc3(
    username: builtins.str,
    password: _aws_cdk_ceddda9d.SecretValue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f366513def1e04612e697b08e7c8224a644a15e7253569d6b718c02c3b943d4(
    username: builtins.str,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a575491ebde5fe3bfc9e69f32ef44ff1ba5507b5e749645203007fb5fe4214ec(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa4e34249a276be45cee21e775f03f7d1e7897d6d161907ebd2793f00e4409a(
    *,
    enable_basic_auth: builtins.bool,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3809f6d0ef297fe501ad051e76013b357eb7facbc26fe8936330556c35d4dc74(
    *,
    username: builtins.str,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    password: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b000a0021ff86c948a7f1d5b6d9915b3dd9424861178bf3ab8c784feb250caeb(
    *,
    asset: typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset] = None,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
    compute_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    performance_mode: typing.Optional[builtins.bool] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    skew_protection: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529d2fd3c9613ce4eb269675040b4e50e2005444ff5b8d0f0cf4702adf37c2da(
    *,
    asset: typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset] = None,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
    compute_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    performance_mode: typing.Optional[builtins.bool] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    skew_protection: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
    app: IApp,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa2a223f4d92f511cf4841627ec77cbadb81380423b16782bcb854435bab9a3c(
    *,
    repository: _aws_cdk_aws_codecommit_ceddda9d.IRepository,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c1962999fedf4ca1e171bdd7613e146d33a972f8a3275a1c82cf2d83ee1b3d(
    *,
    headers: typing.Mapping[builtins.str, builtins.str],
    pattern: builtins.str,
    app_root: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716b401b2530f2ea497b885540df3538442041316ceef4d35cbbdb92fa7c627d(
    *,
    source: builtins.str,
    target: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    status: typing.Optional[RedirectStatus] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e333b720149581cace67c91dbe1444026f7810389a4b7e045740c2cc6daec4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app: IApp,
    auto_sub_domain_iam_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c869e76fd73bca8b756321422ccc73fc84cda2d048155aaa02c2be3ca35b44b(
    branch: IBranch,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa160eb48a0fec188e680884a7d6535fc2cc3d4e1b98f3dea06a760deb6186c4(
    branch: IBranch,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c320927402b9dc876549f614a833ea8c346cc42aadbbe883e3d2646c5dd361ff(
    *,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bcc4553ef04f08c67c00e5ca845c349b18cd93f97e022c79c4b74ef6e4b08c4(
    *,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
    app: IApp,
    auto_sub_domain_iam_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a971b7d216fe8bfb4bdd8a433546879b4d66a8bf5db40ad1bec42594688a780b(
    *,
    oauth_token: _aws_cdk_ceddda9d.SecretValue,
    owner: builtins.str,
    repository: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a410ebec7c5d44edc4b31cd124a785c4320c6fc00e5255e7e368cb8c5a23a054(
    *,
    oauth_token: _aws_cdk_ceddda9d.SecretValue,
    owner: builtins.str,
    repository: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827844675225f813772a868238ca8ec0955c868d8d638a34104a2a053abc8b6b(
    app: App,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac2e4799ab05086079fd0209d56fa5d22cdc005ae42195d771cdce9310ea40d(
    *,
    repository: builtins.str,
    access_token: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    oauth_token: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6446d0b441d64cdc5587fba11548aaa739970869298a998c56e521c703c189(
    *,
    branch: IBranch,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb3fdecad4b351bd290c8a9d65c70964afb63130c3af329024642f751e1c88d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_name: typing.Optional[builtins.str] = None,
    auto_branch_creation: typing.Optional[typing.Union[AutoBranchCreation, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_branch_deletion: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
    cache_config_type: typing.Optional[CacheConfigType] = None,
    compute_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    custom_response_headers: typing.Optional[typing.Sequence[typing.Union[CustomResponseHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_rules: typing.Optional[typing.Sequence[CustomRule]] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    platform: typing.Optional[Platform] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    source_code_provider: typing.Optional[ISourceCodeProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f336cf0eaa13206e537622709ef647bef74d888dac99cd443461cc4455f954(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    app_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4175887e8f0238227347c352129f3e79394976ffce631cfdc2d4a9f0f90bd6(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2df726a9de1c19f40cb6ef900a079002cd8f15beecdff87621764c6d7dd0531(
    id: builtins.str,
    *,
    asset: typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset] = None,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
    compute_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    performance_mode: typing.Optional[builtins.bool] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    skew_protection: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6783891a6cd7f3088a3bed2c1715b515a14c667057f4628ec4078468d12da60c(
    rule: CustomRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eded460e79858e0488221a5d3720c49b396d004a89444fee1e0b50398d19393(
    id: builtins.str,
    *,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51be2fb6676f14c991e00fb755d16c1ced49655e61e9ae209c7cc236cedc927(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d9ca053e5c72ede5db7f548cddd267aa4e3612c2ede03b31b18efcb9826978(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app: IApp,
    asset: typing.Optional[_aws_cdk_aws_s3_assets_ceddda9d.Asset] = None,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.BuildSpec] = None,
    compute_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    performance_mode: typing.Optional[builtins.bool] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    skew_protection: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa5ffbe763f20879178517ee1de040b22dd307df63054ff4d34194b83dc836f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    branch_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3bb818e563fb94e108a4ac51c6856e0f40137143fc5b1abb03be954bc2d372(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b2e5a130d115ac93f5dc1c7a49d85af09f80db57b20a2c3aacf0df76ee411f(
    app: App,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95bb551e0bd0c5908f812aa7521905b367f553a81d84e74c14963deac202e989(
    _app: App,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29dad1f763523380f6a67ed0ae532ec1546e13d4d89b8aa9148ee6c401326b7d(
    _app: App,
) -> None:
    """Type checking stubs"""
    pass
